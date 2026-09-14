# Macha Minecraft Layer — Technical Foundation（技术地基）

> **STATUS: PENDING — 计划文档，未经团队审视。本轮不写代码。**
>
> 阶段定位：不再讨论 Macha 定位，不修改 Macha Core。本文件只建立
> **独立 `macha-minecraft/`（Minecraft Layer）的技术地基**。
>
> 上游依据：
> `docs/architecture.md`（Layer 定义 / Layer Protocol / 边界图）·
> `papers/notes/drafts/environment-integration-layer.md`（审计 A–G）·
> `papers/notes/accepted/decision-layer-first-sequencing.md`（Layer 先、Core 后 + 约束 C1–C5）·
> `../../plans/minecraft-layer-validation-plan.md`（V1–V5 / M1–M9）
>
> 配套文档：
> [`01-protocol-v0.md`](01-protocol-v0.md)（协议 v0 草案）·
> [`02-observation-and-events.md`](02-observation-and-events.md)（观测字段与最小事件集）·
> [`03-build-and-module-layout.md`](03-build-and-module-layout.md)（Gradle / 模块 / 边界守护）

---

## 0. 本阶段的范围与非目标

**唯一目标**

> 让 Minecraft Layer 成为一个**可以独立运行、观察 Minecraft、执行基本环境操作、并为未来
> Macha Runtime 提供稳定连接点**的薄层。

**明确不实现**（任一出现即视为跑偏，见 §G）

```text
LLM · RAG · Memory · Vector DB · Agent Framework · LangChain/LangGraph
Multi-Agent · NPC Dialogue · NPC Personality · Behavior Tree · World Simulation
Quest System · Custom UI · Custom Model · Renderer · Villager AI 替换 · 复杂导航
```

第一阶段允许使用**一个极简的 Minecraft 实体**作为被测对象。它只用来验证这条回路：

```text
Observation → Layer → Action → Minecraft → World Change → Observation
```

---

## A. Current Repository Assessment（当前仓库盘点）

审计时间 2026-09-13。结论：**Minecraft Layer 是完全的 greenfield**，且当前仓库具备足够的
上游文档，可以直接进入技术地基阶段。

### A.1 已存在的内容

| 位置 | 内容 | 对本阶段的作用 |
|---|---|---|
| `src/macha/`（Python，~140 行） | `Observation`/`ActionResult`；`BaseAgent.perceive/think/act` 全 `NotImplementedError`；`Memory` 取末 N 条；`Reasoning` 硬编码；`Perception.process_text` / `Action.execute(decision:str)` | **Macha Core 侧，本阶段不碰。** 注意它隐含了 text channel 环境——这正是本 Layer 要替换掉的东西 |
| `pyproject.toml` / `requirements.txt` / `tests/` | Python 打包与测试 | 与 Gradle 无关；**不得**被 Gradle 构建触及 |
| `docs/architecture.md` | Core / Layer / Environment 三段、Layer Protocol 五类交换、能力模型、最小 Layer M1–M9、边界图、反模式 | Layer 的**规范定义**，本项目的宪法 |
| `papers/notes/drafts/environment-integration-layer.md` | 审计 A–G、仓库组织论证（§E） | 目录隔离方案的依据 |
| `papers/notes/accepted/decision-layer-first-sequencing.md` | 顺序决策 + 约束 C1–C5 | C2 跨语言传输、C3 词表隔离、C4 模拟器不可省 |
| `research/plans/minecraft-layer-validation-plan.md` | V1–V5 判据、G0–G2 门槛、M1–M9 | 本项目的验收口径 |
| `docs/research/engineering_npc_architectures.md` §4.1 | Mineflayer 被定位为"只有原语、没有认知"的适配层模板 | 备选方案的对照（见 §C.3） |

### A.2 不存在的内容（= 本阶段要建的）

