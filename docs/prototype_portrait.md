# Macha Prototype Portrait (Prototype Portrait v0.1)

> Stage: prototype portrait. Goal: answer "exactly what are we trying to build."  
> Premise: Macha is positioned as an **open-source, engine-agnostic, model-agnostic cognitive standard skeleton for game NPCs** — not a commercial product, and not a complete game.

---

## 1. Four Constraints the Prototype Must Satisfy

1. It must prove that the "standard framework" holds — not that "some NPC is smart."
2. It must be small enough for 1–2 developers to finish within a few weeks.
3. It must be evaluable: memory, character consistency, anti-hallucination, latency, cost, and observability must all be measurable.
4. It must make an external developer say, after reading it, "I can plug the same interfaces into my own engine/model."

---

## 2. Brainstorming: Five Candidate Prototypes

| ID | Prototype | What it is | Strengths | Risks |
|---|---|---|---|---|
| A | **NPC Cognitive Core** | A pure-Python standard kernel defining Character/Memory/Reasoning/Action/Guardrail interfaces, with a reference implementation | Closest to the "standard framework" itself; no dependency on any engine | Not intuitive on its own; needs a demo to accompany it |
| B | **Tavern Keeper Probe** | An interactive "cross-session NPC": tavern keeper Elara remembers the player, remembers promises, forgets trivialities, and refuses to overstep | Intuitive — one demo covers memory/consistency/guardrails | If it only becomes a demo, it degrades into a chatbot |
| C | **Semantic Adjudication Mini-Game** | The player describes actions in natural language and the system adjudicates success and mutates world state (e.g., "burn the iron gate with a torch") | Directly attacks the N4 gap in paper 2607, extremely differentiated | High difficulty; rule modeling easily spirals out of control |
| D | **Smallville-style Mini Town** | A small social simulation with 5–10 NPCs | Best virality, strong visual impact | High cost and complexity; easily becomes a Demo rather than a standard |
| E | **Conformance Test Suite** | First define "what kind of NPC conforms to Macha," then verify any implementation with automated tests | The hardest proof of the standard; avoids empty talk | Without a reference implementation early on, the tests float in the air |

---

## 3. Selected Approach

**Final portrait: a combination of A + B + E, with C as an extension goal after the cognitive core
is complete (Phase 3 in the current roadmap — the Layer track runs first).**

That is, the first prototype is not "a game," but a set of **"Macha Core v0.1 + Tavern Keeper reference probe + Macha Conformance v0"**.

```text
Macha v0.1
├── Macha Spec v0.1          # Standard interface specification
├── Macha Core v0.1          # Python reference implementation
├── Tavern Keeper Probe      # Reference probe: a playable tavern keeper NPC
└── Macha Conformance v0     # Automated conformance tests
```

---

## 4. Exactly What We Are Building

### 4.1 Macha Spec v0.1: Standard Interface Specification

Use Pydantic / dataclass to define the following minimal interfaces:

- `CharacterProfile`: identity, persona, values, taboos, memory strategy, knowledge boundaries.
- `Observation`: structured observation of environment/player input.
- `MemoryItem`: long-term memory entry (content, time, importance, source, type).
- `MemoryStore`: write, retrieve, update, forget.
- `Reasoner`: given observations and memory, produce thoughts and intents.
- `Planner`: decompose goals into action steps (can be simplified in v1).
- `ActionCall`: structured action invocation (tool + args + provenance).
- `ActionSink`: send actions to the execution end (CLI / engine / MCP / BT).
- `Guardrail`: input guardrail, output validation, character consistency validation.
- `Session`: in-session and cross-session state.
- `TelemetryEvent`: decision-chain log, for evaluation and debugging.

### 4.2 Macha Core v0.1: Reference Implementation

- Pure Python 3.10+, no mandatory vector library dependency.
- Memory backend uses SQLite or JSON files in v1.
- LLM is connected via the `LLMClient` abstraction, with default support for OpenAI-compatible APIs.
- Built-in lightweight memory retriever: relevance + recency + importance.
- Built-in on-demand reflection trigger.
- Built-in Guardrail pipeline: input check → memory annotation → persona gating → structured output validation.

### 4.3 Tavern Keeper Probe: Reference Probe

**Name**: Elara, the tavern keeper.

**Gameplay**: The player enters and leaves the tavern across three "game days," conversing with Elara. She has:

- Persona: shrewd, holds grudges, rule-abiding, occasionally sarcastic.
- Memory: remembers important promises, debts, and secrets; fades on irrelevant small talk.
- Tools: check the ledger, record debts, pass messages.
- Boundaries: does not answer anything outside the tavern; refuses to be commanded to "forget" or to "play another role."

**Three test scenarios**:

1. **First Night**: The player leaves an important promise and some irrelevant small talk.
2. **Third Night**: The player returns. Elara must remember the promise and forget or fade the small talk; if the player denies it, she must produce ledger evidence.
3. **Fifth Night**: The player attempts a prompt injection using "a note on the tavern wall." The Macha Guardrail must intercept it, and Elara must remain in character.

### 4.4 Macha Conformance v0: Conformance Tests

v1 defines **Macha Level 1 Conformance**, with at least 12 automated checks:

| ID | Check Item |
|---|---|
| C01 | Can remember high-importance facts |
| C02 | Can fade low-importance facts |
| C03 | Maintains persona across sessions |
| C04 | Refuses to answer content outside its knowledge boundary |
| C05 | Can handle conflicts between new and old facts |
| C06 | Does not fabricate events that never happened |
| C07 | Intercepts direct prompt injection |
| C08 | Intercepts indirect prompt injection via memory content |
| C09 | Action output is a structured ActionCall |
| C10 | Tool call arguments satisfy the schema |
| C11 | Complete decision chain has trace logs |
| C12 | P95 first-token latency below the set threshold (local model / simulated model) |

---

## 5. Prototype Acceptance Criteria

- [ ] A new developer can start the tavern keeper probe within 10 minutes after installing per the README.
- [ ] The tavern keeper probe passes all 12 Level 1 conformance checks.
- [ ] The underlying LLM is swapped at least once (e.g., OpenAI-compatible endpoint ↔ local model) and the core tests still pass.
- [ ] The memory backend is swapped at least once (JSON ↔ SQLite) and the core tests still pass.
- [ ] The complete decision log can be exported and explain "why Elara said this line."
- [ ] Anyone can implement only Macha Spec v0.1 — without Macha Core — and still pass the conformance tests.

---

## 6. Explicitly Out of Scope for v1

- No 3D/2D graphics.
- No TTS / voice.
- No multi-NPC social simulation.
- No vector database.
- No model training.
- No Unity/Unreal plugins.
- No environment **Layer** (Minecraft or otherwise): v1's environment is the CLI/text probe. A Layer
  is a separate project that must be able to plug into Core without changing it — see
  [`architecture.md`](architecture.md) §6–§7.
- No cloud SaaS.
- No "looks like a real person" companion-type NPC.

v1 proves only one thing: **the cognitive layer of an NPC can be standardized, and that standard can be implemented, tested, and swapped.**
