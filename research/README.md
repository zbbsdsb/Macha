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
- `scratch/` — quick probes, reviews of others' frameworks, "one look at how X does it"
  notes. Lowest permanence. Example: `aetherflow-*.md` live here.
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