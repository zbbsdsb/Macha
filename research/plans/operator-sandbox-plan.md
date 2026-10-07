# Operator Sandbox — 第一阶段实施计划（PLAN ONLY）

> **STATUS: PLAN — 本轮不写代码。** 计划日期 2026-09-25。
> **目标**：建一个足够小的 **Operator Interpreter / Cognitive Sandbox**，让五个候选 primitive
> （`SELECT / RELATE / TRANSFORM / TEST / COMMIT`）能真的跑起来，并用三个最小实验回答
> "这套算子空间能不能表达 continuity / reinterpretation / contradiction"。
> **不是**目标：证明五个已完备、把 SepMay 设计完、写 Core/SDK。
>
> 上游设计：[`../paths/01-sepmay-ivy/operator-space.md`](../paths/01-sepmay-ivy/operator-space.md)（研究草案）·
> [`../paths/01-sepmay-ivy/README.md`](../paths/01-sepmay-ivy/README.md)（IC 路径本体）·
> [`../paths/01-sepmay-ivy/open-decisions.md`](../paths/01-sepmay-ivy/open-decisions.md)（D8–D11）·
> 方法规范：[`../../docs/research-methodology.md`](../../docs/research-methodology.md)（Gate 1–4 · 十条规则 · §10 预算上限）

---

## 1. Repository Audit（基于真实仓库，不假设结构）

### 1.1 运行时与语言（实测）

| 侧 | 事实 | 出处 |
|---|---|---|
| Python | `requires-python >=3.10`；setuptools，`packages.find where=["src"]`；依赖仅 `pydantic>=2.0` + `pyyaml>=6.0`；dev 依赖 `pytest>=7.0` + `ruff>=0.4` | `pyproject.toml` · `requirements.txt` |
| Python 测试 | `[tool.pytest.ini_options] testpaths = ["tests"]` —— **只收根 `tests/`** | `pyproject.toml` |
| JVM | 独立 Gradle 构建根（不在仓库根）；Java **25** / Kotlin **2.4.20** / Gradle **9.7.1**；Minecraft 26.2 / Paper API | `layers/gradle/libs.versions.toml` · `layers/settings.gradle.kts` |
| JVM 模块 | `:kit:protocol` `:kit:runtime` `:kit:transport` `:minecraft` `:simulator` `:testclient` | `layers/settings.gradle.kts` |
| CI | **不存在**（无 `.github/`）。任何"测试会自动跑"的假设不成立 | 目录实测 |

### 1.2 Python 侧实际内容（全部 6 个文件，非认知骨架）

| 文件 | 行数 | 内容 |
|---|---|---|
| `src/macha/core/agent.py` | 48 | `Observation{content,source,timestamp,metadata}`、`ActionResult`、`BaseAgent` 三个方法全 `NotImplementedError` |
| `src/macha/core/memory.py` | 38 | `MemoryItem{content,importance,timestamp,kind,metadata}`；`Memory.add/retrieve/all`，`retrieve()` 只返回最后 N 条（`TODO: proper scoring`） |
| `src/macha/core/perception.py` | 15 | `process_text(text, source) → Observation` |
| `src/macha/core/reasoning.py` | 19 | `decide()` 返回一句硬编码字符串（`TODO: call LLM`） |
| `src/macha/core/action.py` | 15 | `execute(decision) → ActionResult` 直通 |
| `src/macha/__init__.py` · `core/__init__.py` | 63/47 字节 | 仅导出 |
| `tests/test_smoke.py` | 8 | 一个 assert：add 一条再 retrieve 回来 |
| `examples/hello_agent.py` | 29 | 演示四个模块怎么接；`examples/README.md` 明说"不是能用的 agent" |

**结论**：Python 侧**没有任何状态机、没有工作集、没有算子、没有 trace、没有可运行的循环**。

### 1.3 Kotlin 侧实际内容（Layer，**非认知**）

- `kit/runtime`：`LayerRuntime`、`ActionDispatcher`、`ActionValidator`、`ObservationScheduler`、`EventThrottle`、`ResultCorrelator`、`port/ClockPort`、`port/EnvironmentPort`（+4 个测试）。
- `kit/protocol`：`Envelope`/`Messages`/`Payloads`/`Capability*`/`ActionVocabulary`/`Codes`/`ProtocolCodec`（+4 个测试）。
- `kit/transport`：`HttpControlPlane`、`WebSocketDataPlane`、`SessionHandshake`、`JsonFraming`（+2 个测试）。
- `minecraft`：plugin + adapter（Paper 端口/事件/观测/执行/注册表）。`testclient`：`VerticalSliceProbe`。
- `simulator`：**仍是骨架**——`collectObservation` 返回 `null`；`execute` 一律
  `REFUSED(not_supported, "simulator action execution not wired yet (scaffold)")`。

**结论**：Layer 侧有协议、有运行时、有"拒绝"语义，但**没有认知、没有算子、没有任何信息变换概念**；
按 `V3`，算子空间**绝不能**落在这一侧。

### 1.4 文档侧（与本计划直接相关的）

| 文档 | 提供什么 |
|---|---|
| `research/paths/01-sepmay-ivy/operator-space.md` | 算子定义、五个候选、作用对象三选、组合、状态语义、E-OS1/E-OS2/E-OS3、禁止清单 |
| 同上 `README.md` §4 §6 §8 | IC 已定基线、**解冻条件三条**、解冻后的最小可证伪版本（Chunk = {开启触发器·预算档·局部工作集·关闭触发器·回流记录}） |
| 同上 `open-decisions.md` | `D1–D11`；其中 **D8/D9/D10/D11** 与本计划直接耦合 |
| `docs/architecture.md` §1.5 | 接收域=准入；内部信息源只由关闭时回流写；**"算子集合 operators"一行 Written/Read 都是 `—`** |
| `docs/research-methodology.md` | Gate 1–4、状态机、十条规则（**规则 2：没有 Question 的实验叫工程验收，不叫研究**；规则 10 + §10 **预算上限**） |
| `research/experiments/README.md` | 边界表：研究实验记录 + **实验脚本/数据/transcript 索引 → 这里**；设计/计划文档 → `../plans/`；工程验收 → `../projects/` |
| `research/questions/README.md` | Question 模板（12 行）、Gate 1 判据、状态取值、探索性实验的 E0 通道 |

### 1.5 仓库现实与文档的偏差（必须先知道，否则计划会建立在幻觉上）

