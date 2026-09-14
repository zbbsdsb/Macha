# 项目文件夹结构（file-level，具体版）

> **STATUS: PENDING — 计划文档，未创建任何目录/文件。**
> 本文件把 [`00-technical-foundation.md`](00-technical-foundation.md) §A.3 / §E 的粗粒度结构
> 细化到**文件夹与文件级**，并给出模块依赖方向、依赖规则、以及未来拆仓路径。
> 版本锁定见 [`03-build-and-module-layout.md`](03-build-and-module-layout.md) §2；边界守护见同文件 §7。
>
> **包根约定**：所有模块统一用 `dev.macha.layer.*`，模块名即包名末段
> （`:kit:protocol` → `dev.macha.layer.protocol`，`:minecraft` → `dev.macha.layer.minecraft`）。
> 这样"共享内核 / 环境模块"在 import 语句里一眼可辨。

---

## 0. 本次优化的五个变化（相对上一版）

| # | 上一版 | 本版 | 为什么 |
|---|---|---|---|
| 1 | 仓库根放 `macha-minecraft/` | 仓库根放 **`layers/`**，其下按环境分模块 | v0 按约束 C4 **必须同时存在 Minecraft 与 Simulator 两个 Layer**；两者共享协议与 runtime，需要一个父目录承载"共享内核 + 环境模块" |
| 2 | 单 Gradle 模块 + 包级隔离 + lint 检查 | **多 Gradle 模块**，`:minecraft` 是唯一可依赖 `paper-api` 的模块 | 边界从"约定 + 检查"升级为**编译期强制**（越界 = 编译失败，而不是 CI 报警） |
| 3 | 只列 7 个包名 | 列出**每个模块的目录与关键文件**（含边界关键文件 ★） | "不够 specific" 的直接修复 |
| 4 | `plugin/` 与 `adapter/paper/` 两个包允许碰 Paper | `:minecraft` 模块内再分 `plugin/`（入口）与 `adapter/`（适配） | 保留包级细分的可读性，同时用模块把硬边界钉死 |
| 5 | 共享模块与环境模块平级（`layers/protocol` 与 `layers/minecraft` 是兄弟） | **`layers/kit/` 收拢共享内核**：`layers/kit/{protocol,runtime,transport}` 与 `layers/minecraft`、`layers/simulator` 并列 | 肉眼可辨"共享内核 vs 环境实现"；Minecraft 成为显式的独立子树，而不是与 `protocol` 平级（决策记录：`../../../papers/notes/accepted/decision-layers-directory-layout.md`） |

---

## 1. 仓库级放置（Level 1）

```text
Macha/                                  # 现有仓库（Python 为主，根目录禁止放 Gradle 文件）
├── src/macha/                          # Macha Core（Python）——本阶段不改
├── tests/                              # Core 的测试——本阶段不改
├── docs/ papers/ research/ reference/ site/ examples/ announcements/
│
└── layers/                             # 【新增】环境接入层：一个 Gradle 构建根，多个模块
    ├── settings.gradle.kts             # include(":kit:protocol", ":kit:runtime", ":kit:transport",
    │                                   #         ":minecraft", ":simulator", ":testclient")
    ├── build.gradle.kts                # 共享配置：toolchain、Kotlin、版本目录、边界守护任务
    ├── gradle.properties
    ├── gradle/
    │   ├── libs.versions.toml          # 所有版本唯一来源
    │   └── wrapper/                    # 锁定 Gradle 9.7.1
    ├── .gitignore                      # build/ .gradle/ .kotlin/ run/
    │
    ├── kit/                            # 【共享内核】与环境无关（纯 JVM）
    │   ├── protocol/                   #   :kit:protocol  协议 v0：DTO + 编解码 + 版本/能力协商
    │   ├── runtime/                    #   :kit:runtime   LayerRuntime：会话/能力清单/派发/结果关联/节流
    │   └── transport/                  #   :kit:transport  HTTP 控制面 + WebSocket 数据面
    │
    ├── minecraft/                      # 【环境】Minecraft Layer —— 唯一依赖 paper-api 的模块
    ├── simulator/                      # 【环境】Simulator Layer —— 纯 JVM 假环境（C4 对照条件）
    ├── testclient/                     # 【工具】垂直切片测试客户端（只依赖 :kit:protocol）
    │
    └── run/                            # 运行期产物（gitignored）：服务器目录、transcript 回放
```

