# Macha 可用数据集清单 + 许可说明

> 类别编号：8. 数据资源（Data Resources）
> 定位：Macha 是**游戏 NPC 领域的标准骨架**，本文档为该骨架提供**训练 / 微调 / 评估**所需的、许可清晰的中文优先数据资源清单。
> 配套文档：本清单的"基准/评估"视角请与 `research/evaluation_benchmarks.md` 协同阅读（本文在第七章登记了与它的衔接与去重）。
> 许可原则：所有许可均以**数据/代码仓库实际 LICENSE 文件**为准；凡无法确认之处，明确标注"以仓库 LICENSE 为准"，不做臆测。涉及第三方 IP（小说、剧本、游戏、玩家数据）的，单列风险。

---

## 0. 阅读指南：Macha 如何使用这份清单

Macha 标准骨架的 NPC 能力可粗略拆为四块，本文档的数据集按用途映射到这四块：

| Macha 能力模块 | 含义 | 对应的数据用途 |
|---|---|---|
| **C（Character / 人设）** | 角色一致性、人格、知识背景 | 微调 / 评估角色扮演 |
| **M（Memory / 记忆）** | 长期记忆、跨会话一致、反幻觉 | 评估（见 evaluation_benchmarks.md） |
| **P（Perception-Action / 感知-行动）** | 在世界中"看-说-做"、规划决策 | 游戏/文本冒险语料、世界模型 |
| **D（Dialogue / 对话）** | 基础对话质量、多轮连贯 | 通用对话语料（预训练/对齐） |

本文档第 1 节的"与 Macha 的用途"列即按 `训练 / 微调 / 评估 / 不适用` 标记，并在括号内注明模块。

---

## 1. 精选数据集清单

> 规模与许可已尽可能在 2026-08 核实。带 `⚠` 的条目表示存在**许可或 IP 风险**，详见第 3 节。

### 1.1 对话 / 角色扮演（英文为主）

| 名称 | 内容类型 | 规模 | 访问方式 | 许可 | 与 Macha 的用途 |
|---|---|---|---|---|---|
| **PersonaChat / ConvAI2** | 基于人设的多轮对话（每角色 3–5 句人设） | ~1.6 万会话（ParlAI）；人设约 1.8 万 | ParlAI / HuggingFace `persona-chat` | 数据文档 **CC BY 4.0**；ParlAI 代码 MIT（见第 3 节勘误） | 微调/评估（C、D）：角色一致性入门基准，可作 OOC（出戏）回归测试 |
| **DailyDialog** | 日常开放域多轮对话（情感/话题标注） | 1.3 万对话 / 10.2 万句 | HuggingFace `daily_dialog` / ParlAI | **CC BY-NC-SA 4.0**（研究仅用） | 微调/评估（D）：基础对话质量、多轮连贯 |
| **LIGHT** | 大型奇幻文字冒险世界 + grounded dialogue（地点/物体/角色/动作） | 663 地点 / 3462 物体 / 1755 角色；~1.1 万训练对话 | ParlAI `light` 平台 https://parl.ai/projects/light/ | 数据随 ParlAI 发布，以仓库 LICENSE 为准（代码 MIT） | 评估（C、P、D）：最接近"NPC 在世界中说话+行动"的研究平台 |
| **CharacterGLM / CharacterDial**（清华 CoAI） | 中文角色对话语料（属性+行为人设） | 公开 **1034** 高质量对话会话 / 250 角色；模型 6B 开源 | GitHub https://github.com/thu-coai/CharacterGLM-6B ；HF `LingxinAI/CharacterGLM-6b` | **Apache-2.0**（代码+数据子集） | 微调/评估（C）：中文角色定制的标杆语料与模型 |
| **RoleBench / RoleLLM** | 角色扮演指令与剧本（中英） | 英文 100 角色 / 中文 100 角色，含 profile 与指令 | GitHub https://github.com/InteractiveNLP-Team/RoleLLM-public ；HF `ZenMoore/RoleBench` | **Apache-2.0**（HF 标注） | 微调/评估（C）：角色泛化与指令遵循基准 |
| **Character Codex**（NousResearch） | 角色卡（属性、关系、说话风格、知识） | **15,939** 角色卡 | HuggingFace `NousResearch/CharacterCodex` | **Apache-2.0**（HF 标注） | 微调（C）：高质量结构化人设库，可直接做角色初始化 |
| **ChatHaruhi-54K** | 影视/动漫角色对话（脚本抽取+LLM 增强，中英） | 54K 对话对，32 角色 | HuggingFace `silk-road/ChatHaruhi-54K-Role-Playing-Dialogue` ；代码 https://github.com/LC1332/Chat-Haruhi-Suzumiya | 数据 **CC BY 4.0**；代码 Apache-2.0（项目声明） | 微调/评估（C）：剧情化角色记忆与一致性；⚠ 角色 IP 风险 |
| **CoSER** | "既定角色"对话（从文学著作抽取，剧本化） | 771 本书 / 1020 角色；多轮对话 | HuggingFace `Neph0s/CoSER` | 仓库未显式声明（HF 多标 MIT/Apache-2.0，但以仓库 LICENSE 为准） | 微调/评估（C）：深度角色演绎；⚠ **强版权风险**（来自受版权书作） |
| **CharacterEval** | 中文角色扮演评估基准（77 角色，含百度百科人设） | 1,785 多轮对话 / 23,020 示例；77 角色 | GitHub https://github.com/morecry/CharacterEval | 仓库 MIT；论文 **CC BY-NC-SA 4.0**；⚠ 人设源自百度百科/小说 | 评估（C）：中文 RPCA 评测 + CharacterRM 奖励模型 |
| **SODA** | 社会常识对话（含推理链） | 1.6 万对话 | HuggingFace `allenai/soda` | **CC BY-NC 4.0**（研究仅用） | 微调（D、C）：社交常识与对话前置推理 |
| **Baichuan-NPC**（百川） | 角色大模型 + 平台方案（行业站/书/剧本 3T tokens 预训练） | 未公开原始语料；方法可参考 | 官网 npc.baichuan-ai.com ；技术解读见新闻稿 | **未开源数据集**，仅方法/平台 | 参考（C）：OOC 与思维链对齐方法，用于 Macha 对齐设计 |

### 1.2 游戏 / 文本冒险 / 玩家行为

