# Macha Research Methodology v1.0

> **状态**：v1.0（2026-09-14）。**规范文档**——团队按此工作。
> **它是什么**：一套让 Macha 团队能持续区分"我们以为是真的 / 我们有理由认为是真的 / 我们真正通过实验知道的"的**最小协议**。
> **它不是什么**：不是论文模板，不是 grant 申请书，不是项目管理工具，也**不决定什么是真理**。
> **设计理由与被拒绝的方案**：[`research-methodology-design.md`](research-methodology-design.md)。
> **与既有规则的关系**：`team-workflow.md` 管**材料与论文**（引用纪律、provenance、claim threshold、生命周期）；
> 本文管**研究过程**（问题→假设→实验→证据→结论）。两者互补，**不建立第二套冲突规则**。

---

## 0. 三层分工（先分清，再谈方法）

| 层 | 回答的问题 | 产物 | 存放 |
|---|---|---|---|
| **Research** | **我们不知道什么？** | Question · Hypothesis · Experiment · Evidence · Failure | `research/questions/`、`research/experiments/`、`research/failures/` |
| **Engineering** | 已知怎么做，**如何可靠实现**？ | Plan · Project · Code · Tests | `research/projects/`（执行）、`layers/`、`src/` |
| **Paper** | 我们最终**声称发现了什么**？ | Claim（含等级与限制） | `papers/notes/`、`papers/` |

**一条判据**：
> 如果这件事**不改变"我们相信什么"**，它是工程；
> 如果它改变了、却拿不出 **E2 及以上**证据，它是一个 **draft claim**，不是发现。

**推论（必须写进团队共识）**：
- "代码写出来了" ≠ "研究完成了"。
- **Minecraft Layer 的 8 步 vertical slice / V1–V5 是工程验收，不是 Macha 的研究方法。** 它证明的是"这个 Layer 抽象能跑"，不是任何关于玩家/关系/认知的主张。第一个 Environment Layer 的实验设计不得被当作总体实验方法。

---

## 1. 核心模型

```text
Observation ──▶ Question ──▶ Hypotheses(≥2) ──▶ Model ──▶ Prediction
                    ▲                                          │
                    │                                          ▼
                 Failure ◀── Experiment ◀── Falsification条件（预注册）
                    │              │
                    │              ▼
                    │           Evidence ──▶ Claim ──▶ Artifact(论文/系统/Benchmark)
                    │                                     │
                    └────────────── New Question ◀────────┘
```

**为什么不照抄这条链**：真实研究不是流水线。三条**回路**与主线同等重要：

- **Failure → New Question**：失败是资产（§7）。
- **Unexpected Result → New Hypothesis**：意外结果不是噪声，是假设生产器。
- **Contradiction → Competing Hypotheses**：冲突结果**不许二选一**（§4）。

**唯一不可让步的顺序**：`Prediction`（含反驳条件）必须在**跑实验之前**冻结；其余环节可以来回走。

---

## 2. 研究对象（6 个 + 2 个内嵌记录）

> 只保留真正会被使用的对象。**对象上限 = 6**（见 §12 预算条款）。

### 2.1 Question（问题）

| 项 | 内容 |
|---|---|
| 解决什么 | 把"一个奇怪现象"变成**可被回答**的东西；防止研究漂移 |
| 谁创建 / 何时 | 任何人，在看到 Observation 之后；**一个文件一个问题** |
| 必须包含 | 可判定的一句话问句；**若答案是"是/否"，会改变什么**（claim / 决策 / 设计）；已知文献是否已答（链接 dossier） |
| 何时变状态 | 每次新增证据或失败时（append-only 历史） |
| 何时失效 | 被回答、被证明不可判定、或已被现有文献回答 → `abandoned`/`promoted` |
| 关系 | 1 Question ── n Hypothesis ── n Experiment；产出 n Claim |

**什么观察值得成为 Question**（Gate 1 的判据）：
1. 它**反直觉或有冲突**（与现有 claim、与常识、与另一个结果矛盾）；或
2. 它**改变设计/主张**（回答之后我们会做不同的事）；或
3. 它**可被判定**（存在一个能给出"是/否/方向"的观测）。

三条缺任何一条 → 先记为 `research/scratch/` 里的观察笔记，**不要**升为 Question。

### 2.2 Hypothesis（假设）

