# World View Taxonomy — Draft 01

> **STATUS: PENDING — 待团队审视与头脑风暴 (Awaiting team review & brainstorm)**
>
> 本文件为**规划草稿（draft）**，尚未经过团队评审，不代表 Macha 的定稿设计。
> 文中所有定义、坐标系、命名（如 World Permeability、六维坐标系）均为**作者提出的待议提案**，
> 需要团队集体审视、反驳、补充与头脑风暴后方可进入下一阶段。
> 请勿将其作为已采纳的架构依据直接引用。

---

## 0. 立论动机（Motivation）

对于 AI NPC Framework 来说：

- 《魔戒》和《赛博朋克 2077》虽然题材完全不同，但它们可能具有**非常相似的"世界结构"**；
- 反过来，同样是奇幻世界，《D&D》和《艾尔登法环》的 AI 接入难度可能**完全不同**。

因此，我们先建立一个**与题材无关的 World Ontology（世界本体）**，作为后续所有分类与设计讨论的共同地基。

---

## 一、先钉死一个底座：什么叫"世界观"？

建议暂时**不要把 Worldview、Lore、World、Setting 混为一谈**。

### 定义

> **World = 一组能够约束、描述并产生事件的状态、规则、实体、关系与历史。**

因此一个世界至少包含六个要素：

```
W = (E, S, R, H, O, C)
```

- **E = Entities**：世界里有什么
- **S = State**：现在是什么状态
- **R = Rules**：什么事情允许发生
- **H = History**：过去发生过什么
- **O = Observability**：谁能知道什么
- **C = Causality**：行动如何造成后果

这六个东西是我们的**第一性底座**。

### 一个重要结论

> **Lore 只是 World 的一种表达方式。**

| 表达 | 本质 |
|------|------|
| "帝国已经存在 800 年" | Lore |
| "帝国成立于 Year 120，经历 7 次战争，目前人口 430 万" | State + History |
| "如果皇帝死亡，继承权按照 A→B→C 顺序转移" | Rule |

**AI NPC 真正需要的是后两者（State/History 与 Rule），而非 Lore 文本本身。**

---

## 二、第二个底座：世界不是"静态地图"，而是状态转移系统

这是我们后面所有讨论的地基。

任何一个世界，都可以抽象成：

```
S_{t+1} = T(S_t, A_t)
```

- `S_t`：世界在时间 `t` 的状态
- `A_t`：行动
- `T`：世界规则（转移函数）
- `S_{t+1}`：行动之后的新世界

示例：

```
国王还活着
      ↓
NPC 尝试刺杀
      ↓
World Rules
      ↓
成功 / 失败
      ↓
新的世界状态
```

> **世界观真正的核心不是"写了什么"，而是"什么能够导致什么"。**
> 这句话建议直接作为 Macha 的理论地基之一。

---

## 三、分类：不是单一分类，而是一个坐标系

"世界类型"本质上是**多维的**。建议至少有 **6 个轴（Axes）**。

### Axis 1：世界的"确定性"（Determinism）

- **A. Scripted World** —— 世界事件主要由作者预先规定。
  ```
  A → B → C → D
  ```
  例：到第 10 天，国王一定死亡。AI NPC 再聪明也不能改变。
- **B. Rule-based World** —— 作者规定规则，而非具体事件。
  ```
  Rules → possible futures → actual events
  ```
  例：国王可以被刺杀，但谁刺杀、何时、成败由系统产生。（AI NPC 的理想环境）
- **C. Emergent World** —— 甚至规则的高层结构都可以演化。
  ```
  NPC → trade → wealth inequality → class formation → political factions → new institutions
  ```
  作者未直接设计该政治制度，它从系统里长出。

```
Scripted → Rule-based → Emergent
作者控制结果 → 作者控制规则 → 作者控制生成规则的条件
```

### Axis 2：世界状态是否"开放"（Openness）

- **Closed World**：世界里有什么基本已被定义。`Entities = fixed`。
  例：这个世界只有 8 个国家，NPC 不能突然创造第 9 个。
