"""Memory module skeleton.

Long-term memory should eventually support:
- storing observations and reflections
- importance scoring
- retrieval by relevance, recency, and importance
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class MemoryItem:
    content: str
    importance: float = 0.5
    timestamp: float = 0.0
    kind: str = "observation"  # observation | reflection
    metadata: dict[str, Any] = field(default_factory=dict)


class Memory:
    """A simple in-memory implementation to be replaced by a persistent store."""

    def __init__(self) -> None:
        self._items: list[MemoryItem] = []

    def add(self, item: MemoryItem) -> None:
        self._items.append(item)

    def retrieve(self, query: str, limit: int = 10) -> list[MemoryItem]:
        # TODO: implement proper scoring (relevance + recency + importance).
        return self._items[-limit:]

    def all(self) -> list[MemoryItem]:
        return list(self._items)
