# Team R&D Workflow — Hard Rules

Status: **v0.1 — ratified scope A & B**. Sections C/D/E are intentionally deferred and
marked `TODO` below; do not implement them until the team has explicitly agreed their
shape.

This is the authoritative ruleset for how the team works. Every rule below is blocking:
deviation requires a recorded decision in `papers/notes/` first.

> **See also:** [`research-methodology.md`](research-methodology.md) — the *upstream* process
> (observation → question → hypothesis → experiment → evidence → claim). It supplies the **evidence
> levels** and **pre-registration** that this document deliberately does not cover, and it changes
> **none** of the rules here: B4's claim threshold still gates what may enter the paper.

Scope marker: `[RATIFIED]` = team-agreed, binding. `[DRAFT]` = proposed, awaiting confirmation.

---

## A. Paper / Material Collection & Merge

### A1. Inclusion Criteria — `[RATIFIED]`
A paper is admitted into `reference/` only if it is plausibly relevant to the Macha
thesis (game agents, player-perspective intelligence, virtual-agent cognition/fields,
relationship design) **and** at least one team member commits to reading it.

- Marketing material, blog posts, and non-archived web pages do **not** enter `reference/`
  as PDFs; if referenced, they are recorded as a link inside the relevant notes file.
- A paper does **not** need to be "good" or "authoritative" to be admitted. Admitted ≠ endorsed.

### A2. Provenance Metadata — `[RATIFIED]`
Every admitted item **must** have a provenance record **before** it is considered read.
Record it in the paper's notes file (see A3):

| Field | Required |
|---|---|
| arxiv id / DOI / stable URL | yes |
| date collected | yes |
| collector (who added it) | yes |
| current status (see A4) | yes |
| why collected / relation to our thesis | yes |
| source of discovery | yes |

### A3. Naming & Location — `[RATIFIED]`
- PDFs live in `reference/` named by identifier: `<id>.pdf` (e.g. `2304.03442v2.pdf`).
- **Every** admitted paper gets a companion markdown file in `papers/notes/papers/<id>.md`
  holding its provenance, one-paragraph summary, and status.
- The four papers currently in `reference/` are treated by the same rule — nothing special,
  nothing authoritative.

### A4. Read → Sink Path — `[RATIFIED]`
Each paper moves through explicit statuses, tracked solely in its notes file:

```
collected → reading → summarized → extracted (conclusions pulled out)
                                                   │
                              ┌────────────────────┴───────────────────┐
                    merged/kept (conclusions enter active notes)      rejected/superseded (recorded why)
```

- Only statuses from this list are valid; a free-form "in progress" is not adequate.
- When a paper's conclusions are merged into an active discussion note, link that note
  from the paper's file and set status to `merged`.
- A rejection records the **reason** (relevance? quality? superseded by which paper?) in the
  paper's notes file.

### A5. Retirement / Archive — `[RATIFIED]`
- A paper is marked `rejected/superseded` in its own notes file; the PDF may stay in
  `reference/` for provenance but is **not** cited as support.
- Bulk removal from `reference/` requires a recorded decision; never silently delete a PDF.

---

## B. Paper-Writing Hard Rules

### B1. Language & Style — `[RATIFIED]`
- The paper body is written in **English only** (no mixed CN/EN inside prose).
- Terminology is defined in a single living glossary (`papers/notes/glossary.md`). A term
  enters the paper only after it is in the glossary.
- Terminology lock: once a term appears in the paper body, renaming it requires a recorded
  decision; `field superposition`, `relationship gap` are under active definition and not yet locked.

### B2. Structural Constraint — `[RATIFIED]`
- The outline (`papers/notes/accepted/05-macha-question-tree.md`) is frozen at its current shape for
  structure disputes; new structure questions go to the "open forks", not ad-hoc re-writes.
- A section is **claimed** before it is written (one owner). No two people draft the same
  section independently.

### B3. Citation Discipline — `[RATIFIED]`
- Only material that has a provenance record (A2) and a status in `reference/`-companions
  may be cited in the paper. Unrecorded citations are ground for review rejection.
- The four initial papers are material, **not** authorities: the paper must not treat them
  as "the" canonical set. Their boundary is discussed in
  `papers/notes/drafts/four-papers-boundary-and-fusion.md`.

### B4. Claim Threshold — `[RATIFIED]`
A sentence makes it into the paper body only if it is supported by at least one of:
  1. a citable source (with provenance), or
  2. a team-ratified conclusion (recorded in `papers/notes/accepted/`), or
  3. an explicit, labeled assumption.

Unsupported assertions are flagged `[ASSUMPTION]` inline until resolved — never silently asserted.

### B5. Versioning & Archiving — `[RATIFIED]`
- When a notes conclusion is promoted into the paper body, the originating notes entry is
  marked `archived` (moved to `papers/notes/archive/`) with a pointer to the paper location.
- The paper file is the single source of truth for its content; notes are history, not an
  alternate truth.
- No two active conclusions may disagree; a contradiction requires a recorded resolution.

---

## C. Team Workflow — `TODO (not ratified)`

- C1 roles/ownership, C2 decision & consensus process, C3 parallelism & merge,
  C4 review/gate rules (incl. the "run TSC + calibrate positioning before commit" rule).

## D. Repository & Engineering Discipline — `TODO (not ratified)`

- D1 directory conventions (partially settled in README), D2 commit conventions,
  D3 doc language policy (CN discussion vs EN artifacts).

## E. Paper ↔ Project Boundary — `TODO (not ratified)`

- E1 paper-vs-implementation priority, E2 site↔paper sync.

---

## Amendment Process

- Add to this document only via the scope markers above.
- Ratifying C/D/E (or changing an `[RATIFIED]` rule) requires a recorded team decision and
  flips the marker to `[RATIFIED]` with the date.