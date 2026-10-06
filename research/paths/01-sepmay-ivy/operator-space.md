# Operator Space（算子空间）— 研究草案

> **STATUS: DRAFT（研究草案）** — 不是已定设计，**不解冻**路径一，也**不修改** [`README.md`](README.md) §4 的已定基线。
> 本文件把 README §2 图里那个叫"算子集合（一切即插件）"的空盒子第一次填上内容，形式是**可实验、可反驳的候选**，不是 taxonomy。
> **本轮不写代码**（审计结论：仓内没有 Operator abstraction；见 §12）。
> 相关：[`README.md`](README.md) · [`open-decisions.md`](open-decisions.md)（D8–D11）· [`../../README.md`](../../README.md)（路径索引）·
> [`../../../docs/architecture.md`](../../../docs/architecture.md) §1.5（算子在接收域图里的位置）· 路径二 §1.5（内驱力算子占的那一格）

---

## 0. 一句话

SepMay 已经回答了"信息**存在哪里**、活多久、以什么粒度写回"；它没有回答
**"信息进入系统之后，可以被做哪些变换"**。本文件是这后半个问题的容器。

---

## 1. 现状审计

### 1.1 已经明确的（可直接引用，不要重定义）

| 概念 | 已定内容 | 出处 |
|---|---|---|
| 接收域 = **准入**，不是接收 | 决定什么进入这个世界模型、以什么粒度与不确定性；产品是"有门的事实" | `architecture.md` §1.5 |
| 外部信息源 | append-only 事实；回流**不改写**它 | `README.md` §2 读法 1 · §4 |
| 内部信息源 | 只由 IC 在 **Chunk 关闭时**写入；两阶段提交 | `README.md` §4 |
| 回流三路 | 事实件 / 陈述件（他自己的版本）/ 权重 | `README.md` §4 |
| 中断 ≠ 关闭 | 中断只提交事实件，不产生"他的版本" | `README.md` §4 |
| Chunk / Thread 结构 | Chunk 不嵌套、Thread 不跨 Chunk、关闭时回流等 10 条基线 | `README.md` §4 |
| 输出域 | Ive Chunk → Ive Thread | `README.md` §2 图 |
| **接收域不做赋义** | 赋义属**运算域的算子** | `README.md` §2 读法 3 · `open-decisions.md` D7 |
| 准入组件的名字与契约 | 暂名 `Intake`，未定 | `open-decisions.md` D7 |
| 内驱力算子的位置 | 运算域里的一格算子：把近期历史折成 drive 变化 | 路径二 `README.md` §1.5 ② |

### 1.2 "算子"目前的真实状态：**这三处全是标签，不是定义**

1. `README.md` §2 图里一行 `算子集合（一切即插件）`；
2. `architecture.md` §1.5 表里一行 `算子集合 operators | Core operators (incl. future appraisal / guardrail)`，
   而它的 **Written by / Read by 两栏都是 `—`**；
3. 两处边界声明"赋义属运算域算子"——只划分了归属，没给定义。

**没有任何**输入/输出、作用对象、组合规则、触发方式、验证方式或清单。

### 1.3 已经隐含存在、但没被叫成 operator 的行为（候选）

| 行为 | 现在住在哪 | 为什么可能是 operator |
|---|---|---|
| 准入（去重/排序/标 provenance/降级） | 接收域，暂名 `Intake`（D7） | 它改变"可见集合"，符合 SELECT/TEST 的形态 |
| 赋义（appraisal） | **明确划给算子，但没有定义** | 这是本草案要填的第一个真空白 |
| 回流写入（三路） | Chunk 关闭时 | 它改变持久状态 → 形态上就是 COMMIT（见 D9） |
| 内驱力算子 | 路径二运算域一格 | 把近期历史折成 drive 变化 → STATE 上的 TRANSFORM/TEST |
| 记忆检索 | 实现层 `memory.py::retrieve()` 返回最后 N 条 | 一个极朴素的 SELECT（且**没有依据**，正是 SEL 缺定义的样子） |
| guardrail | `architecture.md` 把它列进 operators 行 | 更像"带约束的判定" → TEST 的候选特例 |

