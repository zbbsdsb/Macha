# Macha

**Revolutionizing game NPCs!**

Macha is a research and engineering repository for next-generation game NPCs. Our goal is not to build an NPC "that can chat," but to construct an LLM-driven NPC framework with **long-term memory, believable reflection, dynamic planning, and multi-agent collaboration**.

> Current status: repository initialization phase.  
> Research foundation: the four core papers in `reference/`.  
> **Current sequencing (decided 2026-09-13): Layer-first, Core later** — the first verifiable
> milestone is the Layer Protocol + a Stub Core + the Minecraft Layer, not the cognitive core.
> See [Development Roadmap](docs/roadmap.md) and the
> [decision record](papers/notes/accepted/decision-layer-first-sequencing.md).

Macha is **two separable systems joined by one contract**: an environment-agnostic **Macha Core**
(cognition), and an independent **Environment Integration Layer** per external world (Minecraft,
Skyrim, Cyberpunk, Unreal, Unity, simulations, …). Minecraft is our first *Concrete Layer Test
Case*, not the framework's identity. See [Target Architecture](docs/architecture.md) for the Layer
boundary and its protocol.

---

## Why "Macha"?

Macha represents the three things we want to achieve:

- **Memory**: let NPCs remember experiences, relationships, and causality.
- **Architecture**: replace "prompt piling" with an extensible, modular architecture.
- **Character**: give every NPC a stable, believable, and evolving "persona".

---

## Repository Structure

```text
Macha/
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── pyproject.toml
├── reference/                 # Running collection of source PDFs (not authoritative)
│   ├── *.pdf                  #   PDFs by identifier, e.g. 2304.03442v2.pdf
│   └── index.md               #   PDF → literature dossier / paper mapping
├── research/                  # Trial-and-error layer: scratch probes + evidence dossiers
│   ├── literature/            #   evidence dossiers (01–07) + literature-map
│   ├── plans/                 #   methodology / collection plans (intelligence plan,
│   │                          #   roadmap rework, Minecraft Layer validation)
│   ├── projects/              #   dated execution projects (how to get there + handover checklist)
│   ├── questions/             #   one file per research question (status on line 1)
│   ├── failures/              #   our own negative results, classified F1–F7
│   ├── paths/                 #   parallel architecture paths for Core (frozen until reality tests them)
│   ├── scratch/               #   lowest permanence, e.g. reviews of others' frameworks
│   └── experiments/           #   case-validation drafts not yet accepted as conclusions
├── papers/                    # Formal output: the paper + reasoning notes
│   ├── notes/                 #   team reasoning & conclusions, layered by maturity
│   │   ├── accepted/          #     team-ratified conclusions
│   │   ├── drafts/            #     in-progress technical drafts
│   │   └── archive/           #     superseded / historical thinking (traceability)
│   └── 2026-crossing-the-game-agent-gap.md
├── announcements/             # Public experiment announcements
├── docs/                      # Formal documents: research positioning, architecture, roadmap
│   ├── research/
│   ├── retired/               #   superseded docs, kept for traceability
│   ├── architecture.md
│   └── roadmap.md
├── site/                      # Deployment source for the Macha site / paper showcase
├── src/
│   └── macha/
│       ├── __init__.py
│       └── core/              # Core module skeleton
│           ├── __init__.py
│           ├── agent.py
│           ├── memory.py
│           ├── perception.py
│           ├── reasoning.py
│           └── action.py
├── layers/                    # Environment Integration Layers — one Gradle build root
│   ├── kit/                   #   shared, environment-agnostic (pure JVM)
│   │   └── protocol/ runtime/ transport/
│   ├── minecraft/             #   Minecraft Layer (only module with paper-api)
│   ├── simulator/             #   fake environment (control condition)
│   └── testclient/            #   vertical-slice test client
├── recruitment/               # Recruiting material (sources + built PDFs; caches ignored)
├── tools/                     # Non-Macha tooling
│   └── stub-core/             #   Python stub counterpart for the Layer (NOT Macha Core)
├── examples/                  # Living case set backing the paper's case studies
└── tests/
    └── test_smoke.py
```

