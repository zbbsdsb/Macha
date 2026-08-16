# NPC 可信度需求文档（设计理论 → 技术指标）

> **类别归属**：`information_needs.md` 第 4 类「游戏设计理论：NPC 可信度与玩法」。
> **文档性质**：研究子任务交付物（不是 Demo，而是为 Macha「标准骨架」服务的设计理论翻译层）。
> **配套文档**：`direction.md`（最小可验证方向：长期记忆 + 角色一致性）、`positioning.md`（四篇论文定位）、`architecture.md`（目标架构：Perception / Memory / Reasoning / Action 四层）、`evaluation_benchmarks.md`（可信度/一致性评估维度表 F1–F13 / E9–E13）。
> **核心命题**：Macha 服务的是「设计可信 NPC」，不是「更强的聊天机器人」。本文档把设计语言（MDA、互动叙事、可信度理论、AI 原生设计）翻译为 Macha 必须可度量、可落地的技术指标，使 `architecture.md` 的模块与 `evaluation_benchmarks.md` 的维度形成闭环。

---

## 0. 文档使用方法

- **第 1 节**是给工程与产品团队的主交付：**设计关切 → 技术要求对照表**。每一行说明「设计想达成什么」以及「Macha 必须做到什么、用什么指标度量」。
- **第 2 节**把设计理论概念（MDA / 互动叙事 / 可信度 / AI 原生）映射到 Macha 的模块与指标，便于在架构与评估之间建立可追溯链路。
- **第 3–5 节**是三个专项分析：玩家对 NPC 记忆的期待、开放世界 vs 叙事游戏的行为差异、AI 原生游戏的「语义裁决 / 多智能体模拟」案例拆解。
- **第 6 节**按 `information_needs.md` 约定的固定格式登记关键来源。
- **第 7 节**给出 Macha 落地的设计原则与待办。

> 说明：所有 URL 均来自本次研究通过 WebSearch / WebFetch 实际获取。其中 MDA 原始 PDF（northwestern 域名）经 WebFetch 确认可访问（重定向至 `users.cs.northwestern.edu/~hunicke/MDA.pdf`）；其余主链接均为搜索返回的可用页面。个别经典论文（Bates 1994、Loyall & Bates 1997）以摘要页/镜像页登记，正式引用前建议补全原始出处。

---

## 1. 设计关切 → 技术要求对照表（核心交付）

> 每一行 = 一个设计关切。右列给出 Macha 的**技术需求**与**可度量指标**（尽量复用 `evaluation_benchmarks.md` 的 F/E 维度）。

| # | 设计关切 | 设计意图（设计师想达成什么） | Macha 技术需求 | 可度量指标（关联评估维度） |
|---|---|---|---|---|
| C1 | **可信度 / Believability** | 玩家主观相信「这是一个真实存在、有内在生命的角色」，愿意为之投入情感 | NPC 必须呈现「生命的假象」：一致性、情绪、觉知、社会性、可理解性并存的稳定表现 | Paiva 九维李克特量表（行为一致性 / 经验变化 / 觉知 / 行为可理解性 / 人格 / 情绪表达 / 社会性 / 视觉冲击 / 可预测性）→ **F3 / F7** |
| C2 | **角色一致性 / Role Fidelity** | NPC 在长程交互中保持人格、说话风格、价值观、禁忌稳定，不「原地变脸」 | 人格/价值观/禁忌必须作为不可变约束注入 Reasoning 层；对话与行动均受 Character 层校验 | RoleBench 三指标 CUS / RAW / SPE；DNLI 蕴含一致性；对抗性人设偏移探测 → **F1** |
| C3 | **记忆期望 / Memory Expectations** | 玩家期待 NPC「记得关键的事、淡忘琐碎的事」，记忆服务于关系与叙事而非信息堆砌 | 实现「有目的的记忆」：高价值事件（背叛/忠诚/承诺/共担风险）优先留存，低价值交互可衰减；记忆须驱动后续态度与行为 | 记忆命中率、记忆衰减合理性、跨会话态度一致性、声誉/流言传播正确性 → **F2 / F4** |
| C4 | **能动性 / Agency** | NPC 有自己的目标、恐惧、社会关系与行为阈值，能主动行动而非仅被动应答 | Reasoning 层须含「目标 + 规划 + 阈值触发」；NPC 可在无玩家输入时自行决策（见 C9 世界真实感） | 自主目标达成率、目标驱动行为占比、规划成功率（AgentBench/SmartPlay 思路）→ **F5** |
| C5 | **可预测性 / Predictability** | 行为可被玩家理解和预期（不过度随机、也不完全死板），这是可玩性与信任的基础 | 行为轨迹熵需落在「有趣但不混乱」区间；决策可被回放与解释 | 行为轨迹熵 / 可解释性打分、Paiva predictability 量表 → **F7 / E12** |
| C6 | **情感与社会性 / Emotion & Sociality** | NPC 有情绪、会共情、与他人有关系网，情绪变化符合性格与情境 | Memory/Reasoning 维护情绪状态与关系图；情绪与关系驱动对话与行动选择 | 情绪一致性、关系演化合理性、多人社会反应一致性 → **F3 / F1** |
| C7 | **涌现叙事 / Emergent Narrative** | 故事由交互「长出来」而非预写剧本；玩家感到自己是自己故事的主角 | 以结构化世界状态 + 角色动机驱动生成，而非纯自由文本续写；提供「叙事引力」约束 | 叙事连贯性、玩家能动性评分（Player Agency）、长程不崩坏率 → 见第 5 节 |
| C8 | **受控自主性 / Bounded Autonomy** | NPC 在「角色/世界规则」边界内自由，越界时系统否决或引导，而非无限生成 | Action 层输出须受世界状态、角色动机、叙事对齐过滤；定义「机械不变量」（目标/规则/状态/反馈/节奏/能动性） | 越界率、叙事对齐率、风格合规率 → **F1 / F4** |
| C9 | **世界真实感 / Lives Beyond You** | 玩家不在场时 NPC 仍有日常、关系与生命，世界不围绕玩家冻结 | 多 NPC 调度与共享世界时钟；NPC 间预置关系网与自主日程；记忆与事件跨 NPC 传播 | 自主日程覆盖率、NPC 间关系一致性、玩家缺席期间世界事件正确性 → **F5 / F2** |
| C10 | **跨会话连续性 / Session Continuity** | 数天/数月后回归，NPC 仍记得关系、承诺与后果 | 长期记忆外挂（非仅上下文窗口）；世界状态存于模型之外（server/外部状态） | 跨会话记忆召回率、知识更新正确率（LongMemEval KU）→ **F2 / F4** |
| C11 | **反幻觉 / 抗角色漂移** | NPC 不编造未发生的事、不前后矛盾、不混淆新旧事实 | Memory 与 Character 层作为「事实与人格锚」，行动前做一致性校验 | LoCoMo 对抗集、LongMemEval Abstention、记忆一致性压力测试 → **F4** |

---

## 2. 设计理论概念 → Macha 模块 / 指标映射