1. **`tools/` 目录不存在**，但根 `README.md` 记录了 `tools/stub-core/`（"Python stub counterpart for the Layer"）。
   即：文档承诺的非 Macha 工具树**还没建**；MC 项目的 Stub Core（M5）也**尚未实现**。
2. **没有 CI**（无 `.github/`）。
3. 根 `tests/` 只有 1 个 8 行的 smoke test，且 pytest 只收 `tests/`。
4. `src/macha/**` 全是 `NotImplementedError` / `TODO` —— 评估文档所称"非认知骨架"属实。
5. "算子"在仓内**只有三处标签**（`operator-space.md` §1.2 已记录），没有任何 abstraction。
6. `Method` / `Flow` / `Method Spec` / `Learner` **零命中**（`operator-space.md` §1.6 已记录）。

### 1.6 已存在、但没被命名为 Operator 的 abstraction（本计划的直接依据）

| 现有物 | 位置 | 形态上像哪个算子 | 缺什么 |
|---|---|---|---|
| `Memory.retrieve()` | `src/macha/core/memory.py` | **SELECT**（取回条目） | 没有选择依据，只取最后 N 条 |
| `Perception.process_text()` | `src/macha/core/perception.py` | **TRANSFORM**（文本→结构化 `Observation`） | 没有任何变换语义定义 |
| `ActionValidator.validate()` | `layers/kit/runtime/.../ActionValidator.kt` | **TEST**（谓词→判定/`refused`） | 判定结果不是领域结论，而是协议拒绝 |
| `ActionDispatcher` | 同上目录 | **Selection**（决定派给谁） | Layer 侧调度，不作用于信息 |
| `ResultCorrelator` | 同上目录 | **RELATE**（请求 id ↔ 结果关联） | 只关联协议消息，不关联知识 |

**回答"有没有已存在的 abstraction"：有形态，但分散在两种语言、两个层级，没有统一语义、没有 trace、没有可组合性。**
这正是本沙盒要在一个地方（Python、无依赖）把它们命名并跑起来的原因。

---

## 2. Architecture Fit（算子在现有架构里挂哪一层）

### 2.1 三层排除

| 候选位置 | 判定 | 理由 |
|---|---|---|
| `layers/**`（Kotlin） | ❌ 排除 | 硬规则 V3：Layer 零认知（`decision-layer-first-sequencing.md` §3；`architecture.md` §0 规则 2） |
| `src/macha/**`（Macha Core） | ❌ 本轮排除 | ① MC 项目的硬边界写着"**不改 `src/macha/**`（V1）**"；② SepMay 路径**仍处冻结**（README §6 解冻条件未触发）；③ 现在冻 Core 接口 = 把错误接口固化成标准 |
| 根 `tests/` | ❌ 排除 | `testpaths=["tests"]` 属于 Macha 的测试面；研究代码混进去等于让 Core 的 CI 依赖研究产物 |

### 2.2 决定（含理由）

| 产物 | 位置 | 为什么在这里 |
|---|---|---|
| **本计划** | `research/plans/operator-sandbox-plan.md` | `research/experiments/README.md` 边界表：**设计/计划文档 → `../plans/`**；同目录已有 `literature-intelligence-plan.md` / `minecraft-layer-validation-plan.md` 先例 |
| **代码 + 测试** | `research/experiments/operator_sandbox/` | 同一边界表：**实验脚本、数据、transcript 索引 → `../experiments/`**。且 `research/` 是明确"可删、可重写、无仪式"的层——沙盒第一阶段本来就该是这种永久度 |
| **跑批证据** | `research/experiments/operator_sandbox/runs/<exp-id>/`（`trace.jsonl` + `state.json`） | 沿用 MC 项目的"原始证据落 transcript"纪律；**可提交进 git**（体积小、是复现依据） |
| **实验登记** | `research/questions/Q-02-*.md`（**本轮只是计划，不创建**） | 规则 2：没有 Question 的实验叫工程验收。三个实验若要成为"研究"，必须先在 Gate 1/Gate 2 下注册 |

**不新建 `tools/` 的理由**：`docs/research-methodology.md` §10 的预算上限要求"新增目录必须回答**它替代谁**"。
`tools/` 在本轮替代不了任何东西——沙盒不需要它，而且它被文档承诺的用途是 Layer 侧的 Stub Core（另一个工程）。
等沙盒活过两轮实验、需要被独立调用时再谈。

### 2.3 与既有边界的接口（本轮**只读不写**）

```text
research/plans/operator-sandbox-plan.md      ← 本文件（"要什么 + 怎么干"）
        ↓
research/experiments/operator_sandbox/       ← 代码 + 测试 + runs/（证据）
        ↓  只通过"计划中的 Q-02"与下列文档发生关系，不修改它们
research/paths/01-sepmay-ivy/operator-space.md（上游设计）· open-decisions.md（D8–D11）
docs/architecture.md（§1.5 算子那一行）· src/macha/**（V1，禁改）· layers/**（V3，禁改）
```

**未来提升路径（写明条件，避免现在就设计）**：若五个算子在两轮实验后仍成立，则"运算域算子层"成为
Macha Core Phase 3 的**候选实现**，届时以**决策记录**（`papers/notes/accepted/decision-*.md`）提升进
`src/macha/core/`，而不是顺手搬代码。**在此之前，沙盒不是 Core，Core 不依赖沙盒。**

### 2.4 语言与依赖决定（Python / 纯标准库）

| 决定 | 理由 |
|---|---|
| **Python 3.10+** | ① 算子在 **Core 侧（运算域）**，而 Core 就是 Python（`src/macha`、`requires-python>=3.10`）；② 若算子层活下来，将来提升进 Core **不用重写**；③ replay / 确定性用标准库最容易做（无 JVM toolchain、无 Gradle、无构建等待） |
| **不用 Kotlin** | `layers/**` 是 Layer，硬规则 **V3：Layer 零认知**。算子一旦写进 Kotlin，边界就漏了 |
| **只用标准库**（`dataclasses` / `json` / `pathlib` / `argparse`） | 项目现有依赖里有 pydantic，但**不用它**：`Unit` 只有 6 个字段、没有校验需求。少一个 import 面，沙盒就能在任意干净 Python 里直接跑（不必 `pip install -e .`），这对"第三方按 README 复现"是关键 |
| **pytest** | 已是 dev 依赖，不新增 |
| **明确不引入** | 无向量库、无 LLM SDK、无网络、无 async、无 ORM（§9 延后清单） |

