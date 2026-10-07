"""Tests for the Operator Sandbox.

Three layers, matching the plan's strategy (§8):

  * unit        -- each operator's pure behaviour, including the hard failures
  * boundary    -- the import surface (no State writes outside COMMIT, no
                   `macha.*`, no Kotlin/Gradle artefacts, no third-party deps)
  * integration -- E-S1's key trace subsequence, the control run, and trace-hash
                   determinism

The determinism test is deliberately marked as the thing to cut first when
time is short (§12.2): it is not a precondition for E-S1's conclusion.
"""

from __future__ import annotations

import ast
import json
import os
import pathlib
import subprocess
import sys

import pytest

HERE = pathlib.Path(__file__).parent.resolve()
sys.path.insert(0, str(HERE))

import metrics as metrics_mod  # noqa: E402
import scenarios  # noqa: E402
from model import SandboxError, UnitStore  # noqa: E402
from program import OperatorCall, Sandbox, run_program  # noqa: E402
from state import State  # noqa: E402
from workspace import open_workspace  # noqa: E402

ALLOWED_STDLIB = {
    "argparse", "ast", "dataclasses", "hashlib", "json", "os", "pathlib",
    "subprocess", "sys", "typing", "__future__",
}
# pytest is the project's existing dev dependency, not something the sandbox
# introduced; it is only allowed in the test module.
ALLOWED_TEST_ONLY = {"pytest"}
LOCAL_MODULES = {
    "model", "workspace", "state", "trace", "metrics", "operators",
    "program", "scenarios", "run_experiment", "test_sandbox",
}


def _fresh() -> Sandbox:
    sb = Sandbox(providers=scenarios.common_providers())
    sb.seed = "const"
    return sb


# ---------------------------------------------------------------------------
# unit
# ---------------------------------------------------------------------------


def test_select_adds_no_unit():
    """SELECT's answer to 'does selection produce information?' is no (plan §4.2)."""
    sb = _fresh()
    ws = sb.open("t-1")
    ws.seed([scenarios.I1_TEXT])
    before = set(sb.store.units)
    sb.run(ws, [OperatorCall(op="SELECT", params={"source": "workspace"})])
    assert set(sb.store.units) == before
    assert ws.focus == ["u0001"]


def test_transform_derives_unit_that_traces_back():
    sb = _fresh()
    ws = sb.open("t-1")
    ws.seed([scenarios.I1_TEXT])
    sb.run(ws, [
        OperatorCall(op="TRANSFORM", params={"transform_name": "normalize"},
                     input_refs=["u0001"]),
    ])
    new = sb.store.get("u0002")
    assert new.origin == "derived"
    assert new.refs == ("u0001",)          # fidelity criterion: traceable back
    assert new.payload["action"] == "take"


def test_commit_is_the_only_state_writer():
    sb = _fresh()
    ws = sb.open("t-1")
    ws.seed([scenarios.I1_TEXT])
    sb.run(ws, [
        OperatorCall(op="TRANSFORM", params={"transform_name": "normalize"},
                     input_refs=["u0001"]),
        OperatorCall(op="COMMIT", params={"key": "events/x"},
                     input_refs=["last:TRANSFORM"]),
    ])
    assert sb.state.version == 1
    writers = {
        r["op"] for r in sb.tracer.rows
        if r["state_version_after"] > r["state_version_before"]
    }
    assert writers == {"COMMIT"}


def test_commit_refuses_to_guess_from_focus():
    """Regression: the first control run committed the raw sentence, because
    resolve() fell back to focus. COMMIT must name its units explicitly."""
    sb = _fresh()
    ws = sb.open("t-1")
    ws.seed([scenarios.I1_TEXT])
    with pytest.raises(SandboxError, match="explicit input_refs"):
        sb.run(ws, [
            OperatorCall(op="SELECT", params={"source": "workspace"}),
            OperatorCall(op="COMMIT", params={"key": "events/x"}),
        ])


