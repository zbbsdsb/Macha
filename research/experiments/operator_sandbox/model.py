"""Minimal data model for the Operator Sandbox.

Four concepts, four jobs. Field counts are hard-capped on purpose: adding a field
means deleting one (see operator-sandbox-plan.md §3.1 / R1).

Standard library only. No third-party imports, anywhere in this package.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

# Logical clock, not wall clock. Monotonic per sandbox run.
# Plan §2.4: wall clock would break reproducibility for no analytical gain.

ORIGIN_EXTERNAL = "external"
ORIGIN_DERIVED = "derived"

STATUS_OK = "ok"
STATUS_FAILED = "failed"


class SandboxError(Exception):
    """Hard failure. Never a silent no-op -- a silent no-op makes the trace lie,
    and the trace is the only evidence this phase produces (plan §5)."""


@dataclass(frozen=True)
class Unit:
    """The carrier of information. Six fields, no more.

    Explicitly NOT here: importance, emotion, confidence, embedding, relation-type
    enums. Importance is "what is worth remembering"; COMMIT does not decide that
    (plan §3.1, U5).
    """

    id: str
    payload: Any
    origin: str
    created_by: Optional[str]
    refs: tuple[str, ...]
    logical_ts: int

    def to_json(self) -> dict:
        return {
            "id": self.id,
            "payload": self.payload,
            "origin": self.origin,
            "created_by": self.created_by,
            "refs": list(self.refs),
            "logical_ts": self.logical_ts,
        }

    @staticmethod
    def from_json(d: dict) -> "Unit":
        return Unit(
            id=d["id"],
            payload=d["payload"],
            origin=d["origin"],
            created_by=d["created_by"],
            refs=tuple(d["refs"]),
            logical_ts=d["logical_ts"],
        )


@dataclass(frozen=True)
class OpResult:
    """What every operator returns. Uniform on purpose (plan §4.1)."""

    output_refs: tuple[str, ...]
    status: str = STATUS_OK
    note: str = ""


@dataclass(frozen=True)
class ExecContext:
    """Execution context handed to every operator. Common semantics, not per-operator."""

    thread_id: str
    op_id: str
    logical_ts: int
    provider: Optional[str]
    state_version: int


@dataclass
class UnitStore:
    """Flat id -> Unit index for one sandbox run.

    Deliberately not a memory system: no scoring, no forgetting, no summarisation
    (plan §4.6 / R6). It is the union of what Threads have produced so far; whether
    a given Thread can *see* a unit is Workspace's business, not the store's.
    """

    units: dict[str, Unit] = field(default_factory=dict)
    _next_id: int = 1

    def allocate_id(self) -> str:
        uid = "u%04d" % self._next_id
        self._next_id += 1
        return uid

    def add(self, unit: Unit) -> Unit:
        if unit.id in self.units:
            raise SandboxError("duplicate unit id: %s" % unit.id)
        self.units[unit.id] = unit
        return unit

    def get(self, uid: str) -> Unit:
        try:
            return self.units[uid]
        except KeyError:
            raise SandboxError("unknown unit: %s" % uid) from None

    def sorted_ids(self) -> list[str]:
        """Always sorted. Dict iteration order is not a reproducibility guarantee
        (PYTHONHASHSEED), so every traversal in this package goes through here."""
        return sorted(self.units)
