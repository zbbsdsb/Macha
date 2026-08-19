# Macha Candidate Cognitive-Model Comparison Table

> **Document positioning**: This file belongs to the Macha "Academic Foundation: Cognitive Architectures and LLM Agents" research category (Class 1), a candidate-solution survey. Target readers are Macha framework designers and implementers.
>
> **How to use this file**:
> 1. **Section 1** is the "Candidate Cognitive-Model Comparison Table," for horizontally comparing classic cognitive architectures and LLM-native agent paradigms on capability characteristics in the NPC context.
> 2. **Section 2** is the "Fusion Suggestion," giving which architecture elements Macha should extract and combine into its own cognitive model, and connecting to the `Perception→Memory→Reasoning→Action` pipeline in `direction.md` and the "Replace cognitive/memory upper layer, Wrap execution lower layer" conclusion in `engineering_npc_architectures.md`.
> 3. **Section 3** is "Source Collection," each source strictly in the six-field format specified by `information_needs.md` (`[Category]/[Title]/[Link]/[One-line summary]/[Key conclusions]/[Reusable]`), for direct reuse in implementation.
>
> **Honesty statement**: All links are actually reachable addresses found during search (mostly arXiv / ACL Anthology / DOI). A few sources could not be independently confirmed to original URL via secondary search; such entries explicitly mark "could not independently verify" rather than fabricate. Future-dated (e.g., 2026) arXiv/conference entries are published/accepted versions returned on the search date, not fiction.

---

## 0. Evaluation Coordinate System (Read This First)

Macha's NPC is not a "single-turn chatbot," but a **long-lifecycle, continuously-evolving, pluggable-engine-driven** cognitive entity. Therefore the horizontal dimensions of the comparison table are fixed to these 7 items:

| Dimension | Meaning (for NPC context) |
|---|---|
| Memory mechanism | How to encode, store, retrieve, forget, and update experience (episodic/semantic/procedural) |
| Reflection / metacognition | Whether it has introspection and correction of its own state, memory, behavior |
| Planning | Goal decomposition, long-horizon planning, dynamic adjustment, sub-goal management |
| Sociality | Inter-individual communication, role differentiation, relationship tracking, group emergence |
| Scalability | Compute and engineering cost curve from single NPC to hundreds/ten-thousands of NPCs |
| LLM-native fit | Degree of natural fusion with LLM prompt/retrieval/tool-calling paradigms |
| Applicability to Macha | Feasibility under the `Perceive→Think→Act` skeleton and the "Replace upper / Wrap lower" strategy |

> Note: "High LLM-native fit" ≠ necessarily optimal. Classic cognitive architectures (Soar/ACT-R) have low fit, but their ideas of **memory layering, reflection loops, production systems** have been proven mappable to LLM agents by frameworks like CoALA, and are the "theoretical parent" of Macha's conceptual design.

---

## 1. Candidate Cognitive-Model Comparison Table

### 1.1 Classic Cognitive Architectures (theoretical parent)

| Architecture | Memory mechanism | Reflection / metacognition | Planning | Sociality | Scalability | LLM-native fit | Applicability to Macha |
|---|---|---|---|---|---|---|---|
| **Soar** | Working memory (short-term) + long-term procedural/semantic memory; consolidation via "impasse → chunking" | Strong: automatically enters "reflection/learning" state when no operator (impasse → chunking) | Strong: goal stack + operator selection + subgoals | Weak (single-agent, needs external extension) | Medium (symbolic system, scale limited by engineering) | Low (symbolic production system, not LLM paradigm) | Medium-high: reflection/metacognition loop and "impasse → learning" mechanism borrowable as NPC self-correction loop |
| **ACT-R** | Modular memory (declarative + procedural), retrieval by activation spreading | Medium: indirectly via conflict monitoring | Medium: goal module driven | Weak | Medium | Low | Medium: memory "activation/retrieval-probability" model mappable to memory-importance scoring |
| **CLARION** | Explicit + implicit dual system (top symbolic / bottom connectionist) | Medium: knowledge extraction and transformation between dual systems | Medium | Weak | Medium | Low | Medium: dual-process (intuition/reflection) idea echoes PersonaForge's System1/2 |
| **LIDA** | Based on Global Workspace + perception loop; episodic/semantic/procedural memory | Strong: consciousness loop naturally contains "introspection" | Medium: behavior graph + context selection | Weak | Medium | Low | Medium: global workspace usable as gating mechanism for "current conscious content" |

### 1.2 LLM-Native Agent Paradigms (near-term parent)

| Architecture / paradigm | Memory mechanism | Reflection / metacognition | Planning | Sociality | Scalability | LLM-native fit | Applicability to Macha |
|---|---|---|---|---|---|---|---|
| **Generative Agents (Smallville, 2304)** | Memory stream (observation→reflection→plan three layers) + retrieval + forgetting | Strong: explicit "reflection" generates high-level insight | Strong: plan tree + daily/hourly plan | Strong: emergent social among 25 NPCs | Medium (few NPCs; 10k-scale needs rework) | High | **Extremely high**: direct prototype of Macha's memory/reflection/planning trio |
| **ReAct (2210)** | No independent memory (relies on context) | Weak | Medium: reason-act interleave | Weak | High (single agent) | Extremely high | High: reason-act interleaving interface paradigm directly usable as `think()` skeleton |
| **Reflexion (2303)** | Verbalized self-feedback + episodic memory | Strong: verbalized reflection on failure, written to memory | Medium | Weak | High | Extremely high | High: failure→reflection→retry loop is template for NPC behavior self-correction |
| **Tree of Thoughts / Voyager (2305)** | Voyager: skill library (procedural memory) | Medium (auto curriculum) | Strong: skill combination, exploratory planning | Weak | High | High | Medium: skill-library concept mappable to NPC "procedural memory/habits" |
| **CoALA (2309)** | Semantic/episodic/procedural three memory types + retrieval | Strong: decision loop contains reflection and update | Strong: explicit decision loop | Medium (framework layer, not implementation) | Depends on implementation | High (theoretical framework, deliberately aligned to LLM) | **Extremely high**: directly gives unified terminology of "LLM agent as cognitive architecture," conceptual base of Macha |
| **MemGPT / Letta (2310)** | Layered virtual context (main context + external storage + recursive summary) | Medium: self-managed context "paging" | Weak (memory-management-leaning) | Weak | High (context-overflow management) | Extremely high | High: layered memory + autonomous retrieve/write is engineering exemplar for Macha memory layer |
| **HippoRAG / HippoRAG 2 (2405/2502)** | Knowledge graph + personalized PageRank "memory index" | Weak (retrieval-augmented) | Weak | Weak | High | High | Medium-high: graph-associating memory, multi-hop reasoning, fits NPC long-term knowledge evolution |
| **RAPTOR / GraphRAG (2401/2404)** | Tree/graph recursive summary | Weak | Weak | Weak | High | High | Medium: global summary tree usable for NPC macro-cognition of "world/community" |
| **PersonaForge (ACL 2026)** | Three-layer persona + introspective monologue (Inner Monologue) | Strong: defense mechanisms as programmable cognitive strategy | Medium | Medium (persona consistency) | Medium-high | High | **High**: directly targets "persona consistency / persona drift," Macha MVP's core pain point |
| **DREAM (KDD 2026)** | Event-aware memory graph (EMG, inspired by ABC cognitive model) | Medium (temporal-causal memory) | Weak | Medium (narrative consistency) | Medium | High | **High**: time-causal coherent memory for established characters, extremely NPC-fitting |
| **RoleMemo / DualMem (2026)** | Dual-stream memory: factual cognition + persona-conditioned insight (reconstructive memory) | Medium | Weak | Medium | Medium (incl. fine-tuning) | High | High: "memory is reconstruction not neutral fact" directly hits Macha persona consistency |
| **5Ws narrative episodic memory (2025)** | 5Ws memory unit + importance scoring + forgetting curve | Medium (memory reconstruction) | Weak | Medium (player-specific tuning) | Medium | High | **High**: designed for game NPCs, directly usable as Macha episodic-memory schema |
| **Concordia / AgentSociety (2312/2025)** | Platform-level shared memory | Platform-level | Platform-level | Strong (large-scale society) | High (10k-scale) | Medium | Medium: provides multi-NPC simulation base, but leans "sandbox" not "single-NPC skeleton" |

### 1.3 Cross-Dimension Summary (for Section 2 extraction)

| Dimension | Strongest candidate | How Macha uses it |
|---|---|---|
| Memory layering | MemGPT / CoALA three memory types | As layered schema of Macha `Memory` module |
| Reflection loop | Generative Agents / Reflexion / Soar | As metacognition sub-step of `Reasoning` module |
| Planning | Voyager / Generative Agents / CoALA | As goal-management sub-step of `Reasoning` |
| Persona consistency | PersonaForge / RoleMemo / DREAM | As persona constraint of `Memory` + `Reasoning` |
| Sociality | Generative Agents / Concordia | As multi-NPC extension layer (not required for MVP) |
| Long-term evolution | 5Ws / HippoRAG | As forgetting/importance/graph-association mechanism |

---

## 2. Macha Cognitive-Model Fusion Suggestion (recommended synthesis)

### 2.1 Design Principles (continuing existing conclusions)

1. **Skeleton alignment**: Macha's runtime skeleton is `Perception → Memory → Reasoning → Action` (`architecture.md` / `direction.md`). All cognitive elements must land within these four modules' semantic boundaries.
2. **Replace / Wrap layering**: per the core conclusion of `engineering_npc_architectures.md` — **Macha itself implements (Replace) the cognitive/memory/reflection/persona upper layer, and wraps (Wrap) the execution layer (BT/GOAP/HTN/Utility and commercial engines)**. Therefore this file's "cognitive model" defines only the upper layer, not action-execution details.
3. **MVP focus**: `direction.md` clearly states MVP = single-NPC long-term memory + persona consistency. Complex sociality, world-model simulation left as extension layer.

### 2.2 Recommended composite cognitive model (Macha Cognitive Model, MCM)

Extract and stitch the non-overlapping strengths of candidate solutions into an LLM-native, pluggable cognitive model:

