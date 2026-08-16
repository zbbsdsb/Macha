# Macha 的"标准接口草案"参考材料

> 类别：标准与生态（Macha 六层框架中的第 6 层）
> 研究目标：为 Macha 成为游戏 NPC 领域的"标准骨架"提供**互操作性（interoperability）**层面的事实依据与接口草案，覆盖互操作协议、游戏工业标准接口、开源框架设计哲学、模型接入标准四大块。
> 关联文档：
> - `direction.md`（Macha = 感知—记忆—推理—行动，最小可验证方向）
> - `positioning.md`（底层认知架构 + 引擎无关接口 + 评估）
> - `architecture.md`（Perception → Memory → Reasoning → Action 四层内核 + `Observation`/`MemoryItem`/`BaseAgent` 接口草案）
> - `engineering_npc_architectures.md`（关键结论：**上层认知/记忆/人格由 Macha 标准化（Replace），下层执行/控制与引擎/商业平台由 Macha 适配（Wrap）**）

---

## 0. 一句话结论（给接口草案用）

要把 Macha 做成"标准骨架"，真正的接口工作只有两层：

1. **对"模型 / 工具 / 引擎"这三件外部事物，采用既有的、已成事实标准的协议形状，不要另起炉灶**——模型接入对齐 **OpenAI 兼容 API**；工具调用对齐 **Anthropic Tool Use / OpenAI Function Calling** 的 JSON Schema 形状、并用 **MCP** 把"外部工具/资源"标准化暴露；引擎适配对齐 **ECS（Unity DOTS / Unreal MassEntity）+ 行为树执行壳 + 各引擎插件规范**；多 NPC 协作对齐 **A2A/ACP（运行时交互）+ AutoGen/OpenAI Agents 式 handoff 编排**（严谨语义可借鉴 **FIPA ACL**）。
2. **只有"认知内核"（记忆、人格、反思、规划、语义感知）是 Macha 必须自己定义标准的领域**——这正好对应 `engineering_npc_architectures.md` 的 Replace 结论：那些被各开源 LLM Mod（RimAI / SkyrimNet）手搓、各商业平台（Inworld / ACE）私有化的"大脑"部分，才是 Macha 要统一取代的碎片化现状。

> 一句话：**Macha 的"标准" = 开放可替换的认知内核 + 对接既成事实标准（OpenAI API / MCP / ECS / A2A）的适配层。** 它不发明传输协议，只定义"认知层 ↔ 标准协议"之间的契约。

---

## 1. 互操作协议（Interop Protocols）

### 1.1 MCP（Model Context Protocol，Anthropic）

- **它标准化了什么**：在"单个 Agent 内部"，把 LLM 与外部**工具（Tools）、资源（Resources）、提示（Prompts）**的标准化连接做成开放协议。本质是一个 **JSON-RPC 2.0** 之上的客户端—服务器协议，定义了 `initialize → tools/list → tools/call`、`resources/read`、`prompts/get`、`sampling`、`elicitation`、`roots`、`completion`、`logging` 等原语。
- **接口形状**：
  - 传输层：`stdio`（本地子进程）或 `Streamable HTTP`（远程，取代早期 SSE），JSON-RPC 消息，2025-11-25 版新增 **Tasks**（异步 call-now / fetch-later）、**Extensions 框架**、企业级 OAuth 2.1。
  - 核心数据类型：`Tool { name, description, inputSchema(JSON Schema) }`、`Resource { uri, mimeType }`、`Prompt`。
  - 客户端可连接任意 MCP Server，Server 也可通过 `sampling` 反向调用客户端 LLM（注意：这打开了"Server 反过来用模型"的回路）。
- **Macha 如何采用 / 适配**：
  - **把 Macha 认知内核的"能力"以 MCP Server 暴露**：例如 `remember`/`recall`/`reflect` 可作为 MCP Tools，让外部 Agent / 编辑器 / 引擎插件都能调用 Macha，而不必耦合 Macha 源码——直接对标 `engineering_npc_architectures.md` 第 6 节"对外暴露 MCP Server + OpenAI 兼容 Tool Use"。
  - **Macha 也作为 MCP Client 消费外部工具**：游戏内"查背包/播动画/读世界状态"等动作可由引擎侧实现为 MCP Server，Macha 只管认知、不管执行。SkyrimNet 已用 MCP Server（44+ 工具）证明这条路线在游戏里可行。
  - 采用 2025-11-25 版的 Tasks 原语表达"长时任务"（如"三天后 NPC 主动提起这件事"可建模为异步 Task）。

### 1.2 OpenAI Function Calling / Anthropic Tool Use（工具调用形状）

- **它标准化了什么**：让 LLM 从"纯文本生成"升级为"输出结构化调用意图"。两者概念一致，但字段形状不同：
  - **OpenAI**：`tools: [{ type:"function", function:{ name, description, parameters(JSON Schema) } }]`，返回 `message.tool_calls[]`（arguments 是 JSON 字符串）。支持 `strict: true`（Structured Outputs，保证参数严格符合 schema）、并行调用、`tool_choice`。
  - **Anthropic**：`tools: [{ name, description, input_schema(JSON Schema) }]`，返回 `content` 中的 `tool_use` 块（`.input` 已是 dict），用 `stop_reason=="tool_use"` 判定，结果以 `role:"user"` + `tool_result` 块回灌；同样支持 `strict: true`、`server tools`（Web Search 等由 Anthropic 托管执行）。
- **接口形状**：**统一的"工具 = 一个 JSON Schema 描述的能力"**。这正是 Macha `Action` 模块最自然的上层契约——无论下发给行为树、发给 Unity、还是交给 MCP，都先收敛成"一个带 JSON Schema 的工具调用"。
- **Macha 如何采用 / 适配**：
  - 把 `Action` 模块的输出定义为 **Tool-Use 形状**（name + input_schema + structured args），使 Macha 同时兼容 OpenAI / Anthropic / 任意 OpenAI 兼容端点（见 §4），也天然能被 MCP `tools/call` 承载。
  - 在 `architecture.md` 的 `Observation`/`MemoryItem` 之外，补一个 `ActionCall` dataclass（`tool: str, args: dict, provenance: str`），作为认知层与执行层之间最小的"语义动作"单元。

### 1.3 多智能体通信协议（FIPA ACL / A2A / ACP）

#### FIPA ACL（Foundation for Intelligent Physical Agents）
- **它标准化了什么**：基于言语行为理论（speech-act）的 **Agent Communication Language**，定义 `inform / request / query-if / propose / cfp / agree / refuse …` 等 22 个 communicative acts，以及 `:sender :receiver :content :language(FIPA-SL) :ontology :protocol :conversation-id` 等消息字段；并用模态逻辑（BDI）给出每个行为的**形式化语义**（feasibility precondition + rational effect）。配套定义交互协议（FIPA-Request / Contract-Net 等）与 Agent 管理平台（AMS / DF / MTS）。
- **接口形状**：消息以 s-expression / XML / 二进制多种编码传输，transport 可用 IIOP / HTTP。强调"若无法处理则回 `not-understood`"。
- **Macha 如何采用 / 适配**：FIPA 偏学术、重语义、在产业落地少，但它是**多 NPC 社会性交互最严谨的语义底座**。Macha 不必实现完整 FIPA，但应借鉴其两点：
  - **用"意图类型（communicative act）"而非裸消息**给 NPC 间通信建模（如 `request`、`inform`、`propose`），让多 NPC 协作可被推理与审计；
  - **ontology 字段**：跨 NPC 共享的"世界/关系本体"正是 Macha 记忆层要做的事，可借 FIPA 的 ontology 概念定义 Macha 的关系/世界知识 schema。

#### A2A（Agent2Agent，Google，2025-04；现由 Linux Foundation 托管）
- **它标准化了什么**：**Agent ↔ Agent** 的发现与协作。核心构件：`Agent Card`（`.well-known/agent.json`，声明能力/技能/认证）、`Task`（状态机：submitted→working→input-required→completed/failed，支持长时任务与 SSE 流式）、`Message`/`Artifact`/`Part`（TextPart / FilePart / DataPart 多模态）。传输用 **HTTP(S) + JSON-RPC 2.0 + SSE**，认证对齐 OpenAPI（OAuth2 / OIDC），并内建 OpenTelemetry 可观测性。
- **接口形状**：客户端拉取远端 Agent Card → 鉴权 → `tasks/send` 或 `tasks/sendSubscribe`（SSE）→ 取 Artifact。
- **Macha 如何采用 / 适配**：当 Macha 驱动**多个 NPC 彼此协作 / 与外部环境 Agent 协作**时，用 A2A 的 `Agent Card` 做 NPC 能力声明、`Task` 做协作任务生命周期。这与 Macha 六层框架中"多 NPC 社会性"目标直接对应，且 `input-required` 状态天然支持"NPC 向玩家/其他 NPC 追问"。

#### ACP（Agent Communication Protocol，IBM BeeAI，2025-03）
- **它标准化了什么**：与 A2A 同期、目标类似的 **Agent ↔ Agent** REST 协议，核心是"让调用 Agent 像调 REST 服务一样简单"——`Agent Manifest`（构建期离线声明，参考 W3C WebFinger / ActivityPub 的 Actor）、`Run`（一次执行，MIME-typed MessagePart）、支持 `await`（暂停等人/物输入）。
- **与 A2A 的关系（重要）**：据 2025-08 的社区状态，**ACP 已合并进 A2A、纳入 Linux Foundation，二者统一为单一 A2A 标准**，BeeAI 平台现运行于 A2A。因此 Macha 新系统设计应**只锚定 A2A**，ACP 仅作为"REST-first / 构建期 manifest"思路的参考，不再单独对接。

> MCP 连接"Agent↔工具/数据"，A2A 连接"Agent↔Agent"——两者互补，正是 Macha 适配层需要同时支持的两个协议层次。

---

## 2. 游戏工业标准接口（Game-Industry Standard Interfaces）

### 2.1 ECS（Entity Component System）架构