**这个选择的唯一真代价**：Python 的 dict/set 迭代顺序与 `PYTHONHASHSEED` 会破坏复现性。对应三条硬纪律
（已写进 §5/§6/§8）：**迭代一律排序**（按 `id`）· **逻辑时钟而非墙钟** · **replay 测试固定 hash seed**。
这不是隐患，是实现时必须遵守的约束。

> 一句话：**Python 是"将来能长成 Core"的语言，标准库是"今天不引入任何新依赖"的选择。**
> 代价是确定性要靠纪律，而不是靠运行时保证。

---

## 3. Minimal Data Model

四个概念，对应四件事；**字段数量设硬上限，超了必须先删一个**。

### 3.1 `Unit`（Information 的载体）

| 字段 | 说明 | 是否必需 |
|---|---|---|
| `id` | 稳定、可排序（`u0001` 递增），复现性依赖它 | ✅ |
| `payload` | 内容；v1 是**结构化 dict 或字符串**，不做多态体 | ✅ |
| `origin` | `external`（准入进来的）或 `derived`（算子产出的） | ✅ |
| `created_by` | 产出它的算子调用 id（`external` 时为 `null`） | ✅ |
| `refs` | 它引用的其它 unit id（派生物用；关系/判定的落点） | ✅ |
| `logical_ts` | **逻辑**时间（计数器），不用墙钟 | ✅ |

**明确不放进 `Unit`**：`importance`、情绪、置信度评分、embedding、关系类型枚举。
（`MemoryItem.importance` 是 Core 的既有字段；本沙盒不复制它——重要性属于"什么值得记住"，而按设计
**COMMIT 不决定这件事**，见 §4.6。）

### 3.2 `Workspace`（Thread = 一次正在进行的认知过程）

| 组成 | 说明 |
|---|---|
| `inputs` | 本 Thread 准入进来的外部 unit（只读引用） |
| `units` | 工作集：外部 + 派生 unit 的索引 |
| `focus` | 当前聚焦的 unit id 集合（**SELECT 的唯一产物**） |
| `status` | `open` / `committed` / `failed` / `closed` |
| `thread_id` | 稳定 id；trace 用 |

**与 Persistent State 的区别（本计划最重要的边界）**：

| | Thread / Workspace | Persistent State |
|---|---|---|
| 生命周期 | 一次认知过程；结束后丢弃 | 跨 Thread 存活 |
| 谁能写 | 除 `COMMIT` 外**任何算子的输出都只落在这里** | **只有 `COMMIT`** |
| 是否进 trace | 是（每个 op 的 before/after 引用） | 是（版本号变化） |
| 是否可被下一次 SELECT 看见 | 否（Thread 结束即不可见） | 是 |

**组成项的归属（"Thread 需要考虑什么"的逐条落地）**：

| 考虑项 | 落点 | 说明 |
|---|---|---|
| `inputs` | `Workspace.inputs` | 本 Thread 准入的外部 unit（只读引用） |
| `working objects` | `Workspace.units` | 外部 + 派生 unit 同居一处，靠 `origin` 区分 |
| `intermediate outputs` | `Workspace.units` 里的 `derived` unit | **不另设"中间结果"层**——多一层就多一种状态语义 |
| `operator trace` | **不进 Workspace** | trace 是跨 Thread 的执行记录，由 runner 统一写（§6）。放进 Workspace 会让"工作集"与"审计日志"混成一个东西 |
| `status` | `Workspace.status` | 见上表 |

### 3.3 `State`（跨 Thread 持续存在的信息）

- 形态：**append-only 条目列表** + 单调递增 `version`。条目 = `{key, unit_id|payload, committed_from(thread_id, op_id), version}`。
- **不做 update-in-place**：Exp2（重新解释）必须能看到"旧版还在"，这正是权威历史与 replay 的前提。
- **不做 ontology**：`memory / belief / relationship / emotion / goal / identity` 只登记为**可能的 key 前缀**，
  不建模、不设 schema、不写类型。等实验逼出需要再加（D8 的性质）。
- `key` 的取值由**场景**声明（v1 就两个 key：`events/*`、`interpretation/*`），不由 operator 发明。

### 3.4 `Operator`（统一语义见 §4.1）

### 3.5 与现有 abstraction 的映射（不复制代码，只对齐形状）

| 沙盒概念 | 现有对应物 | 处理方式 |
|---|---|---|
| `Unit`(external) | `Observation`（`agent.py`）· `MemoryItem`（`memory.py`） | **镜像字段形状，不 import**（避免研究代码反向绑架 Core） |
| `Workspace` | IC 的"**局部工作集**"（`README.md` §8 的 Chunk 五元组之一） | 概念同名对齐，实现独立 |
| `State` | "内部信息源"（`architecture.md` §1.5）· `Memory` | 只对齐"append-only + 只有关闭/提交流程能写"这一条 |
| `Operator` | **无**（§1.6 的五个形态分散在两语言） | 本沙盒第一次给它统一语义 |

---

## 4. Primitive Operator Contracts

### 4.1 共同语义（所有算子一致，不交给具体算子）

| 面 | 共同语义 |
|---|---|
| **Input** | 一个 `Workspace` 的只读视图 + **显式 `input_refs`**（unit id 列表，可为空）+ `params`（dict） |
| **Output** | 一条 `OpResult`：`output_refs`（新/被选中的 unit id）+ `status ∈ {ok, failed}` + `note` |
| **Execution Context** | `thread_id` · `op_id` · `logical_ts` · `provider/comparator 名`（谁提供的确定性实现） · **只读的 State 视图**（版本号） |
| **State Mutation** | **只有 `COMMIT` 允许**（默认 `None`；越权 = 硬失败） |
| **Trace** | 由 runner 统一写（算子不自己写 trace，避免格式分裂） |

**交给具体算子的部分**：如何解释 `params`、如何挑/建 unit、判定枚举、以及"用哪个 provider"。

### 4.2 SELECT

- **v1 职责**：按**声明式依据**（`kind` / `payload` 字段匹配 / 显式 id 列表 / 是否 `derived`）从
  `Workspace.units` + `State` 只读视图里挑出 unit，写入 `focus`。
- **它回答的核心问题**：**是否产生新信息？→ v1 的答案是"不"**：只改 focus，`origin` 不新增任何 unit。
  （这条是可测的：Exp1 的 trace 里 SELECT 的 `output_refs` 必须都指向已存在的 id。）
- **明确不做**：embedding / 向量检索 / 相关性打分 / LLM 判断 / 语义模糊匹配。
- **第一版实现**：纯函数 + 排序确定性（按 id 排序，不依赖 dict 顺序）。

### 4.3 RELATE

