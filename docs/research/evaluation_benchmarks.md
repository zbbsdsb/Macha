# Macha's Evaluation-Dimension Table + Benchmark Dataset List

> **Category**: `information_needs.md` Category 5 "Evaluation Benchmarks: How to Prove the Skeleton Is a Standard."
> **Document nature**: Research sub-task deliverable (not a Demo, but the evaluation system serving Macha's "standard skeleton").
> **Companion documents**: `direction.md` (minimum verifiable direction: long-term memory + character consistency), `positioning.md` (four-paper positioning), `architecture.md` (target architecture).
> **Core proposition**: No standard evaluation, no standard skeleton. Macha's evaluation must simultaneously cover **functional dimensions** (believability, consistency, memory, planning) and **engineering dimensions** (latency, cost, throughput, observability), and be able to prove in a reusable way that it is "more believable, more consistent, more debuggable than other NPC solutions."

---

## 0. How to Use This Document

- **Section 1** gives the evaluation framework's layers, to assemble scattered benchmarks into a system.
- **Section 2 "Evaluation-Dimension Table"** is the main deliverable for engineering teams: each row is a metric landable in Macha (dimension / measured object / method / related benchmark / meaning for Macha).
- **Section 3 "Benchmark Dataset List"** is the main deliverable for researchers: datasets directly runnable for experiments.
- **Section 4 "Source Collection"** registers key sources in the fixed format agreed in `information_needs.md`.
- **Section 5** gives Macha landing suggestions (anti-hallucination stress-test design, engineering instrumentation, observability).

> Note: All URLs were actually obtained via WebSearch / WebFetch in this research. **LongMemEval** was only found via secondary surveys (primary arXiv direct link not verified), clearly marked in the corresponding entry; other main links were verified or come from paper / official-repo pages.

---

## 1. Evaluation Framework Overview

Macha's evaluation system is recommended in three layers, to avoid "only running academic leaderboards, not solving game landing":

| Layer | Name | Solves what | Typical means |
|---|---|---|---|
| L1 | **Offline functional benchmark** | Whether the NPC "remembers, speaks in-character, doesn't ramble" | LoCoMo / LongMemEval / MemoryArena / RoleBench / PersonaChat |
| L2 | **Online engineering metrics** | Whether the NPC "runs, is measurable, is tunable" | Latency/cost/throughput instrumentation + LangSmith/Phoenix tracing |
| L3 | **Player subjective evaluation** | Whether the NPC "looks believable, predictable" | Believability scale + TrueSkill pairing evaluation |

> The three layers correspond to the three-layer meaning of the Macha name: **M** (Memory, L1), **A** (Architecture/Action, L1 planning + L2 engineering), **C** (Character, L1 consistency + L3 believability).

---

## 2. Evaluation-Dimension Table

> Dimension classification: functional (F) / engineering (E). The "method" column gives concrete operable practices; the "related benchmark" column points to Section 3 datasets.

| # | Dimension | Measured object | Method | Related benchmark | Meaning for Macha |
|---|---|---|---|---|---|
| F1 | **Role Fidelity / character consistency** | Stability of personality, speaking style, values, taboos over long interaction | 1) RoleBench three metrics: CUS (style consistency), RAW (character accuracy & propriety), SPE (character-specific knowledge); 2) DNLI-based dialogue entailment-consistency judgment; 3) fixed persona then "adversarial persona-drift" detection | RoleLLM/RoleBench, PersonaChat, LoCoMo, Clembench | Macha's core selling point distinguishing it from "generic chatbots"; a property the "standard skeleton" must be able to measure and guarantee |
| F2 | **Long-term memory stability** | Cross-session information extraction, multi-session reasoning, knowledge update, temporal reasoning, abstention ability | 1) Long-dialogue multi-hop Q&A; 2) knowledge-update test (take latest when same fact contradicts across time); 3) temporal Q&A; 4) explicit abstention rate when info not provided | LoCoMo, LongMemEval, MemoryArena, RULER | Directly proves Macha's M (Memory): "still remembers the player after multiple dialogues" is the first milestone |
| F3 | **Believability** | Degree to which players subjectively think the NPC "is like a real existing person/character" | 1) Paiva believability dimensions Likert scale (consistency, experience change, awareness, understandability, personality, emotion expression, sociability, visual impact, predictability); 2) perceived-intelligence scale (competent/knowledgeable/responsible/clever/wise) | Clembench, LIGHT, custom player research | Directly corresponds to project goal "believable NPC"; prerequisite for player adoption and investment |
| F4 | **Anti-hallucination / anti-character-drift** | Whether it fabricates un-happened events, drifts from setting over long run, confuses old/new facts | 1) LoCoMo adversarial QA; 2) LongMemEval's Knowledge Update + Abstention; 3) custom "memory-consistency stress test" (see Section 5) | LoCoMo, LongMemEval, MemoryArena | Related to player trust and safety; the bottom line of "standard skeleton" reliability |
| F5 | **Planning & decision ability** | NPC's goal planning, tool use, multi-agent collaboration in the game world | 1) Multi-environment task-success rate; 2) collaboration-efficiency score CoS; 3) 9 agent-capability sub-items (object-dependency reasoning, prospective planning, spatial reasoning, learning from history, randomness understanding, etc.) | AgentBench, SmartPlay, MindAgent, WebArena | Corresponds to A (Architecture) action layer: NPC not just chats, must be able to act in the world |
| F6 | **Dialogue quality / multi-turn consistency** | Multi-turn dialogue coherence, task completion, role-play naturalness | 1) MT-Bench multi-turn eight-dimension (GPT-4 scoring); 2) task-oriented dialogue DST accuracy; 3) grounded-dialogue reasonableness | MT-Bench, DSTC/MultiWOZ, LIGHT | Base dialogue-layer quality; the floor of role-play experience |
| F7 | **Predictability** | Whether behavior can be understood and anticipated by players (not over-random, not fully rigid) | 1) Paiva predictability-dimension scale; 2) behavior-trajectory entropy / explainability score | LIGHT, custom | Foundation of playability; also premise of "debuggable NPC" (see F12/E12) |
| F8 | **Long-context understanding** | Retrieval and reasoning robustness in ultra-long context | 1) Synthetic controllable tasks (NIAH variants, multi-hop tracking, aggregation); 2) real long-document QA | LongBench, RULER | Complements Macha memory retrieval: decides "stuff memory into context" vs. "externalized memory system" |
| E9 | **Latency** | Single-response, time-to-first-token, end-to-end turn latency | Inference instrumentation timing (first token / last token); trace auto-collection | Self-built + Phoenix/LangSmith trace | Hard constraint of real-time dialogue experience; decides "whether usable in online games" |
| E10 | **Cost** | Per-turn / per-session token cost, retrieval and tool-call cost | Token counting + cost dashboard; compare unit cost of different memory strategies | Self-built | Commercial feasibility; economic trade-off of externalized memory vs. long context |
| E11 | **Throughput** | Concurrent NPC count, QPS, sessions processed per unit time | Load test (concurrent scenario, batch inference) | Self-built | Multi-NPC scenario scaling; open world needs to drive many NPCs simultaneously |
| E12 | **Observability** | Decision chain traceable, replayable, debuggable | OpenTelemetry/OpenInference trace; LangSmith or Phoenix dashboard | Self-built trace spec + LangSmith/Phoenix | Engineering landing of explainability: players need "predictable NPC", developers need "debuggable NPC" |
| E13 | **Reproducibility / regression** | Cross-version quality stability | Fixed dataset + experiment comparison; Phoenix datasets/experiments | Phoenix, LongMemEval fixed set | Continuous-iteration guarantee: every skeleton change proves "no regression" |

---

## 3. Benchmark Dataset List

> "Access & license": confirmed specific licenses noted; others subject to repo LICENSE (paper datasets mostly released with repo, commercial use needs item-by-item check).

