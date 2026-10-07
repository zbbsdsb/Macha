"""Persistent state: append-only, versioned, and writable by exactly one thing.

Only COMMIT may mutate State. Everyone else gets a read-only view whose version
number is the number they must quote in their trace row (plan §4.1).

No update-in-place: Exp2 (reinterpretation) must be able to see that the old
version still exists. That is the whole reason this is a list and not a dict
(plan §3.3).
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Optional

from model import Unit


@dataclass(frozen=True)
class StateEntry:
    key: str
    unit_id: str
    committed_from_thread: str
    committed_from_op: str
    version: int

    def to_json(self) -> dict:
        return {
            "key": self.key,
            "unit_id": self.unit_id,
            "committed_from": {
                "thread": self.committed_from_thread,
                "op": self.committed_from_op,
            },
            "version": self.version,
        }


@dataclass(frozen=True)
class ReadOnlyState:
    """What non-COMMIT operators see. Carries the version so they can quote it."""

    version: int
    entries: tuple[StateEntry, ...]
    unit_ids: tuple[str, ...]

    def select(self, key_prefix: Optional[str] = None) -> tuple[str, ...]:
        """Unit ids whose key matches. Sorted; no dict order dependence."""
        out = [
            e.unit_id
            for e in self.entries
            if key_prefix is None or e.key == key_prefix or e.key.startswith(key_prefix)
        ]
        return tuple(sorted(out))


@dataclass
class State:
    entries: list[StateEntry] = field(default_factory=list)
    version: int = 0

    def append(
        self,
        key: str,
        unit_id: str,
        thread_id: str,
        op_id: str,
    ) -> int:
        """The only mutation in the whole sandbox. Called from COMMIT and nowhere else.

        The boundary-guard test asserts that statically.
        """
        self.version += 1
        self.entries.append(
            StateEntry(
                key=key,
                unit_id=unit_id,
                committed_from_thread=thread_id,
                committed_from_op=op_id,
                version=self.version,
            )
        )
        return self.version

    def view(self) -> ReadOnlyState:
        return ReadOnlyState(
            version=self.version,
            entries=tuple(self.entries),
            unit_ids=tuple(sorted(e.unit_id for e in self.entries)),
        )

    def to_json(self, store: dict[str, Unit]) -> dict:
        """State plus the payload of every unit it points at.

        Payloads live in the run's UnitStore, not in State; without them a later
        Thread could see that *something* was committed but not what.
        """
        return {
            "version": self.version,
            "entries": [e.to_json() for e in self.entries],
            "unit_payloads": {
                e.unit_id: store[e.unit_id].to_json()
                for e in sorted(self.entries, key=lambda x: x.version)
                if e.unit_id in store
            },
        }


def load_state(data: dict, store: dict[str, Unit]) -> "State":
    st = State()
    st.version = data["version"]
    st.entries = [
        StateEntry(
            key=e["key"],
            unit_id=e["unit_id"],
            committed_from_thread=e["committed_from"]["thread"],
            committed_from_op=e["committed_from"]["op"],
            version=e["version"],
        )
        for e in data["entries"]
    ]
    for uid, u in data.get("unit_payloads", {}).items():
        store[uid] = Unit.from_json(u)
    return st