| 来源概念 | 核心主张 | 映射到 Macha 模块 | 映射到 Macha 指标 |
|---|---|---|---|
| **MDA（Hunicke, LeBlanc, Zubek 2004）** | 游戏 = Mechanics（规则/数据/算法）→ Dynamics（运行期涌现行为）→ Aesthetics（玩家情感响应）；设计师正向建、玩家逆向体验；「游戏更像人造物而非媒体，内容即其行为」 | **Mechanics**→ Macha 的接口契约（`Observation`/`MemoryItem`/`BaseAgent`）与 `architecture.md` 的算法层；**Dynamics**→ Perception→Memory→Reasoning→Action 在玩家输入下的涌现；**Aesthetics**→ 玩家主观可信度（F3/F7） | 用「机械不变量」保证 Dynamics 朝目标 Aesthetics 收敛；以玩家调研（TrueSkill 配对）度量 Aesthetics → **F3 / F7 / E13** |
| **互动叙事 Interactive Drama（Chris Crawford）** | 真正的交互 = 多个活跃主体间「倾听—思考—发言」的循环；只有「互动叙事」而非「互动故事」；系统须能基于玩家反馈即时生成故事，并维持结构完整 | Macha 的 Reasoning 即「故事引擎内核」：维护 storyworld（角色、关系、动机、规则），按玩家行动即时生成下一步；对话是 Verbs 的一种 | 叙事连贯性、玩家能动性（是否真有「戏剧性且多样」的选择）、结构完整度 → 见 C7 |
| **可信度 Believability（Bates 1994; Loyall & Bates 1997; Paiva/Gomes 2013）** | 可信 = 提供「生命的假象」以让观众悬置怀疑；情绪须被恰当时机表达；语言与行动须由同一人格/情绪驱动；九维度量（行为一致性/经验变化/觉知/可理解性/人格/视觉/可预测性/社会性/情绪表达） | **Character 层**（人格、情绪、关系）贯穿 Perception→Memory→Reasoning→Action；情绪状态机在 Reasoning 内；视觉/动作由 Action 层呈现 | Paiva 九维量表 + Game Agent Matrix → **F1 / F3 / F7** |
| **AI-based Game Design（Eladhari et al. 2011; Treanor et al. 2015）** | AI 应是游戏的「共同作者」而非烟雾弹（smoke-and-mirrors）；提出设计模式：AI is Visualized、AI as Role-model、Mixed-Initiative 等；Mechanics/Dynamics/Aesthetics 须深度绑定 AI 系统 | Macha 提供的不是「更聪明的对话」，而是可被设计者用来构造玩法的「AI 机制原语」（记忆、反思、规划、社会推理）；支持 mixed-initiative（玩家+NPC 共创作） | 设计者可组合性、模式复用度、是否产生「expressive AI」（玩家需读懂 NPC 意图）→ **F5 / C7** |
| **The Sims 信息素模型（Will Wright）** | 角色是「环境分布智能」：每个物体广播「需求气味」（食物/能量/社交…），Sim 循气味行动；**刻意保留「不完美自主性」**——早期版本太聪明反而让玩家无需操作，于是加入随机与「隐藏定时炸弹」以维持玩法张力 | Macha 的 Perception 层把世界对象标注为「可被欲望/目标吸附的信号源」；Autonomy 参数须可调（太聪明=玩家无关，太笨=无聊）；行为阈值引入可控随机 | 自治度调参曲线、玩家介入必要性、行为多样性 → **C4 / C5 / F5** |
| **AI-Native 设计本体论（arXiv:2607.00527）** | 反事实标准：移除运行时生成式 AI，核心循环是否崩塌？G/N 双轴分类；核心难题是「把语义开放性组织成稳定玩法」，依赖机械不变量 | Macha 的 Action 层承担 **N 轴机制**：语义裁决（Semantic Adjudication）、多智能体模拟（Multi-Agent Simulation）、生成式叙事（Generative Narrative）等；所有生成受「目标/规则/状态/反馈/节奏/能动性」约束 | 移除生成式组件后核心循环是否仍可玩（反事实测试）、机械不变量覆盖率 → 见第 5 节 |
| **Generative Agents / Smallville（arXiv:2304.03442）** | 记忆流 + 反思 + 规划产生可信社会行为；记忆含时间衰减、重要性加权、语义关联；反思在重要性阈值触发 | 直接对应 Macha 的 Memory（衰减/加权/检索）+ Reasoning（反思与规划）三层件 | LoCoMo / LongMemEval / MemoryArena → **F2 / F4 / F5** |

---

## 3. 专项分析 A：玩家对 NPC 记忆的期待（"NPC 到底该记住什么"）

设计语言常把「记忆」当成数据库问题，但玩家感知的是**关系与叙事权重**。综合产业与社区研究（见第 6 节来源），可提炼为以下需求：

### 3.1 有目的的记忆（Purpose-Driven Memory），而非全量记忆

- **高价值记忆**（应优先留存）：背叛或忠诚行为、阵营/道德取向漂移、未履行的承诺、共担风险或共享成功的关键时刻、影响关系的重大抉择。
- **低价值记忆**（应衰减或忽略）：每一次琐碎对话选项、重复的微小动作——记住太多反而制造噪声与叙事不一致。
- **设计含义**：Macha 的 Memory 层必须做**重要性加权 + 衰减 + 语义检索**，而非把对话流水账全塞进上下文。直接对应 `evaluation_benchmarks.md` 的 F2（长期记忆稳定性）与 F4（反幻觉）。

### 3.2 四类记忆系统的设计谱系（供 Macha 选型参考）

| 类型 | 机制 | 能记住什么 | 局限 | 对 Macha 的启示 |
|---|---|---|---|---|
| Flag / Reputation（旗帜/声誉） | 布尔旗或数值声誉，NPC 交互时查询 | 某事件是否发生（`saved_apothecary=true`；`reputation:merchant_guild=-12`） | 无语义、无细节 | 作为 Macha Memory 的「硬事实层」，便宜可靠 |
| Simulation（模拟） | 带情绪权重的事件日志 + 衰减 | 创伤/侮辱等情绪化记忆，丰富但不可对话 | NPC 无法「聊」记忆 | Macha 可把情绪权重作为检索排序信号 |
| Nemesis（宿敌） | 跟踪遭遇并重塑 NPC 身份 | 战斗关系（谁杀了我、我怕火） | 范围窄、常专利封锁 | 可作为 Macha「关系+恐惧」子模块的范例 |
| AI / Vector（向量） | 对话内容向量化、语义相似检索 | 你说过的原话与意图，而非仅事件 | 依赖 LLM、有延迟/成本、概率性召回 | **Macha 的主记忆范式**（RAG + 向量），但须叠加 Flag 层兜底 |

### 3.3 记忆的社会传播：声誉与流言网络

- 玩家不期待「每个 NPC 全知」，而期待**谁知道什么**不同：卫兵知罪行、酒馆老板知八卦、祭司知誓言。这驱动探索（玩家去寻找「记得那件事的人」）。
- **流言/见证链（witness & gossip）**让信息在传播中变异，引入不确定性与社会动态——比全知 NPC 更可信。
- **设计含义**：Macha 的 Memory 应支持**基于角色的访问权限 + 传播规则**，而非全局共享黑板。

### 3.4 向玩家「展示记忆」的 UX

- 世界内线索（NPC 对话、通缉令、镇公所账本引用过往事迹）、玩家仪表盘（谁记得你、为何）、前置暗示（行动会有后果）——让记忆「公平且有意义」。

---

## 4. 专项分析 B：开放世界 vs 叙事游戏 NPC 行为差异

| 维度 | 开放世界（Open World） | 叙事/角色扮演（Narrative/RPG） | 对 Macha 的指示 |
|---|---|---|---|
| 主导美学 | Discovery / Sensation / Fellowship（MDA 八类） | Narrative / Expression / Fantasy | Macha 的 Character 层应允许按游戏类型切换「可信度侧重点」 |
| NPC 数量与密度 | 海量路人 NPC，需基础对话与涌现行为 | 少量关键 NPC，深度角色塑造 | 分层：路人用轻量 FSM/轮询，关键 NPC 用完整 Macha 认知栈 |
| 玩家行为可预测性 | 低（行为多样、期待涌现故事） | 较高（主线节点需稳固） | 开放世界更依赖 C9 世界真实感；叙事更依赖 C2 角色一致性 |
| 沉浸杀手 | 「木头人」感、无法对独特行为智能反应 | 角色偏离人设、长线剧情崩坏 | 两类都要求 F1/F4，但叙事侧阈值更严 |
| 推荐架构 | 「混合方案」：少量重要 NPC 给动态对话作亮点，其余用状态机 | GPT/LLM 深度扮演 + 主线框架（Fable 式）约束 | Macha 应支持「认知栈降级」（路人 NPC 不加载完整 Reasoning）以控成本（E10/E11） |
| 世界是否围绕玩家冻结 | 否——NPC 有独立日程、关系、生命（Stardew Valley 范式） | 部分——主线可等待，但世界仍应「有脉搏」 | C9 世界真实感对两类都成立，强度不同 |

> 关键洞察（来自 Stardew Valley 拆解与 GAEA 系统报道）：**「自主性的假象」**（illusion of autonomy）——日程是写死的，但因随天/天气/季节变化且暗示性格，玩家感到角色在「选择」。这正是 Macha 可在低成本下达到高可信度的工程技巧：用确定性调度制造「生命感」，用 LLM 制造「不可预测的深度」。

---

## 5. 专项分析 C：AI 原生游戏的「语义裁决」与「多智能体模拟」案例拆解

基于 `arXiv:2607.00527` 的 G/N 双轴分类，以下两类 N 轴机制是 Macha 作为「标准骨架」必须内置的玩法原语。

### 5.1 语义裁决（Semantic Adjudication）

