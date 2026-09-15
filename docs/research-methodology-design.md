# Macha Research Methodology — 设计说明（v1.0）

> 配套规范：[`research-methodology.md`](research-methodology.md)。
> 本文记录：**审计结论 · 设计理由 · 方法论锚点 · 被明确拒绝的方案 · Red Team 与由此产生的修改 · 未来升级信号**。
> 审计基线：commit `01143c1`（2026-09-14），远程 `github.com/zbbsdsb/Macha`。

---

## 1. 审计（先理解，再设计）

### 1.1 Macha 当前到底在研究什么？

三个层次，只有前两个在动：

| 线 | 实际内容 | 状态 |
|---|---|---|
| **理论** | 从玩家视角问"我们想要什么样的游戏智能体"；核心判断是**缺的是场、不是信息**（field superposition / perspective gap）；主张关系是一等计算对象（R 作控制变量） | 有骨架与文献支撑；**只有两条在 `paper-status.md` 里是"确定"的** |
| **系统** | 两个可分离系统 + 一份契约：Macha Core（认知）+ Environment Integration Layer；当前在造第一个 Layer（Minecraft） | Layer 骨架已落地、20 单测过；**服务器零次启动** |
| **评测** | conformance（C01–C12）、V1–V5、matched-surface 对照、violation-injection、primitive ablation | **只有设计，没有任何数据** |

**结论**：Macha 现在是"**理论与工程先行、没有任何实验证据**"的项目。

### 1.2 当前研究流程已经有什么？

- `team-workflow.md` A/B（材料与论文硬规则，已批准）+ C/D/E 显式 TODO；
- 成熟度分层（`research/` 试错 → `papers/notes/` drafts/accepted/archive → 论文正文）+ lifecycle rule；
- 文献证据层：`research/literature/` 00–07 + `00-literature-map-paper-gaps.md`（claim→dossier 映射）；
- `papers/notes/accepted/paper-status.md` 的三态区分；`05-macha-question-tree.md` 的问题树与 4 个岔路；
- `research/paths/`（候选架构：冻结/解冻 + `eval/` + `open-decisions.md`）；
- `research/projects/`（带日期的执行项目 + **承接检查清单**）；
- `research/world view taxonomy/methodology.md`（**一个真实的六阶段方法学实例**，含止损线）；
- `research/plans/minecraft-layer/` 00–06 + validation plan（V1–V5 / M1–M9）；
- `layers/` 的**工程**验收：8 步 vertical slice、三个边界守护任务。

### 1.3 哪些只是文件管理，而不是研究方法？

| 现有物 | 性质 |
|---|---|
| 四层目录 + lifecycle rule | **信息架构**（决定东西放哪） |
| provenance 表、命名规范、语言政策 | **材料管理** |
| `06-next-step-plan`、`plans/*` | **项目计划** |
| 边界守护 Gradle 任务 | **工程约束**（很强，但管的是依赖与 import） |
| 承接检查清单 | **协作/交接** |

**判据**：以上没有一项回答"**我们凭什么相信这个结论**"。这正是方法论的空白区。

### 1.4 当前最大的 epistemic weakness

1. **没有证据分级，也没有预注册。** 唯一的质量闸门是 `team-workflow` **B4 claim threshold**
   （可引用来源 / 已批准结论 / 显式假设）——它管"这句话**有没有出处**"，
   **完全不管**"这个结论**有没有被检验过、检验得够不够强**"。
2. **失败无家可归。** `research/literature/07-failure-modes-negative-results.md` 是**别人的**失败；
   我们自己的失败没有归档机制 → 只存在于聊天记录与记忆里。
3. **冲突只有半条规则。** B5 说"两个活跃结论不得互相矛盾"，但没写**如何产生决定性实验**去区分它们。
4. **路径系统与结论系统之间没有桥。** `paths/` 有冻结/解冻与评分，但"凭什么解冻"缺一个证据标准。
5. **最隐蔽的一条**：论文的 **pre-registered failure conditions 已经存在**（`research/scratch/macha_import/04_Paper_FINAL.md`），
   但它是一份**文件**，不是一个**每天会被走的机制**。

### 1.5 哪些已有设计必须保留

- `team-workflow` **A/B**（引用纪律、provenance、claim threshold、生命周期）——一个字不改；
- `papers/notes` 的 **maturity tier**（drafts → accepted → archive）；
- **literature dossiers + claim→dossier map**（仓库里最接近"证据系统"的东西，别动）；
- `paper-status.md` 的三态区分；`05-macha-question-tree.md` 的问题树；
- **边界守护**（V1–V3 的可检查部分）；
- `paths/` 的冻结/解冻骨架；`projects/` 的承接清单；
- `world view taxonomy/methodology.md` 的六阶段（作为方法论的**实例**保留，不并入）。

### 1.6 重复 / 过度设计 / 伪抽象

