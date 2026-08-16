# 团队信息收集清单（给团队的任务列表）

> 目标：Macha 要做的是**游戏 NPC 领域的标准骨架**，不是某个单点 Demo。  
> 因此信息收集必须覆盖：学术前沿、工程实现、产业现状、设计理论、评估基准、生态标准六个层次。

---

## 1. 学术基础：认知架构与 LLM 代理

**为什么需要**：标准骨架必须有自己的“认知模型”，不能只靠 Prompt 工程。

请团队收集：

- [ ] 经典认知架构：Soar、ACT-R、CLARION、LIDA 的综述或入门材料。
- [ ] LLM 代理基础论文：
  - ReAct（推理与行动结合）
  - Reflexion（自我反思）
  - Tree of Thoughts（搜索式推理）
  - Voyager（开放世界代码型行动）
  - Generative Agents（已有，2304）
  - CAMEL / AutoGen / MetaGPT（多代理协作）
  - MemGPT / Letta（分层记忆）
  - HippoRAG / RAPTOR / GraphRAG（结构化记忆）
- [ ] LLM 游戏代理综述（已有 2404，可再补充 2025-2026 年的新综述）。
- [ ] 世界模型、具身智能与游戏环境中的 LLM 决策论文。

**期望产出**：一份“Macha 认知模型候选方案”的对照表。

---

## 2. 工程实现：现有 NPC/游戏 AI 架构

**为什么需要**：我们要替代或兼容 Behavior Tree、GOAP、HTN、Utility AI，必须知道现有标准长什么样。

请团队收集：

- [ ] 游戏工业标准：
  - Behavior Tree（行为树）规范与常见实现
  - GOAP（Goal-Oriented Action Planning）
  - HTN（Hierarchical Task Network）
  - Utility AI
  - FSM（有限状态机）
- [ ] 游戏引擎 AI 能力：
  - Unity ML-Agents、Unity Behavior
  - Unreal Engine AI（Behavior Tree、Perception、MassAI、Smart Objects）
  - Godot 导航/行为模块
- [ ] 开放源码 NPC 框架：
  - Inworld AI 文档/白皮书
  - NVIDIA ACE 技术文档
  - Convai、Altera、Rival Theory 等公开资料
- [ ] 游戏脚本/模组接口：
  - Minecraft（Mineflayer、MCU）
  - Skyrim/Oblivion 模组 AI
  - RimWorld / Dwarf Fortress / The Sims 的 AI 架构分析

**期望产出**：现有 NPC 技术栈的“功能边界”和“痛点清单”。

---

## 3. 产业现状：市场与产品调研

**为什么需要**：标准骨架必须回答“产业为什么需要它”，不能只从论文出发。

请团队收集：

- [ ] 游戏产业 AI 报告：
  - a16z、Sequoia、Newzoo、Niko Partners 等关于 AI 游戏/NPC 的公开报告。
  - 腾讯、网易、米哈游等大厂在 AI NPC 上的公开分享（如有）。
- [ ] 产品案例：
  - AI Dungeon（AI GM）
  - Suck Up!、Vaudeville、Infinite Craft（AI 原生游戏）
  - 逆水寒/永劫无间等国产游戏中的 AI NPC 落地案例
  - 独立游戏圈采用 LLM NPC 的成功/失败经验。
- [ ] 初创公司地图：
  - 公司/产品/融资/技术路线/合作游戏。
  - 哪些公司做“NPC 大脑”，哪些做“工具链”，哪些做“平台”。

**期望产出**：一份“产业现状与竞争格局”简报，标注各家技术路线和卡点。

---

## 4. 游戏设计理论：NPC 可信度与玩法

**为什么需要**：标准骨架要服务的是“设计可信 NPC”，而不是“更强的聊天机器人”。

请团队收集：

- [ ] 设计理论：
  - MDA 框架（Mechanics-Dynamics-Aesthetics）
  - The Sims 的设计笔记（Will Wright 等）
  - Interactive Drama（Chris Crawford）
  - AI-based Game Design（Eladhari 等）
  - NPC 可信度（Believability）经典论文
- [ ] 游戏体验分析：
  - 角色扮演游戏中“角色一致性”为什么重要
  - 玩家对 NPC 记忆的期待（“NPC 到底该记住什么”）
  - 开放世界与叙事游戏的 NPC 行为差异
- [ ] AI 原生游戏设计：
  - 已有 2607，可补充其对“语义裁决、多智能体模拟”的具体案例拆解。

**期望产出**：一份“NPC 可信度需求文档”，把设计语言翻译成技术指标。

---

## 5. 评估基准：如何证明骨架是标准

**为什么需要**：没有标准评估，就没有标准骨架。

请团队收集：

- [ ] 代理/LLM 评估基准：
  - AgentBench、ToolBench、WebArena
  - 游戏代理基准：MindAgent、SmartPlay、Clembench
  - 长时记忆基准：LoCoMo、LongBench、RULER 等
