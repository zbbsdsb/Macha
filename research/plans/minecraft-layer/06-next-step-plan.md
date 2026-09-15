# 下一步计划：从"能编译"到"能接入真实世界"（vertical slice）

> **STATUS: PENDING — 计划提案，含 3 项待拍板（§5）。**
> 上游：`00-technical-foundation.md` §F（8 步验收）· `../minecraft-layer-validation-plan.md`（V1–V5 / G0–G2）·
> `05-scaffold-review-2026-09-14.md`（F1–F6 已闭环）· `04-project-structure.md`（结构）。
> 本次复核基线：commit `ead3a3d`。

---

## 0. 现状基线（2026-09-14）

**已达成**

- 结构：`layers/kit/{protocol,runtime,transport}` + `minecraft`/`simulator`/`testclient`，与 `04` §1 一致。
- 边界：编译期模块依赖 + 三个守护任务（`verifyPaperScope`/`verifyEnvClean`/`verifyCoreClean`），
  已重指到 `kit/*` 并加"扫到 0 个文件即失败"防呆；`stripComments` 支持跨行块注释。
- 协议与运行时骨架：协议 v0 DTO/编解码/词表校验、`LayerRuntime`/`ActionCall`（`JsonElement` 无损）、
  `EnvironmentPort`、HTTP+WS 骨架、Paper 适配器四个子包骨架。
- 测试：**20 例 0 失败**（protocol 8 / runtime 11 / transport 1）；`minecraft-0.1.0-all.jar`（shadow）产出。

**仍是空白（本计划要补的）**

| # | 空白 | 影响 |
|---|---|---|
| G-A | **没有 dev loop**：`layers/run/` 不存在，构建里没有 run-paper；`plugin.yml api-version: '26.2'` 从未被真实服务器检验 | `00` §F Step 1–3 全部未验证 |
| G-B | **没有 Stub Core**（决策记录 C1 要求的非认知对手方）；`testclient` 只是协议探针 | 没有对手方 → 只能证明"能连"，不能证明"回路成立" |
| G-C | **8 步 vertical slice 一步未跑**：`/healthz`、`hello_ack`、observation、action、event 全未在真实环境出现 | Layer 尚未接入任何真实世界 |
| G-D | **M4 能力探测 / M8 可判定性报告 / M9 transcript** 未实现 | 无法回答"这个环境实际能做什么、结果是否可验证" |

---

## 1. 本阶段唯一目标与判据

> **目标**：在真实 Paper 26.2 服务器上跑通 `00` §F 的 8 步闭环，并由**脚本**复现。

判据（缺一不可）：

1. 8 步由 `:testclient` 的脚本在 **10 分钟内**可重复完成；
2. 全程 **Layer 内零认知**（无记忆/人格/规划/社交判断）——V3 的自检；
3. **`src/macha/**` 零改动**——V1 的自检（Core 尚未开始，这条现在等价于"Layer 不伸手要 Core"）；
4. 每一步都有**可贴出的原始输出**（日志、`/healthz` JSON、`action_result`、事件 JSON）。

---

## 2. 工作分解

| ID | 工作 | 对应验收 | 依赖 | 预估 |
|---|---|---|---|---|
| **W0** | 收尾：提交文档改动（`README`/`architecture`/`00`/`03`/`04`/`05`/决策记录）+ 补 `layers/README.md`（如何 build / 起服 / 跑测试） | 仓库无"文档说未做、实际已做"的不一致 | — | 0.5 人日 |
| **W1** | **dev loop（P2 已定：手工 pin jar + 脚本）**：版本化脚本 `layers/scripts/run-server.ps1`（下载/校验 `paper-26.2-123.jar`，sha256 `7b7b3b43…fecd08` → 放入 `layers/run/minecraft/`，首次启动生成 eula/世界）→ 加载插件 → 验证 `plugin.yml`（`api-version`、`main`、`load: POSTWORLD`） | Step 1–3：控制台 `Done` + 插件启动日志 + `GET /healthz` 200 + WS `hello_ack`（含 capability manifest） | — | 1–2 人日 |
| **W2** | **观测**：`PaperObservationCollector` + 实体/方块扫描器 + 世界状态；窗口参数与截断标记；push 节奏 | Step 4–5：position/rotation/health 与游戏内一致（±0.1）；30 秒内收到含 `tick`/provenance 的 observation | W1 | 1–2 人日 |
| **W3** | **动作**：`ActionExecutor` 回主线程执行 `move`/`look`；`refused` 分支（未声明能力、超范围） | Step 6–7：`action_result(ok)`；世界内真实位移；`refused` 有明确 `reason` | W1 | 1–2 人日 |
| **W4** | **事件**：至少实现 `entity_move`、`block_break`、`interaction`（`02` §5 的最小族：状态变化 / 世界突变 / 意图）；节流与合并 | Step 8：客户端收到事件，字段含 actor/target/position/world/tick | W1 | 1–2 人日 |
| **W5** | **Stub Core（P1 已定：Python，`tools/stub-core/`）**：非认知对手方——WS 连 Layer，收 observation → 按规则发 `ActionCall`（如"跟随最近玩家"）→ 处理 `refused`；**不放在 `src/macha/`**，并自带边界：不得 import 任何 Minecraft 概念、不得出现"记忆/人格"字样 | §1 判据 2/3；同时**第一次实证 C2（协议与语言无关：Core 侧 Python ↔ Layer 侧 Kotlin）** | 可**与 W1 并行**（只依赖协议规范文本） | 1 人日 |
| **W6** | **M4/M8/M9**：能力探测（真探测而非抄文档）、每能力可判定性报告、NDJSON transcript 落盘 + 回放 | `validation-plan` M4/M8/M9 | W2–W4 | 1–2 人日 |