- **Expandable World**：世界允许产生新实体。`Entities(t+1) ⊃ Entities(t)`。
  例：NPC 可以成立一个新的政治组织。
- **Generative World**：实体类别本身都可能产生。
  例：AI NPC 发明一种新的社会制度。开始接近 **World Genesis**。

### Axis 3：世界的因果封闭程度（Causality）

- **Strongly Closed**：所有重要因果都已被游戏系统定义。
  例：`sword_damage(); health -= damage`，AI 无法绕过。
- **Partially Closed**：底层规则稳定，但存在大量开放空间。
  例：Physics = fixed；Social behavior = open；Politics = open；Economy = partially open。
  **（最适合 AI NPC 的甜蜜区间）**
- **Weakly Closed / Open Causal World**：AI 可以引入新的因果关系。
  例：NPC 发明一种新的魔法。要求 Framework 允许 `R_{t+1} ≠ R_t`。

### Axis 4：世界的"真相结构"（Knowledge）

- **Omniscient World**：真相明确存在，原则上所有 Agent 都可访问。最容易实现。
- **Partially Observable World**：真实状态存在，但每个 Agent 只看到一部分。
  ```
         WORLD TRUTH
        /     |     \
       /      |      \
    NPC A   NPC B   NPC C
     30%     50%     10%
  ```
  这才开始出现：谣言、阴谋、情报战、误解、欺骗、政治、推理。
- **Epistemically Open World**：世界本身可能没有唯一可访问的"真相"。
  例：历史、宗教、意识、宇宙起源。不同 NPC 有不同解释。
  ```
  Truth ≠ Belief
  Belief_A ≠ Belief_B
  ```

### Axis 5：世界历史的"硬度"（Canon）

- **Hard Canon**：`Past = immutable`。例：二战已发生，NPC 不能改变。
- **Soft Canon**：历史存在，但局部细节可被重新解释。例：大家都知道战争发生，但不知真正原因。
- **Living Canon**：历史本身持续生成。
  ```
  Past → NPC actions → new history → future canon
  ```
  玩家今天做的事，十年后变成这个世界的历史。

### Axis 6：世界是否允许"世界内智能"（Agency）

- **Passive World**：世界不会主动做什么。`Player → World reacts`。
- **Reactive World**：世界对行动做出反应。`Player → World → Reaction`。
- **Autonomous World**：世界中的实体拥有自己的目标。
  ```
  Player       ↘
               WORLD
              ↗
  NPC → NPC → NPC
  ```
  玩家离开后，世界依然继续。
- **Self-organizing World**：NPC 之间可形成组织、制度、文化、经济和社会结构 = **Agent Society**。

---

## 四、六维坐标系（Six-Axis Coordinate System）

```
Axis         低端             高端
Determinism  Scripted         Emergent
Openness     Closed           Generative
Causality    Fixed            Evolving
Knowledge    Omniscient       Epistemically fragmented
Canon        Hard             Living
Agency       Reactive         Autonomous society
```

"世界观类型"不再是几个类别，而是一个**六维空间**。一个具体世界可表示为：

```
World = (D, O, C, K, H, A)
```

---

## 五、对已有世界观的粗暴定位（示例）

> 以下柱状条为示意性估计，仅供讨论，非精确测量。

**《超级马里奥》**
```
Determinism   █████████░
Openness      ██░░░░░░░░
Causality     █████████░
Knowledge     ████████░░
Canon         █████████░
Agency        ███░░░░░░░
```
很封闭。

**《Minecraft》**
```
Determinism   ███░░░░░░░
Openness      █████████░
Causality     ████████░░
Knowledge     ███████░░░
Canon         ███░░░░░░░
Agency        ████░░░░░░
```
开放度极高，但原生 NPC 社会复杂度有限。

**《The Sims》** —— 重点完全不同：
```
World → Needs → Agents → Interactions → Emergence
```
在 Agency / Emergence 上很高。

