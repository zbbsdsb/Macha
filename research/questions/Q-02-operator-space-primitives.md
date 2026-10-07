# Q-02 五个候选算子（SELECT / RELATE / TRANSFORM / TEST / COMMIT）能不能表达一次真实的认知过程？

status: pre-registered   # observed → questioned → pre-registered → tested → supported│weakened│falsified → revised│abandoned│promoted
owner: TBD
opened: 2026-10-07
related: 路径一 [`../paths/01-sepmay-ivy/operator-space.md`](../paths/01-sepmay-ivy/operator-space.md) ·
         [`../paths/01-sepmay-ivy/open-decisions.md`](../paths/01-sepmay-ivy/open-decisions.md)（D8/D9/D10/D11）·
         [`../plans/operator-sandbox-plan.md`](../plans/operator-sandbox-plan.md)（实施计划）·
         [`../../docs/research-methodology.md`](../../docs/research-methodology.md)

## 1. Observation

- 玩家拿走箱子里的东西 → 玩家离开 → 很久以后再次出现。NPC 需要做到的事只有一件：
  **第二次见面时，它知道自己曾经知道过这件事。** 这件事在仓内没有任何实现。
- `operator-space.md` §1.2 审计结论：仓内"算子"只有三处**标签**（`architecture.md` §1.5 那一行的
  `Written by / Read by` 两栏都是 `—`；SepMay 路径 §2 图里一个空盒子），**零定义**。
- 而**形态上已经存在**五个像算子的东西，散在两种语言里、没有统一语义、没有 trace：
  `Memory.retrieve()`（`src/macha/core/memory.py`）像 SELECT · `Perception.process_text()` 像 TRANSFORM ·
  `ActionValidator.validate()` 像 TEST · `ResultCorrelator` 像 RELATE · 回流三路像 COMMIT。
- 症状（`../paths/01-sepmay-ivy/README.md` §6）：连续数轮都在**定义概念**，没有任何一项被现实检验。

## 2. Question

**用 SELECT / RELATE / TRANSFORM / TEST / COMMIT 这五个动作，能否表达"玩家偷走东西 → 离开 → 很久以后回来"
这段认知过程里的 continuity（还记得）、reinterpretation（改了看法）、contradiction（两种说法同时留着）？**

- 若答案是"能" → 这五个算子是一个**可用的最小集**，可以进入 Core Phase 3 的候选实现
  （以决策记录提升，不顺手搬代码）。
- 若答案是"不能" → 至少要指出**缺哪一个**、或**哪一个是多余的**；这比"能跑通"值钱。
- **会改变什么**：`operator-space.md` §3 的候选基增删 · D10（可分性/完备性）·
  `architecture.md` §1.5 那个全 `—` 的算子行第一次有内容可填。
- 文献是否已答：**没有**。仓内 `research/literature/` 七份 dossier 无一份讨论 primitive operator 分解；
  外部相关工作（Generative Agents / MemGPT / ACT-R）都是**整体架构**，
  没有把认知过程拆成五个可判定动作并逐条 trace 的做法。

## 3. Hypotheses（≥2 个互相竞争）

> 三个实验共用这三条。每条都必须能被 trace 杀死。

- **H-A 边界假设**：临时/持久边界（Thread 工作集 vs append-only State，只有 COMMIT 有写权）
  本身就足以产生 continuity。机制 = Thread 关闭时工作集丢弃、State 保留，第二次 SELECT 读 State 即可。
  预测 = Exp1 四条判据全过，且 trace 里除 COMMIT 外无任何 `state_version` 变化。
  ｜ **falsifier**：Thread B 取不回 A 提交的内容；或 trace 出现非 COMMIT 的 State 写入。

