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
├── reference/                 # PDFs of the four core papers
├── papers/                    # Papers and idea drafts written by the team
├── announcements/             # Public experiment announcements
├── docs/
│   ├── research/
│   │   ├── positioning.md     # Positioning of the four papers and our entry point
│   │   └── direction.md       # Preliminary technical direction and project proposal
│   ├── architecture.md        # Target architecture sketch
│   └── roadmap.md             # Development roadmap
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
├── examples/
│   └── hello_agent.py
└── tests/
    └── test_smoke.py
```

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
- [Research Positioning and Paper Differences](docs/research/positioning.md)
- [Preliminary Technical Direction](docs/research/direction.md)
- [Team Information Collection Checklist](docs/research/information_needs.md)
- [Prototype Portrait](docs/prototype_portrait.md)
- [Target Architecture](docs/architecture.md)
- [Development Roadmap](docs/roadmap.md)

---

## License

[MIT](LICENSE)
