# 下一步计划（目标成果导向）：到"能在服务器里与 NPC 交互"

> **STATUS: PENDING — 计划提案。** 里程碑以**可演示的成果**为单位，不以任务为单位。
> 上游：`00-technical-foundation.md` §F（8 步验收）· `../minecraft-layer-validation-plan.md`（V1–V5 / M1–M9）·
> `05-scaffold-review-2026-09-14.md`（F1–F6 已闭环）· `04-project-structure.md`。
> 基线：commit `01143c1`；环境事实见 §4。
>
> **执行入口（本计划只定义"要什么"）**：`research/projects/2026-09-14-mc-vertical-slice/`
> —— 项目卡 + [`handover-checklist.md`](../../projects/2026-09-14-mc-vertical-slice/handover-checklist.md)（承接检查清单）
> + `plans/01–03`（怎么干）+ `prompts/`（可直接粘给 agent 的提示词）。

---

## 0. 终点形态（先写结果，再倒推）

**本计划的终点**：一个**不看代码的人**，按一页脚本，在真实 Paper 26.2 服务器里对一个实体做动作，
并在 **1 秒内**看到它给出**与自己的动作相关、可解释**的反应。全程无 LLM、无记忆、无人格。

**演示脚本（终点验收，5 步）**

1. 进服（平坦世界），世界里有一个由 Layer 生成的实体（`agent_001`）。
2. 走近到 5 格内 → **它转头看你**。
3. 站远 → **它转回自己原来的朝向**（不再理你）。
4. 右键它 → **它后退两步并面向你**。
5. 全程 transcript 落盘，事后可回放：能看到"玩家做了什么 → 它收到什么 → 它发了什么"。

**一句话判据**：*别人看完能说出"它在回应我"，而不是"它在播动画"。*

**四条硬判据（缺一不可）**：① 10 分钟内**脚本可复现**；② 全程 **Layer 内零认知**（无记忆/人格/规划/社交判断）；
③ **`src/macha/**` 零改动**；④ 每一步都有**可贴出的原始输出**（日志、`/healthz` JSON、`action_result`、事件 JSON）。

> 说明：本阶段**没有对话**（对话需要 Core/LLM，属 Phase 3）。这里的"交互"= **非语言反应**：
> 注视 / 避让 / 面向 / 靠拢。

---

## 1. 现状基线（2026-09-14）

| 状态 | 内容 |
|---|---|
| ✅ 真的能用 | 协议 v0（信封/消息/词表/编解码，8 例单测）；runtime（`LayerRuntime`/派发/校验/节流/`EnvironmentPort`/`ClockPort`，11 例）；`HttpControlPlane`（JDK 内置 HttpServer：`/healthz`、`/capabilities`）；插件入口装配并打启动日志；**`minecraft-0.1.0-all.jar`（shadow，2.9 MB）已产出** |
| 🕳 空壳（有签名无行为） | `WebSocketDataPlane`（`start()` 只置 `running = true`）→ **无 `hello`/`hello_ack`、无事件推送、无动作往返** |
| ❌ 缺 | `HttpControlPlane` 未注册 `/action`（`01` §5 要求）；`PaperEnvironmentPort` 标注 `TODO(scaffold)`：观测/事件/动作未接入；`PaperObservationCollector`(9 行)、`PaperEventBridge`(9)、`ActionExecutor`(10)、`AgentRegistry`(5) 全为空壳 |
| ✅ 已发生（2026-09-15） | **服务器已启动并加载插件**：`layers/scripts/run-server.ps1` + `layers/run/minecraft/`；`Done (9.701s)`；`/healthz` 实测 `{"ok":true,"protocol":"0"}`；`api-version: '26.2'` 被接受（结论已回写 `03` §4 附录） |
| ❌ 未开始 | Stub Core（`tools/stub-core/`，P1 已定）；能力探测 M4 / 可判定性 M8 / transcript M9 |

---

## 2. 里程碑阶梯（每级一个可演示成果）

