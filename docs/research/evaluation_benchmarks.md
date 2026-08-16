# Macha 的评估维度表 + 基准数据集清单

> **类别归属**：`information_needs.md` 第 5 类「评估基准：如何证明骨架是标准」。
> **文档性质**：研究子任务交付物（不是 Demo，而是为 Macha「标准骨架」服务的评估体系）。
> **配套文档**：`direction.md`（最小可验证方向：长期记忆 + 角色一致性）、`positioning.md`（四篇论文定位）、`architecture.md`（目标架构）。
> **核心命题**：没有标准评估，就没有标准骨架。Macha 的评估必须同时覆盖**功能性维度**（可信度、一致性、记忆、规划）与**工程性维度**（延迟、成本、吞吐、可观测），并能以可复用的方式证明自己"比其他 NPC 方案更可信、更一致、更可调试"。

---

## 0. 文档使用方法

- **第 1 节**给出评估框架的层次，方便把零散基准拼成体系。
- **第 2 节「评估维度表」**是给工程团队的主交付：每一行都是一个可在 Macha 中落地的度量（维度 / 度量对象 / 方法 / 相关基准 / 对 Macha 的意义）。
- **第 3 节「基准数据集清单」**是给研究员的主交付：可直接拿来跑实验的数据集。
- **第 4 节「来源收集」**按 `information_needs.md` 约定的固定格式登记关键来源。
- **第 5 节**给出 Macha 落地建议（反幻觉压力测试设计、工程埋点、可观测性）。

> 说明：所有 URL 均为本次研究通过 WebSearch / WebFetch 实际获取。**LongMemEval** 仅找到二手综述（未核验到主论文 arXiv 直链），已在对应条目明确标注；其余主链接均经核验或来自论文/官方仓库页面。

---

## 1. 评估框架总览

Macha 的评估体系建议分为三层，避免"只跑学术榜单、不解决游戏落地"：

| 层 | 名称 | 解决什么 | 典型手段 |
|---|---|---|---|
| L1 | **离线功能基准** | NPC 是否"记得住、说得像、不胡说" | LoCoMo / LongMemEval / MemoryArena / RoleBench / PersonaChat |
| L2 | **在线工程度量** | NPC 是否"跑得起、测得清、调得动" | 延迟/成本/吞吐埋点 + LangSmith/Phoenix 追踪 |
| L3 | **玩家主观评估** | NPC 是否"看起来可信、可预期" | Believability 量表 + TrueSkill 配对评测 |

> 三个层对应 Macha 名称的三层含义：**M**（Memory，L1）、**A**（Architecture/Action，L1 规划+L2 工程）、**C**（Character，L1 一致性 + L3 可信度）。

---

## 2. 评估维度表

> 维度分类：功能性（F）/ 工程性（E）。"方法"列给出可操作的具体做法；"相关基准"列指向第 3 节数据集。

| # | 维度 | 度量对象 | 方法 | 相关基准 | 对 Macha 的意义 |
|---|---|---|---|---|---|
| F1 | **角色一致性 / Role Fidelity** | 人格、说话风格、价值观、禁忌在长程交互中的稳定性 | 1) RoleBench 三指标：CUS（风格一致性）、RAW（角色准确性与分寸）、SPE（角色专属知识）；2) 基于 DNLI 的对话蕴含一致性判定；3) 固定人设后做"对抗性人设偏移"探测 | RoleLLM/RoleBench、PersonaChat、LoCoMo、Clembench | Macha 区别于"通用聊天机器人"的核心卖点；是"标准骨架"必须可度量、可保证的属性 |
| F2 | **长期记忆稳定性** | 跨会话的信息提取、多会话推理、知识更新、时序推理、拒答能力 | 1) 长对话多跳问答；2) 知识更新测试（同一事实前后矛盾时取最新）；3) 时序问答；4) 未提供信息时的显式拒答率 | LoCoMo、LongMemEval、MemoryArena、RULER | 直接证明 Macha 的 M（Memory）："多次对话后仍记得玩家"是立项第一里程碑 |
| F3 | **可信度 / Believability** | 玩家主观认为 NPC"像一个真实存在的人/角色"的程度 | 1) Paiva believability dimensions 李克特量表（一致性、经验变化、觉知、可理解性、人格、情绪表达、社会性、视觉冲击、可预测性）；2) 感知智能量表（胜任/有知/负责/聪明/明智） | Clembench、LIGHT、自定义玩家调研 | 直接对应项目目标"可信 NPC"；是玩家采纳与投入的前提 |
| F4 | **反幻觉 / 抗角色漂移** | 是否编造未发生事件、是否在长程中偏离设定、是否混淆旧/新事实 | 1) LoCoMo adversarial QA；2) LongMemEval 的 Knowledge Update + Abstention；3) 自定义"记忆一致性压力测试"（见第 5 节） | LoCoMo、LongMemEval、MemoryArena | 关系玩家信任与安全；是"标准骨架"可靠性的底线 |
| F5 | **规划与决策能力** | NPC 在游戏世界中的目标规划、工具使用、多智能体协作 | 1) 多环境任务成功率；2) 协作效率分 CoS；3) 9 项智能体能力分项（对象依赖推理、前瞻规划、空间推理、从历史学习、随机性理解等） | AgentBench、SmartPlay、MindAgent、WebArena | 对应 A（Architecture）的行动层：NPC 不只是聊天，要能在世界中做事 |
| F6 | **对话质量 / 多轮一致** | 多轮对话连贯性、任务完成度、角色扮演自然度 | 1) MT-Bench 多轮八维度（GPT-4 判分）；2) 任务型对话 DST 准确率；3) grounded dialogue 合理性 | MT-Bench、DSTC/MultiWOZ、LIGHT | 对话层基础质量；角色扮演体验的底座 |
| F7 | **可预测性 / Predictability** | 行为是否可被玩家理解和预期（不过度随机、也不完全死板） | 1) Paiva predictability 维度量表；2) 行为轨迹熵 / 可解释性打分 | LIGHT、自定义 | 可玩性基础；也是"可调试 NPC"的前提（见 F12/E12） |
| F8 | **长上下文理解** | 在超长上下文中的检索与推理鲁棒性 | 1) 合成可控任务（NIAH 变体、多跳追踪、聚合）；2) 真实长文档 QA | LongBench、RULER | 与 Macha 记忆检索互补：决定"把记忆塞进上下文"还是"外挂记忆系统" |
| E9 | **延迟 / Latency** | 单次响应、首字延迟、端到端回合延迟 | 推理埋点计时（首 token / 末 token）；trace 自动采集 | 自建 + Phoenix/LangSmith trace | 实时对话体验硬约束；决定"能否用于在线游戏" |
| E10 | **成本 / Cost** | 每轮/每会话 token 成本、检索与工具调用成本 | token 计数 + 成本看板；对比不同记忆策略的单位成本 | 自建 | 商业可行性；外挂记忆 vs 长上下文的经济性权衡 |
| E11 | **吞吐 / Throughput** | 并发 NPC 数量、QPS、单位时间内处理会话数 | 压测（并发场景、批量推理） | 自建 | 多 NPC 场景规模化；开放世界需同时驱动大量 NPC |
| E12 | **可观测性 / Observability** | 决策链路可追踪、可回放、可调试 | OpenTelemetry/OpenInference trace；LangSmith 或 Phoenix 看板 | 自建 trace 规范 + LangSmith/Phoenix | 可解释性的工程落地：玩家需要"可预测的 NPC"，开发者需要"可调试的 NPC" |
| E13 | **可复现 / 回归** | 版本间质量稳定性 | 固定数据集 + 实验（experiment）对比；Phoenix datasets/experiments | Phoenix、LongMemEval 固定集 | 持续迭代保障：每次改骨架都能证明"没变差" |

---

## 3. 基准数据集清单

> 「访问方式与许可」：能确认的具体许可已注明；其余以仓库 LICENSE 为准（论文数据集多随仓库发布，商用需逐条核对）。

