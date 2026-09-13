# Minecraft Layer 验证计划（Concrete Layer Test Case）

> **STATUS: PENDING — 草案，未经团队审视**
>
> **顺序已定（2026-09-13 决策）**：Layer 先、Core 后。
> 见 `papers/notes/accepted/decision-layer-first-sequencing.md`。本计划据此改写：
> Macha Core 是 Phase 3，本轨道是 Phase 1–2。
>
> 定位：本文件不是"Minecraft 接入方案"，而是**用 Minecraft 验证 Layer 抽象是否成立**的工作计划。
> 定稿设计见 `docs/architecture.md`（Layer 定义、协议、边界图）；
> 审计推理见 `papers/notes/drafts/environment-integration-layer.md`。
> 与 `research/plans/roadmap-rework-draft.md` 的关系：那份是整体 roadmap 改造提案，
> 本文件只负责其中 ①（勘测）②（Permeability）⑨（Adapter / Capability Probe）三步的落地验证。
>
> **技术地基（2026-09-13 新增）**：`research/plans/minecraft-layer/`
> —— [`00-technical-foundation.md`](minecraft-layer/00-technical-foundation.md)（A–F 技术方案与版本锁定）·
> [`01-protocol-v0.md`](minecraft-layer/01-protocol-v0.md)（协议 v0 草案）·
> [`02-observation-and-events.md`](minecraft-layer/02-observation-and-events.md)（观测字段与最小事件集）·
> [`03-build-and-module-layout.md`](minecraft-layer/03-build-and-module-layout.md)（Gradle / 模块 / 边界守护）。
> 分工：本文件管**验收口径**（V1–V5 / M1–M9），子目录管**技术地基**。

---

## 0. 一句话

> 我们的目标不是 **Build Macha for Minecraft**，而是 **Build one concrete Layer to validate the
> Layer abstraction**。

Minecraft 只是第一个样本。判断标准不是"NPC 在 Minecraft 里表现好不好"，而是"这套 Layer 边界
能不能在不改 Core 的前提下换一个世界"。

---

## 0.1 唯一因变量

> 给定 Core，接入 Minecraft 所需的一切，是否**全部**落在 Layer 一侧？

| # | 判据 | 通过条件 |
|---|------|---------|
| V1 | Core 代码改动量 | 接入期间 `src/macha/` 的改动 = 0（协议缺口导致的改动算**失败**） |
| V2 | 环境泄漏 | Core 内不出现任何 Minecraft 概念（block / chunk / tick / player entity id） |
| V3 | 认知上移 | Layer 内不出现记忆、人格、动机、规划、社交判断 |
| V4 | 可替换性 | 同一 Core 构建同时跑通 Minecraft Layer 与 Simulator Layer |
| V5 | 可独立实现 | 第三方仅凭协议文档 + conformance kit 能写出一个 Layer |

**V1 是本计划的核心。** 一旦为了接通 Minecraft 而改 Core，说明协议错了——修协议，不是让 Core
认识 Minecraft。

**Layer-first 顺序带来的额外要求**：Phase 1–2 期间对手方是 **Stub Core**（非 LLM、规则式）。
V1/V4 先在 Stub Core 上成立，Phase 3 用真 Core **重测**。顺序倒置会让"把认知塞进 Layer"的诱惑变强，
Stub Core 越笨，这条诱惑越无处藏身。

---

## 1. 三个前置门（Gate 0–2）

| 门 | 产出 | 人日估算* | 依赖 |
|----|------|----------|------|
| **G0 · 环境勘测** | 最小活连接（world state + 事件流）、**探测得到的**能力清单、可判定性报告、写权限（Permeability）边界 | 2–4 | **无，今天可开工** |
| **G1 · 协议 v0 冻结** | 五类交换形状 + manifest 最小字段 + 拒绝语义 + 来源约定 + 传输约定 + conformance kit 骨架 | 1–2（评审是最大变数） | 与 G0 互相印证 |
| **G2 · Stub Core** | 非 LLM 规则式对手方：收观测 → 发 `ActionCall`；可脚本化场景 | 1 | G1 的形状 |

\* 人日估算假设 1–2 人、接口栈已选定（见 G0），不含团队评审排期。

**结论口径**：勘测今天开始；Layer 代码（M1–M9）**第 3–5 个工作日**可启动；"抽象是否成立"的判决点
（V1–V5 含模拟器对照）约在 **3–4 周**。

---

## 2. 非目标（明确不做）

- 不做完整 Minecraft mod / 商业模组。
- 不做通用 Layer Framework、多引擎抽象层、Unity/Unreal 插件。
- 不做 Minecraft 世界模拟（世界不是我们的，只勘测与接入）。
- 不在 Phase 1–2 做任何真实认知（记忆 / 人格 / 推理 / 反思 / 规划 / 护栏）——那属于 Phase 3+。
- 不在本阶段定义"所有世界都需要的能力"清单。

---

## 3. 已定的技术约束（来自决策记录）

