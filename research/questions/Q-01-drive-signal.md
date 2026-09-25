# Q-01 在没有玩家、没有外部任务的世界里，什么信号能让 NPC 持续产生"非重复、可满足、不漂移"的目标？

status: questioned          # observed → questioned → pre-registered → tested → supported│weakened│falsified → revised│abandoned│promoted
owner: TBD
opened: 2026-09-16
related: 路径二 [`../paths/02-intrinsic-motivation/README.md`](../paths/02-intrinsic-motivation/README.md) ·
         `architecture.md` §1.5（接收域=准入）· 路径一（IC 回流三路）· 论文原语 `independence`

## 1. Observation

- `architecture.md` §1 的 Core 是 Perception → Memory → Reasoning → Action + Guardrail；关系状态 R 是**控制变量**（状态），
  记忆是"记得"（不是"想要"）。**没有任何机制回答"它此刻想做什么"**。
- 论文的 3+2 原语里，`independence`（它有自己的生活）**至今没有实现机制**；其余四根都能靠"更会回应"改善。
- 二手材料（`intrinsic-motivation-report/…html`）归纳出四条构建路径，并指出 LLM 角色扮演的三条反方判据：
  无持久状态 / 动机来自提示 / 移除提示即消失。→ 整理后的可检索条目：[`../paths/02-intrinsic-motivation/report-four-build-paths.md`](../paths/02-intrinsic-motivation/report-four-build-paths.md)（§1 四条路径、§6.1 三条判据）

## 2. Question

**在一个没有玩家、没有外部任务的世界里，什么信号能让 NPC 持续产生"非重复、可满足、不漂移"的目标？**

- 若答案是"是"（存在这样的信号）→ `independence` 有机制，`Other` 原型可落地。
- 若答案是"否" → 内驱力整条放弃，`independence` 改由**预置 ambient 行为**实现。
- 会改变什么：`docs/architecture.md` 是否新增"drive"作为 Core 的一等内部状态；路径一 D1/D4 是否有答案。
- 文献是否已答：**没有**。调研报告 §9.2 明确"目前没有统一的内驱力度量标准"，且现有指标全部是单智能体的。

## 3. Hypotheses（≥2 个竞争；只换"drive 信号来源"这一项）

- **H-A 稳态设定点**：机制 = 若干慢变量对设定点的偏离量之和最小化 → 预测 = 在空世界里仍持续产生目标，
  且行为随 drive 此消彼长而切换 ｜ **falsifier：行为锁死在同一动作，或 drive 变化不引起行为变化。**
- **H-B 学习进度**：机制 = 用**预测误差的变化率**（非误差本身）排序候选目标 → 预测 = coverage/step 显著优于
  随机与"新奇性"基线，且 LP 随时间衰减（饱和） ｜ **falsifier：LP 排序与随机排序无差异，或瞬间饱和。**
- **H-C 赋能/affordance 寻求**：机制 = 最大化可达成动作集合（选项数）的增长 → 预测 = 出现**改造环境**的行为，
  且选项增长与实际环境改动相关 ｜ **falsifier：估计与真实选项增长无关，或行为过度保守（不动）。**
- **H-D 连接/关系驱动**：机制 = 关系状态 R 的偏离驱动接近/回避 → 预测 = 找玩家率 >0 但**有界**，
  且退场后行为不坍塌 ｜ **falsifier：无视玩家（等于无连接需求），或粘人/纠缠（contingency 被挤掉）。**

**控制组 P2-0**：无 drive（随机或纯反应）。任一设计若不显著优于 P2-0，该设计失败。

## 4. Pre-registration（**提交后不得修改**）

```yaml
prereg: <pending — 提交时回填 commit hash>
experiment: 同一 Simulator Layer 环境 + 同一 agent 接口，只替换 drive 模块；每设计 5 个种子 × 10k tick
env: layers/simulator（首轮实现）；确定性 tick；无玩家（E-1）
baseline: P2-0 无 drive（随机策略）+ 各设计的"无学习"退化版
control: 同种子重跑（复现性）；drive 关闭开关（关掉后应退化为 P2-0）
metrics: 自主目标数/时间、行为熵、coverage/选项增长、drive 满足后是否切换、无干预时长、
         行为漂移率、复现性（同种子）、找玩家率（仅 E-3）
expected: H-B 在 coverage/step 上 > H-A ≈ H-C > P2-0；H-A 在"行为可读性/切换"上最稳；
          H-C 是唯一产生环境改造的；H-D 在 E-3 上产生有界找玩家率
falsification: 任一设计相对 P2-0 无显著差异 → 该设计失败；四个全部失败 → 本问题答"否"，路径二放弃
```

**注意**：`prereg` 的 hash 只有在**提交之后**才存在。写下本块之后**先提交、再跑实验**；跑完只允许追加，
不允许修改本块。

## 5. Experiments

| ID | 设计 | 状态 |
|---|---|---|
| E-1 | 空世界：P2-0 / A / B / C | ⬜ 未开始（依赖 substrate S0） |
| E-2 | 有 affordance 世界：P2-0 / C | ⬜ |
| E-3 | 脚本玩家进出：P2-0 / D（含"退场测试"） | ⬜ |
| E-4 | 长期（10× 时长）：全部 | ⬜ |
| E-5 | 换环境（sim → Minecraft，M7 之后）：胜出者 | ⬜ |

## 6. Evidence

*（空——尚无证据。等级 E0–E3；产物路径与可重跑命令填写在此。）*

## 7. Failures

*（空——失败按 `../failures/README.md` 分类 F1–F7 归档。）*

## 8. Status history（append-only）

| 日期 | 状态 | 依据 | commit |
|---|---|---|---|
| 2026-09-16 | observed | 二手材料 + 架构缺口审计（§1） | — |
| 2026-09-16 | questioned | 通过 Gate 1：可判定 + 会改变架构 + 文献未答（§2） | — |

## 9. Next questions

- 若 H-B 胜出：LP 能否直接当作**路径一 D1（寿命类分档）**的依据？（还在学 → Chunk 短；饱和 → Chunk 长）
- 若 H-D 胜出：`independence × contingency` 的**预算仲裁**该由谁做？（IC 准入，还是算子层竞争）
- 若全部失败：预置 ambient 行为的最小形式是什么？（世界很活时它是否足够）
