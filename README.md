# Macha

**Revolutionizing game NPCs!**

Macha is a research and engineering repository for next-generation game NPCs. Our goal is not to build an NPC "that can chat," but to construct an LLM-driven NPC framework with **long-term memory, believable reflection, dynamic planning, and multi-agent collaboration**.

> Current status: repository initialization phase.  
> Research foundation: the four core papers in `reference/`.

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
│   ├── plans/                 #   methodology / collection plans (intelligence plan)
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

> Concrete runnable examples will be added after Phase 1 MVP completion.

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
- [Target Architecture](docs/architecture.md)
- [Development Roadmap](docs/roadmap.md)

---

## License

[MIT](LICENSE)