### 1.4 完全没有定义的（本草案要动的）

operator 的作用对象是什么 · 输入输出与"改变了什么" · 组合规则与类型约束 · 谁触发调用 ·
operator 与 Method 的关系 · **如何验证一个 operator 是必要的而不是想象出来的**。

### 1.5 三处最容易混淆的边界（先钉住）

1. **准入 vs 赋义**：都在"处理信息"，但**准入不许做意义判断**（D7 已定）。operator 空间从赋义才开始。
2. **算子 vs 回流**：一个发生在**处理期间**，一个发生在**关闭时点**。"COMMIT 是不是就是回流"是本草案最大的悬案 → D9。
3. **算子 vs 插件**：README 说"一切即插件"。插件是**实现形态**，算子是**被实现的东西**。本草案只谈后者，不谈打包方式。

### 1.6 两套待检查链路的审计结论

**链路 A**（`信息源 → 准入 → Chunk → Thread → 处理 → 关闭 → 回流 → 内部信息源`）：
**存在，但只有一半**。准入、Chunk/Thread、关闭、回流三路都已定（见 1.1 表）；
**"处理"那一步是空的**——它就是本文件要填的算子空间。

**链路 B**（`Flow / Method / Method Spec / Learner / Agent State / Memory`）：
**在本仓不存在。** 全仓检索结果：`Method Spec` / `Learner` / `Information Lifecycle` **零命中**；
`Flow` 只作为外部方案 AetherFlow 的 `MFlow`（记忆流）出现在
[`../../scratch/aetherflow-review.md`](../../scratch/aetherflow-review.md) 的评审笔记里，
且被粗略映射到 Macha 的 `Memory` + `Reflection`——**那是别人的概念，不是本仓的定义**。

**结论**：链路 B 没有可"补齐"的对象，它需要先决定"要不要有 Method 这一层"。
本草案**不建立**这一层，只在 §8 把 Method 当作**待验证的输入**（"Method 能否表达为算子组合"）。

---

## 2. Operator Space（定义）

> **Operator（算子）**：对**信息、Thread 或内部状态**施加的一次**状态变换操作**。
>
> *Operator: a state-transforming operation over information, threads, or internal state.*

关键不是"工具调用"（那是 `ActionCall` → Layer，已定，不在这里），而是：

```text
State  →  Operator  →  State'
```

Operator 的核心问题只有一个：**什么发生了变化？**

### 2.1 三个必须分开的东西（本文件所有条目都按这三栏写）

以"玩家偷了 NPC 的东西"为例：

| 层 | 它回答的问题 | 例子 |
|---|---|---|
| **External Information** | 系统**获得了什么** | "玩家拿走了箱子里的东西"（一条事实，带 provenance） |
| **Operator** | 系统对信息/状态**做了什么** | 取出这条事实 → 与"我的东西"建立关系 → 检验它与"我以为他在帮忙"冲突 → 提交为对这名玩家的关系变化 |
| **Internal State** | 系统**留下了什么** | 对"玩家"的信任权重变化 + 一条"他拿走了我的东西"的陈述件 |

**判定边界**（用来防止两类最常见混淆）：
- 属于"获得了什么" → **不是** operator；
- 属于"留下了什么" → **不是** operator，那是状态。
- 于是：**Memory Store ≠ Operator Space**，**Tool Calling ≠ Operator Space**。
  Operator 只活在中间那一层。这条边界也是 §7 能把算子空间和内部状态真正接起来的原因。

---

## 3. 最小候选基（**实验假设**，不是 taxonomy）

以下五个是**第一版候选**，提出方式很朴素：读 1.3 表里那六件已存在的行为，找它们共同的最小动作。
**它不完备、不声称正交、不排除合并或删除。** 一个候选若在实验中从不出现，就该被删掉。

