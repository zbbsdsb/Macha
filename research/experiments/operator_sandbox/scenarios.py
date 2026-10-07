"""E-S1 (Continuity) and its `mono` control.

Scene (from operator-space.md §11.1, unchanged so the two documents corroborate
each other): the player takes something out of a chest, leaves, and comes back a
long time later. The one thing the NPC must be able to do is remember that it
knew.

I1 = "玩家拿走了箱子里的东西"

  prog, Thread A: SELECT -> TRANSFORM(normalize) -> COMMIT, then close
  prog, Thread B: **seed nothing**, SELECT(state) -> close
  mono, Thread A: one opaque step that produces the same State
  mono, Thread B: one opaque step that reads the same State

`mono` is a CONTROL, not a lazy path and not a failure path. It is the equally
rigorous "equivalent implementation without decomposition" written by the same
person at the same time. Without it, "decomposition is necessary" has no
detector -- and the whole point of the control is that if `prog` cannot say
WHICH step caused a change, it is no better than `mono` (plan §7.0a).
"""

from __future__ import annotations

import json
from typing import Any, Optional

from model import (
    STATUS_OK,
    ExecContext,
    OpResult,
    SandboxError,
    Unit,
)
from program import OperatorCall, Sandbox, run_program
from state import ReadOnlyState
from workspace import Workspace

I1_TEXT = "玩家拿走了箱子里的东西"

# ---------------------------------------------------------------------------
# Providers. Named, generic, reusable -- a comparator that reads
# `if scenario == "exp3"` is the scenario doing the operator's job (plan §12.1 R4).
# ---------------------------------------------------------------------------

# A declared verb lexicon, not a hand-written answer for I1. The same provider
# serves E-S1 through E-S3; a payload it cannot parse comes back as
# {"kind": "opaque", "text": ...} rather than being guessed at.
VERB_LEXICON: tuple[tuple[str, str], ...] = (
    ("拿走", "take"),
    ("偷走", "take"),
    ("还了", "return"),
    ("还回", "return"),
    ("放下", "put_down"),
    ("破坏", "destroy"),
    ("杀", "kill"),
)

OBJECT_LEXICON: tuple[tuple[str, str], ...] = (
    ("箱子里的东西", "chest_contents"),
    ("箱子", "chest"),
    ("火把", "torch"),
)


def _match_lexicon(text: str, lexicon) -> tuple[str, str]:
    """Longest-match, deterministic. Sorted so ties resolve the same way every run."""
    best = None
    for surface, canonical in sorted(lexicon, key=lambda kv: (-len(kv[0]), kv[0])):
        if surface in text:
            best = (surface, canonical)
            break
    return best if best else ("", "")


def normalize(unit: Unit) -> dict:
    """String -> structured dict. Deterministic, no model, no scoring."""
    text = unit.payload if isinstance(unit.payload, str) else str(unit.payload)
    _, action = _match_lexicon(text, VERB_LEXICON)
    _, obj = _match_lexicon(text, OBJECT_LEXICON)
    if not action and not obj:
        return {"kind": "opaque", "text": text}
    out: dict[str, Any] = {"kind": "event"}
    if action:
        out["action"] = action
    if obj:
        out["object"] = obj
    out["source_text"] = text
    return out


def common_providers() -> dict:
    """Built fresh per run, so one experiment cannot leak into another's trace."""
    return {"normalize": normalize}


# ---------------------------------------------------------------------------
# The opaque control step. Not a candidate operator: it exists so the control is
# an honest equivalent implementation, and it is named to make that obvious in
# the trace.
# ---------------------------------------------------------------------------


