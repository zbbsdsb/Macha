"""Reasoning module skeleton.

Will contain planning, reflection, and decision-making logic.
"""

from __future__ import annotations

from .memory import Memory


class Reasoning:
    """Placeholder for LLM-based or hybrid reasoning."""

    def __init__(self, memory: Memory) -> None:
        self.memory = memory

    def decide(self, observation_text: str) -> str:
        # TODO: call LLM or rule-based policy.
        return "I should respond based on my memories."
