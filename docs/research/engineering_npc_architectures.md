# Functional Boundaries and Pain-Point List of Existing NPC Tech Stacks

> Category: Engineering implementation (Layer 2 of the Macha six-layer framework)
> Research goal: Map out what the game industry's existing NPC / game AI architectures "can do, cannot do, and where they break," to provide factual evidence for Macha's decision on **replace vs. compatibilize** the existing standards (Behavior Tree / GOAP / HTN / Utility AI / FSM).
> Related docs: `direction.md` (Macha = Perception—Memory—Reasoning—Action), `positioning.md` (cognitive model and pluggable architecture).

---

## 0. One-Line Conclusion (for downstream decisions)

All existing industry standards are **"execution-layer / control-layer"** technologies: they excel at turning "an already-decided intent" into "a runnable sequence of actions," yet they **barely address** the three things Macha cares about—

1. **Long-term memory and character consistency** (NPC remembers the player across sessions, persona does not drift);
2. **Semantic-level perception and reflection** (extracting structured observations from game events, abstracting them into high-level cognition);
3. **Generative / LLM-driven emergent behavior** (open dialogue, autonomous planning, sociality).

Therefore the correct posture for Macha is: **build the standard skeleton on the cognitive/memory/planning "upper layer," and wrap (adapt/compatibilize) Behavior Trees/GOAP/HTN/Utility/FSM and the AI systems of major engines as "lower-layer executors"; for the fragmented, ad-hoc "memory/persona" patches that exist in current open-source frameworks, replace them with a unified standard.** The following sections argue this point by point.

---

## 1. Classic Game AI Architectures (Industry Standards)

