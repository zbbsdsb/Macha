"""Linear program runner.

A program is a flat list of OperatorCall. No DSL, no grammar, no parser, no file
format (plan §5). No branches, no loops -- if an experiment needs a conditional
("only go this way if TEST says conflict"), that gets recorded as a FINDING
about linear programs being insufficient, not patched on the spot.

The runner owns the trace, not the operators: one writer means the row shape
cannot fork per operator (plan §4.1). It also owns the State write, so no
operator module ever holds a reference to State's write function.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Callable, Optional

from model import (
    STATUS_FAILED,
    STATUS_OK,
    ExecContext,
    OpResult,
    SandboxError,
    UnitStore,
)
from operators import REGISTRY
from state import State
from trace import Tracer
from workspace import (
    STATUS_CLOSED,
    STATUS_COMMITTED,
    STATUS_FAILED as WS_FAILED,
    Workspace,
    open_workspace,
)


@dataclass(frozen=True)
class OperatorCall:
    op: str
    params: dict = field(default_factory=dict)
    input_refs: Optional[list[str]] = None
    why: str = ""


@dataclass
class Sandbox:
    """One run: a unit store, a state, a tracer, and a logical clock."""

    store: UnitStore = field(default_factory=UnitStore)
    state: State = field(default_factory=State)
    tracer: Tracer = field(default_factory=Tracer)
    logical_ts: int = 0
    seed: Any = None
    registry: dict = field(default_factory=lambda: dict(REGISTRY))
    # Per-run, not global: one experiment's provider must not be able to leak
    # into another experiment's trace.
    providers: dict = field(default_factory=dict)

    def open(self, thread_id: str) -> Workspace:
        return open_workspace(thread_id, self.store)

    def run(self, ws: Workspace, program: list[OperatorCall]) -> None:
        for i, call in enumerate(program):
            self.run_one(ws, call, i)

    def run_one(self, ws: Workspace, call: OperatorCall, i: int) -> dict:
        op_name = call.op
        fn = self.registry.get(op_name)
        if fn is None:
            # An unknown operator is still a traceable event: a run that dies
            # with no row is a run whose evidence is missing (plan §5).
            self.logical_ts += 1
            self.tracer.record(
                thread=ws.thread_id,
                op=op_name,
                params=call.params,
                input_refs=call.input_refs or [],
                output_refs=[],
                status=STATUS_FAILED,
                sv_before=self.state.version,
                sv_after=self.state.version,
                logical_ts=self.logical_ts,
                provider=call.params.get("transform_name"),
                comparator=call.params.get("comparator"),
                why=call.why,
                note="error: unknown operator: %s" % op_name,
                seed=self.seed,
            )
            ws.status = WS_FAILED
            raise SandboxError("unknown operator: %s" % op_name)

        self.logical_ts += 1
        op_id = "%s#%d" % (ws.thread_id, i + 1)
        ctx = ExecContext(
            thread_id=ws.thread_id,
            op_id=op_id,
            logical_ts=self.logical_ts,
            provider=call.params.get("transform_name"),
            state_version=self.state.version,
        )
        sv_before = self.state.version
        # input_refs travel in the call but operators read params, so merge them
        # into one dict here. Operators then have a single place to look.
        params = dict(call.params)
        if call.input_refs is not None:
            params["input_refs"] = self._resolve_refs(ws, call.input_refs)

        try:
            result, writes = fn(ws, ctx, params, self.state.view(), self.providers)
        except SandboxError as exc:
            # Hard failure, recorded as failed. Never a silent no-op: a silent
            # no-op makes the trace lie, and the trace is the only evidence.
            self.tracer.record(
                thread=ws.thread_id,
                op=op_name,
                params=call.params,
                input_refs=call.input_refs or [],
                output_refs=[],
                status=STATUS_FAILED,
                sv_before=sv_before,
                sv_after=sv_before,
                logical_ts=ctx.logical_ts,
                provider=ctx.provider,
                comparator=call.params.get("comparator"),
                why=call.why,
                note="error: %s" % exc,
                seed=self.seed,
            )
            ws.status = WS_FAILED
            raise

        # Only COMMIT produces writes, and the runner is the only writer.
        for key, unit_id in writes:
            self.state.append(key, unit_id, ws.thread_id, op_id)

        row = self.tracer.record(
            thread=ws.thread_id,
            op=op_name,
            params=call.params,
            input_refs=call.input_refs or [],
            output_refs=list(result.output_refs),
            status=result.status,
            sv_before=sv_before,
            sv_after=self.state.version,
            logical_ts=ctx.logical_ts,
            provider=ctx.provider,
            comparator=call.params.get("comparator"),
            why=call.why,
            note=result.note,
            seed=self.seed,
        )
        if op_name == "COMMIT":
            ws.status = STATUS_COMMITTED
        return row

    def close(self, ws: Workspace) -> None:
        if ws.status in (STATUS_COMMITTED, WS_FAILED):
            final = ws.status
        else:
            final = STATUS_CLOSED
        ws.close(final)

    def _resolve_refs(self, ws: Workspace, refs: list[str]) -> list[str]:
        """Allow `last:TRANSFORM` alongside a literal unit id.

        A literal id would have to be hard-coded in the program, which means the
        program breaks the moment an operator allocates an extra unit. `last:X`
        says "the units the most recent X produced" -- a reference, not control
        flow: still a flat linear program, no branches, no loops (plan §5).
        """
        out: list[str] = []
        for ref in refs:
            if not ref.startswith("last:"):
                out.append(ref)
                continue
            op_name = ref.split(":", 1)[1]
            for row in reversed(self.tracer.rows):
                if row["thread"] == ws.thread_id and row["op"] == op_name:
                    if row["status"] != "ok":
                        raise SandboxError(
                            "last:%s refers to a failed step" % op_name
                        )
                    out.extend(row["output_refs"])
                    break
            else:
                raise SandboxError("no prior %s in thread %s" % (op_name, ws.thread_id))
        return out


def run_program(
    sandbox: Sandbox,
    thread_id: str,
    program: list[OperatorCall],
    seed_payloads: Optional[list] = None,
    open_only: bool = False,
) -> Workspace:
    """open -> seed -> run -> close. The whole Thread lifecycle (plan §5).

    `open_only` leaves the Thread open so a caller can inspect it (Thread B of
    E-S1 needs to read its own working set before closing).
    """
    ws = sandbox.open(thread_id)
    if seed_payloads:
        ws.seed(seed_payloads)
    sandbox.run(ws, program)
    if not open_only:
        sandbox.close(ws)
    return ws