- 任何 Kotlin / Gradle / JVM 配置；
- 任何 `macha-minecraft/` 目录；
- 任何 Paper 插件、`plugin.yml`、服务器运行目录；
- 任何协议实现、传输端点、能力清单；
- 任何从 Minecraft 读取状态或写入状态的代码。

### A.3 Repository Boundary（目录隔离方案）

**方案：单仓 + `layers/` 独立构建根（不拆仓，但按可拆仓的方式组织）。文件级结构见 [`04-project-structure.md`](04-project-structure.md)。**

```text
Macha/                          # 现有仓库（Python 为主）
├── src/macha/                  # Macha Core（Python）——本阶段不改
├── docs/ papers/ research/ …   # 现有文档层
└── layers/                     # 【新增】环境接入层：一个 Gradle 构建根，多个模块
    ├── settings.gradle.kts     #   :kit:protocol :kit:runtime :kit:transport
    │                           #   :minecraft :simulator :testclient
    ├── kit/                    # 共享内核（纯 JVM，零环境依赖）
    │   └── protocol/ runtime/ transport/
    ├── minecraft/              # 唯一依赖 paper-api 的模块（环境子树）
    ├── simulator/              # 假环境（约束 C4 的对照条件）
    ├── testclient/             # 垂直切片测试客户端
    └── run/                    # 运行期产物（gitignored）
```

> 为什么共享内核收进 `kit/`：`layers/protocol` 与 `layers/minecraft` 平级时，磁盘上看不出
> "共享内核 vs 环境实现"这条中心区分；收进 `kit/` 后 Minecraft 是与整个共享内核并列的**独立子树**。
> 纯构建布局改动，**Kotlin 包名不变**。决策记录：
> `papers/notes/accepted/decision-layers-directory-layout.md`。

> 2026-09-14 状态更新：团队已创建 `layers/` 骨架（6 个模块、边界守护任务齐备）；
> 物理目录从"平铺"改为 `kit/` 分组是**尚未执行的机械迁移**，步骤见决策记录 §3。

> 为什么是 `layers/` 而不是根级 `macha-minecraft/`：v0 按约束 **C4 必须同时存在 Minecraft 与
> Simulator 两个 Layer**，两者共享 `protocol`/`runtime`/`transport`；`layers/` 这一层父目录用来
> 承载"共享内核 + 环境模块"，拆仓时把 `layers/minecraft/` 整体移出即可。完整论证见 `04` §1。

隔离规则（硬性）：

1. **不在仓库根创建 `settings.gradle.kts` / `build.gradle.kts`。** 根是 Python 项目；根级
   Gradle 会把整仓声明成 Gradle 项目，日后拆仓时要拆两次。
2. **`layers/` 构建不得引用仓库上级路径**（不 `../` 引 `src/`、不带 `includeBuild`、
   不读上级文件）。这样未来把它整目录移出即可成为独立 repo。
3. **依赖方向单向**：Layer 依赖 *协议规范*；Macha Core **不得**依赖 Layer，Layer **不得**
   import Core 代码。两者只通过网络通信。
4. **Minecraft 专有代码被限制在 `:minecraft` 模块**（其内再分 `plugin/` 与 `adapter/`）：
   只有该模块可以依赖 `paper-api` / import `org.bukkit` / `io.papermc`。**由 Gradle 模块依赖
   在编译期强制**；`03-build-and-module-layout.md` §7 的 import 扫描是第二道防线
   （用于捕获模块内不该出现的环境字面量）。
5. **不进仓库**：Paper 服务端 jar、世界存档、`run/` 运行目录、构建产物
   （`layers/**/build/`、`layers/**/.gradle/`、`layers/run/` 需要进 `.gitignore`）。

> 不做的事：不为了"将来可能拆仓"引入 submodule、多仓工具或发布流水线。**边界现在定，
> 拆仓以后再说**（与 `environment-integration-layer.md` §E 的结论一致）。

---