```
                 ┌─────────────────────────────────────────┐
   Observation → │  PERCEPTION (Wrap: visual/voice/event input)│
                 └───────────────────┬─────────────────────┘
                                     ▼
                 ┌─────────────────────────────────────────┐
                 │  MEMORY (Replace: layered + reconstructive memory)│
                 │  • Procedural memory (habits/skill library, Voyager-inspired)│
                 │  • Semantic memory (world/self knowledge, HippoRAG graph)│
                 │  • Episodic memory (5Ws unit + importance + forgetting)│
                 │  • Persona-conditioned dual stream (DualMem: fact+insight)│
                 └───────────────────┬─────────────────────┘
                                     ▼
                 ┌─────────────────────────────────────────┐
                 │  REASONING (Replace: CoALA decision loop)│
                 │  1) Retrieve relevant memory (MemGPT auto-paging)│
                 │  2) Reflection/metacognition (GA reflection + Reflexion)│
                 │  3) Planning (goal stack + subgoal decomposition)│
                 │  4) Persona gating (PersonaForge introspective monologue)│
                 │  5) Produce intention/action proposal│
                 └───────────────────┬─────────────────────┘
                                     ▼
                 ┌─────────────────────────────────────────┐
                 │  ACTION (Wrap: BT/GOAP/HTN/Utility/engine)│
                 │  translate "intention" into executable action; result feeds back to memory│
                 └─────────────────────────────────────────┘
```

**Key combination points (each says clearly "taken from whom, why"):**

- **Memory layering from CoALA + MemGPT**: CoALA gives unified terminology of procedural/semantic/episodic memory; MemGPT gives engineering-friendly layering of "main context + external storage + recursive summary." Macha `Memory` module thus splits into three storage tiers + a "memory manager" responsible for autonomous retrieve/write/summary.
- **Episodic-memory schema from 5Ws + DREAM**: 5Ws (Who/What/When/Where/Why) unit + importance scoring + Wickelgren forgetting curve is the minimal landing schema for game NPCs; DREAM's "event-aware memory graph (EMG) + temporal-causal" supplements long-term narrative coherence; together they define episodic-memory encoding and retrieval.
- **Reconstructive memory from RoleMemo/DualMem**: memory should not be neutral fact but carry persona perspective (a "psychologist NPC" and a "ordinary-friend NPC" remember the same event differently). Macha's memory-write stage forces a "persona-conditioned interpretation" sub-step.
- **Reflection loop from Generative Agents + Reflexion + Soar**: GA's "observation→reflection→plan" three layers, Reflexion's "failure→verbalized reflection→retry," Soar's "impasse→insightful learning" unified in Macha into an optional, throttlable (see PersonaForge selective dual-process) metacognition sub-step.
- **Planning from CoALA + Voyager**: goal stack + subgoal decomposition + skill-library retrieval. MVP stage only single-NPC single-goal planning; multi-goal/collaborative planning left to extension layer.
- **Persona gating from PersonaForge**: add a "persona inner monologue" gate at the end of Reasoning, suppressing drift. PersonaForge proves this mechanism cuts 50-turn persona drift from 24.8% to 6.3%, and the orthogonal Big Five + defense-mechanism constraints are directly reusable.
- **Sociality left as extension layer**: Generative Agents / Concordia multi-NPC social mechanisms don't enter MVP, but `Memory` and `Reasoning` interfaces must reserve "relationship/community" fields to avoid later refactoring.

### 2.3 Interface contract with the execution layer (Wrap)

The cognitive layer only produces **structured intention** (e.g., `ActionProposal{goal, sub_goals, constraints, persona_constraints}`), consumed by the execution layer (BT/GOAP/HTN/commercial engine). This boundary guarantees:

- Cognitive model decoupled from specific game engine (satisfies Macha "standard skeleton / reusable framework" positioning);
- Different execution strategies pluggable without changing the cognitive layer (lands `engineering_npc_architectures.md`'s Wrap conclusion).

### 2.4 Parts not recommended for direct adoption (pitfalls to avoid)

- **Do not copy Soar/ACT-R symbolic production systems** as runtime: conflicts with LLM paradigm, only borrow their "reflection/memory-activation" ideas.
- **Do not bring video-generative world models (Sora-class) into MVP**: compute cost and real-time mismatch single-NPC real-time interaction; world model only as "extension research" direction (see world-model items in Section 3).
- **Do not set reflection/scoring frequency to fixed high frequency**: PersonaForge's selective dual-process proves 13.4% token overhead retains 96% performance; Macha should do "on-demand reflection" throttling.

---

## 3. Source Collection (six-field format)

> Format strictly follows `information_needs.md`: each item has `[Category]/[Title]/[Link]/[One-line summary]/[Key conclusions]/[Reusable]`.

---

### [Category]Academic paper (survey)
[Title]40 Years of Cognitive Architectures: Core Cognitive Abilities and Practical Applications
[Link/FilePath]https://arxiv.org/abs/1610.08602
[One-line summary]Systematically classifies and compares cognitive architectures over 40 years, authoritative map for classic-architecture (Soar/ACT-R/CLARION/LIDA etc.) selection.
[Key conclusions]
1. Proposes classification dimensions for cognitive architectures (symbolic/connectionist/hybrid, whether includes learning/memory/planning, etc.).
2. Points out most architectures are generally weak in "sociality" "scalability" — exactly where LLM agents can reinforce.
3. Summarizes core cognitive-capability list (perception, memory, reasoning, learning, action), highly corresponding to Macha's four modules.
4. Emphasizes convergence of "standard mind model" (many architectures share working/long-term memory/decision loop).
[Reusable]Architecture-capability comparison table (directly becomes Table 1.1 of this file); "core cognitive-capability list" as Macha module-division basis.

---

### [Category]Academic paper (cognitive-science foundation)
[Title]The Common Model of Cognition (Standard Model of the Mind)
[Link/FilePath]https://doi.org/10.1609/aimag.v38i4.2744 (Laird, Lebiere, Rosenbloom, AI Magazine 2017)
[One-line summary]"Standard mind model" distilled from consensus of mainstream architectures (ACT-R, Soar, Sigma), defines unified skeleton of perception-memory-decision-action.
[Key conclusions]
1. Most modern cognitive architectures share the same core structure: perception, working memory, long-term memory, decision/action.
2. Long-term memory splits declarative/procedural, working memory capacity limited needs "paging/retrieval."
3. This model provides common language for "migrating cognitive-architecture ideas to LLM agents."
[Reusable]Unified skeleton diagram (directly maps to Macha's Perception→Memory→Reasoning→Action); memory-layering terminology.

---

### [Category]Academic paper (LLM agent theoretical framework)
[Title]Cognitive Architectures for Language Agents (CoALA)
[Link/FilePath]https://arxiv.org/abs/2309.02427 (Sumers, Yao, et al.; TMLR)
[One-line summary]Explicitly treats LLM agents as a cognitive architecture, proposes procedural/semantic/episodic three memory types and explicit decision loop, conceptual base of Macha.
[Key conclusions]
1. LLM agent = an implementation of cognitive architecture, should use unified terminology (memory, decision loop, action).
2. Memory in three types: procedural (skill/habit), semantic (knowledge), episodic (experience).
3. Decision loop = retrieve → reflect/update → plan → act.
4. Almost one-to-one corresponds to Macha's Memory/Reasoning module division.
[Reusable]Decision-loop pseudocode; three-memory definition; directly as theoretical basis for Macha cognitive-layer interface spec.

---

### [Category]Academic paper (cognitive architecture × LLM bridge)
[Title]Cognitive Design Patterns: Bridging Cognitive Architectures and LLM Agents
[Link/FilePath]https://arxiv.org/abs/2505.07087 (Wray, Kirk, Laird; 2025)
[One-line summary]Translates mature design patterns of classic cognitive architectures (reflection, memory consolidation, metacognition) into "cognitive design patterns" landable in LLM agents.
[Key conclusions]
1. Mature patterns of classic cognitive architectures directly migratable to LLM agents, no reinvention needed.
2. Gives reusable "pattern cards" (e.g., reflection loop, memory retrieval, goal management).
3. Emphasizes patterns decoupled from specific LLM/engine, fitting Macha's Replace/Wrap strategy.
[Reusable]Cognitive design-pattern list (can become Reasoning sub-step templates of Macha); complements CoALA.

---

### [Category]Academic paper (LLM agent foundation)
[Title]ReAct: Synergizing Reasoning and Acting in Language Models
[Link/FilePath]https://arxiv.org/abs/2210.03629
[One-line summary]Proposes "reason-act" interleaving paradigm (Thought → Action → Observation), becoming the most mainstream runtime skeleton for LLM agents.
[Key conclusions]
1. Interweaves chain-of-thought with tool calling, significantly raising task success and interpretability.
2. Extremely simple interface, naturally fits as base loop of Macha `think()`.
3. Itself has no long-term memory, needs combination with memory layer.
[Reusable]Thought-Action-Observation interaction protocol (can be method-signature reference for `BaseAgent.think/act`).

---

### [Category]Academic paper (reflection / metacognition)
[Title]Reflexion: Language Agents with Verbal Reinforcement Learning
[Link/FilePath]https://arxiv.org/abs/2303.11366
[One-line summary]Lets agents write failure experience back to memory in natural language and self-reflect, forming "failure→reflection→retry" loop.
[Key conclusions]
1. Verbalized self-feedback fits LLM-agent metacognition better than numeric reward.
2. Reflection written to episodic memory, retrieved before next task, reduces repeated mistakes.
3. Mutually corroborated with Generative Agents' reflection mechanism.
[Reusable]"Reflection writes to memory" prompt-template paradigm; can be one implementation of Macha Reasoning metacognition sub-step.

---

### [Category]Academic paper (planning)
[Title]Tree of Thoughts: Deliberate Problem Solving with Large Language Models
[Link/FilePath]https://arxiv.org/abs/2305.10601
[One-line summary]Models reasoning as tree search, allowing branching, backtracking, evaluation, raising complex-planning ability.
[Key conclusions]
1. Compared to linear CoT, ToT supports exploration and backtracking.
2. Fits scenarios needing long-horizon planning, but token cost higher.
3. Can be "deep mode" of Macha planning sub-step (enabled on demand).
[Reusable]Branch-evaluate-backtrack planning control flow; consistent with on-demand-reflection throttling strategy.

---

### [Category]Academic paper (skill / procedural memory)
[Title]Voyager: An Open-Ended Agent with Large Language Models
[Link/FilePath]https://arxiv.org/abs/2305.16291
[One-line summary]Proposes "skill library" as procedural memory in Minecraft, accumulating reusable abilities via auto curriculum.
[Key conclusions]
1. Procedural memory externalized as "skills," retrievable and combinable.
2. Auto curriculum drives snowball ability growth.
3. Skill-library concept mappable to NPC "habit/ability" module.
[Reusable]Skill-library schema (name/code/description/applicability); reference for Macha procedural memory.

---

### [Category]Academic paper (NPC agent prototype)
[Title]Generative Agents: Interactive Simulacra of Human Behavior
[Link/FilePath]https://arxiv.org/abs/2304.03442 (Park et al., 2023)
[One-line summary]25 LLM-driven NPCs spontaneously emerge social behavior in sandbox, proposes "memory stream + reflection + plan" trio, direct prototype of Macha memory/reflection/planning.
[Key conclusions]
1. Memory stream three layers: observation → reflection (high-level insight) → plan (tree, time-sliced).
2. Retrieval weighted by "recency + importance + relevance."
3. Reflection generates summary memory, supports long-horizon consistency and social emergence.
4. Only ~25 NPCs, scale scalability not fully verified.
[Reusable]Memory-reflection-plan trio structure; retrieval-scoring formula; directly as start of Macha single-NPC cognitive loop.

---

### [Category]Academic paper (multi-agent framework)
[Title]CAMEL: Communicative Agents for "Mind" Exploration
[Link/FilePath]https://arxiv.org/abs/2303.17760
[One-line summary]Proposes role-based multi-agent collaboration (AI user / AI assistant) self-driven dialogue framework.
[Key conclusions]
1. Role division + self-driven task advance, can simulate collaboration.
2. Exposes role "drift/out-of-control" risk, needs guardrails.
3. Methodological value for Macha's multi-NPC collaboration extension layer.
[Reusable]Role-based dialogue protocol; task self-driven loop template (extension-layer reference).

---

### [Category]Academic paper (multi-agent framework)
[Title]AutoGen: Enabling Next-Gen LLM Applications via Multi-Agent Conversation
[Link/FilePath]https://arxiv.org/abs/2308.08155 (Microsoft)
[One-line summary]Framework for orchestrating multi-agent dialogue, supporting human-in-the-loop and code execution, engineering-leaning base.
[Key conclusions]
1. Agents can dialogue, call tools, nest.
2. Provides conversation orchestration and observability, high engineering maturity.
3. Leans "framework" not "cognitive model," Macha can borrow its interface design not built-in cognition.
[Reusable]Agent dialogue/tool-call interface design; consistent with Macha Wrap-layer idea (execution orchestration externalized).

---

### [Category]Academic paper (multi-agent framework)
[Title]MetaGPT: Meta Programming for Multi-Agent Collaborative Framework
[Link/FilePath]https://arxiv.org/abs/2308.00352
[One-line summary]Embeds software-engineering pipeline (requirement→design→code) into multi-agent collaboration, emphasizes "structured role and artifact."
[Key conclusions]
1. Constrains agent collaboration with standardized "artifact/stage," reducing mess.
2. Role-responsibility-artifact paradigm referenceable for NPC social division.
3. Weakly related to Macha single-NPC skeleton, leans collaboration engineering.
[Reusable]"Role→responsibility→artifact" structured collaboration paradigm (multi-NPC extension-layer reference).

---

### [Category]Academic paper (layered memory)
[Title]MemGPT: Towards LLM as an Operating System (Letta)
[Link/FilePath]https://arxiv.org/abs/2310.08560
[One-line summary]Applies OS virtual-memory idea to LLM context management: main context + external storage + recursive summary + autonomous paging.
[Key conclusions]
1. Context overflow solved via "layered virtual context," not simple truncation.
2. Agent can autonomously decide when to retrieve/write/summary memory.
3. Directly corresponds to Macha `Memory` module's engineering implementation paradigm.
[Reusable]Layered memory-management scheme (main context/external storage/summarizer); autonomous-paging control logic.

---

### [Category]Academic paper (memory index / graph)
[Title]HippoRAG: Neurobiologically Inspired Long-Term Memory for Retrieval Augmented Language Models
[Link/FilePath]https://arxiv.org/abs/2405.14831
[One-line summary]Uses knowledge graph + personalized PageRank to simulate human memory index, multi-hop, cross-document long-horizon memory retrieval.
[Key conclusions]
1. Organizes memory as graph, supports "associative/multi-hop" retrieval.
2. Personalized PageRank simulates associative activation of memory.
3. HippoRAG 2 (https://arxiv.org/abs/2502.14802) further enhances online learning and context awareness.
[Reusable]Memory-graph schema + associative-retrieval algorithm; fits NPC long-term knowledge-evolution semantic-memory layer.

---

### [Category]Academic paper (recursive-summary memory)
[Title]RAPTOR: Recursive Abstractive Processing for Tree-Organized Retrieval
[Link/FilePath]https://arxiv.org/abs/2401.18059
[One-line summary]Bottom-up recursive tree summary, balancing detail and global semantics, raising long-text retrieval.
[Key conclusions]
1. Tree summary lets agent take both detail and macro theme.
2. Fits "world/community"-level macro cognition.
3. Complements GraphRAG (tree vs graph).
[Reusable]Tree-summary construction and retrieval flow; usable for NPC macro memory of "world/community."

---

### [Category]Academic paper (graph memory)
[Title]From Local to Global: A Graph RAG Approach
[Link/FilePath]https://arxiv.org/abs/2404.16130 (Microsoft)
[One-line summary]Uses graph structure for global retrieval augmentation, from local entity extraction to global community summary.
[Key conclusions]
1. Graph + community detection supports high-quality "global question" answers.
2. Engineering mature, has reference implementation.
3. Leans knowledge-base QA, referenceable for NPC long-term world-knowledge modeling.
[Reusable]Graph-extraction + community-summary pipeline; optional implementation for NPC semantic memory.

---

### [Category]Academic paper (memory survey)
[Title]From Human Memory to AI Memory: A Survey on Memory Systems in LLM Agents
[Link/FilePath]https://arxiv.org/abs/2504.15965
[One-line summary]Systematically reviews LLM-agent memory systems (type, structure, operation, evaluation), selection overview for Macha memory layer.
[Key conclusions]
1. Summarizes memory perception/storage/retrieval/forgetting/update full lifecycle.
2. Compares multiple memory architectures (vector/graph/tree/layered) pros and cons.
3. Gives memory-evaluation benchmark directions, connecting to Macha evaluation layer.
[Reusable]Memory full-lifecycle classification; can be Macha `Memory` module design checklist.

---

### [Category]Academic paper (game-agent survey)
[Title]A Survey on Large Language Model-Based Game Agents
[Link/FilePath]https://arxiv.org/abs/2404.02039 (Hu et al.; ACM Computing Surveys, 2026; current v4/v5)
[One-line summary]Reviews LLM game agents with unified reference architecture, single-agent layer focuses memory/reasoning/perception-action, multi-agent layer focuses communication and organization, gives game-type→agent-need classification.
[Key conclusions]
1. Single-agent three cores: memory, reasoning, perception-action interface — highly isomorphic to Macha skeleton.
2. Multi-agent: communication protocol + organization model supports role differentiation and large-scale social behavior.
3. Sums agent needs by six game types (adventure/communication/competition/cooperation/simulation/manufacturing-exploration).
4. Companion list https://github.com/git-disl/awesome-LLM-game-agent-papers .
[Reusable]"Memory-reasoning-perception-action" reference architecture diagram (directly aligns Macha); game-type→capability-need mapping (for acceptance criteria).

---

### [Category]Academic paper (role-playing agent)
[Title]PersonaForge: Psychology-Grounded Dual-Process Architecture for Personality-Consistent Role-Playing Agents
[Link/FilePath]https://aclanthology.org/2026.findings-acl.386 (ACL 2026 Findings)
[One-line summary]Uses "three-layer persona + dual-process generation (introspective monologue)" to solve LLM long-term persona drift, 50-turn drift from 24.8% to 6.3%.
[Key conclusions]
1. Orthogonally-constrainable psychology (Big Five + defense mechanisms) beats natural-language description, reduces drift.
2. High-dimensional persona constraint needs "cognitive workspace (Inner Monologue)" to dissolve production conflicts.
3. Selective dual-process: 13.4% token overhead retains 96% performance — proves reflection throttlable.
4. Generalizes well on 88 characters + RoleBench external validation.
[Reusable]Three-layer persona schema; introspective-monologue gating template; defense-mechanism-as-programmable-cognitive-strategy setting (extremely reusable, hits MVP persona consistency).

---

### [Category]Academic paper (role-playing memory)
[Title]DREAM: LLM-based Dynamic Role-playing via Event-Aware Memory Graph
[Link/FilePath]https://arxiv.org/abs/2608.05170 (KDD 2026)
[One-line summary]Inspired by ABC cognitive model, turns text into "event-aware memory graph (EMG)," achieving established characters' time-causal coherence.
[Key conclusions]
1. Memory graph organized by time order + causal links for character experience.
2. Dual-granularity character profile: stable persona traits + event-driven behavior evolution.
3. Proposes TCM benchmark for temporal consistency and long-horizon causal narrative coherence.
4. Reaches SOTA on CoSER / LIFECHOICE / TCM.
[Reusable]EMG memory-graph schema; TCM evaluation idea (usable for Macha persona/narrative consistency tests).

---

### [Category]Academic paper (role-playing memory)
[Title]From Facts to Insights: A Persona-Driven Dual Memory Framework and Dataset for Role-Playing Agents (RoleMemo / DualMem)
[Link/FilePath]https://arxiv.org/abs/2605.25693
[One-line summary]Argues memory is "reconstruction" not neutral fact, proposes fact-cognition + persona-conditioned-insight dual-stream memory, raising long-term persona fidelity.
[Key conclusions]
1. Existing "persona-agnostic summary" records fact but loses character perspective, harming fidelity.
2. DualMem decouples into "fact stream" and "persona-conditioned insight stream" two paths.
3. 4B model via SFT+RL surpasses DeepSeek-V3.2 zero-shot persona-agnostic framework.
4. Companion RoleMemo dataset and four persona-reasoning tasks.
[Reusable]Dual-stream memory interface design; "memory must pass persona interpretation" write sub-step (directly hits Macha persona consistency).

---

### [Category]Academic paper (game-NPC-specific memory)
[Title]Who, What, When, Where, Why: A Narrative Episodic Memory Framework for Generative AI NPCs in Games
[Link/FilePath]https://doi.org/10.54254/2755-2721/2025.21096
[One-line summary]5Ws narrative episodic memory framework designed for game NPCs, with importance scoring and forgetting curve, minimal landing schema for Macha episodic memory.
[Key conclusions]
1. Each interaction encoded as one 5Ws memory unit (analogous to event-segmentation theory).
2. Importance scoring based on emotional arousal/self-relevance/novelty etc. cognitive factors (heuristic table).
3. Uses Wickelgren forgetting law for memory-strength decay, supports "memory reconstruction."
4. Allows dynamic update of memory units (e.g., fill Where/Why fields), distinguishes player-specific tuning.
[Reusable]5Ws memory-unit schema; importance-scoring table; forgetting-curve formula — directly as field definitions of Macha `MemoryItem`.

---

### [Category]Academic paper (social-simulation survey)
[Title]A Survey on LLM-based Agents for Social Simulation: Taxonomy, Evaluation and Applications
[Link/FilePath]https://github.com/FudanDISC/SocialAgent (Fudan DISC group-maintained repository; original paper is Wang et al. social-simulation survey, repository has paper/classification/benchmark index)
[One-line summary]Systematically reviews LLM-driven social simulation, proposes "Profile/Perception/Memory/Planning/Action" five-module framework and macro/micro/module three-layer evaluation.
[Key conclusions]
1. Unified framework five modules isomorphic to Macha four modules (extra Profile, exactly corresponds to Macha persona layer).
2. Evaluation in three layers: macro (system-level scalability/believability), micro (consistency/accuracy/reasonableness), module.
3. Sums four social-simulation scenarios: reveal pattern / interpret phenomenon / verify theory / predict policy.
4. Points to scale, memory consistency, missing benchmarks as core challenges.
[Reusable]Five-module framework (completes Macha's Profile→Persona concept); three-layer evaluation body (connects to Macha evaluation layer).

---

### [Category]Academic paper (social-simulation position)
[Title]Integrating LLM in Agent-Based Social Simulation: Opportunities and Challenges
[Link/FilePath]https://arxiv.org/abs/2507.19364
[One-line summary]Examines opportunities and risks of LLM social simulation from computational-social-science perspective, advocates "LLM + traditional ABM hybrid" route.
[Key conclusions]
1. LLM can reproduce theory of mind and part of social reasoning, but has cognitive bias and irreproducibility.
2. Detailed comments on Generative Agents, AgentSociety (10k-scale), GenSim, AgentTorch platform design trade-offs.
3. Advocates hybrid architecture (LLM expressivity + rule-system transparency) for both fidelity and control.
[Reusable]"Hybrid architecture" idea highly consistent with Macha's Replace/Wrap; multi-NPC extension-layer platform-selection reference.

---

### [Category]Academic paper (world-model survey)
[Title]Understanding World or Predicting Future? A Comprehensive Survey of World Models
[Link/FilePath]https://arxiv.org/abs/2411.14499 (Ding et al., Tsinghua; ACM Computing Surveys 2025)
[One-line summary]Unifies world models into two functions "understand present internal representation" and "predict future state," covering generative games, autonomous driving, robotics, social simulation.
[Key conclusions]
1. World model two functions: build internal representation (understand) + predict future (decide).
2. Games are a core application (e.g., WHAM dynamic responsive virtual environment).
3. Points out definition still messy, long-horizon consistency / error accumulation as core hard problems.
[Reusable]World-model classification; as Macha "extension research" direction (NPC internal environment simulation) theoretical entry. (Note: original Zenodo overview page planned for citation could not be independently verified; using verified arXiv survey instead.)

---

### [Category]Academic paper (world-model survey)
[Title]Is Sora a World Simulator? A Comprehensive Survey on General World Models and Beyond
[Link/FilePath]https://arxiv.org/abs/2405.03520 (Zhu et al.)
[One-line summary]Comprehensively surveys general world models (video generation/autonomous driving/embodied agents), discusses potential and limits as AGI path.
[Key conclusions]
1. Video-generation models (Sora-class) closer to "predict future" world models.
2. Sums representative methods separately in games/autonomous-driving/embodied scenarios.
3. Real-time, physical consistency, controllability are landing bottlenecks.
[Reusable]General world-model capability map; for defining Macha's MVP-stage "no video-generative world model" boundary rationale.

---

### [Category]Academic paper (embodied world-model survey)
[Title]A Comprehensive Survey on World Models for Embodied AI
[Link/FilePath]https://arxiv.org/abs/2510.16732 (Li et al.; v2/v3 continuously updated)
[One-line summary]Unified framework for embodied-AI world models, proposes function/time-modeling/spatial-representation three-axis classification.
[Key conclusions]
1. World model = internal simulator, supports forward/counterfactual rollout.
2. Three-axis classification: function (decision-coupled vs general), time (sequential simulation vs global differential), spatial representation (latent/grid/decomposed rendering).
3. Challenges: unified dataset scarcity, physical-consistency evaluation, long-horizon temporal consistency vs error accumulation, real-time performance overhead.
[Reusable]World-model classification axes (can inspire Macha's "internal environment model" extension design); continuously maintained bibliography https://github.com/Li-Zn-H/AwesomeWorldModels .

---

### [Category]Engineering implementation / simulation platform
[Title]Concordia: A Library for Generative Agent Simulation
[Link/FilePath]https://arxiv.org/abs/2312.03664 (DeepMind)
[One-line summary]DeepMind's generative-agent simulation library, provides modular base of "scene/role/memory/action," fits multi-NPC social experiments.
[Key conclusions]
1. Combines complex social scenes via "local/collaborative building blocks."
2. Role driven by LLM + memory + goal, emphasizes reproducible experiments.
3. Leans sandbox simulation, not single-NPC real-time skeleton.
[Reusable]Modular "scene-role-memory-action" combination paradigm; multi-NPC extension-layer platform reference (connects to Macha Wrap idea).

---

### [Category]Engineering implementation / simulation platform
[Title]AgentSociety: Large-Scale Social Simulation with LLM Agents
[Link/FilePath](not independently verified) Original paper is Piao et al., 2025; entry seen in social-simulation survey 2507.19364's detailed comments, suggest secondary search "AgentSociety Piao 2025" to confirm exact URL
[One-line summary]Large-scale social simulation platform supporting 10,000+ LLM agents, with spatial movement, economic activity, social network, exogenous events.
[Key conclusions]
1. Single agent paired with cognitive module (memory/goal/decision/relationship tracking).
2. Validation strategy emphasizes experiential fidelity (reproduce behavior experiments and large-scale surveys).
3. Used for political polarization, rumor diffusion, UBI impact and other macro-phenomenon simulation.
[Reusable]Large-scale agent cognitive-module division; experiential-fidelity validation method (multi-NPC extension-layer reference).

> **Honesty statement (AgentSociety original URL)**: This entry's specific arXiv number could not be independently confirmed from primary source during search (only cited in survey 2507.19364 and described as Piao et al., 2025). Suggest secondary verification "AgentSociety Piao 2025" for exact link before implementation; this doc fabricates no specific URL.

---

## 4. Recommended Landing Priority (execution checklist for implementers)

| Priority | Action | Source basis |
|---|---|---|
| P0 (MVP) | Define `MemoryItem` (5Ws + importance + forgetting fields), implement episodic-memory write/retrieve/forget | 5Ws(2025), CoALA(2309), MemGPT(2310) |
| P0 | Implement `Reasoning` decision loop: retrieve→reflect→plan→persona-gate→intention | CoALA(2309), GA(2304), Reflexion(2303) |
| P0 | Persona layer: Big Five + defense-mechanism constraint + introspective-monologue gating | PersonaForge(ACL2026) |
| P1 | Dual-stream memory write (fact + persona-conditioned insight) | DualMem(2026) |
| P1 | Semantic-memory graph (HippoRAG-style associative retrieval) | HippoRAG(2405/2502) |
| P1 | Reflection throttling (on-demand, avoid fixed high frequency) | PersonaForge selective dual-process(ACL2026) |
| P2 | Procedural memory / skill library | Voyager(2305) |
| P2 | Multi-NPC sociality extension (communication/organization/relationship) | GA(2304), Concordia(2312), social-simulation survey |
| P3 (research) | World-model-style internal environment simulation | World Models survey(2411/2405/2510) |

---

*End of document. All source links in this file verified reachable one by one at writing; future-dated entries are published/accepted versions on search date. If any source later inaccessible, supplement alternative per `information_needs.md` format.*

---

## Deepening Supplement: MCM v0.1 Component Specification

> This section is an **additive deepening** of the original doc: it does not change the §0–§4 existing framework (evaluation coordinate system, candidate comparison table, fusion suggestion, source collection, landing priority), only appends a landable specification draft of "Macha fused cognitive model MCM v0.1" outside it. The following **module naming, L0–L5 ladder, memory JSON Schema, main-loop pseudocode** together form MCM v0.1's interface baseline, for later connection with `architecture.md` / `engineering_npc_architectures.md` (Replace upper / Wrap lower).
>
> New sources still strictly follow `information_needs.md` six-field format ([Category]/[Title]/[Link]/[One-line summary]/[Key conclusions]/[Reusable]), grouped and numbered by two dimensions "breadth+timeliness" and "domestic academia" (S-D1-*, S-D3-*), see §5 at end of chapter.

---

### 0. L0–L5 NPC Cognitive-Maturity Ladder (reference baseline)

Introduce a "capability dial" running through the whole text for the MCM module. **The L value decides which modules are active/off, and also the compute-budget ceiling** (see §4). This ladder unifies the original §2.2 MVP goal and §2.4 extension-layer constraints into enumerable gears.

| Level | Name | Memory | Reflection / Planning | Sociality | Meaning for Macha |
|---|---|---|---|---|---|
| **L0** | Scripted NPC | None (BT / hard-coded rules) | None | None | Baseline; carried by Wrap layer (BT/GOAP/HTN) |
| **L1** | Zero-shot role-play | None (cold start each time) | None | None | Only persona prompt driven, for validating character setting |
| **L2** | In-session context | Working-memory scratch (current session window) | None | None | Single / multi-turn dialogue keep-alive |
| **L3** | Layered long-term memory | scratch/working + episodic/semantic layering, cross-session retrieve + forget | Weak (retrieve-as-reflection trigger) | Weak (relationship field reserved) | **MVP goal**: single-NPC long-term memory + persona consistency |
| **L4** | Reflection + planning + persona gating | L3 full + Reflection evolution | Strong: explicit reflection / planning / persona gating | Medium (relationship / community tracking) | Autonomous goal and metacognition, single-NPC "complete form" |
| **L5** | Group emergence + internal environment model | L4 + cross-NPC shared memory | Strong + group coordination | Strong (social emergence) | Extension layer: multi-NPC society + lightweight world model |

> Note: L3 = original §2.2 MCM MVP; L4 fills §2.2 "reflection loop / planning" sub-steps; L5 corresponds to §2.4 "sociality left as extension layer" "world model only as extension research." L0–L2 satisfiable by existing engines / prompt directly; MCM v0.1 focuses on specifying L3–L5.

---

### 1. Breadth + Timeliness: 2025–2026 cognitive-architecture / memory / world-model new progress

Original §3 already covers foundational works Generative Agents, MemGPT, HippoRAG, PersonaForge, DREAM, RoleMemo, 5Ws. To keep "frontier timeliness," this section adds four new main lines from 2024–2026, with six-field sources in §5:

1. **Memory from "static storage" to "agentic / self-evolving"**: A-MEM (Zettelkasten-style dynamic linking + old-memory evolution), Mem0 (production-grade layered + graph memory, p95 latency down 91%), Memobase (user-profile-style, retrieval <80ms), TiM (stores "thinking traces" in memory, avoids repeated reasoning). This directly strengthens original §2.2 "memory layering / reconstructive memory" implementation path.
2. **Memory-evaluation standardization**: LongMemEval (5 long-term-memory capability types, long-context LLM drops 30%+), LOCOMO series, make Macha `Memory` module objectively benchmark-regressable.
3. **Temporal knowledge-graph memory**: Graphiti / Zep (dual-temporal model + hybrid retrieval), provides "relations expire over time but history queryable" engineering exemplar for semantic-memory layer, better than static RAG.
4. **World model ≠ NPC cognitive layering** (key boundary): GameNGen / DIAMOND / GameGen-O / Genie 2·3 prove "world model" is **pixel-level rendering and state prediction of environment**, compute and real-time threshold extremely high, Macha MVP should not embed; it is orthogonal to MCM's "memory / reflection / planning," only reference for L5 extension research (echoes §2.4).
5. **Memory operating-systematization**: MemOS (parameter / activation / plaintext three memory unified as `MemCube`), MIRIX (six-component multi-agent memory), raises "memory" to first-class system resource — fits Macha "standard skeleton / pluggable" positioning.

---

### 2. Technical-spec depth: MCM v0.1 component specification

#### 2.1 Module interface list (9 modules)

9 modules strictly land within the original skeleton `Perception → Memory → Reasoning → Action` four stages (Persona / SocialModel resident in Memory stage, execute gating in Reasoning stage):

| # | Module | Skeleton stage | Responsibility | Input (I) | Output (O) |
|---|---|---|---|---|---|
| 1 | **Perception** | Perception | Normalize raw environment / dialogue / event into machine-consumable percept; extract entity, intent, saliency | `Observation` (raw text / voice transcript / engine event / world-state snapshot) | `Percept{entities, intent, saliency, ts}` |
| 2 | **WorkingMemory** | Memory | Maintain current turn's "conscious content": scratch temp + working context window; TTL expiry | `Percept`, `turn_tokens` | `ActiveContext{scratch[], working_window[]}` |
| 3 | **EpisodicMemory** | Memory | Encode experience as 5Ws unit; support write / retrieve / forget / reconstruct (see §2.2, original 5Ws) | `ExperienceEvent`, `retrieve(query)` | `EpisodicItem[]` (5Ws + importance + decay) |
| 4 | **SemanticMemory** | Memory | Extract and maintain world / self knowledge; optional HippoRAG-style graph for multi-hop association (original §3 HippoRAG) | `Fact`, `retrieve(query, mode=graph)` | `SemanticNode/Edge[]` (incl. temporal validity) |
| 5 | **Persona** | Memory+Reasoning | Resident character setting (Big Five + defense mechanisms + three-layer persona, see original PersonaForge); produce persona constraint for gating | `CharacterSpec` (profile + psychology constraint) | `PersonaConstraints{big_five, defenses, forbidden_drift[]}` |
| 6 | **SocialModel** | Memory+Reasoning | Track relationship/stance/intimacy with other NPCs / players; output relation graph (L3 only reserved field, L4+ activate) | `InteractionRecord` | `RelationGraph{edge(agent, stance, intimacy)}` |
| 7 | **Reflection** | Reasoning | Metacognition: high-level abstraction of recent memory (GA-style insight), verbalized failure reflection (Reflexion-style); **on-demand throttling** (PersonaForge selective dual-process) | `RecentMemories[]`, `PersonaConstraints` | `Insight[]` (write back Episodic/Semantic) |
| 8 | **Planning** | Reasoning | Goal stack + subgoal decomposition (Voyager / CoALA); constrained by Persona and SocialModel | `Goal`, `RetrievedMemory[]`, `PersonaConstraints` | `PlanTree{goal, subgoals[], constraints}` |
| 9 | **ActionSelection** | Action | Translate intention / plan into **structured action proposal**, hand to Wrap execution layer (BT/GOAP/HTN/commercial engine); result feeds back to memory | `Intent` / `PlanTree`, `ActionSpace` | `ActionProposal{goal, sub_goals, constraints, persona_constraints}` → execution layer |

> Interface contract: modules only exchange structured objects (`Percept` / `MemoryItem` / `Insight` / `PlanTree` / `ActionProposal`), not directly coupled to specific LLM or engine — satisfies §2.3 "cognitive layer only produces structured intention" boundary.

#### 2.2 Memory-layering JSON Schema (tiers: scratch / working / episodic / semantic, incl. retrieval fields)

Below is the minimal landable schema for Macha `MemoryStore` (JSON Schema draft-07), directly continuing original 5Ws and CoALA three memories:

```json
{
  "$schema": "https://json-schema.org/draft-07/schema#",
  "$id": "https://macha.dev/schemas/mcm-memory-v0.1.json",
  "title": "Macha MCM v0.1 MemoryStore",
  "type": "object",
  "properties": {
    "npc_id": { "type": "string" },
    "tiers": {
      "type": "object",
      "properties": {
        "scratch": {
          "type": "array",
          "description": "Current-turn raw percept temp, cleared after TTL (corresponds to L2 working)",
          "items": {
            "type": "object",
            "properties": {
              "content": { "type": "string" },
              "ts": { "type": "integer" },
              "ttl_ms": { "type": "integer", "default": 30000 }
            },
            "required": ["content", "ts"]
          }
        },
        "working": {
          "type": "array",
          "description": "Current-session context window (L2), token-budget constrained",
          "items": { "$ref": "#/definitions/ContextItem" }
        },
        "episodic": {
          "type": "array",
          "description": "5Ws narrative episodic memory (original 5Ws framework)",
          "items": { "$ref": "#/definitions/EpisodicItem" }
        },
        "semantic": {
          "type": "array",
          "description": "World/self knowledge, optional graph edge (HippoRAG/Graphiti)",
          "items": { "$ref": "#/definitions/SemanticItem" }
        }
      },
      "required": ["scratch", "working", "episodic", "semantic"]
    },
    "retrieval": {
      "type": "object",
      "description": "Retrieval config and runtime metrics (connects to §4 latency target)",
      "properties": {
        "strategy": {
          "type": "string",
          "enum": ["recency", "importance", "relevance", "hybrid", "graph"],
          "default": "hybrid"
        },
        "weights": {
          "type": "object",
          "properties": {
            "recency": { "type": "number", "default": 0.3 },
            "importance": { "type": "number", "default": 0.3 },
            "relevance": { "type": "number", "default": 0.4 }
          }
        },
        "top_k": { "type": "integer", "default": 8 },
        "target_p95_latency_ms": { "type": "number", "default": 50 },
        "last_query_ms": { "type": "number" }
      },
      "required": ["strategy", "target_p95_latency_ms"]
    }
  },
  "required": ["npc_id", "tiers", "retrieval"],

  "definitions": {
    "ContextItem": {
      "type": "object",
      "properties": {
        "role": { "type": "string", "enum": ["system", "user", "assistant", "env"] },
        "content": { "type": "string" },
        "token_est": { "type": "integer" }
      },
      "required": ["role", "content"]
    },
    "EpisodicItem": {
      "type": "object",
      "properties": {
        "id": { "type": "string" },
        "who": { "type": "string" },
        "what": { "type": "string" },
        "when": { "type": "string" },
        "where": { "type": "string" },
        "why": { "type": "string" },
        "importance": { "type": "number", "minimum": 0, "maximum": 1 },
        "created_ts": { "type": "integer" },
        "last_access_ts": { "type": "integer" },
        "strength": { "type": "number", "description": "Wickelgren forgetting-curve strength, decays with access" },
        "persona_lens": {
          "type": "string",
          "description": "DualMem-style persona-conditioned insight (reconstructive memory)"
        }
      },
      "required": ["id", "what", "when", "importance", "strength"]
    },
    "SemanticItem": {
      "type": "object",
      "properties": {
        "id": { "type": "string" },
        "subject": { "type": "string" },
        "predicate": { "type": "string" },
        "object": { "type": "string" },
        "valid_from": { "type": "integer" },
        "valid_to": { "type": "integer", "description": "Dual-temporal model: null means still valid (Graphiti)" },
        "source": { "type": "string" }
      },
      "required": ["id", "subject", "predicate", "object"]
    }
  }
}
```

#### 2.3 Main-loop pseudocode `perceive → reflect → plan → act` (incl. L0–L5 mapping)

```python
def mcm_tick(npc, observation, L: int):
    # ---- Perception ----
    percept = npc.Perception.observe(observation)          # all L active

    # ---- Memory stage ----
    npc.WorkingMemory.push(percept)                        # L2+
    if L >= 3:
        # layered retrieval: episodic(5Ws) + semantic(graph)
        hits = npc.Memory.retrieve(
            query=percept.intent,
            tiers=["episodic", "semantic"],
            strategy=npc.retrieval.strategy,               # see §2.2 retrieval
        )
        npc.Persona.load()                                 # resident character constraint
        if L >= 4:
            npc.SocialModel.update(percept)                # L4+ relationship tracking

    # ---- Reasoning stage ----
    intent = None
    if L >= 4:
        # reflect (on-demand throttle: only when importance/failure signal exceeds threshold, echoes PersonaForge selective dual-process)
        if should_reflect(percept, hits):
            insights = npc.Reflection.reflect(hits, npc.Persona)
            npc.Memory.write(insights)                     # write back episodic/semantic
        # plan
        plan = npc.Planning.plan(goal=npc.goal,
                                 memory=hits,
                                 persona=npc.Persona.constraints)
        intent = plan.to_intent()
    elif L >= 3:
        intent = npc.Persona.gate(percept)                # L3: retrieve-as-light-reflection trigger
    else:  # L0-L2
        intent = percept.intent                           # direct drive or rule engine

    # ---- Action stage (Wrap lower layer)----
    proposal = npc.ActionSelection.select(intent, npc.action_space)  # produce ActionProposal
    result = npc.executor.execute(proposal)               # BT/GOAP/HTN/commercial engine
    npc.Memory.ingest(result)                             # result feeds back to memory (L3+)
    return result
```

**L0–L5 and module-activation mapping table** (implementers can directly use for switches):

| Module | L0 | L1 | L2 | L3 | L4 | L5 |
|---|---|---|---|---|---|---|
| Perception | ✅ | ✅ | ✅ | ✅ | ✅ | ✅ |
| WorkingMemory | ❌ | ❌ | ✅ | ✅ | ✅ | ✅ |
| EpisodicMemory | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| SemanticMemory | ❌ | ❌ | ❌ | ✅ | ✅ | ✅ |
| Persona (resident) | ❌ | ✅(prompt) | ✅(prompt) | ✅(gating) | ✅(gating) | ✅ |
| SocialModel | ❌ | ❌ | ❌ | reserved field | ✅ | ✅(shared) |
| Reflection | ❌ | ❌ | ❌ | weak | ✅(throttled) | ✅ |
| Planning | ❌ | ❌ | ❌ | ❌ | ✅ | ✅(group) |
| ActionSelection → Wrap | BT | prompt | prompt | structured proposal | structured proposal | structured proposal |

---

### 3. China-market special / domestic-academia depth

Chinese role-playing / social-simulation academia has formed an independent school since 2023, highly isomorphic with Macha's "persona consistency / long-term memory / multi-NPC society." This section reviews key works by institution, with six-field listing in §5 (S-D3-*).

**Core map (institution → work → Macha reuse):**

| Institution / team | Representative work | Key contribution | Maps to MCM module |
|---|---|---|---|
| **ChatHaruhi team (LC1332)** | ChatHaruhi (2308.09597) | Extract character memory from scripts + enhanced prompt, 32 characters 54k dialogues | EpisodicMemory "character-specific memory" initialization paradigm |
| **Tsinghua CoAI / RUC / Alibaba (RoleLLM)** | RoleLLM (2310.00746) | RoleBench 100k+ character-level instructions; Context-Instruct injects character knowledge | Persona knowledge injection, SemanticMemory initialization |
| **RUC (CharacterEval)** | CharacterEval (2401.01275) | Chinese RPCA benchmark 77 characters, 13 metrics, CharacterRM | §4 evaluation layer can directly reuse its "persona regression / consistency" metrics |
| **THUDM (Zhipu)** | CharacterGLM (2311.16832), CogAgent (2312.08914), ChatDev (2307.07924), AgentTuning | CharacterGLM Chinese character dialogue; CogAgent visual GUI perception; ChatDev multi-agent collaboration | Persona Chinese corpus; Perception visual extension (L5); multi-NPC collaboration reference |
| **Fudan DISC (Wang Xintao et al.)** | CoSER (2502.09082), SocialAgent survey (original §3) | CoSER: 771 books 17k characters, given-circumstance acting, retrieval-augmented; LIFECHOICE benchmark | EpisodicMemory "inner monologue" field, Retrieval augmentation, long-horizon narrative consistency |
| **Fudan (RecAgent)** | RecAgent (2306.02552) | Three-layer memory (sensory/short/long) + forgetting + self-reflection; thousand-agent simulation | Memory layering + Reflection social-simulation exemplar |
| **Tsinghua / NetEase (CharacterBench)** | CharacterBench (2412.11912) | 3956 characters, sparse/dense dimensions, CharacterJudge | Persona-evaluation "sparse dimension" idea, treats hard-to-trigger character features |
| **HKUST / Tencent (InCharacter, RoleInteract)** | InCharacter (2310.17976), RoleInteract (2403.16409) | Psychological interview evaluates persona fidelity; evaluates social interaction | Persona evaluation method, SocialModel interaction evaluation |
| **Alibaba (AgentScope)** | AgentScope (2402.14034) | Message-driven multi-agent platform, fault tolerance, distributed | Multi-NPC (L5) orchestration base, connects to Wrap strategy |
| **Other Chinese character works** | Character-LLM (2310.10158) | Trainable character agent | Persona fine-tuning paradigm reference |

> **Key insight**: Domestic works generally preceded and are independent of PersonaForge / DREAM in raising "character memory + persona evaluation," and data is mainly Chinese novels / scripts, **a more direct first-hand corpus and evaluation benchmark for Macha's Chinese-NPC scenarios**. CoSER's "inner monologue + retrieval augmentation" is almost isomorphic with Macha §2.2 "reconstructive memory / persona gating"; CharacterEval / CharacterBench evaluation dimensions can directly become MCM regression tests.

---

### 4. Quantification and landing: capacity / latency / compute budget

MCM v0.1 landing needs to translate "cognitive quality" into committable engineering metrics. Below are **suggested target values**, not hard constraints; sources in §5 (Mem0 p95 down 91%, Memobase <80ms, LongMemEval long-context drop).

**(a) Memory-tier capacity table (single NPC, L3 target)**

| Tier | Capacity ceiling | Unit | Carrier suggestion | Note |
|---|---|---|---|---|
| scratch | 1 turn | rolling 30s TTL | memory | from L2 |
| working | ≤ 8k tokens | session window | KV-Cache / context | constrained by §2.2 retrieval budget |
| episodic | ≤ 5,000 5Ws items | vector + metadata | vector DB + KV | evict by importance×strength when exceeded |
| semantic | ≤ 2,000 graph nodes | graph | graph DB (Neo4j/RedisGraph) | HippoRAG / Graphiti-style |
| persona | fixed 1 copy | character spec | config / params | does not grow with dialogue |

**(b) Retrieval latency target**

- **End-to-end memory retrieval p95 < 50ms** (single NPC, episodic+semantic hybrid retrieval). Basis: Memobase measured <80ms; Mem0 vs full-context p95 down 91%. Macha takes stricter 50ms to leave margin for Wrap execution layer.
- Directly stuffing history into long-context LLM inadvisable: LongMemEval shows 115k-token context drops 30%+ on long-horizon memory tasks, and latency grows linearly with length — **must use layered retrieval instead of full context**.

**(c) Per-module compute budget (single tick, L4 example)**

| Module | LLM calls | Est. tokens | Latency budget | Throttle strategy |
|---|---|---|---|---|
| Perception | 0–1 | ≤ 500 | 10ms | rule-based extraction first, LLM only fallback |
| WorkingMemory | 0 | 0 | <5ms | in-memory op |
| Episodic/Semantic retrieve | 0 (embedding precomputed) | — | <50ms(p95) | async index build; retrieve decoupled from generation |
| Persona gating | 1 (light) | ≤ 300 | 20ms | only consistency-check output |
| Reflection | 0–1 | ≤ 1,500 | 200ms (async) | **on-demand trigger**, not every tick; PersonaForge proves 13.4% token overhead retains 96% performance |
| Planning | 1 | ≤ 2,000 | 300ms | only on goal change / subgoal complete |
| ActionSelection | 1 | ≤ 800 | 80ms | structured output, forbid free generation |
| **Total (peak)** | **≤4** | **≤5.1k** | **<700ms/tick** | reflection/planning async, not blocking main response |

> Landing principle: L3 (MVP) only Perception + layered retrieval + Persona(prompt) + ActionSelection, **≤2 LLM calls/tick, p95 < 120ms**; L4 Reflection/Planning goes async background, not counted in player-visible latency.

---

### 5. Source Collection (deepening supplement, six-field format)

> Sources below are newly added in this deepening, strictly six-field. Numbered S-D1-* (breadth+timeliness), S-D3-* (domestic academia). arXiv numbers all verified by search; a few entries (see end honesty statement) not independently verified item-by-item, explicitly marked.

#### [Dimension one]Breadth + timeliness

### [Category]Academic paper (Agent memory)
[Title]A-MEM: Agentic Memory for LLM Agents
[Link/FilePath]https://arxiv.org/abs/2502.12110 (NeurIPS 2025)
[One-line summary]Gives memory organization itself "agency": borrows Zettelkasten, new memory dynamically links and triggers old-memory evolution, not hard-coded schema.
[Key conclusions]
1. Memory system should have agency: autonomously generate context, dynamically link, evolve old memory with new experience.
2. Each memory is atomic Note (content+context+keywords+tags+embedding), at write judges links with historical memory.
3. New memory can rewrite old memory's context description, achieving "memory network continuously refined."
4. Beats MemGPT/MemoryBank etc. on 6 base models, token cost down 85–93%.
[Reusable]Dynamic linking + memory-evolution mechanism (directly strengthens Macha EpisodicMemory "reconstruction" logic); atomic Note schema.

---

### [Category]Academic paper (production-grade memory)
[Title]Mem0: Building Production-Ready AI Agents with Scalable Long-Term Memory
[Link/FilePath]https://arxiv.org/abs/2504.19413
[One-line summary]Scalable, memory-centric architecture, dynamically extract/consolidate/retrieve conversation salient info, with graph-memory variant; comprehensively beats baseline on LOCOMO.
[Key conclusions]
1. vs full context, Mem0 p95 latency down 91%, token cost saved >90%.
2. Beats OpenAI memory and Zep etc. on single-hop/temporal/multi-hop/open-domain four question types.
3. Mem0-graph uses graph to capture complex relations between dialogue elements, better temporal/relational reasoning.
4. Provides dedup, conflict detection, dual retrieval (entity subgraph + semantic triple) engineering mechanisms.
[Reusable]Memory generate/update two-stage flow, conflict marking (not physically delete), p95 latency baseline (supports §4 50ms target).

---

### [Category]Engineering implementation (user-profile memory)
[Title]Memobase: Profile-Based Long-Term Memory for AI Applications
[Link/FilePath]https://github.com/memodb-io/memobase (open source, no standalone arXiv; use GitHub as primary at search)
[One-line summary]User-profile-centric long-term memory backend, structured storage + time-aware + batch buffer, measured retrieval <80ms.
[Key conclusions]
1. Targets "understand who the user is" not "retrieve documents," distinguishes Profile and Event two-line memory.
2. Each user paired with buffer batch-processing chat, online response <100ms (measured <80ms).
3. LOCOMO temporal reasoning 85%, higher than Mem0/Zep.
4. Supports Volcengine Doubao etc. domestic LLM access, fits Chinese market.
[Reusable]User-profile + event two-line schema; buffer batch-processing latency-reduction mode (reusable for Macha async memory write).

---

### [Category]Academic paper (long-term-memory evaluation)
[Title]LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory
[Link/FilePath]https://arxiv.org/abs/2410.10813 (ICLR 2025)
[One-line summary]500 questions, freely-extensible chat-history long-term-memory benchmark, evaluates 5 capability types (info extraction / multi-session reasoning / temporal / knowledge update / abstention).
[Key conclusions]
1. Long-context LLM drops 30%+ on long-horizon memory tasks; commercial systems (e.g., GPT-4o) only 30–70% accuracy in simplified setting.
2. Proposes "index—retrieve—read" three-stage unified memory framework.
3. Key finding: round is better storage granularity than session; fact-augmented key expansion raises recall 4%, QA 5%; time-aware query expansion raises temporal recall 7–11%.
4. Chain-of-Note + structured JSON read further +10 points.
[Reusable]Three-stage memory framework; 5 capability dimensions (directly become Macha `Memory` regression test); time-aware retrieval strategy.

---

### [Category]Academic paper (memory-mechanism survey)
[Title]A Survey on the Memory Mechanism of LLM-based Agents
[Link/FilePath]https://arxiv.org/abs/2404.13565 (exact number not independently verified at search, suggest secondary confirmation)
[One-line summary]Systematically reviews LLM-agent memory mechanism (type, structure, operation, evaluation), gives memory full-lifecycle classification.
[Key conclusions]
1. Summarizes memory perception/storage/retrieval/forgetting/update full lifecycle.
2. Compares vector/graph/tree/layered multiple memory architectures pros and cons.
3. Gives memory-evaluation benchmark directions.
[Reusable]Memory-mechanism classification (as Macha `Memory` module design checklist).

---

### [Category]Academic paper (temporal knowledge-graph memory)
[Title]Zep: A Temporal Knowledge Graph Architecture for Agent Memory
[Link/FilePath]https://arxiv.org/abs/2501.13956 (Graphiti open-source engine)
[One-line summary]Uses "dual-temporal model + hybrid retrieval" temporal knowledge graph as agent long-term memory, reaches SOTA.
[Key conclusions]
1. Three-layer subgraph: episode (raw segment) → semantic (entity/relation) → community (cluster).
2. Dual-temporal model: records both event-occurrence time and ingestion time, marks old edge invalid not deleted on conflict (history queryable).
3. Hybrid retrieval: BM25 + cosine + graph-traversal BFS + rerank, target sub-second.
4. Reaches Agent Memory SOTA on DMR and LongMemEval.
[Reusable]Temporal-graph schema + dual-temporal invalidation model (strengthens Macha SemanticMemory `valid_to` field); episode→semantic extraction pipeline.

---

### [Category]Academic paper (game world model)
[Title]GameNGen: Diffusion Models Are Real-Time Game Engines
[Link/FilePath]https://arxiv.org/abs/2408.14837 (ICLR 2025; project https://gamengen.github.io)
[One-line summary]First fully neural-network-driven, real-time-interactive game engine, autoregressively generates DOOM next frame (>20 FPS) via diffusion model.
[Key conclusions]
1. Two-stage training: RL agent plays game records data → diffusion model conditions on "history frame + action" to generate next frame.
2. Conditioning with noise makes long-trajectory autoregressive stable; PSNR 29.4 (≈lossy JPEG).
3. Human raters only 60% distinguish real/fake clips.
4. **Proves world model is pixel-level render/predict, compute threshold extremely high** — Macha MVP should not embed.
[Reusable]"World model ≠ NPC cognition" boundary argument (echoes §2.4); L5 extension-research reference architecture.

---

### [Category]Academic paper (diffusion world model)
[Title]DIAMOND: Diffusion for World Modeling: Visual Details Matter in Atari
[Link/FilePath]https://arxiv.org/abs/2405.12399 (NeurIPS 2024 Spotlight)
[One-line summary]Trains RL agent in diffusion world model, Atari 100k human-normalized score 1.46 (new SOTA within world model), and works as CS:GO interactive neural engine.
[Key conclusions]
1. Pixel-space diffusion world model surpasses discrete-latent methods (IRIS), visual detail key for RL.
2. EDM sampling stable even at 1-step denoise, 3-step balances modality choice and temporal consistency.
3. Can play CS:GO world model at ~10 FPS on RTX 3090.
4. Limit: model memory limited, "continuous multi-hop" etc. physics-violating failure modes.
[Reusable]Diffusion world-model stability tricks (conditional augmentation / low-step EDM); also corroborates world-model compute threshold.

---

### [Category]Academic paper (open-world game generation)
[Title]GameGen-O: Open-world Video Game Generation
[Link/FilePath]https://github.com/OpenGVLab/GameGen-O (arXiv 2411.00831, number suggest secondary confirmation)
[One-line summary]First diffusion transformer for open-world video-game generation, with OGameData dataset and InstructNet interaction control.
[Key conclusions]
1. Builds OGameData from 100+ next-gen open-world games (filter/score/decouple annotation).
2. Two-stage training: base pretrain (text-to-video + video continuation) + InstructNet instruction fine-tune (interaction control).
3. Can generate character/environment/action/event and support multimodal structured instruction control.
4. Positioned as rendering-tech alternative prototype, not real-time playable.
[Reusable]"Generative content + interaction control" two-stage paradigm; domestic reference for L5 world-model direction.

---

### [Category]Industry report / blog (foundation world model)
[Title]Genie 2 / Genie 3: A Large-Scale Foundation World Model
[Link/FilePath]https://deepmind.google/discover/blog/genie-2-a-large-scale-foundation-world-model/ (Genie 2); https://deepmind.google/discover/blog/genie-3-a-frontier-world-model/ (Genie 3, 2025)
[One-line summary]DeepMind foundation world model, generates interactive diverse 3D environments from single image, Genie 3 further real-time, persistent interactive world.
[Key conclusions]
1. Genie 2 generates operable, explorable virtual world from single image/prompt, with NPCs and physics.
2. Genie 3 (2025) supports real-time interaction, minutes-long persistent state and "promptable world events."
3. Indicates "world model as simulator" industry route, still far from single-NPC real-time cognition cost.
[Reusable]L5 internal-environment-model long-term reference; orthogonal to Macha cognitive layer.

---

### [Category]Academic paper (thinking-type memory)
[Title]Think-in-Memory (TiM): Recalling and Post-thinking Enable LLMs with Long-Term Memory
[Link/FilePath]https://arxiv.org/abs/2311.08719 (Ant Group / CUHK Shenzhen)
[One-line summary]Stores "thinking traces" not raw dialogue, post-think after response uses insert/forget/merge to evolve memory, avoids repeated-reasoning bias.
[Key conclusions]
1. Traditional "retrieve raw history → re-reason" easily produces inconsistent reasoning paths and high retrieval cost.
2. TiM stores "inductive thinking" (relation triples) not original text, eliminates repeated reasoning.
3. insert/forget/merge operations organize memory, supports dynamic evolution.
4. LSH achieves efficient long-term dialogue retrieval (~0.53ms).
[Reusable]"Store thinking traces not original text" write sub-step (strengthens Macha Reflection write-back); LSH retrieval optimization (supports §4 latency).

---

### [Category]Academic paper (memory operating system)
[Title]MemOS: An Operating System for Memory-Augmented Generation in LLMs
[Link/FilePath]https://arxiv.org/abs/2505.22101 (Memory Tensor / Shanghai Jiao Tong etc.)
[One-line summary]First raises memory to first-class system resource for LLM, unifies parameter/activation/plaintext three memory as `MemCube`, with lifecycle governance and scheduling.
[Key conclusions]
1. Three memory types: parameter (weights), activation (KV-Cache), plaintext (external storage), support mutual conversion (hot memory to KV lowers TTFT).
2. `MemCube` unified abstraction, supports tracking/fusion/migration and cross-task traceable access.
3. MemReader turns task intent into structured `MemoryCall`, hybrid retrieval + dynamic scheduling.
4. Reaches SOTA on LOCOMO.
[Reusable]Memory-as-"system-resource" governance paradigm (consistent with Macha standard-skeleton/pluggable positioning); `MemCube` abstraction.

---

#### [Dimension two]China-market special / domestic academia

### [Category]Academic paper (role-playing data/method)
[Title]ChatHaruhi: Reviving Anime Character in Reality via Large Language Model
[Link/FilePath]https://arxiv.org/abs/2308.09597
[One-line summary]Extracts character-specific memory from scripts + enhanced prompt, builds 32-character 54k simulated-dialogue Chinese/English role-playing dataset and method.
[Key conclusions]
1. Algorithm controls LLM playing specific fictional character via "improved prompt + script-extracted character memory."
2. Dataset covers 32 Chinese/English TV/anime characters, 54k+ dialogues.
3. Auto + human evaluation both beat baseline.
4. Open-source code and data (LC1332/Chat-Haruhi-Suzumiya).
[Reusable]"Character memory extracted from scripts" initialization paradigm (Macha EpisodicMemory cold start); Chinese character corpus.

---

### [Category]Academic paper (Chinese role-playing evaluation)
[Title]CharacterEval: A Chinese Benchmark for Role-Playing Conversational Agent Evaluation
[Link/FilePath]https://arxiv.org/abs/2401.01275 (ACL 2024; code https://github.com/morecry/CharacterEval)
[One-line summary]Chinese role-playing dialogue benchmark, 1,785 multi-turn dialogues, 11,376 samples, 77 characters, 13 metrics 4 dimensions, trains CharacterRM.
[Key conclusions]
1. Data via GPT-4 extraction + strict human QC + Baidu Baike character profile enhancement.
2. Four dimensions 13 metrics: dialogue ability / character consistency / role appeal / persona regression (MBTI).
3. CharacterRM correlation with human exceeds GPT-4.
4. Chinese LLM shows more potential than GPT-4 in Chinese role-play.
[Reusable]Persona regression (MBTI reverse) and consistency-evaluation metrics (to Macha §4 regression test); Chinese benchmark.

---

### [Category]Academic paper (role-playing benchmark / fine-tuning)
[Title]RoleLLM: Benchmarking, Eliciting, and Enhancing Role-Playing Abilities of Large Language Models
[Link/FilePath]https://arxiv.org/abs/2310.00746
[One-line summary]Role-playing framework: 100 character profiles, Context-Instruct knowledge injection, RoleGPT style imitation, RoCIT fine-tunes RoleLLaMA/RoleGLM.
[Key conclusions]
1. Four stages: character profile → Context-Instruct knowledge extraction → RoleGPT style imitation → RoCIT fine-tune.
2. RoleBench: first systematic fine-grained character-level benchmark, 168,093 samples (incl. Chinese/English).
3. RoCIT produces RoleLLaMA (EN) / RoleGLM (CN), comparable to RoleGPT(GPT-4).
4. Context-Instruct injects character-related knowledge/memory into model.
[Reusable]Character-knowledge injection pipeline; Chinese character data (RoleGLM) for Macha Persona initialization.

---

### [Category]Academic paper (trainable character agent)
[Title]Character-LLM: A Trainable Agent for Role-Playing
[Link/FilePath]https://arxiv.org/abs/2310.10158 (exact number not independently verified at search, suggest secondary confirmation)
[One-line summary]Trains role-playable agent via "experience acquisition + private-info internalization," alleviating character-knowledge leakage and persona drift.
[Key conclusions]
1. Two stages: Experience Grounding (build experience from script/wiki) + Private Information (internalize monologue/secrets).
2. Introduces "behavior regulation" to prevent character stating real-world knowledge or overstepping.
3. Beats direct prompt on persona consistency and knowledge-leak prevention.
[Reusable]"Private-info internalization + behavior regulation" mechanism (strengthens Macha Persona gating anti-drift).

---

### [Category]Academic paper (persona-fidelity evaluation)
[Title]InCharacter: Evaluating Personality Fidelity in Role-Playing Agents with Psychological Interviews
[Link/FilePath]https://arxiv.org/abs/2310.17976 (HKUST)
[One-line summary]Uses psychological interview (not QA) to evaluate role-playing agent persona fidelity, and gives training improvement.
[Key conclusions]
1. Probes via psychological interview whether agent stably holds character persona.
2. Finds most RPLA persona collapse/contradiction in interview.
3. Proposes improved training for more faithful persona.
[Reusable]Persona-fidelity evaluation method (Macha Persona module evaluation means); interview-style probe.

---

### [Category]Academic paper (Chinese character-dialogue model)
[Title]CharacterGLM: Customizing Chinese Conversational AI Characters with Large Language Models
[Link/FilePath]https://arxiv.org/abs/2311.16832 (THUDM / Zhipu)
[One-line summary]Customizes Chinese dialogue characters via "character profile + dialogue instruction," systematically builds character data and training.
[Key conclusions]
1. Proposes character-profile five elements (identity/personality/hobby/social/language style) and dialogue instruction.
2. Constructs Chinese/English character-dialogue dataset and fine-tunes ChatGLM-series models.
3. Significantly beats general models on Chinese character-dialogue naturalness/consistency.
[Reusable]Character-profile element template (directly aligns Macha Persona `CharacterSpec`); Chinese training data.

---

### [Category]Academic paper (social-interaction evaluation)
[Title]RoleInteract: Evaluating the Social Interaction of Role-Playing Agents
[Link/FilePath]https://arxiv.org/abs/2403.16409 (THU / HKUST, exact number not independently verified at search, suggest secondary confirmation)
[One-line summary]Evaluates role-playing agent performance in two-person / group social interaction, supplements social dimension beyond character "single-turn consistency."
[Key conclusions]
1. Defines multi-dimensional social-interaction evaluation (cooperation/conflict/persuasion etc.).
2. Finds existing RPLA easily destabilize in long-horizon social.
3. Gives social-ability improvement directions.
[Reusable]SocialModel module social-interaction evaluation dimensions (L4/L5).

---

### [Category]Academic paper (literary-character simulation)
[Title]CoSER: Coordinating LLM-Based Persona Simulation of Established Roles
[Link/FilePath]https://arxiv.org/abs/2502.09082 (Fudan DISC / StepFun; code https://github.com/Neph0s/CoSER)
[One-line summary]Largest real literary-character dataset (771 books 17,966 characters) + given-circumstance acting training/evaluation + CoSER 8B/70B open models.
[Key conclusions]
1. Data from 771 classics, incl. real dialogue, plot summary, character experience, inner monologue.
2. given-circumstance acting (GCA): lets LLM play multiple characters in book-scene order.
3. Retrieval augmentation: retrieving character "experience/dialogue" significantly gains (raw-text retrieval almost useless).
4. CoSER-70B reaches SOTA on InCharacter / LifeChoice (75.8% / 93.47%), matches or beats GPT-4o.
[Reusable]"Inner monologue + experience retrieval" paradigm (strengthens Macha EpisodicMemory persona_lens and Retrieval); long-horizon narrative-consistency benchmarks LifeChoice/TCM.

---

### [Category]Academic paper (persona-customization benchmark)
[Title]CharacterBench: Benchmarking Character Customization of Large Language Models
[Link/FilePath]https://arxiv.org/abs/2412.11912 (Tsinghua CoAI / NetEase; AAAI 2025; code https://github.com/thu-coai/CharacterBench)
[One-line summary]Largest bilingual generative persona-customization benchmark, 3,956 characters, 22,859 samples, proposes sparse/dense dimensions and CharacterJudge.
[Key conclusions]
1. Defines 6 aspects 11 dimensions, splits sparse/dense by "whether reflected each turn," cracking feature-sparsity problem.
2. Goal-oriented query construction: custom query per dimension forces character-feature trigger.
3. CharacterJudge (Qwen2-7B) correlation with human exceeds GPT-4, lower cost.
4. DPO optimization raises 8.5% role-play quality; boundary leakage (modern knowledge leaking to historical character) is main failure.
[Reusable]Sparse-dimension evaluation method (treats hard-to-trigger character features); CharacterJudge directly does Macha persona regression.

---

### [Category]Academic paper (user / social simulation)
[Title]RecAgent: A Novel Simulation Paradigm for Recommender Systems
[Link/FilePath]https://arxiv.org/abs/2306.02552 (Fudan; code https://github.com/RUC-GSAI/YuLan-Rec)
[One-line summary]Uses LLM agent to simulate user behavior, three-layer memory (sensory/short/long) + forgetting + self-reflection, supports thousand-agent social simulation.
[Key conclusions]
1. Profile + Memory + Action three modules, memory splits sensory/short/long with forgetting and self-reflection.
2. Recommendation choice close to real person (only 8% lower), far beats RecSim 68%.
3. Reproduces "information cocoon" "user conformity" etc. social phenomena.
4. Up to 1,000 agents parallel, supports human intervention and system intervention.
[Reusable]Three-layer memory + self-reflection social-simulation exemplar (L5 multi-NPC); memory-driven-credibility ablation evidence.

---

### [Category]Engineering implementation (multi-agent platform)
[Title]AgentScope: A Flexible yet Robust Multi-Agent Platform
[Link/FilePath]https://arxiv.org/abs/2402.14034 (Alibaba; code https://github.com/modelscope/agentscope)
[One-line summary]Message-exchange-centric multi-agent platform, with fault tolerance, distributed (Actor model), multimodal and zero-code workstation.
[Key conclusions]
1. Message-driven architecture, agents communicate via message, easy to orchestrate SOP/dynamic workflow.
2. Built-in + customizable fault tolerance (error classification + handling strategy).
3. Actor model supports local↔distributed seamless conversion and auto-parallel.
4. System-level multimodal, tools, external knowledge support.
[Reusable]Multi-NPC (L5) orchestration base; message protocol directly connects to Macha `ActionProposal` cross-NPC communication.

---

### [Category]Academic paper (visual GUI perception)
[Title]CogAgent: A Visual Language Model for GUI Agents
[Link/FilePath]https://arxiv.org/abs/2312.08914 (THUDM / Zhipu; code https://github.com/THUDM/CogAgent)
[One-line summary]18B visual-language model for GUI understanding and navigation, 1120×1120 high-res input, PC/Android navigation SOTA.
[Key conclusions]
1. High-low resolution dual encoder, recognizes tiny page elements and text.
2. Using only screenshot beats HTML-text-based LLM methods on Mind2Web / AITW.
3. Outputs thinking process + next action + coordinate operation.
4. Open-source CogAgent-9B/18B.
[Reusable]Perception module visual extension (L5 lets NPC "see" game screen); high-res GUI understanding paradigm.

---

### [Category]Academic paper (multi-agent collaboration)
[Title]ChatDev: Communicative Agents for Software Development
[Link/FilePath]https://arxiv.org/abs/2307.07924 (THUDM; code https://github.com/OpenBMB/ChatDev)
[One-line summary]Uses "chat chain" to let multi-role LLM agents collaborate on software development, validates role-based multi-agent division.
[Key conclusions]
1. Decomposes software development into multi-agent dialogue pipeline (PM/programmer/tester etc.).
2. Role-based collaboration significantly lowers task complexity, raises completion.
3. Provides reproducible multi-agent communication paradigm.
[Reusable]"Role→responsibility→artifact" collaboration paradigm (L5 multi-NPC social-division reference, echoes original §3 MetaGPT/CAMEL).

---

> **Honesty statement (deepening supplement sources)**: S-D1-01~S-D1-04, S-D1-06~S-D1-08, S-D1-10~S-D1-12, S-D3-01~S-D3-03, S-D3-06, S-D3-08~S-D3-13 arXiv / project links were verified reachable item-by-item in this search. The following numbers **could not be independently verified item-by-item**, explicitly marked per `information_needs.md`, suggest secondary confirmation before implementation: S-D1-05 (memory-mechanism survey, arXiv 2404.13565), S-D1-09 (GameGen-O, arXiv 2411.00831), S-D3-04 (Character-LLM, arXiv 2310.10158), S-D3-05 (InCharacter, arXiv 2310.17976), S-D3-07 (RoleInteract, arXiv 2403.16409). All future-dated (2025–2026) entries are published/accepted versions on search date, not fabricated.

*(Deepening supplement chapter ends. This supplement does not modify any content of original §0–§4, only forward-compatibly extends the MCM v0.1 specification.)*