| Name | Measured content | Access & license | Relevance to Macha |
|---|---|---|---|
| **AgentBench** | LLM as agent multi-turn decision & reasoning in 8 environment classes (OS/DB/knowledge graph/card/puzzle/housework/shopping/browsing) | Paper https://arxiv.org/abs/2308.03688 ; code/data https://github.com/THUDM/AgentBench ; leaderboard https://llmbench.ai/agent ; subject to repo LICENSE | Verify Macha action layer (F5) capability baseline on general tasks |
| **WebArena** | Real self-hostable Web environment (e-commerce/forum/collab-dev/content-mgmt) end-to-end task-success rate (programmatic correctness check) | Paper https://arxiv.org/abs/2307.13854 ; env/data https://webarena.dev (ICLR 2024) | Evaluate NPC planning & execution on "open-environment tool use" (F5) |
| **ToolBench / ToolLLM** | 16,464 real REST API tool-call ability (single/multi-tool, DFSDT planning); ToolEval pass rate / win rate | Paper https://arxiv.org/abs/2307.16789 ; data/model https://github.com/OpenBMB/ToolBench ; subject to repo LICENSE | Benchmark for NPC calling game / external tools (F5, E10 cost) |
| **MindAgent (CUISINEWORLD)** | Multi-NPC collaboration + human-machine collaboration planning / coordination; new metric CoS (collaboration score) | Paper https://arxiv.org/abs/2309.09971 ; homepage https://mindagent.github.io (NAACL 2024 Findings) | Direct reference for Macha multi-agent collaboration scenario (F5); provides CoS measurement paradigm |
| **SmartPlay** | 6 games (incl. Minecraft, tower, RPS, etc.) evaluate 9 agent capabilities; infinite environment variation | Paper https://arxiv.org/abs/2310.01557 ; code https://github.com/LLMsmartplay/SmartPlay (paper labeled) / Microsoft/SmartPlay | Use "game" itself as agent-capability probe (F5, F7 predictability) |
| **Clembench** | Evaluate conversational agents via dialogue games (Taboo, Wordle, Drawing, etc.); third paradigm "dialogue-game evaluation" | EMNLP 2023 https://aclanthology.org/2023.emnlp-main.689 ; 2025 paradigm paper https://arxiv.org/abs/2507.08491 ; framework https://clembench.github.io | Measure dialogue ability via "gamified interaction" (F6), naturally fits NPC scenario; reusable for Macha self-test |
| **LoCoMo** | Ultra-long-horizon dialogue memory (longest 35 sessions / ~300 turns / 9K token); QA (single-hop/multi-hop/temporal/open-domain/adversarial) + event summary + multimodal generation | Paper https://arxiv.org/abs/2402.17753 (ACL 2024); code/data https://github.com/snap-research/LoCoMo ; subject to repo LICENSE | Macha memory module (F2, F4) most core dialogue-memory benchmark; adversarial set directly tests anti-hallucination |
| **LongMemEval** | Long-horizon interactive memory five dimensions: info extraction, multi-session reasoning, temporal reasoning, knowledge update, abstention; with S (~115K token) and M (~1.5M token) variants | Primary arXiv direct link not verified this round; obtainable via ICLR 2025 proceedings / project page. Survey ref: https://www.emergentmind.com/topics/longmemeval , https://www.gamgee.ai/blogs/longmemeval-explained | Key supplement for "does memory guide action"; knowledge-update / abstention dimensions hit character drift (F2, F4). **Primary link pending verification** |
| **MemoryArena** | Multi-session, subtask strongly causal-dependent "memory-agent-environment" closed loop; memory must come from past actions and guide future actions | Paper https://arxiv.org/abs/2602.16313 (2026-02, verified) | Reveals gap "high static-memory-test score ≠ truly usable" (F2, F4, F5 closed loop); exemplar for Macha memory-action coupling evaluation |
| **LongBench** | Chinese-English bilingual, 6 major classes (single/multi-doc QA, summary, few-shot, synthetic, code) long-context understanding | Paper https://arxiv.org/abs/2308.14508 ; data/code https://github.com/THUDM/LongBench | Long-context capability baseline (F8); includes Chinese, good for Chinese NPC scenarios |
| **RULER** | Synthetic controllable long-context benchmark: retrieval/multi-hop tracking/aggregation/QA, supports arbitrary length & difficulty | Paper https://arxiv.org/abs/2404.06654 (COLM 2024); code https://github.com/NVIDIA/RULER | Diagnose Macha's real ceiling of "stuff memory into context" (F8), stricter than NIAH |
| **PersonaChat** | Persona-based multi-turn dialogue consistency & engagement | Paper https://arxiv.org/abs/1801.07243 ; data ParlAI / HuggingFace `persona-chat` (**CC BY 4.0**, not MIT; commercial use requires attribution) | Entry-level benchmark for role consistency (F1); directly usable as consistency regression test |
| **LIGHT** | Large fantasy text-adventure world (663 locations / 3462 objects / 1755 characters), tests "speaks and acts" grounded dialogue | Paper https://arxiv.org/abs/1903.03094 ; platform https://parl.ai/projects/light (subject to repo LICENSE) | Unified environment for NPC "perceive-speak-act" in world (F3, F6, F7); closest research platform to game NPCs |
| **DSTC / MultiWOZ** | Task-oriented dialogue state tracking (DST) and multi-domain task completion | DSTC series https://github.com/tranmduc/Awesome-Dialogue-State-Tracking ; MultiWOZ etc. released with respective repos | Metric for NPC as "functional dialoguist" (task/trade/guidance) (F6); DST accuracy can serve as consistency proxy |
| **RoleLLM / RoleBench** | Fine-grained role-play: CUS (style consistency) / RAW (character accuracy & propriety) / SPE (character knowledge) | Paper https://arxiv.org/abs/2310.00746 ; ACL 2024 https://aclanthology.org/2024.findings-acl.878 ; data RoleBench (168,093 samples) | Most systematic academic benchmark for role consistency (F1); provides quantifiable "role fidelity" definition |
| **MT-Bench** | Multi-turn dialogue quality eight dimensions (writing/role-play/reasoning/math/code/knowledge/extraction/STEM), GPT-4 scoring | Paper/code https://github.com/lm-sys/FastChat (MT-Bench with repo) | Quick regression for dialogue quality (F6); role-play dimension directly reusable as Macha role-play score |

---

## 4. Source Collection (in agreed format)

> Each entry follows `information_needs.md` specified format:
> [Category] / [Title] / [Link / file path] / [One-sentence summary] / [Key conclusions] / [Reusable things]

---

[Category]Academic paper / Engineering implementation
[Title]AgentBench: Evaluating LLMs as Agents
[Link / file path]https://arxiv.org/abs/2308.03688 ; https://github.com/THUDM/AgentBench
[One-sentence summary]The first systematic multi-dimensional benchmark evaluating "LLM as agent," covering 8 real environment classes.
[Key conclusions]
1. Existing LLM-as-agent capability remains a main bottleneck in long-horizon reasoning, decision, instruction following.
2. Commercial API models significantly stronger than open-source, but still clearly far from "usable."
3. Code and high-quality multi-turn alignment-data training can improve agent performance.
4. Provides a plug-and-play evaluation toolkit to score any LLM.
[Reusable things]Evaluation package (8 environments), leaderboard method, multi-environment task-success-rate caliber — can serve as Macha action-layer baseline.

---

[Category]Academic paper / Engineering implementation
[Title]WebArena: A Realistic Web Environment for Building Autonomous Agents
[Link / file path]https://arxiv.org/abs/2307.13854 ; https://webarena.dev
[One-sentence summary]Self-hostable real Web environment, evaluates agent end-to-end task-success rate via programmatic checks.
[Key conclusions]
1. Even GPT-4 end-to-end success rate only 14.41%, far below human 78.24%.
2. Tasks are long-horizon, need cross-site planning and reasoning.
3. Provides reproducible self-hosted environment and 812 benchmark tasks.
[Reusable things]Self-hosted environment setup, programmatic correctness validation — can inform Macha's "game-environment auto-scoring."

---