## B. Proposed Minecraft Layer Architecture（实际架构）

### B.1 四段边界（与 `docs/architecture.md` §8 对齐）

```text
Macha Runtime（Python/任意语言，进程外）
   │
   │  Macha ↔ Environment Protocol v0（JSON over HTTP + WebSocket）
   │  ▲ Observation · Event · Action Result · Capability
   │  ▼ Action
   ▼
┌──────────────────────────────────────────────────────────────┐
│ macha-minecraft（Paper 插件进程内）                           │
│                                                              │
│  transport/      连接、帧收发、会话                      ← 不认识 Minecraft
│      │                                                       │
│  protocol/       v0 消息 DTO、编解码、版本/能力协商      ← 纯 Kotlin
│      │                                                       │
│  runtime/        LayerRuntime：会话、能力清单、动作派发、    ← 纯 Kotlin
│      │           结果关联、事件归一化、观测窗口编排            │
│      │                                                       │
│  adapter/paper/  观测采集、事件监听、动作执行、agent 绑定 ← 唯一允许 import Paper
│      │                                                       │
│  plugin/         JavaPlugin 入口、配置、生命周期 wiring   ← 唯一另一个允许 import Paper
└──────────────────────────────────────────────────────────────┘
   │
   │  Paper API（org.bukkit / io.papermc）
   ▼
Paper Server（Minecraft Environment 的运行时；我们不改它）
   │
   ▼
Minecraft
```

**这张图里最重要的东西是那条横切虚线**：`transport` / `protocol` / `runtime` / `observation` /
`events` 全部**不 import Paper**。它保证三件事：

1. 层内可单测（不需要服务器）；
2. 未来同一套 runtime 可复用给别的环境（Simulator Layer 就是这么来的一半）；
3. 一旦有人把 Paper 类型塞进协议 DTO，构建会直接失败。

### B.2 数据流

```text
[Observation]  runtime 按窗口编排 → adapter 采集（主线程读世界）→ 归一化 → protocol 编码 → WS push
[Event]        Paper 事件（主线程）→ adapter 归一化 → runtime 节流/合并 → protocol 编码 → WS push
[Action]       WS 收到 → transport 解码 → protocol 校验 → runtime 校验能力与前置条件
                     ├─ 不满足 → action_result(status=refused, reason=…)
                     └─ 满足   → 回主线程由 adapter 执行 → 采集 state delta
                                 → action_result(status=ok, delta=…) → （随后由 Event 确认世界变化）
[Hello]        连接建立 → 携带 protocol version + capability manifest（探测得到）+ 世界/时间基准
```

### B.3 进程与线程模型（工程约束，先写死）

| 关注点 | 规则 | 原因 |
|---|---|---|
| Macha Runtime 位置 | **进程外**，只走网络 | 不嵌入 Paper，不用 JNI/Python embedding |
| 世界读写线程 | **只在 Paper 主线程**调用 Bukkit API | Bukkit API 非线程安全；异步访问世界是崩服常见原因 |
| 网络线程 | transport 独立线程；收到 action 后 `runTask` 回主线程执行 | 不阻塞网络读，也不阻塞服务器 tick |
| 事件出口 | 主线程监听 → 立即归一化为纯数据 → 投递到队列/通道 → 由网络线程发送 | 监听器里做 IO 会拖慢 tick |
| `action_result` 时序 | 异步回传，允许"已接受但未完成"的中间状态（v0 简化为 ok/refused/failed） | 真实世界动作有耗时 |

---

## C. Technology Stack（锁定版本）

### C.1 基线（当前开发基线，全部明确锁定）

