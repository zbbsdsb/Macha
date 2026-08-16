"""Base agent interface for Macha.

This is the initial skeleton. The goal is to define stable interfaces early
so that Memory / Reasoning / Perception / Action can be developed in parallel.
"""

from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any


@dataclass
class Observation:
    """A structured observation coming from the environment or player."""

    content: str
    source: str = "unknown"
    timestamp: float = 0.0
    metadata: dict[str, Any] = field(default_factory=dict)


@dataclass
class ActionResult:
    """Result of an agent's action."""

    content: str
    success: bool = True
    metadata: dict[str, Any] = field(default_factory=dict)


class BaseAgent:
    """Minimal agent contract.

    Subclasses should implement the cognitive loop:
    perceive -> think -> act.
    """

    name: str = "MachaAgent"

    def perceive(self, observation: Observation) -> None:
        raise NotImplementedError

    def think(self) -> str:
        raise NotImplementedError

    def act(self) -> ActionResult:
        raise NotImplementedError