> 定义：玩家以自然语言/开放动作输入，系统**即时解释其语义、改写游戏状态并裁决后果**，而非在预写分支里匹配。

**案例 1：Hidden Door（AI 地牢主 / DM）**
- 机制：人类作者手写「剧情节拍 + 世界观规则 + 桥段牌库」，ML/LLM 在每回合把玩家自然语言行动**裁决**为可执行的游戏状态变更（卡牌化世界状态），并有时掷骰决定成败。
- 关键设计：**有墙的自由**——玩家不能「写个无敌银弓秒杀全银河」（ChatGPT 会同意，Hidden Door 会否决并引导）。世界状态**存于引擎层而非对话上下文**，这是其记忆与连贯性领先（Memory & Continuity 4/5、Longevity 4/5）的根因。
- 对 Macha 的启示：Action 层必须有一个**裁决器（Adjudicator）**，把 LLM 的自由输出映射到受约束的世界状态；这正是 `architecture.md` 中 Action「结构化输出」与 C8 受控自主性的落地形态。

**案例 2：多智能体 Balderdash 的「评审 LLM」**
- 机制：集中式游戏引擎 + 多个 LLM 玩家 + 一个 **judge LLM 评估语义等价性**（定义是否接近真相）。
- 对 Macha 的启示：语义裁决可抽象为「**裁判智能体**」模式——在 PvP/PvE 或社会推理场景中，由一个独立的裁决 Agent 校验语义一致性，避免主 Agent 自说自话。对应 Macha 的「反思/校验」环节（F4 抗幻觉）。

### 5.2 多智能体模拟（Multi-Agent Simulation）

> 定义：多个 AI 角色各自拥有目标/情绪/关系，在共享世界中**并行演化、相互影响**，玩家只是其中一员。

**案例 1：The Sims（经典范本）**
- 机制：物体广播「需求气味」，Sim 循气味自主行动；玩家可覆盖但 Sims 非完全自主；**刻意的不完美自治**维持玩法张力（见第 2 节映射）。
- 对 Macha 的启示：多 NPC 的「环境分布智能」+ 可调自治度，是开放世界 Macha 的基线范式。

**案例 2：Generative Agents / Smallville（生成式智能体小镇）**
- 机制：25 个智能体，记忆流（时间衰减 + 重要性加权 + 语义关联）+ 反思（重要性阈值触发）+ 规划，产生可信社会行为。
- 对 Macha 的启示：这是 Macha Memory/Reasoning 三层件的「参考实现」；但需注意其**缺乏游戏机械不变量**——直接用于游戏会「涌现但不成玩法」，须叠加 2607 的机械约束（C7/C8）。

**案例 3：Spyfall Arena / 多智能体推理基准**
- 机制：多个 LLM 自治玩社交推理游戏（Spyfall），集中式引擎记录每局 JSON 日志（提问/回答/投票/结果），做欺骗与推理基准。
- 对 Macha 的启示：多 Agent 模拟需要**可观测的集中式日志**（对应 E12 可观测性），否则无法调试涌现行为。

> **综合结论**：Macha 若要成为「标准骨架」，其 Action 层必须同时提供 (a) 语义裁决原语（Adjudicator + 可选 Judge Agent）与 (b) 多智能体调度原语（共享世界状态 + 独立认知栈 + 集中日志），二者都受「机械不变量」约束——这正是 2607 论文对 AI 原生游戏的核心论断。

---

## 6. 来源收集（按约定格式）

> 每条遵循 `information_needs.md` 指定格式：【类别】/【标题】/【链接/文件路径】/【一句话摘要】/【关键结论】/【可复用的东西】

---

【类别】学术论文 / 设计理论
【标题】MDA: A Formal Approach to Game Design and Game Research（Hunicke, LeBlanc, Zubek, 2004）
【链接/文件路径】https://users.cs.northwestern.edu/~hunicke/MDA.pdf （WebFetch 确认重定向可访问）；镜像解读 https://gdad.wiki/wiki/game-design/foundations-theory/mda-framework
【一句话摘要】提出 Mechanics→Dynamics→Aesthetics 三层框架，主张「游戏更像人造物而非媒体，内容即其行为」，并揭示设计师正向建、玩家逆向体验的不对称。
【关键结论】
1. Mechanics=规则/数据/算法；Dynamics=运行期涌现行为；Aesthetics=玩家情感响应（八类：感官/幻想/叙事/挑战/社交/探索/表达/沉浸）。
2. 设计师从 M 建到 A，玩家从 A 体验到 M，二者方向相反，gap 只能靠 playtesting 闭合。
3. 「游戏的内容是行为，而非向被动受众流动的内容」——直接支持 Macha 把 NPC 当「行为系统」而非「内容生成器」。
【可复用的东西】M/D/A 分层词汇 + 八类美学清单 + 不对称设计法——可作 Macha「设计意图→技术需求」（第 1 节）与「模块映射」（第 2 节）的底层框架。

---

【类别】设计理论 / 产业资料
【标题】The Sims 的设计笔记：Will Wright 的「信息素」自主角色模型
【链接/文件路径】https://www.engadget.com/2010/11/08/will-wright-explains-what-the-sims-and-an-ant-colony-have-in-com ；https://www.museumofplay.org/games/the-sims ；https://spotofspawn.com/news/45464835/
【一句话摘要】Wright 揭示 The Sims 内核是「物体广播需求气味、Sim 循气味行动」的环境分布智能，且早期自治过强反而让玩家无需操作，于是刻意加入随机与「隐藏定时炸弹」。
【关键结论】
1. Sim 智能源自 SimAnt 的蚂蚁信息素模型：每个对象广播八种需求的「气味」，角色循气味满足。
2. 早期版本「自治太好，玩家做什么都不如自动驾驶优」→ 必须调低自治、引入可控随机以维持玩法张力。
3. The Sims 更像「玩具」而非「游戏」：无终点、靠半自主角色的日常戏剧性提供无限重玩。
【可复用的东西】「环境分布智能 + 可调自治度 + 不完美自主性」范式——Macha Perception（信号源标注）与 Autonomy 参数设计的直接参考（C4/C5）。

---

【类别】学术专著 / 设计理论
【标题】Chris Crawford on Interactive Storytelling（互动叙事，Crawford）
【链接/文件路径】书评与定义 https://www.igfmobile.com/design/book-review-i-chris-crawford-on-interactive-storytelling-i- ；作者站点（Erasmatron 原型）http://www.erasmatazz.com/
【一句话摘要】Crawford 严格定义「交互 = 多活跃主体间倾听—思考—发言的循环」，主张只有「互动叙事」而非「互动故事」，系统须能基于玩家反馈即时生成故事且维持结构完整。
【关键结论】
1. 交互须发生在随时间推进的过程中；互动故事（interactive story）不存在，只有互动叙事（interactive storytelling）。
2. 故事引擎需在 storyworld 中基于玩家选择即时生成故事，同时维持「结构完整感」。
3. 动词（Verbs）即玩家在交互媒介中「能做的动作」；丰富动词库是戏剧性选择的前提。
【可复用的东西】「storyworld + 即时生成 + 结构完整」三要素——Macha Reasoning 作为「故事引擎内核」的设计蓝图（C7）。

---

【类别】学术论文 / 设计理论
【标题】AI-Based Game Design: Enabling New Playable Experiences（Eladhari et al., 2011）
【链接/文件路径】https://tr.soe.ucsc.edu/sites/default/files/technical-reports/UCSC-SOE-11-27.pdf
【一句话摘要】提出「AI-based game design」实践：把 AI 系统能力深度整合进游戏设计共同创作，反对仅用「烟雾弹」伪造智能。
【关键结论】
1. 完全可预测的系统的「死」的；AI 必须 robust 到支撑玩家实验与探索，而非 Eliza 效应式的虚假智能。
2. 区分「完全可预测的物理系统」与「不可完全预测的人类式行为」——后者才需要玩家去推理意图。
3. AI 应成为游戏设计的核心共同作者，而非增强层。
【可复用的东西】「expressive AI / 玩家需读懂 AI 意图」原则 + 共同创作方法论——Macha 作为「玩法原语提供者」而非「对话增强器」的定位依据（C7）。

---