| 名称 | 度量内容 | 访问方式与许可 | 与 Macha 的关联 |
|---|---|---|---|
| **AgentBench** | LLM 作为智能体在 8 类环境（OS/DB/知识图谱/卡牌/谜题/家务/网购/浏览）的多轮决策与推理 | 论文 https://arxiv.org/abs/2308.03688 ；代码/数据 https://github.com/THUDM/AgentBench ；榜单 https://llmbench.ai/agent ；以仓库 LICENSE 为准 | 验证 Macha 行动层（F5）在通用任务上的能力基线 |
| **WebArena** | 真实可自托管 Web 环境（电商/论坛/协作开发/内容管理）中端到端任务成功率（功能正确性自动校验） | 论文 https://arxiv.org/abs/2307.13854 ；环境/数据 https://webarena.dev （ICLR 2024） | 评估 NPC 在"开放环境工具使用"上的规划与执行（F5） |
| **ToolBench / ToolLLM** | 16,464 个真实 REST API 的工具调用能力（单/多工具、DFSDT 规划）；ToolEval 通过率/胜率 | 论文 https://arxiv.org/abs/2307.16789 ；数据/模型 https://github.com/OpenBMB/ToolBench ；以仓库 LICENSE 为准 | NPC 调用游戏/外部工具能力的基准（F5、E10 成本） |
| **MindAgent（CUISINEWORLD）** | 多 NPC 协作 + 人机协作的规划/协调能力；新指标 CoS（协作得分） | 论文 https://arxiv.org/abs/2309.09971 ；主页 https://mindagent.github.io （NAACL 2024 Findings） | Macha 多智能体协作场景（F5）的直接参考；提供 CoS 度量范式 |
| **SmartPlay** | 6 款游戏（含 Minecraft、塔、剪刀石头布等）评估 9 项智能体能力；无限环境变化 | 论文 https://arxiv.org/abs/2310.01557 ；代码 https://github.com/LLMsmartplay/SmartPlay （论文标注）/ Microsoft/SmartPlay | 用"游戏"本身作为智能体能力探针（F5、F7 可预测性） |
| **Clembench** | 用对话游戏（Taboo、Wordle、Drawing 等）评估对话智能体；第三范式"对话博弈评估" | EMNLP 2023 https://aclanthology.org/2023.emnlp-main.689 ；2025 范式论文 https://arxiv.org/abs/2507.08491 ；框架 https://clembench.github.io | 以"游戏化交互"测对话能力（F6），且天然适配 NPC 场景；可复用到 Macha 的自测 |
| **LoCoMo** | 超长时程对话记忆（最长 35 会话/约 300 轮/9K token）；QA（单跳/多跳/时序/开放域/对抗）+ 事件摘要 + 多模态生成 | 论文 https://arxiv.org/abs/2402.17753 （ACL 2024）；代码/数据 https://github.com/snap-research/LoCoMo ；以仓库 LICENSE 为准 | Macha 记忆模块（F2、F4）最核心的对话记忆基准；对抗集直接测反幻觉 |
| **LongMemEval** | 长程交互记忆五维：信息提取、多会话推理、时序推理、知识更新、拒答；含 S（~115K token）与 M（~1.5M token）变体 | 主论文 arXiv 直链本次未核验；可经 ICLR 2025 论文集/项目页获取。综述参考：https://www.emergentmind.com/topics/longmemeval 、https://www.gamgee.ai/blogs/longmemeval-explained | "记忆是否指导行动"的关键补充；知识更新/拒答维度直击角色漂移（F2、F4）。**主链接待核验** |
| **MemoryArena** | 多会话、子任务强因果依赖的"记忆—智能体—环境"闭环；记忆必须来自过往行动并指导未来行动 | 论文 https://arxiv.org/abs/2602.16313 （2026-02，已核验） | 揭示"静态记忆测试高分 ≠ 真实可用"的差距（F2、F4、F5 闭环）；Macha 记忆-行动耦合评估的范本 |
| **LongBench** | 中英双语、6 大类（单/多文档 QA、摘要、少样本、合成、代码）长上下文理解 | 论文 https://arxiv.org/abs/2308.14508 ；数据/代码 https://github.com/THUDM/LongBench | 长上下文能力基线（F8）；含中文，利于中文 NPC 场景 |
| **RULER** | 合成可控长上下文基准：检索/多跳追踪/聚合/QA，支持任意长度与难度 | 论文 https://arxiv.org/abs/2404.06654 （COLM 2024）；代码 https://github.com/NVIDIA/RULER | 诊断 Macha"把记忆塞进上下文"的真实上限（F8），比 NIAH 更严格 |
| **PersonaChat** | 基于人设的多轮对话一致性与参与度 | 论文 https://arxiv.org/abs/1801.07243 ；数据 ParlAI / HuggingFace `persona-chat`（**CC BY 4.0**，非 MIT；商用需署名） | 角色一致性（F1）的入门级基准；可直接做一致性回归测试 |
| **LIGHT** | 大型奇幻文字冒险世界（663 地点/3462 物体/1755 角色），测"会说话也会行动"的 grounded dialogue | 论文 https://arxiv.org/abs/1903.03094 ；平台 https://parl.ai/projects/light （以仓库 LICENSE 为准） | NPC 在世界中"感知-说话-行动"的统一环境（F3、F6、F7）；最接近游戏 NPC 的研究平台 |
| **DSTC / MultiWOZ** | 任务型对话状态跟踪（DST）与多领域任务完成 | DSTC 系列 https://github.com/tranmduc/Awesome-Dialogue-State-Tracking ；MultiWOZ 等随各仓库发布 | NPC 作为"功能型对话者"（任务/交易/指引）的度量（F6）；DST 准确率可作为一致性代理指标 |
| **RoleLLM / RoleBench** | 细粒度角色扮演：CUS（风格一致）/RAW（角色准确与分寸）/SPE（角色知识） | 论文 https://arxiv.org/abs/2310.00746 ；ACL 2024 https://aclanthology.org/2024.findings-acl.878 ；数据 RoleBench（168,093 样本） | 角色一致性（F1）最系统的学术基准；提供"角色保真度"可量化定义 |
| **MT-Bench** | 多轮对话质量八维度（写作/角色扮演/推理/数学/代码/知识/抽取/STEM），GPT-4 判分 | 论文/代码 https://github.com/lm-sys/FastChat （MT-Bench 随仓库） | 对话质量（F6）快速回归；角色扮演维度可直接复用为 Macha 角色扮演评分 |

---

## 4. 来源收集（按约定格式）

> 每条遵循 `information_needs.md` 指定格式：
> 【类别】 / 【标题】 / 【链接/文件路径】 / 【一句话摘要】 / 【关键结论】 / 【可复用的东西】

---

【类别】学术论文 / 工程实现
【标题】AgentBench: Evaluating LLMs as Agents
【链接/文件路径】https://arxiv.org/abs/2308.03688 ；https://github.com/THUDM/AgentBench
【一句话摘要】首个系统性评估"LLM 作为智能体"的多维基准，覆盖 8 类真实环境。
【关键结论】
1. 现有 LLM 作为智能体的能力在长程推理、决策、指令遵循上仍是主要瓶颈。
2. 商业 API 模型显著强于开源模型，但距"可用"仍有明显差距。
3. 代码与高质量多轮对齐数据训练可提升 agent 表现。
4. 提供即插即用的评估工具包，可对任意 LLM 跑分。
【可复用的东西】评估包（8 环境）、leaderboard 方法、多环境任务成功率口径——可作 Macha 行动层基线。

---

【类别】学术论文 / 工程实现
【标题】WebArena: A Realistic Web Environment for Building Autonomous Agents
【链接/文件路径】https://arxiv.org/abs/2307.13854 ；https://webarena.dev
【一句话摘要】可自托管的真实 Web 环境，用程序化校验评估 agent 端到端任务成功率。
【关键结论】
1. 即便 GPT-4 端到端成功率仅 14.41%，远低于人类 78.24%。
2. 任务长程、需跨站点规划与推理。
3. 提供可复现的自托管环境与 812 个基准任务。
【可复用的东西】自托管环境搭建方式、功能正确性自动校验（programmatic validation）——可借鉴为 Macha 的"游戏环境自动评分"。

---

