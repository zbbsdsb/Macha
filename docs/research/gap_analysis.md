# 初步收集验收与信息缺口分析

> 日期：2026-08-16
> 验收对象：团队提交的 8 份研究文档（academic_cognitive_models / engineering_npc_architectures / industry_landscape / design_theory_believability / evaluation_benchmarks / standards_interop / safety_compliance / data_resources）

---

## 1. 验收结论：通过（可进入下一阶段，但需补充“硬材料”）

**已覆盖的 8 类信息**：

| 类别 | 文档 | 质量判断 |
|---|---|---|
| 1 学术认知模型 | academic_cognitive_models.md | 优秀：有对照表、有融合建议、来源格式规范 |
| 2 工程现有架构 | engineering_npc_architectures.md | 优秀：FSM/BT/GOAP/HTN/Utility 边界清晰，Replace/Wrap 结论可用 |
| 3 产业现状 | industry_landscape.md | 良好：卡点清单很好；部分数据来自二手转引，需回溯一手 |
| 4 设计理论 | design_theory_believability.md | 优秀：设计语言→技术指标翻译表可落地 |
| 5 评估基准 | evaluation_benchmarks.md | 优秀：L1/L2/L3 分层合理，基准清单完整 |
| 6 标准与生态 | standards_interop.md | 优秀：MCP/A2A/OpenAI API/ECS 接口形状梳理清楚 |
| 7 安全合规 | safety_compliance.md | 优秀：中国拟人化互动办法、AI Act、COPPA 等落地为合规开关 |
| 8 数据资源 | data_resources.md | 优秀：许可风险标注诚实，商用/研究用区分清楚 |

**总体评价**：团队已经完成了“文献与公开资料层”的收集，足以支持 Macha 进入架构设计。但若目标真的是“颠覆产业的标准骨架”，目前还缺三类材料：**一手产业证据、代码级接口事实、来自真实开发者的需求验证。**

---

## 2. 需要补充的信息（按优先级）

### P0-1 一手产业数据 / 授权报告

**现状**：industry_landscape.md 的规模数据多来自 CSDN 转引、pmarketresearch 厂商测算，作者已诚实标注“需回溯一手来源”。

**需要补充**：

- [ ] Newzoo 原始报告或官方新闻稿（全球游戏市场、AI 游戏细分）。
- [ ] Niko Partners《China Gamer Behaviour and Market Insights 2025》原始报告或官方摘要。
- [ ] a16z Games 原始调研（73%/88% 使用率、OpenRouter 流量研究）。
- [ ] 伽马数据《中国游戏产业 AI 发展报告》原报告。
- [ ] 任何可引用的 GDC 2025/2026 游戏 AI 演讲（如 AI NPC 落地成本、留存数据）。

**为什么**：标准骨架的立项依据不能建立在二手博客上。否则对外宣讲、论文引用、开源社区背书都会被打折扣。

**交付格式**：报告 PDF + 出处页截图 + 关键数字摘要。

---

### P0-2 代码级拆解：现有框架的“接口事实”

**现状**：engineering 文档总结到位，但没有到“能直接照抄接口签名”的颗粒度。

**需要补充**（目标：每个仓库产出 1 页接口拆解）：

- [ ] `joonspk-research/generative_agents`：记忆流、反思、计划树的实际数据结构与函数签名。
- [ ] `letta-ai/letta`（MemGPT）：主上下文/外部存储/自主换页的状态机与 API。
- [ ] `OpenBMB/Voyager` 或同类：技能库 schema、环境接口。
- [ ] `SkyrimNet`：Papyrus 与 MCP 工具清单、提示模板热重载结构。
- [ ] `RimAI Core`：IOrchestrationService / IPersonaService / IToolRegistryService 接口。
- [ ] `mineflayer`：插件接口与事件模型（作为 Perception/Action 适配层范本）。
- [ ] NVIDIA ACE NIM / Inworld / Convai 的**公开 API 文档字段**（即使部分需注册）。

**为什么**：Macha 要定义标准接口，不能只靠论文摘要。我们需要“接口事实”：字段名、调用顺序、错误处理、状态生命周期。

**交付格式**：每个仓库一份 `reference/teardowns/<name>.md`，包含：架构图、关键接口签名、数据模型、可复用点、不可复用点。

---

### P0-3 模型能力与推理成本/延迟基准

