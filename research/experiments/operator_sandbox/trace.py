"""Trace: one JSONL row per operator call, plus the metrics computed from it.

The trace is the only evidence this phase produces, so its shape is frozen and
non-extensible (plan §6 / R2). Replay metadata slots that v1 does not use are
written as explicit `null` / `none` rather than omitted -- when a model is
attached later, that is filling a slot, not changing the format.

No OpenTelemetry, no schema version, no exporter, no dashboard (plan §6).
"""

from __future__ import annotations

import hashlib
import json
from dataclasses import dataclass, field
from typing import Any, Optional

# Frozen field set. Adding a key here is a plan change, not a convenience.
FIELDS = (
    "seq",
    "thread",
    "op",
    "params",
    "input_refs",
    "output_refs",
    "status",
    "state_version_before",
    "state_version_after",
    "logical_ts",
    "provider",
    "comparator",
    "seed",
    "why",
    "note",
)


@dataclass
class Tracer:
    rows: list[dict] = field(default_factory=list)
    _seq: int = 0

    def record(
        self,
        thread: str,
        op: str,
        params: dict,
        input_refs: list[str],
        output_refs: list[str],
        status: str,
        sv_before: int,
        sv_after: int,
        logical_ts: int,
        provider: Optional[str],
        comparator: Optional[str],
        why: str,
        note: str,
        seed: Any = None,
    ) -> dict:
        self._seq += 1
        row = {
            "seq": self._seq,
            "thread": thread,
            "op": op,
            "params": params,
            "input_refs": list(input_refs),
            "output_refs": list(output_refs),
            "status": status,
            "state_version_before": sv_before,
            "state_version_after": sv_after,
            "logical_ts": logical_ts,
            "provider": provider,
            "comparator": comparator,
            "seed": seed,
            "why": why,
            "note": note,
        }
        assert set(row) == set(FIELDS), "trace row drifted from the frozen field set"
        self.rows.append(row)
        return row

    # -- serialisation -----------------------------------------------------
    def canonical(self) -> str:
        """Key-sorted, stable. The hash is the reproducibility criterion."""
        return "\n".join(
            json.dumps(r, sort_keys=True, ensure_ascii=False, separators=(",", ":"))
            for r in self.rows
        )

    def trace_hash(self) -> str:
        return hashlib.sha256(self.canonical().encode("utf-8")).hexdigest()

    def write(self, path) -> None:
        with open(path, "w", encoding="utf-8", newline="\n") as fh:
            for r in self.rows:
                fh.write(
                    json.dumps(r, sort_keys=True, ensure_ascii=False) + "\n"
                )

    def subseq(self, ops: list[str]) -> list[dict]:
        """Rows for a given op sequence -- what the integration test asserts on.
        Asserting on a subsequence rather than the whole file avoids brittle
        tests (plan §8)."""
        out = []
        i = 0
        for want in ops:
            while i < len(self.rows) and self.rows[i]["op"] != want:
                i += 1
            if i >= len(self.rows):
                raise AssertionError("trace lacks expected op %r" % want)
            out.append(self.rows[i])
            i += 1
        return out