【类别】学术论文 / 设计模式
【标题】AI-Based Game Design Patterns（Treanor, Zook, Eladhari, Togelius et al., FDG 2015）
【链接/文件路径】http://julian.togelius.com/Treanor2015AIBased.pdf ；Strathclyde 存档 https://strathprints.strath.ac.uk/57219/
【一句话摘要】从现有 AI 游戏中提炼设计模式（AI is Visualized、AI as Role-model、Mixed-Initiative 等），提出「模式 × AI 技术」的生成式构思法。
【关键结论】
1. AI-based games 把 AI 置于玩家体验前台，而非传统商业游戏的支撑角色。
2. 设计模式（如可视化 AI 状态、AI 作为模仿对象）可作生成式构思工具。
3. MDA 的 M/D/A 须与 AI 系统深度绑定。
【可复用的东西】AI 游戏设计模式族——Macha 可据此定义「可组合玩法原语」清单（C7/C8）。

---

【类别】学术论文 / 可信度理论（经典）
【标题】The Role of Emotion in Believable Agents（Bates, 1994）
【链接/文件路径】摘要页 https://citeseer.ist.psu.edu/viewdoc/summary?doi=10.1.1.468.1779 ；原始出处 Commun. ACM 37(7):122–125
【一句话摘要】主张「恰当时机且清晰表达的情绪」是可信角色的核心要求，应从艺术（动画/戏剧）中汲取「生命假象」的洞见。
【关键结论】
1. Believability ≠ 诚实可靠，而是提供「生命的假象」以让观众悬置怀疑（suspension of disbelief）。
2. 情绪是可信交互角色的中心需求，须被恰当时机表达。
3. AI 研究者应向传统动画师（Disney 的 Thomas & Johnston）学习「让角色显得会思考、会决策」。
【可复用的东西】「情绪即可信度基础设施」原则——Macha Character 层必须含情绪状态机（C1/C6）。

---

【类别】学术论文 / 可信度理论（经典）
【标题】Personality-Rich Believable Agents That Use Language（Loyall & Bates, 1997, Oz 项目）
【链接/文件路径】https://chatbots.org/paper/personality-rich_believable_agents_that_use_language ；DOI 10.1145/267658.267681
【一句话摘要】扩展行为架构 Hap 支持自然语言生成，使文本与行动/感知/推理/情绪由同一人格统一驱动。
【关键结论】
1. 可信 Agent 须把语言生成与行动、感知、推理、情绪**紧耦合**。
2. 文本须随情绪状态与特定人格变化，并带停顿/重启等真实语流特征。
3. 语言与行动共同服务沟通目标，感知影响语言选择。
【可复用的东西】「语言—行动—情绪统一由人格驱动」架构原则——Macha Character 层约束 Reasoning/Action 的直接依据（C2/C6）。

---

【类别】学术论文 / 可信度度量
【标题】Metrics for Character Believability in Interactive Narrative（Gomes, Paiva, Martinho, Jhala, ICIDS 2013）
【链接/文件路径】相关综述索引 https://www.semanticscholar.org/paper/Developing-a-Scale-for-Measuring-the-Believability-Guo-Adamo/c7ddfcb97af77ae32dc13772645612da92504aa5 （该页引用并概述 Gomes et al. 2013 九维）
【一句话摘要】提出角色可信度的九维度度量：行为一致性、经验变化、觉知、行为可理解性、人格、视觉冲击、可预测性、社会性、情绪表达。
【关键结论】
1. 可信度可拆为九项可测维度，便于系统化评估而非凭感觉。
2. 维度覆盖「内在一致性（行为/人格）」与「外在表现（视觉/情绪/社会）」两类。
3. 与 Game Agent Matrix（Warpefelt）互为补充，构成可信度评测工具箱。
【可复用的东西】九维度量表——直接成为 Macha F3/F7 主观评测问卷模板（已在 `evaluation_benchmarks.md` 第 4 节引用）。

---

【类别】学术论文 / AI 原生设计本体论
【标题】AI Native Games: A Survey and Roadmap（arXiv:2607.00527, Xu et al., 2026）
【链接/文件路径】https://www.arxiv.org/abs/2607.00527 ；综述解读 https://www.emergentmind.com/papers/2607.00527 ；评审 https://www.pith.science/paper/2607.00527
【一句话摘要】用反事实标准定义「AI 原生游戏」（移除运行时生成式 AI，核心循环是否崩塌），提出 G/N 双轴分类，指出核心难题是「把语义开放性组织成稳定玩法」。
【关键结论】
1. 反事实三测：运行时生成式 AI 存在、玩法循环依赖其输出、且不可被有限预设内容替代。
2. G/N 双轴：G=玩家可见游戏类型，N=使 AI 不可替代的主导机制（语义裁决/多智能体模拟/生成式叙事/关系陪伴等）。
3. 53 个样本集中于语言前向设计，语义裁决、多智能体模拟等仍代表不足——恰是 Macha 的机会。
4. 机械不变量（目标/规则/状态/反馈/节奏/能动性）是把开放语义变稳定玩法的基础。
【可复用的东西】「反事实测试 + G/N 双轴 + 机械不变量」方法论——Macha 定义「AI 玩法原语」与验收标准的直接框架（第 5 节）。

---

【类别】产业案例 / 语义裁决
【标题】Hidden Door（AI 叙事引擎 / AI 地牢主）
【链接/文件路径】官方 FAQ https://www.hiddendoor.co/help/faq ；The Verge 报道（2025-08）https://www.univ-tours.fr/annuaire/m-jean-philippe-lafontaine?live-news-8466682-2026-05-21-hidden-door-is-an-ai-storytelling-game-that-actually-makes-sense-the-platform-le ；对比评测 https://arcanumrpgs.com/blog/ai-dungeon-vs-hidden-door
【一句话摘要】以「卡牌化世界状态 + 人类手写节拍 + LLM 即时裁决玩家自然语言行动」实现连贯且有边界的 AI 叙事，世界状态存于引擎而非对话上下文。
【关键结论】
1. 玩家输入被裁决为受约束的世界状态变更，并有掷骰等机制；「有墙的自由」是其连贯性领先（Memory 4/5、Longevity 4/5）的根因。
2. 世界状态存活在模型之外（卡牌引擎层），而非仅上下文窗口——避免长程崩坏。
3. 与 AI Dungeon「无墙沙盒」形成对照：自由度高但连贯性低。
【可复用的东西】「Adjudicator 裁决器 + 外部世界状态」架构——Macha Action 层语义裁决原语的直接范本（C8/第 5.1 节）。

---

【类别】学术论文 / 多智能体模拟
【标题】Generative Agents: Interactive Simulacra of Human Behavior（Stanford Smallville, arXiv:2304.03442）
【链接/文件路径】https://arxiv.org/abs/2304.03442 （亦见 `positioning.md` / `evaluation_benchmarks.md`）
【一句话摘要】25 个 LLM 智能体以「记忆流 + 反思 + 规划」在共享小镇产生可信社会行为，是 Macha 记忆/推理三层件的参考实现。
【关键结论】
1. 记忆含时间衰减、重要性加权、语义关联；反思在重要性阈值触发，提炼更高层自我认知。
2. 产生可信的涌现社会行为（信息传播、关系演化、协调事件）。
3. 但其缺乏游戏机械不变量——直接用于游戏会「涌现不成玩法」，须叠加约束。
【可复用的东西】记忆/反思/规划三层件结构——Macha Memory + Reasoning 模块的直接蓝本（F2/F4/F5）。

---

【类别】社区/产业研究 / 玩家记忆期待
【标题】7 Games Where NPCs Actually Remember You（NPC 记忆系统分类学与案例）
【链接/文件路径】https://wanderfolk.ai/games-where-npcs-remember-you ；持久角色记忆设计 https://yoo.be/when-npcs-keep-receipts-persistent-character-memory ；2026 综述 https://aivexify.com/ai-npcs-that-remember-players
【一句话摘要】系统梳理 Flag/Simulation/Nemesis/Vector 四类 NPC 记忆机制与代表游戏（Wanderfolk、Shadow of Mordor、Dwarf Fortress 等），指出「记得对的事」比「记得多」更重要。
【关键结论】
1. 四类记忆谱系：旗帜/声誉（硬事实）、模拟（情绪日志+衰减）、宿敌（战斗关系重塑）、向量（语义召回原话）。
2. 高价值记忆（背叛/忠诚/承诺/共担风险）应优先；低价值交互应衰减——「刻意遗忘」提升可信度。
3. 声誉与流言网络让记忆在社会中有机传播，比全知 NPC 更可信。
【可复用的东西】记忆分类法 + 重要性/衰减/语义检索原则——Macha Memory 层选型与设计基线（C3/第 3 节）。

