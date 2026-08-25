# Team Information Collection Checklist (task list for the team)

> Goal: What Macha is building is a **standard skeleton for the game NPC domain**, not a single-point demo.
> Therefore information collection must cover six layers: academic frontier, engineering implementation, industry status, design theory, evaluation benchmarks, and ecosystem standards.

---

## 1. Academic Foundation: Cognitive Architectures and LLM Agents

**Why needed**: A standard skeleton must have its own "cognitive model"; it cannot rely only on prompt engineering.

Please collect:

- [ ] Classic cognitive architectures: survey or introductory materials on Soar, ACT-R, CLARION, LIDA.
- [ ] Foundational LLM-agent papers:
  - ReAct (reasoning combined with action)
  - Reflexion (self-reflection)
  - Tree of Thoughts (search-based reasoning)
  - Voyager (open-world code-based action)
  - Generative Agents (already have, 2304)
  - CAMEL / AutoGen / MetaGPT (multi-agent collaboration)
  - MemGPT / Letta (hierarchical memory)
  - HippoRAG / RAPTOR / GraphRAG (structured memory)
- [ ] LLM game-agent surveys (already have 2404, can supplement with new 2025–2026 surveys).
- [ ] World models, embodied intelligence, and LLM decision-making papers in game environments.

**Expected output**: a comparison table of "Macha cognitive-model candidate solutions."

---

## 2. Engineering Implementation: Existing NPC / Game-AI Architectures

**Why needed**: To replace or be compatible with Behavior Tree, GOAP, HTN, Utility AI, we must know what the existing standards look like.

Please collect:

- [ ] Game-industry standards:
  - Behavior Tree specification and common implementations
  - GOAP (Goal-Oriented Action Planning)
  - HTN (Hierarchical Task Network)
  - Utility AI
  - FSM (Finite State Machine)
- [ ] Game-engine AI capabilities:
  - Unity ML-Agents, Unity Behavior
  - Unreal Engine AI (Behavior Tree, Perception, MassAI, Smart Objects)
  - Godot navigation / behavior modules
- [ ] Open-source NPC frameworks:
  - Inworld AI docs / whitepaper
  - NVIDIA ACE technical docs
  - Convai, Altera, Rival Theory and other public materials
- [ ] Game scripting / mod interfaces:
  - Minecraft (Mineflayer, MCU)
  - Skyrim / Oblivion mod AI
  - RimWorld / Dwarf Fortress / The Sims AI architecture analysis

**Expected output**: "functional boundaries" and a "pain-point list" of the existing NPC tech stack.

---

## 3. Industry Status: Market and Product Research

**Why needed**: A standard skeleton must answer "why the industry needs it," not start only from papers.

Please collect:

- [ ] Game-industry AI reports:
  - Public reports on AI games / NPCs from a16z, Sequoia, Newzoo, Niko Partners, etc.
  - Public shares from big studios like Tencent, NetEase, miHoYo on AI NPCs (if any).
- [ ] Product cases:
  - AI Dungeon (AI GM)
  - Suck Up!, Vaudeville, Infinite Craft (AI-native games)
  - AI NPC deployment cases in domestic games like Justice Online / Naraka: Bladepoint
  - Success / failure experiences of indie circles adopting LLM NPCs.
- [ ] Startup map:
  - Company / product / funding / tech route / partner games.
  - Which companies build "NPC brains," which build "toolchains," which build "platforms."

**Expected output**: a brief on "industry status and competitive landscape," annotating each company's tech route and bottlenecks.

---

## 4. Game Design Theory: NPC Believability and Gameplay

**Why needed**: The standard skeleton serves "designing believable NPCs," not "a stronger chatbot."

Please collect:

- [ ] Design theory:
  - MDA framework (Mechanics-Dynamics-Aesthetics)
  - The Sims design notes (Will Wright et al.)
  - Interactive Drama (Chris Crawford)
  - AI-based Game Design (Eladhari et al.)
  - Classic NPC believability (Believability) papers
- [ ] Game-experience analysis:
  - Why "character consistency" matters in role-playing games
  - What players expect from NPC memory ("what exactly should the NPC remember")
  - NPC behavior differences between open-world and narrative games
- [ ] AI-native game design:
  - Already have 2607; can supplement its concrete case teardown of "semantic adjudication, multi-agent simulation."

**Expected output**: an "NPC believability requirement document" that translates design language into technical metrics.

---

## 5. Evaluation Benchmarks: How to Prove the Skeleton Is a Standard

**Why needed**: Without standard evaluation, there is no standard skeleton.

Please collect:

- [ ] Agent / LLM evaluation benchmarks:
  - AgentBench, ToolBench, WebArena
  - Game-agent benchmarks: MindAgent, SmartPlay, Clembench
  - Long-term memory benchmarks: LoCoMo, LongBench, RULER, etc.
- [ ] Dialogue-quality evaluation:
  - PersonaChat, LIGHT, DSTC related tasks
  - Quantitative methods for character consistency (Role Fidelity)
  - Human-evaluation protocols (TrueSkill, etc.)
