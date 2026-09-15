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