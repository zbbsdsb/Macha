"""Action module skeleton.

Converts decisions into game commands or natural language output.
"""

from __future__ import annotations

from .agent import ActionResult


class Action:
    """Placeholder action executor."""

    def execute(self, decision: str) -> ActionResult:
        return ActionResult(content=decision)