| 项 | 内容 |
|---|---|
| 解决什么 | 给出**机制**，从而让预测成为必然而非巧合 |
| 必须包含 | 机制（一句因果/结构说明）+ 可观测预测 + **falsifier（什么结果会杀死它）** |
| 关键约束 | 每个 Question **至少 2 个互相竞争**的 Hypothesis（Strong Inference） |
| 何时失效 | 被 falsify（→ Failure 记录）或被更简假设吸收 |

**四个词的区别（团队最容易混）**

| 词 | 定义 | 判据 |
|---|---|---|
| **Idea** | 还没想清的念头 | 写不出预测 → 不是假设 |
| **Assumption** | 我们**选择**不去验证的前提 | 必须显式标注，可被后续实验推翻 |
| **Claim** | 我们希望别人**相信**的陈述 | 需要证据等级支撑 |
| **Hypothesis** | 一个**可被杀死**的机制解释 | 必须有预测 + falsifier |

### 2.3 Model（模型）

**不是独立对象**，而是 Hypothesis 的 `mechanism` 字段被形式化后的形态（公式、状态机、结构图）。
它存在的唯一理由：**让预测可以被别人推导出来**——因此它必须能被写成"输入→输出"的形式，而不是叙述。
若模型本身是论文贡献，它作为 **Claim（type=model）** 进入 §2.5。

### 2.4 Experiment（实验）

见 §5 的 16 项协议。**Prediction 是 Experiment 的冻结字段**，不是独立对象（原设计把它单列，red-team 后合并）。
**一次实验只回答一个 Question**；没有 Question 的实验属于工程验收，不叫研究。

### 2.5 Evidence（证据）

见 §3。Evidence **不单独建目录**——它由 Experiment 的产物（日志、transcript、脚本、数据）与记录构成，
索引在 Question 文件里；文献证据继续住在 `research/literature/`（既有 dossier 体系）。

### 2.6 Failure（失败）

见 §7。**独立目录** `research/failures/`（因为失败最容易被悄悄丢掉）。

### 内嵌记录 A：Prediction（冻结块）

写在 Question 文件的 `Pre-registration` 区块：环境 pin、baseline/control、metrics、期望方向与量级、
**反驳条件**。提交后**不得修改**（§4）。

### 内嵌记录 B：Status history（append-only）

每个 Question 文件末尾的状态历史：`日期 + 状态 + 依据 + commit`。**状态与证据同一次提交更新**。

### 2.7 Claim（结论）

| 项 | 内容 |
|---|---|
| 必须包含 | 陈述 + **证据等级** + limitations + 可反驳条件 + 支撑它的 Question/Experiment 链接 |
| 类型 | `empirical` / `model` / `engineering` / `synthesis`（synthesis = 对多个 claim 的 claim） |
| 规则 | **Claim 的强度不得超过其证据等级**（§3）；冲突 → §4 的 competing 状态 |
| 存放 | `papers/notes/`（沿用既有 maturity tier：drafts → accepted → archive），**不新建第二套** |

### 2.8 Artifact（产物）

论文 / 系统 / Benchmark / 数据集 / 规范。Artifact 只继承**已经过 Gate 4 的 Claim**；
不应把未定级的东西写进 artifact 的"贡献"列表。

---

## 3. 证据标准

### 3.1 等级（等级是 claim 的**上限**，不是分数）

| 等级 | 形态 | 可支持的最强 claim |
|---|---|---|
| **E0** | Demo / 单次演示 / 截图 / 视频 | **只能**支持"可实现 / 可跑通"（engineering claim） |
| **E1** | 单案例观察，含 provenance 与可重跑命令 | 支持"某条件下观察到 X"（存在性，不可外推） |
| **E2** | **对照实验**：baseline + control + 预注册方向一致 | 支持"X 导致/改善 Y（在该环境内）" |
| **E3** | **复制或跨环境**：第二个实现/环境/独立复现，或通过一次预注册的**破坏性检验**（violation-injection / ablation） | 支持"该结论不依赖单一实现/环境" |

**因果语言（cause / because / leads to）只在 E2 及以上允许**——E0/E1 只能描述共现。

### 3.2 四条禁令

- **Demo ≠ Evidence**
- **Observation ≠ Evidence**
- **Correlation ≠ Causation**
- **One successful example ≠ Generalization**

### 3.3 与既有规则的连接（不重复造第二套）