- **H-B 分解假设**：算子分解的价值**不在于结果更对，而在于能指出是哪一步造成的改变**。
  机制 = 每步都留下可归因记录（`output_refs` + `state_version` 前后 + `why`），因此 `prog` 运行的
  trace 能定位改变来源，而压成一步的 `mono` 运行不能——即使两者终态完全相同。
  预测 = `prog` 与 `mono` **终态相同**，且 `prog` 的 `attributable_steps` 与"可指认的中间产物数"
  严格多于 `mono`（`mono` 两者均为 1 步 / 0 个中间产物）。
  ｜ **falsifier**：`prog` 也指不出"是哪一步造成的改变"（例如所有状态变化都只能归到同一个 TRANSFORM 调用），
  或 `mono` 的终态与 `prog` 不同（则分解引入了额外行为，不是等价对照）。

- **H-C 冗余假设（与 H-B 竞争）**：在 continuity 这一档，SELECT 与 TRANSFORM 是**同一个动作**，
  五算子在本任务上过细。机制 = SELECT 只改 focus、TRANSFORM 只换表征，而 Exp1 里"取出事实"与
  "把事实变成结构化陈述"在时间上不可分。
  预测 = Exp1 中 SELECT 步骤对最终 `state.json` **零贡献**（删掉它，`prog` 终态不变、trace 步数少一）。
  ｜ **falsifier**：删掉 SELECT 后 `prog` 无法取回 unit（说明"选择"与"变换"确实是两件事）。

> **三者的关系**：H-A 与 H-B 不互斥（可以既边界成立、分解也必要）。**H-C 与 H-B 互斥**——
> 若 SELECT 真是装饰，则"分解带来可归因性"是幻觉，归因到的其实是 TRANSFORM 一个动作。
> 这正是本问题最可能出现的真发现。

## 4. Pre-registration（**提交后不得修改**）

```yaml
prereg: d24f2dbdc2211fc1c610d09a54f05087306dfed1   # 预测内容冻结于该提交；本行于第二次提交回填
experiment: E-S1（Continuity）。一个 NPC，两次「见到玩家」：
             Thread A：seed I1「玩家拿走了箱子里的东西」→ SELECT → TRANSFORM(normalize) → COMMIT → 关闭；
             Thread B：**不 seed 任何东西** → SELECT(state) → 关闭。
             对照 mono：同等输入同等输出，压成一步（不产出中间产物、不做算子分解）。
env: Python 3.13（stdlib only，无第三方依赖，无网络，无 LLM）；逻辑时钟（非墙钟）；迭代按 id 排序；
     沙盒代码 research/experiments/operator_sandbox/；固定 PYTHONHASHSEED
baseline: 无（首次运行，无历史基线）
control: mono —— 同输入、同 State 终态要求的**不透明整体动作**，用于分离"结果"与"可归因性"
metrics: research/experiments/operator_sandbox/metrics.py（机械计算，不靠人读）→ runs/exp1/metrics.json
          · attributable_steps = 改变了 State 版本或 focus 的步数 ÷ 总步数
          · unmapped_steps   = 既未改 State、未改 focus、未产出 derived unit 的步数（=无法说明作用的步）
          · reuse            = 本次用的 operator/provider 名与其它实验的交集（首轮无其它实验 → null）
          · 【预登记时已知缺陷】attributable_steps 对 prog 与 mono 都可能等于 1.0，无法区分；
            因此**同时**记录两个原始计数：intermediate_units（派生 unit 数）、
            attributable_changes（可唯一归因到某一步的 State/focus 变化数）。
            这两个数在 mono 上必须是 0 / 1，在 prog 上必须 > 1 —— 否则 H-B 被杀死。
expected: H-A：state 最终 version = 1（只有一次 COMMIT），Thread B 取回条目数 = A 提交条目数，
          trace 中除 COMMIT 外 state_version 不变。
          H-B：prog 终态与 mono 逐 key 相同；prog 的 attributable_changes ≥ 2 且 mono = 1。
          H-C：删掉 SELECT 后 prog 终态不变（则 SELECT 是装饰）。
falsification: H-A 死 ← B 取不回 / 出现非 COMMIT 的 State 写入（F7 边界发现，非算子空间的错）
               H-B 死 ← prog 与 mono 终态不同，或 prog 的 attributable_changes = 1（F1）
               H-C 死 ← 删掉 SELECT 后 prog 取不回 unit（F1：SELECT 与 TRANSFORM 可分）
               本实验作废 ← 事后改动本块（F4）
```

