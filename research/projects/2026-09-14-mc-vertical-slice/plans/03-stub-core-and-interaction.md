# 计划三：Stub Core 与交互演示（M5–M6，+ M7 stretch）

> 里程碑定义见 [`../../../plans/minecraft-layer/06-next-step-plan.md`](../../../plans/minecraft-layer/06-next-step-plan.md) §0、§2。
> 预估：**M5 +1 天；M6 +1 天。** 依赖：计划二（观测/动作/事件都能跑）。
> **本计划是这条项目的终点**：玩家真的能和 NPC 交互。

---

## 前置：Stub Core（`tools/stub-core/`，P1 已定）

**它是什么**：非认知的规则式对手方，用 **Python** 写，WS 连 Layer，**收观测 → 发动作 → 处理拒绝**。
**它不是什么**：不是 Macha Core（不放进 `src/macha/`），没有 LLM、没有记忆、没有人格、没有规划。

**硬边界（写进它的 README）**

- 不得 import 任何 Minecraft 概念（不出现 `minecraft:` 之外的 Minecraft 词）
- 不得出现"记忆 / 人格 / 情绪 / 关系"字样或等价结构
- 代码里任何状态都必须能在**一次连接内**重建（无跨会话状态）

**顺带产出的价值**：这是 **C2（协议与语言无关）** 的第一份实证 —— Core 侧 Python ↔ Layer 侧 Kotlin。

---

## M5 · NPC 动起来（+1 天）

**结果**：进服靠近 → 它转头看你；站远 → 它转回原朝向。第一次"它对我有反应"。

### 规则（无状态，全部可在一帧内判定）

| 条件 | 动作 |
|---|---|
| 玩家距离 ≤ 5 格 | `look`（转向该玩家） |
| 玩家距离 > 8 格 | `look`（转回原朝向） |
| 收到 `interaction` 事件（玩家右键它） | `move`（后退两步）+ `look`（面向玩家） |
| 目标超范围 / 前置不满足被 `refused` | 记录一行日志，**不改策略**（M5 不处理失败恢复） |

### 验收

- [ ] 玩家靠近，实体朝向变化在一次可见延迟内发生
- [ ] 玩家离开，实体恢复原朝向
- [ ] Stub Core 日志里能看到：`observation → 规则命中 → action`（可贴）

---

## M6 · 与 NPC 交互（终点，+1 天）

**结果**：`06` §0 的 5 步演示脚本可复现，**不看代码的人 10 分钟能跑**。

### 步骤

1. 写**演示脚本**（一页，给不看代码的人）：进服 → 走近被注视 → 站远被忽略 → 右键被回应后退 →
   这一步开始记录
2. transcript 落盘（M9）：每条 observation / event / action / action_result 一行 NDJSON →
   `layers/run/minecraft/transcripts/<日期>-<场景>.ndjson`
3. 端到端跑一遍，把**原始输出**（日志 + JSON 片段）贴进项目 README 的 M6 行

### 验收（终点判据）

- [ ] 别人按脚本 10 分钟复现，**且能说出"它在回应我"**
- [ ] 四条硬判据同时成立：① 脚本可复现 ② Layer 内零认知 ③ `src/macha/**` 零改动 ④ 每步有原始输出
- [ ] transcript 可回放：能看到"玩家做了什么 → 它收到什么 → 它发了什么"的因果链

---

## M7 · (stretch) 双环境预演（+1 天）

**结果**：同一份 Stub Core 在 **Simulator Layer** 上跑同一份脚本，产出结构同构的 transcript。

- [ ] `:simulator` 实现 `EnvironmentPort` 并起 WS，端口与 Minecraft 版区分
- [ ] 同一份 Python Stub Core **不改代码**连上它并完成同一套规则
- [ ] 两份 transcript 的字段结构一致（值不同不算问题）

> 这一步是 **V4/V5 的预演**：证明"换环境不改 Core"，只是这次 Core 还是 Stub。

---

## 本计划之后

Layer 侧的证伪判据（V1–V5）已在 M6/M7 得到**初步**证据；正式判决在 **Phase 3**——
真 Macha Core 上线、Layer 一行不改、重跑 V1/V4。