- **v1 职责**：在 ≥2 个 unit 之间建立一条**显式关系**，产物是一个 `derived` unit
  （`payload = {kind: "relation", rel: <声明的关系名>, members: [ids...]}`）。
- **它回答的核心问题**：关系是 Thread-local 还是 State？→ **v1 默认 Thread-local**：
  RELATE 只写 `Workspace`，**不 COMMIT**。关系要进 State，必须由后续 `COMMIT` 显式提交。
- **关系名**由场景声明（v1 只有 `negates` / `explains` / `same_subject` 三个候选），**不建关系 ontology**。
- **待验证风险**：RELATE 可能被二元的 `TEST` 吸收（见 §12 与 D10）。

### 4.4 TRANSFORM

- **v1 职责**：把 unit 的 `payload` 变成另一种表征 / 另一抽象层，产物是新 `derived` unit，
  `refs` 指向输入（**保真度判据 = 可对回**：新 unit 必须能通过 `refs` 找回输入）。
- **边界（用户明确要求）**：**Core 只定义 transformation 语义，不内置 LLM 推理。**
  具体实现来自 **provider seam**：`TRANSFORM(params.transform_name)` → 场景注册的**确定性纯函数**
  （v1 只有两个：`normalize`（字符串→结构化 dict）、`reinterpret`（按 `negates`/`explains` 改写 interpretation key））。
- **明确不做**：LLM / 模型 / 外部服务 / 抽象层级的自动选择。

### 4.5 TEST

- **v1 职责**：对 ≥1 个 candidate（unit）施加一个**声明式 comparator**，返回判定
  `verdict ∈ {support, conflict, unknown}` + 证据引用（`refs`）+ 差异位置。
- **明确不做**：logic engine、规则引擎、概率推理、不确定性演算（`uncertainty` 留作 §11 的开放问题）。
- **第一版实现**：comparator 是场景声明的纯函数（v1：`exact`（dict 相等）、`negation`（按 `negates` 边））。
- **它回答的核心问题**：判定必须**显式落盘**才算发生（否则不可观测）——v1 让 TEST 产出 `derived` unit。

### 4.6 COMMIT

- **v1 职责**：把 `Workspace` 中**显式指定**的 unit（或 unit 组合）写入 `State`，追加条目 + 抬 `version`。
- **第一版唯一允许产生持久状态变化的 primitive。**
- **明确（用户指定）**：**COMMIT 不决定"什么值得记住"**。它只执行 state mutation；
  "值得"这个判断若存在，属于上游决定（本轮不实现，登记为 §11 开放问题）。
- **不做**：去重策略、重要性打分、摘要压缩、淘汰/遗忘。

---

## 5. Execution Model

- **Program = 线性 `OperatorCall[]`**；`OperatorCall = {op, params, input_refs?}`。
  **不设计 DSL**（不做 grammar、不做解析器、不做文件格式）。
- **数据流**：算子输出进 `Workspace`，后续算子通过 `input_refs` 显式引用或通过选择依据隐式取用。
  因此**一个输出天然可以被多个后续算子使用**（它就在工作集里）——不需要额外机制。
- **分支 / 循环**：**v1 一律不允许**。若实验中确实需要条件分支（例如"若 TEST=conflict 才走这条"），
  先把它记为**发现**（说明线性程序不足），不要当场加机制。
- **Thread 生命周期**：`open(thread_id)` → `seed(external units)` → `run(program)` → `COMMIT` → `close`。
  关闭后 `Workspace` 丢弃（只有 trace 与 State 留存）。
- **写权限守卫**：只有 `COMMIT` 模块可以 import `state` 写入函数；其余算子拿到的是只读视图。
  建议加一条**边界守卫测试**（扫描算子模块的 import），沿用 `layers/kit` 的 boundary-guard 思路。
- **失败语义**：缺输入、未知算子、未知 comparator/provider → **硬失败**（抛错 + trace 记 `status=failed`）。
  **禁止静默 no-op**——静默会让 trace 撒谎，而 trace 是本阶段唯一的证据来源。

---

## 6. Trace Model

一次算子执行 = **一行 JSONL**，字段固定，不扩展：

```json
{"seq": 3, "thread": "t-002", "op": "TEST", "params": {"comparator": "negation"},
 "input_refs": ["u0004","u0007"], "output_refs": ["u0008"], "status": "ok",
 "state_version_before": 1, "state_version_after": 1, "logical_ts": 3,
 "provider": null, "why": "check new interpretation against committed one", "note": "verdict=conflict"}
```

- **`why` 字段由场景/程序填写**（自由文本），这是回答"这个行为究竟是哪个算子导致的"的入口。
- **canonicalization**：键排序 + 稳定序列化 → 求 **trace hash**，作为复现性判据（§8）。
- **Replay 元数据（v1 用不到，也要留格子）**：`params`（算子参数）· `provider`（用的是哪个确定性实现）·
  `comparator`（TEST 的比较器名）· 场景级 `seed`（v1 恒为常量）。**v1 没有 model metadata、没有外部依赖**
  ——这两个格子在 v1 的 trace 里**显式写 `null` / `none`**，而不是省略：将来接模型时是**填格子**，不是改格式。
- **Replay 的两件事必须分开**：① **确定性校验**（同输入 + 同初始 State + 同程序 → 同 trace hash）→ **v1 支持**；
  ② **从 trace 重放执行**（拿一条已记录的 trace 重新跑出同样结果）→ **v1 不做**，登记在 §9 延后清单。
- **不做**：不接 OpenTelemetry、不做面板、不做指标聚合系统（方法规范规则 9：不造第二套工具）。
- `trace.jsonl` 与末态 `state.json` 一起落 `runs/<exp-id>/`，**提交进 git** 作为 E0/E1 证据。

---

## 7. Experiments（三个最小实验）

统一场景（沿用 `operator-space.md` §11.1 的叙事，便于两份文档互相印证）：
**"玩家偷走东西 → 玩家离开 → 很久以后再次出现"**。

### 7.0 三个实验的共同设计（对照组 · 可数指标 · 结论条件）

> **本节为 2026-09-25 补强新增。** 原稿只验证"能不能表达"，缺三样：**没有对照组**（无法回答"非这样分解不可吗"）、
> **判据是定性的**（"读 trace 觉得没问题"）、**Exp3 的结论不可归因**（成功是场景干的活，失败说不清是算子空间还是编码）。
> 三样都在这里补齐；§7.1–§7.3 只写各自特有的部分。