| 候选 | 一句话 | 作用对象（见 §5） |
|---|---|---|
| **SELECT** | 从当前可见的信息/状态中取出、聚焦某一部分 | Information / State |
| **RELATE** | 在两个或多个单位之间建立或显式化关系 | Information |
| **TRANSFORM** | 改变信息的表征形式、抽象层级或认知表达 | Information |
| **TEST** | 比较、检验、冲突检测、约束检查、证据评估 | Information / State |
| **COMMIT** | 把 processing result 固化/回写/提交到更持久的状态 | → Internal State |

### 3.1 SELECT

- **Input**：一个可见集合（准入后的事实、当前 Chunk 的工作集、或某个状态快照）+ 一个（可能模糊的）选择依据
- **Output**：被取出的子集或指向它的指针
- **Primary effect**：**可见范围改变**，内容本身不变
- **Can compose with**：几乎总是入口；常见接 RELATE / TRANSFORM / TEST，且 TEST 与 RELATE 的输出常**再次**进入 SELECT
- **Open questions**：选择依据从哪来——是算子的一部分，还是 §9 的 selection policy？"找到 X"与"确认这就是 X"是同一个操作吗（SELECT 与 TEST 是否可分）？

### 3.2 RELATE

- **Input**：≥2 个信息/状态单位
- **Output**：一条关系（显式的边，或一条断言）
- **Primary effect**：**新增关系**；不改变被关联单位的内容
- **Can compose with**：常用于接 TRANSFORM（把关系当作结构来处理）或直接 COMMIT
- **Open questions**：关系算事实件还是陈述件（决定它走回流哪一路）？关系能不能以算子自身为端点（如"这两次 TEST 是同一件事"）？

### 3.3 TRANSFORM

- **Input**：一个单位（或一个集合）
- **Output**：同一内容的**另一表征 / 另一抽象层**
- **Primary effect**：**表征改变**，原则上应能与原单位对回
- **Can compose with**：可与自身组合（这是"递归/重构"类过程唯一可能的基础）；常接 SELECT 或 TEST
- **Open questions**：**缺"还是同一个东西"的判据**——没有保真度/可逆性标准，TRANSFORM 会退化成"随便改写"。这是 §11 必须测的一条。

### 3.4 TEST

- **Input**：≥2 个单位，或 1 个单位 + 1 个约束
- **Output**：一个判定（一致 / 冲突 / 满足 / 不满足）+ 差异位置
- **Primary effect**：**不改变被检验对象**，产生判定
- **Can compose with**：常由 SELECT 触发；常接 COMMIT，或再接 SELECT（"问下一问"）
- **Open questions**：判定必须显式落盘才算发生吗（否则无法观测）？guardrail 是不是 TEST 的一个**带特殊约束的特例**？

### 3.5 COMMIT

- **Input**：一个 processing result + 一个目标位置（Chunk 内暂存 / 内部信息源三路之一）
- **Output**：状态变化（可能附一条可读结论）
- **Primary effect**：**持久化 + 可见性改变**
- **Can compose with**：所有流程的出口；COMMIT 之后通常不再接 TEST 同一个未提交结果
- **Open questions**：**COMMIT 与"回流"是不是同一件事**（若允许 Chunk 内 COMMIT，则回流只是它的一个特定时点；若不允许，则 COMMIT 只在关闭时发生）→ D9。**由谁授权 COMMIT**——直接压在 D4（权重更新语义）上。

> **不在表里的**：Reasoning / Reflection / Planning / Regret / Analogy / Causal Learning。
> 理由见下一节。

---

## 4. Reasoning ≠ Primitive Operator

```text
Reasoning · Reflection · Planning · Regret · Analogy · Causal Learning
```

它们**不应该**直接作为 primitive operator，三条理由：