- [ ] Game-NPC-specific evaluation:
  - Believability metrics
  - Anti-hallucination / long-term consistency stress-test design
  - Engineering metrics like latency, cost, throughput
- [ ] Interpretability and debuggability:
  - Why players need "predictable NPCs"
  - Existing agent observability tools (LangSmith, Phoenix, etc.)

**Expected output**: Macha's evaluation-dimension table + benchmark dataset list.

---

## 6. Standards and Ecosystem: Interoperability

**Why needed**: To become a "standard skeleton," clear interfaces and protocols must be defined.

Please collect:

- [ ] Interoperability protocols:
  - MCP (Model Context Protocol)
  - OpenAI Function Calling / Anthropic Tool Use
  - Multi-agent communication protocols (FIPA ACL, Agent Communication Languages)
- [ ] Game-industry standard interfaces:
  - ECS (Entity Component System) architecture
  - Common data interfaces between behavior trees / decision modules and game engines
  - Unity / Unreal / Godot plugin specifications
- [ ] Open-source framework design:
  - LangChain / LlamaIndex abstraction style
  - AutoGen / OpenAI Agents multi-agent abstraction
  - "Declarative / modular" design ideas like Haystack, DSPy
- [ ] Model-access standards:
  - OpenAI-compatible API
  - vLLM, llam.cpp, Ollama local service interfaces
  - Deployment schemes like quantization / distillation / speculative decoding

**Expected output**: reference materials for Macha's "standard interface draft."

---

## 7. Safety, Ethics, and Compliance

**Why needed**: An NPC is a long-running "anthropomorphic system," with risks far higher than ordinary software.

Please collect:

- [ ] Safety:
  - LLM prompt-injection attack cases in games
  - NPC jailbreak / character drift
  - Runtime guardrails solutions
- [ ] Ethics:
  - Psychological impact of anthropomorphic NPCs on players
  - Protection of child and minor players
  - Addiction-design ethics
- [ ] Compliance:
  - Applicability of the EU AI Act to game AI
  - China's generative-AI service regulations
  - Privacy protection of player data and conversation content
  - Copyright of AI-generated content (model training data, generated-asset copyright)

**Expected output**: a "Macha risk and compliance checklist."

---

## 8. Data Resources

**Why needed**: Training, fine-tuning, and evaluation all need data.

Please collect:

- [ ] Dialogue datasets:
  - PersonaChat, DailyDialog, LIGHT, CharacterGLM, etc.
- [ ] Game / interaction data:
  - Game logs, player-behavior data, NPC dialogue corpora
  - Text-adventure corpora (e.g., Zork, AI Dungeon public data)
- [ ] Character-setting data:
  - Public character-card / persona datasets
- [ ] Multilingual data (if considering the Chinese market):
  - Chinese dialogue, Chinese role-play datasets

**Expected output**: Macha's usable dataset list + license notes.

---

## Priority Suggestions (do these first)

| Priority | Category | Reason |
|---|---|---|
| P0 | 2. Engineering implementation: existing NPC architectures | Decides whether Macha "replaces" or "is compatible with" existing standards |
| P0 | 5. Evaluation benchmarks | Without evaluation, the standard is meaningless |
| P0 | 3. Industry status | Proves the real need for a "standard skeleton" |
| P1 | 1. Academic foundation | Determines cognitive model and memory architecture |
| P1 | 6. Standards and ecosystem | Decides what the interface looks like |
| P1 | 4. Design theory | Translates design requirements into technical requirements |
| P2 | 8. Data resources | Collect after the architecture direction is clear |
| P2 | 7. Safety, ethics, compliance | Can run in parallel with architecture design |

---

## Format the Team Should Follow When Collecting

To avoid drowning in materials, please submit in the following format:

```text
[Category]Engineering implementation / Academic paper / Industry report / ...
[Title]...
[Link / file path]...
[One-sentence summary]What does it solve? Relationship to Macha?
[Key conclusions]3-5 bullet points
[Reusable things]Architecture diagram? Interface definition? Data? Evaluation method?
```

After collection, first put everything uniformly in the `reference/` or newly created `research/` directory, and register an index at the end of this file.

---

## Research Index

> Registration date: 2026-08-16 | Status: all eight P0–P2 categories completed | Form: each document contains a "source collection" subsection formatted per the team's required six fields ([Category][Title][Link][One-sentence summary][Key conclusions][Reusable things]).
> Cross-document consistency: all documents uniformly connect to the "perception—memory—reasoning—action" skeleton and the "Replace the upper cognitive core / Wrap the lower executor" conclusion in `direction.md` / `positioning.md`.