@pytest.mark.parametrize(
    "call,match",
    [
        (OperatorCall(op="TRANSFORM", params={}, input_refs=["u0001"]),
         "transform_name"),
        (OperatorCall(op="COMMIT", params={"input_refs": ["u0001"]}), "params.key"),
        (OperatorCall(op="COMMIT", params={"key": "k", "state": "x"},
                      input_refs=["u0001"]),
         "does not decide what is worth remembering"),
        (OperatorCall(op="SELECT", params={"source": "nowhere"}), "unknown SELECT source"),
        (OperatorCall(op="NOPE", params={}), "unknown operator"),
    ],
)
def test_hard_failure_never_silent(call, match):
    """A silent no-op would make the trace lie (plan §5)."""
    sb = _fresh()
    ws = sb.open("t-1")
    ws.seed([scenarios.I1_TEXT])
    with pytest.raises(SandboxError, match=match):
        sb.run(ws, [call])
    assert sb.tracer.rows[-1]["status"] == "failed"
    assert ws.status == "failed"


def test_unknown_provider_is_a_hard_failure():
    sb = _fresh()
    ws = sb.open("t-1")
    ws.seed([scenarios.I1_TEXT])
    with pytest.raises(SandboxError, match="unknown provider"):
        sb.run(ws, [
            OperatorCall(op="TRANSFORM", params={"transform_name": "nope"},
                         input_refs=["u0001"]),
        ])


def test_normalize_is_generic_not_scenario_specific():
    """R4 guard: the provider must not contain a branch on the scene."""
    src = (HERE / "operators.py").read_text(encoding="utf-8")
    assert 'if scenario' not in src
    out = scenarios.normalize(
        _mk_unit("他把火把放下了")
    )
    assert out["action"] == "put_down"
    assert out["object"] == "torch"


def _mk_unit(text: str):
    from model import Unit

    return Unit(id="uX", payload=text, origin="external", created_by=None,
                refs=(), logical_ts=0)


def test_state_is_append_only():
    st = State()
    st.append("a", "u0001", "t", "op1")
    st.append("a", "u0002", "t", "op2")
    assert st.version == 2
    assert [e.unit_id for e in st.entries] == ["u0001", "u0002"]
    assert st.view().select("a") == ("u0001", "u0002")


def test_closed_thread_is_invisible_to_the_next_one():
    """The temporary/persistent boundary, in one assertion."""
    sb = _fresh()
    run_program(sb, "t-A", scenarios.prog_thread_a(), seed_payloads=[scenarios.I1_TEXT])
    ws_b = sb.open("t-B")
    assert ws_b.unit_ids() == []
    sb.run(ws_b, scenarios.prog_thread_b())
    assert ws_b.focus == ["u0002"]


# ---------------------------------------------------------------------------
# boundary
# ---------------------------------------------------------------------------


def _imports(path: pathlib.Path) -> set:
    tree = ast.parse(path.read_text(encoding="utf-8"))
    names = set()
    for node in ast.walk(tree):
        if isinstance(node, ast.Import):
            for a in node.names:
                names.add(a.name.split(".")[0])
        elif isinstance(node, ast.ImportFrom) and node.module and node.level == 0:
            names.add(node.module.split(".")[0])
    return names


def test_no_third_party_imports():
    for py in sorted(HERE.glob("*.py")):
        extra = _imports(py) - ALLOWED_STDLIB - LOCAL_MODULES
        if py.name == "test_sandbox.py":
            extra -= ALLOWED_TEST_ONLY
        assert not extra, "%s imports %s" % (py.name, sorted(extra))


def test_no_macha_or_gradle_coupling():
    """V1 / V3: the sandbox must not touch src/macha or layers/.

    The test module is excluded -- it names those paths in order to forbid them.
    """
    for py in sorted(HERE.glob("*.py")):
        if py.name == "test_sandbox.py":
            continue
        names = _imports(py)
        assert "macha" not in names
        text = py.read_text(encoding="utf-8")
        assert "layers/" not in text
        assert "gradle" not in text.lower()


def test_state_write_is_confined_to_the_runner():
    """`State.append` must be called from exactly one place, and that place is
    the runner -- not any operator (plan §5 write-permission guard)."""
    callers = []
    for py in sorted(HERE.glob("*.py")):
        tree = ast.parse(py.read_text(encoding="utf-8"))
        for node in ast.walk(tree):
            if not (isinstance(node, ast.Call)
                    and isinstance(node.func, ast.Attribute)):
                continue
            if node.func.attr != "append":
                continue
            target = node.func.value
            # matches both `state.append(...)` and `self.state.append(...)`
            if isinstance(target, ast.Name) and target.id == "state":
                callers.append(py.name)
            elif isinstance(target, ast.Attribute) and target.attr == "state":
                callers.append(py.name)
    assert set(callers) == {"program.py"}, callers