- **它标准化了什么**：一种"数据导向"的软件架构范式——**Entity（唯一 ID）+ Component/Fragment（纯数据）+ System/Processor（逻辑）**解耦数据与行为，靠 `Query`（按组件组合筛选实体）驱动批处理，内存按 Archetype/Chunk 紧凑排布以榨干 CPU 缓存。
- **接口形状（Unity DOTS）**：`IComponentData`（数据）；`System`（逻辑，配 Job/Burst）；`EntityManager` 管理实体与组件；GameObject 经 `Baking`/`IConvertGameObjectToEntity` 转换进 ECS；配套 `Entities Graphics / Unity Physics / Netcode for Entities`。
- **接口形状（Unreal MassEntity）**：术语略有差异——`Fragment`（=Component，逻辑无关数据）、`Processor`（=System，无状态、用 `EntityQuery` 批处理）、`Archetype`（相同 Fragment+Tag 组合的实体集合）、`Chunk`（内存块）、`Tag`（空结构，用于筛选）、`Trait`（Fragment+Processor 的功能集合，可在 `MassEntityConfig` 资产里声明/继承）。UE5.5 起 MassEntity 已并入核心引擎。
- **Macha 如何采用 / 适配**：
  - **把 Macha 的"世界状态 / 实体认知"建模为 ECS 友好结构**：NPC、玩家、物品都是 Entity；Macha 写入的 `PersonaState`/`RelationState`/`Belief` 作为 Fragment（Component），引擎的执行系统（BT/导航/动画）读取这些 Fragment。这与 `engineering_npc_architectures.md` 把引擎 AI 当作"可被适配的执行后端"完全同构。
  - Macha 不必自己实现 ECS，而是定义**一组标准化 Fragment/Component 的 schema**（如 `MachaMemoryFragment`、`MachaGoalFragment`），由 Unity/Unreal 适配器把 Macha 的认知状态投影（project）进各自 ECS。

### 2.2 行为树 / 决策模块 ↔ 游戏引擎的常见数据接口

- **现状**：行为树（BT）是行业默认执行壳（Unreal 内建 BT+Blackboard、Unity `com.unity.behavior`、Godot 社区 Beehave）。`Blackboard` 是 1:N 的共享数据区，`Tick` 每帧自顶向下求值；`Service/Decorator` 注入外部数据。Macha 的 `Action` 模块（§1.2）输出"结构化动作意图"后，最合适的落地形态就是**驱动一个 BT 叶子节点或写入 Blackboard**，由引擎去执行 `MoveTo`/`PlayAnim`/`UseSmartObject` 等。
- **Macha 如何采用 / 适配**：
  - 定义 **`ActionSink` 接口**（见 `architecture.md` 设想），其实现包括：`BehaviorTreeSink`（写 Blackboard/触发 BT 节点）、`HTNPlannerSink`、`UtilitySink`、`MCPToolSink`。认知层只产 `ActionCall`，执行层负责"怎么一步步做"——严格兑现 Replace/Wrap 分工。
  - 借鉴 Unreal **Smart Objects**：把"关卡中可被 NPC 动态发现并使用的交互槽位"抽象成 Macha 的 `InteractionSlot` 数据模型，让 NPC 的"意图→可执行交互"解耦。

### 2.3 Unity / Unreal / Godot 插件规范

| 引擎 | 插件/扩展规范 | 适配器落点 |
|---|---|---|
| Unity | Package（`com.unity.*`，含 `package.json`、Editor/RT 分目录）+ Burst/DOTS | 发布 `com.macha.npc` 包，内含 ECS `IComponentData` 投影与 BT `Action` 节点 |
| Unreal | Plugin（`.uplugin` + Module）+ MassEntity `Trait`/`Processor` | 发布 Macha 插件，提供 `UMachaBrainComponent` 与 Mass `Trait`，把 Macha 认知状态映为 Fragment |
| Godot | Addon（GDExtension / 编辑器插件，4.x 引入 GDExtension C++ 绑定） | 提供 Godot 4 Addon，用 `Node` 包装 Macha Agent，经 `Signal` 与场景通信 |

- **Macha 如何采用 / 适配**：统一以 **"引擎无关内核（Python/C#/C++ 抽象）+ 各引擎薄适配器"** 形态分发，每个适配器只做"Macha 认知状态 ↔ 引擎原生结构（Component/Fragment/Node）"的投影，避免为每个引擎重写认知逻辑（这也是 RAIN 停更教训的反面：内核开放、适配器社区可维护）。

---

## 3. 开源框架设计哲学（Framework Design Philosophy）

### 3.1 LangChain / LlamaIndex —— 组合式与数据导向抽象

- **LangChain / LCEL**：核心抽象是 **`Runnable` 协议**（`invoke`/`batch`/`stream`），用管道符 `|` 把 `prompt | model | parser` 组合成链；链自动可流式、可批、可追踪。Agent = LLM 自主选择工具的循环。配套 LangSmith（追踪/评估）、LangServe（链转 REST）。
- **LlamaIndex**：核心抽象是 **`Index`**（向量/树/知识图谱/SQL 索引）+ `QueryEngine` + `Retriever`，专注"把 LLM 连到你自己的数据"。提供 160+ 数据连接器与子问题分解、混合检索、重排等检索策略。
- **Macha 如何采用 / 适配**：
  - 借鉴 **LCEL 的"一切皆 Runnable、用组合代替继承"**：Macha 的认知循环（Perceive→Memory→Reason→Act）应表达为**可组合管线**，而非硬编码单例，方便替换记忆后端、替换推理策略。
  - 借鉴 **LlamaIndex 的检索/索引抽象**：Macha 的长期记忆检索（向量/图谱/时序）直接复用其 `Retriever` 概念与评估指标（Faithfulness / Relevancy）。
  - 注意边界：LangChain/LlamaIndex 是"通用 LLM 应用框架"，**不是 NPC/游戏认知框架**；Macha 只借用其组合与检索抽象，不引入其全部依赖。

### 3.2 AutoGen / Microsoft Agent Framework / OpenAI Agents —— 多智能体抽象

- **AutoGen（Microsoft，v0.4 重写）**：把 Agent 建模为**消息传递的 Actor**（AssistantAgent / UserProxyAgent），通过 `GroupChatManager`（轮流或自动选 speaker）或自定义编排器驱动多 Agent 对话；跨语言（Python/.NET），事件驱动异步，OpenTelemetry 可观测。
- **Microsoft Agent Framework（2025-10 公开预览，MIT）**：合并 **AutoGen（运行时/多 Agent 模式）** 与 **Semantic Kernel（企业级状态/插件/类型契约）**，以 `AIAgent` 基类做到 provider-agnostic，支持 **Agent Orchestration（LLM 驱动决策）** 与 **Workflow Orchestration（确定性业务流程）** 两种编排，以 **thread 作为状态/可复现/可审计单元**，可接 Azure AI Foundry / OpenAI / Ollama 等。AutoGen 转维护模式，新项目建议 Agent Framework。
- **OpenAI Agents SDK（2025-03）**：轻量 code-first 框架，核心是 **Agent + Handoffs（把对话所有权交给专家 Agent，对 LLM 呈现为 `transfer_to_x` 工具）+ agents-as-tools（经理保留所有权）+ Guardrails + Sessions + Tracing**；同时支持把 MCP Server 作为工具挂载。判定原则：**handoff 用于"专家接管"，as-tool 用于"经理调用专家做有界子任务"**。
- **Macha 如何采用 / 适配**：
  - 多 NPC 编排采用 **handoff / as-tool 两种模式**：NPC 间"我把这件事交给你负责"用 handoff 语义；"我调用守卫 NPC 查一下玩家通缉状态"用 as-tool 语义。这与 §1.3 的 A2A `Task`/`Agent Card` 对齐。
  - 借鉴 **thread 作为状态单元**：Macha 每个 NPC 的"人生线程"对应一个 thread（记忆/对话/关系状态），便于可复现与审计（呼应 `engineering` 文档对"可调试/可观测"的要求）。
  - 借鉴 **Agent Framework 的 AIAgent provider-agnostic 接口**：Macha 的 `Agent` 接口下游可挂 OpenAI / 本地 vLLM / Ollama，不锁模型。

### 3.3 Haystack / DSPy —— 声明式 / 模块化设计思想

- **Haystack（deepset，Apache-2.0）**：企业级 **Pipeline 编排引擎**，把 `Retriever / Reader / Ranker / PromptBuilder / Generator` 等组件以 **DAG（显式图）** 组合；每个组件独立可见、可替换、可测；内置评估（EM/F1）、REST/Docker 部署、监控。哲学是"**你掌控图，每个组件可独立调试**"。
- **DSPy（Stanford，MIT）**：**声明式"编程而非提示"**——把 Prompt 与检索策略视为**可学习参数**，用 `Signature（输入/输出契约）+ Module + Optimizer（如 BootstrapFewShot / MIPROv2）` 通过"编译"自动优化整条管线；强调 typed signature、可评估指标驱动的自动调优。
- **Macha 如何采用 / 适配**：
  - 借鉴 **Haystack 的显式 DAG + 组件可替换**：Macha 认知内核内部应是声明式管线，调试面板能逐组件查看"感知→记忆命中→反思→决策"，避免 LangChain 式抽象遮蔽错误（呼应 GOAP 不可预测的教训）。
  - 借鉴 **DSPy 的"契约 + 自动优化"**：把 NPC 的"人格/回答风格"定义为 typed signature，用少量标注样本自动优化提示与检索策略（如"角色一致性"评估指标驱动），降低手写 prompt 漂移。

---

## 4. 模型接入标准（Model-Access Standards）

### 4.1 OpenAI 兼容 API（事实标准）

- **它标准化了什么**：OpenAI 的 `/v1/chat/completions`、`/v1/embeddings`、`/v1/models`、`/v1/completions` 的 **JSON 请求/响应形状**（model + messages + 参数 → choices）已成为 LLM 接入的**事实 wire format**；流式用 SSE。Years of 工具（OpenAI SDK、LangChain、LlamaIndex、各类 chat UI）都写死在这个形状上。
- **Macha 如何采用 / 适配**：
  - Macha 的 `LLMClient` 接口（`direction.md` 已规划）**以 OpenAI 兼容形状为默认契约**：`chat(messages) -> choices`、`embed(texts) -> vectors`。任何一个本地/云端端点只要暴露 `/v1`，Macha 就不改代码切换（见 §4.2）。
  - 这保证了 Macha "模型无关"——既可用 OpenAI/Anthropic（经兼容网关），也可用本地模型，满足"可私有化部署"的开放定位。

### 4.2 本地服务接口（vLLM / llama.cpp / Ollama）

- **三者共同点**：都暴露 **OpenAI 兼容 `/v1`**，差异只在端口与加载格式，不在 API 形状：

| 运行时 | 默认 base_url | 定位 | 关键能力 |
|---|---|---|---|
| **Ollama** | `http://localhost:11434/v1` | 开发/单机/演示 | 一键拉取、GGUF 量化、Apple MLX；默认上下文 2048（需 `OLLAMA_CONTEXT_LENGTH` 调大） |
| **llama.cpp**（`llama-server`） | `http://localhost:8080/v1` | 离线/边缘/无 GPU | 最强量化控制（GGUF、batched、mmap），从树莓派到多卡皆可 |
| **vLLM** | `http://localhost:8000/v1` | 生产/并发/团队服务 | PagedAttention + 连续批处理，吞吐 2–4×；需 CUDA/ROCm；支持 AWQ/GPTQ/FP8 |