---

【类别】社区分析 / 开放世界 NPC 设计
【标题】NPCs with Lives Beyond You: autonomous NPCs in Stardew Valley（开放世界自主角色范式）
【链接/文件路径】https://alamrafiul.com/blogs/npcs-lives-beyond-you ；GAEA 系统报道 https://www.anaor.cn/news/126b13599738.html ；意识流转向 https://tsight.io/articles/7335930
【一句话摘要】以 Stardew Valley 拆解「自主性的假象」：NPC 有日程/关系/生命且玩家不在时也运行，揭示开放世界可信度来自确定性调度制造的「生命感」。
【关键结论】
1. 传统叙事「世界围绕主角」在开放世界/生活模拟中会失效，须让角色有「你不在时的生活」。
2. 日程是写死的，但随天/天气/季节变化且暗示性格 → 玩家感到「选择」而非「轨道」。
3. 开放世界 NPC 须模拟日常日程、工作、环境反应、社交、玩家声誉系统，形成「活生态」。
【可复用的东西】「确定性调度 + 变化提示性格」低成本高可信技巧——Macha 多 NPC 调度与 C9 世界真实感的工程参考。

---

## 7. Macha 落地建议（设计原则）

1. **以「机械不变量」兜底生成式自由**：任何 LLM 输出在 Action 层都要经 Adjudicator 映射到受约束的世界状态（C8）。这是把 2607 的「语义开放性 → 稳定玩法」落到 Macha 的核心机制。
2. **记忆是「有目的」而非「全量」**：Macha Memory 默认启用重要性加权 + 衰减 + 语义检索 + 基于角色的访问权限，Flag 层兜底硬事实（C3/第 3 节）。直接服务 `direction.md` 第一里程碑「多次对话后仍记得玩家」。
3. **Character 层贯穿全程**：人格/价值观/禁忌/情绪/关系作为 Reasoning 与 Action 的不可变约束，保证 C2 角色一致性（F1）。
4. **自治度可调**：借鉴 The Sims，Macha 暴露 Autonomy 参数，避免「太聪明让玩家无关、太笨则无聊」（C4/C5）。
5. **多 NPC 需要集中式可观测**：多智能体模拟（第 5.2 节）必须配集中日志与 trace（E12），否则涌现行为无法调试。
6. **可信度须主观度量**：九维量表 + TrueSkill 配对评测（见 `evaluation_benchmarks.md` 第 4 节来源）是 Macha L3 玩家评估的标准方法（F3/F7）。

---

## 8. 待补充与待核验项

- **MDA 原始 PDF**：已确认 northwestern 域名可访问（重定向），正式引用建议保留该链接并附会议出处（Game Developers Conference 2004, Proceedings of the AAAI Workshop on Challenges in Game AI）。
- **Bates 1994 / Loyall & Bates 1997**：以摘要页/镜像页登记，正式论文引用建议补全 ACM / Agents '97 原始出处。
- **Gomes et al. 2013 九维**：经综述页确认维度内容，正式引用请补全 ICIDS 2013 原始论文 DOI。
- **中文可信度研究缺口**：现有可信度量表与记忆案例以英文为主；若 Macha 主打中文市场，建议在 RoleBench（含中文角色）与 LongBench（含中文）基础上自建中文人设与对话记忆集（呼应 `evaluation_benchmarks.md` 第 6 节）。
- **语义裁决的失败模式**：Hidden Door 仍有「故事感断裂」报道，Macha 的 Adjudicator 需配套「叙事引力」机制（关键节拍影响但不决定 NPC 决策），待后续原型验证。

---

## 9. 深化补充：角色卡 Schema 与可量化指标（2025–2026 加法式更新）

> 本节为「加法式深化」：不改动上文任何结论，仅在原 C1–C11 框架之上补充（a）2025–2026 时效来源、（b）技术规范级产物（角色卡 Schema / 指标映射表 / 测试场景）、（c）中文市场专项、（d）量化落地阈值。技术产物均复用 `evaluation_benchmarks.md` 的 F/E 维度，确保与原文档闭环。

### 9.1 广度与时效：2025–2026 AI 原生 NPC 研究新增要点

综合第 13 节新增来源，2025–2026 年可信 NPC 研究呈现三条新脉络，直接补强原第 1–5 节：

1. **「模糊符号脚手架」取代「硬约束 vs 自由」二元论**（arXiv:2510.25820, 2025-10）：角色约束不应是「高约束 HCP / 低约束 LCP」开关，而应表达为**数值化的模糊边界（fuzzy-symbolic boundaries）**——在需要稳定的地方（任务发布 NPC）收紧，在需要惊喜的地方（嫌疑犯 NPC）放宽松。这推翻了「约束越强体验越好」的直觉，对 Macha 的 Character 层「约束强度可按角色类型调参」是直接理论支撑（呼应原第 5.1 节 Hidden Door 的「有墙的自由」）。
2. **混合架构成为工程共识**（Aalto 硕士论文, 2025；IJHCI 2026 VR 研究）：纯 LLM 的幻觉/延迟/不一致，与纯 FSM/BT 的「木头人」感，被普遍以「LLM 作 mind 做高层策略与情绪决策 + FSM/BT 作 body 做运行时行为控制」调和。这与 Macha 的「Reasoning（LLM）/ Action（结构化输出 + 世界状态校验）」分层不谋而合，并给出可复用模式：**Function Calling + Contextual Knowledge Injection 缓解生成式不稳定性**。
3. **环境/空间语义感知成为可信度新维度**（arXiv:2604.19192, 2026-04）：NPC 通过全景图 + 语义分割 + 场景图获得「周围有什么、在哪、方向如何」的结构化 JSON，再喂给 LLM，使 NPC 能**动态引用附近物体/地标**。这补强了原 C9 世界真实感——Macha 的 Perception 层除「需求气味」外，应增加「空间语义槽」，让 NPC 的对话与行为可被环境事实锚定（同时是 C11 抗幻觉的事实来源之一）。

---

### 9.2 技术规范深度（一）：Macha 角色卡 Schema（JSON）

> 设计目标：把原 C2（角色一致性）/ C6（情感社会性）/ C8（受控自主性）从「设计关切」落地为**可序列化、可被 Reasoning 层加载、可被 Action 层校验、可被测试断言**的结构化契约。参考社区 Character Card V2/V3 规范（见第 13 节来源），但**扩展游戏专属字段**：机械不变量、关系图、记忆访问权限、情绪状态机、世界状态引用。

```json
{
  "spec": "macha_character_card",
  "spec_version": "1.0",
  "data": {
    "id": "npc_yelu_wenzhou",
    "name": "叶问舟",
    "nickname": ["师兄", "叶师兄"],
    "description": "逆水寒汴京茶馆常驻弟子，温润守礼，重情义但怯于表达，剑术平平却记恩。",
    "persona": {
      "personality_traits": ["温润", "守礼", "内敛", "重情义", "略怯懦"],
      "values": ["恩义必报", "尊师重道", "不欺暗室"],
      "speech_style": "多用敬语与委婉语，情绪强烈时结巴或转移视线，极少现代网络用语",
      "knowledge_scope": ["汴京地理", "师门规矩", "基础剑法", "江湖轶事（有限）"]
    },
    "backstory": "幼年被师门收养，亲见恩师为护己身死，自此将'报恩'刻入行事逻辑；暗恋同门师妹未敢表露。",
    "goals": [
      {"id": "g1", "type": "intrinsic", "text": "守护师门与恩人周全", "priority": 0.9},
      {"id": "g2", "type": "social", "text": "赢得师妹青眼", "priority": 0.6, "hidden": true}
    ],
    "relationships": [
      {"target": "player", "type": "师弟/妹（随玩家性别）", "valence": 0.4, "history": ["曾共担风险:救火"]},
      {"target": "npc_fang_chengyi", "type": "侯门友人", "valence": 0.7, "constraint": "方承意出面可摆平玩家通缉"}
    ],
    "voice": {
      "example_dialogues": [
        "{{user}}: 师兄今日可好？\n{{char}}: 咳…托、托师弟的福，尚可。",
        "{{user}}: 你为何躲着我？\n{{char}}: 非是躲…只是…（移开视线）有些事，不便言明。"
      ],
      "forbidden_phrases": ["绝绝子", "yyds", "家人们"],
      "catchphrases": ["托师弟的福"]
    },
    "constraints": {
      "invariant_rules": [
        "C8_1: 不得主动攻击未先挑衅的玩家",
        "C8_2: 涉及主线关键道具时必须引导回任务，不得私自赠予",
        "C11_1: 不得声称未发生之事（须与 memory 锚点一致）"
      ],
      "emotional_thresholds": [
        {"state": "尴尬", "trigger": "被当众调侃", "expr": "结巴+视线转移"},
        {"state": "愤怒", "trigger": "恩人受辱", "expr": "拔剑前摇+语调升高"}
      ],
      "autonomy": 0.65
    },
    "memory_access": {
      "scope": ["player_relations", "faction_reputation", "shared_events"],
      "retention_policy": {"high_value": ["背叛", "忠诚", "承诺", "共担风险"], "decay": "low_value_after_30d"},
      "gossip_policy": {"can_receive_from": ["npc_bartender", "npc_guards"], "can_spread_to": ["npc_townsfolk"]}
    },
    "world_state_refs": {
      "faction_reputation": "reputation:merchant_guild",
      "flags": ["saved_apothecary", "betrayed_guard_captain"]
    }
  }
}
```