[Category]Academic paper / Engineering implementation
[Title]ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs (incl. ToolBench)
[Link / file path]https://arxiv.org/abs/2307.16789 ; https://github.com/OpenBMB/ToolBench
[One-sentence summary]Builds a tool-use instruction dataset of 16,464 real APIs and evaluator ToolEval.
[Key conclusions]
1. Open-source model fine-tuned on ToolBench (ToolLLaMA) can reach ChatGPT-comparable tool-use ability.
2. DFSDT (depth-first search decision tree) significantly improves complex-instruction planning.
3. ToolEval auto-evaluates with pass-rate / win-rate dual metrics.
[Reusable things]API retriever design, auto-evaluator idea — Macha NPC calling game/external tools can directly adopt.

---

[Category]Academic paper / Engineering implementation
[Title]MindAgent: Emergent Gaming Interaction (incl. CUISINEWORLD)
[Link / file path]https://arxiv.org/abs/2309.09971 ; https://mindagent.github.io
[One-sentence summary]Game-interaction evaluation infrastructure for "multi-NPC collaboration + human-machine collaboration," proposes collaboration score CoS.
[Key conclusions]
1. Existing game frameworks lack a "general multi-agent collaboration" benchmark.
2. Introduces CUISINEWORLD scenario and collaboration-efficiency metric CoS.
3. Deployable to VR version and Minecraft domain.
[Reusable things]CoS collaboration metric, memory-history/action-module interface design — direct reference for Macha multi-agent collaboration evaluation.

---

[Category]Academic paper
[Title]SmartPlay: A Benchmark for LLMs as Intelligent Agents
[Link / file path]https://arxiv.org/abs/2310.01557 ; https://github.com/LLMsmartplay/SmartPlay
[One-sentence summary]Splits 6 games into 9 agent capabilities, diagnosable item-by-item for weaknesses.
[Key conclusions]
1. Each game challenges a subset of 9 capabilities (object-dependency reasoning, prospective planning, spatial reasoning, learning from history, randomness understanding, etc.).
2. Provides unified extensible API, supports infinite environment variation.
3. Both a benchmark and a methodology (capability triage).
[Reusable things]"Capability dimension × game" mapping method — Macha can use same idea to split NPC capabilities into measurable items.

---

[Category]Academic paper / Engineering implementation
[Title]clembench: Using Game Play to Evaluate Chat-Optimized LLMs as Conversational Agents
[Link / file path]EMNLP 2023 https://aclanthology.org/2023.emnlp-main.689 ; 2025 paradigm paper https://arxiv.org/abs/2507.08491 ; https://clembench.github.io
[One-sentence summary]Evaluates conversational agents via constrained dialogue games (Taboo, Wordle, etc.), and proposes the "dialogue-game evaluation" third paradigm.
[Key conclusions]
1. Gamified interaction can test goal-oriented dialogue under controlled, reproducible, multi-turn, no-reference conditions.
2. Metrics far from saturated, continuous diagnostic value.
3. 2025 clembench optimized into an easily reusable framework, customizable tests.
[Reusable things]Dialogue-game evaluation framework and game instances — can be remodeled into Macha's NPC dialogue self-test mini-games.

---

[Category]Academic paper
[Title]Evaluating Very Long-Term Conversational Memory of LLM Agents (LoCoMo)
[Link / file path]https://arxiv.org/abs/2402.17753 ; https://github.com/snap-research/LoCoMo
[One-sentence summary]Builds an ultra-long-horizon dialogue-memory benchmark up to 35 sessions, with five QA classes + event summary + multimodal generation.
[Key conclusions]
1. Long context and RAG help, but far behind humans, especially temporal/multi-hop/adversarial questions.
2. Dialogue via "LLM generation + human verification," anchored to temporal event graph.
3. Public `locomo10.json` (~10 longest dialogues, ~1540 QA).
[Reusable things]QA five-classification (single-hop/multi-hop/temporal/open-domain/adversarial) + event-graph summary task — core template for Macha memory evaluation.

---

[Category]Academic paper (survey, primary link pending verification)
[Title]LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory
[Link / file path]Primary arXiv direct link not verified this round; survey ref https://www.emergentmind.com/topics/longmemeval and https://www.gamgee.ai/blogs/longmemeval-explained (ICLR 2025, UCLA & Tencent AI Lab)
[One-sentence summary]Uses 500 questions on real chat history to systematically test long-horizon memory five dimensions (info extraction / multi-session reasoning / temporal / knowledge update / abstention).
[Key conclusions]
1. Long-context LLM drops 30–60% performance from Oracle to standard set (not a length issue, an attention issue).
2. Knowledge update very easily returns stale facts; even with perfect retrieval, reading comprehension still errs.
3. Provides S (~115K) / M (~1.5M token) two tiers, M exceeds most context windows, forcing a real memory system.
[Reusable things]Memory five-dimension definition and variant design — direct basis for Macha anti-hallucination / knowledge-update stress test.

---

[Category]Academic paper
[Title]MemoryArena: Benchmarking Agent Memory in Interdependent Multi-Session Agentic Tasks
[Link / file path]https://arxiv.org/abs/2602.16313 (2026-02, verified)
[One-sentence summary]Evaluates in a "memory-agent-environment" multi-session closed loop whether memory truly guides future action.
[Key conclusions]
1. Existing benchmarks split "memory" and "action"; MemoryArena forces subtask causal dependency.
2. Systems near-saturated on LoCoMo/LongMemEval have extremely low task-completion here.
3. Average 6.9 interdependent subtasks, ~57 action steps, trajectory over 40K token per task.
[Reusable things]"Memory-action-environment" closed-loop evaluation structure, interdependent-subtask design — exemplar for Macha end-to-end evaluation.

---

[Category]Academic paper
[Title]LongBench / RULER (long-context understanding benchmarks)
[Link / file path]LongBench https://arxiv.org/abs/2308.14508 , https://github.com/THUDM/LongBench ; RULER https://arxiv.org/abs/2404.06654 , https://github.com/NVIDIA/RULER
[One-sentence summary]LongBench is the first Chinese-English bilingual long-context multi-task benchmark; RULER is synthetic-controllable, stricter than NIAH long-context diagnosis.
[Key conclusions]
1. LongBench has 21 datasets, 6 major classes, auto-evaluation, includes Chinese.
2. RULER near-perfect on vanilla NIAH, but multi-hop/aggregation tasks drop sharply with length; only about half of 32K models maintain satisfactory performance.
3. RULER supports arbitrary length/difficulty config, convenient for stress testing.
[Reusable things]Long-context evaluation task family and config method — for deciding Macha memory "stuff context" vs. "externalized retrieval."

---

[Category]Academic paper / Dataset
[Title]Personalizing Dialogue Agents: I have a dog, do you have pets too? (PersonaChat)
[Link / file path]https://arxiv.org/abs/1801.07243 ; HuggingFace `persona-chat` (MIT License)
[One-sentence summary]Uses explicit personas to drive multi-turn dialogue, evaluates role consistency, foundational dataset for role-play research.
[Key conclusions]
1. Early revealed "chat models lack consistent personality and long-term memory" problem.
2. Provides persona-conditioned generation and reply-selection tasks.
3. Spawned DNLI dataset turning consistency judgment into natural-language inference.
[Reusable things]Persona-driven dialogue protocol, consistency-evaluation idea — starting point for Macha role-consistency regression test.

---

[Category]Academic paper / Engineering implementation
[Title]Learning to Speak and Act in a Fantasy Text Adventure Game (LIGHT)
[Link / file path]https://arxiv.org/abs/1903.03094 ; https://parl.ai/projects/light
[One-sentence summary]Large fantasy text-adventure world, studies "speaks and acts" grounded dialogue.
[Key conclusions]
1. 663 locations / 3462 objects / 1755 characters, fully natural-language described, with dialogue and action/emotion.
2. Grounded (location, object, character, past action) significantly improves dialogue and action prediction.
3. Human performance still beats models, showing grounded interaction far from solved.
[Reusable things]"World state + character persona + dialogue/action" unified environment — closest research platform to game NPCs, usable as Macha simulation sandbox.

---