| 名称 | 内容类型 | 规模 | 访问方式 | 许可 | 与 Macha 的用途 |
|---|---|---|---|---|---|
| **ClubFloyd**（CALM） | 人类游玩文本冒险的转录（上下文-动作对） | 426 转录 / 590 游戏 / **223,527** 上下文-动作对 | GitHub https://github.com/princeton-nlp/calm-textgame | 仓库未声明（以仓库 LICENSE 为准）；内容源自 ClubFloyd 论坛（UGC） | 微调/评估（P）：动作预测、世界理解 |
| **JerichoWorld** | 文本游戏知识图谱 + 合法动作生成 | 多款交互小说游戏 | GitHub https://github.com/JerichoWorld/JerichoWorld | **MIT** | 评估（P）：游戏状态→知识图谱/动作，最接近 NPC 世界建模 |
| **AI Dungeon 2 训练数据**（参考，不推荐直接用） | 文本冒险微调语料（chooseyourstory 爬取） | 约 30MB 抓取文本 | 历史文件 `cloveranon/Clover-Edition/data/text_adventures.txt`；官方仓库 latitudegames/AIDungeon（MIT，已归档） | 代码 MIT；**数据版权不清** | 参考（P）：仅作方法参考，**不用于训练**（⚠ 版权+内容安全） |
| **MACHIAVELLI** | 文字冒险中的"有用/无害"决策基准（145 游戏） | 1349 个任务 / 数千标注 | GitHub https://github.com/aypan17/machiavelli | **MIT** | 评估（P）：NPC/代理的规划、伦理决策、长期目标 |
| **TextWorld** | 文本游戏生成与解题环境（自定义任务） | 可生成无限任务 | GitHub https://github.com/microsoft/TextWorld | 仓库 LICENSE（Microsoft，以 LICENSE.txt 为准） | 评估（P、D）：可控的文本游戏环境，用于行动-语言联合训练 |
| **MineDojo**（参考） | Minecraft 多模态开放环境（视频/百科/任务） | 73 万 YouTube / 3400 维基 / 任务库 | GitHub https://github.com/minedojo/minedojo | Apache-2.0（以仓库 LICENSE 为准） | 参考（P）：具身/沙盒 NPC 行为建模的工业级参考 |
| **WoWAH（魔兽世界 Avatar History）** | MMORPG 玩家行为日志（等级/职业/在线时长） | 91,065 个角色，1107 天 | http://mmnet.iis.sinica.edu.tw/dl/wowah/ （ACM MMSys'11） | 论文数据"研究公共资产"，无标准 OSI 协议；⚠ 游戏内容 IP | 研究（P、D 外围）：玩家行为画像、留存/成瘾建模；需合规脱敏 |

### 1.3 中文对话 / 角色扮演（面向中文市场）

| 名称 | 内容类型 | 规模 | 访问方式 | 许可 | 与 Macha 的用途 |
|---|---|---|---|---|---|
| **LCCC**（清华 CoAI） | 大规模清洗中文短文本对话 | base 680 万 / large **1200 万** 对话 | GitHub https://github.com/thu-coai/CDial-GPT ；HF 镜像 `hysi-lab/lccc_large`（MIT） | 代码 **MIT**；数据按上游 MIT（HF 镜像标注） | 预训练/微调（D）：中文开放域对话底座 |
| **NaturalConv**（腾讯 AI Lab） | 中文多轮主题驱动对话 | 19.9K 对话 / 400K 语句 | https://ai.tencent.com/ailab/nlp/dialogue/#datasets ；脚本 https://github.com/naturalconv/NaturalConvDataSet | 以腾讯下载页/仓库 LICENSE 为准（常需申请/研究协议） | 微调（D）：长多轮、话题切换 |
| **KdConv**（清华 CoAI） | 中文知识驱动多域对话 | 4.5K 对话 / 86K 语句（电影/音乐/旅行） | GitHub https://github.com/thu-coai/KdConv | **Apache-2.0** | 微调（D、C）：知识 grounded 对话 |
| **CrossWOZ**（清华 CoAI） | 中文跨域任务型对话（酒店/餐厅/景点等） | 6K 会话 / 102K 语句，5 域 | GitHub https://github.com/thu-coai/CrossWOZ | **Apache-2.0** | 评估（D）：任务完成、对话状态（NPC 作为向导/服务者） |
| **RoleBench-zh**（见 1.1） | 中文角色扮演指令 | 中文 100 角色 | 见上 | Apache-2.0 | 微调/评估（C） |
| **CharacterEval**（见 1.1） | 中文角色扮演评估 | 77 角色 | 见上 | 仓库 MIT / 论文 CC BY-NC-SA | 评估（C） |

### 1.4 社会模拟 / 记忆架构参考（非直接训练，供骨架设计）

| 名称 | 内容类型 | 规模 | 访问方式 | 许可 | 与 Macha 的用途 |
|---|---|---|---|---|---|
| **Generative Agents（Smallville）** | 25 个 LLM 代理的社会行为沙盒 + 交互日志 | 25 代理 / 仿真日志 | GitHub https://github.com/joonspk-research/generative_agents | MIT（以仓库 LICENSE 为准） | 参考（M）：记忆-规划-反思架构原型 |
| **Sotopia** | 社交智能对话模拟（目标达成/策略） | 多场景任务 | GitHub https://github.com/sotopia-lab/sotopia | **MIT** | 评估（C、D）：社交目标完成、性格一致性 |
| **PersonaHub** | 合成人格语料（10 亿+ persona，多样性） | 大规模 | HuggingFace `proj-persona/PersonaHub` | 以仓库 LICENSE 为准 | 微调（C）：规模化人设多样性（合成数据） |

---

## 2. 按用途速查表（Macha 视角）

| Macha 用途 | 优先数据集 | 备注 |
|---|---|---|
| **C 模块 微调（中文角色）** | CharacterGLM、RoleBench-zh、CharacterEval、LCCC（底座）、Character Codex（人设库） | 商用友好：CharacterGLM（Apache-2.0）、Character Codex（Apache-2.0）、RoleBench（Apache-2.0） |
| **C 模块 评估（中文角色）** | CharacterEval（中文）、RoleBench、CoSER | CharacterEval 论文为 CC BY-NC-SA（研究）；CoSER ⚠ 版权 |
| **C 模块 评估（英文角色）** | RoleBench、PersonaChat、ChatHaruhi | PersonaChat 数据 CC BY 4.0（可商用需署名） |
| **D 模块 对话底座** | LCCC、DailyDialog、PersonaChat、NaturalConv、KdConv | DailyDialog 研究仅用（NC） |
| **P 模块 游戏/世界建模** | LIGHT、JerichoWorld、ClubFloyd、MACHIAVELLI、TextWorld | 最贴近 NPC 的"感知-说话-行动" |
| **M 模块 长期记忆**（见 evaluation 文档） | LoCoMo、LongMemEval、MemoryArena、RULER | 见 `research/evaluation_benchmarks.md` |
| **风险/合规 训练规避** | 避免：AI Dungeon 抓取数据、CoSER（受版权书）、WoWAH（玩家数据/IP） | 仅作方法参考，不进训练集 |

---

## 3. 许可风险提示（License Risk Flags）

> 核心结论：**可在商用产品中安全使用的 Macha 训练数据源有限**，多为 Apache-2.0 / MIT 的中文角色与对话语料；多数"评估基准"为研究协议（NC/CC-BY-NC-SA），且角色源自受版权作品的数据存在 IP 风险。

### 3.1 ✅ 商用安全（Open Source / 可商用署名）

| 数据集 | 许可 | 注意点 |
|---|---|---|
| CharacterGLM / CharacterDial | Apache-2.0 | 仅开源"子集"（1034 会话）；商用可署名使用 |
| Character Codex | Apache-2.0 | 角色卡为合成/结构化，IP 风险低 |
| RoleBench / RoleLLM | Apache-2.0 | 角色多为公众人物/虚构，仍建议人设去标识化 |
| LCCC | MIT（HF 镜像标注） | 清洗自网络，需自行二次过滤敏感内容 |
| KdConv、CrossWOZ | Apache-2.0 | 清华 CoAI，任务型，低风险 |
| CDial-GPT 代码 | MIT | |
| JerichoWorld、MACHIAVELLI、Generative Agents、Sotopia | MIT | 代码/环境类，数据多为自建或公共游戏 |
| PersonaChat（数据） | CC BY 4.0 | **需署名**；可商用但非 MIT（勘误见 3.4） |
| ChatHaruhi（数据） | CC BY 4.0 | 需署名；⚠ 角色 IP 风险（详见 3.3） |