【类别】学术论文 / 工程实现
【标题】ToolLLM: Facilitating Large Language Models to Master 16000+ Real-world APIs（含 ToolBench）
【链接/文件路径】https://arxiv.org/abs/2307.16789 ；https://github.com/OpenBMB/ToolBench
【一句话摘要】构建 16,464 个真实 API 的工具使用指令数据集与评测器 ToolEval。
【关键结论】
1. 开源模型经 ToolBench 微调（ToolLLaMA）可达与 ChatGPT 相当的工具使用能力。
2. DFSDT（深度优先搜索决策树）显著提升复杂指令规划。
3. ToolEval 用通过率/胜率双指标自动评测。
【可复用的东西】API 检索器设计、自动评测器思路——Macha NPC 调用游戏/外部工具的评测可直接套用。

---

【类别】学术论文 / 工程实现
【标题】MindAgent: Emergent Gaming Interaction（含 CUISINEWORLD）
【链接/文件路径】https://arxiv.org/abs/2309.09971 ；https://mindagent.github.io
【一句话摘要】面向"多 NPC 协作 + 人机协作"的游戏交互评测基础设施，提出协作得分 CoS。
【关键结论】
1. 现有游戏框架缺乏"通用多智能体协作"基准。
2. 引入 CUISINEWORLD 场景与协作效率指标 CoS。
3. 可部署到 VR 版本与 Minecraft 域。
【可复用的东西】CoS 协作度量、记忆历史/动作模块接口设计——Macha 多智能体协作评估直接参考。

---

【类别】学术论文
【标题】SmartPlay: A Benchmark for LLMs as Intelligent Agents
【链接/文件路径】https://arxiv.org/abs/2310.01557 ；https://github.com/LLMsmartplay/SmartPlay
【一句话摘要】用 6 款游戏分拆出 9 项智能体能力，可逐项诊断短板。
【关键结论】
1. 每款游戏挑战 9 项能力的一个子集（对象依赖推理、前瞻规划、空间推理、从历史学习、随机性理解等）。
2. 提供统一可扩展 API，支持无限环境变化。
3. 既是基准也是方法论（能力分诊）。
【可复用的东西】"能力维度 × 游戏"映射法——Macha 可用同一思路把 NPC 能力拆成可测项。

---

【类别】学术论文 / 工程实现
【标题】clembench: Using Game Play to Evaluate Chat-Optimized LLMs as Conversational Agents
【链接/文件路径】EMNLP 2023 https://aclanthology.org/2023.emnlp-main.689 ；2025 范式论文 https://arxiv.org/abs/2507.08491 ；https://clembench.github.io
【一句话摘要】用约束性对话游戏（Taboo、Wordle 等）评测对话智能体，并提出"对话博弈评估"第三范式。
【关键结论】
1. 游戏化交互能在受控、可复现、多轮、无参考的条件下测目标导向对话。
2. 指标远未饱和，具持续诊断价值。
3. 2025 版 clembench 已优化为易复用框架，可自定义测试。
【可复用的东西】对话博弈评估框架与游戏实例——可改造成 Macha 的 NPC 对话自测小游戏。

---

【类别】学术论文
【标题】Evaluating Very Long-Term Conversational Memory of LLM Agents（LoCoMo）
【链接/文件路径】https://arxiv.org/abs/2402.17753 ；https://github.com/snap-research/LoCoMo
【一句话摘要】构建最长 35 会话的超长时程对话记忆基准，含五类问答 + 事件摘要 + 多模态生成。
【关键结论】
1. 长上下文与 RAG 有帮助，但远落后人类，尤其时序/多跳/对抗问题。
2. 对话经"LLM 生成 + 人工校验"，锚定时间事件图。
3. 公开 `locomo10.json`（约 10 段最长对话，~1540 QA）。
【可复用的东西】QA 五分类（单跳/多跳/时序/开放域/对抗）+ 事件图摘要任务——Macha 记忆评测的核心模板。

---

【类别】学术论文（综述待核验主链接）
【标题】LongMemEval: Benchmarking Chat Assistants on Long-Term Interactive Memory
【链接/文件路径】主论文 arXiv 直链本次未核验；综述参考 https://www.emergentmind.com/topics/longmemeval 与 https://www.gamgee.ai/blogs/longmemeval-explained （ICLR 2025，UCLA & Tencent AI Lab）
【一句话摘要】用 500 个问题在真实聊天史上系统测长程记忆五维（信息提取/多会话推理/时序/知识更新/拒答）。
【关键结论】
1. 长上下文 LLM 从 Oracle 到标准集有 30–60% 性能跌落（非长度问题，是注意力问题）。
2. 知识更新极易返回过时事实；即便检索完美，阅读理解仍会出错。
3. 提供 S（~115K）/M（~1.5M token）两档，M 超出多数上下文窗口，逼出真实记忆系统。
【可复用的东西】记忆五维定义与变体设计——Macha 反幻觉/知识更新压力测试的直接依据。

---

【类别】学术论文
【标题】MemoryArena: Benchmarking Agent Memory in Interdependent Multi-Session Agentic Tasks
【链接/文件路径】https://arxiv.org/abs/2602.16313 （2026-02，已核验）
【一句话摘要】在"记忆—智能体—环境"多会话闭环中评测记忆是否真的指导了未来行动。
【关键结论】
1. 现有基准把"记忆"与"行动"割裂；MemoryArena 强制子任务因果依赖。
2. 在 LoCoMo/LongMemEval 接近饱和的系统，在本基准任务完成率极低。
3. 平均每个任务 6.9 个互赖子环节、~57 个行动步骤、轨迹超 4 万 token。
【可复用的东西】"记忆-行动-环境"闭环评测结构、互赖子任务设计——Macha 端到端评估的范本。

---

【类别】学术论文
【标题】LongBench / RULER（长上下文理解基准）
【链接/文件路径】LongBench https://arxiv.org/abs/2308.14508 、https://github.com/THUDM/LongBench ；RULER https://arxiv.org/abs/2404.06654 、https://github.com/NVIDIA/RULER
【一句话摘要】LongBench 是首个中英双语长上下文多任务基准；RULER 是合成可控、比 NIAH 更严格的长上下文诊断。
【关键结论】
1. LongBench 含 21 数据集、6 大类、自动评测，含中文。
2. RULER 在 vanilla NIAH 上近乎满分，但多跳/聚合任务随长度急剧下降；仅约半数 32K 模型能维持满意表现。
3. RULER 支持任意长度/难度配置，便于压力测试。
【可复用的东西】长上下文评测任务族与配置方法——用于决定 Macha 记忆是"塞上下文"还是"外挂检索"。

---

【类别】学术论文 / 数据集
【标题】Personalizing Dialogue Agents: I have a dog, do you have pets too?（PersonaChat）
【链接/文件路径】https://arxiv.org/abs/1801.07243 ；HuggingFace `persona-chat`（MIT License）
【一句话摘要】用显式人设驱动多轮对话，评测角色一致性，是角色扮演研究的奠基数据集。
【关键结论】
1. 早期揭示"聊天模型缺乏一致人格与长期记忆"的问题。
2. 提供 persona-conditioned 生成与回复选择任务。
3. 衍生 DNLI 数据集把一致性判定转为自然语言推断。
【可复用的东西】人设驱动对话协议、一致性评测思路——Macha 角色一致性回归测试的起点。

---

【类别】学术论文 / 工程实现
【标题】Learning to Speak and Act in a Fantasy Text Adventure Game（LIGHT）
【链接/文件路径】https://arxiv.org/abs/1903.03094 ；https://parl.ai/projects/light
【一句话摘要】大型奇幻文字冒险世界，研究"会说话也会行动"的 grounded 对话。
【关键结论】
1. 663 地点/3462 物体/1755 角色，全自然语言描述，含对话与动作/情绪。
2. grounded（地点、物体、角色、过往动作）显著提升对话与行动预测。
3. 人类表现仍优于模型，说明 grounded 交互远未解决。
【可复用的东西】"世界状态 + 角色人设 + 对话/动作"统一环境——最接近游戏 NPC 的研究平台，可作 Macha 仿真沙盒。

---

