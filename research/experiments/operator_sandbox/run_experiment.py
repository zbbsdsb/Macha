"""Run an experiment and write its evidence.

    python research/experiments/operator_sandbox/run_experiment.py exp1

Produces, per run arm:

    runs/exp1/prog/trace.jsonl    one row per operator call, the primary evidence
    runs/exp1/prog/state.json     terminal state, with the payload of every
                                  unit it points at
    runs/exp1/prog/metrics.json   three raw counts, computed from the trace

Committed to git on purpose: the rows are small, and they are what a reviewer
reads line by line (plan §2.2).
"""

from __future__ import annotations

import argparse
import json
import os
import sys

sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from metrics import compute_metrics, write_metrics  # noqa: E402
import scenarios  # noqa: E402
from trace import FIELDS  # noqa: E402

HERE = os.path.dirname(os.path.abspath(__file__))
RUNS = os.path.join(HERE, "runs")

EXPERIMENTS = {
    "exp1": {
        "title": "E-S1 Continuity",
        "arms": {"prog": scenarios.run_prog, "mono": scenarios.run_mono},
        # The ablation named in Q-02's pre-registration as H-C's falsifier. Not a
        # third design: it is the prog program with one step deleted.
        "ablations": {"no_select": scenarios.run_prog_no_select},
    },
}


def write_json(path: str, data) -> None:
    with open(path, "w", encoding="utf-8", newline="\n") as fh:
        json.dump(data, fh, indent=2, sort_keys=True, ensure_ascii=False)
        fh.write("\n")


def run(exp_id: str, arm: str) -> dict:
    spec = EXPERIMENTS[exp_id]
    runner_fn = spec["arms"].get(arm) or spec.get("ablations", {})[arm]
    sandbox, extra = runner_fn()

    out_dir = os.path.join(RUNS, exp_id, arm)
    os.makedirs(out_dir, exist_ok=True)

    sandbox.tracer.write(os.path.join(out_dir, "trace.jsonl"))
    write_json(
        os.path.join(out_dir, "state.json"),
        sandbox.state.to_json(sandbox.store.units),
    )
    m = compute_metrics(sandbox.tracer.rows)
    write_metrics(os.path.join(out_dir, "metrics.json"), m)

    return {
        "arm": arm,
        "sandbox": sandbox,
        "thread_b_focus": extra["thread_b_focus"],
        "state_version": sandbox.state.version,
        "trace_hash": sandbox.tracer.trace_hash(),
        "state_signature": scenarios.state_signature(sandbox),
        "metrics": m,
    }


def main() -> int:
    ap = argparse.ArgumentParser(description="Operator Sandbox experiments")
    ap.add_argument("exp", choices=sorted(EXPERIMENTS))
    args = ap.parse_args()

    spec = EXPERIMENTS[args.exp]
    print("%s -- %s" % (args.exp, spec["title"]))
    print("trace fields: %s" % ", ".join(FIELDS))
    print()

    results = {}
    for arm in spec["arms"]:
        results[arm] = run(args.exp, arm)
    for name in spec.get("ablations", {}):
        results[name] = run(args.exp, name)

    for arm, r in results.items():
        m = r["metrics"]
        print("[%s]" % arm)
        print("  steps            %d  (%s)" % (m["total_steps"], ", ".join(m["ops_used"])))
        print("  attributable     %.2f  attributable_changes=%d"
              % (m["attributable_steps"], m["attributable_changes"]))
        print("  intermediate     %d derived unit(s)" % m["intermediate_units"])
        print("  unmapped         %d" % m["unmapped_steps"])
        print("  state version    %d" % r["state_version"])
        print("  thread B focus   %s" % (r["thread_b_focus"] or "[] -- RETRIEVED NOTHING"))
        print("  trace hash       %s" % r["trace_hash"][:16])
        print()

    # The control comparison, printed rather than asserted: the judgement belongs
    # to a reader looking at the traces, and a "PASS" here would be exactly the
    # self-grading the plan forbids (§7.0b: raw counts, not a score).
    sigs = {arm: r["state_signature"] for arm, r in results.items()}
    arms = sorted(sigs)
    same = all(sigs[a] == sigs[arms[0]] for a in arms)
    print("control: terminal state identical across arms = %s" % same)
    for a in arms:
        for key, payload in sigs[a]:
            print("  %-5s %-28s %s" % (a, key, payload))
    print()

    prog_m = results.get("prog", {}).get("metrics", {})
    mono_m = results.get("mono", {}).get("metrics", {})
    if prog_m and mono_m:
        print("H-B discriminator (pre-registered): attributable_changes must be")
        print("  >1 on prog and ==1 on mono.")
        print("  prog=%d  mono=%d  ->  %s"
              % (
                  prog_m["attributable_changes"],
                  mono_m["attributable_changes"],
                  "supports H-B"
                  if prog_m["attributable_changes"] > mono_m["attributable_changes"]
                  else "H-B KILLED",
              ))
        print()

    abl = results.get("no_select")
    if abl:
        same = abl["state_signature"] == results["prog"]["state_signature"]
        got = bool(abl["thread_b_focus"])
        print("H-C ablation (pre-registered as H-C's falsifier): prog with SELECT")
        print("  deleted.")
        print("  terminal state unchanged = %s" % same)
        print("  thread B still retrieves  = %s" % got)
        print("  ->  %s"
              % (
                  "H-C survives (SELECT and TRANSFORM are not separable here)"
                  if not (same and got)
                  else "SELECT contributed nothing to continuity"
              ))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