- **兼容性谱系（诚实标注）**：`/v1/chat/completions`、`/v1/embeddings`、`/v1/models`、SSE 流式、tool/function calling 三者大多支持但**严格度不一**（llama.cpp 依赖 chat template + `--jinja`；Ollama 仅对声明了 tools 的模型有效；vLLM 需 `--enable-auto-tool-choice` + 对应 parser）。JSON mode / structured output 在三者上靠 GBNF/grammar/guided decoding 实现，严格度低于原版 OpenAI。**Macha 不应假设本地端点 100% 等价于 OpenAI，应在 `LLMClient` 里做能力协商（capability negotiation）。**
- **Macha 如何采用 / 适配**：**所有客户端代码锚定 OpenAI SDK**（仅改 `base_url` + `api_key`），"开发用 Ollama、生产换 vLLM"是配置变更而非重写；工具调用/流式/embedding 代码原样保留。这正是 Macha "可替换、不锁模型"的工程落点。

### 4.3 量化 / 蒸馏 / 投机解码（部署选项）

- **量化（Quantization）**：降低权重/激活精度以压缩体积、提速。常见：`FP8 / INT4 / GPTQ / AWQ / GGUF-Q4_K_M`；2025 进展含极低比特（2–4bit，部分场景精度损失<1%）、混合精度自适应（敏感层保高精度）、硬件感知量化（TensorRT-LLM、TPU）。实践：DeepSeek-R1 671B 上 FP4 推理吞吐近 FP8 的 2×；4-bit 单机部署吞吐翻倍。
- **蒸馏（Distillation）**：用大模型（教师）监督训练小模型（学生），传递软标签/特征/注意力/关系知识。2025 进展：多教师蒸馏、自蒸馏、任务特定蒸馏。案例：DeepSeek-R1 蒸馏出 32B/70B 小模型逼近 o1-mini；Phi-3 自蒸馏；Claude Mini 系列以 1/10 体积保 85%+ 能力。
- **投机解码（Speculative Decoding）**：用轻量草稿模型多步预测、主模型单次并行验证，减少自回归调用次数，无损加速。变体：**EAGLE（Meta，树形注意力 + 在线蒸馏草稿，Llama4 上 1.4–2.0×）**、**SubSpec（NeurIPS 2025，低比特 substitute layers，消费级 GPU 上 9–12×）**、MTP（DeepSeek 多头预测，吞吐 +144%）。
- **Macha 如何采用 / 适配**：
  - Macha 不绑定某一部署方案，但 **`LLMClient` 必须把"部署形态"作为参数暴露**：量化等级、是否用投机解码、上下文长度。评估阶段（六层之第 5 层）据此测量"延迟/成本/角色一致性"的 trade-off。
  - 对 NPC 实时对话，**延迟是硬约束**：建议开发期 Ollama（Q4_K_M）+ 生产期 vLLM（更高精度 + 投机解码），且**必须在部署精度上做评估**（避免"笔记本上调 Q4、上线静默升精度"导致行为漂移，这是 MatterAI 明确警示的陷阱）。

---

## 5. Macha 接口映射总表（Interface Map）

> 把上面四类标准映射到 Macha 六层内核（感知—记忆—推理—行动）+ 适配层。原则：**认知内核自己定义标准，外部世界对接既成事实标准。**

| Macha 层 / 关注点 | 采用 / 对齐的标准 | 接口形状（Macha 侧契约） | 理由（呼应 Replace/Wrap） |
|---|---|---|---|
| **模型接入**（LLMClient） | **OpenAI 兼容 API**（+ vLLM/Ollama/llama.cpp 本地端点） | `chat(messages)->choices`、`embed(texts)->vectors`；能力协商 | 事实 wire format，保证"模型无关/可私有化" |
| **工具调用 / Action 输出** | **Anthropic Tool Use / OpenAI Function Calling** 形状 | `ActionCall{ tool, input_schema, args }` | 统一"语义动作"单元，下游可投 BT/MCP/引擎 |
| **外部工具 / 资源** | **MCP（Model Context Protocol）** | Macha 既做 MCP Server（暴露记忆/反思工具）也做 Client（消费引擎工具） | 标准化"Agent↔工具/数据"，SkyrimNet 已证游戏可行 |
| **引擎适配（执行后端）** | **ECS**（Unity DOTS / Unreal MassEntity）+ **行为树执行壳** + 各引擎插件规范 | 标准化 Fragment/Component schema（`PersonaState`/`Goal`/`Belief`）+ `ActionSink` 多实现 | Wrap：引擎 AI 是"可被适配的执行后端" |
| **多 NPC 协作** | **A2A**（Agent Card + Task + SSE）；编排借鉴 **OpenAI Agents handoff / as-tool**、**AutoGen/Agent Framework** thread | `AgentCard` 能力声明、`Task` 生命周期、handoff 语义 | Wrap：社会性交互用既成 agent 协议 |
| **严谨语义（可选）** | **FIPA ACL**（communicative act + ontology + 形式化语义） | 用"意图类型 + 共享本体"建模 NPC 间消息 | 借鉴语义底座，不必全量实现 |
| **记忆检索** | **LlamaIndex Retriever / Haystack Pipeline** 抽象；embeddings 用 OpenAI 兼容 `/v1/embeddings` | `Retriever.retrieve(query)->MemoryItem[]`；声明式 DAG | 复用成熟检索/评估，不自造轮子 |
| **认知循环组合** | **LangChain LCEL Runnable** 组合哲学；**Haystack** 显式可调试图；**DSPy** 契约+自动优化 | `Perceive→Memory→Reason→Act` 可组合管线；typed signature 自动调优 | 借鉴组合/可观测/声明式，内核自定标准 |
| **认知内核（记忆/人格/反思/规划）** | **Macha 自有标准**（Replace 层；借鉴 Inworld 组件、ACE 分层、RimAI 模块划分，但开放可替换） | `MemoryStore` / `PersonaSchema` / `ReflectionLoop` / `Planner` 接口 | Replace：取代碎片化私有"大脑" |

**一句话接口哲学**：
> Macha 内部用"可组合认知管线 + 四类最小接口（`Agent` / `MemoryStore` / `PerceptionSource` / `ActionSink`）"定义标准；对外，模型走 OpenAI 兼容、工具走 MCP、引擎走 ECS+BT+插件、多 NPC 走 A2A。需要 Macha 自己标准化的，只有"记忆/人格/反思/规划"这一上层认知内核。

---

## 6. 给 Macha 标准接口草案的落地建议

1. **先冻结"认知内核最小接口"**：`Agent` / `MemoryStore` / `PerceptionSource` / `ActionSink` 四类（沿用 `architecture.md`），其中 `ActionSink` 必须有 BT / HTN / MCP / 引擎 多后端实现，兑现"Wrap 下层"。
2. **把 `Action` 收敛成 Tool-Use 形状**：`ActionCall{ tool, input_schema(JSON Schema), args }` 是认知层与一切执行层的唯一契约；这样既对接 OpenAI/Anthropic，又天然可承载为 MCP `tools/call`。
3. **Macha 同时是 MCP Server 与 MCP Client**：对外暴露 `recall/reflect/remember` 等工具（让编辑器/外部 Agent 调用），对内消费引擎侧 MCP Server（背包/动画/世界状态）。
4. **LLMClient 锚定 OpenAI 兼容 + 能力协商**：不假设本地端点等同于 OpenAI；把量化等级、投机解码、上下文长度作为可配置参数，并在评估阶段测量延迟/成本/一致性的 trade-off。
5. **多 NPC 用 A2A（弃用 ACP 单线）**：用 `Agent Card` 声明每个 NPC 的能力、`Task` 管理协作生命周期；NPC 间消息用 FIPA 式"意图类型 + 共享本体"建模，保证可被推理与审计。
6. **可观测/可调试优先**：借鉴 Haystack 显式 DAG 与 LangSmith/OpenTelemetry，内置"记忆流 / 决策链 / 人格状态 / 工具调用"面板，避免重蹈 GOAP"不可预测、难 QA"的覆辙（呼应 `engineering` 文档第 6 节）。
7. **开放治理、避免 RAIN 式停更**：内核 MIT/Apache 开源、引擎适配器社区可维护、清晰版本与兼容策略。

---

## 7. 来源收集（Source Collection）

> 格式遵循 `information_needs.md` 约定。所有 URL 均来自本次 WebSearch/WebFetch 实际命中；未能稳定验证的已显式标注"未检索到稳定链接"，未编造。

---

【类别】工程实现（互操作协议）
【标题】Model Context Protocol Specification（2025-11-25，最新版）
【链接】https://modelcontextprotocol.io/specification/2025-11-25
【一句话摘要】Anthropic 主导的开放协议，用 JSON-RPC 2.0 标准化"单个 Agent 内部 LLM 与外部 Tools/Resources/Prompts"的连接；2025-11-25 版新增 Tasks（异步）、Extensions、企业级 OAuth。
【关键结论】
1. 传输层 stdio + Streamable HTTP，消息为 JSON-RPC 2.0。
2. 核心原语：tools/list、tools/call、resources/read、prompts/get、sampling、elicitation、roots、completion、logging。
3. 2025-11-25 版引入 Tasks（call-now/fetch-later 异步）与 Extensions 框架。
4. SDK 多语言，已成为"Agent↔工具/数据"的事实标准。
【可复用的东西】Macha 既做 MCP Server（暴露记忆/反思工具）又做 Client（消费引擎工具）的协议形状；Tasks 可建模"长时记忆提醒"。

【类别】工程实现（互操作协议）
【标题】MCP Architecture（官方架构文档）
【链接】https://modelcontextprotocol.io/docs/learn/architecture
【一句话摘要】解释 MCP 的 Host/Client/Server 角色与生命周期，是理解"Macha 如何同时作为 Server 与 Client"的底座。
【关键结论】
1. Host 承载多个 Client，每个 Client 连一个 Server。
2. Server 提供 tools/resources/prompts，Client 通过标准化请求调用。
3. sampling 允许 Server 反向请求 Client 的 LLM。
【可复用的东西】Macha 双角色（Server+Client）拓扑图。

【类别】工程实现（互操作协议）
【标题】Anthropic Tool Use with Claude（官方文档）
【链接】https://platform.claude.com/docs/en/agents-and-tools/tool-use/overview
【一句话摘要】Anthropic 的工具调用形态：tools 用 name/description/input_schema，返回 content 中的 tool_use 块（.input 为 dict），stop_reason=="tool_use" 判定；支持 strict 与 server tools。
【关键结论】
1. 与 OpenAI 差异：input_schema 而非 parameters，无 function 包装，结果在 role:user + tool_result 块。
2. 支持 client tools（自执行）与 server tools（Anthropic 托管执行）。
3. strict:true 保证参数严格符合 schema。
【可复用的东西】Macha `ActionCall` 工具形状定义；双供应商工具调用兼容方案。