#### (a) 每个实验跑两次：算子程序 vs 不透明大步

| 运行 | 是什么 | 用来回答 |
|---|---|---|
| **`prog`** | 我们声明的算子程序（2–5 步，有中间产物、有 trace） | 这套算子空间**能不能**表达 |
| **`mono`** | **同等输入、同等输出，但压成一步**（一个不透明的整体动作：不产出中间产物、不做算子分解） | 分解**是否必要**——即"能不能回答是哪一步造成的改变" |

**判据**：若两种运行**终态相同**，则分解的全部价值都体现在**可归因性**上——`prog` 能指出是哪一步改了
State / focus，`mono` 指不出来。**若 `prog` 也指不出来，则分解在本任务上是装饰**——§12.1 的头号风险
（"分解是虚假的"）从此有了探测器，不再靠眼看。

**纪律（否则对照不公平）**：`mono` 是**对照**，不是失败路径，也不是"偷懒版"；它必须由**同一个人、
在同一时间、用同等严格的程度**写成"不做分解的等价实现"。

#### (b) 三个可数量（每次运行都记，落 `runs/<exp-id>/metrics.json`）

| 指标 | 定义 | 为什么是它 |
|---|---|---|
| `attributable_steps` | trace 中**能唯一归因**到某个算子、且该步改变了 State 或 focus 的步数 ÷ 总步数 | 分解价值的直接度量，也是 (a) 的判据来源 |
| `unmapped_steps` | 标"**都不是**"（无法对应任何候选算子）的步数 | 候选基缺口的第一手数据（对应 `operator-space.md` §11.2 E-OS1 的缺口感） |
| `reuse` | 本次用的 comparator / provider / 算子集，是否与其它实验**同名同实现** | 防"每个实验各发明一套"（§12.1 R4：场景替代算子） |

**不做**：不打分、不加权、不算"通过率"。三个数是**给人和论文看的原始计数**，不是 KPI。

#### (c) 结论条件

每个实验必须在**预注册里先写死**"什么结果算什么"（方法规范规则 1：先注册后实验）。
**Exp3 的条件最严**，因为它的失败最可能来自**编码太弱**，而不是**算子空间太弱**——见 §7.3。

### 7.1 Experiment 1 — Continuity

```text
I1（"玩家拿走了箱子里的东西"）
  → SELECT → TRANSFORM(normalize) → COMMIT      [Thread A]
  → 关闭 A
later Thread B
  → SELECT(state)                                [跨 Thread 取回]
```

- **Expected capability**：Thread B 能在**不重新摄入 I1** 的前提下取回 A 提交的内容；trace 显示
  A 里唯一的 State 写入者是 `COMMIT`。
- **Failure condition**：B 取不回；或必须重新喂 I1 才能取回；或 trace 显示有非 COMMIT 的写入。
- **What failure means**：持久边界不成立——此时问题**不在算子空间**，而在 State/Thread 语义（§3.2）。
- **Next design question**：State 需要"可见性/作用域"吗（谁能看见哪些 key），还是全局可见就够？

### 7.2 Experiment 2 — Reinterpretation

```text
I1 → TRANSFORM → COMMIT                              [v1 解释]
I2（"玩家回来了，把东西还了"）
  → SELECT(旧 State 条目) → RELATE(I2 ↔ v1) → TRANSFORM(reinterpret) → TEST → COMMIT   [v2]
```

- **Expected capability**：终态同时存在 v1 与 v2，且 v2 ≠ v1；trace 能指出**是 RELATE/TEST 造成的改变**，
  而不是 TRANSFORM 一个人干完的。
- **Failure condition**：① v2 直接覆盖 v1（丢失历史）；② 改变完全由 TRANSFORM 产生，RELATE/TEST 是装饰
  （"算子分解只是装饰"）；③ 无法把 v2 归因到具体某次算子调用。
- **What failure means**：① → State 的 mutation model 错了（应 append-only，见 §3.3）；
  ② → **五个 primitive 的分解在本任务上是虚假的**，应记 failure 并重估候选基；
  ③ → trace 信息不足，必须先补 trace 再谈结论。
- **Next design question**：重新解释应由谁触发——程序写死，还是 Operator Selection（D11）？

### 7.3 Experiment 3 — Contradiction

```text
I1 = X（"玩家拿走了东西" 的结构化形式）
I3 = ¬X（"玩家没有拿走东西"）
  → SELECT(两条) → RELATE(negates) → TEST(negation) → TRANSFORM(保留冲突) → COMMIT
```

- **Expected capability**：终态**保留双方 + 冲突标记**，`verdict=conflict`；**不静默选边**。
- **Failure condition**：终态只剩一条合并后的说法（即"只会 summarization"）；或 TEST 给不出 conflict；
  或必须靠场景里预置的答案才能判定。
- **What failure means**：算子空间**无法表达冲突**——这是本计划最容易出现的真发现，
  直接回答 `operator-space.md` §11 的核心疑问，并应写成 failure 记录（F 类）+ 更新 D10。
- **Next design question**：冲突是**状态**（两条并存）还是**算子**（需要一个 join/resolve 算子）？
- **声明的限制（必须写进场景 README）**：v1 的 negation 判定依赖场景**显式声明** `negates` 边 +
  结构化 payload；**这不是自然语言矛盾检测**。若实验结果被解读为"能处理任意矛盾"，即为误读。
- **结论条件（预注册时必须先写死；不写就只能算 exploratory / E0）**：
  1. **同一结论必须在两份独立编码下成立**——编码一：场景显式声明 `negates` 边；编码二：comparator
     **不看 `negates`**，靠结构化 payload 自行比对。**两份编码结论不一致 → 本次结果为"不确定"**，两边都不得采信；
  2. 允许写出的最强结论是：**"在声明式编码下，算子空间能 / 不能保留冲突"**——**不得**升级为"能处理任意矛盾"；
  3. 只有 `unmapped_steps > 0` 且**集中在冲突处理步骤上**，才算"缺一个 primitive"的可接受证据；
     **仅"终态只剩一条"不算证据**——那可能只是编码太弱。

---

## 8. Test Strategy

