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
| **M0** | 服务器活着 + 插件加载 + `/healthz` | 半天 | 🟡 部分（服务器 `Done (12.761s)` + 插件启动日志已见 `run/minecraft/logs/latest.log` 19:41:36 / 19:41:35；`/healthz` 原始输出待补） |
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

## 5. 硬边界（任何里程碑都不许破）

- **不改 `src/macha/**`**（V1）；**不扩协议字段**（要改先在 `01-protocol-v0.md` §9 登记）；
  **Layer 内零认知**（V3）；**不把服务器目录提交进 git**；**不加依赖**。
- 明确不做：LLM / 对话 / 记忆 / 人格 / 规划 / 自定义实体与渲染 / 世界模型。