| # | 成果（人能看见什么） | 判据（可贴出的原始输出） | 依赖 | 预估 | 状态 |
|---|---|---|---|---|---|
| **M0** | **服务器活着，插件加载成功** | 控制台出现 `Done` + 插件日志 `Macha Minecraft Layer v0.1.0 up — protocol v0, transport 127.0.0.1:8765`；`curl /healthz` → `{"ok":true,"protocol":"0"}` | — | **半天** | 🟡 服务器+插件已达成（`layers/run/minecraft/logs/latest.log`：`Done (12.761s)`、插件 up 日志）；`/healthz` 原始输出待补 |
| **M1** | **能握手**（外部程序连上并拿到世界/能力声明） | WS 客户端发 `hello` → 收到 `hello_ack`（含 `capabilities`、世界名、`tick` 基准） | M0 | +1–2 天 | 未开始 |
| **M2** | **能看见**（外部程序拿到 agent 视角快照） | 收到 `observation`：`position/rotation/health` + 附近实体/方块 + `tick` + `truncated`；与游戏内 `/tp` 对照 ±0.1 | M1 | +1 天 | 未开始 |
| **M3** | **能动手**（外部指令真的改变世界） | 发 `move`/`look` → `action_result(ok)` → 实体在游戏内真的动了；发超范围目标 → `refused(out_of_range)` | M1 | +1–2 天 | 未开始 |
| **M4** | **能听见世界**（玩家的动作变成事件） | 玩家拆一个方块、右键一次实体 → 各收到一条 `event`（`entity_move`/`block_break`/`interaction`），字段含 actor/target/position/world/tick | M1 | +1 天 | 未开始 |
| **M5** | **NPC 动起来**（第一次"它对我有反应"） | 进服靠近 → 收到注视（`look`）；站远 → 转回原朝向。行为由 `tools/stub-core/`（Python，规则式）驱动 | M2+M3+M4+Stub Core | +1 天 | 未开始 |
| **M6** | **与 NPC 交互（本计划终点）** | §0 的 5 步脚本：一个不看代码的人 10 分钟复现，且能说出"它在回应我"；transcript 可回放 | M5 | +1 天 | 未开始 |
| **M7** | *(stretch)* 同一份 Stub Core 在 Simulator Layer 上跑同一份脚本 | 两条环境产出同构 transcript | M6 | +1 天 | 未开始 |

**合计：半天拿到第一行绿色；此后约 5–7 人日到 M6（1 人全职）。**

**顺序**：M0 → M1 → (M2 ∥ M3 ∥ M4) → M5 → M6。**M0 是咽喉**——没有真实服务器，后面全是纸上作业。

---

## 3. 服务器与脚本的落地约定（本次已定）

```text
layers/
├── scripts/                     # ✅ 版本化：怎么起服的知识在这里
│   └── run-server.ps1           #   下载 + sha256 校验 + eula + 启动（用 JDK 25 路径）
└── run/minecraft/               # ❌ gitignored：服务器"家"目录，全部内容都不入库
    ├── paper-server.jar         #   落盘名（M0-E）；真正的锁是 sha256（见 00 §C.1）
    ├── eula.txt · server.properties
    ├── plugins/minecraft-0.1.0-all.jar
    ├── world/ · logs/ · libraries/ · versions/ · cache/
    └── transcripts/             #   M9 回放（NDJSON）
```

**规则**：`run/` 里**不放任何需要版本化的东西**；要保留的知识（pin 版本、sha256、启动方式、
`server.properties` 的关键项）写在 `layers/scripts/` 与本计划里。
`.gitignore` 已加固：`run/` + 兜底 `eula.txt` / `server.properties` / `paper-*.jar`。

---

## 4. 环境事实与风险（已实测）