【类别】工程实现（互操作协议）
【标题】OpenAI Function Calling（官方指南）
【链接】https://platform.openai.com/docs/guides/function-calling
【一句话摘要】OpenAI 的函数调用形状：tools:[{type:function, function:{name,description,parameters(JSON Schema)}}]，返回 tool_calls（arguments 为 JSON 字符串）；支持 strict/并行/tool_search。
【关键结论】
1. strict:true（Structured Outputs）保证参数严格匹配 schema。
2. 支持并行调用、tool_choice 控制、pydantic/zod 自动生成 schema。
3. 已统一进 Responses API 与 Agents SDK。
【可复用的东西】与 Anthropic 工具调用对齐的字段映射表；Macha ActionSink 的 JSON Schema 约束。

【类别】学术论文/标准（多智能体通信）
【标题】FIPA ACL Specification（OC00003A， communicative acts）
【链接】https://www.fipa.org/specs/fipa00003/OC00003A
【一句话摘要】基于言语行为理论的 Agent 通信语言，定义 22 个 communicative acts 与消息结构（:sender/:receiver/:content/:language(FIPA-SL)/:ontology/:protocol/:conversation-id），用 BDI 模态逻辑给出形式化语义。
【关键结论】
1. 每个 communicative act 有 narrative + 形式化语义（feasibility precondition + rational effect）。
2. 最小合规要求：收到无法处理的消息须回 not-understood。
3. 配套交互协议（FIPA-Request / Contract-Net）与 Agent 管理平台（AMS/DF/MTS）。
【可复用的东西】NPC 间"意图类型 + 共享本体"建模思路；ontology 字段对应 Macha 关系/世界知识 schema。

【类别】学术论文/标准（多智能体通信）
【标题】History of FIPA ACL（官方历史文档）
【链接】http://fipa.org/subgroups/ROFS-SG-docs/History-of-FIPA.htm
【一句话摘要】FIPA ACL 1997 起基于 ARCOL、2002 标准化；基于 speech-act 理论，22 个 message types，内容语言用 FIPA-SL/KIF/RDF。
【关键结论】
1. 源于 KQML 之后的标准化 ACL，目标是跨 Agent 知识级通信。
2. 定义 Agent Platform、AMS、DF、Message Transport 完整体系。
3. 现由 IEEE 继承维护。
【可复用的东西】"Agent 平台"分层参考；消息信封/传输解耦思想。

【类别】工程实现/产业报告（多智能体通信）
【标题】What is the Agent2Agent (A2A) Protocol?（IBM 解读）
【链接】https://www.ibm.com/think/topics/agent2agent-protocol
【一句话摘要】Google 2025-04 推出、现由 Linux Foundation 托管的开放 Agent↔Agent 协议；与 MCP 互补（MCP 连工具，A2A 连 Agent）。核心：Agent Card、Task、Message/Artifact/Part，传输用 HTTP+JSON-RPC 2.0+SSE。
【关键结论】
1. Agent Card（.well-known/agent.json）做能力发现；Task 有 submitted→working→input-required→completed/failed 状态机。
2. Part 支持 Text/File/Data 多模态；SSE 流式。
3. 认证对齐 OpenAPI（OAuth2/OIDC），内建 OpenTelemetry 可观测。
【可复用的东西】Macha 多 NPC 协作的发现/任务生命周期模型；与 MCP 的层次分工图。

【类别】工程实现/产业报告（多智能体通信）
【标题】What You Need to Know About Agent2Agent Protocol（Snyk）
【链接】https://snyk.io/articles/what-you-need-to-know-about-agent2agent-protocol
【一句话摘要】详述 A2A 的 client-server 交互模型、Agent Card 数字身份、Task 状态机、富通信原语，以及安全/长时任务/多模态原则。
【关键结论】
1. 单 Agent 可在不同交互中同时充当 client 与 server，支持 mesh 拓扑。
2. 内置可观测（trace ID + OTLP 结构化日志）。
3. 设计原则：基于现有 web 标准、安全默认、支持长时任务、模态无关。
【可复用的东西】A2A 安全/可观测设计对 Macha NPC 协作的借鉴（审计、追踪）。

【类别】工程实现（多智能体通信）
【标题】Agent Communication Protocol (ACP) — IBM Research 博客
【链接】https://research.ibm.com/blog/agent-communication-protocol-ai
【一句话摘要】IBM BeeAI 2025-03 推出的 REST 风格 Agent↔Agent 协议，目标是"Agent 通信的 HTTP"；与 MCP 互补（ACP 连 Agent，MCP 连工具）。
【关键结论】
1. REST + JSON + OAuth2/API Key，Agent 携 manifest 支持离线发现。
2. 支持 peer-to-peer 去中心交互（非仅 manager 模式）。
3. 重要状态：2025-08 起 ACP 已合并进 A2A、纳入 Linux Foundation，BeeAI 现运行于 A2A。
【可复用的东西】"REST-first / 构建期 manifest"思路（仅供 A2A 设计参考）；Macha 新系统应只锚定 A2A。

【类别】工程实现（多智能体通信）
【标题】MCP and A2A — Agent Communication Protocol（ACP 官方对比页）
【链接】https://agentcommunicationprotocol.dev/about/mcp-and-a2a
【一句话摘要】澄清 MCP（Agent↔工具）、A2A（Agent↔Agent，Google）、ACP（Agent↔Agent，IBM）三者层次分工与关系。
【关键结论】
1. MCP 解决单 Agent 内"模型连工具/资源"，A2A/ACP 解决 Agent 间通信。
2. ACP 优势：Linux Foundation 开放治理、REST 通信、离线 Agent 发现、MIME 消息可扩展。
3. A2A 与 ACP 目标重叠，已统一为 A2A。
【可复用的东西】Macha 适配层"MCP + A2A 双协议"的分层图景。

【类别】工程实现（游戏工业标准）
【标题】Unity Entities package（DOTS / ECS 官方文档）
【链接】https://docs.unity3d.com/Packages/com.unity.entities@latest/
【一句话摘要】Unity 的 Data-Oriented Technology Stack 中 ECS 实现：Entity + IComponentData（数据）+ System（逻辑）+ EntityManager；GameObject 经 Baking 转 ECS；配套 Graphics/Physics/Netcode。
【关键结论】
1. 核心是数据导向，配 Burst/Job 提升性能。
2. 提供 ConvertToEntity / SubScene / IConvertGameObjectToEntity 转换工作流。
3. 适合大规模实体（Megacity 演示支持 64+ 玩家）。
【可复用的东西】Macha 把认知状态投影为 Unity `IComponentData` 的适配器模式。

【类别】工程实现（游戏工业标准）
【标题】Unreal Engine MassEntity Overview（官方文档）
【链接】https://docs.unrealengine.com/5.3/de/overview-of-mass-entity-in-unreal-engine
【一句话摘要】UE5 的 archetype-based ECS：Fragment（=Component，纯数据）、Processor（=System，无状态、EntityQuery 批处理）、Archetype、Chunk、Tag、Trait；UE5.5 起并入核心引擎。
【关键结论】
1. Fragment 只存数据，Processor 经 EntityQuery 批处理，按 Archetype/Chunk 紧凑排布榨缓存。
2. Trait 是"Fragment+Processor"功能集合，可在 MassEntityConfig 资产声明/继承。
3. MassSimulation 子系统管理每帧周期；支持与 StateTree/导航组合。
【可复用的东西】Macha 认知状态 → Unreal `Fragment` 的投影 schema；Trait 作为"人格/目标"功能集合。

【类别】工程实现（游戏工业标准）
【标题】Unreal Smart Objects Overview（官方文档）
【链接】https://dev.epicgames.com/documentation/en-us/unreal-engine/smart-objects-in-unreal-engine---overview
【一句话摘要】UE 的"关卡中可经预订系统使用的活动集合"，只提供数据不含执行逻辑，由 Subsystem 全局管理、空间分区索引、按 Gameplay Tag 查询。
【关键结论】
1. 定义含 Activity Tags / Slots / Behavior Definition。
2. Agent 搜索→认领 Slot→执行自身逻辑。
3. 让背景 NPC 动态发现并交互而无需逐物体硬编码。
【可复用的东西】Macha `InteractionSlot`（"可发现交互槽位"）抽象，解耦"意图↔可执行交互"。

【类别】工程实现（开源框架设计）
【标题】LangChain（框架概览与 LCEL）
【链接】https://ai-hub.emersonbraun.dev/docs/tools/langchain
【一句话摘要】LangChain 以"组合与编排"为核心：LLM/prompt/parser/retriever/tool 模块化，LCEL 用 `|` 组合成可流式/批/追踪的链；Agent 是 LLM 自主选择工具的循环；LangSmith 提供追踪评估。
【关键结论】
1. 核心抽象 Runnable（invoke/batch/stream），管道式组合。
2. Agent = 推理循环（选工具→执行→回灌→继续）。
3. 生态广但抽象层多，简单场景有开销。
【可复用的东西】Macha 认知循环"一切皆可组合 Runnable"的管道哲学；避免抽象遮蔽错误。

【类别】工程实现（开源框架设计）
【标题】LlamaIndex vs LangChain（2026 对比）
【链接】http://ai-tldr.dev/learn/agent-frameworks/orchestration-frameworks/llamaindex-vs-langchain
【一句话摘要】LlamaIndex 核心是 Index + QueryEngine + Retriever，专注"把 LLM 连到你自己的数据"（160+ 连接器、子问题分解、混合检索、重排）；LangChain 核心是控制流与工具链（LCEL + LangGraph）。
【关键结论】
1. LlamaIndex 检索策略内置且高级（hybrid / sub-question / auto-merge）。
2. LangChain 1.0（2025-10）起 agent 运行于 LangGraph（显式 state + 条件边 + human-in-the-loop）。
3. 最佳实践：底层检索用 LlamaIndex 封装为 Tool，交给 LangChain Agent 调度。
【可复用的东西】Macha 记忆检索复用 LlamaIndex Retriever 抽象；Agent 调度借鉴 LangGraph 状态图。

【类别】工程实现（开源框架设计）
【标题】Multi-Agent Frameworks: AutoGen, CrewAI, OpenAI Agents SDK（学习计划第 8 章）
【链接】https://pixelbank.dev/agent-study-plan/chapter/8
【一句话摘要】2025 年主流多 Agent 框架横评：AutoGen 的 Actor 模型（消息传递 Agent）、OpenAI Agents SDK 的 handoffs、Claude Agent SDK 的 subagents、Agno/Mastra 运行时。
【关键结论】
1. AutoGen v0.4 重写为异步 Actor，Agent 各有内存/工具/LLM，靠 GroupChatManager 选 speaker。
2. OpenAI Agents SDK 轻量、handoffs/guardrails/sessions 一等公民。
3. 框架选择矩阵按 state/streaming/subagents/vendor 匹配约束。
【可复用的东西】Macha 多 NPC 编排的"Actor + handoff"抽象。

