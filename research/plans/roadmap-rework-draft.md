# Roadmap Rework Draft — 常规 AI NPC Roadmap 在 Macha 的改造提案

> **STATUS: PENDING — 草案，未经团队审视**
>
> 本文基于对全仓的调研（README / docs / research / papers / src / site / announcements），
> 判断一份"常规 AI NPC framework roadmap"在 Macha 场景下需要哪些改动。
> 按仓库 lifecycle rule，未定稿提案先置于 `research/`；成熟后再提升进 `docs/`。
>
> **相关（2026-09-13 新增）**：本文第 ⑦⑧⑨ 步（Adapter / Capability Probe / World Interaction）
> 的边界定义已由 Layer 校准补齐：定稿见 `docs/architecture.md`，审计见
> `papers/notes/drafts/environment-integration-layer.md`，落地验证见
> `research/plans/minecraft-layer-validation-plan.md`。本文其余部分（① 勘测、② Permeability、
> ⑤ Guardrail、⑩ 三分）仍为 PENDING，未被该次校准覆盖。

---

## 0. 现状基线（调研事实）

### 0.1 代码

| 项 | 事实 |
|----|------|
| `src/macha/` | 共 140 行，7 个文件，全部为骨架 |
| `core/agent.py` | `perceive/think/act` 三个方法全部 `raise NotImplementedError` |
| `core/memory.py` | 唯一有逻辑：`retrieve()` = 取末 N 条，注释 `TODO: implement proper scoring` |
| `core/reasoning.py` | `decide()` 硬编码返回一句固定文本，注释 `TODO: call LLM` |
| `tests/test_smoke.py` | 1 个用例，因 retrieve 取末 N 条，断言恒真，**不测任何检索语义** |
| `examples/` | README 明写 "Placeholder — no cases written yet" |
| 依赖 | `pydantic` 声明但未使用；`openai/anthropic` 在 requirements 中被注释；无向量库、无 web 框架 |

**结论：代码层面等价于尚未开工。**

### 0.2 文档与结论的不一致

- `docs/architecture.md`：四层 —— Perception → Memory → Reasoning → Action
- `research/scratch/.../aetherflow-review.md` 中 Macha 骨架：**五层 —— 上述四层 + Guardrail**

**Guardrail 在正式架构文档里丢失了**，而它是 Elara 原型第五夜（"墙上的纸条"提示注入）的核心验收项。这是一处明确的文档缺陷。

### 0.3 已确立的理论核心

| 概念 | 含义 |
|------|------|
| Cognitive Field `F_a=(W_a,Φ_a,T_a,V_a)` | 观察窗 / 解释函数 / 时间记忆层 / 价值人格层 |
| Field Superposition | `F_player = F_in ⊕ F_meta`；`F_npc ⊆ F_in` |
| Perspective Gap `G` | `F_player \ F_npc ≈ F_meta` —— **缺的是场，不是信息** |
| 3+2 Primitives | Continuity、Contingency、Independence + Expression、Reciprocity |
| Relational State `R` | 有类型的解释性关系结构，**作控制变量**，非标量好感度 |
| Interpreted Event Stream | 事件经 **appraisal** 赋关系意义后再存储 |
| Grounded Compositional Agency | 真正的命题不是"任意动作"，而是可移植、可控的组合式 agency |
| Affordance | agent-对象-状态-语境 的"可做"关系 |

### 0.4 明确空白

- 多智能体：无通信协议、无社会结构模型、无组织涌现机制
- 记忆分层与反思触发：无设计（只在 docs 有雏形）
- Conformance：只有"标准应含 conformance tests"的主张，无实现
- `research/experiments/`：当前为空
- 实验轨道（Minecraft / InZOI）：无时间线、无里程碑

---

## 1. 根本冲突

> **常规 roadmap 假设"你拥有这个世界"；Macha 的场景是"你要接入一个你改不了的世界"。**

常规 roadmap 从 ①World Authoring 起，自上而下构建 —— 这是新游戏/自建世界的思路。