| 层 | 测什么 | 判据 |
|---|---|---|
| **单元** | 每个算子的纯函数行为 | SELECT 不产生 unit；RELATE/TEST/TRANSFORM 产出 `derived` 且 `refs` 可对回；COMMIT 之外无 State 写入；缺参数/未知 provider → 硬失败 |
| **边界守卫** | import 面 | 算子模块不得 import State 写入；代码不得 import `macha.*`（`src/macha`）与任何 Kotlin/Gradle 产物；不得引入第三方依赖 |
| **集成** | 三个实验各一条 | 断言 canonical trace 的**关键子序列** + 末态 `state.json` 的**声明式断言**（不比对整份文件，避免脆断言） |
| **对照运行** | 每个实验的 `prog` 与 `mono` 两次运行（§7.0a） | 两次终态一致；`attributable_steps` 能从 trace 算出；`mono` 的 trace 里**不存在**中间归因 |
| **可数指标** | `attributable_steps` / `unmapped_steps` / `reuse`（§7.0b） | 三个数能由 trace 与场景元数据**机械算出**（不靠人读），落 `metrics.json` |
| **Replay / 确定性**（**排第二**） | 同输入 + 同初始 State + 同程序 → 同结果 | 两次运行的 `trace hash` 相同；固定 `PYTHONHASHSEED`；逻辑时钟非墙钟；迭代一律排序。**这是赶工时第一个可以砍的项——砍掉不影响三个实验的结论**（见 §12.2） |
| **手工验收（E0）** | 一条命令产出证据 | `python research/experiments/operator_sandbox/run_experiment.py exp1` → `runs/exp1/{trace.jsonl,state.json}` |
| **不做** | CI | 仓内无 `.github/`；本轮**不新建**（预算上限）。命令写进 sandbox README，人工执行 |

**可重跑命令（写进 sandbox README）**：

```text
python -m pytest research/experiments/operator_sandbox -q
python research/experiments/operator_sandbox/run_experiment.py exp1|exp2|exp3
```

---

## 9. Deferred Scope（明确不做）

用户给定清单照单全收：**LLM Agent · Planner · Orchestrator · Automatic Operator Selection · Social Graph ·
Spatial Grid · Multi-Agent Runtime · Distributed Execution · ECS · Pub/Sub · Vector Database ·
Complex Memory Hierarchy · Operator Learning · Operator Discovery**。

**本计划另外补上（诚实补充，都有仓内依据）**：

- 不做 **DSL / grammar / 配置文件格式**（§5）；
- 不做**从 trace 重放执行**（v1 只做确定性校验，见 §6）；
- 不做**分支与循环**（§5）；
- 不做**重要性/置信度打分**（§3.1：那属于"什么值得记住"，而 COMMIT 不决定它）；
- 不做 **CI / 打包 / 发布**（§1.1 无 CI；`pyproject.toml` 不动）；
- 不碰 **`src/macha/**`**（V1）与 **`layers/**`**（V3）；
- 不改**根 `tests/` 与 `pyproject.toml` 的 testpaths**；
- 不建 **`tools/`** 树（§2.2）；
- 不把 **trace 升级成 observability 系统**（§6）。

**文件预算上限（对齐方法规范规则 10）**：沙盒第一阶段 ≤ **10 个 Python 文件 + 1 个 README + 3 份 runs 证据**。
超出必须先删一个。

---

## 10. Implementation Order

| Step | 内容 | 产出 / 判据 | 预估 |
|---|---|---|---|
| **0** | 评审本计划；**按 U8 二选一走哪条腿**（见 §10.1） | 研究腿 → `research/questions/Q-02-*.md`（`prereg:` 有 commit hash）；工程腿 → 无 Question，结果只到 E0 | 0.5 天 |
| **1** | `model.py` + `workspace.py` + `state.py` + `trace.py`（spine）+ 单元测试 | 能 open/seed/close 一个空 Thread；State append + version；trace 可读 | 0.5–1 天 |
| **2** | Operator 协议 + registry + 线性 runner + trace 接线 + 写权限守卫测试 | 一个假算子能跑通并被记录 | 0.5 天 |
| **3** | `SELECT` / `TRANSFORM`（provider seam）/ `COMMIT` + **Exp1** 场景 | `runs/exp1/` 落地；Exp1 的四个判据可判 | 1 天 |
| **4** | `RELATE` / `TEST` + **Exp2** 场景 | `runs/exp2/`；v2≠v1 且历史保留 | 1 天 |
| **5** | **Exp3** 场景（含 `negates` 声明） | `runs/exp3/`；`verdict=conflict` 且双方保留 | 0.5 天 |
| **6** | replay/determinism 测试 + 证据归档 + sandbox README | 两次运行 trace hash 相同；README 含重跑命令 | 0.5 天 |
| **7** | 复盘写回：`operator-space.md` §3/§11.2（哪些算子被用到、哪些是装饰）、`open-decisions.md`（D8/D9/D10/D11 的答案或更新）、必要时 `research/failures/` | 文档更新 diff | 0.5 天 |
| **8** | 决策点：**继续 / 停止**（若 Exp3 失败且诊断为"算子空间不足"，按路径惯例**如实记录并停止**，不缝补） | 决策记录或失败记录 | — |

**合计：约 6–7 人日**（原为 5–6；新增的 `mono` 对照组与 `metrics.json` 各占约半天），不含 Step 0 的评审。
全部可在不碰 Core/Layer 的前提下完成。

### 10.1 Step 0 的两条腿（U8 未定，但计划对两条腿都成立）

| | **研究腿（推荐）** | **工程腿** |
|---|---|---|
| 前提 | 三个实验要产生**可定级的证据**（E1；有 `mono` 对照后可能够到 E2） | 只想知道"这套东西能不能跑" |
| Step 0 产出 | `research/questions/Q-02-*.md`：机制 + ≥2 竞争假设 + 预测 + falsifier + `prereg:` commit hash | 无 Question；在 sandbox README 写明验收条件（三个实验各自的可观测判据）即可 |
| 结果能说什么 | "在某条件下观察到 X"（E1）；有对照后**可能够到 E2** | 只能说"能跑通"（E0）；**不得**写成研究结论，不得进 `papers/notes/` |
| 失败怎么办 | 按 F 类归档进 `research/failures/` | README 记一条备注即可 |
| 代价 | 多 0.5 天写预注册 | 省 0.5 天，但结论不可用 |

**推荐走研究腿**：`mono` 对照（§7.0a）已经把对照条件准备好了，多花半天把 E0 变成 E1/E2，
是这笔投入里性价比最高的一步。

### 10.2 预算与止损闸门（硬线，到点就停）