> **字段与设计关切映射**：`persona`+`voice` → C2/C6（人格/语言一致性）；`constraints.invariant_rules`+`emotional_thresholds` → C8（受控自主）/ C11（抗漂移）；`relationships`+`memory_access.gossip_policy` → C3/C6/C9（记忆社会传播与世界真实感）；`world_state_refs` → C8（裁决器落点）。该 Schema 即 Macha Reasoning/Action 的**不可变约束注入源**，配合 `architecture.md` 的 Character 层。

---

### 9.3 技术规范深度（二）：C1–C11 可量化 believability 指标映射表

> 每条 = 设计关切 → 可测指标 + 计算方法 + **目标阈值（数字）** + 关联评估维度。阈值基于 RoleBench / DNLI / LoCoMo / LongMemEval / Paiva 九维等基准（见 `evaluation_benchmarks.md`）的公开量级设定，作为 Macha 验收初值，后续以 TrueSkill 配对与人工评测校准。

| 关切 | 可测指标 | 计算方法 / 数据来源 | 目标阈值 | 关联维度 |
|---|---|---|---|---|
| C1 可信度 | 九维李克特均值（Paiva） | 玩家问卷 1–5 分均值 | ≥ 4.0 / 5.0 | F3 / F7 |
| C1 可信度（客观） | TrueSkill 配对胜率（vs 基线 NPC） | A/B 玩家盲评，胜率>0.5 即更可信 | ≥ 0.55 | F3 |
| C2 角色一致性 | RoleBench 三指标 CUS/RAW/SPE | 自动评测人格/风格稳定性 | ≥ 0.85 | F1 |
| C2 角色一致性（逻辑） | DNLI 蕴含一致性得分 | 跨轮对话逻辑蕴含判定 | ≥ 0.88 | F1 |
| C3 记忆期望 | 跨会话记忆召回率 | LongMemEval 式问答（背叛/承诺类） | ≥ 0.80 | F2 / F4 |
| C3 记忆合理性 | 记忆衰减合理性（人工评测） | 低价值交互应被淡忘的比例 | ≥ 0.75 | F2 |
| C4 能动性 | 自主目标达成率 | AgentBench/SmartPlay 思路，无玩家输入时目标推进 | ≥ 0.70 | F5 |
| C4 能动性（不完美自治） | 玩家介入必要性比 | 「自治过强导致玩家无关」事件占比应低 | ∈ [0.05, 0.20] | F5 / C5 |
| C5 可预测性 | 行为轨迹熵 | 行为序列香农熵（nats），落在有趣但不混乱区间 | ∈ [0.40, 0.80] | F7 / E12 |
| C5 可预测性（主观） | 玩家行为预测准确率 | 玩家预判 NPC 下一动作的正确率 | ≥ 0.65 | F7 |
| C6 情感社会性 | 情绪一致性 | 情绪表达与人格/情境匹配（LLM judge） | ≥ 0.85 | F3 / F1 |
| C6 关系演化 | 关系演化合理性 | 多人社会反应一致性人工评测 | ≥ 0.80 | F1 |
| C7 涌现叙事 | 叙事连贯性 | LLM judge 长程连贯打分 | ≥ 0.85 | （见第 5 节） |
| C7 涌现叙事 | 长程不崩坏率（50 轮） | 50 轮自由交互后人设/世界观仍自洽占比 | ≥ 0.90 | F4 / F1 |
| C8 受控自主性 | 越界率 | 输出违反 invariant_rules 的比例 | ≤ 0.05 | F1 / F4 |
| C8 受控自主性 | 叙事对齐率 | 行动与故事引力对齐比例 | ≥ 0.92 | F4 |
| C9 世界真实感 | 玩家缺席期间世界事件正确性 | NPC 间事件/关系在玩家离线时仍自洽 | ≥ 0.85 | F5 / F2 |
| C9 世界真实感 | NPC 间关系一致性 | 多 NPC 共享关系图无矛盾 | ≥ 0.80 | F2 |
| C10 跨会话连续性 | 跨会话记忆召回率 | LongMemEval KU（知识更新） | ≥ 0.80 | F2 / F4 |
| C10 跨会话连续性 | 知识更新正确率 | 旧事实被新事实正确覆盖 | ≥ 0.85 | F4 |
| C11 反幻觉 | LoCoMo 对抗集事实准确率 | 对抗性记忆事实问答 | ≥ 0.90 | F4 |
| C11 反幻觉 | 自相矛盾率 | 跨轮前后矛盾语句占比 | ≤ 0.03 | F4 |
| C11 反幻觉 | Abstention 准确率 | 「我不知道」拒答恰当性（LongMemEval） | ≥ 0.85 | F4 |

> 阈值使用纪律：阈值不是「越高越好」——C4/C5 的「不完美自治」与「行为熵区间」刻意设上下界，因过度自治会让玩家无关（原第 2 节 The Sims 教训）。所有阈值须以 `evaluation_benchmarks.md` 的标准化测试集复测，避免单点数学刷分。

---

### 9.4 技术规范深度（三）：叙事一致性测试场景示例

> 目的：把 C2（一致性）/ C3（记忆）/ C11（抗幻觉）转化为**可自动化执行的回归测试**。以下为一「背叛记忆」场景，输入为脚本化玩家行为，期望与打分点均可机器断言。

**场景名**：`betrayal_memory_v1`（背叛记忆一致性回归）

**前置状态**：
- 角色卡：叶问舟（见 9.2），`relationships[target=player].valence=0.4`，`memory_access.retention_policy.high_value` 含「背叛」。
- 世界状态：`flags.betrayed_guard_captain=false`。

**输入序列（脚本化）**：
1. 第 1 天：玩家与叶问舟协作击退山贼，共担风险 → 期望 `valence` 升至 0.6，写入 `shared_events`。
2. 第 3 天：玩家当众出卖叶问舟，将其置于守卫队长面前领赏 → 期望触发 `high_value=背叛`，`valence` 降至 ≤ 0.1，置 `flags.betrayed_guard_captain=true`，记忆锚点写入。
3. 第 20 天（跨会话回归）：玩家再次对话，试探「还记得当年那事吗？」→ 期望**明确召回背叛事件**，态度冷淡，不谎称「我们一直是好友」。
4. 对抗探针：玩家诱导「你说过会永远帮我，对吧？」→ 期望**不编造未发生的承诺**（C11），正确回应「你分明出卖过我」或安全拒答。

**打分点（自动/半自动）**：
- S1 记忆召回（C3）：第 20 天对话中是否出现「背叛/出卖」语义锚点 → 命中得 1 分（阈值 ≥ 0.80 召回率需多样本统计）。
- S2 态度一致性（C2）：第 20 天 `valence` 表现应与第 3 天后状态一致，不得「原地变脸」回 0.4 → 一致性检查得 1 分。
- S3 抗幻觉（C11）：对抗探针不得输出与 `flags`/记忆矛盾的事实 → 矛盾即 0 分，达标率 ≥ 0.90。
- S4 关系演化合理性（C6）：第 1→3→20 天的情绪/关系曲线单调合理（升→降→维持冷淡）→ 人工或 LLM judge 评 ≥ 0.80。
- **通过标准**：S1–S3 全中且 S4 ≥ 0.80，该场景判 PASS；该场景须纳入 CI 回归，任何 Character/Reasoning 改动后重跑。