**《Dwarf Fortress》** —— 更加极端。它更接近一个**历史生成器**，而非"写好的故事"。对 AI NPC Framework 极其值得研究。

**一个典型线性 RPG** —— 可能是：
```
Hard Canon + Strong Causality + High Scriptedness + Low Agency
```
但这并不意味着不能接入 AI：**AI 可以只被允许在某个局部区域获得自由度。**

---

## 六、核心概念：World Permeability（世界渗透性）

建议单独命名：

> **World Permeability = 世界对新智能的"渗透性"**
> 即：一个已有世界允许外部 Autonomous Agent 在多大程度上进入其因果系统。

```
0%   WORLD ████████████   AI NPC ×
     NPC 只能说台词。

25%  NPC → Dialogue → Relationship
     AI 可以改变关系。

50%  NPC → Actions → Economy / Politics / Social state
     AI 开始真正参与世界。

75%  NPC → Institutions → History → Culture
     世界开始被 AI 改造。

100% AI Agents → WORLD → WORLD TRANSFORMATION
     AI 不再是"嵌入世界"，而是成为了世界的一部分。
```

---

## 七、建议先钉住的理论底座（待评审）

暂不继续设计 Macha 的具体模块。先把下面这个模型钉住：

```
                     WORLD
                       │
        ┌──────────────┼──────────────┐
        │              │              │
     Entities        State         History
        │              │              │
        └──────────────┼──────────────┘
                       │
                     Rules
                       │
                  Causality
                       │
                  Observability
                       │
                 ┌─────┴─────┐
                 │           │
              Agents       Player
                 │           │
                 └─────┬─────┘
                       │
                    Actions
                       │
                  Transition
                       │
                       ▼
                 New World
```

用六个问题描述任何世界：

1. 什么东西存在？
2. 世界当前是什么状态？
3. 什么规则约束它？
4. 谁知道什么？
5. 什么历史是不可改变的？
6. 谁拥有改变世界的能力？

> 这六个问题作为目前足够坚固的**第一版理论底座**。

---

## 八、更深一层：世界的"智能接入模式"

如果真要做 Macha，最终不能只分类"世界"，还必须分类**世界允许什么类型的智能进入**。

同一世界可存在不同的 AI integration mode：

```
               Existing World
                     │
        ┌────────────┼────────────┐
        ▼            ▼            ▼
     Actor         Citizen      Creator
        │            │            │
   affects        lives in     modifies
   events         society      world rules
```

这意味着：**AI NPC Framework 的真正 API 可能不是 `createNPC()`，而是：**

```
register_world()
define_canon()
define_rules()
define_observability()
register_agent()
grant_agency()
validate_action()
commit_transition()
```

> 它不再是一个 "NPC AI SDK"，而更像一个 **让已有数字世界接纳 Autonomous Intelligence 的 Runtime**。

---

## 九、下一步最值得头脑风暴的锋利问题（供团队讨论）

> **如果把一个世界的"可渗透性"从 0% 一路推到 100%，中间究竟会出现哪些新的世界形态？**

我（作者）的猜测：这里会自然长出一张 **World × Agency × Canon 的完整地图**，而这张地图很可能比"AI NPC Framework 架构图"本身更接近 Macha 真正的理论核心。

### 待团队回应的问题清单（Open Questions for Review）

1. 六要素 `W = (E,S,R,H,O,C)` 的拆分是否完备？是否遗漏了关键维度（如时间、空间、价值体系）？
2. 六个轴的选择是否正交？是否存在两两强相关、需要合并的轴？
3. "World Permeability" 应作为独立维度，还是 Axes 的函数？
4. 示例世界的定位（柱状条）是否经得起反驳？需要更严谨的标定方法吗？
5. API 形态（`register_world()` 等）是否过度工程？它应该首先服务哪种集成场景？
6. 这份草稿的下一版，应该先深化"坐标系"，还是先落地一个最小可验证的 World Runtime 原型？

---

*Draft 01 — PENDING. Authored as a proposal for team review. Not yet adopted as Macha design.*