1. **把结论当公理**：它们每一个都预设"已经有一批可用操作"才有意义。直接把高级能力设为原语，等于把待解释的东西写进解释里。
2. **不可判定**："NPC 会反思"无法判定；"这里发生了一次 SELECT、一次 TEST、一次 COMMIT"可以判定（trace 里查得到）。
3. **粒度不齐**：Planning（目标的生成与排序）、Reflection（对已提交状态的再处理）、Regret（很可能是 TEST+COMMIT 的**结果**而非操作）不在同一层，并列会造成伪分类。

**核心思想**：一个高级 cognitive capability 可能实际上是多个 primitive operators 的**组合**。

示意（**hypothesis，不是证明**）：

```text
SELECT → RELATE → TEST → COMMIT          # 可能构成某类"判断/推理"
TRANSFORM → SELECT → TRANSFORM → TEST    # 可能构成某类递归认知（自指 / 重构）
```

> 这两行是**待验证假设**。它们的作用是**产生实验**，不是解释世界。禁止写成"就是"。

---

## 5. Operator 的作用对象：Information / Thread / State

**为什么这个问题比"到底有几个 operator"更重要**：operator 的数量可以随实验增删；而**作用对象决定了类型系统**——
哪些组合合法、结果写到哪里、谁有写入权。它也是算子空间与 IC / 内部信息源之间的接口面。

| 候选作用对象 | 含义 | 风险 |
|---|---|---|
| `Operator(Information)` | 作用在准入后的事实/信息条目上 | 基本无风险：不碰 IC 结构、不碰提交权 |
| `Operator(Thread)` | 作用在 Thread 的组织上（分组、合并、标寿命类） | **危险区**：会碰 IC 的调度面，而 D3 已明确反对把语义放进调度器 |
| `Operator(State)` | 作用在内部状态（含 drive 电平）上 | **生死线**：会碰回流写入权，直接连 D4 |

**不要假设所有 operator 都必须对同一种对象操作。** 很可能 TEST 对 Information 与对 State 是**两种不同的操作**
（判据不同、授权不同、可观测性不同）；SELECT 可能只在 Information 上有意义。

这个问题**保留为后续实验**（D8），本轮不做裁决。

---

## 6. Operator Composition

```text
X  →  Op1  →  Op2  →  Op3  →  X'
```

要回答的问题（全部保留，本轮不裁决）：

- operator 可以任意组合吗？（推测**否**：COMMIT 之后不应再 TEST 同一个未提交结果）
- 哪些组合有类型约束？（目前唯一看得见的是**数量约束**：SELECT 输出集合，RELATE 需要 ≥2）
- 哪些组合无意义？——"无意义"有两种：真正的非法（越权写），和**语义奇怪但可能正好是我们要的**
  （`COMMIT → SELECT`＝读回自己刚写的东西，这可能正是"回忆"的形态，不要急着判它非法）
- 是否存在可复用的 **Operator Pattern**？
- Method 是否可以被表示为 **Operator Program**？

最小概念（**不是 grammar**）：

```text
Primitive Operator  →  Composition  →  Operator Pattern  →  Method
```

> **"Method = Operator Program" 是需要实验验证的研究假设**，不是定义。见 §8 与 §11 的 E-OS2。

---

## 7. State Semantics

**不要把 operator 写成 `X → Y`。** 更现实的形式是：

```text
(X, Internal State, Context)
            ↓
         Operator
            ↓
(X', Internal State')
```

原因：**同一个信息，在不同内部状态下做同一个操作，可能得到不同结果。**

```text
Information: "Bob left early."

Agent A（关系紧密、曾被中途抛下过） → "Bob abandoned me."
Agent B（关系松、自己也常早退）     → "Bob probably had another task."
```

Operator 本身可能相同，state / context 不同。

**这条对 Macha 的四个具体后果**：

1. **"同一个 operator"这个说法变得可疑**：输出依赖 state，因此需要区分
   **operator identity**（做了什么变换）与 **operator outcome**（得到了什么）。这是 D8 的一半。
