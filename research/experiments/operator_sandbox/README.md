# Operator Sandbox

A small, deliberately incomplete interpreter for the five candidate operators in
[`../../paths/01-sepmay-ivy/operator-space.md`](../../paths/01-sepmay-ivy/operator-space.md).
It exists to answer one question with data instead of discussion: **can this
operator space express a cognitive process, and is the decomposition necessary?**

The plan is [`../../plans/operator-sandbox-plan.md`](../../plans/operator-sandbox-plan.md).
The pre-registered question is
[`../../questions/Q-02-operator-space-primitives.md`](../../questions/Q-02-operator-space-primitives.md).

> **This is an experiment bench, not a feature.** The host NPC still does not
> speak, remember, or act. Evidence here tops out at E1. Nothing in this
> directory is Core, and Core does not depend on it.

## Rerun

```text
python -m pytest research/experiments/operator_sandbox -q
python research/experiments/operator_sandbox/run_experiment.py exp1
```

Python 3.10+, standard library only. `pytest` is the project's existing dev
dependency. No install step, no network, no LLM, no Gradle.

## What is here

| File | What it holds |
|---|---|
| `model.py` | `Unit` (six fields, hard cap) · `OpResult` · `ExecContext` · `UnitStore` |
| `workspace.py` | one Thread in progress: working set + focus; discarded on close |
| `state.py` | append-only entries + version; the only mutable thing in the sandbox |
| `trace.py` | one JSONL row per operator call; frozen field set; trace hash |
| `metrics.py` | the three raw counts, computed from the trace |
| `operators.py` | `SELECT` · `TRANSFORM` · `COMMIT` + the provider seam |
| `program.py` | linear runner; owns the trace and the State write |
| `scenarios.py` | E-S1 and its `mono` control |
| `run_experiment.py` | CLI; writes `runs/` |
| `test_sandbox.py` | unit · boundary guard · integration · determinism |

`RELATE` and `TEST` are **not** here yet. They arrive with E-S2/E-S3, and only
if those experiments cannot be expressed without them — `RELATE` may turn out to
be redundant and get deleted (Q-02's D10).

## The two boundaries that matter

**Temporary vs persistent.** Every operator's output lands in the Thread's
working set. Only `COMMIT` escapes into `State`. A closed Thread is invisible
to the next one; the only way back is `SELECT(source="state")`. A test asserts
this directly.

**Who may write.** `State.append` is called from exactly one place — the runner.
Operators declare *what* they want written; the runner performs it. The
boundary-guard test parses the AST and fails if a second call site appears.

## Determinism

Python's dict and set iteration order is not a reproducibility guarantee, so
every traversal sorts by id, the clock is logical rather than wall-clock, and
one test re-runs a program in a **fresh interpreter with a pinned
`PYTHONHASHSEED`** and compares trace hashes.

This is the part to cut first if time runs short — it is not a precondition for
E-S1's conclusion (plan §12.2).

## Evidence

`runs/exp1/{prog,mono}/` each hold `trace.jsonl` · `state.json` · `metrics.json`,
committed to git so a reviewer can read them line by line. A test asserts the
committed trace equals a fresh run, so the evidence cannot go stale unnoticed.

`prog` and `mono` are the same computation with and without decomposition. The
control is what makes "decomposition is necessary" a question with a detector:
if `prog` cannot name the step that changed something, it is no better than
`mono`.