### Four Layers + One Reference Store

| Layer | Where | Nature |
|---|---|---|
| 研究试错 | `research/` | Throwaway, expandable, unwritten; nothing here is a conclusion |
| 论文落地 | `papers/` | The only outward formal output; defends against deviation |
| 正式文档 | `docs/` | Stable, for humans / future developers |
| 部署站点 | `site/` | Statically hostable website build over `docs/` + paper |
| 材料收录 | `reference/` | A running collection of source papers/material we draw on; not authoritative, grows over time |

**Lifecycle rule:** work starts in `research/` or `papers/notes/drafts/`; once it matures
into a team-accepted conclusion it is promoted into `papers/notes/accepted/` (with a status
update), and a conclusion that enters the paper body marks its notes entry `archive/`.

### Where Layers Live

Environment Integration Layers are deliberately **not** part of the Core package tree. The build root
`layers/` exists; the shared core is grouped under `kit/` so the distinction "shared core vs
environment implementation" is visible on disk ([decision record](papers/notes/accepted/decision-layers-directory-layout.md)):

```text
layers/                          # one Gradle build root, several modules
├── kit/                         # shared, environment-agnostic (pure JVM)
│   └── protocol/  runtime/  transport/
├── minecraft/                   # Minecraft Layer — the only module with paper-api
├── simulator/                   # fake environment — control condition (constraint C4)
└── testclient/                  # vertical-slice test client
```

> **Landed 2026-09-14 (commit `ead3a3d`)**: the `kit/` regroup is done — `layers/kit/{protocol,runtime,transport}`
> plus `minecraft/`, `simulator/`, `testclient/`; the boundary guards were re-pointed to `kit/*` and
> hardened with a "zero files scanned ⇒ fail" check. 20 unit tests pass; the shadow plugin jar builds.

Later, when a Layer earns its own release cycle, `layers/minecraft/` moves out to become the
standalone repo `macha-minecraft` (triggers: T1–T4 in the same record).

The rule that makes the split worth it: **adding a Layer must not require changing Macha Core.**
Rationale and audit:
[`papers/notes/drafts/environment-integration-layer.md`](papers/notes/drafts/environment-integration-layer.md) §E.

---

## Quick Start (Placeholder)

```bash
# Create a virtual environment
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Run smoke tests
pytest
```

> Concrete runnable examples will be added after the Phase 3 cognitive-core MVP completion.
> Phase 1–2 produce the Layer track (protocol, Stub Core, Minecraft + simulator Layers), not examples.

---

## Documentation Navigation

- [Repository Initialization Checklist](docs/initialization.md)
- [Team R&D Workflow (Hard Rules)](docs/team-workflow.md)
- [Research Methodology v1.0](docs/research-methodology.md) — evidence levels, pre-registration, gates
- [Research Methodology — Design Notes](docs/research-methodology-design.md) — audit, rejected designs, red team
- [Literature Intelligence Plan](research/plans/literature-intelligence-plan.md)
- [Literature Map → Paper Gap Mapping](research/literature/00-literature-map-paper-gaps.md)
- [Research Positioning and Paper Differences](docs/research/positioning.md)
- [Preliminary Technical Direction](docs/research/direction.md)
- [Team Information Collection Checklist (retired → see plans)](docs/retired/information_needs.md)
- [Prototype Portrait](docs/prototype_portrait.md)
- [Target Architecture](docs/architecture.md) — includes the Environment Integration Layer boundary
- [Environment Integration Layer (draft note)](papers/notes/drafts/environment-integration-layer.md)
- [Minecraft Layer Validation Plan (draft, CN)](research/plans/minecraft-layer-validation-plan.md)
- [Development Roadmap](docs/roadmap.md)

---

## License

[MIT](LICENSE)