[Category]Academic paper / Dataset
[Title]RoleLLM: Benchmarking, Eliciting, and Enhancing Role-Playing Abilities of LLMs (RoleBench)
[Link / file path]https://arxiv.org/abs/2310.00746 ; https://aclanthology.org/2024.findings-acl.878
[One-sentence summary]First fine-grained character-level benchmark RoleBench (168,093 samples), gives quantifiable "role fidelity" definition.
[Key conclusions]
1. Three metrics: CUS (Lexical Consistency + Dialogic Fidelity), RAW (accuracy & propriety), SPE (character-specific knowledge).
2. System-instruction method beats retrieval augmentation, saves context and is more noise-resistant.
3. Open-source RoleLLaMA can approach GPT-4-level RoleGPT on style/knowledge.
[Reusable things]Role-fidelity three-metric definition — direct measurement standard for Macha F1 dimension (role consistency).

---

[Category]Academic paper / Methodology
[Title]Generative Agents human evaluation and TrueSkill ranking (incl. TrueSkill protocol)
[Link / file path]Generative Agents paper https://arxiv.org/abs/2304.03442 ; TrueSkill human-evaluation explanation https://www.53ai.com/news/qianyanjishu/2024070161709.html ; Chatbot Arena methodology https://lumenfall.ai/arena/methodology
[One-sentence summary]Uses TrueSkill (Bayesian skill rating, μ/σ dual parameters) to turn human paired ranking into comparable interval scores.
[Key conclusions]
1. TrueSkill is the multi-player extension of Elo, naturally supports uncertainty modeling (σ).
2. Generative Agents had 100 evaluators rank 5 conditions, then TrueSkill score + Kruskal-Wallis significance test.
3. Leaderboards often use `Elo = 1000 + 10×(μ − 3σ)` conservative lower bound, avoiding few-win inflation.
[Reusable things]TrueSkill paired-evaluation protocol — standardized method for Macha L3 player subjective evaluation (believability / predictability).

---

[Category]Academic paper / Design theory
[Title]Breaking Players' expectations: the Role of NPCs' coherence and consistency (incl. Believability scale)
[Link / file path]https://arxiv.org/abs/2512.07388 (verified); Believability dimensions from Paiva et al. survey (fenix.tecnico.ulisboa.pt PDF) and Gorman et al. believability index
[One-sentence summary]In a military shooter proves: NPC coherent/consistent design reinforces player expectations, conversely challenges them; gives perceived-intelligence and believability scales.
[Key conclusions]
1. Player "perceived intelligence" measured by five-semantic-item scale (competent/knowledgeable/responsible/clever/wise) on two dimensions: understandability + performance.
2. "Believability" measured by nine-dimension Likert scale: awareness, behavior understandability, personality, visual impact, predictability, behavior consistency, experience change, sociability, emotion expression.
3. Coherent consistent design reinforces player expectations; breaking consistency significantly affects evaluation.
[Reusable things]Believability scale and "coherence/consistency → player expectation" framework — Macha F3/F7 subjective-evaluation questionnaire template.

---

[Category]Engineering implementation / Industry tool
[Title]LangSmith (Agent engineering platform: observability, evaluation, deployment)
[Link / file path]https://www.langchain.com/ ; https://support.langchain.com/articles/8854797554-what-is-langsmith
[One-sentence summary]Framework-agnostic agent observability and evaluation platform, splits each run into structured steps via trace.
[Key conclusions]
1. Compatible with any framework / self-built code, one env variable to enable tracing.
2. Provides tracing, real-time monitoring (cost/latency/quality), auto-clustering similar dialogues, evaluation and deployment.
3. Supports OpenTelemetry, can self-host, promises not to train on customer data.
[Reusable things]Trace data structure, cost/latency dashboard idea — reference implementation for Macha E9/E10/E12 observability.

---

[Category]Engineering implementation / Open-source tool
[Title]Arize Phoenix (open-source LLM observability and evaluation, based on OpenInference/OpenTelemetry)
[Link / file path]https://arize.com ; https://www.aiwisdom.dev/articles/ai-observability/phoenix
[One-sentence summary]Locally / self-hostable open-source observability and evaluation stack, native OTel, built-in hallucination/QA/relevance evaluators.
[Key conclusions]
1. Uses OpenInference semantic conventions (superset of OTel gen_ai.*), trace portable to any OTLP backend.
2. Built-in HallucinationEvaluator / QAEvaluator / RelevanceEvaluator, scores hung back on span.
3. Datasets + Experiments supports "extract dataset from failed trace → run experiment comparing prompt/model → regression test."
[Reusable things]Evaluators (hallucination/relevance/QA) + experiment-comparison workflow — direct tool for Macha E12/E13 anti-hallucination evaluation and regression testing.

---

## 5. Macha Landing Suggestions

### 5.1 Anti-hallucination / Long-term Consistency Stress-Test Design (Macha-specific)

"Translate" the above benchmarks into stress tests Macha can run automatically; suggest covering four adversarial classes:

1. **Memory adversarial (from LoCoMo adversarial + LongMemEval Abstention)**: plant "trap questions" in long dialogue, induce NPC to fabricate un-happened events; expect NPC to return "I'm not sure / no such info" rather than hallucinate.
2. **Knowledge update (from LongMemEval KU)**: same fact given contradictory versions in session 1 and session N (e.g., "my brother is A" → "my brother is B"), test whether NPC takes the latest value without self-contradiction.
3. **Time dislocation (from LongMemEval TR + LoCoMo temporal)**: ask with relative-time words ("last week," "tomorrow afternoon"), test whether NPC anchors to correct session time.
4. **Action-memory closed loop (from MemoryArena)**: design subtask strongly causal-dependent mini-games; NPC must remember key constraints in early sessions to correctly complete later tasks; directly exposes "remembers but can't use" pseudo-memory.

> Form: each stress test produces **quantifiable score + failed trace** (recorded via Phoenix), included in Macha regression set.

### 5.2 Engineering-Metric Instrumentation (latency / cost / throughput)

- Instrument at each stage of `Agent` (see `src/macha/core/agent.py`) perception→memory→reasoning→action, recording time-to-first-token, per-stage duration, token count.
- Send trace via OpenTelemetry/OpenInference to LangSmith or Phoenix (either, both framework-agnostic).
- Build a "memory-strategy comparison table": same NPC with (a) pure long context, (b) RAG, (c) Macha externalized memory, compare F2/F4 scores and E9/E10 cost, give engineering conclusion of "when to use memory system."

### 5.3 Explainability and Debuggability

