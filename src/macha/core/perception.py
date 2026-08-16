"""Perception module skeleton.

Converts environment/player input into structured observations.
"""

from __future__ import annotations

from .agent import Observation


class Perception:
    """Default perception simply wraps text input as an Observation."""

    def process_text(self, text: str, source: str = "player") -> Observation:
        return Observation(content=text, source=source)