### 4.1 关于 `prereg:` 的回填

方法规范 §4.1 要求预测块带 commit hash。做法：**先提交本文件（预测内容冻结）→ 再回填 hash → 第二次提交**。
第二次提交**只改 `prereg:` 一行与 §8 状态历史**，不触碰 `experiment / env / baseline / control / metrics / expected / falsification`。
若第二次提交动了预测内容，本实验按 F4 作废。

### 4.2 另两个实验的预注册（**本块不含它们**）

`E-S2`（Reinterpretation）与 `E-S3`（Contradiction）**在各自开工前另开一块预注册**，
沿用 §4.1 的两步提交做法，并在 §8 记明"为什么新增"。
理由：方法规范规则 1 要求预测先于该次实验冻结；把三个实验写进同一块会让后两个失去"先注册"的效力。

## 5. Experiments

| ID | 做什么 | 对照 | 状态 |
|---|---|---|---|
| **E-S1** | Continuity（§4 已预注册） | `mono` 不透明大步 | 🔄 进行中（2026-10-07 开工） |
| **E-S2** | Reinterpretation：v2 ≠ v1 且 v1 仍在；改变**不能**全由 TRANSFORM 一个人完成 | `mono` | ⬜ 待预注册 |
| **E-S3** | Contradiction：终态保留双方 + `verdict=conflict`，不静默选边。**必须两份独立编码结论一致**，否则本实验结论为"不确定" | `mono` + 第二编码 | ⬜ 待预注册 |

产物路径：`../experiments/operator_sandbox/runs/exp1/{prog,mono}/`
（各含 `trace.jsonl` + `state.json` + `metrics.json`，提交进 git 作为可逐行审查的证据）

## 6. Evidence

*（空——E-S1 尚未跑完。等级上限 E0–E3；产物路径与可重跑命令在此登记。）*

可重跑命令（写此栏时必须已实测通过）：

```text
python -m pytest research/experiments/operator_sandbox -q
python research/experiments/operator_sandbox/run_experiment.py exp1
```

## 7. Failures

*（空——按 `../failures/README.md` 归档 F1–F7。特别注意：F3/F4/F5 不得当作负面研究结论使用。）*

## 8. Status history（append-only）

| 日期 | 状态 | 依据 | commit |
|---|---|---|---|
| 2026-10-07 | observed | §1 的四条：算子只有标签没有定义 · continuity 无实现 · 路径 §6 的"只定义不检验"症状 | — |
| 2026-10-07 | questioned | 通过 Gate 1：可判定（trace 里能判）· 会改变候选基增删与 D10 · literature/ 无覆盖 | — |
| 2026-10-07 | pre-registered | 通过 Gate 2：H-A/H-B/H-C 三条竞争假设各带机制+预测+falsifier；E-S1 预测块已写死（含已知的 `attributable_steps` 缺陷与两个补充原始计数） | `d24f2d` |
| 2026-10-07 | pre-registered | 回填 `prereg:` hash（§4.1 第二次提交）。**仅改 `prereg:` 一行与本表**，预测块其余内容未动 | 见下条 commit |

## 9. Next questions

- **U1**：SELECT 真的不产生信息吗？还是"选择依据"本身就该是一条新信息？（E-S1 的 trace 可判）
- **U2 / D10**：RELATE 会不会被二元的 TEST 吸收？（要等 E-S2/E-S3）
- **U3 / D9**：沙盒允许处理中途 COMMIT，SepMay 只允许 Chunk 关闭时回流——哪个语义是必须的？
  （E-S1 若**需要**中途 COMMIT 才能取回，则 D9 有证据；否则说明关闭时回流够用）
- **U4**：State 只要 append-only 就够，还是需要版本/取代语义？（E-S2 的 v1/v2 并存）
- **U9**：线性程序够不够？若 E-S2/E-S3 需要"若 TEST=conflict 才走那条"，说明分支是必需能力，
  还是说明**算子划分错了**？