| 发现 | 处置 |
|---|---|
| `docs/research/`（正式）与 `research/`（试错）同名 | 不动结构，只在规范里点明分工；方法论文档放 `docs/` |
| `research/experiments/` 与 `research/projects/`、`plans/` 边界模糊 | 明确：`experiments/` = **研究实验记录**；`projects/` = 工程执行；`plans/` = 设计/计划。规范里写死 |
| `papers/notes/` 同时存在主题文档与成熟度目录 | 层级不纯（README 已承认）。保留，但在规范里指明"**成熟度优先**" |
| 路径一的 IC（Ive Chunk/Thread）自称数据组织层，却只有定义没有实测 | **已被冻结**——这正是新方法要能**正式表达**的状态：`questioned` 或 `observed`，**不是** `supported` |
| `00-technical-foundation.md` 的 D1–D10（10 项待拍板） | 过度设计的**倾向**：只有协议形状不可逆必须现在冻；其余按需。规范用"**只有不可逆的决定值得预注册**"来约束 |
| **伪抽象警戒**：任何"层/对象/门/字段"若无人使用即删除 | 写入规范 §10 预算条款 |

### 1.7 新 methodology 应该插在哪里

| 位置 | 内容 |
|---|---|
| 新增（规范） | `docs/research-methodology.md` |
| 新增（设计） | `docs/research-methodology-design.md`（本文件） |
| **只新增 2 个目录** | `research/questions/`（一个问题一个文件）、`research/failures/`（失败归档） |
| 不新增 | `hypotheses/`、`evidence/`、`syntheses/` —— 它们被**合并**进 Question 文件、Experiment 产物与 `papers/notes`（理由见 §2） |
| 接入点 | `team-workflow.md` 顶部一行 "See also"（**不改任何已批准规则**）；`research/README.md` Contents +2；根 `README.md` 导航 +1 |
| 不动 | `papers/notes` 分层、`research/literature/`、`layers/`、`research/projects/` |

---

## 2. 为什么这样设计（对齐给定优先级）

优先级：**epistemic correctness > operational simplicity > reproducibility > collaboration > scalability > formalization**。

| 设计 | 服务于 | 取舍 |
|---|---|---|
| 对象只有 6 个 | epistemic correctness + simplicity | 合并 Prediction（→实验字段）、Model（→假设字段/claim 类型）、Synthesis（→claim 类型） |
| 一个 Question 一个文件 | simplicity + collaboration | 牺牲"按对象类型检索"，换来"状态一眼可见" |
| 证据 4 级（E0–E3） | correctness | 等级是**上限**不是分数；防止"用等级装点" |
| 预注册 = 一个 YAML 块 + commit hash | correctness + reproducibility | **不造版本号系统**：交给 git |
| Gate 从 7 压到 4 | simplicity | 只保留"能阻断传播"的四道 |
| Failure 独立目录 | correctness | 因为失败最容易被悄悄丢掉 |
| 预算条款（6/2/4/10） | 全部 | 防止 framework 变成项目 |

**为什么不做 6 个对象目录**：一次探究会被拆散在 5 个文件里，导致"状态在哪儿"这个最该被解决的问题反而更糟。
**为什么不做 7 个 Gate**：G1/G2 常常是同一次 10 分钟讨论；门越多，绕过越多。
**为什么把 Synthesis 并进 Claim**：synthesis 只是"对多个 claim 的 claim"，它需要的仍是 §3 的证据等级与 §6 的 Gate 4。

---

## 3. 方法论锚点（参考了哪些已有科学方法）

> 这些是**方法学锚点**，用于说明设计不是凭空发明。
> **注意**：若其中任何一项要进**论文**，仍须走 `team-workflow` A2/A3/B3 的 provenance 与引用纪律——
> 本文档不构成可引用来源。

| 锚点 | 一句话 | 本方法落在哪 |
|---|---|---|
| Popper 的证伪主义 | 可反驳性是科学陈述的门槛 | §2.2 falsifier 必填、§4 证伪协议 |
| Platt《Strong Inference》(1964) | 多个竞争假设 + 决定性实验 | §2.2"每问至少 2 个竞争假设"、§4.3 冲突处理 |
| Mayo 的 severe testing | 一个实验只有在**有能力**反驳时才提供证据 | Gate 2 只判"实验有没有能力产生反驳" |
| 心理学/医学的**预注册与 Registered Reports** | 先冻结预测与条件，后看数据 | §4.1 预注册块 + commit hash |
| Merton 的科学规范（有组织的怀疑） | 制度化的怀疑，而非个人品德 | §6 Gate + §4.4 反例优先 |
| FAIR / 可复现性徽章（ACM badging） | 产物可查、可重跑 | §3.1 等级须附 provenance 与可重跑命令 |
| Design Science Research（Hevner） | 设计类研究要 artifact + evaluation 双轨 | §0 三层分工（工程 vs 论文）、§5 分层提醒 |
| 负结果期刊传统 | 失败也是知识 | §7 Failure 系统 |

---

## 4. 明确拒绝的设计（以及为什么）