【类别】工程实现（开源框架设计）
【标题】Microsoft Unveils Agent Framework（AutoGen + Semantic Kernel 合并）
【链接】https://kiadev.net/news/2025-10-03-microsoft-agent-framework-multi-agent-orchestration
【一句话摘要】Microsoft 2025-10 公开预览的开源 SDK/运行时，合并 AutoGen（多 Agent 运行时）与 Semantic Kernel（企业状态/插件/类型契约）；以 `AIAgent` 基类做到 provider-agnostic，支持 Agent/Workflow 两种编排，thread 为状态单元。
【关键结论】
1. 两种编排：Agent Orchestration（LLM 驱动）+ Workflow Orchestration（确定性流程）。
2. 以 thread 为单位做可复现/重试/审计。
3. 支持 Azure OpenAI / OpenAI / Ollama / GitHub Models，新项目建议 Agent Framework（AutoGen 转维护）。
【可复用的东西】Macha `Agent` 接口 provider-agnostic 设计；thread 作为 NPC"人生状态"单元。

【类别】工程实现（开源框架设计）
【标题】OpenAI Agents SDK — Orchestration and Handoffs（官方）
【链接】https://developers.openai.com/api/docs/guides/agents/orchestration
【一句话摘要】OpenAI Agents SDK 的核心编排模式：Handoffs（专家接管对话，对 LLM 呈现为 transfer_to_x 工具）与 agents-as-tools（经理保留所有权调用专家做有界子任务）。
【关键结论】
1. handoff 用于"专家应拥有下一段回答"，as-tool 用于"经理综合最终回答"。
2. 每个 specialist 应职责窄、handoffDescription 具体。
3. 过早拆分 agent 会增加 prompt/trace/审批面。
【可复用的东西】Macha 多 NPC "接管 vs 调用"两种协作语义；handoffDescription 映射 NPC 能力描述。

【类别】工程实现（开源框架设计）
【标题】OpenAI Agents SDK 总览（官方平台页）
【链接】https://openai.com/agent-platform/
【一句话摘要】Agents SDK 与 Responses API 的定位区分：SDK 管 agent loop 与多 Agent 编排（handoffs、sessions、guardrails、tracing、MCP 挂载）；Responses API 让你自管循环。
【关键结论】
1. Agents SDK 内置 sessions、tracing、guardrails、可恢复 approval 流。
2. 工具含平台工具、function calling、远程 MCP、agents-as-tools。
3. 适合"server 拥有部署/工具/状态"的 code-first 场景。
【可复用的东西】Macha 把 MCP Server 作为工具挂到 NPC Agent 的运行时模式。

【类别】工程实现（开源框架设计）
【标题】Haystack vs DSPy（框架对比）
【链接】https://zairalabs.ai/guide/compare/dspy-vs-haystack
【一句话摘要】Haystack（deepset，Apache-2.0）是企业级显式 Pipeline（DAG）编排，组件独立可替换可测；DSPy（Stanford，MIT）是声明式"编程而非提示"，把 prompt/检索当可学习参数经编译器自动优化。
【关键结论】
1. Haystack 哲学："你掌控图，每组件可见可测"；适合需逐阶段控制检索/嵌入/路由的 RAG。
2. DSPy 哲学："框架控制优化，prompt 经学习改变"；需可评估输出与标注样本。
3. 两者均为自托管、开源。
【可复用的东西】Macha 认知循环用 Haystack 式显式可调试图；人格/回答风格用 DSPy 式 typed signature 自动优化。

【类别】工程实现（开源框架设计）
【标题】Haystack vs DSPy: different paradigm（官方示例）
【链接】https://theneuralbase.com/haystack/learn/advanced/vs-dspy-different-paradigm
【一句话摘要】用同一 RAG 示例对比：Haystack 显式加组件并连边（你控图），DSPy 写高层 forward 让框架编译优化（框架控优化）。
【关键结论】
1. Haystack 组件图显式、可独立调试、换实现无需重训。
2. DSPy 行为改变靠训练数据+优化器，非手工改 prompt。
3. 生产环境 Haystack 显式法更可控可调试。
【可复用的东西】Macha 调试面板"逐组件查看感知→记忆→反思→决策"的设计依据。

【类别】工程实现（模型接入标准）
【标题】OpenAI-Compatible Local LLM Endpoints（Ollama / vLLM / llama.cpp）
【链接】https://inventivehq.com/blog/openai-compatible-endpoint-for-local-llm
【一句话摘要】所有主流本地运行时都暴露 OpenAI 兼容 `/v1`，差异只在端口与加载格式；应用只需改 base_url 即可从云端切到本地硬件，streaming/tool/embeddings 原样可用。
【关键结论】
1. 端口：Ollama 11434、llama.cpp 8080、vLLM 8000，均挂 `/v1`。
2. 本地 auth 是形式（占位 api_key 即可），外暴露需加真实 auth。
3. Ollama 默认上下文 2048 会静默截断长提示，需调 `OLLAMA_CONTEXT_LENGTH`。
【可复用的东西】Macha `LLMClient` 仅改 base_url 切换模型的部署策略。

【类别】工程实现（模型接入标准）
【标题】Ollama vs vLLM vs llama.cpp: Choosing the Right Local LLM Runtime（MatterAI）
【链接】https://www.matterai.so/guides/ollama-vs-vllm-vs-llamacpp-runtime-comparison
【一句话摘要】三者都说同一 OpenAI 协议，故互换是配置变更而非重写；典型路径：笔记本用 Ollama 原型 → 真实流量换 vLLM（同精度更高）；并警示"在笔记本 Q4 上调参、上线静默升精度"的行为漂移陷阱。
【关键结论】
1. Ollama：零配置、GGUF、Apple MLX；llama.cpp：离线/边缘/无 GPU；vLLM：并发/延迟 SLA/批处理。
2. 因都讲 OpenAI 形状，客户端代码（prompt/tool/streaming/embedding）迁移零改动。
3. 必须在部署精度上做评估，而非笔记本量化精度。
【可复用的东西】Macha 开发→生产运行时迁移路径；精度一致评估原则。

【类别】工程实现（模型接入标准）
【标题】OpenAI API Compatibility Matrix（wideareaai）
【链接】https://wideareaai.com/tools/openai-compatibility-matrix
【一句话摘要】量化对比 llama.cpp / Ollama / vLLM 对 OpenAI 各端点与特性的兼容度（chat/embeddings/streaming/tool-calling/JSON-mode/vision…），结论是"兼容是谱系而非勾选框"。
【关键结论】
1. chat/completions、embeddings、models、SSE 基本都支持。
2. tool-calling 依赖模型 chat template，三者严格度不一（llama.cpp 需 --jinja；Ollama 限声明 tools 的模型；vLLM 需 --enable-auto-tool-choice）。
3. JSON/structured output 靠 GBNF/grammar/guided decoding，严格度低于原版 OpenAI。
【可复用的东西】Macha `LLMClient` 必须做"能力协商"，不可假设本地端点 100% 等价 OpenAI。

【类别】工程实现（部署/压缩）
【标题】大模型优化与压缩技术：2025 年的实践与突破（阿里云开发者社区）
【链接】https://developer.aliyun.com/article/1683981
【一句话摘要】系统梳理 2025 年量化/剪枝/蒸馏/低秩分解四大压缩技术，及硬件协同（Blackwell/TPU/HBM3e）与软件优化（TensorRT-LLM/TVM/并行策略/KV 缓存/投机执行）。
【关键结论】
1. 量化：极低比特（2–4bit，部分<1% 损失）、混合精度自适应、硬件感知、可微分量化。
2. 蒸馏：多教师/自蒸馏/任务特定蒸馏，案例含 Claude Mini、Phi-3、通义千问-M。
3. 投机解码、动态批处理、KV 缓存复用是推理加速关键。
【可复用的东西】Macha 部署选项清单（量化等级/蒸馏/投机解码）作为 `LLMClient` 可配置参数。

【类别】学术论文（推理加速）
【标题】SubSpec: Lossless and Training-Free Acceleration for Offloaded LLMs via Substitute Speculative Decoding（NeurIPS 2025）
【链接】https://abdelfattah-lab.github.io/pubs/speculate_deep_and
【一句话摘要】用目标 LLM 低位量化 substitute layers 构造高对齐草稿模型，做无损、免训练的投机解码，消费级 GPU 上 Qwen2.5 7B/32B 达 9.1×/12.5× 加速。
【关键结论】
1. 投机解码 = 轻量草稿模型多步预测 + 主模型单次并行验证，减少自回归调用。
2. SubSpec 共享 GPU 常驻层与 KV-Cache，进一步降内存并提升对齐。
3. 无损且免训练，适合资源受限部署。
【可复用的东西】Macha 本地 NPC 推理延迟优化的可选方案（尤其消费级 GPU）。

---

## 8. 未检索到稳定公开链接的资料（诚实标注，未编造）

- **Unity `com.unity.behavior`（新版可视化行为树包）手册深链**：在 Unity 文档与 ML-Agents 手册中有提及，但本次未单独获取其手册深链；建议以 Unity 官方 Package 文档补全（行为树作为 Macha `ActionSink` 执行壳的 Unity 实现可参考它）。
- **Godot 官方 BT/Utility 模块**：Godot 4 至今无官方高级 AI 模块，依赖社区 Beehave（`github.com/bitbrain/beehave`）与自研；本文 §2.3 的 Godot 适配器建议基于 GDExtension Addon 形态，具体 API 以 Godot 4.x 官方扩展文档为准。
- **EAGLE 投机解码原始论文（arxiv 2508.08192）**：搜索命中新浪新闻对其的报道（含 Llama4 上 1.4–2.0×、INT4 量化草稿等数据），但原始 arxiv 链接未在本次搜索中直接验证，建议团队以 arxiv 编号 2508.08192 复核一手论文。
- **Microsoft Agent Framework 官方 GitHub 仓库深链**：本文以 kiadev.net / ai-trends.today 的发布报道为准（均指向 MIT 许可、Python/.NET、合并 AutoGen+Semantic Kernel），如需精确 API 请以 Microsoft 官方仓库与文档复核。

> 以上资料若需精确引用，建议团队后续用官方/一手来源复核；本文未为它们编造 URL。

---

## 9. 深化补充：接口草案与国产兼容（2025–2026）

> 本章为"加法式深化"：不改动 §1–§8 任何结论，仅在原框架（Macha 六层内核 → 事实标准适配层）下补充四类新内容——(1) 2025–2026 标准时效更新；(2) 四份具体接口草案；(3) 国产大模型 API 兼容专项；(4) 量化与落地预算。新来源严格按 §7 的六字段格式列于 §9.5。
>
> 统一前提（与 §0 一致）：**Macha 只自定认知内核标准（记忆/人格/反思/规划），对外一律对接既成事实标准**——模型走 OpenAI 兼容、工具走 MCP、引擎走 ECS+BT、多 NPC 走 A2A。本章四份草案正是该前提的"最小可落地契约"。