> **为什么共享内核要单独收进 `kit/`**：`layers/protocol` 与 `layers/minecraft` 平级时，磁盘上看不出
> "共享内核 vs 环境实现"这条中心区分；收进 `kit/` 后，Minecraft 是与整个共享内核并列的**独立子树**，
> 读目录即可确认边界。这是纯构建布局改动，**Kotlin 包名不变**（仍为 `dev.macha.layer.*`）。
> 见 `papers/notes/accepted/decision-layers-directory-layout.md`。

**为什么是 `layers/` 而不是根级 `macha-minecraft/`**

1. **v0 就需要两个 Layer**（Minecraft + Simulator，约束 C4）。两个根级目录
   `macha-minecraft/` `macha-sim/` 会各带一套 Gradle 构建，而它们共享的 `protocol` / `runtime` /
   `transport` 无处安放（要么复制、要么上 composite build）。
2. **`layers/` 让"Layer 是一类东西"在文件系统里可见**——这正是我们校准出的架构原语。
3. **拆仓成本不变**：把 `layers/minecraft/` 整体移出即成为独立 repo `macha-minecraft/`；
   共享模块届时以已发布构件（Maven）引用，或按协议规范自行实现。
4. 未来加 `layers/skyrim/`、`layers/cyberpunk/` 只是加一个同级模块，不动根目录。

> 若团队更希望根级 `macha-minecraft/`：把本文件所有 `layers/minecraft/` 替换为
> `macha-minecraft/`，并让 `macha-minecraft/` 自己充当 Gradle 构建根（把 `protocol/` `runtime/`
> `transport/` 移入其内），其余结构不变。**不建议**把 Gradle 构建根放在仓库根（根是 Python 项目）。

---

## 2. 模块依赖图与规则（Level 2）

```text
              ┌────────────────────┐
              │   :kit:protocol    │  纯 JVM：DTO / 编解码 / 版本 / 能力清单模型
              └─────────┬──────────┘
            ┌───────────┼───────────────┐
            ▼           ▼               ▼
     ┌──────────────┐ ┌──────────────┐ ┌───────────────┐
     │ :kit:runtime │ │:kit:transport│ │ :testclient   │  纯 JVM：垂直切片测试客户端
     └──────┬───────┘ └──────┬───────┘ └───────────────┘
            └────────┬───────┘
        ┌────────────┴─────────┐
        ▼                      ▼
 ┌──────────────┐      ┌──────────────┐
 │ :minecraft   │      │ :simulator   │
 │ + paper-api  │      │ 纯 JVM       │
 └──────────────┘      └──────────────┘
```

| 模块 | 可以依赖 | 禁止依赖 | 允许 import 的环境 API |
|---|---|---|---|
| `:kit:protocol` | kotlinx-serialization | 其他一切 | 无 |
| `:kit:runtime` | `:kit:protocol` | `:kit:transport`、`:minecraft`、`:simulator` | 无 |
| `:kit:transport` | `:kit:protocol` | `:kit:runtime`、环境模块 | 无（只有 HTTP/WS 库） |
| `:minecraft` | `:kit:protocol`、`:kit:runtime`、`:kit:transport`、`paper-api`(compileOnly) | — | `org.bukkit`、`io.papermc` |
| `:simulator` | `:kit:protocol`、`:kit:runtime`、`:kit:transport` | `paper-api` | 无 |
| `:testclient` | `:kit:protocol` | `:kit:runtime`、`:kit:transport`、环境模块 | 无 |

**关键性质**：`:kit:runtime` **不依赖** `:kit:transport`——传输实现（HTTP/WS）不得渗进 Layer 逻辑；
两个环境模块**共用同一份 runtime 与 protocol**，这是 V4（同一 Core 跑通两个环境）在 Layer 侧的镜像。

**强制方式**：Gradle 模块依赖 = 编译期边界。`03-build-and-module-layout.md` §7 的 import 扫描任务
保留为**第二道防线**（捕获"模块内不该出现的环境字面量/类型引用"）。

---

## 3. 每个模块的目录与文件（Level 3）

