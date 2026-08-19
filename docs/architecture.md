# Target Architecture (Draft)

## High-Level View

```text
Game Engine / Environment
        │
        ▼
┌─────────────────┐
│  Perception     │  Convert environment state and player input into structured Observations
└────────┬────────┘
         ▼
┌─────────────────┐
│  Memory         │  Short-term context + long-term experiences + reflection summaries
└────────┬────────┘
         ▼
┌─────────────────┐
│  Reasoning      │  Goal parsing, planning, decision-making, reflection
└────────┬────────┘
         ▼
┌─────────────────┐
│  Action         │  Generate dialogue, game commands, or API calls
└─────────────────┘
```

## Core Module Responsibilities

### Perception

- Input: game state, player messages, events.
- Output: `Observation` (structured description).
- Initially can use text templates; later can connect vision/APIs.

### Memory

- Short-term memory: current session context.
- Long-term memory: important facts, relationships, and reflections across sessions.
- Retrieval: ranked by relevance, recency, and importance.
- Initially use SQLite/JSON; later can connect vector retrieval.

### Reasoning

- Make decisions based on current observations and memory.
- Includes planning (goal decomposition) and reflection (learning from failures/successes).
- Initially can call the LLM, or fall back to rules.

### Action

- Convert decisions into in-game actions or natural language replies.
- Should support "structured output" for easy parsing by the game engine.

## Interface Conventions (Draft)

```python
@dataclass
class Observation:
    content: str
    timestamp: float
    source: str

@dataclass
class MemoryItem:
    content: str
    importance: float
    timestamp: float
    metadata: dict

class BaseAgent:
    def perceive(self, observation: Observation) -> None: ...
    def think(self) -> str: ...
    def act(self) -> str: ...
```

> Detailed interfaces will be implemented incrementally in `src/macha/core/`.
