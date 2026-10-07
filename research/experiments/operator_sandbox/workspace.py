"""Workspace = one Thread in progress: the temporary side of the boundary.

The Thread / Persistent State split is the most important boundary in this phase
(plan §3.2):

  * Workspace lives for one cognitive process, then is discarded.
  * Every operator's output lands here. Only COMMIT escapes.
  * A closed Thread's units are invisible to the next SELECT.

`operator trace` deliberately does NOT live here -- it is cross-thread execution
record owned by the runner. Folding it in would merge "working set" with
"audit log".
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Optional

from model import Unit, UnitStore

STATUS_OPEN = "open"
STATUS_COMMITTED = "committed"
STATUS_FAILED = "failed"
STATUS_CLOSED = "closed"


@dataclass
class Workspace:
    thread_id: str
    store: UnitStore
    units: dict[str, Unit] = field(default_factory=dict)
    inputs: list[str] = field(default_factory=list)
    focus: list[str] = field(default_factory=list)
    status: str = STATUS_OPEN

    # -- admission ---------------------------------------------------------
    # Seeding is not an operator. It is the intake step (D7): facts come in, and
    # intake does not assign meaning (plan §2.1, operator-space.md §1.5).
    def seed(self, payloads: list) -> list[str]:
        if self.status != STATUS_OPEN:
            raise SandboxErrorForStatus(self.thread_id, self.status)
        ids: list[str] = []
        for payload in payloads:
            uid = self.store.allocate_id()
            unit = Unit(
                id=uid,
                payload=payload,
                origin="external",
                created_by=None,
                refs=(),
                logical_ts=0,
            )
            self.store.add(unit)
            self.units[uid] = unit
            self.inputs.append(uid)
            ids.append(uid)
        return ids

    # -- working set -------------------------------------------------------
    def add_derived(self, unit: Unit) -> Unit:
        if unit.origin != "derived":
            raise SandboxErrorForStatus("derived unit must have origin=derived")
        if unit.id in self.units:
            raise SandboxErrorForStatus("duplicate unit in workspace: %s" % unit.id)
        self.store.add(unit)
        self.units[unit.id] = unit
        return unit

    def get(self, uid: str) -> Unit:
        if uid not in self.units:
            raise SandboxErrorForStatus(
                "unit %s is not in thread %s's working set" % (uid, self.thread_id)
            )
        return self.units[uid]

    def has(self, uid: str) -> bool:
        return uid in self.units

    # -- focus -------------------------------------------------------------
    def set_focus(self, uids: list[str]) -> None:
        """SELECT is the only thing that writes focus. Sorted, deduplicated."""
        self.focus = sorted(set(uids))

    def visible_from_state(self, unit_ids: tuple[str, ...]) -> tuple[str, ...]:
        """Which of these state-referenced units this Thread can actually see.

        v1 policy: a committed unit is re-materialised into the new Thread's
        working set on demand, so a later Thread can retrieve without re-ingesting
        the original input. This is the whole point of Exp1.
        """
        out = []
        for uid in unit_ids:
            if uid in self.units:
                out.append(uid)
                continue
            unit = self.store.units.get(uid)
            if unit is None:
                continue
            self.units[uid] = unit
            out.append(uid)
        return tuple(sorted(out))

    def unit_ids(self) -> list[str]:
        return sorted(self.units)

    def close(self, status: str) -> None:
        self.status = status
        # Discard: a closed Thread's working set is gone. Only trace and State
        # survive. The UnitStore keeps payloads so State can still be rendered;
        # it is not reachable as a working set without going through State.
        self.units = {}
        self.focus = []
        self.inputs = []


class SandboxErrorForStatus(Exception):
    pass


def open_workspace(thread_id: str, store: UnitStore) -> Workspace:
    return Workspace(thread_id=thread_id, store=store)


def resolve(
    ws: Workspace,
    input_refs: Optional[list[str]],
    params: dict,
) -> list[Unit]:
    """Explicit refs win; if absent, operators fall back to focus.

    An output unit is in the working set, so one output can feed several later
    operators with no extra mechanism (plan §5).
    """
    if input_refs:
        return [ws.get(uid) for uid in input_refs]
    return [ws.get(uid) for uid in ws.focus]