### 9.1 广度 + 时效：2025–2026 标准 / 协议更新

#### 9.1.1 MCP：从 2025-11-25 实验版到 2026-07-28 正式版

- **时间线（据官方 changelog 与周年博客）**：
  - **2025-11-25（v1 周年版）**：引入实验性 `Tasks`（长时异步，`working/input_required/completed/failed/cancelled` 五态）、`Extensions` 框架、OAuth Client ID Metadata Documents（CIMD，取代 DCR）、`Sampling with Tools`（SEP-1577）、企业级 OAuth（Cross App Access / client credentials）。
  - **2025-12-09**：Anthropic 将 MCP 捐赠给 **Linux Foundation 旗下 Agentic AI Foundation**（OpenAI 为共同发起方，Google/Microsoft/AWS/Cloudflare/Bloomberg 为支持组织）——跨厂商治理正式落地，降低单一公司锁定风险。
  - **2026-07-28（正式版，RC 于 2026-05-21 锁定）**：相对 2025-11-25 有**破坏性变更**，方向是"无状态化 + 扩展外置"。
- **对 Macha 影响最大的变更**：
  1. **移除协议级 session 与 `Mcp-Session-Id`**，改为无状态：每个请求在 `_meta` 携带 `protocolVersion` 与 `clientCapabilities`，版本不符返回 `UnsupportedProtocolVersionError`；新增 `server/discover` RPC 做前置版本协商。→ Macha 的 MCP 客户端/服务端须升级到"每请求自描述"模型，不再依赖长连接会话。
  2. **`Tasks` 移出核心、变为官方扩展** `io.modelcontextprotocol/tasks`：重做为轮询式 `tasks/get` + `tasks/update`（客户端回灌输入），移除 `tasks/list`；服务端可主动返回 task handle。→ Macha 的"三天后 NPC 主动提起"式长时记忆提醒，应建模为该扩展而非核心原语。
  3. **工具 `inputSchema` 升格为完整 JSON Schema 2020-12**（支持 `oneOf/anyOf/allOf/$ref/$defs`）；`structuredContent` 可为任意 JSON。→ Macha 的 `ActionCall` 参数 schema 可直接用 2020-12 表达复杂嵌套。
  4. **`Roots` / `Sampling` / `Logging` 进入弃用周期**（标注式弃用，至少 12 个月移除窗口）；`subscriptions/listen` 取代 `resources/subscribe`；结果新增 `resultType`（`complete` / `input_required`），并引入 **Multi Round-Trip Requests (MRTR)** 模式取代 server 主动请求。→ Macha 若用到 server 侧 sampling，需预留迁移路径。
  5. **`CacheableResult`（`ttlMs` / `cacheScope`）**：`tools/list` 等结果可声明缓存新鲜度。→ Macha 暴露的 MCP 工具列表应稳定排序以支持客户端缓存与 prompt cache 命中。

#### 9.1.2 A2A：v1.0 稳定 + Linux Foundation Agentic AI Foundation

- **2026-04-09（一周年里程碑，据 Linux Foundation 新闻稿）**：A2A 达 **v1.0 稳定**，150+ 组织生产环境使用（非试点），GitHub 22K+ stars，SDK 覆盖 Python/JS/Java/Go/.NET 五语言；原生集成进 **Microsoft Copilot Studio / Azure AI Foundry / Amazon Bedrock AgentCore**。
- **Signed Agent Cards**：用密码学签名做跨厂商身份校验（域名级可信），取代早期明文 Agent Card。→ Macha 多 NPC 协作中，每个 NPC 的 `Agent Card` 应带签名，避免"伪 NPC"注入。
- **Agent Payments Protocol (AP2)** 同步推出（60+ 支付/金融机构支持），把 A2A 从"通信"扩展到"可审计的经济协调"。→ 对 Macha 而言是"NPC 间的交易/任务报酬"可选能力，非必需。
- **治理归属**：A2A 与 MCP 同归 **Linux Foundation Agentic AI Foundation**，二者互补（MCP=Agent↔工具，A2A=Agent↔Agent）已构成多智能体互操作基础层。→ Macha 适配层"MCP + A2A 双协议"分层图景（§1.3）得到基金会级背书，坚定只锚定 A2A、弃用 ACP 单线的判断。

#### 9.1.3 Anthropic / OpenAI Tool Use 最新

- **OpenAI Responses API 原生支持 MCP**：`tools` 中可直接放 `{ "type": "mcp", "server_protocol": "sse", "server_url": "...", "server_label": "..." }`，由模型侧驱动 MCP 工具调用（通义千问百炼文档给出了该用法的官方示例，见 §9.5）。→ Macha 的 `ActionSink` 可新增"把 MCP Server 声明为 OpenAI 工具"的零代码桥接模式。
- **strict 模式普及**：OpenAI（`strict:true` Structured Outputs）与 Anthropic（`strict:true`）及 DeepSeek/Kimi 均已支持参数严格符合 schema；Kimi 的 strict 默认开启（遵循 MFJS 子集）。→ Macha `ActionCall` 默认开启 strict，保证下游 BT/引擎拿到的参数合法。
- **Sampling with Tools（MCP SEP-1577）**：MCP Server 可在 sampling 请求里声明工具选择行为，让 Server 在 client token 下部署内部 agent。→ 与 Macha"既做 Server 又做 Client"双角色（§1.1）天然契合。

#### 9.1.4 ECS 新实践（Unity 6 DOTS / Unreal MassEntity 5.5+）

- **Unity 6 DOTS 最佳实践**（综合官方与社区 2024–2025 资料）：优先 `ISystem`（Burst 兼容）、用 `EntityCommandBuffer` 批量排队结构变更、用 **Tag 组件 + 启用/禁用** 而非频繁创建/销毁实体、共享组件做分组、用 Profiler 的 DOTS 分析器监控 Chunk 利用率。适用场景明确包含 **NPC 人群、AI 决策**。
- **Unreal MassEntity 5.5+**：已并入核心引擎，`Fragment`（纯数据）+ `Processor`（无状态、`EntityQuery` 批处理）+ `Trait`（Fragment+Processor 功能集合）模式成熟，可与 StateTree/导航组合。
- **对 Macha 影响**：§2.1 的"认知状态投影为标准化 Fragment/Component"结论不变，但落地约束更明确——`NPCBrainComponent`（§9.2.3）应做成**细粒度、可启用/禁用、无逐帧分配**的数据块；推理不在 ECS tick 内跑 LLM，只在 tick 内做"状态投影 + 冷却判断"，把 LLM 调用异步化（呼应 §4.3 延迟硬约束）。

### 9.2 技术规范深度：四份具体接口草案

> 以下草案均遵循 §0 哲学：**认知层只产出"语义动作/状态"，执行层各后端自行落地**。四个草案分别对应 Macha 适配层的四条标准通道（MCP / OpenAI 兼容 / ECS / A2A）。

#### 9.2.1 (a) MCP Server for NPC —— tools: `speak` / `act` / `remember` / `observe`

Macha 把"单个 NPC 的认知能力"暴露为一个 MCP Server（Host=游戏/编辑器，Client=引擎或外部 Agent）。`list_tools` 返回四个工具，输入 schema 用 JSON Schema 2020-12：

```json
{
  "tools": [
    {
      "name": "speak",
      "description": "NPC 向目标角色（玩家/其他 NPC）说出一段台词。",
      "inputSchema": {
        "type": "object",
        "properties": {
          "utterance": { "type": "string", "description": "要说出的自然语言文本" },
          "tone": { "type": "string", "enum": ["neutral", "friendly", "angry", "fearful", "suspicious"] },
          "target": { "type": "string", "description": "接收者实体 ID，缺省为当前对话玩家" }
        },
        "required": ["utterance"]
      }
    },
    {
      "name": "act",
      "description": "NPC 执行一个具身动作意图（移动/使用物品/交互）。",
      "inputSchema": {
        "type": "object",
        "properties": {
          "action": { "type": "string", "description": "动作类型或语义标签，如 'move_to' / 'use_item' / 'patrol'" },
          "params": { "type": "object", "description": "动作参数（坐标/物品 ID 等）" },
          "priority": { "type": "string", "enum": ["low", "normal", "high", "critical"] },
          "blocking": { "type": "boolean", "description": "是否阻塞直到动作完成" }
        },
        "required": ["action"]
      }
    },
    {
      "name": "remember",
      "description": "将一条经历/事实/关系/情绪写入 NPC 长期记忆。",
      "inputSchema": {
        "type": "object",
        "properties": {
          "content": { "type": "string", "description": "记忆内容" },
          "type": { "type": "string", "enum": ["event", "fact", "relationship", "emotion"] },
          "importance": { "type": "number", "minimum": 0, "maximum": 1, "description": "记忆重要性 0..1" },
          "related_entities": { "type": "array", "items": { "type": "string" }, "description": "相关实体 ID 列表" },
          "source": { "type": "string", "enum": ["observed", "told", "inferred"] }
        },
        "required": ["content", "type"]
      }
    },
    {
      "name": "observe",
      "description": "查询世界状态/其他实体，返回 NPC 当前可观测信息。",
      "inputSchema": {
        "type": "object",
        "properties": {
          "entity_or_location": { "type": "string", "description": "实体 ID 或位置" },
          "query": { "type": "string", "description": "感兴趣的属性或事件" },
          "radius": { "type": "number", "description": "以米为单位的观测半径" },
          "include_entities": { "type": "boolean", "description": "是否返回范围内实体清单" }
        },
        "required": ["entity_or_location"]
      }
    }
  ]
}
```

`tools/call` 的返回（结构化结果）：`speak → {delivered:bool, utterance_id:str}`；`act → {task_id:str, accepted:bool, estimated_ms:int}`；`remember → {memory_id:str, stored:bool}`；`observe → {observations:[...], observed_at:str}`。Macha 同时可消费引擎侧 MCP Server（背包/动画/世界状态），兑现 §1.1 双角色。长时任务（如"三天后主动提起"）走 `io.modelcontextprotocol/tasks` 扩展的轮询式 handle。

#### 9.2.2 (b) OpenAI-compatible Function Schema for NPC 动作

当 Macha 内核产出一个"语义动作"、要直接投给 OpenAI / 通义 / 智谱 / DeepSeek / Kimi / 本地 vLLM 等任意 OpenAI 兼容端点时，使用如下 function 定义（与 §1.2 的 `ActionCall` 完全同构，strict 默认开）：