**顺序**：W0 → W1 ‖ W5 → W2 → W3 → W4 → W6。W1 是咽喉（没有真实服务器，后面全是纸上作业）。

---

## 3. 本阶段结束时应当能回答的三个问题

1. **协议够不够**：真实世界里有没有出现过"五类交换装不下"的信息？（每一条都记成协议问题，不得就地在 Layer 里打补丁）
2. **能力清单真不真**：探测清单与实际可执行动作是否一致？有哪些动作是"文档说支持、探测说不支持"？
3. **可判定性如何**：哪些能力能对着真实状态核验（`checked`），哪些只能采信回报（`trusted`）？——这决定未来 Guardrail 的形态。

---

## 4. 风险与对策

| 风险 | 对策 |
|---|---|
| `plugin.yml api-version: '26.2'` 可能不被服务器接受（Paper 的 `api-version` 取值规则未核实） | W1 第一件事就是加载插件；不接受则按 Paper 报错信息调整并**回写 `03` §4** |
| 本机/团队是否有 JDK 25：`gradle.properties` 已说明本机曾连不上 `services.gradle.org`；fooJay 自动下载需要网络 | W1 先确认工具链可用；不可用则按 `00` §C.1 回退 `jvmTarget=21`（JDK 25 运行）并记录 |
| run-paper 与 26.2 兼容性未知、且需要下载服务器 jar | 备选：手工脚本下载 pin 的 `paper-26.2-123.jar`（sha256 已记录）到 `layers/run/minecraft/`，不经插件 |
| **shadow relocate 仍是 TODO**：Kotlin/WS 库未重定位，可能与其它插件类冲突 | 只影响"与其它插件共存"；本阶段单插件测试可接受，但 W0 应在 README 里写明该限制 |
| Bukkit API 必须在主线程：异步改动世界会崩服 | 已写进 `03` §6；W3 的 code review 必须逐条对照 |
| WS/HTTP 端口与本地其它服务冲突 | `config.yml` 可改端口；W1 记录实际使用端口 |

---

## 5. 已拍板（2026-09-14）

| # | 决定 | 选定 | 直接后果 |
|---|---|---|---|
| **P1** | Stub Core 放哪、用什么语言 | **Python，`tools/stub-core/`** | 仓库新增顶层目录 `tools/`（已在根 `README.md` 结构树登记）；**不放进 `src/macha/`**，避免与 Core 混淆、也让 V1「Core 零改动」保持干净；副产品 = C2 跨语言结论的第一份证据 |
| **P2** | Paper 怎么起 | **手工 pin jar + 版本化脚本** | 新增 `layers/scripts/run-server.ps1`（版本化）；jar/世界/日志落 `layers/run/`（已 gitignored）；不引入 run-paper 依赖，离线可复现 |
| **P3** | 协议 v0 冻结时点 | **边跑边冻，跑完 8 步再冻结** | 试跑期任何协议改动**必须先在 [`01-protocol-v0.md`](01-protocol-v0.md) §9「试跑期变更记录」登记**，再改代码；8 步跑完后把记录汇总为 v0 定稿（G1 关闭） |

**P3 的纪律（防止"边跑边改"退化成"边跑边失控"）**：

1. 先改文档、再改代码（仓库既有铁律）；
2. 每条变更写明：哪条消息/字段、为什么真实环境需要它、是否能被 Simulator Layer 表达（判据 J3）；
3. 出现"为了让当前 demo 好写而扩协议"的条目 → 停下来标记，而不是直接加进去。

---

## 6. 明确不做（本阶段）

LLM / 记忆 / 人格 / 规划 / 多智能体 / 自定义实体与渲染 / 对话系统 / 世界模型 / 任务系统 /
通用 Layer 框架 / Unity-Unreal 插件。**也不做 Macha Core**——Core 是 Phase 3。

---

## 7. 之后（本阶段达成后）

1. **Phase 2 收尾**：Simulator Layer 与 Minecraft Layer 跑**同一份构建**（V4 预演），并做一次
   "第三方只凭规范实现 Layer"的桌面演练（V5 预演）。
2. **Phase 3**：Macha Core（真认知）上线，Layer **一行不改**，重跑 V1/V4 —— 这才是证伪判据的真正判决点。
