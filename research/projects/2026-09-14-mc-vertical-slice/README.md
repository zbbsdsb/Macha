# 项目：MC Layer 垂直切片（2026-09-14 起）

> **STATUS: 进行中 — 里程碑 M0 未开始（服务器零次启动）。**
> **本目录只放"怎么干"（执行）；"要什么"在 [`../../plans/minecraft-layer/06-next-step-plan.md`](../../plans/minecraft-layer/06-next-step-plan.md)；
> "设计规范"在 [`../../plans/minecraft-layer/00-technical-foundation.md`](../../plans/minecraft-layer/00-technical-foundation.md)。**

---

## 1. 项目一句话

在真实 Paper 26.2 服务器里，让一个实体由 Macha Layer 接入、由 **Stub Core（Python，非认知）** 驱动，
玩家能对它做动作并看到**与自己的动作相关的反应**；全程无 LLM、无记忆、无人格，可回放。

**终点验收**：一个**不看代码的人**按脚本 10 分钟复现，看完能说出"**它在回应我**"。

## 2. 里程碑（定义以 `06` 为准，此处只做索引）

| # | 成果 | 预估 | 状态 |
|---|---|---|---|
| **M0** | 服务器活着 + 插件加载 + `/healthz` | 半天 | ✅ 2026-09-15（`Done (9.701s)`；插件 up 日志；`/healthz` 实测 `{"ok":true,"protocol":"0"}`；`/capabilities` 实测 4 条；`run/` 未入库。**遗留见 `plans/01` §M0 遗留修正**） |
| **M1** | 能握手（`hello` → `hello_ack`） | +1–2 天 | ⬜ |
| **M2** | 能看见（observation） | +1 天 | ⬜ |
| **M3** | 能动手（`move`/`look` + `refused`） | +1–2 天 | ⬜ |
| **M4** | 能听见世界（三类事件） | +1 天 | ⬜ |
| **M5** | NPC 动起来（Stub Core 规则反应） | +1 天 | ⬜ |
| **M6** | **与 NPC 交互（终点）** | +1 天 | ⬜ |
| **M7** | *(stretch)* Simulator Layer 跑同一脚本 | +1 天 | ⬜ |

## 3. 计划（本目录 `plans/`）

| 计划 | 覆盖 | 文件 |
|---|---|---|
| 计划一 | M0–M1：起服、加载、握手 | [`plans/01-server-and-handshake.md`](plans/01-server-and-handshake.md) |
| 计划二 | M2–M4：观测、动作、事件 | [`plans/02-observe-act-events.md`](plans/02-observe-act-events.md) |
| 计划三 | M5–M6：Stub Core 与交互演示 | [`plans/03-stub-core-and-interaction.md`](plans/03-stub-core-and-interaction.md) |

## 4. 接手先读（顺序）

1. [`handover-checklist.md`](handover-checklist.md) —— **承接检查清单**（逐条打勾才算接手）
2. [`../../plans/minecraft-layer/06-next-step-plan.md`](../../plans/minecraft-layer/06-next-step-plan.md) §0–§4
3. [`../../plans/minecraft-layer/05-scaffold-review-2026-09-14.md`](../../plans/minecraft-layer/05-scaffold-review-2026-09-14.md) §5（现状证据）
4. 本目录对应的那份 `plans/0N-*.md`

## 5. 环境（**两个**，一份 Layer 构建）

| | 本地 dev loop | **云端实验环境** |
|---|---|---|
| 地址 | `127.0.0.1:25565`（`layers/run/minecraft/`） | **`play.simpfun.cn:15463`**（`43.248.103.155`） |
| 服务端 | Paper **1.20.1** build 196（sha256 pin，见 `plans/00`）← **P0 切换后** | **Arclight 1.20.1**（Forge 混合端，protocol 763） |
| Java | **17** | **17** |
| 角色 | 可复现的**研发/调试**回路 | **实验环境**（团队决定，非演示服） |
| 传输 | `transport.mode: listen` | **`transport.mode: dial`**（Layer 主动拨出；托管面板不开放任意 TCP） |
| 客户端 | **1.20.1 客户端** | **1.20.1 客户端** |

> 版本对齐的理由：云端是 **Arclight**（Bukkit 实现是子集，事件行为可能不同）。
> 让两边**同版本、不同实现**，"行为差异"才只可能来自实现，而不是版本。

→ 构建目标取**下界**：Bukkit/Spigot API **1.20.1** + **Java 17**，禁用 Paper 专有 API。
决策记录：[`../../../papers/notes/accepted/decision-arclight-cloud-environment.md`](../../../papers/notes/accepted/decision-arclight-cloud-environment.md)。

**实验环境的确定性控制**（因为它是实验环境，不是演示服）：whitelist、固定世界与种子、跑批期间无第三方玩家、
上传 jar 记 sha256、每次跑批记录 jar sha + 世界快照、原始证据落 transcript。

## 6. 硬边界（任何里程碑都不许破）

- **不改 `src/macha/**`**（V1）；**不扩协议字段**（要改先在 `01-protocol-v0.md` §9 登记）；
  **Layer 内零认知**（V3）；**不把服务器目录提交进 git**；**不加依赖**。
- 明确不做：LLM / 对话 / 记忆 / 人格 / 规划 / 自定义实体与渲染 / 世界模型。

## 7. 下一步顺序（重心：**外部信息源** = Layer/plugin 的入站半边）

```text
P0 基线切换（plans/00）  ← 先把版本/构建/传输对齐，否则后面全返工
   ↓
M1 握手（plans/01）      ← WS 数据面 + hello/hello_ack + /action
   ↓
M2 观测（plans/02）      ← 快照：位置/朝向/生命/附近实体与方块/世界时间 + window/truncated
   ↓
M4 事件（plans/02）      ← 事实流：entity_move / block_break / interaction
   ↓
M3 动作（plans/02）      ← 出站半边（move/look + refused）；到这一步回路才闭合
   ↓
云端 dial 验证 → M5 Stub Core → M6 与 NPC 交互
```

**为什么把 M4 提到 M3 前面**：本题明确"重心放在外部信息源（入站）"。
M2 + M4 是**纯入站**，而且**不需要 Core**——一个真人玩家进服就能产生事件、就能验收；
M3 是出站，留到入站稳了再做（M5/M6 才真正需要它）。

### 外部信息源的验收定义（inbound half 的 DoD）

入站半边算"合格"，必须同时满足：

1. **事实**：只有 actor / target / position / world / tick / 原始数据，**没有解释**（无情绪、无关系、无意图）；
2. **有界**：观测窗口 + `truncated` 标记**不撒谎**（截断必须被标出，且不报错）；
3. **有序**：事件与快照共享同一 `tick` 基准，**可按 tick 排序、可对齐**；
4. **可重放**：原始证据落 transcript（M9），能重建"玩家做了什么 → 它收到什么"；
5. **可判定性**：每个字段/能力标 `checked` 或 `trusted`；
6. **能力清单是探测得到的**：不声明做不到的动作（M4 能力探测）。

> 第 3、4 条是**为未来 Core 的"准入"（`Intake`，见 `architecture.md` §1.5 / 路径一 D7）预置的契约**：
> 现在满足它们，将来 Core 侧就不需要写兼容层。