2. **它把 Operator Space 与 Memory / Internal State 真正接起来**：state 是 operator 的输入之一，
   operator 的输出之一是 state 的变化——这正是与回流三路（尤其"权重"）的接口处。
3. **对实验的硬要求**：任何"operator 有效性"实验必须**固定 state**，否则复现性直接失效
   （同源要求见 [`../../questions/Q-01-drive-signal.md`](../../questions/Q-01-drive-signal.md) §5-7）。
4. **反例警告**：不能把 state 当万能解释项——若所有差异都归因于"state 不同"，该假设**不可反驳**。
   所以实验必须能事先写出"在 state S 下，这个 operator 输出 X"这样的**可证伪预测**。

---

## 8. From Method to Operator Composition（实验，不是归约）

三个待研究对象：

```text
Socratic · GEB Recursive · Structural Reconstruction Method
```

> **审计事实（重要）**：这三个名字**目前在仓内不存在**（全仓检索零命中）。
> 它们是本草案引入的**待研究对象**，因此第一步不是归约，而是**先各自有一份来源与定义**
> （谁提的、在哪、判据是什么）。没有来源，"把 Method 表达为算子组合"就没有对象。

**待验证形式**（全部标注为 hypothesis，禁止写成结论）：

```text
Socratic
  可能涉及：SELECT → TEST → SELECT → TEST → COMMIT

GEB Recursive
  可能涉及：TRANSFORM(self-representation) → SELECT → TRANSFORM → TEST(termination)

Structural Reconstruction
  可能涉及：SELECT(evidence) → RELATE → TRANSFORM(structure) → TEST(consistency) → COMMIT
```

**我们将通过实验尝试把已有 Method 表达为 Operator Composition。** 每个 Method 的验证只允许产出三样之一：

1. **能用候选基表达** → 记为一个 pattern；
2. **需要一个新的 primitive** → 记为候选新 operator，并必须给出"为什么现有五个不够"；
3. **表达不出来** → 这是**反例**，价值最高，直接进入 `../../failures/` 的分类流程。

---

## 9. Operator Selection

**"有哪些 operator"（§3）与"什么时候调用哪个"（本节）是两个问题。** 混在一起会让人以为算子里包含"意图"。

```text
State
  ↓
Available Operators
  ↓
Selection Policy
  ↓
Operator
  ↓
Updated State
```

可能影响选择策略的变量：`uncertainty` · `goal` · `conflict` · `urgency` · `novelty` · `relevance`。

**这些变量不是 operator**——它们没有一个"改变状态"，它们只是**排序**操作。

- 与已有工作的接口：[`Q-01`](../../questions/Q-01-drive-signal.md) §9 问的"预算仲裁该由谁做（IC 准入，还是算子层竞争）"
  与本节的 Selection Policy 是同一个问题 → 交叉登记为 D11。
- 本轮**不实现 Orchestrator**。只登记"谁做选择"是未定项。

---

## 10. Operator Discovery（远期方向，不是当前目标）

若某串组合反复出现：

```text
SELECT + RELATE + TEST + TRANSFORM
```

系统是否可以把它抽象成一个新的 reusable operator？

```text
Primitive  →  Composition  →  Pattern  →  Discovered Operator
```

**明确：这是远期研究方向，不在当前实现目标内。** 而且它依赖 §11 的标注实验先产出数据
（没有标注数据，"反复出现"无从统计）。若数据不支持，本节的答案就是"不发现"。

---

## 11. How We Discover the Operator Space

**我们不打算坐在桌面上直接设计完整 Operator Taxonomy。** 采用：

```text
Concrete Cognitive Task
        ↓
Observe what must happen
        ↓
Ask: "What operation changed the state?"
        ↓
Extract candidate operator
        ↓
Test whether it is reusable
        ↓
Try composition
        ↓
Refine / merge / discard
```

### 11.1 最小实验场景

