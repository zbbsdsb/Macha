# Paper Notes Index

The notes are organized by **maturity tier** (see Archiving Rules below), not by topic.
Dossiers backing the paper's literature layer live in `research/literature/`.

## accepted/ — team-ratified conclusions

| File | Content |
|---|---|
| [accepted/05-macha-question-tree.md](accepted/05-macha-question-tree.md) | The paper's question tree (L0–L3) and the 4 positioning forks — current scaffold |
| [accepted/paper-goal-and-world-architecture.md](accepted/paper-goal-and-world-architecture.md) | Paper goal vs. world architecture separation |
| [accepted/paper-section-directions.md](accepted/paper-section-directions.md) | Candidate section directions A–G |
| [accepted/paper-status.md](accepted/paper-status.md) | Overall paper writing status and next steps |
| [accepted/decision-layer-first-sequencing.md](accepted/decision-layer-first-sequencing.md) | **Decision (RATIFIED 2026-09-13)**: build the Minecraft Layer before Macha Core |
| [accepted/decision-layers-directory-layout.md](accepted/decision-layers-directory-layout.md) | **Decision (RATIFIED 2026-09-14)**: `layers/` build root, shared core under `kit/`; split triggers T1–T4 |
| [accepted/decision-arclight-cloud-environment.md](accepted/decision-arclight-cloud-environment.md) | **Decision (RATIFIED 2026-09-15)**: experiment environment = cloud Arclight 1.20.1; Layer stays a plugin; build targets the lower bound (Spigot API 1.20.1 + Java 17); `transport.mode: dial` |

> Decision records (`decision-*.md`) live in `accepted/` as well: per
> `../../docs/team-workflow.md`, a deviation from a ratified rule or plan requires a recorded
> decision. They are project decisions, not paper conclusions.

## drafts/ — in-progress technical drafts

| File | Content |
|---|---|
| [drafts/field-superposition-formalization.md](drafts/field-superposition-formalization.md) | Formal discussion draft of "field superposition" |
| [drafts/four-papers-boundary-and-fusion.md](drafts/four-papers-boundary-and-fusion.md) | Boundary probing of four papers and a five-layer fusion attempt |
| [drafts/environment-integration-layer.md](drafts/environment-integration-layer.md) | Layer architecture audit (A–G): Layer as an architectural primitive, Core↔Layer↔Environment boundaries, repo organization (PENDING) |

## archive/ — superseded / historical thinking (traceability only)

| File | Content | Archived Note |
|---|---|---|
| [archive/what-we-desire-in-game-agents.md](archive/what-we-desire-in-game-agents.md) | What the player desires in a game agent: six questions, four relationship archetypes | Superseded by question tree + paper-status |
| [archive/conclusions-desired-agent.md](archive/conclusions-desired-agent.md) | Current-stage conclusions on the "desired agent" | Conclusions absorbed into active notes |
| [archive/npc-world-boundary.md](archive/npc-world-boundary.md) | The NPC's world boundary | Superseded by accepted notes |

## Not in This Folder

- AetherFlow review / borrowings notes (`aetherflow-*.md`) were **moved to
  `research/scratch/`** on 2026-08-21 as throwaway exploration — they study an external
  framework and carry no team conclusion. See `research/README.md` for the lifecycle rule.
- Per-team-workflow A3, each paper in `reference/` gets a companion note in `papers/notes/papers/<id>.md`.

## Archiving Rules

- Memory layering maps to **maturity** (accepted / drafts / archive), not topic — see the
  lifecycle rule in `README.md`.
- Once a discussion yields conclusions, the original note is not deleted but moved to
  `archive/` (or marked archived in place).
- Archived files retain only traceability value and are no longer the primary basis for advancing work.
- New conclusions must be written into `accepted/` (or promoted to the paper body), not by
  continuing to modify archived files.