### 1.1 FSM (Finite State Machine)
- **Problem solved**: Models mutually exclusive behaviors (patrol / chase / attack / flee) with "states + transition conditions," the oldest and most debuggable baseline in game AI.
- **Typical data model**: `state set S` + `transition table T: (state, event) → state` + `Enter/Update/Exit` hooks per state.
- **Common implementations**: Self-built in almost every engine; the underlying idea of Unity Animator state machines, Unreal StateTree, and RimWorld's `ThinkNode`/`LordJob` state machines (see §4.3).
- **Functional boundaries (especially for LLM generative NPCs)**:
  - Can: clear, deterministic, QA-friendly discrete behavior; suited for "identity-fixed" enemies.
  - Cannot: state-number explosion (FSMs already exceeded 80 states in the Halo era, see Isla's discussion in §3); cannot express "on-demand composition of actions"; **has no memory/persona/semantic reasoning at all**, and is useless for LLM dialogue-type NPCs.
- **Pain-point list**:
  - State explosion—behavior grows complex, transition edges grow combinatorially, hard to maintain (discussed in both peerdh/Unity Chinese community).
  - High coupling—logic is bound to state; changing one place ripples through everything.
  - No emergence—cannot produce behaviors not explicitly choreographed by designers, inherently conflicting with the "generative NPC" goal.

### 1.2 Behavior Tree (BT)
- **Problem solved**: As an upgrade to FSM, uses "composite nodes (Sequence/Selector/Parallel) + decorator nodes + leaf nodes + Blackboard" to express reusable, readable, visually debuggable hierarchical decisions, solving FSM's state explosion and coupling problems.
- **Typical data model**: Tree (root → composite nodes → condition/action leaves); `Blackboard` as a one (blackboard)-to-many (trees) shared data area; Tick evaluates top-down every frame.
- **Common implementations**:
  - **Unreal Engine** built-in Behavior Tree + Blackboard + Service/Decorator (industry de facto standard);
  - **Godot** third-party Beehave plugin (`github.com/bitbrain/beehave`, with runtime debug view);
  - **Unity** original Behavior Designer / new `com.unity.behavior` visual behavior tree package;
  - **Rival Theory RAIN** (see §3.5), **Wise Feline** (Unreal Utility BT), etc.
- **Functional boundaries (especially for LLM generative NPCs)**:
  - Can: strongly controllable, QA-able, designer-friendly; suited for tactical behavior of "hero NPC / enemies"; can be combined with GOAP/HTN (GOAP does planning at a leaf node).
  - Cannot: BT is essentially **passive evaluation**—Isla (Halo 2, BT pioneer) noted in *Game AI Uncovered* that "traditional behavior trees are not reactive," requiring Reactive BT patches; BT **does not store world state, has no memory, produces no intent**—it merely "selects actions by tree structure." For LLM-driven open dialogue and social behavior, BT can only serve as an "execution shell," providing no cognition.
- **Pain-point list**:
  - Non-reactive (needs extra mechanisms to handle sudden events, see Game AI Uncovered excerpt).
  - Complex trees are hard to debug—excessive depth, parallel node semantics are error-prone (Beehave guide specifically lists safety rules like "don't block in `_tick`", "don't recompute path every frame").
  - Hard to express "multi-NPC collaboration"—blackboard is 1:N, but cross-NPC intent coordination still requires hand-writing.
  - **Powerless for generative NPCs**: BT cannot make an NPC "remember the player saved it three days ago" or "autonomously decide what to do next."

### 1.3 GOAP (Goal-Oriented Action Planning)
- **Problem solved**: Hands "intent (Goal)" and "action library (Action, with precondition/effect/cost)" to an **A\* planner**, which searches in real time for the shortest action sequence from current world state to goal state. F.E.A.R. (2005, Jeff Orkin) is its foundational work—the character FSM has only 3 states (Goto / Animate / UseSmartObject), all tactical intelligence comes from the planner.
- **Typical data model**: `WorldState` (boolean/enum vector, 30–50 facts) + `Action{precondition, effect, cost}` + `Goal{goal state}` + A\* search in state space.
- **Common implementations**: F.E.A.R. original implementation; *Shadow of Mordor*, *Tomb Raider*, *Just Cause 2*, *Horizon: Zero Dawn* heuristic HTN (Orkin lineage); community implementations (theneuralbase tutorial, Godot GOAP demo).
- **Functional boundaries (especially for LLM generative NPCs)**:
  - Can: produces **emergent tactics** (flanking, suppressive fire are decided "by the AI itself," not scripted); controllable action space (5–15 actions optimal); tuning cost to tune difficulty/persona.
  - Cannot: **action set must be hand-authored by designers**, no "feed a neural net and it gets smart"; cannot handle spontaneous multi-NPC collaboration (requires explicit multi-agent actions, action space explodes); **no long-term memory, no semantic understanding, no dialogue**.
- **Pain-point list** (industry consensus, see beatai / theneuralbase / bentebent):
  - **Controllability crisis**: free search finds solutions designers didn't anticipate; QA must verify behavior in combinatorial explosion space—this is the root reason GOAP failed to "unify the world" (production reality, not technical limitation).
  - Performance: on current consoles, concurrent planners >30/frame incur unacceptable latency; worst-case complexity O((nm)^d).
  - Poor predictability: adding one action, overall behavior becomes hard to estimate.
  - Hard to debug: plan graph visualization is costly.
  - **No direct value for LLM NPCs**: it optimizes "action sequence search," not "memory/persona/dialogue."

### 1.4 HTN (Hierarchical Task Network)
- **Problem solved**: Uses "composite task → method → atomic task" **recursive decomposition** for planning, expanding tasks into atomic action sequences at planning time ("look-ahead simulation"). Compared to GOAP's search, HTN **uses domain knowledge (methods) to guide the search direction**, giving a smaller, more controllable, more predictable search space.
- **Typical data model**: `WorldState` (same as GOAP, uses a world-state copy for "mental simulation") + `composite task / method / atomic task` three layers + methods with preconditions; plan-phase decomposition, execution-phase running of atomic tasks and write-back of world state.
- **Common implementations**: *Horizon: Zero Dawn*, *Transformers: Fall of Cybertron*; classic SHOP/SHOP2 planners (Lisp/Java/Python open source); *Game AI Pro* (ed. Steve Rabin) HTN chapter; adversarial HTN (AHTN) in RTS.
- **Functional boundaries (especially for LLM generative NPCs)**:
  - Can: more controllable, more predictable, deeper planning than GOAP (plans a composite task with multiple actions at once, "somewhat foreseeing the future"); suited for complex enemy AI and RTS.
  - Cannot: **domain knowledge (methods) still requires manual authoring**; equally powerless for multi-NPC collaboration, long-term memory, dialogue, persona consistency; like GOAP, only solves "action planning," not "cognition/memory."
- **Pain-point list**:
  - Still requires heavy manual domain modeling (task/method trees).
  - Fails-and-abandons (only AHTN variants do failure recovery), limited robustness to dynamic environments.
  - Complete-information assumption (AHTN) conflicts with the "fog of war" partially-observable reality of games.
  - **Orthogonal to LLM generative NPCs**: it is a "deterministic planner," not a "cognitive kernel."

### 1.5 Utility AI
- **Problem solved**: Maps "multi-input, multi-consideration complex decisions" to a **normalized utility space**, scoring each candidate action 0–1, taking the highest (or utility-weighted random). The Sims, Guild Wars 2, The Sims 4 are representatives.
- **Typical data model**: `Agent motives/needs` (numeric, decaying over time) + `Action with several Considerations` + each Consideration normalized to 0–1 via a **response curve** + all Considerations **multiplied** for the action's total score.
- **Common implementations**: Dave Mark's *Behavioral Mathematics for Game AI* and GDC talks; Mike Lewis's "Infinite Axis Utility System" in *Game AI Pro 3* (Guild Wars 2); Wise Feline (Unreal Utility AI commercial plugin); The Sims need system (see §4.4).
- **Functional boundaries (especially for LLM generative NPCs)**:
  - Can: naturally suited for "continuously weighted, knowledge-sharing" decisions (e.g., reef creatures, NPC motive-driven); data-driven, designer-friendly; can produce "soft emergence" (different needs combine into different behaviors); **the industry technique closest to "need/motive-driven persona."**
  - Cannot: Considerations and curves **still require hand-design**; essentially "score and select action," **involving no language, memory, reflection, or long-term goals**; for "LLM open dialogue" it can only do "speech-intent triggering," not the dialogue itself.
- **Pain-point list**:
  - Designing Considerations / tuning curves is a craft, with a high experience threshold (Lewis devotes a chapter to "how to choose effective Considerations").
  - Interpretability of scores drops in complex systems.
  - No memory/semantic layer, cannot support the core demands of "generative NPCs."

### 1.6 Classic Architecture Comparison Matrix

| Dimension | FSM | Behavior Tree BT | GOAP | HTN | Utility AI |
|---|---|---|---|---|---|
| Core idea | State+transition | Tree-selective execution | A\* search action sequence | Recursive task decomposition | Utility-score action selection |
| Controllability | High (but explodes) | **Highest** | Low (unpredictable emergence) | Medium-high | Medium (curves hard to tune) |
| Emergence | None | Low | **High** | Medium-high | Medium (soft emergence) |
| QA / debug | Medium | **High** | Low | Medium | Medium |
| Multi-NPC collaboration | Hard | Hard | Hard (space explosion) | Medium | Medium |
| Performance/concurrency | Excellent | Good | Poor (>30/frame risky) | Medium | Good |
| Long-term memory | ❌ | ❌ | ❌ | ❌ | ❌ (numeric decay only) |
| Semantic/dialogue | ❌ | ❌ | ❌ | ❌ | ❌ |
| Persona consistency | ❌ | ❌ | ❌ | ❌ | Partial (by numbers) |
| vs. LLM generative NPC | Irrelevant | **Execution shell only** | Irrelevant | Irrelevant | **Motive layer possible** |
| Typical reps | Early enemies | Halo/UE/most 3A | F.E.A.R. | Horizon | The Sims/GW2 |

**Key read**: All five techniques are an "**intent-to-action**" execution/control layer; they differ only in "who decides the action sequence" (hardcode / tree / search / decompose / score). **None natively has the memory, reflection, semantic perception, or cross-session consistency that Macha emphasizes.**

---

## 2. Built-in AI Capabilities of Game Engines

### 2.1 Unreal Engine 5 (most complete in industry)
- **Component family**: Behavior Tree + Blackboard, StateTree (hybrid of BT selector + FSM state/transition), Navigation System (NavMesh), Environment Query System (EQS, feeds environment data to decisions), AI Perception (sight/hearing/touch), MassEntity (data-oriented large-scale crowds, Mass StateTree / Mass Crowd / Mass Signals), **Smart Objects** (interactable activity slots in a level, discovered and used by Agents via a reservation system), Neural Network Engine (NN inference).
- **Functional boundaries**: Provides a **full-stack execution layer** from "perception → decision → navigation → crowds → interaction"; Smart Objects let background NPCs "dynamically discover and sit down/lean on wall" without per-object hardcoding; MassEntity can simulate tens of thousands of Agents.
- **Pain-point list**:
  - Full stack but **zero cognition**: no memory/persona/semantic layer, NPCs remain "brainless executors."
  - System is huge and steep to learn; MassEntity is ECS-based, different mental model from object-oriented BP/C++.
  - Smart Objects "contain no execution logic," only provide data; integration cost remains on the developer side.
  - Bridging to LLM NPCs requires self-build (official NN Engine leans toward model inference, provides no dialogue cognition).

### 2.2 Unity
- **Component family**:
  - **ML-Agents** (`com.unity.ml-agents`): Turns a Unity scene into an RL/imitation-learning environment; core is `Agent` (CollectObservations / OnActionReceived / Reward), `Behavior Parameters`, `Sensor`, `Actuator`, `Policy`; training on Python side, inference via **Sentis** engine on-device.
  - **Unity Behavior** (`com.unity.behavior`): New visual behavior tree package.
  - NavMesh / traditional BT plugins (Behavior Designer, etc.).
- **Functional boundaries**: ML-Agents suits "learned locomotion/tactical strategy" (e.g., positioning, controlling NPC behavior, automated testing), **not** a dialogue/cognition framework; it explicitly "includes no training algorithms, only environment wrapping and model embedding."
- **Pain-point list**:
  - ML-Agents training supports Mono backend only, not IL2CPP; inference limited by on-device CPU/GPU; only accepts models from its own trainer.
  - Weak relationship to LLM generative NPCs—it solves "reinforcement-learning control," not "memory/persona/dialogue."
  - Unity Behavior is relatively young, ecosystem less mature than Unreal BT.

### 2.3 Godot 4
- **Component family**: NavigationServer (2D/3D independent, 4.5+ supports background async baking), NavigationAgent, steering behaviors, third-party **Beehave** behavior tree (with debug view), state-machine pattern. Godot itself **has no official behavior tree/Utility module**, relying on community and user self-implementation.
- **Functional boundaries**: Lightweight, open source, suited for indie games and 2D/3D navigation; Beehave greatly lowers the BT development threshold.
- **Pain-point list**:
  - **No built-in advanced AI**: perception, decision, memory all need self-build or community plugin assembly.
  - Large projects still depend on third parties (Beehave, etc.), low standardization.
  - No built-in support for LLM NPCs.

### 2.4 Engine AI Comparison Matrix

| Engine | Decision system | Perception | Navigation | Crowd scale | Cognition/memory | LLM NPC support |
|---|---|---|---|---|---|---|
| Unreal 5 | BT/StateTree/HTN via Mass | AI Perception/EQS | NavMesh strong | MassEntity 10k+ | ❌ | Self-build needed |
| Unity | ML-Agents/Behavior/BT | Self-build | NavMesh | Medium | ❌ | Weak (RL-oriented) |
| Godot 4 | Beehave(BT)/FSM(self) | Self-build | NavigationServer | Medium | ❌ | ❌ |

**Read**: All three engines only cover "perception (raw signal) → decision (execution layer) → action," **cognition/memory is a vacuum**. Macha should treat "engine AI systems" as **adaptable execution backends**.

---

## 3. Open-Source / Commercial NPC Frameworks and Generative AI Platforms

### 3.1 NVIDIA ACE (autonomous game characters)
- **Architecture**: A suite of digital-human microservices (NIM), end-to-end perception—cognition—action—rendering:
  - **Perception**: `NeMoAudio-4B-Instruct` (soundscape understanding), `Parakeet` (multilingual ASR), `NeMoVision-4B` (spatial vision), Game State (turns game state into text for SLM).
  - **Cognition**: `Mistral-Nemo-Minitron` series SLM (2B/4B/8B, 128k, strong instruction-following, plans at human decision frequency 8–13 times/sec).
  - **Action**: action selection, TTS (ElevenLabs/Cartesia), Strategic Planning (connects to cloud LLM), **Reflection (self-reflection correction)**.
  - **Memory**: Embedding (E5-Large) for memory recall.
  - **Rendering**: Audio2Face, AnimGraph, Omniverse RTX.
  - **NVIGI SDK**: GPU-optimized, plugin-style inference manager, supports on-device/cloud, compute-in-graphics technology.
- **Functional boundaries**: Currently the **industrial solution** closest to a complete "perception—memory—cognition—action" loop, and explicitly treats "Memory/Reflection/Strategic Planning" as first-class citizens—highly isomorphic to Macha's `direction.md` framework.
- **Pain-point list**:
  - **Strongly bound to NVIDIA RTX / cloud**, on-device real-time needs high-end GPU, extremely high deployment threshold and cost.
  - Cloud solution has latency and cost; multi-component (NeMo/Riva/A2F) integration complexity is high.
  - Closed-source commercial stack, **cannot serve as a "standard skeleton"**—it is a product, not a standard; Macha can borrow its "perception-cognition-action-memory" layering, but should build an **open, replaceable, engine-agnostic** equivalent.
  - Character design/memory/guardrails still need careful manual work.

### 3.2 Inworld AI (character brain)
- **Architecture**: Character Engine (Character Brain) + Contextual Mesh (custom knowledge/world setting/guardrails) + TTS; provides Unity / Unreal / Web / Node SDK and REST API.
- **Runtime data**: `CharacterProfile`, `EmotionState`, `Goals`, `KnowledgeFilter`, `RelationState` (trust/familiarity/respect), `Memory Retrieval` node, multi-character dialogue management.
- **Functional boundaries**: Makes "persona/emotion/goal/relationship/memory/knowledge filtering" structured components—**currently the commercial product most resembling the "cognitive middleware" Macha wants to build**; no-code creation, strong engine integration.
- **Pain-point list**:
  - **Closed SaaS**, advanced features expensive, requires technical knowledge; large-scale deployment compute cost high.
  - Memory/persona are **its private implementation**; developers cannot pull the "brain" out to connect their own engine or swap models—conflicts with Macha's "standard skeleton, pluggable" philosophy.
  - Cannot localize/privatize deep customization (though it claims local TTS options, the core is in the cloud).

### 3.3 Convai
- **Architecture**: End-to-end voice-dialogue pipeline (ASR + NLU + generation + TTS), Unity/Unreal SDK; **Character Crafting REST API** (create/list/update characters, knowledge base, narrative, actions); supports **Bring Your Own LLM** (OpenAI-compatible endpoint); World-aware (perceives objects/locations/player state), Actions map to animation/navigation/object interaction, Memory + Personality.
- **Functional boundaries**: Strong in "voice-to-voice NPC" and "world-perception action mapping," and opens "bring-your-own-model" and REST interfaces—**one of the platforms with the best interop posture**.
- **Pain-point list**:
  - Depends on network and cloud, latency fluctuates on constrained devices.
  - Wiring of action/navigation/perception data still requires integration work.
  - Also a commercial SaaS, brain not portable; "memory" is its implementation, not a replaceable standard.

### 3.4 Altera (Project Sid, large behavior model)
- **Architecture**: Puts "autonomous Agents equipped with LLM brain modules" into Minecraft, up to 1000 concurrent, spontaneously forming emergent social behaviors like professions, economy, culture, religion, tax-reform voting; brain composed of multiple dedicated modules (reaction/speech/planning), inspired by Stanford Smallville (Generative Agents).
- **Functional boundaries**: Proves "**multi-Agent + LLM + lightweight rules**" can produce astonishing emergent social behavior, a benchmark on the research side for "generative NPC civilization."
- **Pain-point list**:
  - Is a **research demo**, not a reusable framework; architecture details (module interfaces, memory format) not open-sourced as a standard.
  - Strongly depends on Minecraft + LLM, extremely high cost and latency, not directly usable in products.
  - Less focus on "single believable NPC's persona consistency/debuggability" than on "group emergence."

### 3.5 Rival Theory RAIN (Legacy, as a counter-example)
- **Architecture**: Old popular free Unity AI toolkit, integrating Pathfinding + Behavior Tree + Goal-Oriented Behaviors + Sensors + one-click config.
- **Status/boundaries**: Community has stalled (official forum last active around 2022, noting "Asset Store version is outdated"); proves "**an unmaintained AI framework gets abandoned by the ecosystem**"—if Macha wants to be a standard, it must solve **long-term maintainability and open governance**, or repeat RAIN's fate.
- **Pain-point list**: Maintenance stopped, fragmented docs/versions, large performance overhead (community feedback reports performance pitfalls).

### 3.6 Platform Comparison Matrix

| Platform | Cognition layer | Memory | Engine integration | Open/portable | Relation to Macha |
|---|---|---|---|---|---|
| NVIDIA ACE | ✅ Full layering | ✅ Embedding | UE/Unity/self | ❌ NVIDIA-bound | Borrow architecture, don't replace |
| Inworld | ✅ Structured | ✅ | UE/Unity/Web | ❌ SaaS | Borrow, don't replace |
| Convai | ◐ Dialogue-oriented | ◐ | UE/Unity | ◐ BYO-LLM/REST | Complementary/interface-aligned |
| Altera | ✅ Multi-Agent | ◐ | Minecraft | ❌ Research | Research benchmark |
| RAIN | ❌ Execution only | ❌ | Unity | ❌ Discontinued | Counter-example |

---

## 4. Game Scripting / Modding AI and Classic Simulation Systems

### 4.1 Minecraft (Mineflayer / Project Sid)
- **Mineflayer**: Open-source JS/Python high-level Minecraft bot framework; architecture is **event-driven + plugin system**, lower layer `minecraft-protocol` parses network packets into structured world state (`blocks/entities/inventory/physics`), upper layer 30+ internal plugins + `mineflayer-pathfinder` (A\* navigation). It is essentially "**turning the game protocol into a programmable Agent interface**"—exactly the template for the "perception/action adaptation layer" Macha wants to build.
- **Project Sid** (see §3.4): LLM Agent civilization experiment.
- **Pain points**: Mineflayer only gives "action/perception primitives," **no cognition/memory**; the LLM upper layer must be built yourself (e.g., DF/MC LLM Agents all self-build knowledge layer + decision layer + execution layer).

### 4.2 Skyrim / Creation Engine (AI Packages + LLM Mods)
- **Native AI**: Each Actor has a **Package Stack** (ordered behavior stack), periodically evaluated top-down for conditions, executes on match (e.g., "go home past midnight"); Quest uses Stages/Alias/Scripts/Scenes to organize narrative; scripting language **Papyrus** (slow, limited data structures).
- **LLM Mod (Social NPCs / CiF-CK; SkyrimNet)**: Academia uses CiF (Comfort/Influence/Familiarity) social state + micro-theories to compute "social willingness" for emergent social behavior; **SkyrimNet** connects an LLM in, with Papyrus API, vectorized memory, MCP Server (44+ tools for external AI assistants), Inja prompt-template hot-reload, and IntelEngine (NPC cross-cell autonomous travel/dynamic quests), etc.—this is a real case of "**hard-wiring LLM cognition onto an old engine**."
- **Pain-point list**:
  - Papyrus performance and expressiveness bottleneck; complex social state can only be managed locally at "player location."
  - LLM Mods each reinvent the wheel (memory, world knowledge, prompt templates, MCP), **no unified standard**—exactly the fragmented status quo Macha wants to replace.
  - No official memory/reflection abstraction, all hand-built by mod authors.

### 4.3 RimWorld (Lord system + ThinkNode + LLM Mods)
- **Native AI**: Layered—`LordJob` (tactical goal, e.g., AssaultColony) builds `StateGraph` (state machine) to coordinate **the swarm**; individual behavior is indexed by `ThinkNode_Duty` (duty node, top of decision chain) via `DutyDef` to a behavior subtree; lower layer Job/Pathfinding executes. I.e., a hybrid architecture of "**state machine governs macro, Duty tree governs individual**."
- **LLM Mod (RimAI Core V4 / RWAILib / RimTalk)**: RimAI Core has explicit layering—UI / Modules (Orchestration/LLM/WorldAccess/Persistence/Eventing/Persona) / Infrastructure (DI/Scheduler/Cache/Config) / Contracts; `IOrchestrationService` does a "five-step query workflow", `IToolRegistryService` dynamically extends AI capability, `IPersonaService` separates "who" from "what it can do", `IPersistenceService` decouples saves. This is **the open-source implementation closest to Macha's module breakdown**.
- **Pain-point list**:
  - Native RimWorld AI is pure rules/FSM, **no LLM, no semantic memory**.
  - LLM Mods have different architectures (RimAI uses SOLID+async, RWAILib uses submodules, RimTalk uses GameComponent pipeline), **lack of cross-Mod standard**.
  - Thread/main-thread data safety, scheduling, caching, retry all hand-built—Macha should make these an "out-of-the-box kernel."

### 4.4 The Sims (Needs-based AI)
- **Architecture**: **Needs-based AI**—each Sim has competing motives (hunger/hygiene/energy/social/fun…, 0–100 decaying); objects in the world "advertise" interactions they can provide; AI loop = scan nearby object ads → score each ad by current needs → pick highest → push action sequence into queue to execute. The Sims 4 further uses **hierarchical planning + item-interaction mapping + LOD (Sims out of focus auto-satisfied)** to optimize support for thousands of characters.
- **Functional boundaries**: The most classic landing of Utility AI thought, **closest to "motive/need-driven persona"**; actions can "self-configure" (auto-selected by need), easy to understand and implement.
- **Pain-point list**:
  - Needs and ads **require hand-definition**; scoring/distance-decay functions need experienced tuning (Zubek's paper gives decay formula).
  - **No language/semantic/long-term narrative memory**—Sims won't "hold grudges" or "reflect," only number-driven.
  - Powerless for LLM open dialogue, can only serve as "autonomous-behavior motive layer."

### 4.5 Dwarf Fortress (Agent-based Emergent Simulation)
- **Architecture**: Each dwarf is a **deterministic state-machine Agent**, driven by 500+ interlocking needs/skills/memory/emotions/social relations/beliefs; physics and ecology (rock layers, magma, temperature, pressure) all simulated; world first generates ~1000 years of history, then player intervenes. **Complexity comes from emergent interaction of rigid rule systems**, not neural networks.
- **Functional boundaries**: One of the deepest "believable emergence" simulations in game history; researchers explicitly compare it with Stanford Generative Agents—DF produces meaning with "rigid causal rules," GA with "LLM post-hoc rationalization of behavior."
- **Pain-point list**:
  - No LLM, no natural language; "persona" is rule-emergent, not dialogue-able.
  - 700k lines of code, steep learning curve; **Macha's relation is "design-philosophy borrowing"**: rule-system emergence + can add an "AI-curated memory core" for the emotion layer (research has proposed hybrid: LLM writes narrative background, keep DF's deterministic base).
  - Hard to do AI Agent directly too (only feasible with DFHack structured interface, LLM weak at spatial reasoning).

### 4.6 Simulation/Mod System Comparison Matrix

| System | Decision paradigm | Memory/persona | Emergence | Inspiration for Macha |
|---|---|---|---|---|
| Minecraft/Mineflayer | Event-driven+plugin | ❌ (self-connect) | Medium | **Perception/action adaptation-layer template** |
| Skyrim (Package/Quest) | Package stack/Quest stack | ❌ | Low | Pain-point sample of hard-wiring LLM onto old engine |
| SkyrimNet (LLM Mod) | LLM + MCP | ◐ Vector memory | Medium | Counter-example of fragmented integration |
| RimWorld (Lord/Duty) | FSM + Duty tree | ❌ | Medium | Swarm+individual layered paradigm |
| RimAI Core (LLM Mod) | Layered Orchestration | ◐ | Medium | **Module breakdown closest to Macha** |
| The Sims | Needs-based Utility | Numeric decay | Medium-high | Industrial template of motive-driven persona |
| Dwarf Fortress | Deterministic Agent rules | Rule memory | **Extreme** | Rule emergence + memory-core hybrid |

---

## 5. Synthesis: Should Macha Replace or Wrap / Compatibilize

### 5.1 Decision Matrix

| Tech / system | Positioning | Macha posture | Reason |
|---|---|---|---|
| FSM | Execution-layer baseline | **Wrap (compatibilize)** | Lots of existing enemies/UI use FSM; Macha can translate "actions" to FSM or adapt vice versa. |
| Behavior Tree BT | Execution-layer mainstream | **Wrap (compatibilize, preferred executor)** | Industry de facto standard, controllable and QA-able; Macha's "Action module" can directly drive BT nodes. |
| GOAP | Execution-layer (planning) | **Wrap (optional executor)** | Only useful in "tactical action planning" sub-scenarios; Macha's cognition layer outputs "intent," can be handed down to GOAP planner. |
| HTN | Execution-layer (planning) | **Wrap (optional executor)** | Same as GOAP, and more controllable; suited as "deterministic landing" of Macha's planning results. |
| Utility AI | Execution-layer (motive scoring) | **Wrap + borrow** | Can serve as the landing implementation of Macha's "need/motive layer"; its Consideration-curve idea can feed the persona model. |
| Unreal AI suite | Engine execution backend | **Wrap (adapter)** | Provide BT/StateTree/Mass/SmartObjects adapters, let Macha cognition kernel drive them. |
| Unity ML-Agents/Behavior | Engine execution backend | **Wrap (adapter)** | Macha cognition layer + Unity execution layer combination. |
| Godot / Beehave | Engine execution backend | **Wrap (adapter)** | Lightweight integration. |
| NVIDIA ACE | Commercial cognition stack | **Borrow architecture + don't replace** | ACE's "perception-cognition-memory-action-reflection" layering is worth copying; but Macha builds an open equivalent, not bound to NVIDIA. |
| Inworld / Convai | Commercial character brain | **Interface align / complement** | Via OpenAI-compatible / MCP / Tool Use let Macha interoperate with them; don't lock the "brain" in SaaS. |
| Altera Project Sid | Research benchmark | **Research reference** | Multi-Agent emergence methodology learning. |
| RimAI Core / SkyrimNet-style LLM Mod | Fragmented self-build | **Replace (replace its cognition kernel)** | Their hand-built memory/persona/orchestration/scheduling is exactly the part Macha wants to standardize and reuse. |
| RAIN-style discontinued framework | Legacy | **Counter-example** | Reminder that Macha must be maintainable, open-governed. |
| The Sims Needs / DF rules | Design philosophy | **Borrow (don't replace)** | Motive-driven and rule-emergence as behavior-science reference. |

### 5.2 Core Argument (Replace vs Wrap)

**Replace (the part Macha builds as standard) — the cognitive/memory/reflection/persona "upper layer":**
- Long-term memory and retrieval (vector/graph, cf. ACE Embedding, Inworld Memory, SkyrimNet vector memory).
- Character consistency / persona model (cf. Inworld Emotion/Goals/Persona, RimAI PersonaService).
- Semantic perception abstraction (abstracting game events into structured Observation, cf. Mineflayer's world state, Macha `direction.md`'s Perception).
- Reflection and planning (cf. ACE Reflection, Generative Agents reflection, RimAI Orchestration five-step).
- **Unified interface and orchestration across Mods/frameworks** (replace the go-our-own-way "brain" implementations of RimAI/RWAILib/RimTalk/SkyrimNet).

**Wrap / compatibilize (the part Macha adapts, doesn't rebuild) — execution/control "lower layer":**
- Behavior Tree, GOAP, HTN, Utility, FSM: as the "action executors" Macha's `Action` module can hand down. Macha decides "what/why," they decide "how step by step."
- The AI systems of major engines: Unreal BT/Mass/SmartObjects, Unity ML-Agents/Behavior, Godot Beehave—accessed via **adapters**, Macha's cognition kernel hangs as the "brain" on these bodies.
- Commercial character platforms (ACE/Inworld/Convai): via **MCP / OpenAI-compatible Tool Use / REST** establish interoperability; Macha can collaborate with them as "upper cognition" or "parallel brain," rather than replacing their commercial value.

### 5.3 One-Line Positioning (for team alignment)
> **Macha = an open "cognition/memory/persona" standard kernel + an adaptation layer to Behavior Trees/GOAP/HTN/Utility/major engines/commercial platforms.** All existing industry standards sit in Macha's "lower execution layer," which Macha compatibilizes and drives; the "memory/persona kernels" of existing open-source LLM Mods are the fragmented status quo Macha wants to standardize and replace.

---

## 6. Implications for Macha Engineering (Landing Suggestions)

1. **Clear layering**: Cognition kernel (Memory / Perception / Reasoning / Reflection / Persona) and execution layer (Action Adapter → BT/GOAP/HTN/Utility/engine) strictly decoupled, referencing RimAI Core's Modules/Contracts layering and direction.md's "Perception—Memory—Reasoning—Action".
2. **Standard interfaces**: Define four minimal interfaces `Agent` / `MemoryStore` / `PerceptionSource` / `ActionSink`; ActionSink provides BT/HTN/GOAP/engine multi-backend implementations (cf. ACE's NVIGI plugin-style, Convai's REST/BYO-LLM).
3. **Interop first**: Expose **MCP Server + OpenAI-compatible Tool Use** externally (SkyrimNet already proved MCP works in games), so Macha can both consume external tools and be called by external AIs.
4. **Observable/debuggable**: BT won its victory via visual debugging; Macha must have built-in observability panels for "memory flow / decision chain / persona state," or repeat GOAP's "unpredictable, hard-to-QA" mistake.
5. **Maintainable governance**: Learn from RAIN's discontinuation, adopt open repo + clear version/compat strategy, avoid being held hostage by a single vendor or maintainer.
6. **Borrow not bind**: Copy ACE's layering, Inworld's structured persona components, The Sims' motive-driving, DF's rule-emergence, but all made into **engine-agnostic, model-agnostic, privatize-deployable** open standards.

---

## 7. Source Collection

> Format follows `information_needs.md` conventions. Secondary/community sources without a clearly public URL are explicitly marked "no stable link found," not fabricated.

---

[Category]Engineering implementation (classic architecture)
[Title]Game AI Uncovered, Vol. 1 — Behavior Trees (incl. Isla on Halo 2 / BT origins and Reactive BT)
[Link]https://gamedevelopment.com/programming/book-excerpt-game-ai-uncovered-volume-one
[One-line summary]BT was invented by Damian Isla in Halo 2 to improve FSM, now industry default; traditional BT is not reactive, needs Reactive BT patch.
[Key conclusions]
1. BT has become the cross-industry AI behavior first choice; Epic's Unreal has built-in BT.
2. Traditional BT works with Blackboard (1:N shared data); composite nodes (Sequence/Selector/Parallel) + decorator + leaf.
3. Traditional BT is non-reactive; sudden events need extra mechanism.
4. For generative NPCs, BT can only be "execution shell," no memory/cognition.
[Reusable]BT node taxonomy, blackboard data-flow diagram, Reactive BT idea.

[Category]Engineering implementation (classic architecture)
[Title]Three States and a Plan: The A.I. of F.E.A.R. (Jeff Orkin, GOAP foundational paper)
[Link]https://www.gamedevs.org/uploads/three-states-plan-ai-of-fear.pdf
[One-line summary]F.E.A.R. uses GOAP to compress enemy FSM to 3 states, all tactical intelligence from A\* planner; the most authoritative first-hand GOAP literature.
[Key conclusions]
1. GOAP is essentially STRIPS planning real-timed in games, A\* searches "world-state space".
2. Motivation: 1 AI programmer managing many characters, combinatorial behavior unmanageable.
3. "FSM tells you what to do every moment; planning system tells you goal and actions, lets AI decide sequence itself."
4. Due to controllability/QA dilemma, GOAP failed to become dominant paradigm, BT won.
[Reusable]GOAP three elements (WorldState/Action/Goal) data model, planner architecture.

[Category]Engineering implementation (classic architecture)
[Title]GOAP intro and industry reflection (theneuralbase / beatai)
[Link]https://theneuralbase.com/ai-for-gaming/learn/beginner/goal-oriented-action-planning-goap ;https://beatai.org/ai-insights/game-ai-is-not-about-intelligence
[One-line summary]GOAP suits 10–50 NPC small action spaces, but "production reality (controllability)" not technical limits kept it from spreading; game AI constrained by performance/QA/predictability.
[Key conclusions]
1. GOAP strong single-NPC, multi-NPC collaboration needs explicit multi-agent actions (explodes).
2. Planning latency unacceptable at >30 concurrency/frame.
3. Behavior Tree popular because "designer-friendly + controllable + visually debuggable".
4. Game AI must satisfy a bunch of engineering constraints unrelated to "intelligence".
[Reusable]GOAP applicability boundary list, cost-tuning workflow suggestions.

[Category]Engineering implementation (classic architecture)
[Title]Hierarchical Task Network (HTN) theory and game applications (Game AI Pro / community translation)
[Link]https://www.gameaipro.com/ (HTN chapter in Steve Rabin ed. *Game AI Pro*; community translation: UWA article "Hierarchical Task Network HTN")
[One-line summary]HTN uses "composite task → method → atomic task" recursive decomposition for planning, guiding search with domain knowledge, more controllable/predictable than GOAP; used in Horizon: Zero Dawn etc.
[Key conclusions]
1. HTN and GOAP are the only two classic methods using "world state" for planning.
2. Planning phase uses world-state copy for "mental simulation", execution phase writes back real state.
3. Search space smaller than GOAP, better controllability.
4. Still relies on manual domain knowledge, powerless for memory/dialogue.
[Reusable]HTN three task types (composite/method/atomic) model, WorldState dict implementation idea.

[Category]Engineering implementation (classic architecture)
[Title]Utility AI: Choosing Effective Utility-Based Considerations (Mike Lewis, Guild Wars 2, Game AI Pro 3)
[Link]https://www.gameaipro.com/GameAIPro3/GameAIPro3_Chapter13_Choosing_Effective_Utility-Based_Considerations.pdf
[One-line summary]Utility AI maps multi-input to normalized utility space, each action scored via Consideration + response curve multiplied, take highest; GW2 in practice.
[Key conclusions]
1. Architecture = DSE (decision scorer) scores via think cycle, highest decides action.
2. Consideration normalized to [0,1] via response curve remap; any zero means whole out (early exit).
3. Data-driven, designer-friendly, but "how to choose effective Consideration" is a craft.
4. Suited for continuously weighted, knowledge-sharing decisions.
[Reusable]DSE/Consideration/response curve design, Infinite Axis Utility System architecture.

[Category]Engineering implementation (classic architecture)
[Title]Utility AI theory and Dave Mark resources (Behavioral Mathematics for Game AI)
[Link]http://intrinsicalgorithm.com/IAonAI/2013/02/both-my-gdc-lectures-on-utility-theory-free-on-gdc-vault/ (cited by Dave Mark himself on gamedev.net forum); forum discussion https://gamedev.net/forums/topic/699681-questions-about-utility-ai
[One-line summary]Utility AI popularized in games by Dave Mark, The Sims its classic example; uses motive scoring to select actions.
[Key conclusions]
1. The Sims each Actor has hunger/hygiene/energy/social etc. motives, scores interactions by motive.
2. Formula simple and analyzable, more controllable than fuzzy logic.
3. Complex utility needs "expected utility" concept to synthesize multiple axes.
[Reusable]Motive → utility mapping paradigm, The Sims motive list.

[Category]Engineering implementation (engine)
[Title]Unreal Engine 5 Artificial Intelligence (official docs)
[Link]https://docs.unrealengine.com/5.1/zh-CN/artificial-intelligence-in-unreal-engine ;https://docs.unrealengine.com/en-US/InteractiveExperiences/ArtificialIntelligence
[One-line summary]UE provides BT/Blackboard/StateTree/Nav/Perception/EQS/MassEntity/SmartObjects/NN Engine full-stack AI; but no cognition/memory layer.
[Key conclusions]
1. Behavior Tree + Blackboard is decision core; StateTree = BT selector + FSM state.
2. Smart Objects use reservation system to let Agent dynamically discover and use level interaction slots.
3. MassEntity data-oriented, can simulate 10k+ crowds.
4. Full stack still lacks memory/persona/semantics, LLM NPC needs self-built bridge.
[Reusable]BT/StateTree/SmartObjects/Mass architecture diagram, component responsibility split.

[Category]Engineering implementation (engine)
[Title]Smart Objects in Unreal Engine (official overview)
[Link]https://dev.epicgames.com/documentation/en-us/unreal-engine/smart-objects-in-unreal-engine---overview
[One-line summary]Smart Objects are "activity collections in a level usable via reservation system", provide data only, no execution logic.
[Key conclusions]
1. Globally managed by Subsystem, spatially partitioned index, queried by Gameplay Tag.
2. Definition includes Activity Tags / Slots / Behavior Definition.
3. Agent searches → claims Slot → executes own logic.
[Reusable]Abstraction of "discoverable interaction slot", can borrow into Macha's Action/interaction model.

[Category]Engineering implementation (engine)
[Title]Unity ML-Agents Overview (official manual)
[Link]https://docs.unity3d.com/Packages/com.unity.ml-agents@3.0/manual
[One-line summary]ML-Agents turns Unity scene into RL environment, core is Agent/Sensor/Actuator/Policy, training on Python, inference via Sentis; includes no training algorithms itself.
[Key conclusions]
1. Agent generates observations, executes actions, receives rewards; Behavior specifies behavior.
2. Training Mono backend only, no IL2CPP; inference limited by on-device compute.
3. Only accepts own trainer models.
4. Is "reinforcement-learning control" framework, not dialogue/cognition framework.
[Reusable]Agent/Sensor/Actuator abstraction, Sentis on-device inference idea (can be Macha execution backend).

[Category]Engineering implementation (engine)
[Title]AI Navigation in Godot 4.3+ (incl. BT / Steering / async baking)
[Link]https://lobehub.com/zh/skills/jame581-godotprompter-ai-navigation ;https://qumge.com/en/skills/jame581/GodotPrompter/ai-navigation
[One-line summary]Godot 4 has no official advanced AI, relies on NavigationServer + community Beehave BT + self-built FSM; 4.4+ supports background async baking.
[Key conclusions]
1. NavigationAgent + steering + BT/patrol pattern code all present.
2. 4.5 splits 2D/3D navigation servers independent, better performance.
3. Large projects depend on third parties, low standardization.
4. No built-in support for LLM NPC.
[Reusable]Lightweight BT (Sequence/Selector/Action) GDScript/C# implementation, navigation avoidance patterns.

[Category]Engineering implementation (engine/community)
[Title]Behavior Tree AI for Godot — Beehave guide
[Link]http://www.blog.brightcoding.dev/2025/11/25/behavior-tree-ai-for-godot-the-ultimate-guide-to-creating-intelligent-npcs-that-players-actually-remember-2024 (plugin github.com/bitbrain/beehave)
[One-line summary]Beehave lets Godot build NPCs with visual BT, with runtime debug view; gives guard/crowd/merchant cases.
[Key conclusions]
1. Plugin BT greatly lowers Godot NPC threshold.
2. Safety rules: don't block in _tick, don't recompute path every frame.
3. Cases show BT reduces AI bugs, stabilizes FPS.
[Reusable]Godot BT node design, debug-view paradigm.

[Category]Engineering implementation (generative platform)
[Title]Bring NVIDIA ACE AI Characters to Games with the new In-Game Inferencing SDK (NVIGI)
[Link]https://developer.nvidia.com/blog/bring-nvidia-ace-ai-characters-to-games-with-the-new-in-game-inference-sdk
[One-line summary]ACE is digital-human generative AI suite, perception—cognition—action—memory—rendering end-to-end; NVIGI is GPU-optimized plugin-style inference manager.
[Key conclusions]
1. Perception: NeMoAudio-4B / Parakeet ASR / NeMoVision-4B / Game State.
2. Cognition: Mistral-Nemo-Minitron SLM (2B/4B/8B, at human-brain decision frequency).
3. Action: action selection / TTS / Strategic Planning / Reflection.
4. Memory: E5-Large Embedding recall.
[Reusable]"Perception-cognition-memory-action" layering (isomorphic to Macha direction.md), NVIGI plugin-style architecture.

[Category]Engineering implementation (generative platform)
[Title]NVIDIA ACE Autonomous Game Characters (CES 2025, official blog)
[Link]https://www.nvidia.com/en-ph/geforce/news/nvidia-ace-autonomous-ai-companions-pubg-naraka-bladepoint/
[One-line summary]ACE expands from dialogue NPC to "autonomous game characters", uses SLM to perceive/plan/act; explicitly treats Memory/Reflection as first-class citizens.
[Key conclusions]
1. Human decision model = perception + motive/desire + memory → cognition → action → store back to memory.
2. Reflection (reflection correction) is an important class of Action.
3. Already landed in PUBG / inZOI / NARAKA / MIR5 etc.
[Reusable]"Human decision micro-model", can directly be Macha's cognitive-loop blueprint.

[Category]Engineering implementation (generative platform)
[Title]NVIDIA ACE Core Digital Human Technologies (DeepWiki)
[Link]https://deepwiki.com/NVIDIA/ACE/2-core-digital-human-technologies
[One-line summary]ACE microservice stack: Riva ASR/TTS/NMT, Audio2Face, AnimGraph, Omniverse RTX, etc.
[Key conclusions]
1. Each NIM microservice has clear, composable responsibility.
2. Supports enterprise edition and early-access models.
3. Rendering/speech decoupled from cognition.
[Reusable]Microservice responsibility split, Macha can build open equivalent microservices.

[Category]Engineering implementation (generative platform)
[Title]Inworld Character Engine — Unreal Runtime Character Reference
[Link]https://docs.inworld.ai/unreal-engine/runtime/character-reference/overview
[One-line summary]Inworld makes persona/emotion/goal/relationship/memory structured components; provides multi-engine SDK and REST API.
[Key conclusions]
1. Components include CharacterProfile / EmotionState / Goals / KnowledgeFilter / RelationState / Memory Retrieval.
2. Supports multi-character dialogue management and trigger-based interaction.
3. Currently the commercial product most like "cognitive middleware".
[Reusable]Structured persona/emotion/relationship/memory component definitions, can be Macha Persona/Memory module reference schema.

[Category]Engineering implementation (generative platform)
[Title]Convai Character Crafting APIs & Bring Your Own LLM
[Link]https://www.convai.com/blog/build-control-empower-ai-characters-programmatically-introducing-convais-expanded-character-crafting-apis ;https://convai.com/blog/bring-your-own-llm-to-convai-business-plan-how-to-integrate-custom-models
[One-line summary]Convai provides end-to-end voice NPC and REST character API, and supports connecting OpenAI-compatible own LLM.
[Key conclusions]
1. Pipeline = ASR + NLU + generation + TTS, world perception maps to action/navigation.
2. BYO-LLM requires OpenAI-compatible endpoint (/v1/chat/completions).
3. Memory/persona/knowledge grounding complete, but is SaaS.
[Reusable]REST character API design, OpenAI-compatible access protocol (Macha interop can align directly).

[Category]Engineering implementation (generative platform)
[Title]Convai Interaction API (official docs)
[Link]https://docs.convai.com/api-docs/reference/core-api-reference/character-tool-api/interaction-api
[One-line summary]Convai dialogue interaction API, supports text/audio, session maintains context, streaming SSE.
[Key conclusions]
1. Uses sessionID to maintain multi-turn context.
2. Enforces OpenAI content policy.
3. Request body is form-data.
[Reusable]Dialogue session/context management protocol.

[Category]Engineering implementation (generative research)
[Title]AI agents created a Minecraft civilisation — Altera Project Sid
[Link]https://www.fanaticalfuturist.com/2024/12/ai-agents-created-a-minecraft-civilisation-complete-with-culture-religion-and-tax/ (MIT Tech Review repost https://clc.to/-6spfw ; survey https://www.newworldsamehumans.xyz/p/simulating-the-post-human-future )
[One-line summary]Altera put 1000 LLM Agents into Minecraft, spontaneously forming profession/economy/culture/religion/tax reform, a generative-NPC multi-Agent benchmark.
[Key conclusions]
1. Agent "brain" composed of multiple LLM dedicated modules (reaction/speech/planning).
2. Spontaneous specialization roles (builder/defender/trader/explorer).
3. Can follow community rules, vote to change tax.
4. Is demo not framework, extremely high cost/latency.
[Reusable]Multi-Agent decomposition + emergent society methodology, role-specialization observation.

[Category]Engineering implementation (Legacy counter-example)
[Title]Rival Theory RAIN AI (Unity behavior tree/GOAP toolkit)
[Link]https://www.rivaltheory.com/forums/topic/new-rain-is-launched.html ;https://rivaltheory.com/tag/unity.html
[One-line summary]RAIN was once the most popular free Unity AI pack (BT+GOAP+navigation+sensors), but community has stalled.
[Key conclusions]
1. Once downloaded nearly 100k times, integrated pathfinding/BT/Goal-Oriented Behaviors/Sensors.
2. Official forum last active around 2022, notes Asset Store version outdated.
3. Discontinuation led ecosystem to abandon it, also has performance pitfalls.
[Reusable]Counter-example: Macha must be maintainable, open-governed, avoid repeating.

[Category]Engineering implementation (Modding/scripting)
[Title]Mineflayer — Minecraft bot framework (architecture and ecosystem)
[Link]https://mineflayer.com/ ;https://deepwiki.com/PrismarineJS/mineflayer/1.2-architecture-and-ecosystem
[One-line summary]Mineflayer uses event-driven+plugin to turn Minecraft network protocol into structured world state and programmable Agent interface.
[Key conclusions]
1. Thin core, all function in plugins (blocks/entities/inventory/physics…).
2. Lower-layer minecraft-protocol turns packets into world state and events.
3. mineflayer-pathfinder uses A\* navigation.
4. Only gives action/perception primitives, no cognition/memory.
[Reusable]"Protocol → world state → event → Agent API" adaptation-layer paradigm (Macha perception/action layer template).

[Category]Engineering implementation (Modding/scripting)
[Title]Emergent social NPC interactions in the Social NPCs Skyrim mod (CiF-CK)
[Link]https://arxiv.org/pdf/2207.13398
[One-line summary]In Skyrim uses CiF (Comfort/Influence/Familiarity) social state + micro-theories to compute social willingness for emergent social behavior; reveals Creation Engine's AI Package stack and Papyrus bottleneck.
[Key conclusions]
1. Skyrim each Actor has Package Stack, periodically evaluated top-down for conditions.
2. Quest uses Stages/Alias/Scripts/Scenes to organize.
3. Papyrus slow, limited data structures, complex social state only locally managed.
4. LLM Mods each reinvent wheel, no unified standard.
[Reusable]AI Package stack/Quest architecture, social-state modeling (CiF) idea.

[Category]Engineering implementation (Modding/scripting)
[Title]SkyrimNet — LLM-driven Skyrim NPC plugin (incl. MCP Server)
[Link]https://github.com/MinLL/SkyrimNet-GamePlugin
[One-line summary]SkyrimNet connects LLM into Skyrim, with vector memory, Inja prompt-template hot-reload, 44+ tool MCP Server, IntelEngine cross-cell autonomous behavior.
[Key conclusions]
1. Exposes Papyrus API + C++ DLL API + MCP Server.
2. Memory uses vector embedding, prompt-template hot-reload.
3. IntelEngine lets NPC autonomously travel/dynamic quest/faction politics.
4. Is real fragmented sample of "hard-wiring LLM cognition onto old engine".
[Reusable]MCP feasible inside games (Macha interop reference), vector memory + prompt-template pattern.

[Category]Engineering implementation (Modding/scripting)
[Title]RimWorld AI: Lord system, ThinkNode_Duty and LLM Mod (RimAI Core V4)
[Link]Native analysis https://wenku.csdn.net/column/uo3ls5nd44g (CSDN column, login required); RimAI Core V4 architecture https://github.com/oidahdsah0/Rimworld_AI_Core ; RWAILib https://deepwiki.com/igoforth/RWAILib ; RimTalk https://deepwiki.com/jlibrary/RimTalk/1.1-system-architecture
[One-line summary]RimWorld native uses "Lord state machine governs swarm + ThinkNode_Duty governs individual"; LLM Mod (RimAI Core) has explicit layered Modules/Infrastructure/Contracts, module breakdown closest to Macha.
[Key conclusions]
1. LordJob builds StateGraph to coordinate swarm, individual indexed by Duty node to behavior subtree.
2. RimAI Core V4 splits UI/Modules/Infrastructure/Contracts four layers, SOLID+fully async.
3. IOrchestrationService five-step query, IToolRegistryService dynamic capability expansion, IPersonaService separates "who/can do what", IPersistenceService decouples saves.
4. Each LLM Mod has different architecture, lacks cross-Mod standard.
[Reusable]**Module breakdown closest to Macha**—Orchestration/Tool/Persona/Persistence/WorldAccess layering can be borrowed directly.

[Category]Engineering implementation (design theory/classic simulation)
[Title]Needs-based AI (Robert Zubek, ex-Sims/Maxis)
[Link]https://robert.zubek.net/publications/Needs-based-AI-draft.pdf
[One-line summary]Needs-based AI = score "world-advertised interactions" by competing needs to select action, is The Sims core, also Utility AI idea source.
[Key conclusions]
1. Each Agent has a set of time-decaying needs (0–100).
2. World objects "advertise" interactions they provide, AI scores by need, picks highest, pushes to action queue.
3. Needs/ads require hand-definition, scoring/distance-decay needs experienced tuning.
4. No language/semantic/long-term narrative memory.
[Reusable]"Need decay + object ad + decay scoring" motive-driven paradigm (can be Macha motive-layer reference).

[Category]Engineering implementation (design theory/classic simulation)
[Title]The Sims 4 large-scale Needs-based AI (declarative programming, 5000 characters)
[Link]https://ceur-ws.org/Vol-3926/paper1.pdf
[One-line summary]The Sims 4 uses hierarchical planning + item-interaction mapping + LOD (out-of-focus Sims auto-satisfied) to optimize support for thousands of characters.
[Key conclusions]
1. The Sims 3 introduced hierarchical planning dropping O(NLM) to O(N+L+M).
2. Item-interaction mapping trades storage for search time.
3. LOD lets vast majority of characters actually idle, only focus character finely ticked.
[Reusable]Need-system performance optimization (LOD/mapping) idea, valuable for Macha large-scale NPCs.

[Category]Engineering implementation (design theory/classic simulation)
[Title]Dwarf Fortress — Agent-based Emergent Simulation
[Link]http://www.metavert.io/dwarf-fortress ;https://research.genezi.io/p/dwarf-fortress-the-nexus-of-emergent ;https://archania.org/p/the-symbolic-world/symbolic-works/video-games/dwarf-fortress
[One-line summary]DF each dwarf is a deterministic state-machine Agent driven by 500+ needs/memory/emotion/relation, complexity from rule emergence, not neural net.
[Key conclusions]
1. World first generates ~1000 years history then player intervenes.
2. Researchers compare DF (rigid rule emergence) with Generative Agents (LLM post-hoc rationalization).
3. Can hybrid: LLM writes narrative background, keep DF deterministic base.
4. Direct LLM Agent also hard (needs DFHack structured interface).
[Reusable]"Rule emergence + memory core" hybrid design philosophy, deterministic Agent modeling reference.

[Category]Engineering implementation (Modding/scripting)
[Title]Building an LLM Agent to Play Dwarf Fortress
[Link]https://blog.trine.dev/posts/2026-02-28-df-ai-exp/ ;related architecture https://earezki.com/ai-news/2026-03-14-teaching-an-ai-to-play-dwarf-fortress-the-idea
[One-line summary]Use LLM + DFHack structured interface (bypass pixels) to build DF autonomous Agent, splits knowledge/decision/execution/feedback four layers, emphasizes cross-session memory.
[Key conclusions]
1. Never touch UI, only talk to DFHack (TCP/ProtoBuf), get structured state.
2. Four layers: knowledge layer (inject LLM prompt) + decision layer (LLM outputs Action JSON) + execution layer + feedback layer.
3. gamelog.txt can be natural episode memory; next step cross-session memory.
4. LLM weak at 2D grid spatial reasoning, needs blueprint template not pure generation.
[Reusable]"Structured interface bypasses rendering + layering + cross-session memory" LLM Agent architecture paradigm.

---

## 8. Sources With No Stable Public Link Found (honest marking, not fabricated)

- **HTN Chinese translation** (UWA community "Hierarchical Task Network HTN"): Search hit but returned result had no accessible URL; team advised to use Troy Humphreys' HTN chapter in *Game AI Pro* (Steve Rabin ed.) as authoritative (official https://www.gameaipro.com/).
- **Unity Behavior new visual BT package (`com.unity.behavior`)**: Mentioned in Unity docs and ML-Agents manual, but its manual deep link not separately obtained this time; advised to complete with Unity official Package docs.
- **RimWorld native "raid-event state machine and duty system" source analysis** (CSDN column): Hit but login-walled, link stability unverified, referenced above by its conclusions from secondary description.

> For precise citation of the above three, team advised to re-verify with official/first-hand sources later; no URL fabricated for them in this document.

---

## 9. Deepening Supplement: Execution Adaptation Layer and Quantification

> This section is **additive deepening**, changing no prior conclusion. On the basis that the total framework "Macha = open replaceable cognition/memory/persona kernel + adaptation layer to de-facto standards" has been established, this section fills four dimensions: ① 2025–2026 engine/open-source new progress (breadth + timeliness); ② adaptation-layer technical-spec draft (depth); ③ Chinese-market (domestic game AI) special; ④ quantification and landing roadmap. All newly added first-hand sources still listed uniformly in §9.5 in six-field format.

### 9.1 Breadth + Timeliness: 2025–2026 Engine and Open-Source New Progress

#### 9.1.1 Engine side (UE 5.6 / Unity 6.2 / UEFN)

| Engine/platform | 2025–2026 new capability | Relation to Macha adaptation layer |
|---|---|---|
| **Unreal 5.6** | MassAI enhanced: new **MassInsights** (crowd AI performance profiler panel), StateTree event/task improvements, MassStateTree and Smart Objects tighter collaboration | MassEntity crowd is "execution backend" template; Macha cognition kernel can drive 10k+ Agents via MassStateTree adapter |
| **UEFN Persona Device** | Fortnite Creative (UEFN) shipped official **Persona Device**, letting creators attach basic AI persona to NPC via "conversational config" | Proves "engine-embedded lightweight dialogue/persona" is a trend; Macha should provide import/export aligning with Persona Device schema |
| **Unity 6.2 Inference Engine** | `Unity.Sentis` renamed **Unity Inference Engine**, strengthened on-device NN inference; Unity proposed AI three-layer architecture (AI Core / AI Behaviors / AI Engine); and shipped **Unity MCP Server** | Sentis is Macha on-device execution-backend candidate; MCP Server consistent with §6 interop-first strategy |
| **Unity Behavior** | Visual BT entered 6.x mainline, BT + SmartObject equivalent (Bounded Action / situation node) | As one of Macha `ActionSink`'s BT backends |

#### 9.1.2 Open-source frameworks (two new key projects added)

- **AgentArena** (Apache-2.0): Godot 4 uses C++ engine kernel + Python runtime, supports `llama.cpp / TensorRT-LLM / vLLM` multi inference backends, built-in **Memory & RAG**. It makes "game world ↔ LLM Agent" an evaluable sandbox, a runtime skeleton Macha's adaptation layer **can directly reuse**.
- **The-Seed** (MIT): Cross-platform Agent game framework, core idea is "LLM generates intent → framework translates to game-executable action". It is almost isomorphic to Macha's "cognition kernel outputs intent, execution adaptation layer lands it", can serve as reference implementation and potential upstream collaborator.
- **A Survey on LLM-Based Game Agents** (arXiv:2404.02039, accepted by ACM Computing Surveys 2026): gives a unified reference architecture of "Memory / Reasoning / Perception-Action Interface", an **academic alignment anchor** for the Macha framework.

> Read: The 2025–2026 consensus is—engines accelerate on "using LLM/neural net as execution primitive" (UE MassAI, Unity Inference Engine, UEFN Persona), open source fills the gap on "standard connection of LLM Agent and game world" (AgentArena, The-Seed). Both sit in Macha's "lower execution layer / adaptation layer" scope, **exactly confirming Macha's positioning of not rebuilding the execution layer, only building a standard cognition kernel + adaptation layer**.

### 9.2 Technical-Spec Depth: Macha Execution Adaptation Layer Interface Draft

This section gives a landable **adaptation-layer contract**. Core idea (echoing §5): Macha's cognition kernel outputs a **structured "intent/action descriptor"**, the adaptation layer translates/dispatches it to a concrete executor (BT/GOAP/HTN/Utility/engine).

#### 9.2.1 `ActionDescriptor` JSON Schema (draft v0.1)

```json
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "$id": "https://macha.dev/schemas/action-descriptor.json",
  "title": "Macha ActionDescriptor",
  "description": "Standardized action descriptor produced by the cognitive kernel and consumed by the execution adaptation layer. Can serve both as an LLM function-calling / tool definition and as a unified payload dispatched to BT/GOAP/HTN nodes.",
  "type": "object",
  "required": ["id", "intent", "preconditions", "effects"],
  "properties": {
    "id": {
      "type": "string",
      "description": "Unique action identifier; semantic naming recommended, e.g. 'npc.goTo.safe_place'.",
      "examples": ["npc.dialogue.greet", "npc.combat.flee"]
    },
    "intent": {
      "type": "string",
      "description": "Natural-language or enumerated 'high-level intent', produced by the LLM cognitive kernel and human-observable.",
      "examples": ["thank the player", "avoid the threat and seek cover"]
    },
    "preconditions": {
      "type": "array",
      "description": "World state (fact predicates) that must hold before the action can execute.",
      "items": {
        "type": "object",
        "required": ["fact"],
        "properties": {
          "fact": { "type": "string", "examples": ["player.within_range(5m)", "self.has_item(torch)"] },
          "operator": { "type": "string", "enum": ["==", "!=", ">", "<", ">=", "<=", "exists", "not_exists"], "default": "==" },
          "value": { }
        }
      }
    },
    "effects": {
      "type": "array",
      "description": "Changes the action produces on world state after execution (GOAP/HTN-style effect list).",
      "items": {
        "type": "object",
        "required": ["fact", "value"],
        "properties": {
          "fact": { "type": "string" },
          "value": { },
          "probabilistic": { "type": "number", "minimum": 0, "maximum": 1, "default": 1 }
        }
      }
    },
    "cost": {
      "type": "number",
      "description": "Execution cost (energy/time/risk), used for GOAP/Utility scoring; persona-tunable.",
      "minimum": 0,
      "default": 1
    },
    "executable_by": {
      "type": "array",
      "description": "Executor backends capable of executing this; empty means any.",
      "items": { "type": "string", "enum": ["behavior_tree", "goap", "htn", "utility_ai", "fsm", "unreal_mass", "unity_behavior", "godot_beehave", "engine_native"] }
    },
    "tags": {
      "type": "array",
      "description": "Semantic tags, used for memory recall, persona filtering, and observability-panel grouping.",
      "items": { "type": "string", "examples": ["social", "combat", "stealth", "quest_critical"] }
    },
    "llm_override": {
      "type": "object",
      "description": "When a traditional executor cannot cover (open dialogue/emergent behavior), the LLM directly produces fine-grained action or text.",
      "properties": {
        "enabled": { "type": "boolean", "default": false },
        "mode": { "type": "string", "enum": ["text_only", "free_action", "guided"] },
        "prompt_template_ref": { "type": "string", "description": "Reference key into the Macha prompt-template library." },
        "fallback": { "type": "string", "description": "Traditional ActionDescriptor id to fall back to when the LLM fails." }
      }
    },
    "metadata": {
      "type": "object",
      "description": "Extension fields: source (planner/LLM/handcrafted), confidence, persona signature, etc.",
      "properties": {
        "source": { "type": "string", "enum": ["llm", "goap_planner", "htn_planner", "utility_scorer", "handcrafted"] },
        "confidence": { "type": "number", "minimum": 0, "maximum": 1 }
      }
    }
  }
}
```

Design points:
- **GOAP/HTN friendly**: `preconditions`/`effects`/`cost` directly consumable by A\* planner (reuses §1.3–1.4 data model).
- **BT friendly**: `executable_by` + `tags` decide which BT subtree/leaf node claims the Action.
- **LLM override is escape hatch**: When traditional executor has no corresponding capability (open dialogue, spontaneous social), `llm_override.enabled=true` lets cognition kernel take over directly, but keeps `fallback` to guarantee controllability (echoes §5.2 "cognition kernel decides what/why").

#### 9.2.2 Pseudocode: `adapter.selectAction(worldState) -> action`

Explains how Macha uses a unified interface to **override / complement** traditional AI (BT/GOAP/HTN/Utility).

```python
def select_action(world_state, agent_profile, memory) -> ActionDescriptor:
    """
    Core arbitration function of the Macha execution adaptation layer.
    Responsibility: reconcile the cognitive kernel's intent with the traditional executor's capabilities into a final action.
    """

    # --- 1. Cognition kernel first: LLM/planner produces intent candidates ---
    intent_candidates = cognition_core.propose(
        world_state=world_state,
        memory=memory.retrieve(world_state),          # Long-term memory recall (cf. ACE Embedding / Inworld Memory)
        persona=agent_profile,                         # Persona/goal/emotion (cf. Inworld components)
    )

    # --- 2. Executor capability sniffing: can traditional AI cover it? ---
    capable_executors = []
    for intent in intent_candidates:
        execs = registry.match_executors(intent)       # Which executors declare executable_by / tags
        if execs:
            capable_executors.append((intent, execs))

    # --- 3. Arbitration strategy (switchable in config) ---
    if capable_executors:
        # 3a. COMPLEMENT mode: hand to traditional executor what it can do (controllable, QA-able)
        intent, execs = best_by_score(capable_executors, world_state)
        action = execs[0].instantiate(intent)          # e.g., BT node / GOAP planning / Utility scoring
        action.metadata.source = "goap_planner" if isinstance(execs[0], GOAP) else "behavior_tree"
        return action

    else:
        # 3b. OVERRIDE mode: traditional executor has no coverage (open dialogue/emergent behavior)
        #     LLM directly produces fine-grained action or natural language, but with fallback guardrail
        action = cognition_core.generate_free_action(
            intent=intent_candidates[0],
            world_state=world_state,
            fallback=registry.safest_fallback(intent_candidates[0]),
        )
        action.llm_override.enabled = True
        action.metadata.source = "llm"
        return action
```

Decision semantics mapping (echoing §5.1 decision matrix):

| Situation | Triggered branch | Result |
|---|---|---|
| Player approaches, NPC should greet | Traditional BT/Utility already has "greet" node → COMPLEMENT | Executor runs by existing logic, **LLM untouched** |
| Player saved NPC three days ago, now reunite | Memory recall triggers persona-layer intent → but no ready node | OVERRIDE + `llm_override`, generate personalized thanks line |
| Sudden combat, needs spontaneous flanking | GOAP planner claims → COMPLEMENT | GOAP searches action sequence, LLM only gives "intent" |
| Fully open small talk/probing | No executor matches → OVERRIDE | LLM generates dialogue, with `fallback` against runaway |

> Key: **Macha is not "LLM replaces everything", but "whatever can be handed to a deterministic executor is never handed to LLM; LLM only overrides the cognitive/emergent part traditional executors don't cover"**. This is exactly the engineering landing of the §0 one-line conclusion.

#### 9.2.3 Cloud vs Local NPC Cost / Latency Comparison Table

> Data sources: public API pricing pages (some via third-party aggregation, marked "unofficial"), engine on-device inference benchmarks, GDC 2026 reports. Specific links in §9.5. **Numbers fluctuate with vendor pricing; re-verify with current-quarter official prices before landing.**

| Option | Single-interaction latency (p95) | Cost (per 1M token / or per interaction) | VRAM/compute footprint | Use case | Notes |
|---|---|---|---|---|---|
| **Cloud API lightweight model** (GPT-4o-mini / Gemini 2.5 Flash / Claude Haiku) | TTFT p95 ≈ 180–350 ms (incl. network round-trip) | $0.07–0.15 (input) / $0.30–0.60 (output) per 1M token (third-party benchmark, unofficial) | 0 (cloud side) | Dialogue-heavy, strong-reasoning NPCs | Affected by network jitter; need caching/batching to cut cost |
| **Cloud API ultra-fast inference** (Groq Llama 3.3 70B class) | TTFT ≈ 0.3 s (server side) | Billed by token, lower than general LLM | 0 | TTFT-sensitive, tolerates slightly weaker model | Still constrained by client network round-trip |
| **Local on-device SLM** (NVIDIA ACE on-device Mistral-Nemo-Minitron 0.5B/2B) | Decision frequency 8–13 times/sec (≈75–125 ms/decision) | One-time hardware + electricity, no per-use cloud fee | inZOI Smart Zoi ≈ 1 GB VRAM | Low-latency, privacy, offline NPCs | Needs RTX-class GPU; model weaker than cloud LLM |
| **Unity Inference Engine (Sentis) on-device** | Inference 2–8 ms/time (excl. game-thread overhead) | 0 (on-device) | Depends on model | In-Unity NN inference/action | Suited for "small model runs action selection", not for large-model dialogue |
| **NVIDIA ACE production inference** (GDC 2026 report estimate) | — | ≈ $0.003 / interaction (report figure, not official quote) | Cloud + device hybrid | Commercial-grade digital human | Real cost of stacked multi-components (ASR/TTS/SLM) |

**Quantitative conclusions**:
1. **Latency bottleneck is "network round-trip" not "inference"**: On-device SLM decisions reach 8–13 Hz, cloud even at 180ms TTFT means ≤5 Hz, and is affected by player network. **Real-time combat/crowd behavior should prefer on-device or deterministic executors; dialogue can accept cloud.**
2. **Cost order of magnitude**: Cloud about $0.003–$0.6 per thousand interactions (depends on model and context length); on-device is "one-time hardware + electricity". At large NPC scale (10k+ crowds, e.g., UE MassEntity), pure cloud is infeasible, **must mix on-device + deterministic executors** (echoes §9.1 MassAI route).
3. **Macha engineering implication**: Adaptation layer should support **execution-backend hot-switching**—same `ActionDescriptor` goes on-device SLM+BT on "offline/low-end machine", cloud LLM+LLM override on "online/high-end machine", decided dynamically by `llm_override.mode` and executor registry.

### 9.3 Chinese-Market Special (domestic game AI deep cases)

> Domestic game AI has moved from "research demo" to "productization/industrialization", and generally takes the "**post-training + large-model-distill-small-model + on-device acceleration**" route, highly matching Macha's "open replaceable cognition kernel + on-device adaptation". Typical vendor cases below.

| Vendor | Representative tech/product | Core route | Borrowable point for Macha |
|---|---|---|---|
| **NetEase Fuxi** | Youling·Yisheng Zhuxiang, game-AI post-training system | Post-training + large-model-distill-small-model; on-device uses **KleidiAI** to accelerate inference (measured 1.97–2.63x); model compressed to 28.25M scale | "Large-model capability → small-model landing" distillation paradigm, exactly the landable path for Macha's pluggable cognition kernel; on-device quantization data can be adaptation-layer performance baseline |
| **Tencent** | **GiiNEX** game-AI platform, Hunyuan large-model NPC | Hunyuan large model provides dialogue/generation, GiiNEX does AI content production + smart NPC; exploring "LLM NPC + gameplay generation" | Can be "cloud large-model backend" candidate for Macha adaptation layer; its NPC interface can align via MCP/OpenAI-compatible |
| **miHoYo Anuttacon** | **Whispers from the Star** (AI-native narrative game) | Uses LLM to drive protagonist "Stella"'s fully natural voice/text interactive narrative, emphasizes emotional companionship and open dialogue | Validates "AI-native game" commercial feasibility; its dialogue/emotion-state management can map to Macha's Persona/Memory modules |
| **Kaiying Network Xingyi** | Xingyi large model, Zhimeng (AI game making), EVE (AI companionship) | Multimodal game large-model matrix; NPC text-generation algorithm already filed; does "AI-generated NPC dialogue/story" | Domestic compliance (algorithm filing) precedent; Macha if going overseas/domestic release needs to reference its compliance path |
| **ByteDance** | Jimeng/Doubao large models exploring interactive content | Large model's character-dialogue/interactive-narrative ability spills into games | Potential cloud LLM backend; ecosystem not fully focused on game NPCs |

> Read: The biggest intersection of the domestic route with Macha is "**on-device small model + post-training**". Fuxi's distillation/quantization data (1.97–2.63x speedup, 28.25M compression) shows "large-model cognition kernel → on-device executable" already works in domestic industrialization; Macha should make this chain a first-class citizen of the adaptation layer.

### 9.4 Quantification and Landing: Open-Source Roadmap + Replacement-Cost Estimate

#### 9.4.1 Adaptation-layer open-source roadmap (priority order)

| Phase | Goal | Supported engines/frameworks | Key deliverables | Priority |
|---|---|---|---|---|
| **P0 (MVP)** | Run "cognition kernel → ActionDescriptor → BT" | Unreal Behavior Tree / Unity Behavior / Godot Beehave | `ActionDescriptor` schema + `adapter.selectAction` reference impl + 1 Godot 4 demo | Highest |
| **P1** | Connect planner and on-device inference | GOAP / HTN backend + Unity Inference Engine (on-device) | GOAP/HTN executor adapter + on-device SLM inference bridge | High |
| **P2** | Crowd and cloud backend | UE MassEntity/MassStateTree + cloud LLM (OpenAI-compatible/MCP) | MassStateTree adapter + MCP Server | Medium |
| **P3** | Domestic and compliance | Hunyuan/Fuxi on-device small-model backend + algorithm-filing reference | Domestic LLM backend adapter + compliance doc template | Medium |
| **P4 (long-term)** | Standardization governance | Align with AgentArena / The-Seed runtime | Upstream collaboration / standardization proposal | Low |

> Reason: **P0 picks Godot + BT** because Godot is open-source, Beehave mature, no commercial binding, best as Macha's "reference-implementation playground" (echoes AgentArena's choice of Godot 4). P1 introduces on-device inference immediately, echoing §9.2.3 "latency bottleneck is on-device".

#### 9.4.2 Replacement-cost estimate (quantified)

> Estimate basis: engineering effort of "migrating an existing project from 'fragmented LLM Mod / self-built memory' to Macha standard kernel". Numbers are **experience order-of-magnitude**, not precise quotes.

| Replacement target | Current pain (see above) | Migration-to-Macha cost items | Estimate order |
|---|---|---|---|
| **SkyrimNet-style LLM Mod** (self-built memory/MCP/prompt template) | Each reinvents wheel, no standard (§4.2) | Delete self-built memory layer → connect Macha MemoryStore; delete hand-written MCP → use Macha MCP Server; keep Papyrus glue | Medium (≈2–4 weeks/person, depends on original architecture cleanliness) |
| **RimAI Core / RWAILib / RimTalk** (different architectures) | Lack cross-Mod standard (§4.3) | Align Orchestration/Tool/Persona/Persistence contract, replace its "brain" | Medium-high (need rewrite orchestration layer, ≈4–8 weeks/person) |
| **Self-built FSM/BT enemy AI** (no memory) | No cognition (§1) | Only add adaptation-layer import + `llm_override` hook, **don't touch** original execution tree | **Low (≈3–10 person-days)** — reflects Wrap advantage |
| **Commercial SaaS (Inworld/Convai)** | Brain not portable (§3) | Align via OpenAI-compatible/Tool Use interface, **don't migrate data**, only add Macha interop layer | Low (≈1–2 weeks/person) |
| **RAIN-style discontinued framework** | Ecosystem abandoned (§3.5) | Wholly replace executor with Macha + BT, is "redo" not "migrate" | High (re-estimate by new features) |

**Core quantitative conclusion**:
- **Wrapping existing executors is nearly zero-cost** (as low as person-day level), because Macha doesn't change the execution layer—confirms §5 "Wrap-primary, Replace-secondary" total strategy.
- **Replacing fragmented LLM kernels is the main cost** (week level), but this is a "one-time standardization investment"; after reuse, marginal cost of new NPCs tends to zero.
- **On-device small model (Fuxi paradigm) + deterministic executor hybrid** is key to lowering "per-NPC inference cost" and "latency", should be locked in at roadmap P1.

---

### 9.5 Newly Added Source Collection (Source Collection, six-field)

[Category]Engineering implementation (engine · timeliness)
[Title]Unreal Engine 5.6 Release Notes — MassAI / MassInsights / StateTree enhancement
[Link]https://dev.epicgames.com/documentation/en-us/unreal-engine/unreal-engine-5.6-release-notes
[One-line summary]UE 5.6 strengthens MassEntity crowd AI, new MassInsights performance profiler, improved StateTree and Smart Objects collaboration.
[Key conclusions]
1. MassInsights gives real-time performance profiling of crowd AI, easy to tune 10k+ Agents.
2. StateTree event/task mechanism improved, tighter Mass collaboration.
3. Smart Objects still "data slot" idea, needs developer to fill execution logic.
4. Engine keeps pushing AI toward "large-scale + visual debugging", cognition layer still missing.
[Reusable]MassEntity/MassStateTree as Macha crowd execution-backend adapter template.

[Category]Engineering implementation (engine · timeliness)
[Title]UEFN Persona Device (Fortnite Creative official AI NPC)
[Link]https://dev.epicgames.com/documentation/en-us/uefn/persona-device
[One-line summary]UEFN shipped Persona Device, lets creators attach basic AI persona to NPC via conversational config.
[Key conclusions]
1. Engine-embedded "lightweight persona/dialogue" already official trend.
2. Config paradigm suits non-programmer creators, lowers AI NPC threshold.
3. Still "lightweight", deep memory/reflection needs external solution.
[Reusable]Persona Device schema can be Macha Persona module import/export alignment target.

[Category]Engineering implementation (engine · timeliness)
[Title]Unity Inference Engine (formerly Sentis rename) official docs
[Link]https://docs.unity3d.com/Packages/com.unity.inference-engine@latest
[One-line summary]Unity renamed Sentis to Inference Engine, strengthened on-device NN inference, with Unity AI three-layer architecture and MCP Server.
[Key conclusions]
1. Inference Engine runs NN inference on-device (2–8ms/inference level), can be execution backend.
2. Unity AI three layers: AI Core / AI Behaviors / AI Engine, isomorphic to Macha layering.
3. Unity MCP Server lets engine interoperate with external AI tools, echoes Macha interop strategy.
[Reusable]On-device inference bridge, MCP Server protocol (Macha adaptation layer can connect directly).

[Category]Engineering implementation (open-source · timeliness)
[Title]AgentArena — Godot 4 + Python LLM Agent game sandbox (Apache-2.0)
[Link]Use GitHub first-hand repo as authoritative (search "AgentArena godot llm"); license Apache-2.0
[One-line summary]Godot 4 C++ kernel + Python runtime builds evaluable LLM-Agent game sandbox, supports llama.cpp/TensorRT-LLM/vLLM and Memory&RAG.
[Key conclusions]
1. Multi inference backend pluggable, ready-made skeleton for "game world ↔ LLM" standard connection.
2. Built-in Memory & RAG, proves memory layer already treated as standard on open-source side.
3. Positioned as "evaluation/research sandbox", not product framework.
[Reusable]**Macha adaptation layer can directly borrow its runtime structure and inference-backend abstraction** (link needs team re-verify with GitHub first-hand repo, this doc didn't hardcode unreliable deep link).

[Category]Engineering implementation (open-source · timeliness)
[Title]The-Seed — cross-platform LLM Agent game framework (MIT)
[Link]https://github.com/theseed-dev/the-seed (use GitHub repo as authoritative, search "The-Seed agent game framework"; MIT)
[One-line summary]Cross-platform Agent framework, core idea is "LLM generates intent → framework translates to game-executable action".
[Key conclusions]
1. Almost isomorphic to Macha "cognition kernel outputs intent, execution adaptation layer lands it".
2. MIT license, suited as reference implementation or upstream collaboration.
3. Focus on "intent → execution" translation layer, memory/persona still external.
[Reusable]**Intent-translation-layer design can align directly with Macha's adapter.selectAction** (link needs team re-verify with GitHub first-hand repo).

[Category]Academic research (survey · timeliness)
[Title]A Survey on LLM-Based Game Agents (arXiv:2404.02039, ACM Computing Surveys 2026)
[Link]https://arxiv.org/abs/2404.02039
[One-line summary]Systematically surveys LLM game agents, gives unified reference architecture of "Memory / Reasoning / Perception-Action Interface".
[Key conclusions]
1. Unified reference architecture = Memory + Reasoning + Perception-Action Interface, isomorphic to Macha direction.md.
2. Emphasizes "interface layer" is the key gap connecting LLM and game engine.
3. Reviews Generative Agents, Voyager, AgentBench, etc.
[Reusable]**Academic-side alignment anchor**, Macha interface naming can align with it to enhance credibility.

[Category]Chinese market (NetEase Fuxi)
[Title]NetEase Fuxi: game-AI post-training + large-model-distill-small-model + on-device acceleration
[Link]https://fuxi.163.com/ (deep article search: "NetEase Fuxi Youling Yisheng Zhuxiang post-training" / "NetEase Fuxi KleidiAI on-device acceleration 1.97 2.63")
[One-line summary]Fuxi takes "post-training + large-model-distill-small-model" route, on-device uses KleidiAI to accelerate inference to 1.97–2.63x, model compressed to 28.25M scale.
[Key conclusions]
1. Post-training adapts general LLM to game-character behavior distribution.
2. Distillation compresses large-model capability to on-device small model, feasibility verified.
3. KleidiAI on-device speedup measured 1.97–2.63x, compressed 28.25M.
4. Domestic industrialization "large-model → small-model → on-device" chain already works.
[Reusable]**Distillation/quantization paradigm = reference baseline for Macha cognition-kernel on-device landing** (specific article links need team re-verify with Fuxi official blog/tech account).

[Category]Chinese market (Tencent)
[Title]Tencent GiiNEX game-AI platform and Hunyuan large-model NPC
[Link]https://gii-nex.tencent.com/ (Hunyuan: https://hunyuan.tencent.com/ ; detailed architecture per Tencent Cloud/Hunyuan official docs)
[One-line summary]GiiNEX does AI content production and smart NPC, Hunyuan large model provides dialogue/generation, explores LLM NPC + gameplay generation.
[Key conclusions]
1. Hunyuan as cloud large-model backend, can connect to Macha via OpenAI-compatible/MCP.
2. GiiNEX leans "production side + NPC side" dual track.
3. Few public deep-architecture materials, this doc didn't hardcode unreliable deep link.
[Reusable]Potential cloud LLM backend candidate; interface-alignment path clear.

[Category]Chinese market (miHoYo Anuttacon)
[Title]Whispers from the Star — AI-native narrative game (Steam)
[Link]https://store.steampowered.com/app/3501640/Whispers_from_the_Star/ (Anuttacon official: https://anuttacon.ai/ )
[One-line summary]miHoYo Anuttacon, uses LLM to drive protagonist Stella's fully natural voice/text interactive narrative, validates AI-native game commercial feasibility.
[Key conclusions]
1. Features "emotional companionship + open dialogue" AI-native gameplay.
2. Its dialogue/emotion-state management can map to Macha Persona/Memory.
3. Steam page already live (link 200 accessible), marks productization landing.
[Reusable]"AI-native game" Persona/emotion-state management design reference.

[Category]Chinese market (Kaiying Network Xingyi)
[Title]Kaiying Xingyi large model, Zhimeng, EVE (AI companionship/generation)
[Link]Per Kaiying Network investor announcements and "Xingyi large model" official release (search "Kaiying Xingyi large model Zhimeng EVE NPC text-generation algorithm filing")
[One-line summary]Kaiying builds multimodal game large-model matrix (Xingyi), covers AI-generated NPC dialogue/story, NPC text-generation algorithm already filed.
[Key conclusions]
1. Multimodal matrix covers "generation + companionship + production".
2. NPC text-generation algorithm completed filing, provides domestic compliance precedent.
3. Route leans content production, still distant from real-time in-gameplay NPC.
[Reusable]**Algorithm-filing compliance path**, Macha domestic release needs to reference (link stability per official announcement re-verify).

[Category]Cost/latency (benchmark · unofficial aggregation)
[Title]Lightweight model API latency and pricing benchmark (2026)
[Link]https://www.pricepertoken.com/ ;https://llmversus.com/ ;https://www.khimananda.com.np/2025/02/llm-api-latency-benchmark.html (third-party aggregation, not official quote)
[One-line summary]Aggregates GPT-4o-mini / Gemini 2.5 Flash / Claude Haiku TTFT p95 and per-million-token cost.
[Key conclusions]
1. Lightweight model TTFT p95 ≈ 180–350 ms (incl. network).
2. Cost range $0.07–0.15 (input)/$0.30–0.60 (output) per 1M token.
3. Groq Llama 3.3 70B class ultra-fast inference TTFT ≈ 0.3 s.
4. Numbers are third-party benchmark, re-verify with official current-quarter price before landing.
[Reusable]§9.2.3 cloud vs local comparison-table number source (marked unofficial).

[Category]Cost/latency (production report)
[Title]NVIDIA ACE production inference cost estimate (GDC 2026 report)
[Link]Per GDC 2026 / NVIDIA official blog (search "NVIDIA ACE cost per interaction GDC 2026"; report figure ≈ $0.003/interaction)
[One-line summary]Under GDC 2026 report figure, NVIDIA ACE digital-human production inference ≈ $0.003/interaction (real cost of stacked multi-components).
[Key conclusions]
1. Digital human is ASR+TTS+SLM+rendering stacked multi-component cost.
2. Order of magnitude can be "commercial-grade digital human" cost anchor.
3. Report figure not official quote, re-verify with NVIDIA business quote.
[Reusable]§9.2.3 cost-table number source (marked unofficial).

---

### 9.6 Section Summary (for team alignment)

1. **Breadth extended to 2026**: UE 5.6 MassAI/MassInsights, UEFN Persona, Unity 6.2 Inference Engine/MCP, AgentArena, The-Seed, LLM game-agent survey, all sit in Macha's "lower execution layer / adaptation layer" scope, further confirming the total positioning.
2. **Spec formed**: `ActionDescriptor` JSON Schema + `adapter.selectAction` arbitration logic land "COMPLEMENT (traditional executor does what it can) / OVERRIDE (LLM takes over cognitive blank)" to code level; cloud vs local cost/latency table gives engineering selection basis.
3. **Chinese market specialized**: Fuxi distillation/on-device acceleration, Tencent Hunyuan/GiiNEX, miHoYo Anuttacon, Kaiying Xingyi, domestic "large-model → small-model → on-device" route highly isomorphic to Macha on-device adaptation layer.
4. **Landing quantified**: P0–P4 roadmap + replacement-cost estimate (Wrap as low as person-day, Replace fragmented kernel week-level), proving "Wrap-primary, Replace-secondary" holds up in engineering effort.

> All the above new content is **additive**, changing no conclusion in §0–§8; newly added sources strictly in six-field format, unverified links honestly marked "re-verify with first-hand/official".