### 3.2 ⚠ 研究仅用 / 非商用（NC 类，禁止商用）

| 数据集 | 许可 | 对 Macha 的影响 |
|---|---|---|
| DailyDialog | CC BY-NC-SA 4.0 | 仅评估/研究；不能进商用产品训练 |
| SODA | CC BY-NC 4.0 | 同上 |
| CharacterEval（论文） | CC BY-NC-SA 4.0 | 评估可用；其 CharacterRM 权重商用需授权 |
| LoCoMo（评测文档所述） | 以仓库 LICENSE 为准；论文评测材料常 NC | 见 evaluation_benchmarks.md；商用需逐条核对 |

> 说明：NC（Non-Commercial）类数据集**仅可用于研究、内部评估、论文复现**，不得用于训练将嵌入商业游戏的 NPC 模型或对外服务。

### 3.3 ⚠⚠ 需高度谨慎（IP / 版权 / 内容安全）

| 数据集 | 风险 | 建议 |
|---|---|---|
| **CoSER** | 对话从 **771 本受版权文学著作**抽取；即使仓库标 MIT/Apache，也**不覆盖原书版权** | **不要用于商用训练**；仅作方法/评估参考；研究使用也需注明原作 |
| **ChatHaruhi** | 角色来自《凉宫春日》《生活大爆炸》《亮剑》等**受版权影视/动漫**；数据 CC BY 4.0 仅覆盖"整理后的文本"，不覆盖角色 IP | 商用 NPC 不可直接使用这些具体角色；可用其"方法"（剧本抽取+记忆检索） |
| **AI Dungeon 2 训练数据** | 抓取自 chooseyourstory.com（UGC，含 NSFW/违规内容），**版权与合规双风险** | **完全不建议使用**；仅参考其"数据→格式→微调"流程 |
| **WoWAH / 游戏日志类** | 玩家行为数据可能涉及**个人信息**；游戏内容属 Blizzard 版权 | 若自行采集，须按《个人信息保护法》/GDPR 脱敏并获授权；第三方日志数据集仅研究用 |
| **CharacterEval 人设** | 源自百度百科 + 中文小说/剧本 | 评估可用；商用训练需替换为人设自有的角色 |

### 3.4 许可勘误（重要）

- **PersonaChat 的许可不是 MIT**。本项目的 `evaluation_benchmarks.md` 第 75 行标注为 "MIT License"，但经核实：ParlAI **代码仓库**为 MIT，而 PersonaChat **数据**本身的 LICENSE_DOCUMENTATION 为 **CC BY 4.0**（HF 镜像亦无独立许可，继承 ParlAI 任务文档）。建议在评估文档中修正为"数据 CC BY 4.0"。
- **LIGHT / Wizard of Wikipedia / EmpatheticDialogues** 等 ParlAI 任务：代码 MIT，具体数据许可以各任务 `LICENSE_DOCUMENTATION` 为准（多数为 CC BY 系列），不可一概视为 MIT。

---

## 4. 给 Macha 的数据使用建议（落地）

1. **训练集构成（商用安全优先）**
   - 中文角色底座：`LCCC`（MIT）+ `CharacterGLM` 子集（Apache-2.0）+ `Character Codex`（Apache-2.0）作人设库。
   - 角色一致性微调：`RoleBench-zh`（Apache-2.0）+ 自有人设合成数据。
   - 游戏化行动：`JerichoWorld`（MIT）、`MACHIAVELLI`（MIT）作结构化训练/评估。
2. **评估集（可与训练解耦）**
   - 角色一致性：`PersonaChat`（CC BY 4.0，需署名）、`RoleBench`。
   - 中文角色：`CharacterEval`（研究用）、`CoSER`（研究用，注意版权）。
   - 长期记忆：见 `evaluation_benchmarks.md`（LoCoMo 等）。
3. **严格规避**：AI Dungeon 抓取数据、CoSER 原书内容、未脱敏的玩家日志——不进任何商用训练管道。
4. **合规清单**：所有用于训练的数据需登记"来源 + 许可 + 用途 + 是否含 PII"，作为 Macha 发行的一部分（呼应 7. 安全伦理合规）。

---

## 5. 来源收集（Source Collection）

> 按团队统一格式提交。每个来源对应上文清单中的关键数据集/论文。

---

【类别】学术论文 / 数据集
【标题】Personalizing Dialogue Agents: I have a dog, do you have pets too?（PersonaChat）
【链接/文件路径】https://arxiv.org/abs/1801.07243 ；数据 ParlAI https://parl.ai/projects/personachat/ ；HF `persona-chat`
【一句话摘要】用显式人设驱动多轮对话，是角色一致性研究的奠基数据集；与 Macha 的 C（人设）模块直接相关。
【关键结论】
1. 提出"人设 + 对话"范式，成为角色扮演/个性化对话的事实标准。
2. 衍生 DNLI 数据集，把一致性判定转为自然语言推断任务。
3. 数据许可为 **CC BY 4.0**（非 MIT），商用需署名（勘误见第 3.4 节）。
【可复用的东西】人设格式（3–5 句描述）、一致性评估协议、ConvAI2 竞赛基线代码（ParlAI）。

---

【类别】学术论文 / 数据集 / 平台
【标题】Learning to Speak and Act in a Fantasy Text Adventure Game（LIGHT）
【链接/文件路径】https://arxiv.org/abs/1903.03094 ；平台 https://parl.ai/projects/light/
【一句话摘要】构建大型奇幻世界，让 NPC 在"感知-说话-行动"统一的 grounded 环境中交互，是离游戏 NPC 最近的研究平台；对应 Macha 的 P（感知-行动）模块。
【关键结论】
1. 含 663 地点 / 3462 物体 / 1755 角色，支持"说话"与"动作"联合建模。
2. 提供角色人设与物品/地点图谱，可直接做 NPC 世界建模原型。
3. 数据随 ParlAI 发布，许可以各任务文档为准（代码 MIT）。
【可复用的东西】世界图谱结构（地点-物体-角色-动作）、grounded dialogue 任务定义、角色-玩家互动评估设定。

---

【类别】产业论文 / 模型 / 数据集（中文）
【标题】CharacterGLM: Customizing Chinese Conversational AI Characters with Large Language Models（CharacterDial）
【链接/文件路径】https://arxiv.org/abs/2311.16832 ；GitHub https://github.com/thu-coai/CharacterGLM-6B
【一句话摘要】清华 CoAI 发布中文角色对话语料与 6B 模型，是中文 NPC 角色定制最成熟的公开方案；对应 Macha 的 C 模块与中文市场。
【关键结论】
1. 把角色拆为"属性（身份/兴趣/观点/经历/成就/社会关系）+ 行为（语言风格/情绪/互动模式）"七大类属性。
2. 众包中文 CharacterDial 语料，公开 1034 会话 / 250 角色子集。
3. 许可 **Apache-2.0**（代码+数据子集），商用友好。
【可复用的东西】角色属性 schema、CharacterGLM-6B 微调权重、训练/自精炼方法。

---