| 项 | 事实 | 对策 |
|---|---|---|
| **JDK** | `PATH`/`JAVA_HOME` = **JDK 21**（Android OpenJDK）；Paper 26.2 需要 **Java 25** | **必须显式用** `C:\Users\chkev\.gradle\jdks\eclipse_adoptium-25-amd64-windows.2\bin\java.exe`（实测 = Temurin **25.0.4.1** LTS，由 foojay 在构建时下载）。脚本里写死/探测该路径，并写进 `layers/README.md` |
| **首次启动需联网** | 64.5 MB 服务器 jar + Paper 运行时下载 `libraries/`、`versions/` | 首次启动留出时间；之后可离线 |
| **客户端** | 要"看见"交互需要 **26.2 客户端** | 若暂无：M0–M4 用 `:testclient` 验证；**M5–M6 才必须真人进服**（记为本阶段外部依赖） |
| `plugin.yml api-version: '26.2'` | ~~从未被服务器检验~~ → **已确认被接受**（Paper `26.2-123`，无 incompatible 报错，插件正常加载；见 `03` §4 附录） | 无需回退；若换 Paper 版本需重验 |
| **实体自身 AI 会污染演示** | 僵尸会自己乱走，"它在回应我"会被噪声淹没 | M5 用**自身不乱跑**的实体（armor stand，或 `setAI(false)` 的僵尸）——这条必须先定 |
| WS 数据面是空壳 | M1 的真实工作量在此 | 不做流控/鉴权，只做 `hello`/`hello_ack` + 单向推送 + 动作往返 |
| `shadow relocate` 仍是 TODO | 与其它插件共存时可能类冲突 | 本阶段单插件测试可接受；写进 `layers/README.md` 限制说明 |
| Bukkit API 线程 | 世界读写只能在主线程 | `03` §6 已写死；M3 的 review 逐条对照 |
| 端口冲突 | 默认 `127.0.0.1:8765` | `config.yml` 可改；M0 记录实际端口 |

---

## 5. 已拍板（2026-09-14，沿用）

| # | 决定 | 选定 |
|---|---|---|
| **P1** | Stub Core | **Python，`tools/stub-core/`**（不进 `src/macha/`；顺带实证协议跨语言 C2） |
| **P2** | Paper 起服 | **手工 pin jar + 版本化脚本**（`layers/scripts/run-server.ps1`）；jar/世界/日志落 `layers/run/`（gitignored） |
| **P3** | 协议 v0 冻结 | **边跑边冻，跑完 8 步再冻结**；试跑期改动先在 [`01-protocol-v0.md`](01-protocol-v0.md) §9 登记，再改代码 |

---

## 6. 结束时应当能回答的三个问题

1. **协议够不够**：真实世界里出现过"五类交换装不下"的信息吗？（每条记成协议问题，不得在 Layer 里就地打补丁）
2. **能力清单真不真**：探测清单与实际可执行动作是否一致？
3. **可判定性如何**：哪些能力能对着真实状态核验（`checked`）、哪些只能采信回报（`trusted`）？

---

## 7. 明确不做（本阶段）

LLM / 对话系统 / 记忆 / 人格 / 规划 / 多智能体 / 自定义实体与渲染 / 世界模型 / 任务系统 /
通用 Layer 框架 / Unity-Unreal 插件。**也不做 Macha Core**——Core 是 Phase 3。

---

## 8. 与任务分解（W0–W6）的映射

| 里程碑 | 对应工作 |
|---|---|
| M0 | W0（收尾提交 + `layers/README.md`）+ W1 的 dev loop 部分 |
| M1 | W1 的 WS 数据面 + `/action` + 握手 |
| M2 | W2 观测 |
| M3 | W3 动作 |
| M4 | W4 事件 |
| M5–M6 | W5 Stub Core + W6 transcript（M4 能力探测 / M8 可判定性报告） |
| M7 | Phase 2 收尾：Simulator Layer 交叉验证（V4/V5 预演） |

之后：**Phase 3** —— Macha Core（真认知）上线，Layer **一行不改**，重跑 V1/V4，那才是证伪判据的真正判决点。