而 Macha 的结论（`research/world view taxonomy/draft-01.md`）是：

> Macha 真正的产品不是 NPC AI SDK，而是**让已有数字世界接纳 Autonomous Intelligence 的 Runtime**。

且两条公开实验轨道 —— **Minecraft（轨道 I）与 InZOI（轨道 II）** —— 均为已有的、不可修改的商业游戏。

方向不同，后续每一步都要跟着转。

---

## 2. 三处结构性改动

### 改动 1：① 从 Authoring 改为 Reconnaissance + 能力协商

不创作世界，而是**勘测**一个已存在的世界，并声明它能被接入到什么程度。

产出不是世界观文档，而是四样东西：

1. 世界的 `(E, S, R)` 声明
2. **Permeability 向量 `(w_S, w_R, w_H, w_E)`**
3. 八轴坐标（World View Taxonomy）
4. 引擎实际暴露的能力清单

**World View Taxonomy 的落点就在这一步** —— 它是 ① 的工具，不是独立的理论装饰。

这一步的输出直接决定 ④⑤⑥ 能长成什么样。在 Minecraft 与 InZOI 上，它会给出完全不同的答案。

### 改动 2：⑤ 与 ⑥ 之间插入独立 Guardrail 层

| 依据 | 内容 |
|------|------|
| `aetherflow-review.md` | 五层骨架含 Guardrail，`architecture.md` 四层没有 |
| `docs/prototype_portrait.md` | Elara 第五夜：提示注入必须被拦截 |
| 原型成功标准 | C01–C12 含直接/间接注入拦截 |

护栏形态由世界的**可判定性**决定：
- 高可判定 → 确定性校验（对着 state 验）
- 低可判定 → 概率性自洽 + 一致性约束

这正是 taxonomy 中 Verifiability 轴要预测的东西 —— 两条线在此接上。

### 改动 3：⑩ 按治理对象拆为三块

常规 ⑩ 把"记忆/学习/测试/调优"混在一起。在 Macha 里它们性质完全不同：

| | 治理对象 | 核心风险 |
|---|---------|---------|
| **⑩a 个体演化** | NPC 记忆巩固与反思 | **人格漂移 —— 是风险，不是目标** |
| **⑩b Canon 治理** | 世界历史 | 谁有权写历史（Living Canon） |
| **⑩c Conformance** | 系统本身 | 换模型、换后端后行为是否仍一致 |

且 Macha 的评估设计已相当具体（A/B/C/D matched-surface 对照、violation-injection、primitive ablation），
不该被压缩成"测试/调优"四个字。

---

## 3. 其余六处改动

| # | 常规做法 | Macha 需要 | 依据 |
|---|---------|-----------|------|
| 4 | ④ 感知/记忆/推理/规划 | 增加 **Appraisal（关系赋义）** 与**核心循环内的 Reflection** | interpreted event stream 是关系记忆区别于向量库的关键层；反思放到 ⑩ 太晚 |
| 5 | 关系 = 好感度数值 | **Relational State R 作控制变量** | Gap A：现有系统把 R 当存储字段，无系统让 R 驱动意图重考虑与目标竞争 |
| 6 | ⑥ API/Tools/Events | **affordance + 双向契约** | grounded compositional agency；不只是 NPC 调工具，还有世界对 NPC 的约束反馈 |
| 7 | ⑦ Unity/Unreal 清单 | **能力探测 + 统一协议** | 轨道是 Minecraft/InZOI，非引擎插件；同接口不同实现的 permeability 差异须显式表达 |
| 8 | Player 缺席 | **显式建模 Player 与认知场边界** | `G = F_player \ F_npc ≈ F_meta` 是核心论点，roadmap 中却没有玩家的位置 |
| 9 | 隐含 LLM | **model-agnostic 为横切轴** | 换模型回归测试已写进原型成功标准，贯穿所有层，非单一模块 |

---

## 4. 修订后的 Macha Roadmap（11 步 + 1 横切）