【类别】学术论文 / 数据集
【标题】RoleLLM: Benchmarking, Eliciting, and Enhancing Role-Playing Abilities of LLMs（RoleBench）
【链接/文件路径】https://arxiv.org/abs/2310.00746 ；https://aclanthology.org/2024.findings-acl.878
【一句话摘要】首个细粒度角色级基准 RoleBench（168,093 样本），给出"角色保真度"可量化定义。
【关键结论】
1. 三指标：CUS（Lexical Consistency + Dialogic Fidelity）、RAW（准确性与分寸）、SPE（角色专属知识）。
2. 系统指令法优于检索增强，省上下文且更抗噪声。
3. 开源 RoleLLaMA 在风格/知识上可逼近 GPT-4 级 RoleGPT。
【可复用的东西】角色保真度的三指标定义——Macha F1 维度（角色一致性）的直接度量标准。

---

【类别】学术论文 / 方法论
【标题】Generative Agents 的人类评估与 TrueSkill 排名（含 TrueSkill 协议）
【链接/文件路径】生成式智能体论文 https://arxiv.org/abs/2304.03442 ；TrueSkill 人类评测说明 https://www.53ai.com/news/qianyanjishu/2024070161709.html ；Chatbot Arena 方法论 https://lumenfall.ai/arena/methodology
【一句话摘要】用 TrueSkill（贝叶斯技能评分，μ/σ 双参数）把人类配对排名转为可比较的区间分数。
【关键结论】
1. TrueSkill 是 Elo 的多人对局推广，天然支持不确定度建模（σ）。
2. Generative Agents 用 100 名评估者对 5 个条件排序，再以 TrueSkill 评分 + Kruskal-Wallis 检验显著性。
3. 排行榜常用 `Elo = 1000 + 10×(μ − 3σ)` 保守下界，避免少量胜场虚高。
【可复用的东西】TrueSkill 配对评估协议——Macha L3 玩家主观评测（可信度/可预测性）的标准化方法。

---

【类别】学术论文 / 设计理论
【标题】Breaking Players' expectations: the Role of NPCs' coherence and consistency（含 Believability 量表）
【链接/文件路径】https://arxiv.org/abs/2512.07388 （已核验）；Believability 维度源自 Paiva et al. 综述（fenix.tecnico.ulisboa.pt PDF）与 Gorman et al. believability index
【一句话摘要】在军事射击游戏中证实：NPC 的连贯/一致设计会强化玩家预期，反之挑战预期；并给出感知智能与可信度量表。
【关键结论】
1. 玩家对 NPC 的"感知智能"用五语义项量表（胜任/有知/负责/聪明/明智）测两个维度：可理解性 + 表现。
2. "可信度"用九维度李克特量表：觉知、行为可理解性、人格、视觉冲击、可预测性、行为一致性、经验变化、社会性、情绪表达。
3. 连贯一致的设计强化玩家预期；破坏一致性会显著影响评价。
【可复用的东西】可信度量表与"连贯性/一致性→玩家预期"框架——Macha F3/F7 主观评测问卷模板。

---

【类别】工程实现 / 产业工具
【标题】LangSmith（Agent 工程平台：可观测、评估、部署）
【链接/文件路径】https://www.langchain.com/ ；https://support.langchain.com/articles/8854797554-what-is-langsmith
【一句话摘要】框架无关的 agent 可观测与评估平台，用 trace 把每次运行拆成结构化步骤。
【关键结论】
1. 与任意框架/自研代码兼容，设一个环境变量即可接入追踪。
2. 提供 tracing、实时监控（成本/延迟/质量）、自动聚类相似对话、评估与部署。
3. 支持 OpenTelemetry，可自托管，承诺不拿客户数据训练。
【可复用的东西】trace 数据结构、成本/延迟看板思路——Macha E9/E10/E12 可观测性的参考实现。

---

【类别】工程实现 / 开源工具
【标题】Arize Phoenix（开源 LLM 可观测与评估，基于 OpenInference/OpenTelemetry）
【链接/文件路径】https://arize.com ；https://www.aiwisdom.dev/articles/ai-observability/phoenix
【一句话摘要】可本地/自托管的开源可观测与评估栈，原生 OTel，内置幻觉/QA/相关性等评估器。
【关键结论】
1. 用 OpenInference 语义约定（OTel gen_ai.* 超集），trace 可移植到任意 OTLP 后端。
2. 内置 HallucinationEvaluator / QAEvaluator / RelevanceEvaluator 等，评估分数回挂到 span。
3. Datasets + Experiments 支持"从失败 trace 萃取数据集 → 跑实验对比 prompt/模型 → 回归测试"。
【可复用的东西】评估器（幻觉/相关性/QA）+ 实验对比工作流——Macha E12/E13 反幻觉评估与回归测试的直接工具。

---

## 5. Macha 落地建议

### 5.1 反幻觉 / 长期一致性压力测试设计（Macha 专属）

把上述基准"翻译"为 Macha 能自动跑的压力测试，建议覆盖四类对抗：

1. **记忆对抗（源自 LoCoMo adversarial + LongMemEval Abstention）**：在长对话中埋设"陷阱问题"，诱导 NPC 编造未发生的事件；期望 NPC 返回"我不确定/没有该信息"而非幻觉。
2. **知识更新（源自 LongMemEval KU）**：同一事实在会话 1 与会话 N 给出矛盾版本（如"我哥哥叫 A"→"我哥哥叫 B"），测 NPC 是否采用最新值且不前后打架。
3. **时间错位（源自 LongMemEval TR + LoCoMo temporal）**：用相对时间词（"上周""明天下午"）提问，测 NPC 是否能锚定到正确会话时间。
4. **行动—记忆闭环（源自 MemoryArena）**：设计子任务强因果依赖的小游戏，NPC 必须在早期会话记住关键约束，才能正确完成后期任务；直接暴露"记得住但用不上"的伪记忆。

> 形式：每个压力测试产出**可量化分数 + 失败 trace**（用 Phoenix 记录），纳入 Macha 回归集。

### 5.2 工程指标埋点（延迟/成本/吞吐）

- 在 `Agent`（见 `src/macha/core/agent.py`）的感知→记忆→推理→行动各阶段打点，记录首字延迟、各阶段耗时、token 数。
- 通过 OpenTelemetry/OpenInference 把 trace 发给 LangSmith 或 Phoenix（任选，均框架无关）。
- 建立"记忆策略对照表"：同一 NPC 分别用（a）纯长上下文、（b）RAG、（c）Macha 外挂记忆，对比 F2/F4 分数与 E9/E10 成本，给出"何时该用记忆系统"的工程结论。

### 5.3 可解释性与可调试性

- **为什么玩家需要可预测 NPC**：NPC 行为熵过高会破坏可信度与"可玩性"（Paiva 的 predictability 维度）；过度随机或完全死板都会损害体验。
- **为什么开发者需要可调试 NPC**：LLM 非确定性使故障难定位。用 trace 把"哪次记忆检索命中、哪条反思被采纳、哪个工具调用失败"显式化，是 Macha 作为"标准骨架"必须提供的可观测底座。
- **建议**：Macha 默认导出 OpenInference 兼容 trace，使开发者可用 Phoenix 免费本地调试，企业可用 LangSmith 托管——两种路径都不锁定单一供应商。

### 5.4 评估与 Macha 架构的对应关系

| Macha 模块（architecture.md） | 主评测维度 | 推荐基准 |
|---|---|---|
| Memory | F2 长期记忆、F4 反幻觉 | LoCoMo、LongMemEval、MemoryArena、RULER |
| Reasoning / Reflection | F1 角色一致性、F5 规划 | RoleBench、AgentBench、SmartPlay |
| Perception / Action | F5 规划决策、F6 对话质量 | WebArena、MindAgent、LIGHT、MT-Bench |
| Character（人格层） | F1/F3/F7 一致性/可信/可预测 | RoleBench、Clembench、Believability 量表 |
| 工程/部署 | E9–E13 | 自建埋点 + LangSmith/Phoenix |

---

## 6. 待补充与待核验项