- **Why players need predictable NPC**: too-high behavior entropy breaks believability and "playability" (Paiva's predictability dimension); over-random or fully rigid both harm experience.
- **Why developers need debuggable NPC**: LLM non-determinism makes faults hard to locate. Using trace to make explicit "which memory retrieval hit, which reflection adopted, which tool call failed" is the observable base Macha as "standard skeleton" must provide.
- **Suggestion**: Macha by default exports OpenInference-compatible trace, so developers can debug locally free with Phoenix, enterprises can use LangSmith hosting — both paths not locked to a single vendor.

### 5.4 Mapping Between Evaluation and Macha Architecture

| Macha module (architecture.md) | Main eval dimension | Recommended benchmark |
|---|---|---|
| Memory | F2 long-term memory, F4 anti-hallucination | LoCoMo, LongMemEval, MemoryArena, RULER |
| Reasoning / Reflection | F1 role consistency, F5 planning | RoleBench, AgentBench, SmartPlay |
| Perception / Action | F5 planning decision, F6 dialogue quality | WebArena, MindAgent, LIGHT, MT-Bench |
| Character (persona layer) | F1/F3/F7 consistency/believability/predictability | RoleBench, Clembench, Believability scale |
| Engineering / deployment | E9–E13 | Self-built instrumentation + LangSmith/Phoenix |

---

## 6. To-Supplement and To-Verify Items

- **LongMemEval primary arXiv direct link not verified**: secondary survey links listed, please complete primary paper source before formal citation (ICLR 2025 proceedings / project page).
- **Commercial license of each dataset**: PersonaChat is actually CC BY 4.0 (not MIT); other paper datasets released with repo, commercial use needs item-by-item check of LICENSE and data source (especially LIGHT, LoCoMo with human annotation and image descriptions).
- **Chinese NPC benchmark gap**: existing role-play / memory benchmarks are mostly English; if Macha targets the Chinese market, suggest building self-owned Chinese persona and dialogue-memory sets on top of RoleBench (already has 5 Chinese characters) and LongBench (has Chinese).
- **Player subjective-evaluation sample**: F3/F7 Believability scale needs real player research (suggest combining TrueSkill paired evaluation, see Section 4 sources).

---

## 7. Deepening Supplement: Evaluation Harness Design and Quantified SLO

> **Chapter positioning**: Without changing the Section 1–6 framework (L1–L3 three layers, F1–F13 dimensions), supplement four deepening contents —
> (A) Breadth + timeliness: 2025–2026 first-hand new benchmarks and dataset scales;
> (B) Macha evaluation harness design spec (config schema + scorer pseudocode + quantified SLO);
> (C) Chinese-market section (SuperCLUE / FlagEval / OpenCompass / Chinese role-consistency benchmark);
> (D) Quantified landing (dataset-scale number table + Macha v0.1 priority-access list and pass thresholds).
>
> **Source credibility note**: New links in this chapter were all actually obtained via WebSearch/WebFetch; those marked "(pending verification)" are primary arXiv direct links or official sites not individually opened this round, please complete before formal citation. Other project pages / code repos / leaderboards come from accessible pages.

### 7.1 Breadth + Timeliness: 2025–2026 Key New Benchmarks

The following benchmarks fill four gaps in the original document — "agent long-effect interaction consistency," "game-world grounded NPC," "long-context deep reasoning," "Chinese role consistency" — registered per original Section 3 caliber, and complete **dataset-scale numbers** (see 7.4 scale table).

| Name | Measured content | Year / conference | Relevance to Macha (dimension) |
|---|---|---|---|
| **τ-bench / τ²-bench / τ³-bench** | Tool-agent-user multi-turn dynamic interaction, domain-rule adherence, consistency (pass^k reliability metric) | 2024 / ICLR 2025 (τ² 2025, τ³ 2026) | Test NPC "customer-service / task-oriented dialogue" **consistency crisis** (F1/F6/E13); pass^k directly maps to Macha regression stability |
| **OSWorld / OSWorld-Verified** | Real OS (Ubuntu/Win/macOS) execution-scored multimodal agent | NeurIPS 2024, 2025 upgrade | "Game-environment auto-scoring" engineering exemplar (F5/F6/E12); execution-state check reusable for Macha world actions |
| **GAIA / GAIA 2** | 466 multi-step tasks needing reasoning + multimodal + web + tools (unique answer, auto-scorable) | 2023 / ICLR 2024; GAIA 2 dynamic-environment upgrade | Task-oriented NPC evaluation reference (F5/F6); difficulty grading inspires Macha stepped stress test |
| **MemBench** | Fact + reflection memory, participatory + observational dual scenario, four metrics (accuracy/recall/capacity/efficiency) | ACL 2025 | **Finer-grained** framework for Macha memory module (M/F2): adds "reflection memory," "observational scenario," "capacity/efficiency" |
| **LongBench v2** | 503 deep-understanding-reasoning long-context multiple-choice, 8k–2M words, 6 major 20 sub-tasks | ACL 2025 | F8 long-context "true understanding vs. retrieval" decision basis; long-dialogue-history understanding subtask hits Macha |
| **FRAMES** | 824 cross-2–15-wiki multi-hop RAG QA, unified tests factuality/retrieval/reasoning | NAACL 2025 | End-to-end stress-test template for Macha memory retrieval (M) + anti-hallucination (F4) |
| **GRUtopia / GRBench** | Embodied-town simulation + LLM NPC (GRResidents) + three-tier embodied evaluation | 2024 (arXiv pending verification) | Game-world grounded NPC simulation sandbox (F3/F5/F6); "describe/localize/dialogue/task-allocation" four abilities |
| **SuperCLUE-Role** | Chinese-native role-play: base ability + acting power + scenario application (incl. game-NPC sub-leaderboard) | 2024 (CLUEbenchmarks) | Macha F1/F3 Chinese landing benchmark; explicitly lists "game NPC" as scenario |
| **CharacterEval** | Chinese role-play conversational agent: 1785 dialogues / 23020 examples / 77 characters / 13 metrics / 4 dims | ACL 2024 | Macha F1 Chinese auto-scorer (CharacterRM) direct tool |
| **CPDC 2025** | Game NPC "commonsense persona-grounded dialogue" challenge: task-oriented / context-aware / fused | 2025 competition | "Task fidelity vs. character immersion" dual-objective trade-off paradigm (F1/F5) |

---

### 7.2 Macha Evaluation Harness Design Spec

#### 7.2.1 (a) YAML / JSON config schema for one benchmark run

> Design principle: one run = "one NPC backend × one memory strategy × one scenario set × one scorer set × one SLO set". Config consumable directly by CI, also replayable by Phoenix/LangSmith.

```yaml
# macha_eval_run.yaml  —— Macha v0.1 evaluation run config
benchmark_run:
  meta:
    name: macha-v0.1-eval
    version: 0.1.0
    run_id: auto            # injected by harness, for regression tracking

  model:
    npc_backend: openai/gpt-4o-mini   # generation backend under test
    memory: macha-external            # none | long-context | rag | macha-external
    temperature: 0.3
    max_tokens: 512

  suite:                     # scenario set: each scenario declares which dims it scores (subset of L1..L13)
    - id: locomo-10
      type: long_term_memory
      path: data/locomo10.json
      dims: [F2, F4]                 # long-term memory stability / anti-hallucination
      scoring: qa_f1
    - id: longmemeval-s
      type: long_term_memory
      path: data/longmemeval_s.json
      dims: [F2, F4]
      scoring: subset_accuracy
    - id: rolebench-cus
      type: role_fidelity
      path: data/rolebench
      dims: [F1]                     # role consistency
      scoring: cus_raw_spe
    - id: superclue-role-game-npc
      type: role_fidelity_zh
      path: data/superclue_role
      dims: [F1, F3]                 # Chinese role consistency / believability
      scoring: characterrm
    - id: charactereval-zh
      type: role_fidelity_zh
      path: data/charactereval
      dims: [F1]
      scoring: characterrm
    - id: macha-adversarial-trap     # self-built anti-hallucination stress test (see 5.1)
      type: anti_hallucination
      path: data/macha_traps.json
      dims: [F4]
      scoring: abstention_rate

  scorer:                    # scorers: correspond one-to-one with dims
    role_consistency:
      method: llm_judge            # or characterrm / dnli
      judge_model: gpt-4o
      threshold: 0.85
    hallucination:
      method: abstention_rate      # trap questions should explicitly refuse not fabricate
      threshold: 0.02
    memory_qa:
      method: qa_f1

  slo:                       # quantified SLO (see 7.3)
    latency_p95_ms: 800
    cost_per_turn_usd: 0.002
    throughput_turn_per_s: 15
    role_fidelity_min: 0.85
    hallucination_max: 0.02
    memory_f2_min: 0.80

  reporting:
    trace_backend: phoenix        # langsmith | phoenix
    export: openinference         # OTel-compatible, vendor-independent
    regression_baseline: results/macha-v0.0.9.json
```

#### 7.2.2 (b) Reference scorer pseudocode

```python
def run_suite(npc, suite, scorer, dims=L1_to_L13):
    """One complete benchmark run: iterate scenario set, run NPC and score on each scenario.

    npc     : Macha NPC runtime (with memory module), must implement reset()/run()
    suite   : scenario set (from config.suite)
    scorer  : scorer set (config.scorer)
    dims    : full eval-dimension set L1..L13; each scenario only scores its declared subset
    """
    report = EvalReport(run_id=auto_id())

    for scenario in suite:
        npc.reset(memory=scenario.seed_memory)     # inject initial memory / persona
        transcript = []

        for turn in scenario.turns:
            # —— NPC inference + engineering instrumentation ——
            npc_output = npc.run(turn.user_input, ctx=scenario.context)
            transcript.append((turn, npc_output))

            # E9/E10: latency and cost collected in real time
            report.latency.record(npc_output.latency_ms)
            report.cost.record(npc_output.cost_usd)
            # E12: export OpenInference-compatible trace, replayable in Phoenix/LangSmith
            emit_trace(openinference_span(scenario, turn, npc_output))

        # —— functional scoring: scorer only scores scenario.dims declared dims (subset of L1..L13) ——
        scores = scorer(
            npc_output=transcript,
            expected=scenario.expected,
            dims=scenario.dims,            # e.g. [F2, F4] or [F1, F3]
        )
        report.scores.merge(scores)

        # F4: adversarial / abstention special — trap questions must refuse not hallucinate
        if scenario.has_trap:
            report.hallucination += scorer.abstention(transcript)

        # E13: compare with regression baseline, record quality fluctuation
        report.delta_vs(report.regression_baseline)

    # —— close: assert SLO, output pass/fail report ——
    return report.assert_slo(SLO)


# scorer internal dispatch example (dimension → metric)
def scorer(npc_output, expected, dims):
    out = {}
    if F1 in dims:   out[F1] = role_consistency_judge(npc_output, expected)   # role consistency
    if F2 in dims:   out[F2] = memory_qa_f1(npc_output, expected)            # long-term memory
    if F3 in dims:   out[F3] = believability_survey(npc_output, expected)    # believability (sample subset)
    if F4 in dims:   out[F4] = abstention_rate(npc_output, expected)         # anti-hallucination
    if F5 in dims:   out[F5] = task_success_rate(npc_output, expected)       # planning decision
    if F6 in dims:   out[F6] = mtbench_style_judge(npc_output, expected)     # dialogue quality
    # F7/F8, E9..E13 computed directly by harness at transcript/trace layer
    return out
```

> Key points: ① `dims` lets the same NPC runtime be reused by different scenarios, scoring only relevant dimensions, avoiding "full rerun"; ② engineering dimensions (E9–E12) auto-accumulate at `emit_trace` / instrumentation layer, not entering `scorer` subjective judgment; ③ `assert_slo` makes run red/green in CI, supporting E13 continuous regression.

#### 7.2.3 (c) Quantified SLO targets (explicit numbers)

> Below are **Macha v0.1 recommended SLO**. Engineering dimensions from Section 2 E9–E13; functional dimensions anchored to F1/F2/F4. Numbers are first-version targets under the hard constraint of "online game NPC," later revised by measured baseline.

| SLO item | Metric | Target | Dimension | Note |
|---|---|---|---|---|
| Turn latency | p95 end-to-end (first token → last token) | **< 800 ms** | E9 | Hard constraint of real-time dialogue; pure long-context strategy easier to meet, externalized memory must control retrieval time |
| Per-turn cost | token + tool-call cost | **< $0.002 / turn** | E10 | Estimated at gpt-4o-mini magnitude; externalized-memory vs. long-context economy trade-off see 5.2 |
| Throughput | single-instance processing rate | **> 15 turn/s** | E11 | Open-world multi-NPC concurrency; additionally set concurrent sessions > 50 as scaling threshold |
| Role consistency | weighted consistency (CharacterRM/CUS style) | **> 0.85** | F1 | Chinese uses SuperCLUE-Role/CharacterEval benchmark; below this = "character drift" |
| Hallucination rate | trap-question hallucination ratio (should refuse but fabricates) | **< 2%** | F4 | From 5.1 anti-hallucination stress test; above triggers alert |
| Long-term memory accuracy | LoCoMo multi-hop QA F1 | **> 0.80** | F2 | Core promise of memory module (M); LongMemEval five-dim overall > 0.75 |
| Consistency reliability | same-scenario pass^k (k=3) | **> 0.70** | E13/F1 | Borrow τ-bench pass^k idea: same task must stably pass across runs |
| Observability coverage | trace export coverage | **100%** | E12 | Every turn exports OpenInference span, debuggable locally in Phoenix |
| Regression stability | fixed-set quality fluctuation (vs. previous version) | **< 3%** | E13 | Fixed set run every PR, any dimension drop beyond threshold blocks merge |

---

### 7.3 Chinese-Market Section: Domestic Evaluation-System Depth

If Macha targets the Chinese game market, it cannot rely only on English benchmarks (LoCoMo/RoleBench/LIGHT). Domestic evaluation systems have formed their own system in **Chinese role consistency** and **engineering landability**, and explicitly cover the "game NPC" scenario.

**(1) SuperCLUE / SuperCLUE-Role (Chinese comprehensive + role-play special)**
- Affiliation: CLUEbenchmarks team (continuation of ChineseCLUE). SuperCLUE comprehensive leaderboard covers base ability / professional ability / Chinese characteristics, with role-play, Agent, long-text, safety special tracks.
- Key value: `SuperCLUE-Role` is a **Chinese-native** role-play benchmark, two core dimensions — "role base ability (dialogue ability / knowledge mastery) + role acting power (language style / behavior habit) + scenario application (emotional companionship / game NPC)". It **explicitly lists "game NPC" as one of its core application scenarios**, directly fitting Macha's positioning.
- Measurement insight (from its release report): ① Chinese models (qwen1.5-72b, ERNIE 4.0) can surpass GPT-4 in role-play; ② **unconventional-question alignment drops sharply**; ③ **multi-turn effect generally decays with turn count** — exactly the long-horizon consistency (F1) Macha must solve, usable as "decay curve" reference baseline.

**(2) CharacterEval (most systematic Chinese role-play academic benchmark)**
- Scale: 1,785 multi-turn dialogues, 23,020 examples, 77 Chinese-novel/script characters; GPT-4 extraction + human QC + Baidu Baike profile.
- Metric: 4-dimension 13 (paper also states 16) metrics; paired **CharacterRM** role-play reward model, correlation with humans significantly exceeds GPT-4.
- Reusability for Macha: CharacterRM can directly serve as Macha F1 Chinese auto-scorer (replacing or calibrating LLM-judge), avoiding English-judge bias on Chinese characters.

**(3) OpenCompass (Simian) and FlagEval (Tianping) — engineering base**
- OpenCompass (Shanghai AI Lab): open-source evaluation system, with CompassKit/CompassHub/CompassRank, integrates many open and closed API, examines language models on language/knowledge/reasoning/math/code/**agent**. Macha can use it for "Chinese model selection + continuous regression".
- FlagEval (Beijing Academy of AI): "capability-task-metric" three-dimension framework, nearly 30 datasets, over 100K questions, Chinese-English subjective/objective; H2 2024 extended tool-call/advanced-programming/financial-quant, and launched "LLM arena" (blind-test battle). Its "dynamic evaluation + multi-task" direction (2025 plan) aligns with Macha E13 regression philosophy.
- Both are **open-source, vendor-independent**, fitting Macha's "debuggable, not locked-in" engineering philosophy (see 5.3).

**(4) Chinese NPC landing suggestion (supplements original Section 6 gap)**
- On top of RoleBench (already has 5 Chinese characters) + LongBench (has Chinese), **use SuperCLUE-Role game-NPC subset + CharacterEval as Chinese main evaluation**;
- When building self-owned Chinese persona and dialogue-memory sets, reuse CharacterEval's "character profile + multi-turn dialogue + human QC" pipeline;
- Player subjective evaluation (F3/F7) combines SuperCLUE Langya-list-style **blind-test battle** and TrueSkill pairing (see Section 4 sources), forming "objective metric + subjective battle" dual track.

---

### 7.4 Quantification and Landing: Dataset-Scale Numbers + v0.1 Priority-Access List

#### 7.4.1 Each Benchmark Dataset Scale Numbers (summary)

| Benchmark | Scale number (quantifiable) | Year / conference | License / access |
|---|---|---|---|
| τ-bench | 165 tasks (115 retail + 50 airline) | 2024 / ICLR 2025 | MIT; GitHub sierra-research/tau-bench |
| OSWorld | 369 tasks + 43 Windows tasks | NeurIPS 2024 | Project os-world.github.io |
| GAIA | 466 questions (166 validation + 300 test) | 2023 / ICLR 2024 | HF leaderboard (test answers hidden) |
| MemBench | 500 user profiles; 51k participatory + 8.5k observational sessions; two tiers 10k/100k token | ACL 2025 | arXiv:2506.21605 |
| LongBench v2 | 503 multiple-choice; context 8k–2M words; 6 major 20 sub-tasks | ACL 2025 | Project longbench2.github.io |
| LongBench | 21 datasets, 6 major classes (incl. Chinese) | 2023 | GitHub THUDM/LongBench |
| RULER | Synthetic controllable (length/difficulty adjustable) | COLM 2024 | GitHub NVIDIA/RULER |
| LoCoMo | Longest 35 sessions / ≈300 turns / 9K token; locomo10 ≈ 1540 QA | ACL 2024 | GitHub snap-research/LoCoMo |
| LongMemEval | 500 Q; S≈115K / M≈1.5M token | ICLR 2025 | Primary direct link pending verification |
| MemoryArena | Avg 6.9 interdependent subtasks / task; ~57 action steps; trajectory >40K token | 2026-02 | arXiv:2602.16313 |
| SuperCLUE-Role | Chinese role-play multi-task (incl. game-NPC sub-leaderboard) | 2024 | GitHub CLUEbenchmark/SuperCLUE-Role |
| CharacterEval | 1,785 dialogues / 23,020 examples / 77 characters / 13 metrics 4 dims | ACL 2024 | GitHub morecry/CharacterEval |
| FRAMES | 824 questions; cross 2–15 wiki; 5 reasoning classes | NAACL 2025 | HF google/frames-benchmark (Apache-2.0) |
| RoleBench | 168,093 samples | ACL 2024 | With paper repo |
| PersonaChat | Persona dialogue set (CC BY 4.0, attribution required) | 2018 | HuggingFace persona-chat |
| LIGHT | 663 locations / 3462 objects / 1755 characters | 2019 | ParlAI LIGHT |

#### 7.4.2 Macha v0.1 Priority-Access List and Pass Thresholds

**Tier 1 — Must connect (prove "standard skeleton" core promise: remembers, speaks in-character, doesn't ramble)**

| Benchmark | Dimension | Pass threshold (v0.1) |
|---|---|---|
| LoCoMo (locomo10) | F2/F4 | Multi-hop QA F1 > 0.80; adversarial / abstention sub-item hallucination rate < 5% |
| LongMemEval (S tier) | F2/F4 | Five-dim overall > 0.75; knowledge-update + abstention sub-item > 0.70 |
| SuperCLUE-Role (game-NPC subset) | F1/F3 (Chinese) | Role-consistency score > 0.80 |
| CharacterEval (Chinese) | F1 (Chinese) | Four-dim weighted > 0.78 (or per CharacterRM correlation) |
| Self-built anti-hallucination stress test (5.1) | F4 | Trap-question hallucination rate < 2% (align SLO) |

**Tier 2 — Must connect (engineering SLO, decides whether it can launch)**

| Dimension | Threshold |
|---|---|
| E9 Latency | p95 < 800 ms |
| E10 Cost | < $0.002 / turn |
| E11 Throughput | > 15 turn/s (single instance) / > 50 concurrent sessions |
| E12 Observability | Trace coverage 100% (OpenInference) |
| E13 Regression | Fixed set every PR, quality fluctuation < 3%; pass^3 > 0.70 |

**Tier 3 — Extension (v0.2+, capability breadth and game grounded)**

| Benchmark | Dimension | Note threshold |
|---|---|---|
| AgentBench / τ-bench | F5 | Task-success aligns chosen baseline; τ-bench focuses pass^k consistency |
| OSWorld / WebArena | F5/F6 | Execution-scored; first run a subset (e.g., 50 tasks) |
| MemBench | F2 (fine-grained) | Reflection memory > 0.70 at 100k token |
| LongBench v2 / RULER | F8 | Long-context deep-reasoning pass; decide "stuff context vs. externalized retrieval" |
| FRAMES | F4/M | Multi-step retrieval + reasoning accuracy > 0.60 |
| GRBench / GRUtopia | F3/F5/F6 | Game-world grounded NPC simulation sandbox (describe/localize/dialogue/task-allocation) |

> **Access-order suggestion**: first Tier 1 + Tier 2 (about one iteration cycle to get harness and SLO red/green running), then expand Tier 3 by resource. Each new benchmark added writes to `macha_eval_run.yaml`'s `suite`, and extends `scorer`'s dimension dispatch, keeping L1–L13 framework unchanged.

---

### 7.5 New Source Collection (in agreed six-field format)

---

[Category]Academic paper / Engineering implementation
[Title]τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains (incl. τ²-bench, τ³-bench)
[Link / file path]arXiv:2406.12045 (primary paper, pending verification); official https://taubench.com ; code https://github.com/sierra-research/tau-bench (historical) / https://github.com/deephyper/tau-bench
[One-sentence summary]First agent benchmark testing "tool-agent-user" multi-turn dynamic interaction and rule-adherence consistency, proposes pass^k reliability metric.
[Key conclusions]
1. 165 tasks (115 retail + 50 airline), scored by database final-state comparison; GPT-4o pass^1<50%, retail pass^8<25%.
2. Reveals "consistency crisis": same task across runs fluctuates hugely, pass^k better reflects deployment reliability than single-pass rate.
3. 2025 τ²-bench adds dual-control telecom domain; 2026 τ³-bench adds voice duplex, knowledge-intensive banking domain, task audit correction.
4. Domain-rule adherence fragile: removing rule doc in airline domain drops performance 22.4%.
[Reusable things]pass^k reliability metric, database-final-state-comparison evaluation, multi-turn interaction protocol — directly borrow for Macha NPC customer-service / task-oriented dialogue "consistency" quantification (E13/F1).

---

[Category]Academic paper / Engineering implementation
[Title]OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments
[Link / file path]Project https://os-world.github.io (NeurIPS 2024); OSWorld 2.0 / OSWorld-Verified 2025 upgrade; arXiv primary paper pending verification
[One-sentence summary]First multimodal agent benchmark running in real OS (Ubuntu/Windows/macOS), execution-scored, 369 real tasks.
[Key conclusions]
1. 369 real computer tasks (across 9 app classes like Chrome/LibreOffice/VS Code) + 43 Windows tasks; human baseline 72.36%, best model initial only 12.24%.
2. 2025-10 OSAgent reached 76.26% first surpassing human, via "verify-generate" loop + large-scale RL.
3. Exposes GUI grounding and operation-knowledge gaps; ~15% tasks pure terminal-completable (mixed ability).
[Reusable things]Execution-based state-check evaluation, parallel self-hostable environment — engineering exemplar for Macha "game-environment auto-scoring" (F5/F6/E12).

---

[Category]Academic paper / Industry report
[Title]GAIA: A Benchmark for General AI Assistants (incl. GAIA 2 dynamic-environment version)
[Link / file path]arXiv:2311.12983 (primary paper, pending verification); HF leaderboard https://huggingface.co/spaces/gaia-benchmark/leaderboard ; Princeton HAL comparison board
[One-sentence summary]466 multi-step tasks needing reasoning + multimodal + web browsing + tool use, unique answer auto-scorable.
[Key conclusions]
1. 466 questions (166 validation + 300 test), L1/L2/L3 three difficulties; at release GPT-4+plugin only 15%, human 92%.
2. 2025 top systems approach 65–87% (test set), early 2026 submissions >90%; Level 3 most telling.
3. Public validation set widely "memorized," should value private test-set scores more; GAIA 2 introduces dynamic environment / time constraints / A2A collaboration.
[Reusable things]Unique-answer + auto-scorable multi-step task design, difficulty grading — reference for Macha task-oriented NPC evaluation (F5/F6).

---

[Category]Academic paper
[Title]MemBench: Towards More Comprehensive Evaluation on the Memory of LLM-based Agents
[Link / file path]arXiv:2506.21605 (ACL 2025); project/data pending verification
[One-sentence summary]First agent-memory benchmark covering "fact + reflection" memory, participatory + observational dual scenario, four metrics (accuracy/recall/capacity/efficiency).
[Key conclusions]
1. Generates 500 user profiles from user-relation graph, 51k participatory factual sessions + 8.5k observational sessions, with reflection-corresponding set; two sub-datasets ~10k / 100k token.
2. At 100k token reflection memory collapses: GenerativeAgent/MemGPT from ~0.74 to 0.33–0.36; RetrievalMemory most stable (participatory 0.833, observational 0.933).
3. Complex memory mechanism read/write latency high: MemGPT read ~4.5s, MemoryBank write 8–18s, prohibitive for real-time.
[Reusable things]"Fact + reflection" memory grading, participatory/observational scenario split, capacity & efficiency metrics — finer-grained framework for Macha memory module (M/F2) evaluation.

---

[Category]Academic paper
[Title]LongBench v2: Towards Deeper Understanding and Reasoning on Realistic Long-context Multitasks
[Link / file path]arXiv:2412.15204 (ACL 2025); project https://longbench2.github.io
[One-sentence summary]503 deep-understanding-reasoning long-context multiple-choice QA, context 8k–2M words, covering 6 major 20 sub-tasks.
[Key conclusions]
1. 503 questions, 6 major classes (single/multi-doc QA, long ICL, long dialogue history, codebase, long structured data), built by ~100 highly-educated annotators.
2. Human expert 15-min limit only 53.7%; best direct answer 50.1%, o1-preview 57.7% first exceeds human by 4%.
3. Proves "long window ≠ true understanding," reasoning and inference-time compute are key.
[Reusable things]Long-dialogue-history understanding subtask, deep-reasoning evaluation caliber — Macha F8 long-context and "stuff memory vs. externalized retrieval" decision basis.

---

[Category]Academic paper / Dataset
[Title]FRAMES: Factuality, Retrieval, And reasoning MEasurement Set (unified RAG evaluation)
[Link / file path]arXiv:2409.12941 (NAACL 2025); dataset https://huggingface.co/datasets/google/frames-benchmark (Apache-2.0)
[One-sentence summary]824 multi-hop RAG QA needing cross 2–15 wiki, unified tests factuality/retrieval/reasoning.
[Key conclusions]
1. 824 questions, labeled 5 reasoning classes (numeric/table/multi-constraint/temporal/post-processing); no retrieval 0.40, multi-step retrieval 0.66, Oracle 0.73.
2. Reveals "reasoning gap": even with Oracle docs, strongest model only ~73%, RAG failure not all retrieval.
3. Iterative retrieval planning nearly doubles improvement — direct inspiration for Macha memory-retrieval design.
[Reusable things]End-to-end RAG evaluation caliber, multi-hop reasoning classification — Macha memory retrieval (M) + anti-hallucination (F4) stress-test template.

---

[Category]Academic paper / Engineering implementation
[Title]GRUtopia: Dreamland of Embodied Agents (incl. GRResidents NPC system and GRBench)
[Link / file path]arXiv:2407.10943 (primary paper, pending verification); code https://github.com/openrobotlab/grutopia
[One-sentence summary]Shanghai AI Lab's embodied-town simulation, with LLM-driven NPC (GRResidents) and three-tier embodied evaluation GRBench.
[Key conclusions]
1. GRResidents NPC can infer object spatial relations, participate in dynamic dialogue and task allocation; object description/localization accuracy decent via human-machine cross-validation.
2. GRBench three tiers increasing: goal-localization navigation, social-localization navigation, localization-operation; LLM backend overall beats random policy.
3. Qwen-VL beats GPT-4o on dialogue — multimodal NPC potential.
[Reusable things]"NPC describe/localize/dialogue/task-allocation" four-ability evaluation, embodied simulation environment — reference for Macha game-world grounded NPC (F3/F5/F6) simulation sandbox.

---

[Category]Industry report / Dataset
[Title]SuperCLUE-Role: Chinese Role-Play Evaluation Benchmark (incl. game-NPC scenario)
[Link / file path]Project https://github.com/CLUEbenchmark/SuperCLUE-Role ; leaderboard www.CLUEbenchmarks.com/superclue_role.html
[One-sentence summary]Chinese-native role-play benchmark, covering "role base ability (dialogue/knowledge) + role acting power (language style/behavior habit) + scenario application (emotional companionship/game NPC)".
[Key conclusions]
1. Two core dimensions, fine-grained multi-criteria scoring; explicitly lists "game NPC" as one of core application scenarios.
2. Chinese models (qwen1.5-72b, ERNIE 4.0) can surpass GPT-4 in role-play; but unconventional-question alignment drops sharply.
3. Multi-turn effect generally decays with turn count — hits Macha long-horizon consistency (F1) pain point, usable as "decay curve" reference baseline.
[Reusable things]Chinese role-play four-dimension scoring system, game-NPC application sub-leaderboard — Macha F1/F3 Chinese landing benchmark.

---

[Category]Academic paper / Dataset
[Title]CharacterEval: A Chinese Benchmark for Role-Playing Conversational Agent Evaluation
[Link / file path]arXiv:2401.01275 (ACL 2024); code/data https://github.com/morecry/CharacterEval
[One-sentence summary]Chinese role-play conversational-agent benchmark, 1785 multi-turn dialogues, 23020 examples, 77 novel/script characters, 13 metrics 4 dimensions, with CharacterRM reward model.
[Key conclusions]
1. 1,785 multi-turn dialogues, 23,020 examples, 77 Chinese characters (novels/scripts), GPT-4 extraction + human QC + Baidu Baike profile.
2. 4 dimensions 13 (paper also states 16) metrics; CharacterRM correlation with humans significantly exceeds GPT-4.
3. Experiment shows Chinese LLM beats GPT-4 in Chinese role-play.
[Reusable things]Chinese character profile + reward model CharacterRM, four-dimension metric — direct tool for Macha Chinese role-consistency (F1) auto-scorer.

---

[Category]Academic paper / Competition
[Title]Commonsense Persona-Grounded Dialogue Challenge (CPDC) 2025 (game NPC dialogue)
[Link / file path]Competition homepage (pending verification); participation-report compilation https://www.chatpaper.ai (specific track page pending verification)
[One-sentence summary]Game-NPC "commonsense persona-grounded dialogue" challenge, three tracks: task-oriented / context-aware / fused.
[Key conclusions]
1. Evaluates agent trade-off between "functional task execution" and "persona-consistent dialogue" (Deflanderization: suppress over-role-play to preserve task fidelity).
2. Top solutions combine lightweight prompting (API track) and Qwen3-14B SFT+LoRA (GPU track).
3. Reveals real game-NPC contradiction: character immersion vs. task completion needs explicit balancing.
[Reusable things]"Task fidelity vs. character immersion" dual-objective evaluation framework — ready paradigm for Macha F1/F5 trade-off.

---

[Category]Engineering implementation / Industry tool
[Title]OpenCompass (Simian) and FlagEval (Tianping) Chinese large-model evaluation systems
[Link / file path]OpenCompass https://opencompass.org.cn ; FlagEval platform (Beijing Academy of AI, official site pending verification); report https://www.stdaily.com/web/gdxw/2024-12/19/content_276198.html
[One-sentence summary]Two domestic open-source evaluation systems: OpenCompass covers language/knowledge/reasoning/math/code/agent; FlagEval uses "capability-task-metric" three-dimension framework, nearly 30 datasets over 100K questions.
[Key conclusions]
1. OpenCompass has CompassKit/CompassHub/CompassRank, integrates many open and closed API, large industry influence.
2. FlagEval H2 2024 extended tool-call/advanced-programming/financial-quant, launched LLM arena (blind-test battle).
3. Both support Chinese subjective/objective questions, base for Macha Chinese model selection and continuous regression, and both open-source, vendor-independent.
[Reusable things]Open-source evaluation toolchain and leaderboard method, Agent evaluation dimensions — ready platform for Macha Chinese model access and regression testing (E13).