| 闸门 | 触发条件 | 动作 |
|---|---|---|
| **G1** | Step 3 超过 **2 天**仍未产出第一条真实 trace（`runs/exp1/trace.jsonl`） | **停止并报告卡在哪一步**；**不得**用"再加一个机制"绕过 |
| **G2** | 任一 Step 的实际耗时达到预估的 **2 倍** | 停止、重估范围：优先砍 §12.2 标为"排第二"的项，**不要**砍实验 |
| **G3** | 累计达到预估上限（**7 人日**）而 Step 5 未完成 | 停止；只交付"已完成到哪一步 + 原始 trace"，**不交付半成品结论** |
| **G4** | 产生改 `src/macha/**` 或 `layers/**` 的冲动 | 记为**协议/Core 问题**写进 `open-decisions.md`，**本轮不做** |

**为什么要有 G1–G3**：这条路径的历史症状是"连续数轮都在定义概念，没有任何一项被现实检验"
（`README.md` §6）。止损线的作用是**逼出第一条 trace**，而不是保护预算。

---

## 11. Open Questions（U = 需要实验回答；D = 需要人决定）

| # | 问题 | 归属 | 谁来答 |
|---|---|---|---|
| **U1** | SELECT 真的不产生信息吗？还是"选择依据"本身就该是一条新信息？ | 实验（Exp1 trace） | 实验 |
| **U2** | RELATE 会被二元的 TEST 吸收吗（即 `RELATE` 冗余）？ | 实验（Exp2/Exp3） | 实验 → D10 |
| **U3** | COMMIT 与"回流"是不是一回事（D9）？本沙盒允许**处理中途 COMMIT**，IC 只允许**关闭时回流** —— 哪个语义对？ | 实验（Exp1 是否需要中途提交） | 用户 + 实验 |
| **U4** | State 需要版本/取代语义，还是 append-only 就够？ | 实验（Exp2 的 v1/v2 并存） | 实验 |
| **U5** | "什么值得记住"住在哪一层？（COMMIT 不决定，那谁决定？） | 设计 | **用户** |
| **U6** | Thread 是 IC 的 `Ive Chunk`，还是比它更低一层的单位？（命名/层级问题，影响未来与 IC 对接） | 设计 | 用户 |
| **U7** | `uncertainty` 是 TEST 的输出，还是 `Unit` 上的一等字段？ | 实验 | 实验 |
| **U8** | 三个实验算**研究**（需 Q-02、结果按 E1/E2 定级）还是**工程验收**（E0，只证明"能跑"）？ | 方法 | **用户**（决定是否写 Q-02） |
| **U9** | 若线性程序不足以表达 Exp2/Exp3，说明"分支"是必需能力，还是说明**算子划分错了**？ | 实验 | 实验 |

---

## 12. Design Risks（+ 过度设计审查）

### 12.1 最可能出错的六处

| # | 风险 | 早期信号 | 缓解 |
|---|---|---|---|
| **R1** | **`Unit` 膨胀**：悄悄加回 `importance`/情绪/置信度 | 字段超过 §3.1 的 6 个 | 字段上限；新增字段必须删一个 |
| **R2** | **trace 变成 observability 工程** | 出现 schema 版本、采样、导出器、面板 | §6 字段固定；只写 JSONL |
| **R3** | **边界漂移**：算子概念漏进 Layer（Kotlin）或 `src/macha` | 出现改 `layers/**` 或 `src/macha/**` 的 PR | §2.1 排除 + §8 边界守卫测试 |
| **R4** | **场景替代算子**：TEST 直接调用场景预置答案，于是"实验通过"只证明场景写得好 | comparator 里出现 `if scenario == "exp3"` | comparator 必须**命名、通用、可复用**；trace 记录 comparator 名；同一条 comparator 跨实验复用 |
| **R5** | **五个一起实现**：为凑齐而起 RELATE/TEST，实验里从不出现 | Step 4 前就想写 RELATE | §10 顺序；Exp1 只用三个 |
| **R6** | **State 变 Memory**：加上检索打分、遗忘、摘要 → COMMIT 事实上在"决定什么值得记住" | 出现 scoring 参数 | §4.6 明确禁止；U5 留给用户 |

### 12.2 过度设计审查（逐条自查）

| 问题 | 自查结论 |
|---|---|
| 删掉一半 abstraction，实验还能做吗？ | **能**。删掉 `Program`（改成函数里手写调用）与 `provider seam`（改成模块内固定函数），三个实验照跑。保留它们只因为**trace 需要统一入口**——这是有依据的保留，不是为未来设计。 |
| 有没有为 Multi-Agent 提前设计？ | **没有**。全仓无 agent 概念进沙盒；`thread_id` 只是 trace 分组用。 |
| 有没有为 LLM 提前设计？ | **没有**。provider seam 是"确定性纯函数"接缝，不是模型接缝；也不预留 prompt/上下文窗口字段。 |
| 有没有把 Method / Operator / State 混在一起？ | **没有**。Method 只在 §7 的实验叙事里出现，且 `operator-space.md` §8 已声明"Method=Operator Program"是**假设**；沙盒不实现任何 Method。 |
| 有没有引入没有实验依据的字段？ | `logical_ts` 与 `why` 是为 trace/replay 服务；`refs` 为"派生物可对回"服务；其余字段都在三个实验里被实际使用。**没有 embedding / confidence / importance。** |
| 有没有一项工程工作其实属于未来阶段？ | 有：`run_experiment.py` 的 CLI 化与 `runs/` 归档严格说属于 Step 6；但它把 E0 证据变成可复跑的东西，值得保留。**CI、打包、SDK 化**全部推迟（§9）。 |
| **五个 primitive 是否真的都需要第一版？** | **不是五个都需要，答案是三加二**：Exp1 只用 `SELECT/TRANSFORM/COMMIT`；`RELATE`/`TEST` 到 Exp2/Exp3 才出现。因此第一版实现顺序是 **3 → 5**（§10 Step 3/4），并且 **`RELATE` 的存在性本身是风险**（U2）：若 Exp2/Exp3 能用二元 `TEST` + `TRANSFORM` 表达，`RELATE` 应当被**删除**，而不是保留以凑五个。 |
| **有没有排错主次的工程项？** | **有：Replay 的确定性校验属于"排第二"的事。** 它不是三个实验得出结论的**必要条件**——砍掉它，三个实验照样能判（§8 已标注）。它值得做（复现性纪律），但**不得**与"临时/持久边界""可归因性"并列；赶工时第一个砍它。 |

---

## 13. Expected Effects（执行完之后会得到什么）

> 这一节的作用是**先写清收益与天花板**，避免把一次沙盒实验读成"Macha 会思考了"。

### 13.1 磁盘上多出什么