- **LongMemEval 主论文 arXiv 直链未核验**：已列二手综述链接，正式引用前请补全主论文出处（ICLR 2025 论文集/项目页）。
- **各数据集商用许可**：PersonaChat 实为 CC BY 4.0（非 MIT）；其余论文数据集随仓库发布，商用需逐条核对 LICENSE 与数据来源（尤其 LIGHT、LoCoMo 含人工标注与图像说明）。
- **中文 NPC 基准缺口**：现有角色扮演/记忆基准以英文为主；Macha 若主打中文市场，建议在 RoleBench（已含 5 个中文角色）与 LongBench（含中文）基础上，自建中文人设与对话记忆集。
- **玩家主观评估样本**：F3/F7 的 Believability 量表需配合真实玩家调研（建议结合 TrueSkill 配对评测，见第 4 节来源）。

---

## 7. 深化补充：评估 Harness 设计与量化 SLO

> **本章定位**：在不改动第 1–6 节框架（L1–L3 三层、F1–F13 维度）的前提下，补充四类深化内容——
> （A）广度+时效：2025–2026 一手新增基准与数据集规模；
> （B）Macha 评估 harness 设计规范（config schema + 评估器伪代码 + 量化 SLO）；
> （C）中文市场专项（SuperCLUE / FlagEval / OpenCompass / 中文角色一致性基准）；
> （D）量化落地（数据集规模数字表 + Macha v0.1 优先接入清单与达标门槛）。
>
> **来源可信度说明**：本章新增链接均经 WebSearch/WebFetch 实际获取；标记为"（待核验）"的为主论文 arXiv 直链或官网未在本轮逐一打开核验，正式引用前请补全。其余项目页/代码仓库/榜单均来自可访问页面。

### 7.1 广度 + 时效：2025–2026 关键新增基准

以下基准填补了原文档"agent 长效交互一致性""游戏世界 grounded NPC""长上下文深度推理""中文角色一致性"四块空白，按原第 3 节口径登记，并补齐**数据集规模数字**（见 7.4 规模表）。

| 名称 | 度量内容 | 年份/会议 | 与 Macha 的关联（维度） |
|---|---|---|---|
| **τ-bench / τ²-bench / τ³-bench** | 工具-智能体-用户多轮动态交互、领域规则遵循、一致性（pass^k 可靠性指标） | 2024 / ICLR 2025（τ² 2025、τ³ 2026） | 测 NPC"客服/任务型对话"的**一致性危机**（F1/F6/E13）；pass^k 直接映射到 Macha 回归稳定性 |
| **OSWorld / OSWorld-Verified** | 真实 OS（Ubuntu/Win/macOS）上执行式评分的多模态 agent | NeurIPS 2024，2025 升级 | "游戏环境自动评分"工程范本（F5/F6/E12）；执行式状态校验可复用到 Macha 世界动作 |
| **GAIA / GAIA 2** | 466 道多步骤、需推理+多模态+网页+工具的通用助手任务（答案唯一可判分） | 2023 / ICLR 2024；GAIA 2 动态环境升级 | 任务型 NPC 评测对照（F5/F6）；难度分级启示 Macha 阶梯式压测 |
| **MemBench** | 事实+反思记忆、参与+观察双场景、四指标（准确性/召回/容量/效率） | ACL 2025 | Macha 记忆模块（M/F2）的**更细粒度**框架：补"反思记忆""观察场景""容量/效率" |
| **LongBench v2** | 503 道深度理解推理长上下文多选，8k–2M 词，6 大类 20 子任务 | ACL 2025 | F8 长上下文"真理解 vs 检索"决策依据；长对话历史理解子任务直击 Macha |
| **FRAMES** | 824 道跨 2–15 篇维基的多跳 RAG 问答，统一测事实性/检索/推理 | NAACL 2025 | Macha 记忆检索（M）+ 反幻觉（F4）的端到端压力测试模板 |
| **GRUtopia / GRBench** | 具身小镇仿真 + 大模型 NPC（GRResidents）+ 三档具身评测 | 2024（arXiv 待核验） | 游戏世界 grounded NPC 仿真沙盒（F3/F5/F6）；"描述/定位/对话/任务分配"四能力 |
| **SuperCLUE-Role** | 中文原生角色扮演：基础能力+演绎力+场景应用（含游戏 NPC 子榜） | 2024（CLUEbenchmarks） | Macha F1/F3 中文落地对标；明确把"游戏 NPC"列为场景 |
| **CharacterEval** | 中文角色扮演对话代理：1785 对话/23020 示例/77 角色/13 指标/4 维 | ACL 2024 | Macha F1 中文自动评分器（CharacterRM）直接工具 |
| **CPDC 2025** | 游戏 NPC"常识人设锚定对话"挑战：任务导向/上下文感知/融合 | 2025 竞赛 | "任务保真 vs 角色沉浸"双目标权衡范式（F1/F5） |

---

### 7.2 Macha 评估 Harness 设计规范

#### 7.2.1 (a) 一次 benchmark run 的 YAML / JSON config schema

> 设计原则：一次 run = 「一个 NPC 后端 × 一种记忆策略 × 一套场景集 × 一组评分器 × 一组 SLO」。config 可被 CI 直接消费，亦可由 Phoenix/LangSmith 回放。

```yaml
# macha_eval_run.yaml  —— Macha v0.1 评估运行配置
benchmark_run:
  meta:
    name: macha-v0.1-eval
    version: 0.1.0
    run_id: auto            # 由 harness 注入，便于回归追踪

  model:
    npc_backend: openai/gpt-4o-mini   # 被测 NPC 的生成后端
    memory: macha-external            # none | long-context | rag | macha-external
    temperature: 0.3
    max_tokens: 512

  suite:                     # 场景集：每个 scenario 声明它要打哪些维度(L1..L13 子集)
    - id: locomo-10
      type: long_term_memory
      path: data/locomo10.json
      dims: [F2, F4]                 # 长期记忆稳定性 / 反幻觉
      scoring: qa_f1
    - id: longmemeval-s
      type: long_term_memory
      path: data/longmemeval_s.json
      dims: [F2, F4]
      scoring: subset_accuracy
    - id: rolebench-cus
      type: role_fidelity
      path: data/rolebench
      dims: [F1]                     # 角色一致性
      scoring: cus_raw_spe
    - id: superclue-role-game-npc
      type: role_fidelity_zh
      path: data/superclue_role
      dims: [F1, F3]                 # 中文角色一致性 / 可信度
      scoring: characterrm
    - id: charactereval-zh
      type: role_fidelity_zh
      path: data/charactereval
      dims: [F1]
      scoring: characterrm
    - id: macha-adversarial-trap     # 自建反幻觉压力测试（见 5.1）
      type: anti_hallucination
      path: data/macha_traps.json
      dims: [F4]
      scoring: abstention_rate

  scorer:                    # 评分器：与 dims 一一对应
    role_consistency:
      method: llm_judge            # 或 characterrm / dnli
      judge_model: gpt-4o
      threshold: 0.85
    hallucination:
      method: abstention_rate      # 陷阱题应显式拒答而非编造
      threshold: 0.02
    memory_qa:
      method: qa_f1

  slo:                       # 量化 SLO（详见 7.3）
    latency_p95_ms: 800
    cost_per_turn_usd: 0.002
    throughput_turn_per_s: 15
    role_fidelity_min: 0.85
    hallucination_max: 0.02
    memory_f2_min: 0.80

  reporting:
    trace_backend: phoenix        # langsmith | phoenix
    export: openinference         # 与 OTel 兼容，供应商无关
    regression_baseline: results/macha-v0.0.9.json
```

#### 7.2.2 (b) 参考评估器伪代码