> 一个 NPC 经历：**玩家偷走东西 → 玩家离开 → 很久以后再次出现。**

逐步问（五问）：

```text
NPC 收到了什么？
        ↓
对信息做了什么？
        ↓
什么发生了改变？
        ↓
什么被留下来了？
        ↓
下一次遇到玩家时，过去如何影响现在？
```

然后把观察结果**反推**成三栏：`External Information` / `Operator` / `Internal State`（§2.1 的表格就是模板）。

### 11.2 三个可跑的实验（对齐"如何验证"）

| ID | 做法 | 判据 | 失败形态 |
|---|---|---|---|
| **E-OS1 标注实验（最便宜，先做）** | 拿一条 trace（真跑、手写或脚本化的 transcript 均可），逐步标注它对应哪个候选 operator（**允许标"都不是"**） | 产出三个数：① **覆盖率**（能被五个覆盖的步数比）② **缺口感**（"都不是"的步数及其样子）③ **信度**（两名标注者一致率）。若"都不是"持续集中在同一类步骤 → 有一个 operator 缺失（这是发现，不是失败）；若一致率低 → 五个算子的定义不合格，先改定义 | 任何步骤都能塞进任一算子、标注全靠事后解释 → **定义太松，本草案作废重来** |
| **E-OS2 组合实验** | 取 §8 里最容易拿到来源的那个 Method，尝试写出 operator program | 三选一：① 表达成功 → 记 pattern ② 需要新 primitive → 候选 ③ 表达失败 → 反例 | 为凑出链路而临时发明算子 → 记录为**理论污染**，不算结果 |
| **E-OS3 状态依赖实验** | 固定 Information、固定 operator、变 Internal State，看输出是否不同（§7 的 Bob 例）；再反过来固定 state 变 information | 必须能**事先**写出"在 state S 下输出 X"的可证伪预测 | 所有差异都用"state 不同"解释 → 不可反驳，实验作废 |

### 11.3 Substrate（诚实说明：本轮不需要 Core，也不需要改 Layer）

- **E-OS1 只需一条 transcript**——手写也可以。
- **E-OS3 需要一个能设定 state 的最小假体**——纸面、表格或一段脚本即可。
- 这就是**本草案不需要解冻路径一**的原因：它不依赖 IC 实现，也不依赖 Layer 改动。

### 11.4 与解冻条件的关系

路径一的解冻条件（[`README.md`](README.md) §6 三条）**未变**。若 E-OS1 产生一个必须由实现回答的问题
（例如"COMMIT 的时点"），它**先落到 `open-decisions.md`**，而不是变成"开始写代码"的理由。

---

## 12. 本轮明确不做

禁止清单（与用户给定的边界一致）：

- ❌ 一上来定义 20–50 个 operator
- ❌ 把 Reflection / Planning / Memory / Reasoning 全都叫 operator
- ❌ 编造数学形式来制造"理论感"
- ❌ 直接宣布 Primitive Basis 已经完备
- ❌ 为了完整而设计复杂 Runtime / Orchestrator
- ❌ 把 Operator Space 与 Tool Calling 混为一谈（后者是 `ActionCall` → Layer）
- ❌ 把 Memory Store 当成 Operator Space
- ❌ 把 Method Taxonomy 当成 Operator Taxonomy
- ❌ **写代码**：本轮不建 Runtime / SDK / Operator class。审计结论是仓内不存在 Operator abstraction，
  因此"先有抽象再实现"的前提不成立。

---

## 13. 自我审查：删掉漂亮话之后还剩什么

一个工程师读完本文件，应当能立刻做的最小动作：

1. 手写或录一条"偷东西 → 离开 → 回来"的 trace；
2. 逐步标注 §3 的五个候选算子（**允许标"都不是"**）；
3. 报三个数：覆盖率、缺口感、标注者一致率；
4. 把结果贴回 §11.2，并把新出现的缺口登记到 `open-decisions.md`。

**做不到这四步，本文件就必须继续改。**