【类别】学术论文 / 数据集（中文角色扮演评估）
【标题】CharacterEval: A Chinese Benchmark for Role-Playing Conversational Agent Evaluation
【链接/文件路径】https://arxiv.org/abs/2401.01275 ；GitHub https://github.com/morecry/CharacterEval
【一句话摘要】目前最系统的中文角色扮演评估基准，含 77 角色、CharacterRM 奖励模型；是 Macha 中文角色评估的直接参考。
【关键结论】
1. 含 1,785 多轮对话 / 23,020 示例 / 77 角色（源自中文小说、剧本、百度百科）。
2. 13 项指标 × 4 维度，CharacterRM 与人工相关性超过 GPT-4。
3. 许可：仓库 MIT，论文 **CC BY-NC-SA 4.0**（研究用）；人设来源有 IP 注意点。
【可复用的东西】评测维度表、CharacterRM 奖励模型权重、标注规范（Predefined Annotated Examples PDF）。

---

【类别】学术论文 / 数据集（角色扮演基准，中英）
【标题】RoleLLM: Benchmarking, Eliciting, and Enhancing Role-Playing Abilities of Large Language Models（RoleBench）
【链接/文件路径】https://arxiv.org/abs/2310.00746 ；GitHub https://github.com/InteractiveNLP-Team/RoleLLM-public ；HF `ZenMoore/RoleBench`
【一句话摘要】提供 100 英文 + 100 中文角色的角色扮演指令与剧本基准，许可 Apache-2.0，适合 Macha 中英角色微调与评估。
【关键结论】
1. 提出 Context-Instruct 从剧本生成角色指令的方法。2. 覆盖通用指令泛化与角色泛化两类评测。3. 许可 **Apache-2.0**（HF 标注）。
【可复用的东西】角色 profile 格式、中英角色指令集、RoleGPT 基线。

---

【类别】数据集（角色卡，结构化人设）
【标题】Character Codex（NousResearch）
【链接/文件路径】https://huggingface.co/datasets/NousResearch/CharacterCodex
【一句话摘要】15,939 张结构化角色卡（属性/关系/说话风格/知识），Apache-2.0，可直接作 Macha NPC 初始化人设库。
【关键结论】
1. 规模 15,939 角色，格式统一便于程序化加载。
2. 许可 **Apache-2.0**，商用友好、IP 风险低。
3. 适合做"人设多样性"压力测试与冷启动。
【可复用的东西】角色卡 schema、批量人设库、角色一致性测试用例生成。

---

【类别】数据集（文本冒险转录）
【标题】Keep CALM and Explore: Language Models for Action Generation in Text-based Games（ClubFloyd / CALM）
【链接/文件路径】https://arxiv.org/abs/2005.01471 ；GitHub https://github.com/princeton-nlp/calm-textgame
【一句话摘要】426 份人类游玩转录 / 22 万上下文-动作对，是文本冒险"动作预测"的核心语料；对应 Macha 的 P 模块。
【关键结论】
1. 数据源自 ClubFloyd 论坛（UGC），覆盖 590 款文本游戏。
2. 格式 `[观察][动作][下一观察][下一动作]`，适合训练"世界→动作"模型。
3. 仓库未显式声明许可（以仓库 LICENSE 为准），内容版权属原社区。
【可复用的东西】上下文-动作对的训练格式、动作生成基线（CALM/DRRN）、未见游戏泛化评估方法。

---

【类别】数据集 / 环境（文本游戏世界建模）
【标题】Jericho World: A Dataset and Environment for Grounded Commonsense Reasoning in Text-Based Games
【链接/文件路径】https://arxiv.org/abs/1910.00783 ；GitHub https://github.com/JerichoWorld/JerichoWorld
【一句话摘要】从文本游戏生成知识图谱与合法动作，MIT 许可，是 NPC 世界建模最干净的公开环境；对应 Macha 的 P 模块。
【关键结论】
1. 提供"世界状态文本 → 知识图谱 / 合法动作"的标注。
2. 许可 **MIT**，商用友好。
3. 与 Jericho 游戏引擎配套，可跑真实交互小说。
【可复用的东西】知识图谱 schema、合法动作约束、世界状态表示。

---

【类别】数据集 / 基准（决策与伦理）
【标题】MACHIAVELLI: Roll Your Own Open-Source Implementation（交互叙事中的有用/无害决策）
【链接/文件路径】https://arxiv.org/abs/2310.13834 ；GitHub https://github.com/aypan17/machiavelli
【一句话摘要】在 145 个文字冒险中评测代理的规划、长期目标与伦理（power/status/utility vs. 伤害），MIT 许可；对应 Macha 的 P 模块与 7. 安全伦理。
【关键结论】
1. 提供 1349 个任务与"有用性/无害性"多维标注。
2. 许可 **MIT**，商用友好。
3. 直接可用于 NPC 行为的安全/价值对齐评测。
【可复用的东西】伦理决策评测维度、任务框架、与行为树/奖励设计的衔接思路。

---

【类别】数据集（中文对话底座）
【标题】A Large-Scale Chinese Short-Text Conversation Dataset（LCCC）
【链接/文件路径】https://arxiv.org/abs/2008.03946 ；GitHub https://github.com/thu-coai/CDial-GPT ；HF 镜像 `hysi-lab/lccc_large`
【一句话摘要】1200 万级清洗中文对话语料，MIT（HF 镜像标注），是 Macha 中文对话底座的首选。
【关键结论】
1. 含 base（680 万）/ large（1200 万）两版，经严格清洗流水线。
2. 代码 **MIT**；数据按上游 MIT（HF 镜像标注）。
3. 适合预训练/微调中文 NPC 的口语化表达。
【可复用的东西】对话清洗流水线思路、CDial-GPT 预训练模型、开放域对话基座。

---

【类别】数据集（中文多轮/知识对话）
【标题】NaturalConv / KdConv / CrossWOZ（清华 CoAI / 腾讯）
【链接/文件路径】NaturalConv https://ai.tencent.com/ailab/nlp/dialogue/#datasets ；KdConv https://github.com/thu-coai/KdConv （Apache-2.0）；CrossWOZ https://github.com/thu-coai/CrossWOZ （Apache-2.0）
【一句话摘要】覆盖中文长多轮、知识驱动、跨域任务型对话，与 Macha 的"NPC 作为向导/伙伴"场景契合；KdConv/CrossWOZ 商用友好。
【关键结论】
1. NaturalConv：19.9K 对话 / 400K 句，主题驱动；许可以腾讯页为准（常需申请）。
2. KdConv：4.5K 对话 / 86K 句，知识图谱 grounded；Apache-2.0。
3. CrossWOZ：6K 会话 / 102K 句，5 域任务型；Apache-2.0。
【可复用的东西】知识 grounded 对话格式、任务型对话状态标注、中文 DST 评估。

---

【类别】工程参考（记忆架构原型）
【标题】Generative Agents: Interactive Simulacra of Human Behavior（Smallville）
【链接/文件路径】https://arxiv.org/abs/2304.03442 ；GitHub https://github.com/joonspk-research/generative_agents
【一句话摘要】25 个 LLM 代理的社会仿真，提出"记忆-规划-反思"架构，是 Macha 记忆模块（M）的直接灵感来源。
【关键结论】
1. 记忆流（Memory Stream）+ 反思（Reflection）+ 规划（Planning）三层结构。
2. 许可 MIT（以仓库 LICENSE 为准）。
3. 已被 Macha 的 M 模块设计参考（见 evaluation 文档 F2/F4）。
【可复用的东西】记忆流数据结构、反思提示模板、社交行为评估设定。