| # | 约束 | 原因 |
|---|------|------|
| C2 | **协议必须与语言/传输无关**（JSON-RPC 形状，优先 MCP 兼容） | Core 是 Python，Mineflayer Layer 是 JS/Node；否则 Layer 的语言选择反向绑住 Core。与 `docs/research/standards_interop.md` §188（`ActionCall` 收敛到 Tool-Use 形状）一致 |
| C3 | **Stub Core 的行动词表不得含环境动词** | `place_block` 属 Minecraft Layer 的 manifest；Core 只说共同能力类（`interact` / `move` / `communicate` / `query`） |
| C4 | **Simulator Layer 不可省** | MC 先做时，它是唯一的对照条件；没有它，三周只能证明"bot 能跑" |
| C5 | **Stub 不得长成真 Core** | 否则错误的接口会被意外冻结 |

---

## 4. 待协议回答的问题（先于写 Layer）

1. 五类交换（Observation / Event / Action / Action Result / Capability）是否已经足够？
   State 是独立一类，还是 Observation 的一种查询形式？
2. Agent 自身状态（位置、背包、生命）的**真值归属**：Core、Layer，还是按字段切分？
3. 时间语义：引擎 tick 与 agent time 如何对齐？跨会话如何表示"过了三游戏日"？
4. 拒绝（refusal）的最小表达：如何区分"这个世界做不到"与"尝试了但失败"？
5. Capability manifest 的最小字段集是什么？如何避免把"文档里写了"当成"环境真支持"？
6. 可判定性（Verifiability）如何随能力上报？它决定 Guardrail 走确定性校验还是概率自洽。
7. 传输与消息边界：一次连接里谁发起、如何流式（事件推送 vs 轮询）、断线后如何重放？

---

## 5. 最小 Layer 交付物（M1–M9）

| # | 交付物 | 缺了会怎样 |
|---|--------|-----------|
| M1 | Agent 绑定：本 Core 实例对应哪个实体/窗口 | 没有视角，感知无法收敛 |
| M2 | 带来源的类型化事件流（不做解释） | Core 无法感知 |
| M3 | 限定在观察窗内的状态查询 | 边界泄漏成全知 |
| M4 | 探测得到的 Capability manifest | Core 会幻想自己会做的事 |
| M5 | ActionCall → 环境操作 的执行器 | 只有内向半边 |
| M6 | 结构化执行结果（含拒绝 + state delta） | 后果不真实 |
| M7 | 会话生命周期（连接/断开/超时/重连） | 环境会挂，agent 变僵尸 |
| M8 | 每能力的可判定性报告 | Guardrail 无形态依据 |
| M9 | 可回放 transcript（观测 + 行动 + 结果） | 边界本身不可审计 |

---

## 6. 里程碑（已按 Layer-first 排序）

1. **P0 · 勘测启动（G0，今天）** —— 选定接口栈、打通最小活连接、开始记录真实事件样本。
2. **P1 · 协议 v0 冻结（G1）** —— 五类交换 + manifest 字段 + 拒绝语义 + 来源约定 + 传输约定。
3. **P2 · Stub Core（G2）** —— 规则式对手方，词表只含共同能力类；建立"记录观测 → 断言行动"的脚本场景。
4. **P3 · Simulator Layer** —— 仓内极简环境实现协议 v0（**对照条件**，让协议在没有 Minecraft
   依赖的情况下先被证伪一次）。
5. **P4 · Minecraft Layer 最小实现** —— M1–M9；M2/M5/M6 优先，M4（能力探测）紧随。
6. **P5 · 交叉验证** —— 同一 Stub Core 跑 Simulator + Minecraft，逐条判定 V1–V5；
   每一条"为了接通而想改 Core"的冲动都转成一个协议问题记录下来。
7. **P6 · 移交 Phase 3** —— 用真 Core 重测 V1/V4，Layer 侧不改。

---

## 7. 产出（本轨道交付什么）

| 产出 | 去向 |
|------|------|
| Layer Protocol v0（规范文本） | `docs/architecture.md` 细化，或独立 spec |
| Capability manifest（探测结果） | 随 Layer 发布，不进 Core |
| 回放 transcript | `research/experiments/` |
| 协议问题清单（V1 违例记录） | 回写本文件 / `papers/notes/drafts/environment-integration-layer.md` |
| Minecraft 侧结论（世界允许什么、拒绝什么） | 与 World View Taxonomy 的 Permeability 对齐 |
| Stub Core 的脚本场景 | 作为 Core 接手前的回归基线 |

---

## 8. 开放问题

1. Simulator Layer 能否算"第二个环境"来证明通用性？还是必须第二个**真实**世界？
2. 如果 Minecraft 的能力面太特殊（方块/合成/维度），是否说明"共同能力类"本身是幻觉，应改为
   "Core 只发意图，Layer 全权翻译"？——G0 勘测结果应能回答一半。
3. 勘测（G0）需要工具化吗？最小版本是人工填表还是脚本探测？
4. 协议 v0 冻结后，允许 Layer 侧先行扩展私有 op 到什么程度而不构成"分叉"？
5. 若 P5 判定 V5 失败（无人能独立实现 Layer），是协议文档不足，还是抽象本身不成立？