```python
def run_suite(npc, suite, scorer, dims=L1_to_L13):
    """一次完整 benchmark run：遍历场景集，对每个 scenario 跑 NPC 并评分。

    npc     : Macha NPC 运行时（含 memory 模块），需实现 reset()/run()
    suite   : 场景集（来自 config.suite）
    scorer  : 评分器集合（config.scorer）
    dims    : 评估维度全集 L1..L13；每个 scenario 只评其声明子集
    """
    report = EvalReport(run_id=auto_id())

    for scenario in suite:
        npc.reset(memory=scenario.seed_memory)     # 注入初始记忆/人设
        transcript = []

        for turn in scenario.turns:
            # —— NPC 推理 + 工程埋点 ——
            npc_output = npc.run(turn.user_input, ctx=scenario.context)
            transcript.append((turn, npc_output))

            # E9/E10：延迟与成本实时采集
            report.latency.record(npc_output.latency_ms)
            report.cost.record(npc_output.cost_usd)
            # E12：导出 OpenInference 兼容 trace，可 Phoenix/LangSmith 回放
            emit_trace(openinference_span(scenario, turn, npc_output))

        # —— 功能评分：scorer 只评 scenario.dims 声明维度（L1..L13 子集）——
        scores = scorer(
            npc_output=transcript,
            expected=scenario.expected,
            dims=scenario.dims,            # 例如 [F2, F4] 或 [F1, F3]
        )
        report.scores.merge(scores)

        # F4：对抗/拒答专项——陷阱题必须拒答而非幻觉
        if scenario.has_trap:
            report.hallucination += scorer.abstention(transcript)

        # E13：与回归基线对比，记录质量波动
        report.delta_vs(report.regression_baseline)

    # —— 收口：断言 SLO，输出达标/未达标报告 ——
    return report.assert_slo(SLO)


# 评分器内部分派示例（维度 → 度量）
def scorer(npc_output, expected, dims):
    out = {}
    if F1 in dims:   out[F1] = role_consistency_judge(npc_output, expected)   # 角色一致性
    if F2 in dims:   out[F2] = memory_qa_f1(npc_output, expected)            # 长期记忆
    if F3 in dims:   out[F3] = believability_survey(npc_output, expected)    # 可信度(可抽样子集)
    if F4 in dims:   out[F4] = abstention_rate(npc_output, expected)         # 反幻觉
    if F5 in dims:   out[F5] = task_success_rate(npc_output, expected)       # 规划决策
    if F6 in dims:   out[F6] = mtbench_style_judge(npc_output, expected)     # 对话质量
    # F7/F8、E9..E13 由 harness 在 transcript/trace 层直接计算
    return out
```

> 要点：① `dims` 让同一 NPC 运行时可被不同场景复用、只算相关维度，避免"全量重跑"；② 工程维度（E9–E12）在 `emit_trace`/埋点层自动累积，不进入 `scorer` 主观判分；③ `assert_slo` 让 run 在 CI 中红/绿，支撑 E13 持续回归。

#### 7.2.3 (c) 量化 SLO 目标（明确数字）

> 以下为 **Macha v0.1 推荐 SLO**。工程维度取自第 2 节 E9–E13；功能维度锚定 F1/F2/F4。数字为"在线游戏 NPC"硬约束下的初版目标，后续以实测基线修订。

| SLO 项 | 指标 | 目标值 | 对应维度 | 说明 |
|---|---|---|---|---|
| 回合延迟 | p95 端到端（首字→末字） | **< 800 ms** | E9 | 实时对话硬约束；纯长上下文策略更易达标，外挂记忆需控制检索耗时 |
| 单轮成本 | token + 工具调用成本 | **< $0.002 / turn** | E10 | 以 gpt-4o-mini 量级估算；外挂记忆 vs 长上下文经济性权衡见 5.2 |
| 吞吐 | 单实例处理速率 | **> 15 turn/s** | E11 | 开放世界多 NPC 并发；另设并发会话 > 50 为规模化门槛 |
| 角色一致性 | 加权一致性（CharacterRM/CUS 风格） | **> 0.85** | F1 | 中文用 SuperCLUE-Role/CharacterEval 对标；低于此值视为"角色漂移" |
| 幻觉率 | 陷阱题幻觉占比（应拒答却编造） | **< 2%** | F4 | 来自 5.1 反幻觉压力测试；高于此值触发告警 |
| 长期记忆准确率 | LoCoMo 多跳 QA F1 | **> 0.80** | F2 | 记忆模块（M）核心承诺；LongMemEval 五维总体 > 0.75 |
| 一致性可靠性 | 同场景 pass^k（k=3） | **> 0.70** | E13/F1 | 借 τ-bench pass^k 思路：同一任务多次运行须稳定达标 |
| 可观测覆盖 | trace 导出覆盖率 | **100%** | E12 | 每回合均导出 OpenInference span，可 Phoenix 本地调试 |
| 回归稳定 | 固定集质量波动（相对上一版） | **< 3%** | E13 | 每次 PR 跑固定集，任一维度跌幅超阈值即阻断合并 |

---

### 7.3 中文市场专项：国产评测体系深度

Macha 若主打中文游戏市场，不能只依赖英文基准（LoCoMo/RoleBench/LIGHT）。国产评测体系在**中文角色一致性**与**工程可落地性**上已自成体系，且明确覆盖"游戏 NPC"场景。

**（1）SuperCLUE / SuperCLUE-Role（中文综合性 + 角色扮演专项）**
- 归属：CLUEbenchmarks 团队（ChineseCLUE 延续）。SuperCLUE 综合榜覆盖基础能力/专业能力/中文特性，含角色扮演、Agent、长文本、安全等专项。
- 关键价值：`SuperCLUE-Role` 是**中文原生**角色扮演基准，两大核心维度——「角色基础能力（对话能力/知识掌握）+ 角色演绎力（语言风格/行为习惯）+ 场景应用（情感陪伴/游戏 NPC）」。它**明确把"游戏 NPC"列为核心应用场景之一**，与 Macha 定位直接契合。
- 实测启示（来自其发布报告）：① 中文模型（qwen1.5-72b、文心一言 4.0）在角色扮演上可超 GPT-4；② **非常规问题对齐能力骤降**；③ **多轮效果随轮数普遍衰减**——这正是 Macha 长程一致性（F1）要解决的问题，可作为"衰减曲线"对照基线。

**（2）CharacterEval（最系统的中文角色扮演学术基准）**
- 规模：1,785 多轮对话、23,020 示例、77 个中文小说/剧本角色；GPT-4 抽取 + 人工质控 + 百度百科画像。
- 度量：4 维度 13（论文亦述 16）指标；配套 **CharacterRM** 角色扮演奖励模型，与人工相关性显著超 GPT-4。
- 对 Macha 的可复用性：CharacterRM 可直接作为 Macha F1 中文自动评分器（替代或校准 LLM-judge），避免英文 judge 在中文角色上的偏差。