> 下列文件为**起步骨架**：★ = 边界关键文件（评审必看），其余为常规实现文件。
> 文件命名可调整，**模块归属不可调整**。

### 3.1 `layers/kit/protocol/` — 协议 v0 参考实现（纯 JVM）

```text
protocol/
├── build.gradle.kts
└── src/
    ├── main/kotlin/dev/macha/layer/protocol/
    │   ├── Envelope.kt                ★ 信封：v / type / id / ts / payload
    │   ├── Messages.kt                ★ hello · hello_ack · observation · event · action · action_result · error
    │   ├── Requests.kt                   observation_request · event_subscribe
    │   ├── Payloads.kt                  AgentView · EntityView · BlockView · WorldView · EventPayload
    │   ├── CapabilityManifest.kt      ★ 能力清单：name / args / preconditions / effect / verifiability / cost
    │   ├── ActionVocabulary.kt        ★ 共同能力类 + 命名空间校验（无前缀=通用，`minecraft:*`=环境特有）
    │   ├── Codes.kt                     status(ok/refused/failed) · reason 码 · error 码
    │   └── ProtocolCodec.kt             Json 配置（严格模式）+ 编解码 + 版本协商
    └── test/kotlin/dev/macha/layer/protocol/
        ├── EnvelopeRoundTripTest.kt     编解码往返
        ├── VocabularyRuleTest.kt      ★ 断言 `place_block` 等环境动词**不得**通过通用词校验
        └── VersionNegotiationTest.kt    版本不兼容 → error(bad_version)
```

> `:kit:protocol` 是**Kotlin 参考实现**；协议**规范文本**是
> [`01-protocol-v0.md`](01-protocol-v0.md)。Macha Runtime 侧（未来 Python）按规范自行实现编解码。

### 3.2 `layers/kit/runtime/` — Layer 运行时（纯 JVM，环境无关）

```text
runtime/
├── build.gradle.kts
└── src/
    ├── main/kotlin/dev/macha/layer/runtime/
    │   ├── LayerRuntime.kt            ★ 生命周期 start/stop、会话建立、消息入口
    │   ├── SessionRegistry.kt          会话与订阅（all / kind 列表）
    │   ├── ActionDispatcher.kt        ★ action → 校验 → 执行 → 结果回传（不阻塞网络线程）
    │   ├── ActionValidator.kt         ★ 能力存在性 + 前置条件 → 产生 refused（含 reason）
    │   ├── ResultCorrelator.kt          action id ↔ action_result 关联与超时
    │   ├── ObservationScheduler.kt      观测窗口编排、push 间隔、无变化跳过
    │   ├── EventThrottle.kt             事件节流/合并（如 entity_move）、有界队列与丢弃计数
    │   └── port/
    │       ├── EnvironmentPort.kt     ★ 环境侧唯一接口：collect() / execute() / subscribe()
    │       └── ClockPort.kt             时间来源（避免直接依赖环境 tick 语义）
    └── test/kotlin/dev/macha/layer/runtime/
        ├── RefusalTest.kt             ★ 未声明能力/前置不满足 → refused 而非 error
        ├── DispatchOrderTest.kt         派发与结果关联
        └── ThrottleTest.kt              事件节流与截断标记
```

**`EnvironmentPort` 是本结构里最重要的接口**：`:minecraft` 与 `:simulator` 各自实现它，
`:kit:runtime` 只认这个接口——"环境接入"因此被压缩成一个可被第二个环境复用的契约。

### 3.3 `layers/kit/transport/` — 传输（HTTP + WS，不认环境）

```text
transport/
├── build.gradle.kts
└── src/main/kotlin/dev/macha/layer/transport/
    ├── TransportServer.kt             ★ 接口：start/stop/onMessage/send
    ├── HttpControlPlane.kt              /healthz · /capabilities · /action
    ├── WebSocketDataPlane.kt            ws://…/ws：推送 + 往返
    ├── Connection.kt                    连接状态、心跳、关闭原因
    ├── SessionHandshake.kt              hello / hello_ack 握手与版本协商
    └── JsonFraming.kt                   帧编解码（唯一知道"消息以 JSON 文本传输"的地方）
```

### 3.4 `layers/minecraft/` — Minecraft Layer（唯一可依赖 paper-api）

