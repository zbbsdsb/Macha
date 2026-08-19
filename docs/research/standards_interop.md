# Reference Material for Macha's "Standard Interface Draft"

> Category: Standards and ecosystem (Layer 6 of the Macha six-layer framework)
> Research goal: Provide **interoperability**-level factual basis and an interface draft for Macha to become the "standard skeleton" of the game-NPC domain, covering four blocks: interop protocols, game-industry standard interfaces, open-source framework design philosophy, and model-access standards.
> Related docs:
> - `direction.md` (Macha = Perception—Memory—Reasoning—Action, minimal verifiable direction)
> - `positioning.md` (underlying cognitive architecture + engine-agnostic interface + evaluation)
> - `architecture.md` (Perception → Memory → Reasoning → Action four-layer kernel + `Observation`/`MemoryItem`/`BaseAgent` interface draft)
> - `engineering_npc_architectures.md` (key conclusion: **upper cognition/memory/persona standardized by Macha (Replace), lower execution/control and engines/commercial platforms adapted by Macha (Wrap)**)

---

## 0. One-Line Conclusion (for the interface draft)

To make Macha a "standard skeleton," the real interface work is only two layers:

1. **For the three external things—"model / tool / engine"—adopt the existing de-facto-standard protocol shapes, don't reinvent**: model access aligns with **OpenAI-compatible API**; tool calls align with the JSON-Schema shape of **Anthropic Tool Use / OpenAI Function Calling**, and use **MCP** to standardize-expose "external tools/resources"; engine adaptation aligns with **ECS (Unity DOTS / Unreal MassEntity) + behavior-tree execution shell + each engine's plugin conventions**; multi-NPC collaboration aligns with **A2A/ACP (runtime interaction) + AutoGen/OpenAI Agents-style handoff orchestration** (rigorous semantics can borrow from **FIPA ACL**).
2. **Only the "cognitive kernel" (memory, persona, reflection, planning, semantic perception) is the domain where Macha must define its own standard**—this exactly corresponds to the Replace conclusion of `engineering_npc_architectures.md`: the "brain" parts hand-built by various open-source LLM Mods (RimAI / SkyrimNet) and privatized by various commercial platforms (Inworld / ACE) are the fragmented status quo Macha wants to unify and replace.

> One sentence: **Macha's "standard" = an open replaceable cognitive kernel + an adaptation layer to established de-facto standards (OpenAI API / MCP / ECS / A2A).** It invents no transport protocol, only defines the contract between "cognitive layer ↔ standard protocol."

---

## 1. Interop Protocols

### 1.1 MCP (Model Context Protocol, Anthropic)

- **What it standardizes**: Inside a "single Agent," standardizes the connection of LLM to external **tools (Tools), resources (Resources), prompts (Prompts)** as an open protocol. Essentially a client—server protocol on top of **JSON-RPC 2.0**, defining primitives `initialize → tools/list → tools/call`, `resources/read`, `prompts/get`, `sampling`, `elicitation`, `roots`, `completion`, `logging`.
- **Interface shape**:
  - Transport layer: `stdio` (local subprocess) or `Streamable HTTP` (remote, replacing early SSE), JSON-RPC messages; the 2025-11-25 version added **Tasks** (async call-now / fetch-later), **Extensions framework**, enterprise OAuth 2.1.
  - Core data types: `Tool { name, description, inputSchema(JSON Schema) }`, `Resource { uri, mimeType }`, `Prompt`.
  - Client can connect to any MCP Server; Server can also call back the client's LLM via `sampling` (note: this opens the loop of "Server using the model in reverse").
- **How Macha adopts / adapts**:
  - **Expose Macha's cognitive-kernel "capabilities" as an MCP Server**: e.g., `remember`/`recall`/`reflect` can be MCP Tools, so external Agents / editors / engine plugins can call Macha without coupling to Macha source—directly targeting §6 of `engineering_npc_architectures.md` "expose MCP Server + OpenAI-compatible Tool Use externally."
  - **Macha also acts as an MCP Client consuming external tools**: in-game actions like "check inventory / play animation / read world state" can be implemented by the engine side as an MCP Server; Macha only handles cognition, not execution. SkyrimNet already proved this route works in games with an MCP Server (44+ tools).
  - Use the 2025-11-25 version's Tasks primitive to express "long-running tasks" (e.g., "NPC proactively brings this up three days later" can be modeled as an async Task).

### 1.2 OpenAI Function Calling / Anthropic Tool Use (tool-call shape)

- **What it standardizes**: Upgrades LLM from "pure text generation" to "output structured call intent." The concepts are consistent but the field shapes differ:
  - **OpenAI**: `tools: [{ type:"function", function:{ name, description, parameters(JSON Schema) } }]`, returns `message.tool_calls[]` (arguments is a JSON string). Supports `strict: true` (Structured Outputs, guaranteeing parameters strictly conform to schema), parallel calls, `tool_choice`.
  - **Anthropic**: `tools: [{ name, description, input_schema(JSON Schema) }]`, returns the `tool_use` block in `content` (`.input` is already a dict), judged by `stop_reason=="tool_use"`, result fed back via `role:"user"` + `tool_result` block; also supports `strict: true`, `server tools` (Web Search etc. hosted by Anthropic).
- **Interface shape**: **Unified "tool = a capability described by one JSON Schema."** This is exactly the most natural upper contract for Macha's `Action` module—whether dispatched to a behavior tree, sent to Unity, or handed to MCP, it first converges into "one tool call with a JSON Schema."
- **How Macha adopts / adapts**:
  - Define `Action` module output as **Tool-Use shape** (name + input_schema + structured args), making Macha compatible with OpenAI / Anthropic / any OpenAI-compatible endpoint (see §4), and naturally carried by MCP `tools/call`.
  - Beyond `architecture.md`'s `Observation`/`MemoryItem`, add an `ActionCall` dataclass (`tool: str, args: dict, provenance: str`) as the minimal "semantic action" unit between cognitive and execution layers.

### 1.3 Multi-Agent Communication Protocols (FIPA ACL / A2A / ACP)

#### FIPA ACL (Foundation for Intelligent Physical Agents)
- **What it standardizes**: A **Agent Communication Language** based on speech-act theory, defining 22 communicative acts like `inform / request / query-if / propose / cfp / agree / refuse …`, plus message fields `:sender :receiver :content :language(FIPA-SL) :ontology :protocol :conversation-id`; and gives each act **formal semantics** (feasibility precondition + rational effect) via modal logic (BDI). Comes with interaction protocols (FIPA-Request / Contract-Net etc.) and Agent management platform (AMS / DF / MTS).
- **Interface shape**: Messages transported in s-expression / XML / binary encodings, transport can be IIOP / HTTP. Emphasizes "reply `not-understood` if cannot process."
- **How Macha adopts / adapts**: FIPA is academic, semantics-heavy, little industry landing, but it is **the most rigorous semantic base for multi-NPC social interaction**. Macha need not implement full FIPA, but should borrow two points:
  - **Model NPC-to-NPC communication with "intent type (communicative act)" not bare messages** (e.g., `request`, `inform`, `propose`), so multi-NPC collaboration can be reasoned about and audited;
  - **ontology field**: the cross-NPC shared "world/relation ontology" is exactly what Macha's memory layer does; borrow FIPA's ontology concept to define Macha's relation/world-knowledge schema.

#### A2A (Agent2Agent, Google, 2025-04; now under Linux Foundation)
- **What it standardizes**: **Agent ↔ Agent** discovery and collaboration. Core constructs: `Agent Card` (`.well-known/agent.json`, declares capability/skill/auth), `Task` (state machine: submitted→working→input-required→completed/failed, supports long-running tasks and SSE streaming), `Message`/`Artifact`/`Part` (TextPart / FilePart / DataPart multimodal). Transport uses **HTTP(S) + JSON-RPC 2.0 + SSE**, auth aligns with OpenAPI (OAuth2 / OIDC), with built-in OpenTelemetry observability.
- **Interface shape**: Client pulls remote Agent Card → auth → `tasks/send` or `tasks/sendSubscribe` (SSE) → fetch Artifact.
- **How Macha adopts / adapts**: When Macha drives **multiple NPCs collaborating with each other / with external-environment Agents**, use A2A's `Agent Card` for NPC capability declaration, `Task` for collaboration-task lifecycle. This directly corresponds to the "multi-NPC sociality" goal in Macha's six-layer framework, and the `input-required` state naturally supports "NPC asks player/other NPC a follow-up."