**（3）OpenCompass（司南）与 FlagEval（天秤）——工程底座**
- OpenCompass（上海 AI 实验室）：开源评测体系，含 CompassKit/CompassHub/CompassRank，已集成大量开源与闭源 API，对语言模型考察语言/知识/推理/数学/代码/**智能体**。Macha 可用其做"中文模型选型 + 持续回归"。
- FlagEval（北京智源研究院）："能力-任务-指标"三维框架，近 30 数据集、超 10 万题，中英文主客观题；2024 下半年扩展工具调用/高级编程/金融量化，并推出"大模型角斗场"（盲测对战）。其"动态评测 + 多任务"方向（2025 规划）与 Macha E13 回归理念一致。
- 两者均为**开源、供应商无关**，契合 Macha"可调试、不锁定"的工程哲学（见 5.3）。

**（4）中文 NPC 落地建议（补充原第 6 节缺口）**
- 在 RoleBench（已含 5 个中文角色）+ LongBench（含中文）基础上，**以 SuperCLUE-Role 游戏 NPC 子集 + CharacterEval 为中文主评测**；
- 自建中文人设与对话记忆集时，复用 CharacterEval 的"角色画像 + 多轮对话 + 人工质控"流水线；
- 玩家主观评估（F3/F7）结合 SuperCLUE 琅琊榜式**盲测对战**与 TrueSkill 配对（见第 4 节来源），形成"客观指标 + 主观对战"双轨。

---

### 7.4 量化与落地：数据集规模数字 + v0.1 优先接入清单

#### 7.4.1 各基准数据集规模数字（汇总）

| 基准 | 规模数字（可量化） | 年份/会议 | 许可/访问 |
|---|---|---|---|
| τ-bench | 165 tasks（115 retail + 50 airline） | 2024 / ICLR 2025 | MIT；GitHub sierra-research/tau-bench |
| OSWorld | 369 tasks + 43 Windows tasks | NeurIPS 2024 | 项目页 os-world.github.io |
| GAIA | 466 题（验证 166 + 测试 300） | 2023 / ICLR 2024 | HF 排行榜（测试集答案隐藏） |
| MemBench | 500 用户画像；51k 参与式 + 8.5k 观察式会话；两档 10k/100k token | ACL 2025 | arXiv:2506.21605 |
| LongBench v2 | 503 道多选；上下文 8k–2M 词；6 大类 20 子任务 | ACL 2025 | 项目 longbench2.github.io |
| LongBench | 21 数据集、6 大类（含中文） | 2023 | GitHub THUDM/LongBench |
| RULER | 合成可控（长度/难度可调） | COLM 2024 | GitHub NVIDIA/RULER |
| LoCoMo | 最长 35 会话 / ≈300 轮 / 9K token；locomo10 ≈ 1540 QA | ACL 2024 | GitHub snap-research/LoCoMo |
| LongMemEval | 500 Q；S≈115K / M≈1.5M token | ICLR 2025 | 主论文直链待核验 |
| MemoryArena | 平均 6.9 互赖子环节 / 任务；~57 行动步；轨迹 >4 万 token | 2026-02 | arXiv:2602.16313 |
| SuperCLUE-Role | 中文角色扮演多任务（含游戏 NPC 子榜） | 2024 | GitHub CLUEbenchmark/SuperCLUE-Role |
| CharacterEval | 1,785 对话 / 23,020 示例 / 77 角色 / 13 指标 4 维 | ACL 2024 | GitHub morecry/CharacterEval |
| FRAMES | 824 题；跨 2–15 篇维基；5 类推理 | NAACL 2025 | HF google/frames-benchmark（Apache-2.0） |
| RoleBench | 168,093 样本 | ACL 2024 | 随论文仓库 |
| PersonaChat | 人设对话集（CC BY 4.0，需署名） | 2018 | HuggingFace persona-chat |
| LIGHT | 663 地点 / 3462 物体 / 1755 角色 | 2019 | ParlAI LIGHT |

#### 7.4.2 Macha v0.1 优先接入清单与达标门槛

**Tier 1 — 必接（证明"标准骨架"核心承诺：记得住、说得像、不胡说）**

| 基准 | 维度 | 达标门槛（v0.1） |
|---|---|---|
| LoCoMo（locomo10） | F2/F4 | 多跳 QA F1 > 0.80；对抗/拒答子项幻觉率 < 5% |
| LongMemEval（S 档） | F2/F4 | 五维总体 > 0.75；知识更新 + 拒答子项 > 0.70 |
| SuperCLUE-Role（游戏 NPC 子集） | F1/F3（中文） | 角色一致性评分 > 0.80 |
| CharacterEval（中文） | F1（中文） | 四维度加权 > 0.78（或以 CharacterRM 相关性为据） |
| 自建反幻觉压力测试（5.1） | F4 | 陷阱题幻觉率 < 2%（对齐 SLO） |

**Tier 2 — 必接（工程性 SLO，决定能否上线）**

| 维度 | 门槛 |
|---|---|
| E9 延迟 | p95 < 800 ms |
| E10 成本 | < $0.002 / turn |
| E11 吞吐 | > 15 turn/s（单实例）/ > 50 并发会话 |
| E12 可观测 | trace 覆盖率 100%（OpenInference） |
| E13 回归 | 固定集每 PR 跑，质量波动 < 3%；pass^3 > 0.70 |

**Tier 3 — 扩展（v0.2+，能力广度与游戏 grounded）**

| 基准 | 维度 | 备注门槛 |
|---|---|---|
| AgentBench / τ-bench | F5 | 任务成功率对齐所选 baseline；τ-bench 关注 pass^k 一致性 |
| OSWorld / WebArena | F5/F6 | 执行式评分；先以子集（如 50 任务）跑通 |
| MemBench | F2（细粒度） | 100k token 下反思记忆 > 0.70 |
| LongBench v2 / RULER | F8 | 长上下文深度推理达标；决定"塞上下文 vs 外挂检索" |
| FRAMES | F4/M | 多步检索 + 推理准确率 > 0.60 |
| GRBench / GRUtopia | F3/F5/F6 | 游戏世界 grounded NPC 仿真沙盒（描述/定位/对话/任务分配） |

> **接入顺序建议**：先 Tier 1 + Tier 2（约 1 个迭代周期跑通 harness 与 SLO 红/绿），再按资源逐步扩 Tier 3。每次接入新基准都写入 `macha_eval_run.yaml` 的 `suite`，并扩展 `scorer` 的维度分派，保持 L1–L13 框架不变。

---

### 7.5 新增来源收集（按约定六字段格式）

---

【类别】学术论文 / 工程实现
【标题】τ-bench: A Benchmark for Tool-Agent-User Interaction in Real-World Domains（含 τ²-bench、τ³-bench）
【链接/文件路径】arXiv:2406.12045（主论文，待核验）；官方 https://taubench.com ；代码 https://github.com/sierra-research/tau-bench（历史版）/ https://github.com/deephyper/tau-bench
【一句话摘要】首个测"工具-智能体-用户"多轮动态交互与规则遵循一致性的 agent 基准，提出 pass^k 可靠性指标。
【关键结论】
1. 165 个任务（115 零售 + 50 航空），以数据库终态比对评分；GPT-4o pass^1<50%、retail pass^8<25%。
2. 揭示"一致性危机"：同一任务多次运行结果波动巨大，pass^k 比单次通过率更能反映部署可靠性。
3. 2025 τ²-bench 增双控电信域；2026 τ³-bench 增语音双工、知识密集银行域、任务审计修正。
4. 领域规则遵循脆弱：航空域移除规则文档性能暴跌 22.4%。
【可复用的东西】pass^k 可靠性指标、数据库终态比对评测、多轮交互协议——Macha NPC 客服/任务型对话"一致性"量化直接借鉴（E13/F1）。

---

【类别】学术论文 / 工程实现
【标题】OSWorld: Benchmarking Multimodal Agents for Open-Ended Tasks in Real Computer Environments
【链接/文件路径】项目页 https://os-world.github.io （NeurIPS 2024）；OSWorld 2.0 / OSWorld-Verified 2025 升级；arXiv 主论文待核验
【一句话摘要】首个在真实 OS（Ubuntu/Windows/macOS）上运行、执行式评分的多模态 agent 基准，369 真实任务。
【关键结论】
1. 369 个真实计算机任务（跨 Chrome/LibreOffice/VS Code 等 9 类应用）+ 43 个 Windows 任务；人类基线 72.36%，最佳模型初版仅 12.24%。
2. 2025-10 OSAgent 达 76.26% 首超人类，靠"验证-生成"闭环 + 大规模 RL。
3. 暴露 GUI grounding 与操作知识短板；约 15% 任务可纯终端完成（混合能力）。
【可复用的东西】执行式（execution-based）状态校验评测法、可并行自托管环境——Macha"游戏环境自动评分"（F5/F6/E12）的工程范本。

---

【类别】学术论文 / 产业报告
【标题】GAIA: A Benchmark for General AI Assistants（含 GAIA 2 动态环境版）
【链接/文件路径】arXiv:2311.12983（主论文，待核验）；HF 排行榜 https://huggingface.co/spaces/gaia-benchmark/leaderboard ；Princeton HAL 对照榜
【一句话摘要】466 道多步骤、需推理+多模态+网页浏览+工具使用的通用助手基准，答案唯一可自动判分。
【关键结论】
1. 466 题（验证集 166 + 测试集 300），分 L1/L2/L3 三难度；发布时 GPT-4+插件仅 15%，人类 92%。
2. 2025 顶尖系统逼近 65–87%（测试集），2026 初出现 >90% 提交；Level 3 最说明问题。
3. 公开验证集已被广泛"记住"，应更看重私有测试集成绩；GAIA 2 引入动态环境/时间约束/A2A 协作。
【可复用的东西】唯一答案 + 自动判分的多步骤任务设计、难度分级——Macha 任务型 NPC 评测（F5/F6）对照参考。

---

【类别】学术论文
【标题】MemBench: Towards More Comprehensive Evaluation on the Memory of LLM-based Agents
【链接/文件路径】arXiv:2506.21605（ACL 2025）；项目/数据待核验
【一句话摘要】首个覆盖"事实+反思"记忆、参与+观察双场景、四指标（准确性/召回/容量/效率）的 agent 记忆基准。
【关键结论】
1. 基于用户关系图生成 500 用户画像、51k 参与式事实会话 + 8.5k 观察式会话，含反思对应集；两档子数据集约 10k / 100k token。
2. 100k token 下反思记忆崩溃：GenerativeAgent/MemGPT 从 ~0.74 跌至 0.33–0.36；RetrievalMemory 最稳（参与 0.833、观察 0.933）。
3. 复杂记忆机制读写延迟高：MemGPT 读 ~4.5s、MemoryBank 写 8–18s，实时应用 prohibitive。
【可复用的东西】"事实+反思"记忆分级、参与/观察场景分离、容量与效率指标——Macha 记忆模块（M/F2）评测的更细粒度框架。

---

【类别】学术论文
【标题】LongBench v2: Towards Deeper Understanding and Reasoning on Realistic Long-context Multitasks
【链接/文件路径】arXiv:2412.15204（ACL 2025）；项目 https://longbench2.github.io
【一句话摘要】503 道需深度理解推理的长上下文多选问答，上下文 8k–2M 词，覆盖 6 大类 20 子任务。
【关键结论】
1. 503 题、6 大类（单/多文档 QA、长 ICL、长对话历史、代码库、长结构化数据），由近 100 位高学历标注者构建。
2. 人类专家 15 分钟限时仅 53.7%；最佳直接回答 50.1%，o1-preview 57.7% 首超人类 4%。
3. 证明"长窗口≠真理解"，推理与 inference-time compute 是关键。
【可复用的东西】长对话历史理解子任务、深度推理评测口径——Macha F8 长上下文与"塞记忆 vs 外挂检索"决策依据。

---

【类别】学术论文 / 数据集
【标题】FRAMES: Factuality, Retrieval, And reasoning MEasurement Set（检索增强生成统一评测）
【链接/文件路径】arXiv:2409.12941（NAACL 2025）；数据集 https://huggingface.co/datasets/google/frames-benchmark （Apache-2.0）
【一句话摘要】824 道需跨 2–15 篇维基的多跳 RAG 问答，统一测事实性/检索/推理。
【关键结论】
1. 824 题，标注 5 类推理（数值/表格/多约束/时序/后处理）；无检索 0.40，多步检索 0.66，Oracle 0.73。
2. 揭示"推理鸿沟"：即便给足 Oracle 文档，最强模型也仅 ~73%，RAG 失败不全是检索问题。
3. 迭代式检索规划近乎翻倍提升——对 Macha 记忆检索设计有直接启示。
【可复用的东西】端到端 RAG 评测口径、多跳推理分类——Macha 记忆检索（M）+ 反幻觉（F4）压力测试模板。

---

【类别】学术论文 / 工程实现
【标题】GRUtopia: Dreamland of Embodied Agents（含 GRResidents NPC 系统与 GRBench）
【链接/文件路径】arXiv:2407.10943（主论文，待核验）；代码 https://github.com/openrobotlab/grutopia
【一句话摘要】上海 AI Lab 的具身小镇仿真，含大模型驱动 NPC（GRResidents）与三档具身评测 GRBench。
【关键结论】
1. GRResidents NPC 能推断物体空间关系、参与动态对话与任务分配；物体描述/定位准确率经人机交叉验证不错。
2. GRBench 三档递增：目标定位导航、社交定位导航、定位操作；大模型后端整体优于随机策略。
3. Qwen-VL 在对话上超过 GPT-4o——多模态 NPC 潜力。
【可复用的东西】"NPC 描述/定位/对话/任务分配"四能力评测、具身仿真环境——Macha 游戏世界 grounded NPC（F3/F5/F6）仿真沙盒参考。

---

【类别】产业报告 / 数据集
【标题】SuperCLUE-Role：中文角色扮演测评基准（含游戏 NPC 场景）
【链接/文件路径】项目 https://github.com/CLUEbenchmark/SuperCLUE-Role ；榜单页 www.CLUEbenchmarks.com/superclue_role.html
【一句话摘要】中文原生角色扮演基准，覆盖"角色基础能力（对话/知识）+ 角色演绎力（语言风格/行为习惯）+ 场景应用（情感陪伴/游戏 NPC）"。
【关键结论】
1. 两大核心维度、细粒度多标准评分；明确将"游戏 NPC"列为核心应用场景之一。
2. 中文模型（qwen1.5-72b、文心一言 4.0）在角色扮演上可超 GPT-4；但非常规问题对齐能力骤降。
3. 多轮效果随轮数普遍衰减——直击 Macha 长程一致性（F1）痛点，可作"衰减曲线"对照基线。
【可复用的东西】中文角色扮演四维评分体系、游戏 NPC 应用子榜——Macha F1/F3 中文落地对标基准。

---

【类别】学术论文 / 数据集
【标题】CharacterEval: A Chinese Benchmark for Role-Playing Conversational Agent Evaluation
【链接/文件路径】arXiv:2401.01275（ACL 2024）；代码/数据 https://github.com/morecry/CharacterEval
【一句话摘要】中文角色扮演对话代理基准，1785 多轮对话、23020 示例、77 个小说/剧本角色，13 指标 4 维度，含 CharacterRM 奖励模型。
【关键结论】
1. 1,785 多轮对话、23,020 示例、77 个中文角色（小说/剧本），GPT-4 抽取 + 人工质控 + 百度百科画像。
2. 4 维度 13（论文亦述 16）指标；CharacterRM 与人工相关性显著超 GPT-4。
3. 实验显示中文 LLM 在中文角色扮演上优于 GPT-4。
【可复用的东西】中文角色画像 + 奖励模型 CharacterRM、四维度度量——Macha 中文角色一致性（F1）自动评分器直接工具。

---

【类别】学术论文 / 竞赛
【标题】Commonsense Persona-Grounded Dialogue Challenge (CPDC) 2025（游戏 NPC 对话）
【链接/文件路径】竞赛主页（待核验）；参与报告汇编见 https://www.chatpaper.ai （具体赛道页待核验）
【一句话摘要】面向游戏 NPC 的"常识人设锚定对话"挑战，分任务导向/上下文感知/二者融合三赛道。
【关键结论】
1. 评测 agent 在"功能任务执行"与"人设一致对话"间的权衡（Deflanderization：抑制过度角色扮演以保任务保真）。
2. 顶尖方案结合轻量 prompting（API track）与 Qwen3-14B SFT+LoRA（GPU track）。
3. 揭示游戏 NPC 真实矛盾：角色沉浸感 vs 任务完成度需显式平衡。
【可复用的东西】"任务保真 vs 角色沉浸"双目标评测框架——Macha F1/F5 权衡的现成范式。

---

【类别】工程实现 / 产业工具
【标题】OpenCompass（司南）与 FlagEval（天秤）中文大模型评测体系
【链接/文件路径】OpenCompass https://opencompass.org.cn ；FlagEval 平台（北京智源研究院，官网待核验）；报道 https://www.stdaily.com/web/gdxw/2024-12/19/content_276198.html
【一句话摘要】两大国产开源评测体系：OpenCompass 覆盖语言/知识/推理/数学/代码/智能体；FlagEval 以"能力-任务-指标"三维框架、近 30 数据集超 10 万题。
【关键结论】
1. OpenCompass 含 CompassKit/CompassHub/CompassRank，已集成大量开源与闭源 API，产业影响大。
2. FlagEval 2024 下半年扩展工具调用/高级编程/金融量化等，推出大模型角斗场（盲测对战）。
3. 二者均支持中文主客观题，是 Macha 中文模型选型与持续回归的底座，且均开源、供应商无关。
【可复用的东西】开源评测工具链与榜单方法、Agent 评测维度——Macha 中文模型接入与回归测试（E13）现成平台。