- [ ] 对话质量评估：
  - PersonaChat、LIGHT、DSTC 相关任务
  - 角色一致性（Role Fidelity）的定量方法
  - 人类评估协议（TrueSkill 等）
- [ ] 游戏 NPC 专属评估：
  - Believability 指标
  - 反幻觉/长期一致性压力测试设计
  - 延迟、成本、吞吐等工程指标
- [ ] 可解释性与可调试性：
  - 为什么玩家需要“可预测的 NPC”
  - 现有 agent 可观测性工具（LangSmith、Phoenix 等）

**期望产出**：Macha 的评估维度表 + 基准数据集清单。

---

## 6. 标准与生态：互操作性

**为什么需要**：要成为“标准骨架”，必须定义清晰的接口和协议。

请团队收集：

- [ ] 互操作协议：
  - MCP（Model Context Protocol）
  - OpenAI Function Calling / Anthropic Tool Use
  - 多智能体通信协议（FIPA ACL、Agent Communication Languages）
- [ ] 游戏工业标准接口：
  - ECS（Entity Component System）架构
  - 行为树/决策模块与游戏引擎的常见数据接口
  - Unity/Unreal/Godot 的插件规范
- [ ] 开源框架设计：
  - LangChain/LlamaIndex 的抽象方式
  - AutoGen/OpenAI Agents 的多智能体抽象
  - Haystack、DSPy 等“声明式/模块化”设计思想
- [ ] 模型接入标准：
  - OpenAI 兼容 API
  - vLLM、llama.cpp、Ollama 的本地服务接口
  - 量化/蒸馏/投机解码等部署方案

**期望产出**：Macha 的“标准接口草案”参考材料。

---

## 7. 安全、伦理与合规

**为什么需要**：NPC 是长期在线的“人格化系统”，风险远高于普通软件。

请团队收集：

- [ ] 安全：
  - LLM 提示注入攻击（Prompt Injection）在游戏中的案例
  - NPC 越狱/角色漂移（Jailbreak/Character Drift）
  - 运行时审核（Guardrails）方案
- [ ] 伦理：
  - 拟人化 NPC 对玩家心理的影响
  - 儿童与未成年玩家保护
  - 成瘾性设计伦理
- [ ] 合规：
  - 欧盟 AI Act 对游戏 AI 的适用性
  - 中国生成式 AI 服务管理法规
  - 玩家数据与对话内容的隐私保护
  - AI 生成内容的版权问题（模型训练数据、生成资产版权）

**期望产出**：一份“Macha 风险与合规检查清单”。

---

## 8. 数据资源

**为什么需要**：训练、微调、评估都要数据。

请团队收集：

- [ ] 对话数据集：
  - PersonaChat、DailyDialog、LIGHT、CharacterGLM 等
- [ ] 游戏/交互数据：
  - 游戏日志、玩家行为数据、NPC 对话语料
  - 文本冒险语料（如 Zork、AI Dungeon 公开数据）
- [ ] 角色设定数据：
  - 角色卡/人设公开数据集
- [ ] 多语言数据（如果考虑中文市场）：
  - 中文对话、中文角色扮演数据集

**期望产出**：Macha 可用数据集清单 + 许可说明。

---

## 优先级建议（先做这些）

| 优先级 | 类别 | 理由 |
|---|---|---|
| P0 | 2. 工程实现：现有 NPC 架构 | 决定 Macha 是“替代”还是“兼容”现有标准 |
| P0 | 5. 评估基准 | 没有评估，标准无从谈起 |
| P0 | 3. 产业现状 | 证明“标准骨架”的真实需求 |
| P1 | 1. 学术基础 | 确定认知模型与记忆架构 |
| P1 | 6. 标准与生态 | 决定接口长什么样 |
| P1 | 4. 设计理论 | 把设计需求翻译成技术需求 |
| P2 | 8. 数据资源 | 等架构方向明确后再收集 |
| P2 | 7. 安全伦理合规 | 可与架构设计并行 |

---

## 团队收集时请遵循的格式

为了不淹没在资料里，请按以下格式提交：

```text
【类别】工程实现 / 学术论文 / 产业报告 / ...
【标题】...
【链接/文件路径】...
【一句话摘要】它解决了什么？和 Macha 的关系？
【关键结论】3-5 条要点
【可复用的东西】架构图？接口定义？数据？评估方法？
```

收集后先统一放入 `reference/` 或新建的 `research/` 目录，并在本文件末尾登记索引。

---

## 研究索引（Research Index）

> 登记日期：2026-08-16 ｜ 状态：P0–P2 八类全部完成 ｜ 形式：每份文档均含按团队规定格式（【类别】【标题】【链接】【一句话摘要】【关键结论】【可复用的东西】）整理的"来源收集"小节。
> 跨文档一致性：所有文档统一对接 `direction.md` / `positioning.md` 的"感知—记忆—推理—行动"骨架与"Replace 上层认知内核 / Wrap 下层执行器"结论。

