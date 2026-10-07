"""Metrics: three raw counts, mechanically computed from the trace.

No score, no weighting, no pass rate (plan §7.0b). These are counts for humans
and for a paper, not a KPI.

Definitions were frozen in Q-02's pre-registration block BEFORE the run. Two
extra counts are in there too, because `attributable_steps` alone cannot
separate `prog` from `mono` -- both can be 1.0, which was known in advance and
recorded as a known defect rather than discovered afterwards.
"""

from __future__ import annotations

import json
from typing import Optional

# Ops that produce a derived unit. Kept explicit: an op appearing here that a
# run never invokes is exactly the "five implemented but two are decoration"
# risk (plan §12.1 R5), and this list is how metrics.py can see it.
DERIVING_OPS = ("TRANSFORM", "RELATE", "TEST")


def compute_metrics(
    rows: list[dict],
    op_names_by_run: Optional[dict] = None,
) -> dict:
    total = len(rows)
    attributable = 0
    unmapped = 0
    changes = 0
    providers = set()
    ops = set()

    for r in rows:
        ops.add(r["op"])
        if r.get("provider"):
            providers.add(r["provider"])

        state_changed = r["state_version_after"] > r["state_version_before"]
        focus_changed = r["op"] == "SELECT" and bool(r["output_refs"])

        if state_changed or focus_changed:
            attributable += 1
        if not state_changed and not focus_changed and not r["output_refs"]:
            unmapped += 1
        if state_changed:
            changes += 1
        if focus_changed:
            changes += 1

    reuse = None
    if op_names_by_run:
        hits = []
        for other_run, names in sorted(op_names_by_run.items()):
            shared = sorted(names & ops)
            if shared:
                hits.append({"run": other_run, "shared_ops": shared})
        reuse = hits or None

    return {
        "attributable_steps": (attributable / total) if total else 0.0,
        "unmapped_steps": unmapped,
        "reuse": reuse,
        "intermediate_units": sum(1 for r in rows if r["op"] in DERIVING_OPS),
        "attributable_changes": changes,
        "total_steps": total,
        "ops_used": sorted(ops),
        "providers_used": sorted(providers),
    }


def write_metrics(path, metrics: dict) -> None:
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(metrics, fh, indent=2, sort_keys=True, ensure_ascii=False)
        fh.write("\n")