def test_operators_module_holds_no_state_object():
    src = (HERE / "operators.py").read_text(encoding="utf-8")
    assert "State(" not in src
    assert "state.append" not in src


def test_trace_field_set_is_frozen():
    from trace import FIELDS

    assert len(FIELDS) == len(set(FIELDS))
    assert "model" not in FIELDS  # v1 has no model; the slot stays unused
    sb, _ = scenarios.run_prog()
    for row in sb.tracer.rows:
        assert set(row) == set(FIELDS)


# ---------------------------------------------------------------------------
# integration -- E-S1
# ---------------------------------------------------------------------------


def test_exp1_prog_trace_shape():
    """Assert on the key subsequence, not the whole file (brittle-test rule)."""
    sb, extra = scenarios.run_prog()
    rows = sb.tracer.subseq(["SELECT", "TRANSFORM", "COMMIT", "SELECT"])
    assert [r["op"] for r in rows] == ["SELECT", "TRANSFORM", "COMMIT", "SELECT"]
    assert rows[0]["output_refs"] == ["u0001"]
    assert rows[1]["provider"] == "normalize"
    assert rows[2]["state_version_after"] == 1
    assert rows[3]["thread"] == "t-B"
    assert extra["thread_b_focus"] == ["u0002"]


def test_exp1_thread_b_never_re_ingested_the_input():
    """E-S1's expected capability: B retrieves without seeing I1 again."""
    sb, _ = scenarios.run_prog()
    b_rows = [r for r in sb.tracer.rows if r["thread"] == "t-B"]
    assert len(b_rows) == 1
    assert b_rows[0]["input_refs"] == []
    assert sb.store.get("u0001").origin == "external"


def test_exp1_only_commit_touches_state():
    sb, _ = scenarios.run_prog()
    for r in sb.tracer.rows:
        if r["op"] != "COMMIT":
            assert r["state_version_before"] == r["state_version_after"]


def test_control_terminal_states_match():
    """If the two arms end differently, the control is not a control."""
    prog, _ = scenarios.run_prog()
    mono, _ = scenarios.run_mono()
    assert scenarios.state_signature(prog) == scenarios.state_signature(mono)


def test_control_cannot_name_the_step_that_changed_state():
    """H-B's discriminator, as pre-registered: attributable_changes must be
    greater on prog than on mono."""
    prog, _ = scenarios.run_prog()
    mono, _ = scenarios.run_mono()
    pm = metrics_mod.compute_metrics(prog.tracer.rows)
    mm = metrics_mod.compute_metrics(mono.tracer.rows)
    assert pm["attributable_changes"] > 1
    assert mm["attributable_changes"] == 1
    assert pm["intermediate_units"] > 0
    assert mm["intermediate_units"] == 0


def test_metrics_are_mechanically_computable():
    sb, _ = scenarios.run_prog()
    m = metrics_mod.compute_metrics(sb.tracer.rows)
    assert m["unmapped_steps"] == 0
    assert m["total_steps"] == len(sb.tracer.rows)
    assert m["reuse"] is None  # first run: nothing to compare against


def test_committed_trace_on_disk_matches_a_fresh_run():
    """The committed evidence must be reproducible, not stale."""
    sb, _ = scenarios.run_prog()
    on_disk = [
        json.loads(line)
        for line in (HERE / "runs" / "exp1" / "prog" / "trace.jsonl")
        .read_text(encoding="utf-8").splitlines()
        if line.strip()
    ]
    assert on_disk == sb.tracer.rows


# ---------------------------------------------------------------------------
# determinism (cut first when short on time -- plan §12.2)
# ---------------------------------------------------------------------------


def test_same_input_same_trace_hash():
    a, _ = scenarios.run_prog()
    b, _ = scenarios.run_prog()
    assert a.tracer.trace_hash() == b.tracer.trace_hash()


def test_hash_survives_a_fresh_interpreter():
    """Guards against dict/set iteration order leaking into the trace."""
    env = dict(os.environ, PYTHONHASHSEED="12345")
    code = (
        "import sys; sys.path.insert(0, %r);"
        "import scenarios; sb,_ = scenarios.run_prog();"
        "print(sb.tracer.trace_hash())" % str(HERE)
    )
    out = subprocess.run(
        [sys.executable, "-c", code], capture_output=True, text=True, env=env,
    )
    assert out.returncode == 0, out.stderr
    sb, _ = scenarios.run_prog()
    assert out.stdout.strip() == sb.tracer.trace_hash()