**现状**：多份文档提到“本地小模型+云端大模型”“延迟 1-3 秒”，但缺少可引用的实测数据。

**需要补充**（可由团队做一轮小基准，或收集可信第三方测试）：

- [ ] 候选小模型：Qwen3-8B/14B、Llama 3.1 8B、Gemma 3、DeepSeek-R1-Distill、Mistral-Nemo 等，记录：上下文长度、Function Calling 质量、中文能力、许可证。
- [ ] 本地推理实测：在 4090/5070/M 系列 Mac 上的 token/s、首字延迟、并发。
- [ ] 成本表：每百万 token 价格（云 API vs 本地折旧）。
- [ ] 结构化输出/JSON Schema 支持度对比（OpenAI、vLLM、llama.cpp、Ollama）。
- [ ] 一个可复跑的延迟/成本测试脚本，纳入 Macha 的 E9/E10/E11。

**为什么**：如果 Macha 默认“成本/延迟作为一等公民”，就需要一套自己的工程基准，而不是引用厂商宣传。

**交付格式**：`docs/research/model_serving_benchmarks.md` + 可复跑脚本。

---

### P0-4 真实开发者访谈 / 需求验证

**现状**：产业文档证明了“市场有兴趣”，但没有证明“开发者愿意采用一个开源标准骨架”。

**需要补充**：

- [ ] 访谈 8–15 位潜在用户：独立游戏团队、Mod 作者、中小工作室 AI 程序员、3A 引擎 TA。
- [ ] 固定问题：
  1. 你现在用什么实现 NPC 对话/记忆？
  2. 你最近一次放弃 LLM NPC 方案的原因是什么？
  3. 如果有一个开源骨架，你最不能接受它哪一点？
  4. 你希望它和现有引擎/行为树怎么配合？
- [ ] 总结成“Jobs To Be Done + 拒绝理由清单”。

**为什么**：避免做出“学术正确但没人用”的标准。标准最终是生态采纳率。

**交付格式**：匿名访谈纪要 + JTBD 卡片 + 采纳障碍清单。

---

### P1-5 标准组织与行业规范细节

**需要补充**：

- [ ] ISO/IEC JTC 1/SC 42（AI 标准）、ISO/IEC 23053（AI 框架）相关文档。
- [ ] IEEE 游戏 AI 相关标准/会议（IEEE CoG 论文、IEEE 7000 伦理）。
- [ ] Khronos / O3DE / Godot 基金会对“AI 游戏中间件”的已有讨论。
- [ ] GDC 2025/2026 关于 AI NPC 的标准动议或行业共识。

**为什么**：Macha 若要成为“标准”，不能只做事实标准，还要知道它未来可能对接的正式标准路径。

---

### P1-6 语义裁决与多智能体模拟的“可玩原型”拆解

**需要补充**：

- [ ] Hidden Door 设计文档/开发者访谈（世界状态如何存在引擎层、如何裁决玩家动作）。
- [ ] Infinite Craft 的合成缓存机制实现分析。
- [ ] Suck Up! 的互动结构与 LLM 调用边界。
- [ ] 一个最小可玩的“语义裁决”Demo 的玩法拆解（可让团队试玩并写体验报告）。

**为什么**：Macha 的 Action 层要内置“裁决器”，需要从可玩产品中提取设计规则，而不是只从论文分类中推导。

---

## 3. 已发现问题（待修正）

1. `data_resources.md` 第 133 行声称“evaluation_benchmarks.md 第 75 行标注为 MIT”，但实际已修正为 CC BY 4.0——该勘误条目可更新或删除。
2. `industry_landscape.md` 中“腾讯 18%、网易 12%、米哈游 8% 份额”等数字已自标“口径存疑”，进入对外材料前必须回溯或删除。
3. `information_needs.md` 的索引尚未更新（团队成员新增文档后未回填索引）。

---

## 4. 结论

- **可以验收**：文献/公开资料层已经合格，且部分文档（认知模型融合、设计理论翻译、标准接口草案）已经直接指导架构设计。
- **还不能止步**：要支撑“标准骨架”的定位，请按 P0-1 → P0-4 补齐一手产业数据、代码级拆解、模型基准和开发者访谈。
- **建议**：先让团队把 P0-2（代码拆解）和 P0-3（模型基准）作为本周任务；P0-1（一手报告）由一人专门负责采购/检索；P0-4（访谈）可同步启动，先访 Mod 作者与独立团队（最容易约到）。