| 既有规则（`team-workflow.md`） | 本方法如何衔接 |
|---|---|
| A2 provenance / A4 状态流 | 文献证据的 provenance 仍按 A2；本方法只要求 Experiment 产物也有 provenance（路径 + 可重跑命令） |
| **B4 claim threshold**（可引用来源 / 已批准结论 / 显式假设） | **不变**。本方法的证据等级是 B4 的**上游**：E2+ 才有资格把结论从 draft 升级为 accepted |
| B3 citation discipline | 不变。本方法不放松任何引用要求 |
| B5 versioning / contradiction | 不变。本文的 §4 只补充**实验层**的版本与冲突处理 |
| `papers/notes` maturity tier | Claim 直接沿用，不新建状态体系 |

---

## 4. 证伪协议（Falsification Protocol）

**任何重要 Hypothesis 在被测试前必须回答**：

> **"如果出现什么结果，我们会承认这个假设是错的？"**

### 4.1 预注册（Pre-registration）

跑实验**之前**，在 Question 文件写下并提交：

```yaml
prereg: <commit hash>          # 冻结凭证；版本管理交给 git，本方法不造第二套版本号
experiment: <设计一句话>
env: <环境/数据集 pin（版本号或 sha）>
baseline: <对照>
control: <控制组>
metrics: <指标及其计算脚本路径>
expected: <方向 + 量级>
falsification: <什么结果会杀死哪个假设>
```

**规则**

1. 预测、支持条件、反驳条件**三者缺一不可**；
2. 提交后**不得修改**预测块；如需修改 → **新增一块**并在状态历史记明"为什么改"，旧块保留；
3. 实验开始后修改预测 = **该实验作废**（进 Failure，类型 F4 实验失败）；
4. 冻结凭证就是 commit hash——**不要**在 markdown 里维护版本号。

### 4.2 结果对照（必须四选一，不许含糊）

| 结果 | 状态转移 |
|---|---|
| 与预测方向一致 | `supported`（证据升级，但仍受 §3 等级上限约束） |
| 与预测相反 | `falsified` → 进 Failure（F1/F2）+ 生成新 Question |
| 部分一致 / 量级不符 | `weakened` → 进入 competing 状态（§4.3） |
| 无法判定（噪声、混淆、样本不足） | **不算结论** → 记 F4/F5，修设计重跑 |

### 4.3 冲突结果

**禁止二选一。** 冲突必须进入 **competing hypotheses** 状态，直到出现一个能**区分二者**的决定性实验。
若长期无法区分 → 明确记为"该问题在当前环境下不可判定"，并写出需要什么条件才能判定。

### 4.4 防"先有结论再找证据"（motivated reasoning）

四道防线，按成本从低到高：

1. **时间戳**：预注册先于实验（git 可验证）；
2. **≥2 竞争假设**：单假设实验本质上无法构成推断；
3. **baseline + control 强制**，人评时**先隐藏系统身份**（matched-surface 设计已存在于 `roadmap-rework-draft.md` §2 改动 3）；
4. **反例优先**：每个 claim 必须先写下"什么会杀死它"，并**安排一次专门尝试杀死它的实验**。

**防"为自己的架构设计实验"**：任何实验若不能被表述为"哪个假设会被杀死"，就不许跑——
它一定是论证而不是检验。

**防 Benchmark 过拟合**：
- benchmark 一旦用于调参，**不得**再用作最终证据（须 hold-out 或预注册测试集）；
- 报告数字必须来自**与提交脚本同源**的计算（禁止手工誊写）；
- benchmark 的题目/阈值变更 = 新版本（旧结果不迁移）。

---

## 5. 实验协议（16 项最小集）

一次高质量实验**至少**包含以下字段。缺项 → 卡在 Gate 3 之前。

| # | 字段 | 要点 |
|---|---|---|
| 1 | Research Question | 一个（R2） |
| 2 | Competing Hypotheses | ≥2，各含机制与 falsifier |
| 3 | Variables | 自变量 / 因变量 / 控制变量（关系状态 R 这类**必须作控制变量**而非目标） |
| 4 | Baseline | 最强可比对手，而不是最弱稻草人 |
| 5 | Control | 无干预或无变化条件 |
| 6 | Intervention | 你实际做了什么 |
| 7 | Dataset / Environment | pin（版本/seed/sha）；Minecraft 实验须记 paper 版本与插件版本 |
| 8 | Procedure | 可被他人照做的步骤；脚本路径 |
| 9 | Metrics | 计算脚本路径 + 定义（不许口头定义） |
| 10 | Expected Result | 预注册的方向与量级 |
| 11 | Falsification Condition | 什么结果杀死哪个假设 |
| 12 | Actual Result | 原始产物路径（日志 / transcript / 数据） |
| 13 | Failure Cases | 反常与失败个案（不许只报平均） |
| 14 | Interpretation | 只写证据允许的强度；越界语言即退回 |
| 15 | Limitations | 环境、样本、测量、外部效度 |
| 16 | Next Question | 生成的后续问题，或明确写"无" |