| 优先级 | 类别 | 文档标题 | 路径 | 一句话摘要 |
|---|---|---|---|---|
| P0 | 2. 工程实现 | 现有 NPC 技术栈的"功能边界"和"痛点清单" | `docs/research/engineering_npc_architectures.md` | 逐条拆解 BT/GOAP/HTN/Utility/FSM、三大引擎 AI、ACE/Inworld/Convai、经典模拟游戏，得出 Macha 应"Replace 认知内核、Wrap 执行层"的结论。 |
| P0 | 5. 评估基准 | Macha 的评估维度表 + 基准数据集清单 | `docs/research/evaluation_benchmarks.md` | 13 个评估维度（功能/工程）× 16 个基准数据集，附反幻觉压力测试与工程埋点建议。 |
| P0 | 3. 产业现状 | 产业现状与竞争格局简报 | `docs/research/industry_landscape.md` | 需求已被验证（厂商 60%+ 采用），但被成本/延迟/可控性/记忆/合规五道卡点锁死——即 Macha 的白空间。 |
| P1 | 1. 学术基础 | "Macha 认知模型候选方案"对照表 | `docs/research/academic_cognitive_models.md` | 7 维对照 Soar/ACT-R/LIDA/Generative Agents/MemGPT/GraphRAG 等，给出融合认知模型（MCM）与 P0–P3 落地优先级。 |
| P1 | 6. 标准与生态 | 标准接口草案参考材料 | `docs/research/standards_interop.md` | 调研 MCP/OpenAI API/ECS/A2A 等，给出 Macha 六层内核→事实标准的接口映射总表。 |
| P1 | 4. 设计理论 | NPC 可信度需求文档 | `docs/research/design_theory_believability.md` | 把 MDA/互动叙事/可信度翻译为 11 项技术需求（C1–C11），并映射到 Macha 四层与评估维度。 |
| P2 | 7. 安全伦理合规 | Macha 风险与合规检查清单 | `docs/research/safety_compliance.md` | S1–S9/E1–E8/C1–C8 分类清单 + 中欧美监管地图 + 合规开关设计；重点对齐中国《拟人化互动服务管理暂行办法》。 |
| P2 | 8. 数据资源 | Macha 可用数据集清单 + 许可说明 | `docs/research/data_resources.md` | 30+ 数据集按对话/游戏/中文/社会模拟分类，含三级许可风险标识，并勘误了 PersonaChat 许可（CC BY 4.0 非 MIT）。 |

**后续建议**：八类研究已为 Macha 标准骨架提供事实底座。下一步可由 P1 学术认知模型 + P1 标准接口草案收敛出"Macha 认知内核 v0.1 规范"，并以 P0 评估维度表建立首个回归基准。

---

## 深化补充登记（2026-08-16 第二轮：四维度加法式深化）

用户反馈首轮"不够全面"，按 **广度+时效 / 技术规范深度 / 中文市场专项 / 量化与落地** 四维度对 8 类文档追加新章节（不删原文，保持 Replace/Wrap 框架与六字段来源格式）：

| 类别 | 文档 | 深化新增要点 |
|---|---|---|
| 工程实现 | `engineering_npc_architectures.md` | §9 执行适配层接口草案（ActionDescriptor JSON Schema + 仲裁伪代码 + 云/本地成本延迟对比）；国产案例（网易伏羲/腾讯/米哈游/恺英/字节）；开源路线图与替换成本估算 |
| 评估基准 | `evaluation_benchmarks.md` | 第7章 评估 harness 规范（config schema + 参考评估器伪代码 + 9 条量化 SLO：p95<800ms、成本<$0.002、一致性>0.85、幻觉<2%）；2025-2026 新基准；国产评测 + v0.1 三档接入清单 |
| 产业现状 | `industry_landscape.md` | §5 量化市场与国产专项（市场规模/CAGR、融资表真实金额、成本结构 $/MAU、国产深度案例 + 技术路线×卡点图） |
| 学术基础 | `academic_cognitive_models.md` | MCM v0.1 组件规范（9 模块接口 + 记忆分层 JSON Schema + perceive→reflect→plan→act 伪代码 + 检索 p95<50ms） |
| 标准生态 | `standards_interop.md` | §9 四份接口草案（MCP NPC Server / OpenAI-compatible function / ECS NPCBrainComponent / A2A 消息 schema）+ 国产大模型 API 兼容表 + 延迟预算 |
| 设计理论 | `design_theory_believability.md` | 第9节 角色卡 Schema(JSON) + C1–C11 可量化指标映射 + 叙事一致性测试场景 + 国产案例 |
| 安全合规 | `safety_compliance.md` | Guardrail pipeline（Input/Output 双层过滤 schema + 注入检测启发式 + 伪代码）+ 14 条 red-team 用例 + 中欧美条款级映射 + 量化目标（过滤<30ms, ASR≤5%） |
| 数据资源 | `data_resources.md` | 第8节 训练/评估数据 JSON schema + 合成数据六阶段 pipeline + Macha v0.1 starter bundle（~33M token）+ 中文数据集专项 |

所有深化来源均按六字段格式登记，未一手核验的链接显式标注、未编造 URL。