def monolith(
    ws: Workspace,
    ctx: ExecContext,
    params: dict,
    state_ro: ReadOnlyState,
    providers: Optional[dict] = None,
) -> tuple[OpResult, list]:
    mode = params.get("mode")
    if mode == "process":
        ids = ws.seed([I1_TEXT])
        unit = ws.get(ids[0])
        payload = normalize(unit)
        new = Unit(
            id=ws.store.allocate_id(),
            payload=payload,
            origin="derived",
            created_by=ctx.op_id,
            refs=(unit.id,),
            logical_ts=ctx.logical_ts,
        )
        ws.add_derived(new)
        return (
            OpResult(
                output_refs=(new.id,),
                status=STATUS_OK,
                note="did everything: take in, restructure, remember",
            ),
            [("events/player_took_item", new.id)],
        )
    if mode == "recall":
        got = ws.visible_from_state(state_ro.select("events/"))
        ws.set_focus(list(got))
        return (
            OpResult(
                output_refs=tuple(got),
                status=STATUS_OK,
                note="did everything: fetch what was remembered",
            ),
            [],
        )
    raise SandboxError("unknown monolith mode: %s" % mode)


MONO_REGISTRY = {"MONOLITH": monolith}


# ---------------------------------------------------------------------------
# Programs
# ---------------------------------------------------------------------------

KEY_EVENTS = "events/player_took_item"


def prog_thread_a() -> list[OperatorCall]:
    return [
        OperatorCall(
            op="SELECT",
            params={"source": "workspace", "kind": None},
            why="look at what just came in",
        ),
        OperatorCall(
            op="TRANSFORM",
            params={"transform_name": "normalize"},
            why="turn the sentence into something comparable",
        ),
        OperatorCall(
            op="COMMIT",
            params={"key": KEY_EVENTS},
            input_refs=["last:TRANSFORM"],
            why="make the structured version survive this Thread closing",
        ),
    ]


def prog_thread_b() -> list[OperatorCall]:
    return [
        OperatorCall(
            op="SELECT",
            params={"source": "state", "key_prefix": "events/"},
            why="much later: find out what I knew, without seeing it again",
        ),
    ]


def mono_thread_a() -> list[OperatorCall]:
    return [
        OperatorCall(
            op="MONOLITH",
            params={"mode": "process"},
            why="control: same in, same out, no decomposition",
        ),
    ]


def mono_thread_b() -> list[OperatorCall]:
    return [
        OperatorCall(
            op="MONOLITH",
            params={"mode": "recall"},
            why="control: same read, no decomposition",
        ),
    ]


# ---------------------------------------------------------------------------
# Runner entry points
# ---------------------------------------------------------------------------


def run_prog() -> tuple[Sandbox, dict]:
    sb = Sandbox(providers=common_providers())
    sb.seed = "const"

    ws_a = run_program(sb, "t-A", prog_thread_a(), seed_payloads=[I1_TEXT])
    assert ws_a.status == "committed"
    # Thread B seeds nothing. If B can still retrieve, retrieval did not depend
    # on re-ingesting I1 -- that is E-S1's expected capability.
    ws_b = run_program(sb, "t-B", prog_thread_b(), open_only=True)
    focus_b = list(ws_b.focus)
    sb.close(ws_b)

    return sb, {"thread_b_focus": focus_b}


def run_mono() -> tuple[Sandbox, dict]:
    sb = Sandbox(registry=dict(MONO_REGISTRY))
    sb.seed = "const"

    ws_a = run_program(sb, "t-A", mono_thread_a(), seed_payloads=[I1_TEXT])
    ws_b = run_program(sb, "t-B", mono_thread_b(), open_only=True)
    focus_b = list(ws_b.focus)
    sb.close(ws_b)

    return sb, {"thread_b_focus": focus_b}


def state_signature(sb: Sandbox) -> list:
    """Terminal state, compared across the two arms.

    Keyed by state key and compared on PAYLOAD, not on unit id: the two arms
    allocate ids in a different order (mono folds intake into its single step),
    so an id-wise comparison would report a difference that is not one. This
    definition is stated here rather than discovered during comparison.
    """
    out = []
    for entry in sorted(sb.state.entries, key=lambda e: e.key):
        unit = sb.store.units.get(entry.unit_id)
        payload = unit.payload if unit is not None else None
        out.append((entry.key, _canonical(payload)))
    return out


def _canonical(value) -> str:
    return json.dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