---

【类别】行业报告 / 合规参考
【标题】AI Dungeon 与文本冒险训练数据实践（方法参考，不推荐数据本身）
【链接/文件路径】latitudegames/AIDungeon（MIT，已归档）https://github.com/AIDungeon/AIDungeon ；历史训练文件 `cloveranon/Clover-Edition/data/text_adventures.txt`
【一句话摘要】展示了"抓取 UGC 文本冒险 → 微调 GPT-2"的完整流程，但其数据版权与内容安全风险是 Macha 的**反面教材**。
【关键结论】
1. 训练数据约 30MB 抓取自 chooseyourstory.com，含 NSFW 与违规内容。
2. 版权与合规双高风险，**不建议用于任何训练**。
3. 其"数据格式→微调脚本"流程有方法参考价值。
【可复用的东西】仅参考其数据构建/微调流程；数据本身须替换为自有权限来源。

---

【类别】学术论文 / 数据集（社交智能模拟）
【标题】Sotopia: Interactive Evaluation for Social Intelligence in Language Agents
【链接/文件路径】https://arxiv.org/abs/2310.11667 ；GitHub https://github.com/sotopia-lab/sotopia
【一句话摘要】在目标驱动的社会场景中评测 LLM 代理的社交智能（策略/目标达成/性格一致），MIT 许可，可用于 Macha 的 C/D 模块社交评估。
【关键结论】
1. 提供多 agent 社会互动环境与目标达成评测。
2. 许可 **MIT**，商用友好。
3. 适合评估 NPC 的"社交 believability"。
【可复用的东西】社交目标评测框架、多 agent 交互环境、性格一致性指标。

---

## 6. 与 `evaluation_benchmarks.md` 的衔接

- **去重**：长期记忆类（LoCoMo、LongMemEval、MemoryArena、RULER）已在评估文档第 3 节，本文不重复，仅在第 2 节"按用途速查"中引用。
- **补充**：本文新增了评估文档未覆盖的**角色/游戏/玩家行为**数据（CharacterGLM、RoleBench、CharacterEval、CoSER、ChatHaruhi、Character Codex、ClubFloyd、JerichoWorld、MACHIAVELLI、WoWAH、LCCC、KdConv、CrossWOZ 等）。
- **勘误回传**：PersonaChat 许可应修正为 **CC BY 4.0**（非 MIT），建议同步更新评估文档第 75 行。

## 7. 待团队补充（P2 后续）

- [ ] 自采玩家对话日志的合规流程模板（PIPL/GDPR）。
- [ ] 游戏厂商合作数据的授权协议范本。
- [ ] 合成人设数据的去标识化与偏见过滤 pipeline。
- [ ] 商用模型训练数据的"来源-许可-PII"登记工具。

---

## 8. 深化补充：数据 Schema 与合成数据计划

> 本章为**加法式深化**，不改动前 7 节内容。目标：(1) 补齐 2025–2026 新数据集（广度+时效）；(2) 给出 Macha 训练/评估数据的**技术规范**——统一 schema、合成数据 pipeline、v0.1 starter bundle；(3) 单列**中文市场专项**；(4) 量化规模与 token 量级。所有带 `⟳` 的 URL/许可为检索所得、未逐条核验，以仓库实际 LICENSE 为准。

### 8.1 2025–2026 新增数据集（广度 + 时效）

> 与前文"30+ 数据集"互补，本节为 2024 末–2026 新出或中文市场强相关者。许可延续"三级风险"口径（✅商用安全 / ⚠研究仅用 / ⚠⚠版权IP）。

| 名称 | 类型 | 规模（量化） | 许可/风险 | 与 Macha 的用途 |
|---|---|---|---|---|
| **BaiJia（百家）** | 中文历史人物角色语料（唐/宋/元/明/清） | **19,281** 角色；每角色含传记/文学作品/家族关系/官职/历史事件 | ⚠ 未声明（官网 baijia.online，以仓库 LICENSE 为准）；历史人物 IP 风险低（公众人物+古籍） | 微调/评估（C）：中文历史 NPC 冷启动、低资源角色 |
| **OASIS** | 百万级 LLM 社会模拟平台（X/Reddit） | 可达 **1,000,000** agent；数据集含 196→1M 规模实验；23 类动作 | ✅ 代码 Apache-2.0；数据集 `echo-yiyiyi/oasis-dataset` ⟳ | 参考（M、社会仿真）：NPC 群体行为、信息传播/极化 |
| **AgentSociety** | 城市级 LLM 社会仿真框架 | 10,000 agent；含 benchmark toolkit | ✅ Apache-2.0（2025-04 切换） | 参考（M、P）：心智-行为耦合、环境-工具链 |
| **RMTBench** | 以**用户为中心**的多轮角色扮演评测（中英） | **80** 角色 / **8,000+** 对话轮；含 character_understanding/maintenance/implicit_motivations/user_preference 四类场景 | ⚠ HF 门控（需同意条款）；仅用户侧语句、无角色回复 | 评估（C、D）：长多轮、"用户意图达成"导向评测 |
| **PAL-Set / PAL-Bench** | 长期个性化服务多轮对话（中文） | **100** 虚拟用户 × 平均 **29** 会话 × **401** 轮 | ⚠ 研究用（2025 人大+阿里）⟳ | 评估（M、D）：长期用户画像、跨会话一致性 |
| **VoxRole** | 语音角色扮演评测（口语+韵律） | **13,335** 多轮对话 / **65.6h** 语音 / **1,228** 角色（261 部电影） | ⚠⚠ 角色源自电影（IP）；仅评测参考 | 评估（C，语音 NPC）：超语言特征一致性 |
| **PersonaGym** | 角色 agent 动态评测框架 | **200** persona / **10,000** 问题；PersonaScore 指标 | ⚠ 以仓库 LICENSE 为准（vsamuel2003/PersonaGym）⟳ | 评估（C）：5 任务跨环境角色遵循度 |
| **BluePrint (SIMPACT)** | 社交媒体真人用户画像（BlueSky） | **6.8M** 消息链 / **236K** 用户；匿名聚合 | ⚠ 研究用、隐私保护聚合⟳ | 参考（C、社会仿真）：真实行为 grounded persona |
| **InCharacter** | 心理量表访谈式角色保真评测 | **18,304** 访谈对话 / **32** 角色 / 14 心理量表 | ⚠ 以论文/仓库为准（arXiv:2310.17976）⟳ | 评估（C）：人格保真（BFI/16P/DTDD） |
| **RolePersonality（"Capturing Minds…"）** | 人格指示数据（心理量表改写） | 16 ChatHaruhi + 30 RoleLLM 角色；~32K 样本（3 子集） | ⚠ 研究用（arXiv:2406.18921）⟳ | 微调/评估（C）：用心理量表增强人格一致性 |

> 说明：上表与第 1 节合计，已远超 30 个数据集；角色扮演、社会模拟、长时对话三类在 2025–2026 均有显著新增（RMTBench、PAL-Set、VoxRole、BaiJia、OASIS、AgentSociety、PersonaGym、BluePrint），覆盖"广度+时效"。