```text
minecraft/
├── build.gradle.kts                   ★ 唯一出现 paper-api 的构建文件
└── src/
    ├── main/kotlin/dev/macha/layer/minecraft/
    │   ├── plugin/                                  # 入口与装配（允许 import Paper）
    │   │   ├── MachaMinecraftPlugin.kt  ★ JavaPlugin：onEnable/onDisable，装配 runtime+transport+adapter
    │   │   ├── PluginWiring.kt            依赖装配：把 EnvironmentPort 实现注入 runtime
    │   │   └── config/LayerConfig.kt      config.yml 映射（bind/port/token/window/订阅/日志）
    │   │
    │   └── adapter/                                 # 环境适配（允许 import Paper）
    │       ├── PaperEnvironmentPort.kt  ★ EnvironmentPort 的 Paper 实现
    │       ├── agent/
    │       │   ├── AgentRegistry.kt        agent id ↔ 实体绑定（主键用内部 id，UUID 进 extras）
    │       │   └── PaperAgentHandle.kt     单个 agent 的读写句柄
    │       ├── observe/
    │       │   ├── PaperObservationCollector.kt ★ 主线程采集 → 纯 DTO
    │       │   ├── NearbyEntityScanner.kt        半径内实体（上限 + 截断标记）
    │       │   ├── NearbyBlockScanner.kt         半径内非空气方块（按距离截断）
    │       │   └── WorldStateReader.kt           time_of_day / dimension
    │       ├── events/
    │       │   ├── PaperEventBridge.kt   ★ 监听器注册 + 只做归一化 + 入队（禁止 IO）
    │       │   ├── PresenceEvents.kt        player_join / player_quit
    │       │   ├── EntityLifecycleEvents.kt entity_spawn / entity_despawn
    │       │   ├── MovementEvents.kt        entity_move
    │       │   ├── DamageEvents.kt          entity_damage
    │       │   ├── BlockEvents.kt           block_break / block_place
    │       │   └── InteractionEvents.kt     interaction
    │       └── action/
    │           ├── ActionExecutor.kt     ★ 主线程执行分发（runTask 回主线程的唯一入口）
    │           ├── MoveAction.kt            move
    │           ├── LookAction.kt            look
    │           ├── InteractAction.kt        interact
    │           ├── SpawnAgentAction.kt      spawn_agent
    │           └── ActionMapping.kt         通用词 → Paper 操作映射（环境特有 `minecraft:*` 在此登记）
    └── main/resources/
        ├── plugin.yml                   ★ name / version / main / api-version
        └── config.yml                     §5 配置项
```

**命名空间的落地点**：`ActionMapping.kt` 是"通用能力类 → Paper 操作"的唯一映射点；
环境特有动作（`minecraft:place_block` 等）将来也只在这里登记，**不进 `:kit:protocol` 的通用词表**。

### 3.5 `layers/simulator/` — 假环境（纯 JVM，C4 对照条件）

```text
simulator/
├── build.gradle.kts                   ★ 不得出现 paper-api
└── src/
    ├── main/kotlin/dev/macha/layer/simulator/
    │   ├── SimulatorEnvironmentPort.kt ★ EnvironmentPort 的假实现（网格世界 + 少量实体）
    │   ├── SimWorld.kt                   状态与时间推进（不套用 Minecraft tick 语义）
    │   ├── SimEntities.kt                实体移动/生成
    │   ├── SimEvents.kt                  产生与 Minecraft 同 kind 的事件（检验判据 J3）
    │   └── SimulatorMain.kt              独立进程入口（便于交叉验证）
    └── test/kotlin/dev/macha/layer/simulator/
        └── ProtocolParityTest.kt      ★ 断言 simulator 能产生 v0 全部消息类型（协议可移植性）
```

### 3.6 `layers/testclient/` — 垂直切片测试客户端

```text
testclient/
├── build.gradle.kts
└── src/main/kotlin/dev/macha/layer/testclient/
    ├── VerticalSliceProbe.kt          ★ 8 步闭环脚本（对应 00 §F）
    ├── HelloProbe.kt                    握手 + 能力清单打印
    ├── MoveProbe.kt                     action → action_result → 等 event
    └── TranscriptRecorder.kt          ★ M9 可回放 transcript（NDJSON 落盘）
```