```json
{
  "type": "function",
  "function": {
    "name": "npc_perform_action",
    "description": "由 NPC 认知内核产出的结构化动作意图，供行为树/引擎执行。",
    "strict": true,
    "parameters": {
      "type": "object",
      "properties": {
        "action_type": { "type": "string", "enum": ["speak", "move", "use_item", "emote", "interact"] },
        "target": { "type": "string", "description": "目标实体 ID（玩家/NPC/物品），可为空" },
        "content": { "type": "string", "description": "speak/emote 的文本或表情名" },
        "location": {
          "type": "object",
          "properties": { "x": { "type": "number" }, "y": { "type": "number" }, "z": { "type": "number" } },
          "required": ["x", "y", "z"], "additionalProperties": false
        },
        "item_id": { "type": "string", "description": "use_item 时的物品 ID" },
        "priority": { "type": "string", "enum": ["low", "normal", "high", "critical"] },
        "provenance": { "type": "string", "description": "来源标记：memory / reasoning / reflection" }
      },
      "required": ["action_type", "priority", "provenance"],
      "additionalProperties": false
    }
  }
}
```

模型返回 `tool_calls[].function.arguments`（JSON 字符串）→ Macha 解析为 `ActionCall` → 路由到 `ActionSink`（BT / HTN / Utility / MCPTool）。该 schema 与 (a) 的 `act`/`speak` 字段集可一一映射，保证 OpenAI 兼容通道与 MCP 通道互通。

#### 9.2.3 (c) ECS Component 定义：`NPCBrainComponent`

Macha 不实现 ECS，只定义**标准化数据块 schema**，由各引擎适配器投影进 Unity `IComponentData` 或 Unreal `Fragment`。关键约束（来自 §9.1.4）：细粒度、可启用/禁用、tick 内不跑 LLM。

**Unity DOTS（`IComponentData`）**：

```csharp
public struct NPCBrainComponent : IComponentData
{
    public FixedString64Bytes  PersonaId;          // 人格/角色模板 ID
    public NPCGoal              CurrentGoal;        // 当前目标（枚举 + 强度）
    public EmotionState         Emotion;            // 情绪状态（枚举 + 强度 0..1）
    public Entity               MemoryHandle;       // 指向 Macha 记忆实体的引用
    public Entity               AttentionTarget;    // 当前注意对象（Entity.Null=无）
    public DialogueState        Dialogue;           // 对话状态机
    public uint                 LastReasoningTick;  // 上次推理的帧/tick
    public float                ReasoningCooldown;  // 推理冷却（秒）
    public FixedString128Bytes  ThreadId;           // 对应 Agent Framework 的 thread
    public int                  RelationshipVersion;// 关系表版本号（脏检查）
    public byte                 Disabled;           // 0/1 启用控制，避免创建/销毁
}
```

**Unreal MassEntity（`FMassFragment` 等价）**：

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

> 短期观测队列建议用独立的 `NPCObservationBuffer`（dynamic buffer / `TArray<FMachaObservation>`），与脑状态分离，避免每帧扩容。该 Component 只承载"投影后的认知快照"，真正推理在 Macha 进程异步完成，结果写回 `MemoryHandle` 指向的记忆实体。

#### 9.2.4 (d) A2A 多 NPC 消息 schema：sender / receiver / intent / payload

多 NPC 社会性交互用 A2A `Message` + FIPA 式意图类型（§1.3）。消息信封如下（基于 A2A `Part` 多模态与 Signed Agent Card 思路，但以 NPC 场景裁剪）：

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

- `sender` / `receiver`：NPC 的 Agent Card URL 或 Stable ID；生产环境经 **Signed Agent Card** 校验身份。
- `intent` ∈ `inform / request / propose / agree / refuse / query-if / cfp`（沿用 FIPA 22 个 communicative acts 的子集，保证可被推理与审计）。
- `payload`：`DataPart`（也可为 `TextPart` / `FilePart`），承载语义内容；`conversation_id` 串联多轮协作，`ttl_ms` 防止陈旧消息。
- 长时协作用 A2A `Task`（`submitted→working→input_required→completed/failed`）建模，NPC 间"追问玩家"对应 `input_required` 状态。

### 9.3 中文市场专项：国产大模型 API 兼容情况

> 以下信息来自 2026 年厂商文档与检索结果；**部分型号/版本号超前于公开训练数据，引用前建议以厂商官网复核**（已在 §9.5 标注来源）。统一结论：**五大国产模型均已提供 OpenAI 兼容端点 + Function Calling；MCP 支持呈分化（阿里/腾讯已较完整，智谱经文档声明，DeepSeek/Kimi 暂以自定义 Server 为主）**。

| 模型 / 平台 | OpenAI 兼容 | Function Calling | MCP 支持 | 备注（已验证要点） |
|---|---|---|---|---|
| **通义千问 Qwen（阿里云百炼）** | ✅ 完整（`compatible-mode/v1`，亦兼容 Anthropic） | ✅ 原生 | ✅ 较完整：Responses API 原生 `type:"mcp"`（SSE，最多 10 个 MCP Server） | 模型矩阵含 Qwen-Max/Plus/Flash 及开源系列；`DASHSCOPE_API_KEY` + 改 `base_url` 即可迁移 |
| **智谱 GLM（bigmodel.cn）** | ✅ OpenAI SDK 兼容 | ✅（GLM-4-Flash / GLM-4.7 等原生支持） | ✅ 文档声明支持 MCP 调用外部工具与数据源；GLM-4.6V 附专用 MCP 工具 | GLM-4.7：200K 上下文 / 128K 输出 / 可控思考（Interleaved/Preserved/Turn-level） |
| **DeepSeek（deepseek.com）** | ✅ 完整（OpenAI + Anthropic 双兼容） | ✅ OpenAI 格式，`strict`(Beta) + 并行(≤128) | ⚠️ 暂未官方 MCP Server 支持（社区经自定义 Server 桥接） | 思考模式下工具调用自 V3.2 起支持；`base_url=https://api.deepseek.com` |
| **混元 Hunyuan（腾讯云）** | ✅（`api.hunyuan.cloud.tencent.com/v1`） | ✅（hunyuan-turbo/pro/functioncall/hy3） | ✅ 腾讯云 MCP 服务已上线；存在 Hunyuan MCP Server 示例（hunyuan_chat/hunyuan_image） | 不支持 Embedding / 图像视频音频生成 / 微调（据社区 SDK 封装） |
| **Kimi（月之暗面 Moonshot）** | ✅（`api.moonshot.cn/v1` / `api.moonshot.ai/v1`） | ✅ Tool Use，strict 默认开（MFJS 子集），≤128 函数 | ⚠️ 实验性（经自定义 MCP Server） | kimi-k3 用 `reasoning_effort`（low/high/max）；含官方 Formula 工具（web-search 等） |

**对 Macha 的落地含义**：
1. **模型接入层可"一套代码通吃国产模型"**：全部 OpenAI 兼容，Macha `LLMClient` 仅改 `base_url` + `api_key`（继承 §4.2 策略）；思考/推理强度用各厂商参数（`thinking` / `reasoning_effort`）做能力协商。
2. **Function Calling 是强事实标准**：五大厂均支持，Macha §9.2.2 的 `npc_perform_action` schema 可直接投递到任意一家；务必开 `strict` 以对齐各厂 JSON Schema 子集差异（DeepSeek 用 JSON Schema 类型白名单，Kimi 用 MFJS 子集）。
3. **MCP 分化 → Macha 采用"MCP Server 自建 + 可选云端 MCP"策略**：Macha 自身作为 MCP Server 暴露 `speak/act/remember/observe`（§9.2.1），不依赖模型侧 MCP；仅当接阿里/腾讯生态的工具链时才启用其托管 MCP。
4. **Embedding 缺口**：混元不提供 Embedding，Macha 记忆检索的向量化应改用 Qwen/GLM/DeepSeek 或本地 `bge` 等，避免锁死单一国产模型。

### 9.4 量化与落地：字段数 / 消息上限 / 延迟预算

#### 9.4.1 接口字段数量（供 schema 评审与最小化约束）

| 草案 | 字段规模 | 备注 |
|---|---|---|
| (a) MCP NPC Server | 4 个工具；单工具输入 schema **3–5 字段**（speak 3 / act 4 / remember 5 / observe 4） | 刻意精简，复杂数据走 `observe` 资源分页 |
| (b) OpenAI function schema | `parameters` **7 字段**（含嵌套 `location` 3 子字段）；`required` 3，`strict:true` | 与 (a) 的 act/speak 可映射 |
| (c) ECS `NPCBrainComponent` | **11 个数据字段**（Unity 与 Unreal 同构） | 含 2 个 Entity 引用 + 版本号 + 启用位 |
| (d) A2A 多 NPC 消息 | **9 个顶层字段** + `payload` 嵌套（subject/target/context） | intent + parts 是核心 |

#### 9.4.2 消息体大小上限（防阻塞、保互通）

| 通道 | 建议上限 | 理由 |
|---|---|---|
| MCP `tools/call` 参数（arguments JSON） | **≤ 8 KB** | 防大对象阻塞 JSON-RPC；大观测改用 `observe` 资源分页 |
| MCP `structuredContent` 结果 | **≤ 64 KB** | 结构化结果；超出走资源 URI 引用 |
| A2A `Artifact` / `Part` | **≤ 2 MB**（NPC 场景） | 文本/小数据为主，超大体量用 URI 引用 |
| OpenAI `tool_calls.arguments` | **≤ 8 KB**（与 MCP 对齐） | 便于双协议互转 |

#### 9.4.3 端到端延迟预算（P50 / P95，60fps 实时约束）

| 环节 | 预算 (P50 / P95) | 备注 |
|---|---|---|
| MCP round-trip（stdio 本地子进程） | **< 100 ms / < 200 ms** | 本地低开销，首选落地形态 |
| MCP round-trip（Streamable HTTP 远程同区） | **< 200 ms / < 400 ms** | 跨进程/网络 |
| ECS brain system tick（仅状态投影） | **< 2 ms**（≤ 16.6 ms 帧预算内） | 不跑 LLM，只投影 + 冷却判断 |
| NPC 对话回合（LLM 生成 + 一次工具往返） | **< 1.5 s / < 3 s**（目标 P50 < 800 ms） | 本地 vLLM Q4 可逼近目标；云端模型需评估 |
| A2A 跨 NPC 协商（Agent Card 已缓存） | **< 300 ms / < 600 ms** | 首轮需拉 Signed Agent Card（可缓存） |
| `act` 执行回执（accepted ack） | **< 100 ms** | 行为树叶子节点接受即 ack，不等动作完成 |

> 延迟红线：**ECS tick 绝不在帧内跑 LLM**；LLM 调用必须异步（Macha 进程内或远程，结果回写 `NPCBrainComponent.MemoryHandle`）。对话回合若超 1.5 s，应降级为"先播思考表情 + 异步生成"（呼应 §4.3 的精度/延迟 trade-off 与评估要求）。

### 9.5 新来源收集（六字段格式，2025–2026）