| 项 | 锁定值 | 依据 |
|---|---|---|
| Minecraft Java Edition | **26.2**（Chaos Cubed，2026-06-16 发布；协议 776；数据版本 4903） | 当前 Paper 稳定线的最新正式版；[Minecraft Wiki](https://minecraft.wiki/w/Java_Edition_26.2) |
| Java（运行时与工具链） | **Java SE 25** | 26.2 的**最低** Java 版本即为 SE 25；低于此无法启动服务器 |
| Paper | **26.2，build 123**（2026-09-09，STABLE） | [PaperMC Fill v3 API](https://fill.papermc.io/v3/projects/paper/versions/26.2/builds) 实测最新稳定构建 |
| Paper jar 校验 | `paper-26.2-123.jar`<br>sha256 `7b7b3b43c009103e1971a0576c26f655a7dd9b56a0a2a4438e352c03a7fecd08` | 同一次 API 响应；写进 `03` 的可复现清单 |
| Kotlin | **2.4.20**（2026-09-07 工具版本；2.4 线支持至 2027-12-03） | [Kotlin releases](https://kotlinlang.org/docs/releases.html)；不选 12 月才发布的 2.5.0（EAP/未发布） |
| Kotlin Gradle Plugin | **2.4.20**（与 Kotlin 同版本） | 同上 |
| Gradle | **9.7.1**（2026-08-19） | [Gradle releases](https://gradle.org/releases/)；备选 **8.14.5**：若 KGP 2.4.20 的受支持 Gradle 上限不覆盖 9.7，则降到 8.14.5（scaffold 时用官方兼容矩阵确认，见 §H-D2） |
| JVM target | **25** | 跟随服务器运行时；若 KGP 2.4.20 的 `jvmTarget` 上限低于 25，则目标 **21**（字节码 21 可运行在 JDK 25 上），scaffold 时实测确定 |
| 传输 | **HTTP（控制面）+ WebSocket（双向流）** | 本阶段建议的形态；**绑定在 `transport/`**，协议本身与传输解耦 |
| 协议格式 | **UTF-8 JSON，v0**，信封采用 JSON-RPC 2.0 风格（`type`/`id`/`payload` 形状） | 见 `01-protocol-v0.md`；未来可换 gRPC/IPC/MQ 而不改协议语义 |
| 构建 | Gradle Kotlin DSL + Version Catalog + **Shadow**（打包第三方依赖） | 见 §D |
| 测试 | JUnit 5（+ kotlin-test）单测；**run-paper** 起真实服务器做集成 | 见 `03` §6 |

### C.2 选择依据（为什么是这一组）

- **为什么 Paper 而不是原版/Forge/NeoForge/Fabric**：Paper 提供稳定的**公开插件 API** 与成熟事件系统，
  无需触碰 NMS/Mojang 映射即可读到位置、实体、方块、时间与全部需要的 Bukkit 事件；插件生态与
  部署方式（丢一个 jar 进 `plugins/`）最省事。Forge/NeoForge/Fabric 让 Layer 与 mod 加载器、
  版本映射强耦合，对"薄层"是负担。
- **为什么不追最新**：26.2 是当前**正式稳定**线（26.3 尚未发布）；26.1.2 是上一条线，保留为
  **回退基线**（当 26.2 上出现阻塞性 API/生态问题时切回，protocol v0 不受影响）。
- **为什么 Kotlin 只属于 Layer**：Kotlin 的协程/空安全/密封类型适合写"协议 + 派发 + 归一化"，
  而 Macha Core 是独立系统，语言由 Core 自己决定，两者只通过网络对齐（决策记录 C2）。

### C.3 备选方案（记录，不选）

| 备选 | 为什么现在不选 |
|---|---|
| **Mineflayer（JS/Node，进程外 bot）** | 需要模拟客户端协议、无法获得服务端**权威**状态；且会把 Node 拉进技术栈。仓库内 §4.1 的定位仍是有效参考，作为**未来"进程外 Layer"路线的对照**保留 |
| **RCON / 命令桥** | 只能执行命令、拿不到结构化世界状态与事件，不满足 Observation 需求 |
| **Mod（Fabric/Forge）+ 客户端渲染** | 引入渲染/客户端分发问题，与"薄层 + 无自定义模型"的非目标冲突 |
| **Ktor / Javalin 作为 transport** | 会带 Netty（Ktor）或 Jetty（Javalin）进插件类加载器；**Paper 自身使用 Netty**，插件内嵌 Netty 易产生类加载冲突，除非整体 relocate。v0 不值得 | 
| **paperweight-userdev（NMS 映射工具链）** | v0 只用 Bukkit 公开 API，不碰 NMS；引入它等于给 Layer 绑定内部映射，升级成本高。**触发条件**：若某动作确实无法用公开 API 完成，再单独评估 |

---

## D. Dependency Rationale（每个关键依赖为什么存在）

| 依赖 | 作用域 | 为什么需要 | 注意 |
|---|---|---|---|
| `io.papermc.paper:paper-api:26.2-…` | `compileOnly` | 编译插件所需的 Bukkit/Paper API | **必须 compileOnly 且禁止打进 jar**——运行期由服务器提供；打包进去会类冲突 |
| `org.jetbrains.kotlin:kotlin-stdlib` | `implementation` | Paper 不提供 Kotlin 运行时 | 必须随插件分发（shadow 打包或 `plugin.yml` 的 `libraries`），二者选一并写进 `03` |
| `org.jetbrains.kotlinx:kotlinx-serialization-json` | `implementation` | 协议 JSON 编解码；编译期需 `kotlin("plugin.serialization")` | 选它是因为**无反射**、Kotlin 原生、可空字段表达清晰；**不要**依赖服务器内部的 Gson（版本随服务器漂移） |
| `org.java-websocket:Java-WebSocket:1.6.0` | `implementation` | WS 服务端（双向流） | 关键理由：**不依赖 Netty**，避免与 Paper 的 Netty 冲突；体积极小 |
| JDK `com.sun.net.httpserver` | JDK 内置 | HTTP 控制面（健康检查、状态查询、单发动作） | 零依赖；避免为 HTTP 再引入 Web 框架 |
| `org.jetbrains.kotlinx:kotlinx-coroutines-core`（可选） | `implementation` | 派发/节流/超时控制 | 仅在 `kit/runtime/` 使用；若 v0 用简单队列即可，则**先不加** |
| `org.junit.jupiter:*` / `kotlin-test` | `testImplementation` | 纯 Kotlin 模块单测 | 不引入 MockBukkit：v0 的 Paper 侧用真服务器集成测试，避免 mock 与真实 API 漂移 |
| `xyz.jpenilla.run-paper`（Gradle Plugin Portal） | 构建期 | 一键启动本地测试服务器（dev loop） | 版本在 scaffold 时从 Plugin Portal 取当前值；若它与 26.2 不兼容，退化方案是手工下载 §C.1 的 pin jar + 本地 `run/` 脚本 |
| `com.gradleup.shadow` | 构建期 | 打包插件 fat jar 并 relocate 第三方包 | 只 shade 运行期必需项；relocate 前缀如 `dev.macha.layer.libs.*`，防止与服务器/其他插件冲突 |

**明确不需要**：任何 LLM SDK、向量库、agent 框架、Web 框架、数据库、消息队列、NMS 映射工具、
Paper 之外的 Minecraft 依赖。

---

## E. Minimal Module Structure（模块清单；文件级结构见 `04`）

**完整、具体到文件的目录结构**在 [`04-project-structure.md`](04-project-structure.md)。此处只列模块划分：

```text
layers/                                  # Gradle 构建根（不在仓库根）
├── kit/                                  共享内核（纯 JVM，零环境依赖）
│   ├── protocol/    协议 v0 DTO / 编解码 / 版本协商 / 能力清单模型
│   ├── runtime/     LayerRuntime（会话、派发、校验、节流、EnvironmentPort）
│   └── transport/   HTTP 控制面 + WebSocket 数据面
├── minecraft/   环境：Paper 插件入口 + 适配器（唯一依赖 paper-api）     ★ 唯一允许碰 Paper
├── simulator/   环境：假环境（C4 对照条件）                            ← 纯 JVM
└── testclient/  工具：垂直切片测试客户端 + transcript 记录
```

**与建议清单的映射**：

| 建议模块 | 处理 |
|---|---|
| `lifecycle/` | 拆进 `:minecraft/plugin/`（Bukkit 生命周期）+ `:kit:runtime`（Layer 会话生命周期） |
| `observation/` | **模型**进 `:kit:protocol`（`Payloads.kt`）；**采集**进 `:minecraft/adapter/observe/` |
| `events/` | **归一化**进 `:kit:runtime`；**监听器**进 `:minecraft/adapter/events/` |
| `actions/` | **词表与校验**在 `:kit:runtime`；**执行**在 `:minecraft/adapter/action/` |
| `entities/` | **视图**在 `:kit:protocol`；**绑定/查找**在 `:minecraft/adapter/agent/` |
| `protocol/` `transport/` | 收进 `kit/`，保持零环境依赖 |

**明确不建的空目录**：`world/`、`ai/`、`npc/`、`persistence/`、`ui/`、`command/`、
层内 `docs/`（计划文档留在本目录，随拆仓再迁）。

---

## F. First Milestone（第一个可运行 vertical slice）

目标：**Minecraft → Layer → Observation → External Action → Minecraft → Event** 闭环。

| Step | 动作 | 验收（可脚本化） |
|---|---|---|
| 1 | 启动 Paper 26.2 server（run-paper，本地 `run/` 目录） | 服务器控制台出现 `Done`，可用客户端连入 |
| 2 | 加载 Minecraft Layer 插件 | 控制台出现 Layer 启动日志（version / protocol v0 / 监听端口） |
| 3 | Layer 连接/初始化 | `GET /healthz` 返回 200 + JSON；WS 客户端连上后收到 `hello_ack`（含 capability manifest） |
| 4 | 读取世界状态 | 请求一次 observation，返回 agent 的 position / rotation / health 与半径内实体/方块摘要；坐标与 `/tp` 后游戏内实际值一致（±0.1） |
| 5 | 产生一个 observation | 客户端 30 秒内至少收到 1 条 push 的 observation，字段含 `tick` 与 provenance |
| 6 | 外部发一个 action | WS 发送 `{"type":"action","action":"move","target":[x,y,z]}` 后，收到 `action_result`（`ok`），并验证 `refused` 分支（例如对超出范围的目标） |
| 7 | Minecraft 中发生对应变化 | 被绑定实体确实移动到目标点附近（游戏内可见） |
| 8 | Layer 捕获变化并回传 | 客户端收到 `event`（如 `minecraft:entity_move` / `minecraft:block_break`），含 actor / target / position / world / tick |

**判定为 v0 成立的条件**：上述 8 步由**一个脚本化的测试客户端**在 10 分钟内可重复完成；
全程无 LLM、无 Memory、无人格；**Macha Core 零改动**。

---

## G. 边界红线与"demo 便利"陷阱

### G.1 一旦出现下列任一情况，**停止并指出**（Minecraft 正在污染 Macha）

1. `kit/protocol/` 的 DTO 里出现 Bukkit/Paper 类型（`Location`、`World`、`Material`、`Entity`…）。
2. 协议**顶层信封**出现 Minecraft 专有概念（tick 作为必填顶层字段、chunk 坐标、维度 id 的硬编码枚举）。
3. 动作词表里出现 `place_block` / `craft` / `break_block` 这类环境动词，**且被当作 Core 的通用词**。
   正确形态：通用词（`move` / `look` / `interact`）+ 带命名空间的环境特有词（`minecraft:place_block`）。
4. Layer 开始存"记忆"、"信任"、"他偷了我的木头"之类的解释性状态。
5. 为了让 Core 好写，把世界的**解释**（谁是敌人、谁在生气）放进 observation。
6. 协议必须改才能容纳第二个环境（Simulator Layer 实现不了 v0 的某条消息）。

### G.2 "只是为了现在方便"却会害了未来 Layer 的设计（点名）

| 陷阱 | 后果 | 替代 |
|---|---|---|
| 用 Paper 的调度语义定义 action 时序（"主线程下一 tick 完成"） | Skyrim/Cyberpunk Layer 无法表达；Core 被迫理解 tick | `action_result` 只表达 `ok/refused/failed` + 可选 `delta`，不承诺时序 |
| observation 直接暴露 Bukkit `Location` 序列化结果（yaw/pitch/维度枚举原样透传） | 协议被 Bukkit 的数据形状绑架 | 自定义最小几何 + `world` 用命名空间字符串，附 `extras` 容纳环境特有字段 |
| capability manifest 用 Java 类名/枚举名表达 | 其他语言实现的 Layer 无法对齐，Core 读到的是 Java 语义 | manifest 用字符串能力名 + JSON Schema 形状的参数描述 |
| 把"观测窗口半径"写死成 Minecraft 的 32 格 | 其他环境没有"格" | 窗口以**语义参数 + 环境声明的上限**表达（Layer 可拒绝） |
| 事件里塞 Minecraft 材质/实体枚举 | 上层被迫依赖 Minecraft 词表 | `kind` 用命名空间，`data` 为不透明 JSON，附 `verifiability` 标记 |

---

## H. 需要人拍板的开放决定

| # | 决定 | 建议 | 影响 |
|---|---|---|---|
| D1 | 包名 / group id | 采用 `dev.macha.layer.*`（模块名即包名末段） | 影响 6 个模块的 import 前缀与 plugin.yml 的 `main` |
| D2 | Gradle 9.7.1 还是 8.14.5 | 先试 9.7.1；KGP 兼容矩阵不支持就降 8.14.5 | 影响 wrapper 与构建脚本写法 |
| D3 | 打包策略：shadow fat jar 还是 `plugin.yml` 的 `libraries` | **shadow + relocate**（离线可复现） | 影响插件体积与部署方式 |
| D4 | agent 绑定方式：真实玩家 / 现成生物 / 自定义实体 | **现成生物**（如 armor stand 或僵尸）为 v0 被测对象 | 决定 M1 的实现难度；自定义实体属非目标 |
| D5 | HTTP 与 WS 的端口与绑定地址 | `127.0.0.1:8765`（HTTP 控制面）与同端口的 WS 升级，或分端口 | 影响 `config.yml` 与安全边界 |
| D6 | `run-paper` 版本与是否引入 | 引入；版本 scaffold 时从 Plugin Portal 取；不兼容则手工 jar | 影响 dev loop |
| D7 | 事件订阅：v0 是否允许客户端选择性订阅 | 允许 `all` 与按 kind 列表订阅（实现成本低，且避免刷屏） | 影响 `event_subscribe` 是否进 v0 |
| D8 | ~~仓库放置：`layers/` 还是根级 `macha-minecraft/`~~ | **已定（2026-09-14）：`layers/` 单构建根；共享内核收进 `layers/kit/`** | 仓库根形态与未来拆仓路径 |
| D9 | ~~多 Gradle 模块 vs 单模块 + import 扫描~~ | **已定：多 Gradle 模块**（编译期边界）；退路见 `03` §7 | 构建复杂度与边界强度 |
| D10 | `layers/kit/` 的物理迁移（当前仍是平铺）+ `.kotlin/` 加入 `.gitignore` | 按决策记录 §3 的清单执行 | 影响团队 IDE 导入与构建 |

---

*Technical Foundation — PENDING. 基于 2026-09-13 全仓审计与官方版本来源。未写任何代码。*