### 3.7 运行期目录（gitignored）

```text
layers/run/
├── minecraft/                          # run-paper 的服务器目录（paper-26.2-123.jar、world/、plugins/）
└── transcripts/                        # M9 回放文件（按日期 + 场景命名）
```

---

## 4. 与建议结构的映射（参考清单 → 实际落点）

| 建议 | 落点 | 说明 |
|---|---|---|
| `lifecycle/` | `minecraft/plugin/MachaMinecraftPlugin.kt` + `kit/runtime/LayerRuntime.kt` | Bukkit 生命周期与 Layer 生命周期分开，各自归位 |
| `observation/` | `kit/protocol/Payloads.kt`（模型）+ `minecraft/adapter/observe/`（采集） | 模型共享、采集环境特有——最常被弄混的一处 |
| `events/` | `kit/protocol/`（事件 payload）+ `kit/runtime/EventThrottle.kt` + `minecraft/adapter/events/` | 归一化共享，监听器环境特有 |
| `actions/` | `kit/runtime/ActionValidator+Dispatcher`（词表与校验）+ `minecraft/adapter/action/`（执行） | 校验共享、执行环境特有 |
| `entities/` | `kit/protocol/Payloads`（视图）+ `minecraft/adapter/agent/`（绑定） | 不单独建模块：内容不足以成为模块 |
| `protocol/` `transport/` | 收进 `kit/`，保持零环境依赖 | `:kit:protocol` / `:kit:transport` 不得反向依赖环境模块 |

---

## 5. 明确**不创建**的目录（现在）

```text
layers/minecraft/world/               # 世界模型不是 v0 的事
layers/*/ai/ · npc/ · persona/        # 认知属于 Macha Core，永不在 Layer
layers/*/persistence/                 # v0 不需要持久化（transcript 落盘除外）
layers/*/ui/ · renderer/ · model/     # NPC Renderer / 自定义模型属非目标
layers/*/command/                     # 除非加一条调试命令，否则不建
layers/minecraft/docs/                # 计划文档留在 research/plans/minecraft-layer/，随拆仓再迁
layers/docker/ · .github/             # 部署与 CI 是后续议题
```

> 呼应 `00-technical-foundation.md` §E：**不为了架构漂亮创建空目录**。上表是"刻意不建"的清单，
> 与 §3 的"必须建"形成对照。

---

## 6. 拆仓路径（未来，不是现在）

| 拆分 | 从 | 到 | 前置条件 |
|---|---|---|---|
| Minecraft Layer 独立 | `layers/minecraft/` | 独立 repo `macha-minecraft` | 共享模块以 Maven 构件发布，或按协议规范自行实现 |
| 共享内核独立 | `layers/kit/protocol` `kit/runtime` `kit/transport` | `macha-layer-kit`（或留在 Core repo） | 出现第二个独立实现的 Layer（V5 的实证） |
| Simulator 独立 | `layers/simulator/` | 可留仓内 | 它是**对照条件**，留仓内更划算 |

约束：`layers/` 构建**不得引用仓库上级路径**（不读 `src/`、不用 `includeBuild`），
这样"移出即独立"永远成立。

**升级触发条件**（满足任一条即应改用"独立构建根/独立仓"：决策记录 §4 T1–T4）：
① Kit 与 Minecraft Layer 需要独立发版；② 出现仓外第三方环境实现；③ 要做 V5 验证；
④ 两者构建配置开始互相牵制。

---

## 7. 待拍板

1. ~~`layers/` vs 根级 `macha-minecraft/`~~ → **已定：`layers/` 单构建根**，且共享内核收进 `layers/kit/`
   （决策记录 `decision-layers-directory-layout.md`；升级触发条件见 §6）。
2. 包根 `dev.macha.layer.*` 是否采用（影响全部模块的 import 前缀与 group id）。
3. ~~是否接受"多 Gradle 模块"~~ → **已定：多模块**（编译期边界）；退路见 `03` §7。
4. `:minecraft` 内的领域包用 `adapter/` 还是 `adapter/paper/` 命名（本文件用 `adapter/`，
   因为模块名已表明环境；若模块将来内含多环境适配，再改回 `adapter/paper/`）。

---

*PENDING。本文件只描述结构，未创建任何目录或代码文件。*
