# Minecraft Layer — 计划文档（research/plans/minecraft-layer/）

> **STATUS: PENDING（全部）— 计划阶段，未写任何代码，未创建任何代码目录。**
>
> 这一目录回答的是：**用 Minecraft 实现 Macha 的第一个独立 Environment Layer，并验证 Layer
> 这个架构抽象是否成立。** 不是"开发 Minecraft NPC"。
>
> 上游依据：`docs/architecture.md`（Layer 规范定义）·
> `papers/notes/drafts/environment-integration-layer.md`（审计 A–G）·
> `papers/notes/accepted/decision-layer-first-sequencing.md`（Layer 先、Core 后 + 约束 C1–C5）。
> 验收口径在上一级：[`../minecraft-layer-validation-plan.md`](../minecraft-layer-validation-plan.md)（V1–V5 / M1–M9）。

---

## 阅读顺序

| # | 文件 | 一句话 | 主要章节 |
|---|---|---|---|
| 00 | [`00-technical-foundation.md`](00-technical-foundation.md) | 总纲：范围、非目标、架构、栈、依赖、里程碑、边界红线 | A–F |
| 01 | [`01-protocol-v0.md`](01-protocol-v0.md) | 协议 v0：信封、6 类消息、4 个动作、拒绝语义、传输绑定 | — |
| 02 | [`02-observation-and-events.md`](02-observation-and-events.md) | 观测字段与观测窗口；事件最小集（9 类/四族）与选择判据 | — |
| 03 | [`03-build-and-module-layout.md`](03-build-and-module-layout.md) | 版本锁定、打包策略、线程规则、测试策略、边界守护任务 | — |
| 04 | [`04-project-structure.md`](04-project-structure.md) | **文件夹结构（file-level）**：仓库放置、Gradle 模块依赖图、每模块文件清单、拆仓路径 | Level 1–3 |

推荐路线：**00 → 04 → 01 → 02 → 03**（先定范围与结构，再看协议与构建细节）。

---

## 各文件与验收判据的对应

| 验收判据（V1–V5） | 主要落点 |
|---|---|
| V1 接入期间 Core 零改动 | `00` §A.3 · `04` §2（模块依赖不含 Core） |
| V2 Core 内不出现 Minecraft 概念 | `03` §7 边界守护第 3 条 |
| V3 Layer 内不出现认知 | `00` §0 非目标 · `04` §5"不创建的目录" |
| V4 同一 Core 跑通两个 Layer | `04` §1–§3.5（`:runtime` + `:simulator` 共享） |
| V5 第三方可独立实现 Layer | `01`（规范文本）· `03` §7（可检查规则）· `04` §6（拆仓路径） |

最小 Layer 交付物 M1–M9 的落点：`00` §F（首个 vertical slice）· `03` §6（线程/回放）·
`04` §3.4（agent 绑定、采集、事件、执行）· `04` §3.6（transcript）。

---

## 目录约定

- 本目录只放**计划与规范草案**；实现的代码将来落在仓库根的 `layers/`（见 `04` §1），
  **不放进本目录**。
- 文档语言：中文说明 + 英文标识符/字段名（与 `research/` 其它内部草稿一致）。
- 铁律：**先改文档，再改代码**。协议字段的任何调整都必须回写 `01-protocol-v0.md`。
- 拆仓时（见 `04` §6），本目录随 Layer 一起迁移，或改为指向新仓库的链接。

---

## 状态一览

| 文件 | 状态 |
|---|---|
| `00-technical-foundation.md` | PENDING（待评审，含 9 项开放决定 D1–D9） |
| `01-protocol-v0.md` | PENDING（含 5 项待定） |
| `02-observation-and-events.md` | PENDING |
| `03-build-and-module-layout.md` | PENDING |
| `04-project-structure.md` | PENDING（含 4 项待拍板） |

**评审通过前不进入实现。**