**分层提醒**：Minecraft Layer 的实验（8 步 vertical slice、V1–V5）是**工程验收**；
Core/理论层的实验（关系缺口、violation-injection、primitive ablation）才是研究实验。
两者可以用同一套模板，但**结论层级不同**，不得互相顶替。

---

## 6. Review Gates（4 个，不是 7 个）

目标：**阻止低质量研究向后传播**，而不是增加流程。每个 Gate 只有一件事要判。

### Gate 1 · Question Gate

- **输入**：Observation 记录
- **必须满足**：可判定 + 若被回答会改变什么 + 文献检索过（链接 dossier）
- **Reviewer 看**：这是不是一个**能失败**的问题？
- **拒绝**：回答之后我们不会做任何不同的事
- **退回**：观察记录不足 → 回 `scratch/`

### Gate 2 · Pre-registration Gate

- **输入**：Question + ≥2 Hypothesis + Model + Prediction + Falsifier + Baseline/Control + Metrics + Env
- **必须满足**：预注册块**已提交**（有 commit hash）
- **Reviewer 看**：实验是否**有能力**产生反驳？（不是"能否支持"）
- **拒绝**：单假设 / 无 falsifier / 无 baseline 或 control / 指标无计算脚本
- **退回**：设计不完整（补完再注册，**不许先跑**）

### Gate 3 · Evidence Gate

- **输入**：实验结果（含失败）
- **必须满足**：按 §5 记录；原始产物路径可查；结果与预测的对照明确（四选一）；失败已进 `research/failures/`
- **Reviewer 看**：这是 **E 几**？等级虚报了吗？
- **拒绝**：只有 demo 却声称结论 / 指标无 provenance / 事后改预测 / 只报平均值不报失败个案
- **退回**：补对照、补失败记录，或**把 claim 降到证据允许的等级**

### Gate 4 · Claim Gate

- **输入**：Evidence + Claim 草案
- **必须满足**：claim 等级 ≤ 证据等级；写明 limitations 与可反驳条件；无与既有 accepted claim 的未处理冲突
- **Reviewer 看**：这句话，如果**是我错了**，会是什么样子？
- **拒绝**：跳跃（E1 → 普适结论）/ 无限制说明 / 与 B4 claim threshold 冲突
- **退回**：改写 claim（降级或加限定），或补实验

> **一次会只过一道 Gate。** 没有 Gate 的"顺手升级"（在别处悄悄把 draft 说成结论）视为违规。

---

## 7. Failure / Negative Result System

**失败是资产。** 团队必须能随时回答：**"我们到底知道了什么不能工作？"**

### 7.1 Failure Taxonomy（按"谁错了"分类）

| 类型 | 含义 | 处理 |
|---|---|---|
| **F1 Hypothesis Failure** | 预测没出现 → 机制可能错 | 研究资产 → 新 Question |
| **F2 Model Failure** | 预测出现但机制解释不了别的现象 / 内部不一致 | 研究资产 → 修模型或换假设 |
| **F3 Implementation Failure** | 产物没按规格工作 | **工程问题，不算结论**；修完重跑 |
| **F4 Experimental Failure** | 设计缺陷（混淆变量、无 control、样本不足、事后改预测） | 作废重设计 |
| **F5 Measurement Failure** | 指标测的不是想测的东西 | 修指标，历史数字作废 |
| **F6 Generalization Failure** | 在 A 成立、在 B 不成立 | 研究资产 → 界定边界 |
| **F7 Boundary-condition Failure** | 只在特定条件成立 | **这不是失败，是发现边界**——必须记录 |

**规则**：F3/F4/F5 **不得**当作负面研究结论使用（先修再进 Evidence Gate）；F1/F2/F6/F7 必须写成 Failure 记录。

### 7.2 Failure 记录（`research/failures/`，短小为准）

必含 6 项：**① 我们试了什么 ② 期望什么 ③ 实际什么 ④ 类型（F1–F7）⑤ 我们现在知道什么不能工作 ⑥ 它生成了哪个 Question（或明确写"无"）**。

**反模式**：把失败写成"未来工作"；把 F3/F4 包装成 F1；失败只存在于某人的聊天记录里。