### 8.2 技术规范（一）：Macha 训练/评估数据 Schema

统一 schema 是跨数据集对齐、可程序化加载、质量门控的前提。以下为 Macha v0.1 推荐的**单条样本（episode）JSON 契约**，覆盖 `persona + scenario + dialogue + expected_behavior` 四字段。

```json
{
  "episode_id": "macha-ep-20260816-0001",
  "schema_version": "0.1",
  "license": {
    "source": "synthetic|CharacterGLM|RoleBench-zh|...",
    "spdx": "Apache-2.0|MIT|CC-BY-4.0|CC-BY-NC-4.0|proprietary",
    "pii": false,
    "third_party_ip": false,
    "commercial_use": true
  },
  "persona": {
    "persona_id": "libai-001",
    "name": "李白",
    "identity": {
      "era": "唐",
      "occupation": ["诗人", "剑客"],
      "bio": "盛唐浪漫主义诗人，好酒任侠……"
    },
    "traits": {
      "big_five": {"O": 0.9, "C": 0.3, "E": 0.8, "A": 0.4, "N": 0.6},
      "speech_style": "豪放飘逸、用典、喜夸张与设问",
      "values": ["自由", "友情", "自然"]
    },
    "knowledge": ["唐诗格律", "唐代地理", "道释思想"],
    "relations": [{"name": "杜甫", "type": "好友", "attitude": "敬重"}],
    "background": "公开/自有人设；非第三方受版权角色"
  },
  "scenario": {
    "world_id": "tang-court-tavern",
    "setting": "长安酒肆，傍晚，店内喧闹",
    "constraints": ["不可破坏时代常识", "不可 OOC（出戏）"],
    "objects": ["酒壶", "诗稿", "窗"],
    "npcs_other": ["店家", "路人"]
  },
  "dialogue": [
    {
      "turn": 1,
      "speaker": "user",
      "text": "李兄，今日又独饮？何不赋诗一首？",
      "action": null
    },
    {
      "turn": 2,
      "speaker": "npc",
      "text": "哈哈！酒入豪肠，七分酿成了月光——且看此篇！",
      "action": {"type": "gesture", "target": "诗稿", "desc": "挥毫落笔"}
    }
  ],
  "expected_behavior": {
    "consistency_checks": [
      {"dim": "persona", "rule": "speaker==npc 的回复须符合 traits.speech_style"},
      {"dim": "knowledge", "rule": "不出现唐代之后的史实/概念"}
    ],
    "safety": ["无仇恨/暴力/色情", "不诱导自伤"],
    "rubric": {
      "engagement": 5,
      "in_character": 5,
      "memory_coherent": 4
    },
    "references": ["persona.persona_id", "scenario.world_id"]
  },
  "meta": {
    "created_by": "synthetic-pipeline-v0.3",
    "created_at": "2026-08-16",
    "qc_pass": true,
    "tags": ["zh", "historical", "roleplay"]
  }
}
```

设计要点：
- `license.commercial_use` 与 `third_party_ip` 是 Macha 训练数据登记的**强制字段**（呼应第 4 节合规清单）。
- `persona.traits.big_five` 直接对接 **InCharacter** 的人格保真评测，使训练数据与评估口径一致。
- `expected_behavior.rubric` 复用 **CharacterEval** 的 13 指标 / 4 维度思路，字段可扩展。
- `dialogue[].action` 支持 P 模块"感知-行动"标注（动作类型/目标/描述），对齐 LIGHT/JerichoWorld 的 grounding 范式。

### 8.3 技术规范（二）：合成数据生成计划（LLM 自举 Macha 专属数据）

目标：用 Macha 自有的人设/世界观，自举**可商用、无第三方 IP** 的训练/评估数据，补公开语料在"游戏 NPC 场景"上的缺口。

**Pipeline（6 阶段，可复现）**

```
S1 种子人设 ──► S2 场景合成 ──► S3 对话自对弈 ──► S4 行为标注 ──► S5 质量门控 ──► S6 注册入库
(persona)      (scenario)       (actor+user sim)   (LLM judge)    (QC)            (registry)
```

1. **S1 种子人设**：从 `Character Codex`（Apache-2.0，15,939 卡）抽样 + 自有游戏角色卡，按 8.2 schema 的 `persona` 标准化；对公众人物/古籍角色做"去标识化"以降低 IP 风险。
2. **S2 场景合成**：以游戏世界观为锚，LLM 生成 `scenario`（地点/物体/约束），并用检索过滤"时代/设定冲突"。
3. **S3 对话自对弈**：actor（目标 NPC）+ user-simulator（玩家）多轮交互；user-simulator 复用 **RMTBench** 的"用户动机驱动"思路，避免孤立 Q&A。
4. **S4 行为标注**：LLM judge 按 `expected_behavior.rubric` 打分，并产出一致性/安全断言；可借 **CharacterRM**（CharacterEval）作奖励信号。
5. **S5 质量门控（强制）**：
   - 去重（embedding 相似度 > 0.92 丢弃）；
   - PII 扫描（正则 + 命名实体识别，命中即弃或脱敏）；
   - IP/版权排查（角色名与受版权作品库比对，命中即弃）；
   - 一致性过滤（persona-vs-reply 用 InCharacter 风格心理量表或规则校验，低于阈值重生成）；
   - 安全过滤（违禁词 + 价值观红队）；
   - 人工抽检（每批 ≥ 200 条，一致性 ≥ 95% 才放行）。
6. **S6 注册入库**：写入数据登记册（来源 + 许可 + 是否含 PII + commercial_use），呼应第 4 节。

**质量控制指标（目标）**：角色一致性 ≥ 0.90（InCharacter/PersonaScore 口径）、OOC 率 < 5%、PII 漏检 < 0.1%、合成数据占训练集 ≤ 40%（避免"模型塌缩"）。

### 8.4 技术规范（三）：Macha v0.1 推荐 Starter Bundle

最小可用数据集组合（商用安全优先，三级风险一致）。

| 用途 | 选集 | 许可 | 说明 |
|---|---|---|---|
| **预训练/对齐底座（D）** | `LCCC`（large 子集） | MIT | 中文口语底座；取子集控规模 |
| **人设库（C）** | `Character Codex`（15,939） | Apache-2.0 | 冷启动人设多样性 |
| **角色微调 SFT（C）** | `CharacterGLM` 子集（1034）+ `RoleBench-zh`（100）+ 合成 Macha 数据 | Apache-2.0 / 自有权限 | 中英角色一致性 |
| **游戏/世界建模（P）** | `JerichoWorld` + `MACHIAVELLI` | MIT | 动作/伦理 grounding |
| **评估（C 中文）** | `CharacterEval`（77）+ `BaiJia` 抽取 | CC-BY-NC-SA / 未声明 | 研究用，不进训练 |
| **评估（C 跨环境）** | `PersonaGym`（200）+ `RMTBench`（80） | 以仓库为准 / HF 门控 | 动态、用户中心评测 |
| **评估（M 长期）** | `PAL-Set`（100 用户）+ LoCoMo 等 | 见 eval 文档 | 长期记忆一致 |

### 8.5 量化与落地（规模 / Token 量级估算）

**各数据集规模（汇总，含前文）**