【类别】工程实现（互操作协议）
【标题】Model Context Protocol — Key Changes (2026-07-28 正式版 changelog)
【链接】https://modelcontextprotocol.io/specification/latest/changelog
【一句话摘要】MCP 自 2025-11-25 起的正式版变更：无状态化（移除 session/`Mcp-Session-Id`、`initialize` 握手）、`Tasks` 移为官方扩展 `io.modelcontextprotocol/tasks`、工具 schema 升格 JSON Schema 2020-12、结果新增 `resultType` 与 MRTR 模式、引入 `CacheableResult`。
【关键结论】
1. 破坏性变更方向：每请求在 `_meta` 自描述协议版本与能力，`server/discover` 做版本协商。
2. `Tasks` 重做为轮询式 `tasks/get` + `tasks/update`，服务端可主动返回 handle；移除 `tasks/list`。
3. 工具 `inputSchema` 支持 `oneOf/anyOf/allOf/$ref`；`Roots/Sampling/Logging` 进入弃用周期。
4. 新增 `ttlMs/cacheScope` 缓存提示，工具列表应稳定排序以支持客户端缓存。
【可复用的东西】Macha MCP 客户端/服务端升级清单（无状态化、Tasks 扩展建模长时记忆提醒、2020-12 schema 表达复杂 ActionCall）。

【类别】工程实现/产业报告（互操作协议）
【标题】One Year of MCP: November 2025 Spec Release + 捐赠 Linux Foundation
【链接】https://blog.modelcontextprotocol.io/posts/2025-11-25-first-mcp-anniversary/ （生态/捐赠背景另见 https://ai-solutions.wiki/news/mcp-turns-one ）
【一句话摘要】MCP 一周年：2025-11-25 版引入实验 Tasks/Extensions/简化 OAuth；2025-12-09 Anthropic 将 MCP 捐赠给 Linux Foundation Agentic AI Foundation（OpenAI 共同发起，Google/Microsoft/AWS/Cloudflare/Bloomberg 支持）；官方 Registry 预览上线。
【关键结论】
1. MCP 成"AI 工具通用端口"，2025-11-25 是走出实验期标志。
2. 跨厂商治理落地，降低单一公司锁定风险，OpenAI 与 Anthropic 共著扩展（Apps/MCP-UI）。
3. 官方 Registry（registry.modelcontextprotocol.io）预览期，尚不建议作生产基础设施。
【可复用的东西】Macha 对 MCP 的"基金会级背书"论证，支撑只锚定 MCP + A2A 双协议。

【类别】产业报告（多智能体通信，Linux Foundation 官方）
【标题】A2A Protocol Surpasses 150 Organizations, Lands in Major Cloud Platforms (v1.0)
【链接】https://linuxfoundation.org/press/a2a-protocol-surpasses-150-organizations-lands-in-major-cloud-platforms-and-sees-enterprise-production-use-in-first-year
【一句话摘要】A2A 一周年达 v1.0 稳定，150+ 组织生产使用，22K+ GitHub stars，五语言 SDK；Signed Agent Cards + AP2 支付协议；原生集成进 Azure AI Foundry / Copilot Studio / Bedrock AgentCore。
【关键结论】
1. v1.0 稳定，多协议支持、企业级多租户、现代安全流、早期采用者迁移路径。
2. Signed Agent Cards 用密码学签名做跨厂商身份校验。
3. A2A 与 MCP 同归 Linux Foundation Agentic AI Foundation，互补构成多智能体基础层。
【可复用的东西】Macha 多 NPC 协作的"签名 Agent Card + Task 生命周期"模型；坚定弃用 ACP 单线。

【类别】工程实现（国产模型 / MCP）
【标题】阿里云百炼 — MCP（Responses API 原生 MCP 工具）
【链接】https://help.aliyun.com/document_detail/2968153.html
【一句话摘要】通义千问在 Responses API 中通过 `tools:[{type:"mcp", server_protocol:"sse", server_url, server_label}]` 原生接入 MCP Server（SSE 协议，最多 10 个），给出官方 Python/Node 示例与受支持模型清单。
【关键结论】
1. 支持模型：Qwen-Max/Plus/Flash 系列及 Qwen3.5/3.6 开源系列（经 Responses API）。
2. MCP server_protocol 当前为 `sse`，需 Bearer Token。
3. 与 OpenAI 兼容端点（`compatible-mode/v1`）并存，可二选一。
【可复用的东西】Macha `ActionSink` 的"零代码把 MCP Server 声明为 OpenAI 工具"桥接模式。

【类别】工程实现（国产模型 / OpenAI 兼容）
【标题】阿里云百炼 — OpenAI 兼容接口（Chat Completions）
【链接】https://www.alibabacloud.com/help/zh/model-studio/compatibility-of-openai-with-dashscope
【一句话摘要】百炼千问模型支持 OpenAI 兼容接口，仅改 API Key / BASE_URL / 模型名即可迁移；给出流式与非流式示例，支持模型含 Qwen、DeepSeek、Kimi、GLM、MiniMax 三方直供。
【关键结论】
1. BASE_URL 形如 `https://{WorkspaceId}.{region}.maas.aliyuncs.com/compatible-mode/v1`。
2. 返回结构含 `choices[].message.tool_calls`，与 OpenAI 一致。
3. 三方直供模型（DeepSeek/Kimi/GLM 等）需先在控制台开通。
【可复用的东西】Macha `LLMClient` 国产模型迁移清单（base_url + key 切换，无需改代码）。

【类别】工程实现（国产模型 / Function Calling + MCP）
【标题】智谱大模型开放平台 — 模型能力（GLM-4-Flash / GLM-4.7）
【链接】https://docs.bigmodel.cn （能力声明见 https://docs.bigmodel.cn/cn/guide/models/free/glm-4-flash-250414 ；GLM-4.7 规格见 https://www.datalearner.com/ai-models/pretrained-models/756 ）
【一句话摘要】智谱全模型矩阵兼容 OpenAI SDK；GLM-4-Flash 声明支持 Function Calling、结构化输出、上下文缓存与 MCP；GLM-4.7 提供 200K 上下文 / 128K 输出、可控思考与 MCP。
【关键结论】
1. OpenAI SDK 兼容，零迁移成本。
2. Function Calling 原生；GLM-4.6V 附专用 MCP 工具（视觉→API 直连）。
3. GLM-4.7 思考机制：Interleaved/Preserved/Turn-level Thinking，按轮控制。
【可复用的东西】Macha 国产模型"思考控制 + 工具调用"参数协商模板。

【类别】工程实现（国产模型 / Tool Calls）
【标题】DeepSeek API — Tool Calls（含 strict 模式与并行）
【链接】https://api-docs.deepseek.com/zh-cn/guides/tool_calls
【一句话摘要】DeepSeek 完全兼容 OpenAI Function Calling 格式；支持思考模式下工具调用、strict(Beta) 严格 JSON Schema、单次最多 128 个并行函数；给出完整 Python 示例与 schema 类型白名单。
【关键结论】
1. `base_url=https://api.deepseek.com`，亦提供 Anthropic 兼容 `https://api.deepseek.com/anthropic`。
2. strict 模式需 `base_url=https://api.deepseek.com/beta`，仅支持 object/string/number/integer/boolean/array/enum/anyOf 等子集。
3. 思考模式工具调用自 DeepSeek-V3.2 起支持；`deepseek-chat/reasoner` 将于 2026-07-24 弃用，更名为 v4-flash 非思考/思考。
【可复用的东西】Macha `ActionCall` 在 DeepSeek 上的 strict schema 校验规则（additionalProperties:false、全属性 required）。

【类别】工程实现（国产模型 / OpenAI 兼容 + Function Call）
【标题】腾讯混元 — OpenAI 兼容接口与 Function Call 实战
【链接】https://developer.cloud.tencent.com/article/2673058 （对话 API 见 https://cloud.tencent.com/document/api/1729/105701 ）
【一句话摘要】混元大模型提供 OpenAI 兼容接口，支持 Function Call（参数名已从旧版 `functions/function_call` 更新为 `tools/tool_choice`）；hunyuan-turbo/pro/functioncall/hy3 等模型支持；腾讯云已上线 MCP 服务。
【关键结论】
1. OpenAI 兼容端点 `api.hunyuan.cloud.tencent.com/v1`，`role` 含 `tool`（functioncall 场景）。
2. 社区存在 Hunyuan MCP Server 示例（hunyuan_chat / hunyuan_image 工具）。
3. 据社区 SDK 封装，混元不支持 Embedding / 图像视频音频生成 / 微调。
【可复用的东西】Macha 记忆检索向量化避开混元（改用其他国产/本地 Embedding）的注意点。

【类别】工程实现（国产模型 / Tool Use）
【标题】Kimi（Moonshot）— Tool Use / 官方工具（Formula API）
【链接】https://platform.kimi.ai/docs/api/tool-use （OpenAI 迁移见 https://platform.kimi.ai/docs/guide/migrating-from-openai-to-kimi ；官方工具见 https://platform.moonshot.cn/docs/guide/use-official-tools ）
【一句话摘要】Kimi 兼容 OpenAI Tool Use，strict 默认开启（MFJS 子集），tools 内函数数 ≤128；kimi-k3 用 `reasoning_effort`（low/high/max）；官方 Formula 工具（web-search/code-runner 等）走标准 function 流程。
【关键结论】
1. `base_url=https://api.moonshot.cn/v1`（或 `api.moonshot.ai/v1`），OpenAI SDK 直连。
2. strict 默认 true，须符合 MFJS 规范；`tool_choice` 支持 none/auto/required/null（部分旧模型不支持 required）。
3. MCP 为实验性，经自定义 MCP Server 桥接。
【可复用的东西】Macha `ActionCall` 投递 Kimi 时的 MFJS schema 约束与 strict 默认行为。

【类别】工程实现（游戏工业标准 / ECS）
【标题】Unity DOTS / ECS 2024–2025 最佳实践（ISystem / ECB / Tag）
【链接】https://blog.csdn.net/qq395280705/article/details/156614856 （Unity 官方 DOTS 手册见 https://docs.unity3d.com/Packages/com.unity.entities@latest/ ）
【一句话摘要】Unity 6 DOTS 把 ECS 作为高性能核心；最佳实践：优先 `ISystem`（Burst 兼容）、`EntityCommandBuffer` 批量结构变更、用 Tag + 启用/禁用替代频繁创建销毁、共享组件分组；明确适用 NPC 人群与 AI 决策。
【关键结论】
1. 数据导向设计，组件连续存储提升缓存命中。
2. 避免逐帧 `EntityManager` 直接增删，改用 ECB 与禁用位。
3. DOTS 分析器监控 Chunk 利用率 / Job 调度。
【可复用的东西】Macha `NPCBrainComponent` 的"细粒度 + 可禁用 + tick 内不跑 LLM"落地约束。

> 注：§9.3 中 Qwen3.7/3.8、GLM-4.7、DeepSeek-V4、kimi-k3 等型号/版本号来自 2026 年厂商文档与检索结果，部分超前于公开训练数据，引用前建议以厂商官网复核；本文仅转述来源内容，未自行编造型号或 URL。