#### ACP (Agent Communication Protocol, IBM BeeAI, 2025-03)
- **What it standardizes**: Same period as A2A, similar goal **Agent ↔ Agent** REST protocol, core is "make calling an Agent as simple as calling a REST service"—`Agent Manifest` (build-time offline declaration, referencing W3C WebFinger / ActivityPub's Actor), `Run` (one execution, MIME-typed MessagePart), supports `await` (pause for person/thing input).
- **Relation to A2A (important)**: Per the 2025-08 community status, **ACP has merged into A2A, brought under Linux Foundation, the two unified into a single A2A standard**, BeeAI platform now runs on A2A. Therefore Macha's new-system design should **anchor only on A2A**, ACP only as a reference for the "REST-first / build-time manifest" idea, no separate integration.

> MCP connects "Agent↔tool/data", A2A connects "Agent↔Agent"—the two are complementary, exactly the two protocol layers Macha's adaptation layer needs to support simultaneously.

---

## 2. Game-Industry Standard Interfaces

### 2.1 ECS (Entity Component System) Architecture

- **What it standardizes**: A "data-oriented" software architecture paradigm—**Entity (unique ID) + Component/Fragment (pure data) + System/Processor (logic)** decouples data and behavior, driven by `Query` (filter entities by component combination) for batch processing, memory laid out compactly by Archetype/Chunk to squeeze CPU cache.
- **Interface shape (Unity DOTS)**: `IComponentData` (data); `System` (logic, with Job/Burst); `EntityManager` manages entities and components; GameObject converted into ECS via `Baking`/`IConvertGameObjectToEntity`; with `Entities Graphics / Unity Physics / Netcode for Entities`.
- **Interface shape (Unreal MassEntity)**: Slightly different terms—`Fragment` (=Component, logic-irrelevant data), `Processor` (=System, stateless, batch via `EntityQuery`), `Archetype` (entity set with same Fragment+Tag combination), `Chunk` (memory block), `Tag` (empty struct, for filtering), `Trait` (functional set of Fragment+Processor, can be declared/inherited in `MassEntityConfig` asset). From UE5.5 MassEntity merged into core engine.
- **How Macha adopts / adapts**:
  - **Model Macha's "world state / entity cognition" as ECS-friendly structure**: NPC, player, items are all Entities; Macha-written `PersonaState`/`RelationState`/`Belief` as Fragment (Component), engine's execution systems (BT/navigation/animation) read these Fragments. This is completely isomorphic to `engineering_npc_architectures.md` treating engine AI as "an adaptable execution backend."
  - Macha need not implement ECS itself, but define **a set of standardized Fragment/Component schemas** (e.g., `MachaMemoryFragment`, `MachaGoalFragment`), with Unity/Unreal adapters projecting Macha's cognitive state into their respective ECS.

### 2.2 Behavior Tree / Decision Module ↔ Game Engine Common Data Interface

- **Status quo**: Behavior Tree (BT) is the industry-default execution shell (Unreal built-in BT+Blackboard, Unity `com.unity.behavior`, Godot community Beehave). `Blackboard` is a 1:N shared data area, `Tick` evaluates top-down each frame; `Service/Decorator` inject external data. After Macha's `Action` module (§1.2) outputs "structured action intent," the most suitable landing form is **driving a BT leaf node or writing to Blackboard**, with the engine executing `MoveTo`/`PlayAnim`/`UseSmartObject` etc.
- **How Macha adopts / adapts**:
  - Define **`ActionSink` interface** (see `architecture.md` proposal), implementations include: `BehaviorTreeSink` (write Blackboard/trigger BT node), `HTNPlannerSink`, `UtilitySink`, `MCPToolSink`. Cognitive layer only produces `ActionCall`, execution layer handles "how step by step"—strictly fulfilling the Replace/Wrap division.
  - Borrow Unreal **Smart Objects**: abstract "interaction slots in a level dynamically discoverable and usable by NPCs" into Macha's `InteractionSlot` data model, decoupling NPC's "intent → executable interaction."

### 2.3 Unity / Unreal / Godot Plugin Conventions

| Engine | Plugin/extension convention | Adapter landing point |
|---|---|---|
| Unity | Package (`com.unity.*`, with `package.json`, Editor/RT split dirs) + Burst/DOTS | Publish `com.macha.npc` package, containing ECS `IComponentData` projection and BT `Action` node |
| Unreal | Plugin (`.uplugin` + Module) + MassEntity `Trait`/`Processor` | Publish Macha plugin, provide `UMachaBrainComponent` and Mass `Trait`, map Macha cognitive state to Fragment |
| Godot | Addon (GDExtension / editor plugin, 4.x introduced GDExtension C++ binding) | Provide Godot 4 Addon, wrap Macha Agent in `Node`, communicate with scene via `Signal` |

- **How Macha adopts / adapts**: Distribute uniformly as **"engine-agnostic kernel (Python/C#/C++ abstraction) + thin adapter per engine"**, each adapter only does "Macha cognitive state ↔ engine-native structure (Component/Fragment/Node)" projection, avoiding rewriting cognitive logic per engine (this is also the inverse of RAIN's discontinuation lesson: kernel open, adapter community-maintainable).

---

## 3. Open-Source Framework Design Philosophy

### 3.1 LangChain / LlamaIndex — compositional and data-oriented abstraction

- **LangChain / LCEL**: Core abstraction is **`Runnable` protocol** (`invoke`/`batch`/`stream`), using pipe `|` to compose `prompt | model | parser` into a chain; chain is automatically streamable, batchable, traceable. Agent = loop where LLM autonomously selects tools. With LangSmith (trace/eval), LangServe (chain-to-REST).
- **LlamaIndex**: Core abstraction is **`Index`** (vector/tree/knowledge-graph/SQL index) + `QueryEngine` + `Retriever`, focused on "connecting LLM to your own data." Provides 160+ data connectors and retrieval strategies like sub-question decomposition, hybrid retrieval, rerank.
- **How Macha adopts / adapts**:
  - Borrow **LCEL's "everything is Runnable, composition over inheritance"**: Macha's cognitive loop (Perceive→Memory→Reason→Act) should be expressed as a **composable pipeline**, not a hardcoded singleton, for easy swapping of memory backend, swapping of reasoning strategy.
  - Borrow **LlamaIndex's retrieval/index abstraction**: Macha's long-term memory retrieval (vector/graph/temporal) directly reuses its `Retriever` concept and evaluation metrics (Faithfulness / Relevancy).
  - Mind the boundary: LangChain/LlamaIndex are "general LLM application frameworks," **not NPC/game-cognition frameworks**; Macha only borrows their composition and retrieval abstractions, doesn't pull in all their dependencies.

### 3.2 AutoGen / Microsoft Agent Framework / OpenAI Agents — multi-agent abstraction

- **AutoGen (Microsoft, v0.4 rewrite)**: Models Agent as **message-passing Actor** (AssistantAgent / UserProxyAgent), driven by `GroupChatManager` (round-robin or auto-select speaker) or custom orchestrator for multi-Agent dialogue; cross-language (Python/.NET), event-driven async, OpenTelemetry observable.
- **Microsoft Agent Framework (public preview 2025-10, MIT)**: Merges **AutoGen (runtime/multi-Agent patterns)** with **Semantic Kernel (enterprise state/plugin/typed contract)**, with `AIAgent` base class achieving provider-agnostic, supporting **Agent Orchestration (LLM-driven decision)** and **Workflow Orchestration (deterministic business process)** two orchestrations, with **thread as state/reproducible/auditable unit**, can connect Azure AI Foundry / OpenAI / Ollama etc. AutoGen goes maintenance mode, new projects advised to use Agent Framework.
- **OpenAI Agents SDK (2025-03)**: Lightweight code-first framework, core is **Agent + Handoffs (hand conversation ownership to expert Agent, presented to LLM as `transfer_to_x` tool) + agents-as-tools (manager keeps ownership) + Guardrails + Sessions + Tracing**; also supports mounting MCP Server as tool. Judgment principle: **handoff for "expert takes over", as-tool for "manager calls expert for bounded subtask".**
- **How Macha adopts / adapts**:
  - Multi-NPC orchestration uses **handoff / as-tool two modes**: NPC-to-NPC "I hand this to you" uses handoff semantics; "I call the guard NPC to check player's wanted status" uses as-tool semantics. This aligns with §1.3's A2A `Task`/`Agent Card`.
  - Borrow **thread as state unit**: Each NPC's "life thread" in Macha corresponds to a thread (memory/dialogue/relation state), easy to reproduce and audit (echoes `engineering` doc's "debuggable/observable" requirement).
  - Borrow **Agent Framework's AIAgent provider-agnostic interface**: Macha's `Agent` interface downstream can hang OpenAI / local vLLM / Ollama, not locking the model.

### 3.3 Haystack / DSPy — declarative / modular design thought

- **Haystack (deepset, Apache-2.0)**: Enterprise-grade **Pipeline orchestration engine**, composes `Retriever / Reader / Ranker / PromptBuilder / Generator` etc. as **DAG (explicit graph)**; each component independently visible, replaceable, testable; built-in evaluation (EM/F1), REST/Docker deployment, monitoring. Philosophy is "**you control the graph, each component independently debuggable**."
- **DSPy (Stanford, MIT)**: **Declarative "program not prompt"**—treats Prompt and retrieval strategy as **learnable parameters**, using `Signature (input/output contract) + Module + Optimizer (e.g., BootstrapFewShot / MIPROv2)` to automatically optimize the whole pipeline via "compilation"; emphasizes typed signature, automatically tuned by evaluable metrics.
- **How Macha adopts / adapts**:
  - Borrow **Haystack's explicit DAG + replaceable components**: Macha's cognitive kernel internals should be a declarative pipeline, debug panel can view component-by-component "perception → memory hit → reflection → decision", avoiding LangChain-style abstraction hiding errors (echoes GOAP unpredictability lesson).
  - Borrow **DSPy's "contract + auto-optimization"**: Define NPC's "persona/response style" as typed signature, use few labeled samples to auto-optimize prompt and retrieval strategy (e.g., driven by "character consistency" eval metric), reducing hand-written prompt drift.

---

## 4. Model-Access Standards

### 4.1 OpenAI-Compatible API (de-facto standard)

- **What it standardizes**: OpenAI's `/v1/chat/completions`, `/v1/embeddings`, `/v1/models`, `/v1/completions` **JSON request/response shapes** (model + messages + params → choices) have become the LLM-access **de-facto wire format**; streaming uses SSE. Years of tools (OpenAI SDK, LangChain, LlamaIndex, various chat UIs) are hardcoded to this shape.
- **How Macha adopts / adapts**:
  - Macha's `LLMClient` interface (planned in `direction.md`) **takes OpenAI-compatible shape as default contract**: `chat(messages) -> choices`, `embed(texts) -> vectors`. Any local/cloud endpoint exposing `/v1` lets Macha switch without code change (see §4.2).
  - This guarantees Macha's "model-agnostic"—usable with OpenAI/Anthropic (via compatible gateway) or local model, satisfying the open positioning of "privatizable deployment."

### 4.2 Local Service Interfaces (vLLM / llama.cpp / Ollama)

- **Common to all three**: All expose **OpenAI-compatible `/v1`**, differing only in port and load format, not API shape:

| Runtime | Default base_url | Positioning | Key capability |
|---|---|---|---|
| **Ollama** | `http://localhost:11434/v1` | Dev/single-machine/demo | One-click pull, GGUF quant, Apple MLX; default context 2048 (need `OLLAMA_CONTEXT_LENGTH` to enlarge) |
| **llama.cpp** (`llama-server`) | `http://localhost:8080/v1` | Offline/edge/no-GPU | Strongest quant control (GGUF, batched, mmap), from Raspberry Pi to multi-GPU |
| **vLLM** | `http://localhost:8000/v1` | Production/concurrency/team service | PagedAttention + continuous batching, 2–4× throughput; needs CUDA/ROCm; supports AWQ/GPTQ/FP8 |

- **Compatibility spectrum (honest note)**: `/v1/chat/completions`, `/v1/embeddings`, `/v1/models`, SSE streaming, tool/function calling are mostly supported by all three but **with varying strictness** (llama.cpp depends on chat template + `--jinja`; Ollama only valid for models declaring tools; vLLM needs `--enable-auto-tool-choice` + corresponding parser). JSON mode / structured output on all three via GBNF/grammar/guided decoding, strictness lower than original OpenAI. **Macha should not assume local endpoint 100% equivalent to OpenAI; do capability negotiation in `LLMClient`.**
- **How Macha adopts / adapts**: **All client code anchors to OpenAI SDK** (only change `base_url` + `api_key`), "dev with Ollama, production switch to vLLM" is config change not rewrite; tool-call/streaming/embedding code kept as-is. This is exactly Macha's "replaceable, not model-locked" engineering landing.

### 4.3 Quantization / Distillation / Speculative Decoding (deployment options)

- **Quantization**: Lower weight/activation precision to shrink size, speed up. Common: `FP8 / INT4 / GPTQ / AWQ / GGUF-Q4_K_M`; 2025 progress includes ultra-low-bit (2–4bit, some scenarios <1% accuracy loss), adaptive mixed precision (sensitive layers keep high precision), hardware-aware quant (TensorRT-LLM, TPU). Practice: DeepSeek-R1 671B on FP4 inference throughput near 2× of FP8; 4-bit single-machine deployment doubles throughput.
- **Distillation**: Use large model (teacher) to supervise-training small model (student), transferring soft-label/feature/attention/relation knowledge. 2025 progress: multi-teacher distillation, self-distillation, task-specific distillation. Cases: DeepSeek-R1 distilled 32B/70B small models approaching o1-mini; Phi-3 self-distilled; Claude Mini series keep 85%+ capability at 1/10 size.
- **Speculative Decoding**: Use lightweight draft model for multi-step prediction, main model single parallel verification, reducing autoregressive call count, lossless speedup. Variants: **EAGLE (Meta, tree attention + online-distill draft, 1.4–2.0× on Llama4)**, **SubSpec (NeurIPS 2025, low-bit substitute layers, 9–12× on consumer GPU)**, MTP (DeepSeek multi-head prediction, +144% throughput).
- **How Macha adopts / adapts**:
  - Macha doesn't bind to one deployment; but **`LLMClient` must expose "deployment form" as a parameter**: quant level, whether to use speculative decoding, context length. Evaluation phase (Layer 5 of six) measures "latency/cost/character-consistency" trade-off accordingly.
  - For NPC real-time dialogue, **latency is a hard constraint**: suggest Ollama (Q4_K_M) in dev + vLLM (higher precision + speculative decoding) in production, and **must evaluate on deployment precision** (avoid "tuned Q4 on laptop, silently raised precision at launch" causing behavior drift, the trap MatterAI explicitly warns about).

---

## 5. Macha Interface Map (Interface Map)

> Map the four standard categories above to Macha's six-layer kernel (Perception—Memory—Reasoning—Action) + adaptation layer. Principle: **cognitive kernel defines its own standard, external world connects to established de-facto standards.**

| Macha layer / concern | Adopted / aligned standard | Interface shape (Macha-side contract) | Reason (echoes Replace/Wrap) |
|---|---|---|---|
| **Model access** (LLMClient) | **OpenAI-compatible API** (+ vLLM/Ollama/llama.cpp local endpoint) | `chat(messages)->choices`, `embed(texts)->vectors`; capability negotiation | De-facto wire format, guarantees "model-agnostic/privatizable" |
| **Tool call / Action output** | **Anthropic Tool Use / OpenAI Function Calling** shape | `ActionCall{ tool, input_schema, args }` | Unify "semantic action" unit, downstream to BT/MCP/engine |
| **External tools / resources** | **MCP (Model Context Protocol)** | Macha both MCP Server (expose memory/reflection tools) and Client (consume engine tools) | Standardize "Agent↔tool/data", SkyrimNet proved game-feasible |
| **Engine adaptation (execution backend)** | **ECS** (Unity DOTS / Unreal MassEntity) + **behavior-tree execution shell** + each engine's plugin conventions | Standardized Fragment/Component schema (`PersonaState`/`Goal`/`Belief`) + `ActionSink` multi-impl | Wrap: engine AI is "adaptable execution backend" |
| **Multi-NPC collaboration** | **A2A** (Agent Card + Task + SSE); orchestration borrows **OpenAI Agents handoff / as-tool**, **AutoGen/Agent Framework** thread | `AgentCard` capability declaration, `Task` lifecycle, handoff semantics | Wrap: social interaction uses established agent protocol |
| **Rigorous semantics (optional)** | **FIPA ACL** (communicative act + ontology + formal semantics) | Model NPC-to-NPC message with "intent type + shared ontology" | Borrow semantic base, no full implementation |
| **Memory retrieval** | **LlamaIndex Retriever / Haystack Pipeline** abstraction; embeddings use OpenAI-compatible `/v1/embeddings` | `Retriever.retrieve(query)->MemoryItem[]`; declarative DAG | Reuse mature retrieval/eval, don't reinvent wheel |
| **Cognitive-loop composition** | **LangChain LCEL Runnable** composition philosophy; **Haystack** explicit debuggable graph; **DSPy** contract+auto-optimize | `Perceive→Memory→Reason→Act` composable pipeline; typed signature auto-tune | Borrow composition/observability/declarative, kernel self-defines standard |
| **Cognitive kernel (memory/persona/reflection/planning)** | **Macha's own standard** (Replace layer; borrows Inworld components, ACE layering, RimAI module breakdown, but open replaceable) | `MemoryStore` / `PersonaSchema` / `ReflectionLoop` / `Planner` interfaces | Replace: replace fragmented private "brain" |

**One-sentence interface philosophy**:
> Internally Macha defines standard with "composable cognitive pipeline + four minimal interfaces (`Agent` / `MemoryStore` / `PerceptionSource` / `ActionSink`)"; externally, model goes OpenAI-compatible, tool goes MCP, engine goes ECS+BT+plugin, multi-NPC goes A2A. The only part Macha must standardize itself is the upper cognitive kernel "memory/persona/reflection/planning".

---

## 6. Landing Suggestions for Macha's Standard Interface Draft

1. **First freeze "cognitive-kernel minimal interfaces"**: the four types `Agent` / `MemoryStore` / `PerceptionSource` / `ActionSink` (continue `architecture.md`), where `ActionSink` must have BT / HTN / MCP / engine multi-backend implementations, fulfilling "Wrap lower layer."
2. **Converge `Action` into Tool-Use shape**: `ActionCall{ tool, input_schema(JSON Schema), args }` is the sole contract between cognitive layer and all execution layers; this both connects OpenAI/Anthropic and is naturally carried as MCP `tools/call`.
3. **Macha is both MCP Server and MCP Client**: Expose `recall/reflect/remember` etc. tools externally (for editors/external Agents to call), consume engine-side MCP Server internally (inventory/animation/world state).
4. **LLMClient anchors OpenAI-compatible + capability negotiation**: Don't assume local endpoint equals OpenAI; expose quant level, speculative decoding, context length as configurable params, and measure latency/cost/consistency trade-off in evaluation phase.
5. **Multi-NPC uses A2A (drop ACP single line)**: Use `Agent Card` to declare each NPC's capability, `Task` to manage collaboration lifecycle; model NPC-to-NPC messages with FIPA-style "intent type + shared ontology" to ensure reasonability and auditability.
6. **Observability/debuggability first**: Borrow Haystack explicit DAG and LangSmith/OpenTelemetry, build-in panel for "memory flow / decision chain / persona state / tool calls", avoid repeating GOAP's "unpredictable, hard-to-QA" mistake (echoes `engineering` doc §6).
7. **Open governance, avoid RAIN-style discontinuation**: Kernel MIT/Apache open-source, engine adapters community-maintainable, clear version and compat strategy.

---

## 7. Source Collection

> Format follows `information_needs.md` conventions. All URLs from this session's actual WebSearch/WebFetch hits; those not stably verified are explicitly marked "no stable link found," not fabricated.

---

[Category]Engineering implementation (interop protocol)
[Title]Model Context Protocol Specification (2025-11-25, latest)
[Link]https://modelcontextprotocol.io/specification/2025-11-25
[One-line summary]Open protocol led by Anthropic, uses JSON-RPC 2.0 to standardize "single Agent's internal LLM ↔ external Tools/Resources/Prompts" connection; 2025-11-25 version adds Tasks (async), Extensions, enterprise OAuth.
[Key conclusions]
1. Transport stdio + Streamable HTTP, messages JSON-RPC 2.0.
2. Core primitives: tools/list, tools/call, resources/read, prompts/get, sampling, elicitation, roots, completion, logging.
3. 2025-11-25 version introduces Tasks (call-now/fetch-later async) and Extensions framework.
4. Multi-language SDK, already de-facto standard for "Agent↔tool/data".
[Reusable]Macha both MCP Server (expose memory/reflection tools) and Client (consume engine tools) protocol shape; Tasks can model "long-term-memory reminder".

[Category]Engineering implementation (interop protocol)
[Title]MCP Architecture (official architecture doc)
[Link]https://modelcontextprotocol.io/docs/learn/architecture
[One-line summary]Explains MCP's Host/Client/Server roles and lifecycle, the base for understanding "how Macha is both Server and Client".
[Key conclusions]
1. Host hosts multiple Clients, each Client connects one Server.
2. Server provides tools/resources/prompts, Client calls via standardized requests.
3. sampling lets Server call back Client's LLM.
[Reusable]Macha dual-role (Server+Client) topology diagram.

[Category]Engineering implementation (interop protocol)
[Title]Anthropic Tool Use with Claude (official docs)
[Link]https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview
[One-line summary]Anthropic tool-call shape: tools use name/description/input_schema, return tool_use block in content (.input is dict), judged by stop_reason=="tool_use"; supports strict and server tools.
[Key conclusions]
1. Differs from OpenAI: input_schema not parameters, no function wrapper, result in role:user + tool_result block.
2. Supports client tools (self-exec) and server tools (Anthropic-hosted exec).
3. strict:true guarantees params strictly conform to schema.
[Reusable]Macha `ActionCall` tool-shape definition; dual-vendor tool-call compat plan.

[Category]Engineering implementation (interop protocol)
[Title]OpenAI Function Calling (official guide)
[Link]https://platform.openai.com/docs/guides/function-calling
[One-line summary]OpenAI function-call shape: tools:[{type:function, function:{name,description,parameters(JSON Schema)}}], returns tool_calls (arguments JSON string); supports strict/parallel/tool_search.
[Key conclusions]
1. strict:true (Structured Outputs) guarantees params strictly match schema.
2. Supports parallel calls, tool_choice control, pydantic/zod auto-gen schema.
3. Unified into Responses API and Agents SDK.
[Reusable]Field-mapping table aligning with Anthropic tool calls; Macha ActionSink JSON Schema constraint.

[Category]Academic paper/standard (multi-agent communication)
[Title]FIPA ACL Specification (OC00003A, communicative acts)
[Link]https://www.fipa.org/specs/fipa00003/OC00003A
[One-line summary]Agent Communication Language based on speech-act theory, defines 22 communicative acts and message structure (:sender/:receiver/:content/:language(FIPA-SL)/:ontology/:protocol/:conversation-id), gives formal semantics via BDI modal logic.
[Key conclusions]
1. Each communicative act has narrative + formal semantics (feasibility precondition + rational effect).
2. Minimal compliance: must reply not-understood to unprocessable message.
3. Comes with interaction protocols (FIPA-Request / Contract-Net) and Agent management platform (AMS/DF/MTS).
[Reusable]NPC-to-NPC "intent type + shared ontology" modeling; ontology field maps to Macha relation/world-knowledge schema.

[Category]Academic paper/standard (multi-agent communication)
[Title]History of FIPA ACL (official history doc)
[Link]http://fipa.org/subgroups/ROFS-SG-docs/History-of-FIPA.htm
[One-line summary]FIPA ACL from 1997 based on ARCOL, standardized 2002; based on speech-act theory, 22 message types, content language FIPA-SL/KIF/RDF.
[Key conclusions]
1. Standardized ACL after KQML, goal cross-Agent knowledge-level communication.
2. Defines Agent Platform, AMS, DF, Message Transport complete system.
3. Now maintained by IEEE.
[Reusable]"Agent platform" layered reference; message-envelope/transport decoupling idea.

[Category]Engineering implementation/industry report (multi-agent communication)
[Title]What is the Agent2Agent (A2A) Protocol? (IBM explainer)
[Link]https://www.ibm.com/think/topics/agent2agent-protocol
[One-line summary]Open Agent↔Agent protocol launched by Google 2025-04, now under Linux Foundation; complements MCP (MCP connects tools, A2A connects Agents). Core: Agent Card, Task, Message/Artifact/Part, transport HTTP+JSON-RPC 2.0+SSE.
[Key conclusions]
1. Agent Card (.well-known/agent.json) for capability discovery; Task has submitted→working→input-required→completed/failed state machine.
2. Part supports Text/File/Data multimodal; SSE streaming.
3. Auth aligns OpenAPI (OAuth2/OIDC), built-in OpenTelemetry observability.
[Reusable]Macha multi-NPC collaboration discovery/task-lifecycle model; layered division diagram with MCP.

[Category]Engineering implementation/industry report (multi-agent communication)
[Title]What You Need to Know About Agent2Agent Protocol (Snyk)
[Link]https://snyk.io/articles/what-you-need-to-know-about-agent2agent-protocol
[One-line summary]Details A2A's client-server interaction model, Agent Card digital identity, Task state machine, rich-communication primitives, and security/long-task/multimodal principles.
[Key conclusions]
1. Single Agent can be both client and server in different interactions, supports mesh topology.
2. Built-in observability (trace ID + OTLP structured log).
3. Design principles: based on existing web standards, secure-by-default, supports long tasks, modality-agnostic.
[Reusable]A2A security/observability design for Macha NPC collaboration (audit, trace).

[Category]Engineering implementation (multi-agent communication)
[Title]Agent Communication Protocol (ACP) — IBM Research blog
[Link]https://research.ibm.com/blog/agent-communication-protocol-ai
[One-line summary]REST-style Agent↔Agent protocol by IBM BeeAI 2025-03, goal "HTTP for Agent communication"; complements MCP (ACP connects Agent, MCP connects tool).
[Key conclusions]
1. REST + JSON + OAuth2/API Key, Agent carries manifest for offline discovery.
2. Supports peer-to-peer decentralized interaction (not only manager mode).
3. Important status: from 2025-08 ACP merged into A2A, under Linux Foundation, BeeAI now runs on A2A.
[Reusable]"REST-first / build-time manifest" idea (only as A2A design reference); Macha new system should anchor only A2A.

[Category]Engineering implementation (multi-agent communication)
[Title]MCP and A2A — Agent Communication Protocol (ACP official compare page)
[Link]https://agentcommunicationprotocol.dev/about/mcp-and-a2a
[One-line summary]Clarifies MCP (Agent↔tool), A2A (Agent↔Agent, Google), ACP (Agent↔Agent, IBM) three-layer division and relations.
[Key conclusions]
1. MCP solves single-Agent "model connects tool/resource", A2A/ACP solve Agent-to-Agent.
2. ACP advantage: Linux Foundation open governance, REST communication, offline Agent discovery, MIME message extensible.
3. A2A and ACP overlap in goal, unified into A2A.
[Reusable]Macha adaptation layer "MCP + A2A dual-protocol" layered picture.

[Category]Engineering implementation (game-industry standard)
[Title]Unity Entities package (DOTS / ECS official docs)
[Link]https://docs.unity3d.com/Packages/com.unity.entities@latest/
[One-line summary]Unity's ECS in Data-Oriented Technology Stack: Entity + IComponentData (data) + System (logic) + EntityManager; GameObject converted to ECS via Baking; with Graphics/Physics/Netcode.
[Key conclusions]
1. Core is data-oriented, with Burst/Job for performance.
2. Provides ConvertToEntity / SubScene / IConvertGameObjectToEntity conversion workflow.
3. Suited for large-scale entities (Megacity demo supports 64+ players).
[Reusable]Macha projects cognitive state to Unity `IComponentData` adapter pattern.

[Category]Engineering implementation (game-industry standard)
[Title]Unreal Engine MassEntity Overview (official docs)
[Link]https://docs.unrealengine.com/5.3/de/overview-of-mass-entity-in-unreal-engine
[One-line summary]UE5's archetype-based ECS: Fragment (=Component, pure data), Processor (=System, stateless, EntityQuery batch), Archetype, Chunk, Tag, Trait; from UE5.5 merged into core engine.
[Key conclusions]
1. Fragment stores only data, Processor batches via EntityQuery, laid out by Archetype/Chunk to squeeze cache.
2. Trait is "Fragment+Processor" functional set, declarable/inheritable in MassEntityConfig asset.
3. MassSimulation subsystem manages per-frame cycle; supports combination with StateTree/navigation.
[Reusable]Macha cognitive state → Unreal `Fragment` projection schema; Trait as "persona/goal" functional set.

[Category]Engineering implementation (game-industry standard)
[Title]Unreal Smart Objects Overview (official docs)
[Link]https://dev.epicgames.com/documentation/en-us/unreal-engine/smart-objects-in-unreal-engine---overview
[One-line summary]UE's "activity collection in level usable via reservation system", provides data only no execution logic, globally managed by Subsystem, spatially partitioned index, queried by Gameplay Tag.
[Key conclusions]
1. Definition includes Activity Tags / Slots / Behavior Definition.
2. Agent searches → claims Slot → executes own logic.
3. Lets background NPC dynamically discover and interact without per-object hardcoding.
[Reusable]Macha `InteractionSlot` ("discoverable interaction slot") abstraction, decouples "intent ↔ executable interaction".

[Category]Engineering implementation (open-source framework design)
[Title]LangChain (framework overview and LCEL)
[Link]https://ai-hub.emersonbraun.dev/docs/tools/langchain
[One-line summary]LangChain centers on "composition and orchestration": LLM/prompt/parser/retriever/tool modular, LCEL composes with `|` into streamable/batchable/traceable chain; Agent is loop where LLM autonomously selects tools; LangSmith provides trace/eval.
[Key conclusions]
1. Core abstraction Runnable (invoke/batch/stream), pipeline composition.
2. Agent = reasoning loop (select tool → execute → feed back → continue).
3. Wide ecosystem but many abstraction layers, overhead in simple scenarios.
[Reusable]Macha cognitive loop "everything composable Runnable" pipeline philosophy; avoid abstraction hiding errors.

[Category]Engineering implementation (open-source framework design)
[Title]LlamaIndex vs LangChain (2026 comparison)
[Link]http://ai-tldr.dev/learn/agent-frameworks/orchestration-frameworks/llamaindex-vs-langchain
[One-line summary]LlamaIndex core is Index + QueryEngine + Retriever, focused on "connect LLM to your own data" (160+ connectors, sub-question decomposition, hybrid retrieval, rerank); LangChain core is control flow and tool chain (LCEL + LangGraph).
[Key conclusions]
1. LlamaIndex retrieval strategy built-in and advanced (hybrid / sub-question / auto-merge).
2. LangChain 1.0 (2025-10) Agents run on LangGraph (explicit state + conditional edge + human-in-the-loop).
3. Best practice: low-level retrieval uses LlamaIndex wrapped as Tool, handed to LangChain Agent to schedule.
[Reusable]Macha memory retrieval reuses LlamaIndex Retriever abstraction; Agent scheduling borrows LangGraph state graph.

[Category]Engineering implementation (open-source framework design)
[Title]Multi-Agent Frameworks: AutoGen, CrewAI, OpenAI Agents SDK (study plan ch.8)
[Link]https://pixelbank.dev/agent-study-plan/chapter/8
[One-line summary]2025 mainstream multi-Agent framework review: AutoGen's Actor model (message-passing Agent), OpenAI Agents SDK's handoffs, Claude Agent SDK's subagents, Agno/Mastra runtime.
[Key conclusions]
1. AutoGen v0.4 rewritten as async Actor, each Agent has memory/tool/LLM, GroupChatManager selects speaker.
2. OpenAI Agents SDK lightweight, handoffs/guardrails/sessions first-class.
3. Framework selection matrix matches by state/streaming/subagents/vendor constraints.
[Reusable]Macha multi-NPC orchestration "Actor + handoff" abstraction.

[Category]Engineering implementation (open-source framework design)
[Title]Microsoft Unveils Agent Framework (AutoGen + Semantic Kernel merge)
[Link]https://kiadev.net/news/2025-10-03-microsoft-agent-framework-multi-agent-orchestration
[One-line summary]Microsoft's Oct 2025 public-preview open-source SDK/runtime, merges AutoGen (multi-Agent runtime) and Semantic Kernel (enterprise state/plugin/typed contract); `AIAgent` base class provider-agnostic, supports Agent/Workflow two orchestrations, thread as state unit.
[Key conclusions]
1. Two orchestrations: Agent Orchestration (LLM-driven) + Workflow Orchestration (deterministic flow).
2. Thread as unit for reproducible/retry/audit.
3. Supports Azure OpenAI / OpenAI / Ollama / GitHub Models, new projects advised Agent Framework (AutoGen maintenance).
[Reusable]Macha `Agent` interface provider-agnostic design; thread as NPC "life state" unit.

[Category]Engineering implementation (open-source framework design)
[Title]OpenAI Agents SDK — Orchestration and Handoffs (official)
[Link]https://developers.openai.com/api/docs/guides/agents/orchestration
[One-line summary]OpenAI Agents SDK's core orchestration: Handoffs (expert takes over conversation, presented to LLM as transfer_to_x tool) and agents-as-tools (manager keeps ownership calling expert for bounded subtask).
[Key conclusions]
1. handoff for "expert should own next segment", as-tool for "manager synthesizes final answer".
2. Each specialist should have narrow responsibility, specific handoffDescription.
3. Over-early agent split increases prompt/trace/approval surface.
[Reusable]Macha multi-NPC "takeover vs call" two collaboration semantics; handoffDescription maps NPC capability description.

[Category]Engineering implementation (open-source framework design)
[Title]OpenAI Agents SDK overview (official platform page)
[Link]https://openai.com/agent-platform/
[One-line summary]Agents SDK vs Responses API positioning: SDK manages agent loop and multi-Agent orchestration (handoffs, sessions, guardrails, tracing, MCP mount); Responses API lets you self-manage loop.
[Key conclusions]
1. Agents SDK built-in sessions, tracing, guardrails, resumable approval flow.
2. Tools include platform tools, function calling, remote MCP, agents-as-tools.
3. Suited for "server owns deployment/tool/state" code-first scenarios.
[Reusable]Macha mounts MCP Server as tool on NPC Agent runtime pattern.

[Category]Engineering implementation (open-source framework design)
[Title]Haystack vs DSPy (framework comparison)
[Link]https://zairalabs.ai/guide/compare/dspy-vs-haystack
[One-line summary]Haystack (deepset, Apache-2.0) is enterprise explicit Pipeline (DAG) orchestration, components independently replaceable/testable; DSPy (Stanford, MIT) is declarative "program not prompt", treats prompt/retrieval as learnable params auto-optimized by compiler.
[Key conclusions]
1. Haystack philosophy: "you control the graph, each component visible/testable"; suited for stage-by-stage control retrieval/embed/route RAG.
2. DSPy philosophy: "framework controls optimization, prompt changes via learning"; needs evaluable output and labeled samples.
3. Both self-hosted, open-source.
[Reusable]Macha cognitive loop uses Haystack-style explicit debuggable graph; persona/response style uses DSPy-style typed signature auto-optimize.

[Category]Engineering implementation (open-source framework design)
[Title]Haystack vs DSPy: different paradigm (official example)
[Link]https://theneuralbase.com/haystack/learn/advanced/vs-dspy-different-paradigm
[One-line summary]Same RAG example compared: Haystack explicitly adds components and connects edges (you control graph), DSPy writes high-level forward letting framework compile-optimize (framework controls optimization).
[Key conclusions]
1. Haystack component graph explicit, independently debuggable, swap impl without retrain.
2. DSPy behavior changes via training data + optimizer, not manual prompt edit.
3. Production Haystack explicit method more controllable/debuggable.
[Reusable]Macha debug panel "component-by-component view perception→memory→reflection→decision" design basis.

[Category]Engineering implementation (model-access standard)
[Title]OpenAI-Compatible Local LLM Endpoints (Ollama / vLLM / llama.cpp)
[Link]https://inventivehq.com/blog/openai-compatible-endpoint-for-local-llm
[One-line summary]All mainstream local runtimes expose OpenAI-compatible `/v1`, differ only in port and load format; app only changes base_url to switch from cloud to local hardware, streaming/tool/embeddings usable as-is.
[Key conclusions]
1. Ports: Ollama 11434, llama.cpp 8080, vLLM 8000, all under `/v1`.
2. Local auth is formal (placeholder api_key enough), external exposure needs real auth.
3. Ollama default context 2048 silently truncates long prompts, need `OLLAMA_CONTEXT_LENGTH`.
[Reusable]Macha `LLMClient` only changes base_url to switch model deployment strategy.

[Category]Engineering implementation (model-access standard)
[Title]Ollama vs vLLM vs llama.cpp: Choosing the Right Local LLM Runtime (MatterAI)
[Link]https://www.matterai.so/guides/ollama-vs-vllm-vs-llamacpp-runtime-comparison
[One-line summary]All three speak same OpenAI protocol, so swap is config not rewrite; typical path: laptop Ollama prototype → real traffic switch vLLM (same precision higher); warns "tuned Q4 on laptop, silently raised precision at launch" behavior-drift trap.
[Key conclusions]
1. Ollama: zero-config, GGUF, Apple MLX; llama.cpp: offline/edge/no-GPU; vLLM: concurrency/latency SLA/batching.
2. Since all speak OpenAI shape, client code (prompt/tool/streaming/embedding) migrates zero-change.
3. Must evaluate on deployment precision, not laptop quant precision.
[Reusable]Macha dev→production runtime migration path; precision-consistency eval principle.

[Category]Engineering implementation (model-access standard)
[Title]OpenAI API Compatibility Matrix (wideareaai)
[Link]https://wideareaai.com/tools/openai-compatibility-matrix
[One-line summary]Quantitatively compares llama.cpp / Ollama / vLLM compatibility with OpenAI endpoints/features (chat/embeddings/streaming/tool-calling/JSON-mode/vision…), conclusion "compatibility is spectrum not checkbox".
[Key conclusions]
1. chat/completions, embeddings, models, SSE basically all supported.
2. tool-calling depends on model chat template, three vary in strictness (llama.cpp needs --jinja; Ollama limits to models declaring tools; vLLM needs --enable-auto-tool-choice).
3. JSON/structured output via GBNF/grammar/guided decoding, strictness lower than original OpenAI.
[Reusable]Macha `LLMClient` must do "capability negotiation", not assume local endpoint 100% equals OpenAI.

[Category]Engineering implementation (deployment/compression)
[Title]Large-Model Optimization and Compression Techniques: 2025 Practice and Breakthrough (Aliyun dev community)
[Link]https://developer.aliyun.com/article/1683981
[One-line summary]Systematically reviews 2025 quantization/pruning/distillation/low-rank four compression techniques, and hardware synergy (Blackwell/TPU/HBM3e) and software optimization (TensorRT-LLM/TVM/parallel strategy/KV cache/speculative exec).
[Key conclusions]
1. Quantization: ultra-low-bit (2–4bit, some <1% loss), adaptive mixed precision, hardware-aware, differentiable quant.
2. Distillation: multi-teacher/self-distill/task-specific distill, cases include Claude Mini, Phi-3, Qwen-M.
3. Speculative decoding, dynamic batching, KV-cache reuse are inference-speedup keys.
[Reusable]Macha deployment-option list (quant level/distill/speculative decode) as `LLMClient` configurable params.

[Category]Academic paper (inference speedup)
[Title]SubSpec: Lossless and Training-Free Acceleration for Offloaded LLMs via Substitute Speculative Decoding (NeurIPS 2025)
[Link]https://abdelfattah-lab.github.io/pubs/speculate_deep_and
[One-line summary]Uses target LLM low-bit substitute layers to build high-alignment draft model, lossless training-free speculative decoding, consumer GPU Qwen2.5 7B/32B reaches 9.1×/12.5× speedup.
[Key conclusions]
1. Speculative decoding = lightweight draft multi-step predict + main model single parallel verify, reduces autoregressive calls.
2. SubSpec shares GPU resident layers and KV-Cache, further lowers memory and improves alignment.
3. Lossless and training-free, suited for resource-constrained deployment.
[Reusable]Macha local NPC inference latency optimization optional scheme (esp. consumer GPU).

---

## 8. Sources With No Stable Public Link Found (honest marking, not fabricated)

- **Unity `com.unity.behavior` (new visual BT package) manual deep link**: Mentioned in Unity docs and ML-Agents manual, but its manual deep link not separately obtained this time; advised to complete with Unity official Package docs (BT as Macha `ActionSink` execution shell's Unity implementation can reference it).
- **Godot official BT/Utility module**: Godot 4 still has no official advanced AI module, relies on community Beehave (`github.com/bitbrain/beehave`) and self-build; §2.3's Godot adapter suggestion based on GDExtension Addon form, specific API per Godot 4.x official extension docs.
- **EAGLE speculative-decoding original paper (arxiv 2508.08192)**: Search hit Sina news report on it (with Llama4 1.4–2.0×, INT4 quant draft data), but original arxiv link not directly verified this search; team advised to re-verify first-hand paper with arxiv number 2508.08192.
- **Microsoft Agent Framework official GitHub repo deep link**: This doc uses kiadev.net / ai-trends.today launch reports (both point to MIT license, Python/.NET, merges AutoGen+Semantic Kernel); for precise API use Microsoft official repo and docs to re-verify.

> For precise citation of the above, team advised to re-verify with official/first-hand sources later; no URL fabricated for them in this document.

---

## 9. Deepening Supplement: Interface Draft and Domestic Compatibility (2025–2026)

> This chapter is "additive deepening": changes no conclusion in §1–§8, only adds four new contents under the original framework (Macha six-layer kernel → de-facto-standard adaptation layer)—(1) 2025–2026 standard timeliness updates; (2) four concrete interface drafts; (3) domestic large-model API compatibility special; (4) quantification and landing budget. New sources strictly in §7's six-field format in §9.5.
>
> Unified premise (consistent with §0): **Macha only self-defines cognitive-kernel standard (memory/persona/reflection/planning), externally always connects to established de-facto standards**—model goes OpenAI-compatible, tool goes MCP, engine goes ECS+BT, multi-NPC goes A2A. The four drafts in this chapter are exactly the "minimal landable contract" of that premise.

### 9.1 Breadth + Timeliness: 2025–2026 Standard / Protocol Updates

#### 9.1.1 MCP: From 2025-11-25 experimental to 2026-07-28 official

- **Timeline (per official changelog and anniversary blog)**:
  - **2025-11-25 (v1 anniversary)**: Introduced experimental `Tasks` (long async, `working/input_required/completed/failed/cancelled` five states), `Extensions` framework, OAuth Client ID Metadata Documents (CIMD, replacing DCR), `Sampling with Tools` (SEP-1577), enterprise OAuth (Cross App Access / client credentials).
  - **2025-12-09**: Anthropic donated MCP to **Linux Foundation's Agentic AI Foundation** (OpenAI co-initator, Google/Microsoft/AWS/Cloudflare/Bloomberg supporters)—cross-vendor governance formally landed, reducing single-company lock-in risk.
  - **2026-07-28 (official, RC locked 2026-05-21)**: Breaking changes vs 2025-11-25, direction "stateless + extensions externalized".
- **Changes with biggest impact on Macha**:
  1. **Removed protocol-level session and `Mcp-Session-Id`, to stateless**: each request carries `protocolVersion` and `clientCapabilities` in `_meta`, version mismatch returns `UnsupportedProtocolVersionError`; added `server/discover` RPC for upfront version negotiation. → Macha's MCP client/server must upgrade to "self-describing per request" model, no longer rely on long-connection session.
  2. **`Tasks` moved out of core, becomes official extension** `io.modelcontextprotocol/tasks`: reworked to polling `tasks/get` + `tasks/update` (client feeds input back), removed `tasks/list`; server can actively return task handle. → Macha's "NPC proactively brings up three days later" long-term-memory reminder should be modeled as this extension not core primitive.
  3. **Tool `inputSchema` promoted to full JSON Schema 2020-12** (supports `oneOf/anyOf/allOf/$ref/$defs`); `structuredContent` can be arbitrary JSON. → Macha's `ActionCall` param schema can directly use 2020-12 to express complex nesting.
  4. **`Roots` / `Sampling` / `Logging` enter deprecation cycle** (annotated deprecation, at least 12-month removal window); `subscriptions/listen` replaces `resources/subscribe`; results add `resultType` (`complete` / `input_required`), and introduce **Multi Round-Trip Requests (MRTR)** pattern replacing server active request. → Macha, if using server-side sampling, needs migration path reserved.
  5. **`CacheableResult` (`ttlMs` / `cacheScope`)**: `tools/list` etc. results can declare cache freshness. → Macha-exposed MCP tool list should be stably ordered to support client cache and prompt-cache hit.

#### 9.1.2 A2A: v1.0 stable + Linux Foundation Agentic AI Foundation

- **2026-04-09 (one-year milestone, per Linux Foundation press)**: A2A reached **v1.0 stable**, 150+ orgs in production (not pilot), GitHub 22K+ stars, SDK covers Python/JS/Java/Go/.NET five languages; natively integrated into **Microsoft Copilot Studio / Azure AI Foundry / Amazon Bedrock AgentCore**.
- **Signed Agent Cards**: Cryptographic signature for cross-vendor identity check (domain-level trust), replacing early plaintext Agent Card. → In Macha multi-NPC collaboration, each NPC's `Agent Card` should carry signature, avoid "fake NPC" injection.
- **Agent Payments Protocol (AP2)** shipped simultaneously (60+ payment/finance orgs support), extends A2A from "communication" to "auditable economic coordination". → For Macha it's optional capability of "inter-NPC transaction/task reward", not required.
- **Governance attribution**: A2A and MCP both under **Linux Foundation Agentic AI Foundation**, complementary (MCP=Agent↔tool, A2A=Agent↔Agent) forming multi-agent interop base layer. → Macha adaptation layer "MCP + A2A dual-protocol" layered picture (§1.3) gets foundation-level backing, firming the judgment to anchor only A2A, drop ACP single line.

#### 9.1.3 Anthropic / OpenAI Tool Use latest

- **OpenAI Responses API natively supports MCP**: `tools` can directly put `{ "type": "mcp", "server_protocol": "sse", "server_url": "...", "server_label": "..." }`, model-side drives MCP tool call (Qwen Bailian doc gives official example of this usage, see §9.5). → Macha's `ActionSink` can add "declare MCP Server as OpenAI tool" zero-code bridge mode.
- **strict mode adoption**: OpenAI (`strict:true` Structured Outputs) and Anthropic (`strict:true`) and DeepSeek/Kimi all support params strictly conforming to schema; Kimi's strict default on (follows MFJS subset). → Macha `ActionCall` default strict on, guarantees downstream BT/engine get legal params.
- **Sampling with Tools (MCP SEP-1577)**: MCP Server can declare tool-selection behavior in sampling request, letting Server deploy internal agent under client token. → Naturally fits Macha's "both Server and Client" dual role (§1.1).

#### 9.1.4 ECS new practice (Unity 6 DOTS / Unreal MassEntity 5.5+)

- **Unity 6 DOTS best practice** (synthesizing official and community 2024–2025): prefer `ISystem` (Burst-compatible), use `EntityCommandBuffer` to batch structure changes, use **Tag component + enable/disable** instead of frequent create/destroy entities, shared component for grouping, use Profiler's DOTS analyzer to monitor Chunk utilization. Applicable scenarios explicitly include **NPC crowds, AI decision**.
- **Unreal MassEntity 5.5+**: Merged into core engine, `Fragment` (pure data) + `Processor` (stateless, `EntityQuery` batch) + `Trait` (Fragment+Processor functional set) pattern mature, can combine with StateTree/navigation.
- **Impact on Macha**: §2.1's "cognitive state projected to standardized Fragment/Component" conclusion unchanged, but landing constraints clearer—`NPCBrainComponent` (§9.2.3) should be **fine-grained, enable/disable-able, no per-frame allocation** data block; inference doesn't run LLM in ECS tick, only does "state projection + cooldown judgment" in tick, async the LLM call (echoes §4.3 latency hard constraint).

### 9.2 Technical-Spec Depth: Four Concrete Interface Drafts

> Following §0 philosophy: **cognitive layer only produces "semantic action/state", execution-layer backends land themselves**. The four drafts correspond to Macha adaptation layer's four standard channels (MCP / OpenAI-compatible / ECS / A2A).

#### 9.2.1 (a) MCP Server for NPC —— tools: `speak` / `act` / `remember` / `observe`

Macha exposes "single NPC's cognitive capability" as an MCP Server (Host=game/editor, Client=engine or external Agent). `list_tools` returns four tools, input schema uses JSON Schema 2020-12:

```json
{
  "tools": [
    {
      "name": "speak",
      "description": "NPC speaks a line to a target character (player/other NPC).",
      "inputSchema": {
        "type": "object",
        "properties": {
          "utterance": { "type": "string", "description": "Natural-language text to be spoken" },
          "tone": { "type": "string", "enum": ["neutral", "friendly", "angry", "fearful", "suspicious"] },
          "target": { "type": "string", "description": "Receiver entity ID, defaults to current dialogue player" }
        },
        "required": ["utterance"]
      }
    },
    {
      "name": "act",
      "description": "NPC performs an embodied action intent (move/use item/interact).",
      "inputSchema": {
        "type": "object",
        "properties": {
          "action": { "type": "string", "description": "Action type or semantic tag, e.g. 'move_to' / 'use_item' / 'patrol'" },
          "params": { "type": "object", "description": "Action parameters (coordinates/item ID etc.)" },
          "priority": { "type": "string", "enum": ["low", "normal", "high", "critical"] },
          "blocking": { "type": "boolean", "description": "Whether to block until action completes" }
        },
        "required": ["action"]
      }
    },
    {
      "name": "remember",
      "description": "Write an experience/fact/relation/emotion into NPC long-term memory.",
      "inputSchema": {
        "type": "object",
        "properties": {
          "content": { "type": "string", "description": "Memory content" },
          "type": { "type": "string", "enum": ["event", "fact", "relationship", "emotion"] },
          "importance": { "type": "number", "minimum": 0, "maximum": 1, "description": "Memory importance 0..1" },
          "related_entities": { "type": "array", "items": { "type": "string" }, "description": "Related entity ID list" },
          "source": { "type": "string", "enum": ["observed", "told", "inferred"] }
        },
        "required": ["content", "type"]
      }
    },
    {
      "name": "observe",
      "description": "Query world state/other entity, return NPC's currently observable info.",
      "inputSchema": {
        "type": "object",
        "properties": {
          "entity_or_location": { "type": "string", "description": "Entity ID or location" },
          "query": { "type": "string", "description": "Property or event of interest" },
          "radius": { "type": "number", "description": "Observation radius in meters" },
          "include_entities": { "type": "boolean", "description": "Whether to return entity list in range" }
        },
        "required": ["entity_or_location"]
      }
    }
  ]
}
```

`tools/call` return (structured result): `speak → {delivered:bool, utterance_id:str}`; `act → {task_id:str, accepted:bool, estimated_ms:int}`; `remember → {memory_id:str, stored:bool}`; `observe → {observations:[...], observed_at:str}`. Macha can also consume engine-side MCP Server (inventory/animation/world state), fulfilling §1.1 dual role. Long-running task (e.g., "proactively bring up three days later") goes through `io.modelcontextprotocol/tasks` extension's polling handle.

#### 9.2.2 (b) OpenAI-compatible Function Schema for NPC action

When Macha kernel produces a "semantic action" to directly send to any OpenAI-compatible endpoint (OpenAI / Qwen / Zhipu / DeepSeek / Kimi / local vLLM), use the following function definition (fully isomorphic to §1.2's `ActionCall`, strict default on):

```json
{
  "type": "function",
  "function": {
    "name": "npc_perform_action",
    "description": "Structured action intent produced by NPC cognitive kernel, for behavior tree/engine to execute.",
    "strict": true,
    "parameters": {
      "type": "object",
      "properties": {
        "action_type": { "type": "string", "enum": ["speak", "move", "use_item", "emote", "interact"] },
        "target": { "type": "string", "description": "Target entity ID (player/NPC/item), can be empty" },
        "content": { "type": "string", "description": "Text or expression name for speak/emote" },
        "location": {
          "type": "object",
          "properties": { "x": { "type": "number" }, "y": { "type": "number" }, "z": { "type": "number" } },
          "required": ["x", "y", "z"], "additionalProperties": false
        },
        "item_id": { "type": "string", "description": "Item ID for use_item" },
        "priority": { "type": "string", "enum": ["low", "normal", "high", "critical"] },
        "provenance": { "type": "string", "description": "Source mark: memory / reasoning / reflection" }
      },
      "required": ["action_type", "priority", "provenance"],
      "additionalProperties": false
    }
  }
}
```

Model returns `tool_calls[].function.arguments` (JSON string) → Macha parses to `ActionCall` → routes to `ActionSink` (BT / HTN / Utility / MCPTool). This schema one-to-one maps to (a)'s `act`/`speak` field set, guaranteeing OpenAI-compatible channel and MCP channel interop.

#### 9.2.3 (c) ECS Component definition: `NPCBrainComponent`

Macha doesn't implement ECS, only defines **standardized data-block schema**, projected by each engine adapter into Unity `IComponentData` or Unreal `Fragment`. Key constraints (from §9.1.4): fine-grained, enable/disable-able, no LLM in tick.

**Unity DOTS (`IComponentData`)**:

```csharp
public struct NPCBrainComponent : IComponentData
{
    public FixedString64Bytes  PersonaId;          // Persona/character template ID
    public NPCGoal              CurrentGoal;        // Current goal (enum + intensity)
    public EmotionState         Emotion;            // Emotion state (enum + intensity 0..1)
    public Entity               MemoryHandle;       // Reference to Macha memory entity
    public Entity               AttentionTarget;    // Current attention object (Entity.Null = none)
    public DialogueState        Dialogue;           // Dialogue state machine
    public uint                 LastReasoningTick;  // Last reasoning frame/tick
    public float                ReasoningCooldown;  // Reasoning cooldown (seconds)
    public FixedString128Bytes  ThreadId;           // Corresponding Agent Framework thread
    public int                  RelationshipVersion;// Relation table version (dirty check)
    public byte                 Disabled;           // 0/1 enable control, avoid create/destroy
}
```

**Unreal MassEntity (`FMassFragment` equivalent)**:

```cpp
USTRUCT()
struct FMachaBrainFragment : public FMassFragment
{
    GENERATED_BODY()
    FName              PersonaId;
    EMachaGoal         CurrentGoal;
    FMachaEmotion      Emotion;
    FMassEntityHandle  MemoryHandle;
    FMassEntityHandle  AttentionTarget;
    EMachaDialogueState Dialogue;
    uint32             LastReasoningTick;
    float              ReasoningCooldown;
    FString            ThreadId;
    int32              RelationshipVersion;
};
```

> Short-term observation queue suggested via separate `NPCObservationBuffer` (dynamic buffer / `TArray<FMachaObservation>`), separated from brain state, avoid per-frame expansion. This Component only holds "projected cognitive snapshot", real reasoning done asynchronously in Macha process, result written back to memory entity pointed by `MemoryHandle`.

#### 9.2.4 (d) A2A multi-NPC message schema: sender / receiver / intent / payload

Multi-NPC social interaction uses A2A `Message` + FIPA-style intent type (§1.3). Message envelope as follows (based on A2A `Part` multimodal and Signed Agent Card idea, trimmed for NPC scenario):

```json
{
  "message_id": "msg_8f3a2c",
  "sender": "npc://town.blacksmith",
  "receiver": "npc://town.guard",
  "intent": "request",
  "protocol": "fipa-request",
  "conversation_id": "conv_brew_quest_12",
  "timestamp": "2026-08-16T10:22:01Z",
  "ttl_ms": 5000,
  "parts": [
    {
      "type": "data",
      "mimeType": "application/json",
      "data": {
        "payload": {
          "subject": "player_arrested",
          "target": "player_001",
          "context": { "location": "market", "severity": "high" }
        }
      }
    }
  ]
}
```

- `sender` / `receiver`: NPC's Agent Card URL or Stable ID; production via **Signed Agent Card** to verify identity.
- `intent` ∈ `inform / request / propose / agree / refuse / query-if / cfp` (subset of FIPA's 22 communicative acts, ensuring reasonability and auditability).
- `payload`: `DataPart` (also `TextPart` / `FilePart`), carries semantic content; `conversation_id` links multi-round collaboration, `ttl_ms` prevents stale messages.
- Long-running collaboration modeled with A2A `Task` (`submitted→working→input_required→completed/failed`), NPC-to-player "follow-up question" corresponds to `input_required` state.

### 9.3 Chinese-Market Special: Domestic Large-Model API Compatibility

> Following info from 2026 vendor docs and search results; **some model/version numbers ahead of public training data, re-verify with vendor official site before citing** (sources marked in §9.5). Unified conclusion: **all five domestic models provide OpenAI-compatible endpoint + Function Calling; MCP support is split (Ali/Tencent fairly complete, Zhipu via doc declaration, DeepSeek/Kimi mainly custom Server for now)**.

| Model / platform | OpenAI-compatible | Function Calling | MCP support | Notes (verified points) |
|---|---|---|---|---|
| **Qwen (Aliyun Bailian)** | ✅ Complete (`compatible-mode/v1`, also Anthropic-compatible) | ✅ Native | ✅ Fairly complete: Responses API native `type:"mcp"` (SSE, up to 10 MCP Servers) | Model matrix includes Qwen-Max/Plus/Flash and open-source series; `DASHSCOPE_API_KEY` + change `base_url` to migrate |
| **Zhipu GLM (bigmodel.cn)** | ✅ OpenAI SDK-compatible | ✅ (GLM-4-Flash / GLM-4.7 etc. native) | ✅ Doc declares MCP support for external tools/data; GLM-4.6V ships dedicated MCP tool | GLM-4.7: 200K context / 128K output / controllable thinking (Interleaved/Preserved/Turn-level) |
| **DeepSeek (deepseek.com)** | ✅ Complete (OpenAI + Anthropic dual-compatible) | ✅ OpenAI format, `strict`(Beta) + parallel(≤128) | ⚠️ No official MCP Server yet (community bridges via custom Server) | Tool call in thinking mode since V3.2; `base_url=https://api.deepseek.com` |
| **Hunyuan (Tencent Cloud)** | ✅ (`api.hunyuan.cloud.tencent.com/v1`) | ✅ (hunyuan-turbo/pro/functioncall/hy3) | ✅ Tencent Cloud MCP service live; Hunyuan MCP Server example exists (hunyuan_chat/hunyuan_image) | No Embedding / image-video-audio generation / fine-tune (per community SDK wrapper) |
| **Kimi (Moonshot)** | ✅ (`api.moonshot.cn/v1` / `api.moonshot.ai/v1`) | ✅ Tool Use, strict default on (MFJS subset), ≤128 functions | ⚠️ Experimental (via custom MCP Server) | kimi-k3 uses `reasoning_effort` (low/high/max); ships official Formula tools (web-search etc.) |

**Landing implications for Macha**:
1. **Model-access layer can "one codebase covers domestic models"**: All OpenAI-compatible, Macha `LLMClient` only changes `base_url` + `api_key` (inherits §4.2 strategy); thinking/reasoning intensity uses each vendor's param (`thinking` / `reasoning_effort`) for capability negotiation.
2. **Function Calling is a strong de-facto standard**: All five support it, Macha §9.2.2's `npc_perform_action` schema can be sent directly to any; must turn on `strict` to align each vendor's JSON Schema subset differences (DeepSeek uses JSON Schema type whitelist, Kimi uses MFJS subset).
3. **MCP split → Macha adopts "self-build MCP Server + optional cloud MCP" strategy**: Macha itself as MCP Server exposes `speak/act/remember/observe` (§9.2.1), doesn't depend on model-side MCP; only enable its hosted MCP when connecting Ali/Tencent ecosystem toolchains.
4. **Embedding gap**: Hunyuan provides no Embedding, Macha memory-retrieval vectorization should use Qwen/GLM/DeepSeek or local `bge` etc., avoid locking single domestic model.

### 9.4 Quantification and Landing: Field Counts / Message Caps / Latency Budget

#### 9.4.1 Interface field counts (for schema review and minimization constraint)

| Draft | Field scale | Notes |
|---|---|---|
| (a) MCP NPC Server | 4 tools; single-tool input schema **3–5 fields** (speak 3 / act 4 / remember 5 / observe 4) | Deliberately lean, complex data via `observe` resource pagination |
| (b) OpenAI function schema | `parameters` **7 fields** (incl. nested `location` 3 subfields); `required` 3, `strict:true` | Mappable to (a)'s act/speak |
| (c) ECS `NPCBrainComponent` | **11 data fields** (Unity and Unreal isomorphic) | Incl. 2 Entity refs + version + enable bit |
| (d) A2A multi-NPC message | **9 top-level fields** + `payload` nesting (subject/target/context) | intent + parts are core |

#### 9.4.2 Message body size caps (prevent block, ensure interop)

| Channel | Suggested cap | Reason |
|---|---|---|
| MCP `tools/call` params (arguments JSON) | **≤ 8 KB** | Prevent large object blocking JSON-RPC; large observation via `observe` resource pagination |
| MCP `structuredContent` result | **≤ 64 KB** | Structured result; beyond via resource URI reference |
| A2A `Artifact` / `Part` | **≤ 2 MB** (NPC scenario) | Text/small-data mainly, huge volume via URI reference |
| OpenAI `tool_calls.arguments` | **≤ 8 KB** (aligned with MCP) | Easy dual-protocol translation |

#### 9.4.3 End-to-end latency budget (P50 / P95, 60fps real-time constraint)

| Stage | Budget (P50 / P95) | Notes |
|---|---|---|
| MCP round-trip (stdio local subprocess) | **< 100 ms / < 200 ms** | Local low-overhead, preferred landing form |
| MCP round-trip (Streamable HTTP remote same zone) | **< 200 ms / < 400 ms** | Cross-process/network |
| ECS brain system tick (state projection only) | **< 2 ms** (within ≤ 16.6 ms frame budget) | No LLM, only projection + cooldown judgment |
| NPC dialogue turn (LLM gen + one tool round-trip) | **< 1.5 s / < 3 s** (target P50 < 800 ms) | Local vLLM Q4 can approach target; cloud model needs eval |
| A2A cross-NPC negotiation (Agent Card cached) | **< 300 ms / < 600 ms** | First round needs Signed Agent Card pull (cacheable) |
| `act` execution ack (accepted ack) | **< 100 ms** | BT leaf node accepts then acks, doesn't wait for action complete |

> Latency red line: **ECS tick never runs LLM within frame**; LLM call must be async (inside Macha process or remote, result written back to `NPCBrainComponent.MemoryHandle`). If dialogue turn exceeds 1.5 s, should degrade to "play thinking emote first + async generate" (echoes §4.3 precision/latency trade-off and eval requirement).

### 9.5 New Source Collection (six-field format, 2025–2026)

[Category]Engineering implementation (interop protocol)
[Title]Model Context Protocol — Key Changes (2026-07-28 official changelog)
[Link]https://modelcontextprotocol.io/specification/latest/changelog
[One-line summary]MCP official changes since 2025-11-25: stateless (remove session/`Mcp-Session-Id`, `initialize` handshake), `Tasks` moved to official extension `io.modelcontextprotocol/tasks`, tool schema promoted to JSON Schema 2020-12, results add `resultType` and MRTR pattern, introduce `CacheableResult`.
[Key conclusions]
1. Breaking-change direction: each request self-describes protocol version and capability in `_meta`, `server/discover` for version negotiation.
2. `Tasks` reworked to polling `tasks/get` + `tasks/update`, server can actively return handle; removed `tasks/list`.
3. Tool `inputSchema` supports `oneOf/anyOf/allOf/$ref`; `Roots/Sampling/Logging` enter deprecation cycle.
4. New `ttlMs/cacheScope` cache hint, tool list should be stably ordered for client cache.
[Reusable]Macha MCP client/server upgrade checklist (stateless, Tasks extension models long-term-memory reminder, 2020-12 schema expresses complex ActionCall).

[Category]Engineering implementation/industry report (interop protocol)
[Title]One Year of MCP: November 2025 Spec Release + Linux Foundation Donation
[Link]https://blog.modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary/ (ecosystem/donation background also https://ai-solutions.wiki/news/mcp-turns-one )
[One-line summary]MCP one year: 2025-11-25 introduced experimental Tasks/Extensions/simplified OAuth; 2025-12-09 Anthropic donated MCP to Linux Foundation Agentic AI Foundation (OpenAI co-initator, Google/Microsoft/AWS/Cloudflare/Bloomberg supporters); official Registry preview launched.
[Key conclusions]
1. MCP became "AI tool universal port", 2025-11-25 marks exit from experimental.
2. Cross-vendor governance landed, reduces single-company lock-in, OpenAI and Anthropic co-author extensions (Apps/MCP-UI).
3. Official Registry (registry.modelcontextprotocol.io) preview, not yet advised as production infra.
[Reusable]Macha's "foundation-level backing" argument for MCP, supports anchoring only MCP + A2A dual protocol.

[Category]Industry report (multi-agent communication, Linux Foundation official)
[Title]A2A Protocol Surpasses 150 Organizations, Lands in Major Cloud Platforms (v1.0)
[Link]https://linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations-lands-in-major-cloud-platforms-and-sees-enterprise-production-use-in-first-year
[One-line summary]A2A one year reaches v1.0 stable, 150+ orgs in production, 22K+ GitHub stars, five-language SDK; Signed Agent Cards + AP2 payment protocol; natively integrated into Azure AI Foundry / Copilot Studio / Bedrock AgentCore.
[Key conclusions]
1. v1.0 stable, multi-protocol support, enterprise multi-tenant, modern security flow, early-adopter migration path.
2. Signed Agent Cards use cryptographic signature for cross-vendor identity check.
3. A2A and MCP both under Linux Foundation Agentic AI Foundation, complementary as multi-agent base layer.
[Reusable]Macha multi-NPC collaboration "signed Agent Card + Task lifecycle" model; firm drop of ACP single line.

[Category]Engineering implementation (domestic model / MCP)
[Title]Aliyun Bailian — MCP (Responses API native MCP tool)
[Link]https://help.aliyun.com/document_detail/2968153.html
[One-line summary]Qwen natively connects MCP Server in Responses API via `tools:[{type:"mcp", server_protocol:"sse", server_url, server_label}]` (SSE protocol, up to 10), gives official Python/Node example and supported-model list.
[Key conclusions]
1. Supported models: Qwen-Max/Plus/Flash series and Qwen3.5/3.6 open-source series (via Responses API).
2. MCP server_protocol currently `sse`, needs Bearer Token.
3. Coexists with OpenAI-compatible endpoint (`compatible-mode/v1`), choose either.
[Reusable]Macha `ActionSink`'s "zero-code declare MCP Server as OpenAI tool" bridge mode.

[Category]Engineering implementation (domestic model / OpenAI-compatible)
[Title]Aliyun Bailian — OpenAI-compatible interface (Chat Completions)
[Link]https://www.alibabacloud.com/help/zh/model-studio/compatibility-of-openai-with-dashscope
[One-line summary]Bailian Qwen models support OpenAI-compatible interface, only change API Key / BASE_URL / model name to migrate; gives streaming and non-streaming examples, supported models include Qwen, DeepSeek, Kimi, GLM, MiniMax third-party direct.
[Key conclusions]
1. BASE_URL like `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`.
2. Return structure includes `choices[].message.tool_calls`, consistent with OpenAI.
3. Third-party direct models (DeepSeek/Kimi/GLM etc.) need console activation first.
[Reusable]Macha `LLMClient` domestic-model migration list (base_url + key switch, no code change).

[Category]Engineering implementation (domestic model / Function Calling + MCP)
[Title]Zhipu large-model open platform — model capability (GLM-4-Flash / GLM-4.7)
[Link]https://docs.bigmodel.cn (capability statement https://docs.bigmodel.cn/cn/guide/models/free/glm-4-flash-250414 ; GLM-4.7 spec https://www.datalearner.com/ai-models/pretrained-models/756 )
[One-line summary]Zhipu full model matrix OpenAI SDK-compatible; GLM-4-Flash declares Function Calling, structured output, context cache and MCP; GLM-4.7 provides 200K context / 128K output, controllable thinking and MCP.
[Key conclusions]
1. OpenAI SDK-compatible, zero migration cost.
2. Function Calling native; GLM-4.6V ships dedicated MCP tool (vision→API direct).
3. GLM-4.7 thinking mechanism: Interleaved/Preserved/Turn-level Thinking, per-round control.
[Reusable]Macha domestic-model "thinking control + tool call" param-negotiation template.

[Category]Engineering implementation (domestic model / Tool Calls)
[Title]DeepSeek API — Tool Calls (incl. strict mode and parallel)
[Link]https://api-docs.deepseek.com/zh-cn/guides/tool_calls
[One-line summary]DeepSeek fully OpenAI Function Calling format-compatible; supports tool call in thinking mode, strict(Beta) strict JSON Schema, up to 128 parallel functions; gives complete Python example and schema type whitelist.
[Key conclusions]
1. `base_url=https://api.deepseek.com`, also provides Anthropic-compatible `https://api.deepseek.com/anthropic`.
2. strict mode needs `base_url=https://api.deepseek.com/beta`, only supports subset like object/string/number/integer/boolean/array/enum/anyOf.
3. Tool call in thinking mode since DeepSeek-V3.2; `deepseek-chat/reasoner` deprecated 2026-07-24, renamed v4-flash non-thinking/thinking.
[Reusable]Macha `ActionCall` strict schema validation rule on DeepSeek (additionalProperties:false, all props required).

[Category]Engineering implementation (domestic model / OpenAI-compatible + Function Call)
[Title]Tencent Hunyuan — OpenAI-compatible interface and Function Call practice
[Link]https://developer.cloud.tencent.com/article/2673058 (dialogue API https://cloud.tencent.com/document/api/1729/105701 )
[One-line summary]Hunyuan provides OpenAI-compatible interface, supports Function Call (param name updated from old `functions/function_call` to `tools/tool_choice`); hunyuan-turbo/pro/functioncall/hy3 etc. supported; Tencent Cloud MCP service live.
[Key conclusions]
1. OpenAI-compatible endpoint `api.hunyuan.cloud.tencent.com/v1`, `role` includes `tool` (functioncall scenario).
2. Community Hunyuan MCP Server example exists (hunyuan_chat / hunyuan_image tools).
3. Per community SDK wrapper, Hunyuan no Embedding / image-video-audio generation / fine-tune.
[Reusable]Macha memory-retrieval vectorization avoids Hunyuan (use other domestic/local Embedding) note.

[Category]Engineering implementation (domestic model / Tool Use)
[Title]Kimi (Moonshot) — Tool Use / official tools (Formula API)
[Link]https://platform.kimi.ai/docs/api/tool-use (OpenAI migration https://platform.kimi.ai/docs/guide/migrating-from-openai-to-kimi ; official tools https://platform.moonshot.cn/docs/guide/use-official-tools )
[One-line summary]Kimi OpenAI Tool Use-compatible, strict default on (MFJS subset), functions in tools ≤128; kimi-k3 uses `reasoning_effort` (low/high/max); official Formula tools (web-search/code-runner etc.) via standard function flow.
[Key conclusions]
1. `base_url=https://api.moonshot.cn/v1` (or `api.moonshot.ai/v1`), OpenAI SDK direct.
2. strict default true, must conform MFJS; `tool_choice` supports none/auto/required/null (some old models no required).
3. MCP experimental, via custom MCP Server bridge.
[Reusable]Macha `ActionCall` MFJS schema constraint and strict default behavior when sending to Kimi.

[Category]Engineering implementation (game-industry standard / ECS)
[Title]Unity DOTS / ECS 2024–2025 best practice (ISystem / ECB / Tag)
[Link]https://blog.csdn.net/qq395280705/article/details/156614856 (Unity official DOTS manual https://docs.unity3d.com/Packages/com.unity.entities@latest/ )
[One-line summary]Unity 6 DOTS makes ECS high-performance core; best practice: prefer `ISystem` (Burst-compatible), `EntityCommandBuffer` batch structure change, use Tag + enable/disable instead of frequent create/destroy, shared component grouping; explicitly applies to NPC crowds and AI decision.
[Key conclusions]
1. Data-oriented design, components stored contiguously improves cache hit.
2. Avoid per-frame `EntityManager` direct add/remove, use ECB and disable bit.
3. DOTS analyzer monitors Chunk utilization / Job scheduling.
[Reusable]Macha `NPCBrainComponent`'s "fine-grained + disable-able + no LLM in tick" landing constraint.

> Note: Qwen3.7/3.8, GLM-4.7, DeepSeek-V4, kimi-k3 etc. model/version numbers in §9.3 come from 2026 vendor docs and search results, some ahead of public training data, re-verify with vendor official site before citing; this doc only restates source content, didn't fabricate models or URLs.