| 步 | 模块 | 与常规的关系 | 关键内容 |
|----|------|------------|---------|
| ① | **World Reconnaissance** | 改造自 ① | 勘测已有世界；产出 (E,S,R) + 八轴坐标 + 能力清单 |
| ② | **Permeability Contract** | **新增** | 写权限 `(w_S,w_R,w_H,w_E)`；Hard Canon 边界；可判定性声明 |
| ③ | World Model | 改造 | ingested 而非 authored；world-state Provider 接口；**不做大世界模拟** |
| ④ | NPC Definition + Field 边界 | 改造 | 除身份/性格/目标外，须定义 `F_a=(W_a,Φ_a,T_a,V_a)`，尤其 `W_a` 观察窗 |
| ⑤ | Cognitive Runtime | 改造 | 感知 → **Appraisal** → 记忆 → 推理 → 规划；**R 作控制变量**；Reflection 在循环内 |
| ⑥ | **Guardrail / Conformance** | **新增** | 形态由 Verifiability 决定；拦注入/canon 违背/persona 漂移；行为 delta 须可追溯到 state delta |
| ⑦ | Behavior + Affordance | 改造 | grounded compositional agency；结构化 ActionCall |
| ⑧ | World Interaction | 改造 | 双向契约：ActionCall 出，约束/拒绝/副作用回 |
| ⑨ | Adapter / Capability Probe | 改造自 ⑦ | 能力探测而非引擎清单；统一事件协议 |
| ⑩ | Execution + 关系后果回路 | 改造 | 状态变更 → **appraisal** → R 更新 → 记忆写入 → 反思触发；世界有 Mental LOD |
| ⑪ | 演化与评估（三分） | 改造自 ⑩ | ⑩a 个体演化 / ⑩b Canon 治理 / ⑩c Conformance 回归 |

**横切：Model-Agnostic Provider（LLMClient）** —— 贯穿 ⑤–⑪，非独立模块。

---

## 5. Phase 1 必须做对的三件事

> **顺序变更提示（2026-09-13）**：本节所说的 "Phase 1" 指**最小认知核心**，在 Layer-first 决策后
> 是 `docs/roadmap.md` 的 **Phase 3**。Layer 轨道（Phase 1–2）不改动本节三条结论，只是把它们
> 的时点推后；其中第 1 条（预留 world-state Provider 接口）已由 Layer Protocol 承接。
> 决策记录：`papers/notes/accepted/decision-layer-first-sequencing.md`。

改造蓝图 ≠ 立刻实现十一层。`docs/roadmap.md` 中"先做 Phase 1 最小认知核心"的判断是对的。
但以下三件事必须在 Phase 1 就做对，**因为它们事后极难改**：

1. **预留 world-state Provider 接口**
   已写入 `paper-goal-and-world-architecture.md` 的工程结论，但代码中尚无。

2. **Guardrail 从第一天就存在**
   不需要复杂，但位置必须在。否则 Elara 第五夜无从验收。

3. **记忆从第一天就存 interpreted event，而非原始对话文本**
   这不是架构洁癖，而是**数据不可逆** —— 一旦按原始文本存进去，关系赋义永远补不回来。

---

## 6. 开放问题（供团队审视）

1. ① 的勘测产出，是否需要一个可执行的工具（而非人工填表）？若是，最小版本长什么样？
2. Permeability 向量是否应在运行时动态协商，还是接入时一次性确定？
3. Guardrail 的最小可用集是什么？（若要收敛到 3 条规则，是哪 3 条？）
4. Relational State R 的数据结构草案是什么？它与"记忆"的边界在哪？
5. ⑩a 的人格漂移边界如何定义？允许多少漂移？由谁判定？
6. 多智能体在 v0.x 明确不做，但架构需预留什么接口？（当前完全空白）
7. 本提案是否应先修 `docs/architecture.md`（补 Guardrail 层），还是等整体 roadmap 定稿后一并更新？

---

*Roadmap Rework Draft — PENDING. 基于 2026-09-09 全仓调研。*