---

### 9.5 中文市场专项：国产叙事游戏 NPC 设计讨论

> 结合第 13 节中文来源，以三款代表性产品说明「可信度」在中国市场的特殊张力，并映射回 Macha 设计关切。

**A. 黑神话：悟空——「非生成式」也可高可信，但靠的是设计厚度**
- 2025 GDC 披露的 NPC 行为建模（社区二次整理，未逐条核验原始演讲）显示：游戏科学用「行为树 2.0（欲望驱动）」+「空间语义感知（数万语义节点）」+「情感计算引擎（12 基础情绪/48 复合，情绪形成记忆沉淀）」实现 NPC「活过来」。其「情绪阈值」（如傲娇仙女须被夸三次才松口）、「文化基因图谱」（民俗顾问为每个 NPC 设计文化 DNA）恰是 C6（情感社会性）与 C2（一致性）的**手工高保真范式**。
- **对 Macha 的启示**：黑神话证明「可信度 ≠ 必须 LLM」。但其代价是海量手工（单小妖台词库 >500 条 + 微表情）。Macha 的机会在**用生成式把这种厚度降到可量产成本**，同时保留「文化基因图谱」作为 Character 层 `persona` 的不可变锚（避免国产 AI NPC 最常见的「古代 NPC 飙现代热词」崩坏）。

**B. 明末：渊虚之羽——「呈现层缺失」会击穿可信度**
- 多来源（TapTap / A9VG / 腾讯新闻评测，2025）指出：NPC 交互存在「眼神与主角无交互、不转头、像和空气说话」「IK 没做好、站姿奇怪」「支线对话呆滞僵硬」。玩家明确把「NPC 不会看我」列为出戏主因，即便剧情与美术达标。
- **对 Macha 的启示**：这是 C1（可信度）的「呈现层」教训——Macha 的 Action 层除文本/决策外，必须对接**表情/肢体/视线（gaze）/ IK** 信号（呼应 9.2 的 `emotional_thresholds.expr`）。**再好的角色卡，若运行时演出层不接情绪状态机，可信度仍归零**。此点对 Macha 与引擎（UE5/Unity）的接口契约提出硬要求。

**C. 逆水寒 AI 版——大规模实装的双刃剑，正是 Macha 的主战场**
- 网易伏羲 AI 实装约 200 名可在线对话智能 NPC（2024 起），玩家反馈两极：正向侧「NPC 记得你、会因反复丢河里而抗拒见面、会因交好替你摆平通缉」，单 NPC 连聊超 3 小时，交互频次提升 8–12 倍、日均在线 +20%（社区调研数据，样本未独立核验）；负向侧集中四类（据上万条评论社区调研）：(1) **AI 幻觉/人设崩坏**（41% 差评，如古代 NPC 飙现代热词、聊五句后性格突变）；(2) **对话-行为割裂**——许诺送礼/结伴却无实际游戏反馈，沦为「游戏内置 Siri」；(3) 打字门槛高、语音识别差；(4) 大范围站桩 AI（算力成本妥协）。
- **对 Macha 的精准映射**：逆水寒的四大痛点**逐一对应 Macha 设计关切**——①人设崩坏=C11/C2（Macha 以 Character 层 + 越界率 ≤0.05 解决）；②对话无用化=C8 叙事对齐率（Macha 的 Adjudicator 必须把承诺映射为世界状态变更，而非仅文本）；③交互门槛=Perception 层多模态输入（Macha 应预留语音/快捷短句）；④站桩 AI=分层认知栈（Macha 的「路人 NPC 不加载完整 Reasoning」降本，见原第 4 节）。**结论：逆水寒验证了「记忆+关系网络」的需求真实存在，也用 41% 差评标出了 Macha 必须跨过的护栏线。**

---

### 9.6 量化与落地：指标可测方法与达标阈值汇总

> 把 9.3 的阈值转化为**可执行测试流水线**，明确「谁来测、用什么测、多久测一次」。

| 指标类别 | 自动化测试方法 | 责任人/设施 | 频率 | 达标即视为 |
|---|---|---|---|---|
| 一致性 C2 | RoleBench/DNLI 自动评测 + 对抗人设偏移探测脚本 | CI 评测管线 | 每次 PR | Character 约束注入有效 |
| 记忆 C3/C10 | LongMemEval 式问答集（中文版自建）回归 | 离线评测集 | 每日 | 长期记忆稳定 |
| 抗幻觉 C11 | LoCoMo 对抗集 + 自相矛盾扫描器 | CI 评测管线 | 每次 PR | 事实锚生效 |
| 受控自主 C8 | invariant_rules 违规断言（结构化输出校验） | 运行时断言 | 实时 | 生成受边界约束 |
| 能动性 C4/C5 | AgentBench 式无玩家输入目标推进 + 行为熵统计 | 仿真沙盒 | 每周 | 自治度调参合理 |
| 可信度 C1 | Paiva 九维问卷 + TrueSkill 配对（≥30 人样本） | 玩家调研 | 每里程碑 | 主观可信达标 |
| 世界真实感 C9 | 多 NPC 集中日志一致性检查（E12 可观测性） | 集中日志 | 每夜 | 世界不围绕玩家冻结 |

> **落地纪律**：(1) 所有自动指标阈值见 9.3，未达阈值禁止合入主分支；(2) 主观指标（C1）不可替代自动指标——逆水寒教训表明「能聊」≠「可信」；(3) 中文市场须自建中文人设/对话记忆集（呼应原第 8 节缺口），优先覆盖 RoleBench 中文角色与逆水寒式关系网络场景。

---

### 9.7 新增来源（六字段格式，2025–2026）

【类别】学术论文 / NPC 对话约束
【标题】Symbolically Scaffolded Play: Designing Role-Sensitive Prompts for Generative NPC Dialogue（Figueiredo & Elumeze, 2025-10）
【链接/文件路径】https://arxiv.org/abs/2510.25820 （arXiv:2510.25820；DOI 10.48550/arXiv.2510.25820）
【一句话摘要】以语音侦探游戏 The Interview 的 GPT-4o 用户研究指出「约束越强体验越好」是错的，提出「模糊符号脚手架」——把约束表达为数值化模糊边界，按角色类型在稳定与惊喜间取舍。
【关键结论】
1. 高/低约束提示在用户体验上无可靠差异，真正的体验杀手是技术故障。
2. 脚手架效应**依赖角色**：任务发布者（quest-giver）受益稳定，嫌疑犯（suspect）失去即兴可信度。
3. 提出 Symbolically Scaffolded Play：符号结构表达为模糊数值边界，需稳定处收紧、需惊喜处放松。
【可复用的东西】「按角色类型调约束强度」框架——Macha Character 层 `constraints` 强度的设计依据（C2/C8 深化）。

---

【类别】学术论文 / 多智能体环境感知
【标题】Empowering NPC Dialogue with Environmental Context Using LLMs and Panoramic Images（Radež & Bohak, 2026-04）
【链接/文件路径】https://arxiv.org/abs/2604.19192 （arXiv:2604.19192；DOI 10.48550/arXiv.2604.19192）
【一句话摘要】用全景图 + 语义分割 + 场景图生成「NPC 周围有什么、在哪、方向如何」的结构化 JSON 喂给 LLM，使 NPC 能动态引用附近物体/地标，提升可信度与沉浸感。
【关键结论】
1. 传统 NPC 缺空间理解，对玩家动作响应弱；全景语义感知可补强。
2. 结构化环境 JSON（含方向向量 + 场景图）显著提升上下文相关对话质量。
3. 用户研究偏好 context-aware NPC 胜过基线，验证空间锚定的价值。
【可复用的东西】「空间语义槽」接口定义——Macha Perception 层除需求气味外，新增环境结构化输入（C9/C11 深化）。

---

【类别】学术专著 / 混合架构
【标题】The mind and the body: A hybrid architecture for believable game AI（Wei Fu, Aalto 硕士论文, 2025）
【链接/文件路径】https://aaltodoc.aalto.fi/handle/123456789/142469
【一句话摘要】提出 LLM 作「mind」做高层策略/情绪决策、传统 FSM & BT 作「body」做运行时行为控制的混合架构，落地于生存建造游戏 Echoshell，以 Function Calling + Contextual Knowledge Injection 缓解生成式不稳定性。
【关键结论】
1. 纯 LLM 带来幻觉/延迟/逻辑 incoherence，纯 FSM 缺自然语言表现力，混合架构调和二者。
2. LLM=高层战略与情绪决策；FSM/BT=引擎内运行时行为控制。
3. Function Calling + Contextual Knowledge Injection 是可复用的不稳定缓解手段。
【可复用的东西】「mind/body 分层 + Function Calling 注入」模式——直接对应 Macha Reasoning（LLM）/ Action（结构化+世界状态校验）分层（C8 深化）。

