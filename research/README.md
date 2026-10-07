# Research (Top-Level)

Exploratory, throwaway, and experimental working space for the paper.

**This is the deliberate opposite of `docs/` and `papers/`.** Anything here may be
deleted, rewritten, or proven wrong without ceremony. Nothing here is a deliverable.

> Do not confuse this directory with `docs/research/`, which holds *formal* research
> documents (positioning, direction). This `research/` folder is the draft-scratch layer.

## Contents

- `literature/` — the seven evidence dossiers (01–07) plus `00-literature-map-paper-gaps.md`;
  load-bearing material that a reviewer cannot dismiss. Read-only as evidence, forwardable to the paper.
- `plans/` — methodology / collection plans and working proposals that are not yet ratified
  (e.g. the literature intelligence plan, `roadmap-rework-draft.md`, and
  `minecraft-layer-validation-plan.md`).
  - `plans/minecraft-layer/` — the Minecraft Layer technical foundation
    ([index](plans/minecraft-layer/README.md)): stack lock, file-level project structure, protocol v0,
    observation/event set, build & boundary rules. Plan only; no code yet.
  - `plans/operator-sandbox-plan.md` — **Operator Sandbox 第一阶段实施计划**（SepMay 算子空间）：
    仓库审计、位置决定（为何落在 `experiments/`）、语言与依赖决定（Python / 纯标准库）、最小数据模型、
    五个算子契约、执行与 trace 模型、三个实验（Continuity / Reinterpretation / Contradiction，含 `prog` vs `mono`
    对照组与三个可数指标）、测试策略、延后清单、实现顺序（含 Step 0 两条腿与 G1–G4 止损闸门）、
    预期效果与天花板、**执行进度表（Step 1–3 已完成，4–8 未开始）**。
    上游设计见 `paths/01-sepmay-ivy/operator-space.md`。
- `experiments/operator_sandbox/` — **代码已落地**（Step 1–3，2026-10-07）。标准库 Python，
  10 个文件：`SELECT / TRANSFORM / COMMIT` 三个算子 + 线性 runner + E-S1 及其 `prog`/`mono`/`no_select`
  三份运行（`runs/exp1/`，已提交进 git）+ 28 条测试。
  预注册与结果：[`questions/Q-02-operator-space-primitives.md`](questions/Q-02-operator-space-primitives.md)（等级 **E1**）。
  **不是 Core，Core 不依赖它**；`src/macha` 与 `layers/` 未被触碰。
- `projects/` — **execution** projects (dated): what to do, in what order, with a handover checklist.
  Design/spec docs stay in `plans/`; a project folder only answers "how do we get there".
  - `projects/2026-09-14-mc-vertical-slice/` — Minecraft Layer vertical slice (M0–M6, up to
    interacting with an NPC in a live server). Contains `handover-checklist.md`, `plans/01–03`, `prompts/`.
- `paths/` — parallel architecture paths for Macha Core, kept deliberately separate so no single route
  becomes the only route ([index](paths/README.md)). Each path is a folder: path doc + `open-decisions.md`
  + `eval/` (assessment, mandatory). Currently: `01-sepmay-ivy/` (IC lifecycle, frozen, scored 6.5/10).
- `scratch/` — quick probes, reviews of others' frameworks, "one look at how X does it"
  notes. Lowest permanence. Example: `aetherflow-*.md` live here.
- `questions/` — **one file per research question** (status on line 1, template inside).
  Governed by [`../docs/research-methodology.md`](../docs/research-methodology.md); engineering
  acceptance (vertical slices, V1–V5) does **not** belong here — that is `projects/`.
- `failures/` — our own negative results, classified F1–F7. Failure is an asset; F3/F4/F5
  (implementation/experimental/measurement) must be fixed, not reported as findings.
- `experiments/` — case-validation drafts that must run (e.g. the 3–5 game-NPC case
  study for the relationship language) but are not yet accepted as conclusions.

## Lifecycle Rule

- Work starts here, or in `papers/notes/drafts/`.
- Once a probe matures into a team-accepted conclusion, it is **promoted** into
  `papers/notes/accepted/` (with a status update). The scratch copy is not kept in sync — it is
  historical residue.
- Evidence dossiers in `literature/` are a special case: they back the paper's claims but
  stay in `research/` (evidence layer), referenced from `papers/notes/accepted/paper-status.md`.
- A conclusion that enters the paper body leaves `papers/notes/accepted/` and lives in the
  paper file itself; the notes entry is moved to `papers/notes/archive/`.