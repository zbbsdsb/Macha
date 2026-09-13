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
├── layers/                    # Environment Integration Layers (planned; see docs/architecture.md)
│   ├── protocol/ runtime/ transport/   #   shared, environment-agnostic
│   ├── minecraft/             #   Minecraft Layer (only module with paper-api)
│   └── simulator/             #   fake environment (control condition)
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

### Where Layers Live **[PENDING]**

Environment Integration Layers are deliberately **not** part of the Core package tree. Planned shape
(no directories created yet — the structure is specified in
[`research/plans/minecraft-layer/04-project-structure.md`](research/plans/minecraft-layer/04-project-structure.md)):

```text
layers/                          # one Gradle build root, several modules
├── protocol/  runtime/  transport/   # shared, environment-agnostic (pure JVM)
├── minecraft/                   # Minecraft Layer — the only module with paper-api
├── simulator/                   # fake environment — control condition (constraint C4)
└── testclient/                  # vertical-slice test client
```

Later, when a Layer earns its own release cycle, `layers/minecraft/` moves out to become the
standalone repo `macha-minecraft`.

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
