"""The three operators E-S1 needs: SELECT, TRANSFORM, COMMIT.

DELIBERATELY not all five (plan §12.2: the answer is "three plus two", and
RELATE's existence is itself a risk -- U2/D10 says it may need deleting). Exp1
only needs these three; RELATE and TEST arrive with Exp2/Exp3 and only if those
experiments fail to be expressible without them.

Shared semantics live here once (input view + explicit input_refs + params;
return OpResult; only COMMIT may mutate State; the runner writes the trace, not
the operator -- plan §4.1). What is left per-operator is how it reads params,
how it picks or builds units, and which provider it uses.
"""

from __future__ import annotations

from typing import Callable, Optional

from model import (
    ORIGIN_DERIVED,
    STATUS_OK,
    ExecContext,
    OpResult,
    SandboxError,
    Unit,
)
from state import ReadOnlyState
from workspace import Workspace, resolve

# ---------------------------------------------------------------------------
# Provider seam
# ---------------------------------------------------------------------------
# Core defines the transformation SEMANTICS; it does not embed an LLM. The
# implementation is a deterministic pure function registered by the scenario
# (plan §4.4). This is a seam for determinism, not a seam for a model: no
# prompt, no context window, no token budget is reserved anywhere.
#
# Providers live on the Sandbox instance, not in a module global. A global
# registry made a second run in the same process fail with "provider already
# registered" -- the seam is a per-run dependency, and keeping it global would
# also have let one experiment's provider leak into another's trace.

Provider = Callable[[Unit], dict]


def get_provider(providers: dict, name: str) -> Provider:
    if name not in providers:
        raise SandboxError("unknown provider: %s" % name)
    return providers[name]


# ---------------------------------------------------------------------------
# SELECT
# ---------------------------------------------------------------------------
# v1 duty: pick units by a DECLARED criterion and write them to focus.
# The core question it answers: does selection produce new information? v1's
# answer is "no" -- it only changes focus, it adds no unit. That is testable:
# in E-S1's trace, every SELECT output_ref must point at an id that already
# existed (plan §4.2).
#
# Not doing: embeddings, vector retrieval, relevance scoring, LLM judgement.


def op_select(
    ws: Workspace,
    ctx: ExecContext,
    params: dict,
    state_ro: ReadOnlyState,
    providers: Optional[dict] = None,
) -> tuple[OpResult, list]:
    source = params.get("source", "workspace")

    if source == "workspace":
        cands = [ws.get(uid) for uid in ws.unit_ids()]
    elif source == "state":
        # Cross-thread retrieval. The key criterion is declarative; the unit
        # payload is re-materialised into this Thread's working set so it can be
        # used without re-ingesting the original input.
        key_prefix = params.get("key_prefix")
        unit_ids = ws.visible_from_state(state_ro.select(key_prefix))
        cands = [ws.get(uid) for uid in unit_ids]
    else:
        raise SandboxError("unknown SELECT source: %s" % source)

    kind = params.get("kind")
    if kind is not None:
        cands = [u for u in cands if isinstance(u.payload, dict) and u.payload.get("kind") == kind]
    origin = params.get("origin")
    if origin is not None:
        cands = [u for u in cands if u.origin == origin]
    explicit = params.get("ids")
    if explicit is not None:
        wanted = set(explicit)
        cands = [u for u in cands if u.id in wanted]

    # Focus changes: visible range changes, content does not (operator-space §3.1).
    before = list(ws.focus)
    ws.set_focus([u.id for u in cands])
    note = "focus %s -> %s" % (before or "[]", ws.focus or "[]")
    return OpResult(output_refs=tuple(ws.focus), status=STATUS_OK, note=note), []


# ---------------------------------------------------------------------------
# TRANSFORM
# ---------------------------------------------------------------------------
# v1 duty: change a unit's representation / abstraction level. The new unit's
# refs point at the input, so "is it still the same thing?" has a checkable
# answer -- traceability back (plan §4.4). Fidelity criterion = traceable back.


def op_transform(
    ws: Workspace,
    ctx: ExecContext,
    params: dict,
    state_ro: ReadOnlyState,
    providers: Optional[dict] = None,
) -> tuple[OpResult, list]:
    transform_name = params.get("transform_name")
    if not transform_name:
        raise SandboxError("TRANSFORM requires params.transform_name")
    fn = get_provider(providers or {}, transform_name)

    units = resolve(ws, params.get("input_refs"), params)
    if not units:
        raise SandboxError("TRANSFORM has no input units")

    out_ids = []
    for unit in units:
        payload = fn(unit)
        if not isinstance(payload, dict):
            raise SandboxError("provider %s must return a dict" % transform_name)
        new = Unit(
            id=ws.store.allocate_id(),
            payload=payload,
            origin=ORIGIN_DERIVED,
            created_by=ctx.op_id,
            refs=(unit.id,),
            logical_ts=ctx.logical_ts,
        )
        ws.add_derived(new)
        out_ids.append(new.id)

    return (
        OpResult(
            output_refs=tuple(out_ids),
            status=STATUS_OK,
            note="transform=%s refs=%s" % (transform_name, [u.id for u in units]),
        ),
        [],
    )


# ---------------------------------------------------------------------------
# COMMIT
# ---------------------------------------------------------------------------
# The only primitive allowed to change persistent state (plan §4.6).
#
# It does NOT decide what is worth remembering -- it only performs the mutation.
# No dedup, no importance scoring, no summarisation, no forgetting. If any of
# those appear as parameters, State has become Memory (plan §12.1 R6).


def op_commit(
    ws: Workspace,
    ctx: ExecContext,
    params: dict,
    state_ro: ReadOnlyState,
    providers: Optional[dict] = None,
) -> tuple[OpResult, list]:
    if "state" in params:
        raise SandboxError("COMMIT does not decide what is worth remembering")

    key = params.get("key")
    if not key:
        raise SandboxError("COMMIT requires params.key")

    # COMMIT writes EXPLICITLY named units (plan §4.6). No fallback to focus:
    # focus still holds whatever SELECT chose, so silently committing that
    # instead of the transform's output is the exact bug the first control run
    # exposed -- the two arms disagreed on terminal state.
    call_refs = params.get("input_refs")
    if not call_refs:
        raise SandboxError(
            "COMMIT requires explicit input_refs; it will not guess from focus"
        )
    units = resolve(ws, call_refs, params)
    if not units:
        raise SandboxError("COMMIT has no input units")

    # The operator declares the intent to write; the runner performs it. That
    # split is what makes the boundary guard checkable: no module under
    # operators.py ever holds a reference to State's write function.
    writes = [(key, u.id) for u in units]
    return (
        OpResult(
            output_refs=tuple(u.id for u in units),
            status=STATUS_OK,
            note="key=%s units=%s" % (key, [u.id for u in units]),
        ),
        writes,
    )


REGISTRY: dict[str, Callable] = {
    "SELECT": op_select,
    "TRANSFORM": op_transform,
    "COMMIT": op_commit,
}