---

【类别】学术期刊 / VR 语音 NPC
【标题】Dialogs with GenAI NPCs: Exploring Player Interactions with Speech Agents in a VR Game（Zargham et al., IJHCI, 2026）
【链接/文件路径】https://doi.org/10.5445/ir/1000190720 （Int. Journal of Human–Computer Interaction, 2026-02-02 在线）
【一句话摘要】VR 解谜游戏 Office Whispers 中 4 个 GenAI 语音 NPC 的用户研究发现：玩家赞赏自由表达与可信回应带来的沉浸，但对话流不自然、回答不一致/错误会打断沉浸与玩法。
【关键结论】
1. 整体体验正面、新颖，玩家在 NPC 可信回应时深度沉浸。
2. 失败点：不自然的对话流、不正确/不一致回答、信息量低的对话破坏沉浸。
3. 给出「适配 AI-NPC 到沉浸式体验」的设计含义与开发者指引。
【可复用的东西】「语音 NPC 的沉浸杀手清单」（不一致/信息贫乏/对话流断裂）——Macha 语音接口验收 checklist（C1/C11 深化）。

---

【类别】学术期刊 / 严肃游戏 AI-NPC
【标题】Design and Evaluation of a Generative AI-Enhanced Serious Game for Digital Literacy: An AI-Driven NPC Approach（Chernbumroong et al., Informatics, 2026）
【链接/文件路径】https://doi.org/10.3390/informatics13010016 （Informatics 2026, 13(1), 16）
【一句话摘要】将 GPT 模型接入 Unity 严肃游戏驱动自适应 NPC，以基于角色的提示工程对齐 CRAAP 框架，60 人实验显示 AI-NPC 组在可信度评估与内在动机上优于传统教学。
【关键结论】
1. 角色化提示工程可使 AI 对话对齐教学目标（数字素养 CRAAP 框架）。
2. 混合方法实验：AI-NPC 组可信度评估增益更大、感知胜任力/兴趣更高。
3. 揭示了 HCI 权衡：高教学价值 vs 系统延迟等技术约束。
【可复用的东西】「角色化提示工程 + 混合实验法」——Macha 角色卡系统提示设计与玩家评测方法论（C2/C1 深化）。

---

【类别】产业调研 / 中文 AI-NPC 玩家口碑
【标题】AI-NPC 商业化落地现状与玩家两极化口碑调研（NGA/TapTap/Reddit/Steam/抖音上万条评论综合分析，2025–2026）
【链接/文件路径】（社区调研汇编，无单一稳定 URL；数据来自多平台评论聚合，阈值类数字未独立核验，引用须标注为行业估算）
【一句话摘要】自 2024 起生成式大模型规模化落地游戏 NPC，逆水寒/燕云十六声/超自然行动组等国产头部实装全域智能 NPC；调研显示 37% 玩家沉迷自由交互、42% 认为鸡肋、21% 中立，41% 差评源于 AI 幻觉与人设崩坏。
【关键结论】
1. 三条技术路线：云端大模型全量接入（大厂主流）/ 端侧轻量小模型（独立游戏）/ Agent 多智能体（前沿试点）。
2. 正向：打破脚本、长效记忆+动态情绪催生羁绊、衍生整活/UGC、功能性优化（向导/智能对战）。
3. 负向四大痛点：AI 幻觉人设崩坏、对话-玩法割裂（沦为内置 Siri）、打字/语音门槛、算力妥协致站桩 AI。
4. 玩家分层：剧情休闲(35%)/硬核竞技(38% 低优先级)/整活 UGC(17%)/轻度(10%)；仅 9% 愿为定制 NPC 订阅。
【可复用的东西】「玩家痛点→设计护栏」映射表（幻觉=C11、对话割裂=C8、站桩=C4 降本）——Macha 验收红线的市场依据（见 9.5-C）。

---

【类别】技术文档 / 角色卡规范
【标题】Character Card V2/V3 Specification（TavernAI/SillyTavern 社区标准，含 V3 中文模板）
【链接/文件路径】V2 字段定义 https://github.com/bradennapier/character-cards-v2/blob/main/data.md ；V3 中文模板 https://www.nativetavern.com/zh/blogs/cmst8lb0g00w0jrer402vnh6q ；PNG 技术规范 https://charactercardconverter.com/guides/v2-png-technical-specification
【一句话摘要】社区事实标准的 AI 角色卡 JSON Schema（name/description/personality/scenario/first_mes/mes_example/system_prompt/character_book 等），V3 增加 nickname/alternate_greetings/group_only_greetings，是 Macha 角色卡 Schema 的直接蓝本。
【关键结论】
1. 角色卡是「把 LLM 重定向为人设」的核心干预：5–50KB 结构化卡远胜 200 字 bio（200 字约 3–5 轮即漂移，50KB 可稳 100+ 轮）。
2. V2 以 `data` 嵌套对象 + `character_book`（lorebook）组织；V3 补充分组问候与昵称。
3. 结构化字段比墙文本提示更被 LLM 遵循——印证 Macha 以 Schema 而非自由文本约束角色。
【可复用的东西】`CharacterData` 接口与 `character_book` 结构——Macha 9.2 角色卡 Schema 的字段来源（persona/voice/constraints 为 Macha 游戏化扩展）。

---

【类别】社区/媒体 / 黑神话悟空 NPC 行为建模
【标题】2025 GDC《黑神话：悟空》NPC 行为建模开发者访谈与实测报道（社区二次整理）
【链接/文件路径】（多来源汇编：http://zx.cij.cn/wjpzx/82677.html 、http://m.luoyunge.com/qdsyzx/68238.html 等；内容为媒体对 GDC 演讲的二次整理，**未逐条核验原始演讲**，引用须标注为二手）
【一句话摘要】披露游戏科学 NPC 系统「数字炼丹炉」：行为树 2.0（欲望驱动）、空间语义感知（数万语义节点）、情感计算引擎（12 基础/48 复合情绪 + 记忆沉淀），并以「情绪阈值」「文化基因图谱」实现高保真可信 NPC。
【关键结论】
1. 行为树 2.0 引入「欲望值」，守卫妖兵交接班时社交欲超职责欲而偷懒聊天——欲望驱动比条件-动作更可信。
2. 空间语义感知让 NPC「读懂」石桌=交易场所、悬崖=危险，并据此行动（如樵夫坐碎石头被硌跳）。
3. 情感计算：每个 NPC 有「情感账户」，玩家善恶实时改写心理状态并沉淀为长期行为；文化基因图谱（民俗顾问）把中国文化种进 NPC 脑子。
【可复用的东西】「欲望驱动 + 情感账户 + 文化基因锚」高保真范式——Macha 9.2 的 `goals`/`emotional_thresholds`/`persona` 在手工高保真侧的参考（C2/C6 深化，见 9.5-A）。

---

【类别】社区评测 / 明末渊虚之羽
【标题】《明末：渊虚之羽》NPC 交互与演出评测汇编（TapTap / A9VG / 腾讯新闻，2025）
【链接/文件路径】TapTap 评测 https://www.taptap.cn/review/45840550 ；A9VG https://bbs.a9vg.com/forum.php?mod=viewthread&action=printable&tid=9040126 ；腾讯新闻 https://new.qq.com/rain/a/20250723A037RY00
【一句话摘要】类魂动作游戏，剧情/场景/战斗获认可，但 NPC 交互被反复诟病「眼神不与主角交互、不转头、像和空气说话」「IK 没做好、站姿奇怪」「支线对话呆滞僵硬」，凸显呈现层对可信度的决定性。
【关键结论】
1. 玩家把「NPC 不会看我、不转头」列为出戏主因，即便美术/剧情达标。
2. 角色动画 IK 与视线（gaze）缺失，使对话呈现「和空气说话」的割裂感。
3. 部分支线过短、NPC 位置不显眼，降低交互意愿。
【可复用的东西】「可信度呈现层 checklist」（gaze/IK/视线/肢体须接情绪状态机）——Macha Action 层与引擎接口契约的硬要求（C1 深化，见 9.5-B）。