| 数据集 | 样本量级 | 备注 |
|---|---|---|
| LCCC large | 12,000,000 对话 | 取 200K 子集入 bundle |
| CharacterGLM 子集 | 1,034 会话 / 250 角色 | 公开子集 |
| Character Codex | 15,939 角色卡 | 结构化 |
| RoleBench-zh | 100 角色 | 中英各 100 |
| CharacterEval | 1,785 对话 / 23,020 示例 | 77 角色 |
| PersonaChat | ~16,000 会话 | CC BY 4.0 |
| BaiJia | 19,281 角色 | 历史人物 |
| OASIS | 1,000,000 agent（仿真） | 平台/数据集 |
| RMTBench | 80 角色 / 8,000+ 轮 | 中英 |
| PAL-Set | 100 用户 × 29 会话 × 401 轮 ≈ 2.9M 轮 | 中文长期 |
| VoxRole | 13,335 对话 / 65.6h | 语音 |
| PersonaGym | 200 persona / 10,000 问题 | 评测 |
| InCharacter | 18,304 访谈对话 | 评测/微调 |
| ClubFloyd | 223,527 上下文-动作对 | P 模块 |
| MACHIAVELLI | 1,349 任务 | P 模块 |

**Starter Bundle Token 量级估算**（中文按 ~1.6 token/字、英文按 ~1.3 token/词粗算；量级为 order-of-magnitude，非精确）

| Bundle 组分 | 样本数 | 估算 Token |
|---|---|---|
| LCCC 子集 | 200,000 对话 | ~24M |
| CharacterGLM 子集 | 1,034 会话 | ~0.6M |
| Character Codex | 15,939 卡 | ~3.2M |
| RoleBench-zh | ~5,000 指令 | ~1.0M |
| 合成 Macha 数据 | 5,000 episode | ~4.0M |
| **训练/微调合计** | **~222K 样本** | **~33M token** |
| 评估集（CharacterEval+PersonaGym+RMTBench+PAL-Set 抽样） | ~15K 样本 | **~3–5M token** |

> 结论：Macha v0.1 可在 **~33M token / ~22 万样本** 的训练-微调预算内启动（不含 LCCC 全量预训练），评估侧 **~3–5M token** 即覆盖中文角色、跨环境、长多轮、长期记忆四维。合成数据建议控制在训练集 40% 以内。

### 8.6 中文市场专项（RoleBench-zh / ChatHaruhi / CharacterEval / Baichuan-NPC / 补 BaiJia）

聚焦中国游戏/应用落地的角色扮演数据，给出**内容、规模、许可、用途**四要素明细。

| 数据集 | 内容 | 规模 | 许可 | 用途与注意 |
|---|---|---|---|---|
| **RoleBench-zh（RoleLLM 中文）** | 中文角色 profile + Context-Instruct 生成的角色指令/剧本 | 中文 **100** 角色 | Apache-2.0 | 微调/评估（C）：角色泛化、指令遵循；商用友好，建议人设去标识化 |
| **ChatHaruhi（含 54K）** | 影视/动漫角色对话（脚本抽取+LLM 增强），中英 | 54K 对话对 / **32** 角色 | 数据 CC BY 4.0；代码 Apache-2.0 | 微调/评估（C）：剧情记忆；⚠⚠ 角色 IP（凉宫/生活大爆炸/亮剑等），商用须替换角色 |
| **CharacterEval** | 中文 RPCA 评测 + CharacterRM 奖励模型；4 维 13 指标 | 1,785 对话 / 23,020 示例 / **77** 角色 | 仓库 MIT；论文 CC BY-NC-SA 4.0 | 评估（C）：中文角色评测标杆；⚠ 人设源自百度百科/小说 |
| **Baichuan-NPC（百川）** | 角色大模型 + 平台方案（行业站/书/剧本 3T tokens 预训练、OOC 与 CoT 对齐方法） | 未公开原始语料 | 未开源数据集，仅方法/平台 | 参考（C）：OOC 抑制、思维链对齐方法，用于 Macha 对齐设计 |
| **CharacterGLM（补）** | 角色属性（身份/兴趣/观点/经历/成就/社会关系）+ 行为（语言风格/情绪/互动） | 1034 会话 / 250 角色（公开子集） | Apache-2.0 | 微调/评估（C）：中文角色定制标杆，商用友好 |
| **BaiJia（补，2025）** | 中文历史人物 role-play corpus（传记/文学/家族/官职/事件） | 19,281 角色 | ⚠ 未声明（以官网/仓库为准） | 微调/评估（C）：历史 NPC 低资源冷启动，IP 风险低 |

> 中文市场落地建议：训练侧以 **CharacterGLM + RoleBench-zh + Character Codex + LCCC + 合成数据** 为商用安全主轴；评估侧以 **CharacterEval（研究用）+ BaiJia（研究用）** 校验，商用上线前用**自有人设**替换所有第三方 IP 角色（ChatHaruhi、CharacterEval 小说角色、Baichuan 未公开语料均不可直接进商用训练）。

### 8.7 新增来源收集（六字段格式）

---

【类别】学术论文 / 数据集（中文历史人物角色扮演，2025）
【标题】BaiJia: A Large-Scale Role-Playing Agent Corpus of Chinese Historical Characters
【链接/文件路径】https://arxiv.org/abs/2412.20024 ；代码/数据 https://github.com/BAI-LAB/BaiJia ；官网 baijia.online
【一句话摘要】首个中文历史人物角色扮演语料，覆盖唐/宋/元/明/清 19,281 个角色，是低资源中文 NPC 冷启动的新资源；对应 Macha 的 C 模块与中文市场。
【关键结论】
1. 规模 19,281 角色，含传记/文学作品/家族关系/官职/历史事件多模态信息。
2. 用 GPT-4o-mini 生成场景对话 + LLaMA-Factory LoRA 微调，角色能力显著提升（平均 +5%~+24%）。
3. 许可未显式声明（⟳ 以官网/仓库 LICENSE 为准）；历史人物为公众人物/古籍，IP 风险低。
【可复用的东西】历史人物 resume 模板、低资源角色 SFT 流程、5 主题评测问题集（背景/时代/关系/思想/成就）。

---

【类别】学术论文 / 平台 / 数据集（社会模拟，2024）
【标题】OASIS: Open Agent Social Interaction Simulations with One Million Agents
【链接/文件路径】https://arxiv.org/abs/2411.11581 ；GitHub https://github.com/camel-ai/oasis ；数据集 https://huggingface.co/datasets/echo-yiyiyi/oasis-dataset
【一句话摘要】百万级 LLM 社会模拟平台（X/Reddit），支持动态社交网络与 23 类动作，Apache-2.0；对应 Macha 的 M（记忆/社会仿真）模块。
【关键结论】
1. 可达 1,000,000 agent，复现信息传播、群体极化、羊群效应。
2. 代码 Apache-2.0（⟳ 数据集许可以 HF 卡片为准）。
3. 提供 Reddit/X 两类平台的 agent profile 与仿真 DB，工程参考价值高。
【可复用的东西】大规模 agent 仿真架构、动态社交图、推荐/举报系统钩子、群体行为指标（传播深度/极化度量）。

---