| Priority | Category | Document title | Path | One-sentence summary |
|---|---|---|---|---|
| P0 | 2. Engineering implementation | "Functional boundaries" and "pain-point list" of the existing NPC tech stack | `docs/research/engineering_npc_architectures.md` | Breaks down BT/GOAP/HTN/Utility/FSM, the three major engine AIs, ACE/Inworld/Convai, and classic simulation games line by line, concluding that Macha should "Replace the cognitive core, Wrap the execution layer." |
| P0 | 5. Evaluation benchmarks | Macha's evaluation-dimension table + benchmark dataset list | `docs/research/evaluation_benchmarks.md` | 13 evaluation dimensions (functional / engineering) × 16 benchmark datasets, with anti-hallucination stress tests and engineering instrumentation suggestions. |
| P0 | 3. Industry status | Industry status and competitive landscape brief | `docs/research/industry_landscape.md` | Demand is validated (60%+ vendor adoption), but locked down by five bottlenecks — cost / latency / controllability / memory / compliance — i.e., Macha's white space. |
| P1 | 1. Academic foundation | "Macha cognitive-model candidate solutions" comparison table | `docs/research/academic_cognitive_models.md` | 7-dimension comparison of Soar/ACT-R/LIDA/Generative Agents/MemGPT/GraphRAG etc., giving a fused cognitive model (MCM) and P0–P3 rollout priorities. |
| P1 | 6. Standards and ecosystem | Standard interface draft reference materials | `docs/research/standards_interop.md` | Surveys MCP/OpenAI API/ECS/A2A etc., giving Macha a six-layer core → de-facto-standard interface mapping master table. |
| P1 | 4. Design theory | NPC believability requirement document | `docs/research/design_theory_believability.md` | Translates MDA / interactive narrative / believability into 11 technical requirements (C1–C11), mapped to Macha's four layers and evaluation dimensions. |
| P2 | 7. Safety, ethics, compliance | Macha risk and compliance checklist | `docs/research/safety_compliance.md` | S1–S9/E1–E8/C1–C8 categorized checklist + China/US/EU regulatory map + compliance-switch design; key alignment with China's "Interim Measures for Anthropomorphic Interaction Services." |
| P2 | 8. Data resources | Macha usable dataset list + license notes | `docs/research/data_resources.md` | 30+ datasets classified by dialogue / game / Chinese / social simulation, with three-tier license-risk labels, and corrected PersonaChat license (CC BY 4.0 not MIT). |

**Next-step suggestion**: The eight categories of research already provide a factual base for the Macha standard skeleton. Next, the P1 academic cognitive model + P1 standard interface draft can converge into the "Macha Cognitive Core v0.1 Specification," and the P0 evaluation-dimension table can establish the first regression benchmark.

---

## Deepening Registration (2026-08-16 second round: four-dimension additive deepening)

The user found the first round "not comprehensive enough," so eight documents were appended with new sections along four dimensions — breadth + timeliness / technical-spec depth / Chinese-market specialization / quantification and landing (original text not deleted, keeping the Replace/Wrap framework and six-field source format):

| Category | Document | Newly added deepening points |
|---|---|---|
| Engineering implementation | `engineering_npc_architectures.md` | §9 Execution adaptation-layer interface draft (ActionDescriptor JSON Schema + adjudication pseudocode + cloud/local cost-latency comparison); domestic cases (NetEase Fuxi / Tencent / miHoYo / Kaiying / ByteDance); open-source roadmap and replacement-cost estimate |
| Evaluation benchmarks | `evaluation_benchmarks.md` | Chapter 7 evaluation harness spec (config schema + reference scorer pseudocode + 9 quantitative SLOs: p95<800ms, cost<$0.002, consistency>0.85, hallucination<2%); 2025–2026 new benchmarks; domestic evaluation + v0.1 three-tier access list |
| Industry status | `industry_landscape.md` | §5 Quantified market and domestic specialization (market size / CAGR, real funding-table amounts, cost structure $/MAU, domestic deep-dive cases + tech-route × bottleneck diagram) |
| Academic foundation | `academic_cognitive_models.md` | MCM v0.1 component spec (9 module interfaces + memory-layering JSON Schema + perceive→reflect→plan→act pseudocode + retrieval p95<50ms) |
| Standards ecosystem | `standards_interop.md` | §9 Four interface drafts (MCP NPC Server / OpenAI-compatible function / ECS NPCBrainComponent / A2A message schema) + domestic large-model API compatibility table + latency budget |
| Design theory | `design_theory_believability.md` | Section 9 character-card Schema (JSON) + C1–C11 quantifiable-metric mapping + narrative-consistency test scenarios + domestic cases |
| Safety & compliance | `safety_compliance.md` | Guardrail pipeline (Input/Output dual-layer filter schema + injection-detection heuristics + pseudocode) + 14 red-team cases + clause-level China/US/EU mapping + quantitative targets (filter<30ms, ASR≤5%) |
| Data resources | `data_resources.md` | Section 8 training/evaluation data JSON schema + six-stage synthetic-data pipeline + Macha v0.1 starter bundle (~33M tokens) + Chinese-dataset specialization |

All deepening sources are registered in six-field format; links not verified against primary sources are explicitly labeled, and no URLs are fabricated.