---

## 8. Research Status Machine

### 8.1 Question 状态（写在 Question 文件第一行）

```text
observed → questioned → pre-registered → tested → supported │ weakened │ falsified
                                                      ↓
                                          revised │ abandoned │ promoted
```

| 状态 | 含义 | 进入条件 |
|---|---|---|
| `observed` | 现象已记录，尚未成为问题 | 有 Observation 记录 |
| `questioned` | 已通过 Gate 1 | 可判定 + 有影响 + 已检索 |
| `pre-registered` | 已通过 Gate 2 | 预注册块已提交 |
| `tested` | 实验跑完，结果未定级 | 原始产物已归档 |
| `supported` / `weakened` / `falsified` | 通过 Gate 3 | 结果与预测的对照明确 |
| `revised` | 假设/设计被修改（保留旧版） | 新一轮预注册 |
| `abandoned` | 放弃（写明为什么，例如不可判定） | 有明确理由 |
| `promoted` | 已进入 Claim / 论文 | 通过 Gate 4 |

### 8.2 Claim 状态（沿用既有 maturity tier，不新建）

```text
draft → candidate → accepted → published │ superseded │ withdrawn
```

映射：`draft` ≈ `papers/notes/drafts/`；`candidate/accepted` ≈ `papers/notes/accepted/`；
`published` ≈ 论文正文；`superseded/withdrawn` ≈ `papers/notes/archive/`。

### 8.3 可见性要求

**任何人进入 repo，应当能在 30 秒内回答"某个问题现在处于什么状态"** ——
办法就是：一个 Question 一个文件、第一行是状态、末尾是 append-only 历史。
（**不建看板**：状态必须写在被引用的文件里，见 §12。）

---

## 9. 十条研究规则

1. **先注册，后实验**：预测 + 支持条件 + 反驳条件在跑之前提交；跑完不得修改预测块。
2. **没有 Question 的实验叫工程验收**，不叫研究。
3. **每个假设必须有机制与 falsifier**；写不出 falsifier 的，是愿望不是假设。
4. **证据有等级，等级是 claim 的上限**：E0 只能支持"可做"。
5. **Demo / 单例 / 相关，一律不得升级为经验结论**。
6. **失败必须入库**（F1–F7），并写明"现在知道什么不能工作"。
7. **冲突结果不许二选一**，进入 competing hypotheses 直到有决定性实验。
8. **Claim 与证据等级同页出现**；无 limitations 的 claim 不得进 accepted。
9. **版本、构建、指标计算交给 git 与 code**；本方法不造第二套版本号、看板或工具。
10. **预算上限**：新增任何对象 / 目录 / Gate / 字段，必须同时删掉一个同类项，否则拒绝。

---

## 10. 预算上限（Anti-bloat 条款）

本方法的总预算是：**6 个对象 · 2 个新目录 · 4 个 Gate · 10 条规则 · 2 份文档**。

新增任何东西前先回答：**它替代谁？** 答不出来就不加。
每季度若无人使用某个对象/字段 → 删除它，并在本文档记一行"已删及原因"。

---

## 11. 与其他文档的连接

| 文档 | 关系 |
|---|---|
| [`team-workflow.md`](team-workflow.md) | 材料/论文规则（A/B 已批准）；本文是其**上游过程**，B4 claim threshold 不变 |
| [`research-methodology-design.md`](research-methodology-design.md) | 本文的设计理由、被拒方案、red-team 与升级路径 |
| [`../research/README.md`](../research/README.md) | 研究试错层；`questions/` 与 `failures/` 是本文的两个新增目录 |
| [research/world view taxonomy/methodology.md](<../research/world view taxonomy/methodology.md>) | **既有实例**：其六阶段（锁因变量→锚样本→轴操作化→轴审计→留出验证→冻结）正是 G1/G2/G3 的一次应用，不必重写 |
| [`../research/literature/00-literature-map-paper-gaps.md`](../research/literature/00-literature-map-paper-gaps.md) | 文献证据索引（本文不重复建 evidence 目录） |
| [`../papers/notes/accepted/paper-status.md`](../papers/notes/accepted/paper-status.md) | Claim 的成熟度台账 |
| [`../research/projects/`](../research/projects/) | 工程执行侧（含承接检查清单） |
| [`../research/paths/`](../research/paths/) | 候选架构路线（冻结/解冻 + 评估），不得在工程阶段被当作结论使用 |