| 被拒 | 理由 |
|---|---|
| 按对象建 6 个目录（questions/hypotheses/experiments/evidence/failures/syntheses） | 拆散单次探究；状态不可见；协作成本上升 |
| 7 个 Gate 照搬 | 官僚化；G1/G2、G3/G4 常在一次讨论内完成 |
| 自造版本号 / 状态字段版本管理 | 与 git 重复；会产生"文档版本 ≠ 代码版本"的假精确 |
| 独立 `evidence/` 目录 | 与 `research/literature/`（文献证据）和实验产物重复，制造**第二真源** |
| 独立的 `Model` 对象 | 模型的价值是"能推导出预测"；作为假设字段/claim 类型已足够 |
| 一套新的 claim/结论状态机 | 与 `papers/notes` maturity tier 冲突；改为**映射**而非新建 |
| 研究看板 / dashboard / 工具 | 现在做等于给没有内容的系统做报表；且它自己会成为新的漂移源（本文 §1.6 的教训） |
| 把 Minecraft Layer 的 8 步/V1–V5 当作 Macha 总体研究方法 | 它是**工程验收**；写成总体方法会污染研究层（规范 §0、§5） |
| 强制"每个 claim 必须有 E2+" | 不可达的场景会逼人造假；改为"**达不到就永久停在 E1 并标注**" |
| 为方法论设立专门的月度流程会 | 与预算条款冲突；门挂在**已有的**写作/评审动作上 |

---

## 5. Red Team（假设 v0.9 是错的，攻击它）

| # | 攻击 | 结论与修改 |
|---|---|---|
| RT1 | **"Prediction 单列是漂亮术语"** | 成立 → 合并为 Experiment 的**冻结字段**；对象从 9 → 6 |
| RT2 | "7 个 Gate 会拖慢研究" | 成立 → 压到 4 个；G1 明确为"5 分钟检查" |
| RT3 | "6 个目录是碎片化" | 成立 → 只留 `questions/`、`failures/` |
| RT4 | **"证据等级会制造虚假严谨感"** | 部分成立 → 加三条约束：①等级必须有 provenance + 可重跑命令；②等级是**上限**不是分数；③E3 必须来自跨环境或破坏性检验，**不得**来自"我觉得更可靠" |
| RT5 | "状态机与 git 重复" | 成立 → 删掉自造版本号；冻结凭证=commit hash；状态历史 append-only 且**与证据同一次提交** |
| RT6 | **"团队不会真的预注册"** | 成立 → ①模板压到 12 行、事前成本 <10 分钟；②Gate 2 只检查"是否已提交"，不检查文笔；③**给探索留合法通道**：探索性实验走 E0 通道，明确"不得升级为 claim"——否则大家会整体绕过流程 |
| RT7 | "Research Framework 自己变成项目" | 成立 → §10 预算条款 + 每季度删除无人使用的对象/字段 |
| RT8 | "把 Minecraft 的实验方法误写成 Macha 总体方法" | 成立且危险 → §0 三层分工 + §5 分层提醒（工程验收 vs 研究实验） |
| RT9 | "与 `team-workflow` 冲突" | 已防 → B4 不变；只为**上游**（证据等级），不建第二套阈值；只加一行 See also |
| RT10 | **"E2/E3 在现实里不可达"** | 成立 → 承认并制度化：不可达时 claim **永久停在 E1 并显式标注**；"该问题在当前条件下不可判定"是**合法结论** |
| RT11 | "谁来当 reviewer？单人团队会自我批准" | 成立 → Gate 2/Gate 4 需**至少一名非作者**；若确实无人，文件里显式标 `self-approved`（可见的债），而不是假装过了评审 |
| RT12 | "哪些东西该交给 git/code，而不是方法论？" | 答案写进 §9 R9：**版本历史、可复现性（脚本）、指标计算、环境 pin** 全部交给 git 与代码；方法论只管**声明与判定** |

### 5.1 因 Red Team 而产生的修改（v0.9 → v1.0）

1. 对象 9 → **6**（Prediction/Model/Synthesis 合并）；
2. Gate 7 → **4**；
3. 目录 6 → **2**；
4. 删除自造版本号，冻结凭证用 commit hash；
5. 证据等级加"上限而非分数""必须可重跑"两条硬约束；
6. 新增**探索性实验合法通道**（E0，不得升 claim）；
7. 新增 `self-approved` 显式标记（应对无人评审）；
8. 新增 §10 预算条款；
9. 新增"不可判定是合法结论"；
10. §0/§5 明确**工程验收 ≠ 研究实验**。

---

## 6. 未来可能需要升级的地方（触发信号）

| 信号 | 需要的升级 |
|---|---|
| `research/questions/` 超过 ~15 个文件 | 生成式索引（**禁止手写**看板） |
| 出现外部复现需求 | Artifact 发布规范（版本、环境、许可） |
| benchmark 成规模或对外 | **预注册测试集 + 版本化阈值**；调参集与测试集分离 |
| 多人同时改同一 Question | owner 字段已在；再加"编辑锁"或拆文件 |
| E3 成为常态 | 独立复现协议（谁复现、如何判定"复制成功"） |
| Gate 成为瓶颈 | **先砍 Gate 1**，把它的检查项并入 Gate 2 |
| 论文进入投稿期 | Claim↔Evidence 的**逐条对照表**（一张表，不是新体系） |

**不升级的条件**：只要上面没有信号出现，v1.0 的规模（6/2/4/10）就不再扩张。