| 产物 | 内容 |
|---|---|
| `research/experiments/operator_sandbox/` | 约 10 个 Python 文件（纯标准库）+ README（含重跑命令） |
| 该目录 `runs/exp1\|exp2\|exp3/` | 每个实验**两份**运行（`prog` / `mono`）：各一份 `trace.jsonl` + `state.json` + `metrics.json`，**提交进 git**：可逐行审查的执行轨迹 |
| `research/questions/Q-02-*.md` | 带预注册（机制 + 预测 + falsifier）的问题文件 |
| 文档更新 | `operator-space.md` §3/§11.2 复盘 · `open-decisions.md`（D8–D11 的答案或更新）· 必要时 `research/failures/` |

### 13.2 哪些问题从"讨论"变成"有数据"

| 计划要检验的问题 | 执行后拿到的东西 |
|---|---|
| 五个 primitive 是否足以表达基础认知过程 | 三条 trace：每步都能对应某个算子，或明确标"**都不是**"——E-OS1 缺口感的第一份真实数据 |
| 不同算子如何组合 | 三个实验各自的实际算子序列（以及"只用三个够不够"） |
| **分解是否必要**（"非这样分解不可吗"） | `prog` vs `mono` 对照（§7.0a）+ `attributable_steps`：**分解的价值 = 可归因性**，不再靠眼看 |
| 算子的输入/输出/状态语义 | 一次可复现的执行：同信息、同算子、不同 `State` → 输出是否不同 |
| 哪些属于 Operator、哪些属于 State/Memory | 边界守卫测试 + `output_refs`：**只有 COMMIT 产生 State 变化**，其余全是 Thread-local |
| 是否存在无法表达的案例 | Exp3 的结果：冲突被**保留**，还是塌缩成"只会 summarization" |
| 顺带 | **D8**（作用对象是否统一）· **D9**（COMMIT 是否就是"回流"——沙盒允许中途 COMMIT，IC 只允许关闭时回流，Exp1/Exp2 会暴露哪种语义是必须的）· **D10**（RELATE 是否冗余）· **D11**（谁触发算子）的部分证据 |

### 13.3 天花板（必须说清，否则一定会被误读）

- **证据等级只到 E0/E1**：单案例观察 + 有 provenance + 可重跑命令。它**只能**支持"可做""在某条件下观察到 X"，
  **永远不能**支持"算子空间完备"。要 E2 需要对照实验，要 E3 需要第二实现或跨环境。
- **不产生任何宿主可见的能力**：NPC 仍然不会说话、不会记事、不会自主行动。这是**实验台，不是功能**。
- **不解冻 SepMay 路径**（解冻条件三条未变）· **不碰 Core/Layer** · **不阻塞 MC 主线**。
- 成本约 **6–7 人日**（含 `mono` 对照与 `metrics.json`）；不新建顶层目录、不加依赖、不建 CI。

### 13.4 三种可能结局，以及各自意味着什么

| 结局 | 含义 | 后续动作 |
|---|---|---|
| **A. Exp1/Exp2 通过，且 `RELATE` 被判冗余** | 最小可用集是 `SELECT/TRANSFORM/TEST/COMMIT` | **删掉 RELATE**（这是发现，不是失败）；更新 D10 |
| **B. Exp3 表达不出冲突** | "五个 primitive 不足"的第一份证据——**本计划最有价值的可能结果** | 记 `research/failures/`，更新 D10；讨论"冲突是新 primitive 还是 State 语义" |
| **C. 改变全由 TRANSFORM 完成，RELATE/TEST 是装饰** | **算子分解在本任务上是虚假的** | §7.0a 的 `mono` 对照 + `attributable_steps` 就是它的**探测器**：若 `prog` 指不出"是哪一步造成的改变"，它与 `mono` 没有区别 → 重估整个候选基（比"跑通"值钱），不要用"再调一版"掩盖它 |

### 13.5 长期效果与分岔

把 `architecture.md` §1.5 里那个 `Written by` / `Read by` 全是 `—` 的算子空格子，变成
**一个能被反驳、能被扩展、能被第三方复现的研究对象**——并给出两条分岔：

```text
活过两轮实验  → 以决策记录提升为 Macha Core 运算域的候选实现（Phase 3）
被现实否掉    → 按路径惯例整条归档，不缝补（README §9 的反对意见）
```

---

## 14. Recommended First Commit（如果只允许一个最小 commit）

> **实现 Step 1 + Step 2 + Step 3 的走通骨架**：`model.py` / `workspace.py` / `state.py` / `trace.py` /
> `operators.py`（**只含 `SELECT` / `TRANSFORM` / `COMMIT`**）/ `program.py` / `scenarios.py`（**只含 Exp1**）+
> 三条测试（单算子、边界守卫、Exp1 集成）+ **`runs/exp1/` 的两份真实运行**（`prog` 与对照 `mono`，
> 各带 `trace.jsonl` + `state.json` + `metrics.json`，提交进 git）。

**为什么是它，而不是更小的"只写数据模型"**：

1. **数据模型单独提交产生不了证据。** 本阶段唯一的证据来源是 trace；没有一次真实执行的 trace，
   `Unit`/`Workspace`/`State` 的字段全部是**未经验证的假设**，评审只能靠讨论——而讨论正是这条路径卡住的原因
   （`operator-space.md` §1.2：算子至今只有名字没有内容）。
2. **它一次性暴露两个最难回填的决定**：**临时/持久边界**（谁有写入权）与 **id/版本语义**。
   这两样错了，上面每个算子都要重写；这两样对了，`RELATE`/`TEST` 只是各加一个纯函数。
3. **它同时就是第一个实验**（Exp1 = Continuity），而且带上 `mono` 对照后**第一次能回答"分解是否必要"**
   ——不只是"能编译"。
4. **它是可评审的**：~7 个文件、三个纯函数算子、两条 trace，一个人一次能看完。

**明确不在首 commit 里**：`RELATE`、`TEST`、Exp2、Exp3、replay 测试套件（§12.2 标为"排第二"）、任何 CLI 美化、
任何 `src/macha` 或 `layers` 改动、任何新依赖。

---

## 附：本计划**没有**做的事（避免误读）

- 没有创建任何代码、目录或 Question 文件（本轮 PLAN ONLY）；
- 没有修改 `src/macha/**`、`layers/**`、`tests/**`、`pyproject.toml`、`docs/architecture.md`；
- 没有替 `operator-space.md` 裁决 D8/D9/D10/D11——它只把这些问题变成**可执行的实验**；
- 没有声称五个 primitive 完备（§12.2 明确：`RELATE` 可能该被删掉）。