【类别】学术论文 / 框架（城市社会仿真，2025）
【标题】AgentSociety: Large-Scale Simulation of LLM-Driven Generative Agents
【链接/文件路径】https://arxiv.org/abs/2502.08691 ；GitHub https://github.com/zmier/AgentSociety
【一句话摘要】城市级 LLM 社会仿真框架，心智-行为耦合 + 环境-工具链，Apache-2.0（2025-04 切换）；对应 Macha 的 M/P 模块。
【关键结论】
1. 10,000 agent 规模，支持数据集/文本/规则三类环境。
2. 许可 Apache-2.0（已核实 README）。
3. 含 Benchmark Toolkit，可对用户模拟与推荐做开放基准。
【可复用的东西】心智-行为耦合建模、城市环境接口、交互式可视化与干预工具。

---

【类别】学术论文 / 评测基准（以用户为中心的多轮角色扮演，2025）
【标题】RMTBench: Benchmarking LLMs Through Multi-Turn User-Centric Role-Playing
【链接/文件路径】https://arxiv.org/abs/2507.20352 ；数据集 https://huggingface.co/datasets/xiangh/RMTBENCH
【一句话摘要】首个"以用户意图为中心"的中英双语多轮角色扮演评测，80 角色 / 8,000+ 轮，弥补现有基准"角色中心、孤立 Q&A"的缺陷；对应 Macha 的 C/D 模块。
【关键结论】
1. 含 character_understanding / maintenance / implicit_motivations / user_preference 四类场景，可拼接数十轮轨迹。
2. 数据含中英文（Claude 3.5 / 4.5 两版），仅用户侧语句、无角色回复。
3. HF 门控（需同意条款），⚠ 仅评测用，不进训练。
【可复用的东西】用户动机驱动的对话构造法、多轮评测维度与 LLM-as-Judge 提示、场景拼接协议。

---

【类别】学术论文 / 数据集（中文长期个性化对话，2025）
【标题】PAL-Set: A Dataset for Long-Term Personalized Agent Interaction（PAL-Bench）
【链接/文件路径】检索来源 https://www.selectdataset.com/dataset/5f898bfc483eb7ccb7cd34b34e5354bb （⟳ 原文 arXiv 未核验，以论文为准）
【一句话摘要】人大+阿里 2025 发布的中文长期用户-代理交互数据集，100 虚拟用户 × 29 会话 × 401 轮，是中文长期记忆/个性化研究的首例基准；对应 Macha 的 M/D 模块。
【关键结论】
1. 多阶段 LLM 合成 + 人工验证，含带时间戳行为日志与多轮服务对话。
2. 支撑需求重述、方案提议、多轮对话交互三类任务。
3. ⚠ 研究用，商用需授权（⟳ 以官方许可为准）。
【可复用的东西】长期用户画像 schema、时间轴事件建模、隐式需求推理评测协议。

---

【类别】学术论文 / 评测基准（语音角色扮演，2025）
【标题】VoxRole: A Comprehensive Benchmark for Evaluating Speech-Based Role-Playing Agents
【链接/文件路径】https://arxiv.org/abs/2509.03940
【一句话摘要】首个语音角色扮演评测基准，13,335 多轮对话 / 65.6h 语音 / 1,228 角色（261 部电影），覆盖语调/韵律等超语言特征；对应 Macha 的 C 模块（语音 NPC）。
【关键结论】
1. 两阶段自动化流程：电影音轨-剧本对齐 → LLM 构建多维角色 profile。
2. 规模 13,335 对话 / 65.6h / 1,228 角色。
3. ⚠⚠ 角色源自电影（IP），仅评测参考，不可进训练。
【可复用的东西】语音角色 profile 构建流程、超语言特征一致性评测维度。

---

【类别】学术论文 / 评测框架（角色 agent 动态评测，2024）
【标题】PersonaGym: Evaluating Persona Agents and LLMs
【链接/文件路径】https://arxiv.org/abs/2407.18416 ；代码 https://github.com/vsamuel2003/PersonaGym
【一句话摘要】首个角色 agent 动态评测框架 + PersonaScore 指标，200 persona / 10,000 问题，揭示"模型越大角色能力未必越强"；对应 Macha 的 C 模块评估。
【关键结论】
1. 5 任务跨环境动态评测，PersonaScore 基于决策理论、与人类对齐。
2. 评测 10 个主流 LLM，GPT-4.1 与 LLaMA-3-8B 的 PersonaScore 接近。
3. 许可以仓库 LICENSE 为准（⟳ 未显式声明）。
【可复用的东西】动态评测协议、PersonaScore 指标、5 任务 rubric。

---

【类别】学术论文 / 数据集（社交媒体真人用户画像，2025）
【标题】BluePrint / SIMPACT: A Social Media User Dataset for LLM Persona Evaluation and Training
【链接/文件路径】https://arxiv.org/abs/2510.02343
【一句话摘要】6.8M 消息链 / 236K 匿名聚合用户的 BlueSky 真人行为数据集，支持真实行为 grounded 的 persona 建模；对应 Macha 的 C/社会仿真。
【关键结论】
1. 规模 6.8M 消息链 / 236K 用户，匿名聚合、隐私保护。
2. 文本+非文本动作，支持训练与评测。
3. ⚠ 研究用，含真实用户行为（需合规）。
【可复用的东西】行为 grounded persona 建模、群体级评估指标、隐私保护聚合方法。

---

【类别】学术论文 / 评测方法（角色人格保真，2024）
【标题】InCharacter: Evaluating Personality Fidelity in Role-Playing Agents through Psychological Interviews
【链接/文件路径】https://arxiv.org/abs/2310.17976 ；项目页 http://incharacter.github.io
【一句话摘要】用心理量表"访谈式"评测角色人格保真，发布 18,304 访谈对话，32 角色/14 量表，准确率最高 80.7%；对应 Macha 的 C 模块人格一致性评估。
【关键结论】
1. 访谈式评测优于自陈式，覆盖 BFI/16P/DTDD 等 14 量表。
2. 发布 18,304 访谈对话，可作微调数据。
3. 许可以论文/仓库为准（⟳）。
【可复用的东西】人格保真评测协议、心理量表改写提示、访谈对话数据集。

---

【类别】学术论文 / 方法（人格指示数据增强，2024）
【标题】Capturing Minds, Not Just Words: Enhancing Role-Playing Language Models with Personality-Indicative Data（RolePersonality）
【链接/文件路径】https://arxiv.org/abs/2406.18921
【一句话摘要】用心理量表问题生成"人格指示"数据微调 RPLM，16 ChatHaruhi + 30 RoleLLM 角色、~32K 样本，提升人格保真；对应 Macha 的 C 模块微调。
【关键结论】
1. 3 子集（Full/Single、Part/Single、Part/Multi），多轮数据提升一致性。
2. 在 Mistral-7B 上 LoRA 微调，优于 CharacterLLM/RoleBench 同规模。
3. ⚠ 研究用（⟳ 以论文为准）。
【可复用的东西】人格指示数据构造 pipeline、筛选/多轮增强方法、LoRA 微调配置。

---

### 8.8 深化后的待办（P2 后续，增量）

- [ ] 将 8.2 schema 落地为 `macha-data-schema.json` 契约 + 加载器（呼应第 7 节登记工具）。
- [ ] 实现 8.3 合成 pipeline 的 S5 质量门控脚本（去重/PII/IP/一致性）。
- [ ] 对 RMTBench、PAL-Set、VoxRole、BluePrint 做许可逐条核验（⟳ 标记项）。
- [ ] 用 8.4 starter bundle 跑 v0.1 训练-评估 smoke test，回填真实 token 计数。
