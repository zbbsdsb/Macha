# Industry Status and Competitive Landscape Brief: Game AI NPCs

> **Document positioning**: Macha project "six-layer standard skeleton" — Layer 3, Industry Status (market and product research)
> **Compiled**: 2026-08-16
> **Data scope**: 2023–2026, weighted toward 2025–2026 public materials
> **One-line conclusion**: Real demand already exists in the industry (60%+ of studios already use generative AI; player interest in intelligent NPCs is clear), yet large-scale deployment is locked down by five bottlenecks: **cost / latency / controllability / long-term memory / compliance**. **This is precisely the problem space Macha, as a "standard skeleton," aims to solve.**

---

## 0. Executive Summary

1. **Demand side validated**: a16z Games research shows 73% of game studios already use AI and 88% plan to adopt it; Niko Partners shows 60% of Chinese studios have incorporated generative AI into their development pipeline, 39.4% of players are interested in in-game generative AI, and 85.2% are already aware of the technology.
2. **Market is in high-speed early stage**: multiple institutions cite annual compound growth of 25–40%. AI-native / AI-assisted games are at a critical inflection point moving from "cost reduction and efficiency gains" to "gameplay innovation."
3. **Competition has stratified**: the leaders are the "NPC Brain" (Inworld, Convai, NetEase Fuxi, miHoYo/Anuttacon), "Toolchain" (NVIDIA ACE, Unity/Unreal, Tencent Hunyuan, Ubisoft Ghostwriter, etc.), and "Platform" (Roblox, NVIDIA ACE Runtime, Inworld Runtime, a16z Game Fund).
4. **Bottlenecks are highly concentrated**: cost explodes exponentially with conversation volume, 1–3 second cloud latency breaks immersion, hallucinations cause persona/worldview collapse, long-term memory is limited by context windows, and cross-border data compliance (GDPR / China algorithm filing) is hard to achieve. Indie teams and small-to-mid studios are especially stuck.
5. **Macha's white space**: existing players either sell a "cloud-hosted brain" (expensive, has latency, has compliance risk) or only build "single-point demos." **What is missing is an open-source, pluggable, engine-agnostic standard skeleton with built-in memory/reflection/planning cognitive architecture that treats cost/latency/compliance as first-class citizens** — this is exactly Macha's positioning.

---

## 1. Market Signal Summary

### 1.1 Demand Side: Players and Studios "Embrace Both Ways"

| Signal | Data | Source |
|---|---|---|
| Global game studio AI usage rate | 73% already using, 88% plan to adopt; small teams (<20 people) 84% already using | a16z Games research (via gam3s.gg) |
| China studio generative AI penetration | 60% already in development pipeline | Niko Partners "China Gamer Behaviour and Market Insights 2025" |
| China player interest in in-game GenAI | 39.4% interested, 85.2% already aware | Niko Partners 2025-08-27 |
| Real use of open-source models | Over 50% of open-source model traffic is for "role-playing + narrative" rather than programming | a16z × OpenRouter production traffic study |
| Shift in vendor investment focus | From "dev/test assistance" toward "gameplay design / narrative interaction" core experience | CICC / brokerage review (ima knowledge base) |

**Interpretation**: Demand is not a hypothesis — it is doubly validated by usage rates and player interest. The a16z × OpenRouter study is especially key: it shows that "chatting with / co-creating stories with virtual characters" is one of the real and largest consumer-grade LLM uses, closely aligned with Macha's "believable NPC" direction.

### 1.2 Scale and Growth (Note the Caliber Differences)

> ⚠️ Note: Newzoo's original paid report could not be obtained directly this time; the table below is all drawn from secondary-market research institutions' citations or vendor (pmarketresearch) estimates. **Numbers are for magnitude reference only; please trace back to primary sources when citing.**

| Metric | Value | Caliber |
|---|---|---|
| Global games market (2024) | ≈$234B, +9.8% YoY | Newzoo / Toulie (per CSDN) |
| Global AI games market (2024) | ≈$35B, 15% of games market, +42.9% YoY | Newzoo / Toulie (per CSDN) |
| Global AI games market (2029 forecast) | ≈$120B, 2025–2029 CAGR 28.4% | Newzoo / Toulie (per CSDN) |
| China AI games market (2024) | ≈$15B, +47.1% YoY, 42.9% of global | CNG (Gama) data / Toulie (per CSDN) |
| **Game AI NPC segment** | 2025 ≈$1.25B → 2032 ≈$5.19B, CAGR 22.58%; LLM dialogue systems account for 59.7% | pmarketresearch (vendor estimate, use with caution) |

**Interpretation**: Overall games market growth has slowed (single digits), but **the AI games segment maintains high growth around 30%**, and NPC dialogue is the largest technology direction within it. Demand is structurally upward.

### 1.3 Bottleneck Summary — This Is Macha's Opportunity List

| # | Bottleneck | Manifestation | Typical Evidence |
|---|---|---|---|
| B1 | **Cost explodes exponentially with conversation volume** | Every NPC line of dialogue is real money; "the more successful, the more you lose" | Latitude (AI Dungeon) nearly went bankrupt early on due to GPT-3 API costs; Gladecore says cloud LLM token billing "punishes success" |
| B2 | **Cloud latency breaks immersion** | Cloud models 1–3s latency turns smooth dialogue into awkward waiting | Gladecore "5 studio-killing problems"; players say "railroading vs. too open" polar extremes |
| B3 | **Poor controllability / consistency** | LLM hallucinations cause persona drift, worldview collapse, plot dead-ends | Square Enix "Port Town" NPCs had poor comprehension, 8–12% positive rating; Vaudeville characters "cookie-cutter, contradictory" |
| B4 | **Long-term memory limited** | Limited context window, cross-session memory loss, world state cannot be maintained | LinkedIn technical analysis; CSDN "brainstorm" series on "offline simulation" difficulty |
| B5 | **Compliance / privacy / localization** | Cross-border data (GDPR), China algorithm filing; fails when offline | Gladecore notes cloud solutions struggle with GDPR compliance; Whispers from the Star deactivated its mainland social accounts because domestic models were unfiled |
| B6 | **Integration friction** | Bloated SDKs, engine version conflicts, build errors | Gladecore: "should be plug-and-play, but becomes weeks of debugging" |
| B7 | **Player resistance to "AI lacking a soul"** | Community resists "soulless content," demands AI-use labeling | Nexaspecs 2025 review: industry culture tug-of-war |
| B8 | **Gap from Demo to production** | POC easy, mass production hard; needs years of engineering | LinkedIn technical analysis: "polishing to production grade takes years" |

---

## 2. Competitive Landscape: Three-Layer Classification Map

### 2.1 NPC Brain — Sells the "Character Soul"

| Company/Product | Technical approach | Representative partners/customers | Known bottlenecks |
|---|---|---|---|
| **Inworld AI** | Character Engine: multi-model orchestration (30+ ML models incl. audio/emotion/memory) + no-code studio; Runtime bridges prototype→production gap | Microsoft Xbox, NVIDIA, Epic/Unreal, Unity, Roblox, Disney, NetEase; cumulative funding ≈$120M, $500M valuation | Cloud-hosted dominant → cost (B1)/latency (B2)/compliance (B5); tightly bound to its ecosystem |
| **Convai** | Embodied conversational AI: multimodal perception (visual/voice/text) + knowledge base + narrative design graph + NPC2NPC; 65+ languages 500+ voices; ISO 27001, supports local deployment | Unreal, Unity, Three.js plugins; NVIDIA ACE partner | Unreal plugin still Beta; multi-agent narrative flow needs careful design |
| **NetEase Fuxi (Smart NPC / AOP)** | Agent-Oriented Programming (AOP): perception—cognition—decision full-loop closed loop; Justice Online smart NPCs, Naraka: Bladepoint voice AI teammates | NetEase full lineup (Justice Online, Naraka: Bladepoint, Eggy Party, All-Star Street Ball) | Strongly bound to NetEase internally; not standardized for external output |
| **miHoYo / Anuttacon (Glossa / Whispers)** | Glossa large model (lines/story generation); Anuttacon builds AI-native game Whispers from the Star (full-voice real-time dialogue) | Honkai: Star Rail "never-repeat dialogue" NPCs; Anuttacon self-published | Leans "dream-building," in validation phase; domestic compliance constrained (algorithm filing) |
| **Altera / other Agent factions** | Enters via "digital humans / long-term companion agents," partly into game NPCs | (Limited public info, listed for observation) | Engineering and game integration not yet proven |

### 2.2 Toolchain — Sells the "Production Line"

| Company/Product | Technical approach | Representative partners/customers | Known bottlenecks |
|---|---|---|---|
| **NVIDIA ACE** | Digital human tech stack: Riva ASR + Audio2Face + Chatterbox TTS + ACE Game Agent SDK; supports cloud/local (IGI SDK, Qwen3-8B local deployment) | Convai, Inworld, miHoYo, NetEase, Tencent, Ubisoft, ZenUnited, Seasun (Mecha BREAK claimed first ACE smart NPC game) | Deeply dependent on NVIDIA GPUs; high local barrier, ecosystem lock-in |
| **Unity (Muse / Behavior / ML-Agents)** | In-engine AI creation and behavior tree tools | World's largest third-party engine ecosystem | Weak native LLM NPC capability, mostly relies on third parties |
| **Unreal Engine** | Built-in AI (Behavior Tree, Perception, MassAI, Smart Objects) + MetaHuman + NVIDIA ACE plugin | 3A standard | Same as above, NPC "brain" relies on external connection |
| **Tencent (Hunyuan Games / Game AIR / GiiNEX)** | Hunyuan visual generation (character in minutes), GiiNEX dual engine; VISVISE skeleton/animation workflow, MagicDawn cross-engine lighting | Peacekeeper Elite "Jili" connected to DeepSeek; self-developed Happy AI mini-game platform | Leans assets/efficiency; gameplay-level NPC still exploratory |
| **Ubisoft Ghostwriter** | Auto-generates NPC side dialogue / environmental "barks," reduces repetitive text ~20% | Ubisoft internal | Only assists writers, not real-time dialogue |
| **Kaiying "Xingyi" / Shengqu VRACE** | China's first AI toolchain spanning the full game dev process (animation/map/numerics/code); VRACE integrates art/voice/text | Kaiying, Shengqu systems | Mainly internal, not yet a standard |

### 2.3 Platform — Sells "Ecosystem and Runtime"

| Company/Product | Technical approach | Representative partners/customers | Known bottlenecks |
|---|---|---|---|
| **Roblox (generative AI assistant + 3D foundation model)** | Generate an entire world from natural language; world's largest multimodal dataset (community-authorized training) | 79M DAU platform | Closed ecosystem, not externally portable |
| **NVIDIA ACE Runtime / IGI SDK** | Local inference runtime, unified API across GPU/NPU/CPU | Same ACE ecosystem | Locked to NVIDIA hardware stack |
| **Inworld Runtime** | Consumer-grade AI infrastructure, prototype→production gap solution | Same as Inworld | Cloud cost structure not fundamentally changed |
| **a16z Game Fund ONE** | Capital platform, fund specifically for AI-era game builders (~$600M per industry reports, scale needs verification) | Invests in early AI-game teams | Not a technical platform, pure capital/resources |
| **Mod community (Skyrim/Fallout etc.)** | Players spontaneously connect LLMs to old-game NPCs (e.g., Skyrim + ChatGPT) | Geek players | Tech demo, "nightmarish" reviews, not a product |

### 2.4 Comprehensive Competitive Map (Overview)

```
                  [NPC Brain]            [Toolchain]              [Platform/Runtime]
  Startup/3rd    Inworld │ Convai │      NVIDIA ACE │         Roblox │ Inworld Runtime │
               Altera                Ubisoft Ghostwriter   NVIDIA IGI SDK │ a16z Fund
  Big-co self    NetEase Fuxi(AOP) │     Tencent Hunyuan/Game AIR │
              miHoYo Glossa/Anuttacon  Unity/Unreal built-in │
                                    Kaiying Xingyi/Shengqu VRACE │
  Community/     (role-playing open-source   Mod community(Skyrim+LLM) │
  geek           models)
```

**Landscape characteristics**:
- **Highly fragmented**: many middleware/startups; engine and cloud vendors consolidate via M&A (pmarketresearch original: "competitive landscape remained fragmented").
- **"Brain" layer occupied by a few players**: Inworld (best funded), Convai lead third-party; big companies each build their own, not open.
- **"Standard interface" absent**: each uses its own SDK/API; cross-engine, cross-model, cross-vendor non-interoperable — this is exactly the layer Macha wants to define.

### 2.5 Product Cases: Who Made It, Who Crashed

| Case | Type | Result | Lesson for Macha |
|---|---|---|---|
| **AI Dungeon (Latitude)** | AI GM / text adventure pioneer | Launched 2019, exploded; 100K in a week, 1.5M users in half a year; later nearly bankrupt from GPT-3 API costs, introduced low-cost models + context limits to "stop the bleeding"; delisted from Steam 2024, but 2025 still ~$7M annual revenue profitable with 12-person team | Validated "open narrative" demand; also blood-and-tears proof that **B1 cost** is a life-or-death line |
| **Suck Up! (Proxima)** | AI-native party game (vampire knocks on doors, each door an AI NPC driven by ChatGPT) | Zero marketing budget, 100M+ YouTube views; only reached Steam 1.0 in 2025-10 | Key is not "used AI" but found an **interactive structure that can be watched/shared/copied** — AI just makes answers happen faster |
| **Vaudeville** | AI-native murder mystery (open dialogue interrogation) | Stunning concept but unstable AI quality: cookie-cutter characters, non-sequiturs, self-contradictions | Confirms **B3 controllability** — open dialogue without constraints and memory cannot sustain complex gameplay |
| **Infinite Craft (Neal Agarwal)** | Browser sandbox, LLaMa-driven "semantic adjudication" (combining items) | Viral spread, 300M recipes/day | "Semantic adjudication" is a more stable AI-native gameplay paradigm than "chat NPCs" (see AI-Native paper) |
| **Justice Online (NetEase)** | China's first in-game AI NPC (200+ smart NPCs → DeepSeek-driven "Shen Qiusuo" → 5 domestic large models forming NPC girl group) | Continuous iteration, high UGC content ratio; retainer system Agent-ized won 2025 Image and Graphics Society Science and Technology Progress First Prize | Validated playability of "long-term memory + multimodal + UGC" combo, **but strongly bound to NetEase internally** |
| **Naraka: Bladepoint (NetEase) voice AI teammate** | AOP framework: ASR + command understanding + knowledge Q&A + persona dialogue + TTS | 300M+ social media views; pathfinding success 77%→99% | Proves AI teammates that "understand, chat, fight" have strong emotional value |
| **Whispers from the Star (Anuttacon/Cai Haoyu)** | AI-native interactive narrative, full-voice real-time dialogue with stranded astronaut Stella | Released Steam 2025-08, 82% positive; ~30K copies; later deactivated mainland social accounts because domestic models unfiled | Pioneer but exposed **B5 compliance** and the controversy of "lacking a game framework, like a big C.AI toy" |
| **Square Enix "Port Town Serial Murder" AI version** | Classic mystery game + NLP natural language understanding | **Crashed**: Steam 8–12% positive, "Overwhelmingly Negative"; NPCs poor comprehension, became a word-guessing game; local NLP took 10GB, 5GB VRAM | Negative example: **B2 latency/performance, B3 controllability, B1 cost** triple failure; also shows "has NLP" ≠ "good experience" |

---

## 3. Implications for Macha: Where Is the White Space

Based on the above evidence, Macha should avoid "building yet another me-too cloud NPC brain" and instead cut into the **"standard skeleton" layer that all existing players jointly lack**:

1. **Gap One: Open-source, engine-agnostic cognitive architecture standard**
   Existing brains (Inworld/Convai/Fuxi) all bind to their own ecosystems. Macha should define a pluggable cognitive architecture of "perception—memory—reflection—planning—action" (consistent with direction.md's MVP) so any game engine and any LLM can connect. **This is a "standard," not "yet another product."**

2. **Gap Two: Treat cost/latency as first-class citizens**
   B1/B2 are the industry's biggest pain points. Macha should build in at the architecture layer: local small-model-first, cloud large-model-fallback tiered routing, request caching, batching, degradation strategy (referencing ByteDance's "async dynamic narrative service layer" idea). A standard skeleton that solves cost by default directly hits small teams' fatal weakness.

3. **Gap Three: Evaluable implementation of long-term memory and character consistency**
   B3/B4 (hallucination, persona drift, cross-session memory) are joint pain points of the academic layer (direction.md) and industry layer. Macha uses structured memory (causal memory, reflection summaries, world-state vectors) rather than raw context windows, plus an evaluation benchmark (character consistency, long-term memory stability) — corresponding to layer 5 of the information-needs list.

4. **Gap Four: Controllable generation and guardrails as standard components**
   Square Enix's crash and players' "AI lacks soul" resistance show: open generation must be constrained. Macha should embed a standard pattern of "strong-constraint prompts + structured output + validation layer + behavior tree/FSM fallback + content safety gateway" (referencing CSDN brainstorm series and ByteDance safety gateway).

5. **Gap Five: Interoperable interface and compliance-friendly local-first**
   Define an MCP-like "NPC communication / tool-calling protocol" so the NPC brain, toolchain, and platform layers can interoperate; also support local deployment by default to meet GDPR / China algorithm filing compliance (B5). Corresponds to layer 6 of the information-needs list.

6. **Gap Six: Evaluation as standard**
   No evaluation, no standard. Macha should ship "industry-understandable evaluation dimensions" (cost/latency/character consistency/long-term memory/compliance) so "whether it meets the Macha standard" can be proven — this is the key leap from "framework" to "standard skeleton."

> **One-line positioning**: Macha = an open-source, engine-agnostic NPC cognitive-architecture standard that makes "cost/latency/memory/control/compliance" default capabilities. It does not compete with historical players for "brain" or "platform," but defines the "skeleton" they all must obey.

---

## 4. Source Collection (Per Team-Specified Format)

> All sources below are pages actually accessed during this search. Items marked "trace primary source / scale to be verified" should be double-checked before citing.

---

[Category]Industry report (secondary-market compilation)
[Title]2025 Global AI Games Market Research Report: Industry Insights and Future Trends
[Link/FilePath]https://blog.csdn.net/bvip911/article/details/150393068
[One-line summary]Compiles Newzoo / Toulie / CNG (Gama) data, giving AI games market size, growth, player behavior, and vendor layout (Tencent/NetEase/miHoYo/37 Interactive). Relevance to Macha: provides market-size magnitudes and the "cost-down→gameplay-innovation" inflection industry evidence.
[Key conclusions]
1. 2024 global AI games market ≈$35B (15% of games), 2029 forecast ≈$120B, CAGR 28.4%.
2. China AI games 2024 ≈$15B, 2029 forecast ≈$50B.
3. Among top vendors Tencent 18%, NetEase 12%, miHoYo 8% share (this share caliber is questionable, pending verification).
4. Technical bottlenecks explicitly listed: unstable AI content quality, NPCs lack long-term memory / unrealistic emotional interaction.
5. Justice Online / Peacekeeper Elite / Honkai: Star Rail all have deployed AI NPCs.
[Reusable]Market-size data table, vendor layout comparison, technical bottleneck list (can directly feed Macha requirements doc).

---

[Category]Industry report (vendor estimate)
[Title]Game AI NPC Market – Size, Share & Industry Analysis 2026–2032
[Link/FilePath]https://pmarketresearch.com/it/game-ai-npc-market
[One-line summary]Independent market research firm's estimate of the "game AI NPC" segment. Relevance to Macha: corroborates NPC dialogue as the largest AI-games technology direction (LLM dialogue 59.7%).
[Key conclusions]
1. 2025 game AI NPC market $1.25B → 2032 $5.19B, CAGR 22.58%.
2. LLM-driven dialogue systems account for 59.7% of 2025 share; PC/console 64.1%.
3. North America + Asia-Pacific lead; "fragmented" competition, many middleware startups, engine/cloud M&A consolidation.
4. Core driver = generative-AI-driven interactive narrative; trend = cloud → on-device/edge inference to cut latency and cost.
5. Multimodal (voice→text→action) becomes modern NPC standard.
[Reusable]Segment market-share structure, on-device trend judgment (supports Macha local-first design).

---

[Category]Industry report (primary, Niko Partners)
[Title]China Gamer Behaviour and Market Insights 2025 (Niko Partners, 2025-08-27)
[Link/FilePath]https://ba.wnconf.com/news/Generative_AI/item-48683 (also see https://wnhub.io/zh/news/other/item-48683)
[One-line summary]Niko Partners survey of 1,058 Chinese players, quantifying Chinese players' awareness and interest in in-game GenAI, and studio penetration. Relevance to Macha: hard demand-side evidence for the China market.
[Key conclusions]
1. 39.4% of Chinese players interested in in-game generative AI, 85.2% already aware.
2. 60% of Chinese game studios have incorporated generative AI into development (ahead of the game).
3. Names NetEase Justice Online mobile's multimodal GenAI features (smart NPC interaction, character-customization video).
4. Short video (Douyin/Kuaishou) became the largest game-info source (41%), mini-games cover 84.4% of players.
5. Asia + MENA games software services 2024 revenue $86.6B, 2029 forecast $96B.
[Reusable]China-market demand-side data points, third-party endorsement of the NetEase case.

---

[Category]Industry viewpoint (a16z Games research)
[Title]How AI Agents Are Transforming Video Games (a16z Games research citation)
[Link/FilePath]https://gam3s.gg/news/agentic-gaming-ai-agents/
[One-line summary]Compiles a16z Games research on game-studio AI adoption and agentic gaming trends. Relevance to Macha: proves AI NPC/agents are industry mainstream, not a gimmick.
[Key conclusions]
1. 73% of studios already use AI, 88% plan to adopt; small teams (<20) 84% already using.
2. Founders most enthusiastic (85%), art roles most cautious (58%).
3. Cites "semi-autonomous NPC" precedents like Skyrim/Red Dead/Left 4 Dead/Nemesis System.
4. "Agentic gaming" defined as: AI autonomously decides, responds to player and environment, produces emergent narrative.
[Reusable]Adoption-rate data (demonstrates "real demand"), agentic gaming definition.

---

[Category]Industry research (a16z × OpenRouter)
[Title]a16z Study: Open-Source LLMs Dominate Role-Playing Games, Storytelling
[Link/FilePath]https://www.linkedin.com/posts/superprotocol_llm-api-openai-activity-7407552384924753920-TcL5 (full 36-page report link in post https://lnkd.in/gCd_xFNg)
[One-line summary]Based on OpenRouter's 100+ trillion token production traffic, reveals open-source models' biggest use is role-playing + narrative. Relevance to Macha: directly proves "chatting with / co-creating stories with virtual characters" is the #1 consumer LLM scenario, strongly related to Macha "believable NPC."
[Key conclusions]
1. Over 50% of open-source model traffic for role-playing / storytelling, not programming.
2. Open-source model share rose from <10% to ~30% in a year; DeepSeek, Qwen growing fastest.
3. Asia traffic share 13%→31%, China becomes 2nd-largest consumer after the US.
4. Medium models (15–70B) best cost-performance; "glass slipper" effect — the first model to perfectly solve the problem wins permanent loyalty.
[Reusable]Demand-scenario evidence, model-selection insight (medium open-source-first → echoes Macha cost control).

---

[Category]Industry viewpoint (a16z 2025 tech outlook)
[Title]a16z "Big Ideas in Tech 2025" (Games chapter: next-gen Pixar, AI companions with an inner world)
[Link/FilePath]https://www.y3pm.com/post/big-ideas-in-tech-2025/ (Chinese citation https://news.qq.com/rain/a/20241212A06MTE00)
[One-line summary]a16z 50 partners' annual outlook, games chapter names "AI-native interactive narrative" and "AI companions with an inner world." Relevance to Macha: gives industry direction judgment on "believable / inner-world NPCs."
[Key conclusions]
1. Next-gen "Pixar": AI-native interactive video, generates visuals in real time from player input, blurs film and games.
2. Next-gen AI companions need an "inner world": their own friends, reactions to news, motives and goals.
3. Game tech (NVIDIA graphics, Unreal real-time 3D) is spilling into commerce/autonomous-driving/defense.
[Reusable]"AI companion needs an inner world" design creed (echoes Macha memory/reflection/motive modules).

---

[Category]Industry viewpoint (Sequoia × Roblox)
[Title]Sequoia talks with Roblox generative-AI lead Stef Corazza
[Link/FilePath]https://www.toutiao.com/article/7472014623378588210
[One-line summary]Sequoia Training Data podcast, Roblox shares generating an entire world from natural language, 3D foundation model, highly vertically integrated metaverse. Relevance to Macha: benchmark case of platform-layer "AI-native creation."
[Key conclusions]
1. Future: speak one sentence via phone mic to generate an entire forest / Boss fight / game mechanic.
2. Vast majority of Roblox creators authorize use of their data for training, owning one of the largest multimodal datasets.
3. Tool success no longer depends on "how much control" but on "whether it accurately captures creative intent."
[Reusable]Platform-layer AI-native creation paradigm, emphasis on "intent capture" (Macha interface design reference).

---

[Category]Company/Product (NPC Brain)
[Title]Inworld AI Closes $50M Series A; Character Engine and Runtime
[Link/FilePath]https://martechseries.com/predictive-ai/ai-platforms-machine-learning/inworld-ai-closes-50m-series-a-to-populate-video-games-and-the-metaverse-with-interactive-ai-driven-characters/ (funding and Chinese background https://m.yfchuhai.com/article/11151.html ; Runtime https://www.ainvest.com/news/inworld-runtime-disrupting-consumer-ai-infrastructure-unlocking-scalability-generation-ai-applications-2508/ )
[One-line summary]Head of AI character platforms, multi-model orchestration Character Engine + Runtime solving prototype→production gap. Relevance to Macha: strongest NPC-brain-layer competitor/benchmark, its Runtime thinking worth borrowing for Macha.
[Key conclusions]
1. Cumulative funding ~$120M, $500M valuation, "best-funded AI+games startup."
2. Investors include Meta, Disney, Intel, Samsung, Microsoft M12, Founders Fund, etc.
3. Character Engine orchestrates 30+ ML models (multimodal character expression: emotion/memory/body language).
4. Customers/partners: Xbox, NVIDIA, Epic, Unity, Roblox, NetEase.
5. Runtime targets "prototype-to-production" scalable consumer AI infrastructure.
[Reusable]Multi-model orchestration architecture, no-code character-studio interaction paradigm, Runtime layering idea.

---

[Category]Company/Product (NPC Brain / embodied dialogue)
[Title]Convai – Conversational AI for Virtual Worlds
[Link/FilePath]http://convai.com (feature details https://www.toolmage.com/zh-hans/tool/convai ; Chinese tutorial https://inviai.com/zh-CN/you-xi-zhong-you-rengong-zhi-neng-sheng-cheng-de-jue-se-dui-hua )
[One-line summary]Developer-facing embodied conversational AI platform, multimodal perception + NPC2NPC + knowledge base + narrative design graph, supports local deployment. Relevance to Macha: important NPC-brain-layer competitor; its "knowledge base + narrative design graph + safety guardrails" is a component split Macha can reference.
[Key conclusions]
1. Multimodal perception (visual/voice/text), knowledge-base memory, graphical narrative design, NPC-to-NPC dialogue.
2. Deep integration with Unreal/Unity/Three.js; 65+ languages 500+ voices; ISO 27001, supports On-Prem.
3. Built by ex-Google/NVIDIA engineers, targets low latency, scalable to millions of users.
4. Unreal plugin still Beta; multi-agent narrative flow needs careful design.
[Reusable]Component split (Mind/Avatar/Deploy three stages), knowledge base + narrative graph + guardrails pattern.

---

[Category]Company/Product (Toolchain / digital-human tech stack)
[Title]NVIDIA ACE – Build On-Device AI Companions & Digital Humans
[Link/FilePath]https://developer.nvidia.com/blog?p=118679 (Chinese Qwen3 local deployment https://developer.nvidia.com/zh-cn/blog/nvidia-ace-adds-open-source-qwen3-slm-for-on-device-deployment-in-pc-games ; ecosystem partners https://www.ttmnq.com/news/39872.html )
[One-line summary]NVIDIA's digital-human tech stack (Riva ASR + Audio2Face + TTS + Game Agent SDK + IGI local-inference SDK), supports cloud/local. Relevance to Macha: strongest toolchain-layer infrastructure; its IGI SDK "unified inference API across GPU/NPU/CPU" is exactly the interoperable-interface prototype Macha wants to define.
[Key conclusions]
1. ACE microservices: ASR, Audio2Face, TTS, Chatterbox, Game Agent SDK.
2. Already supports open-source Qwen3-8B local deployment (IGI SDK plugin), MultiLoRA, CUDA in Graphics.
3. Adopters include Convai, Inworld, miHoYo, NetEase, Tencent, Ubisoft, ZenUnited, Seasun.
4. Combined with Inworld to "drive dynamic narrative."
[Reusable]On-device inference technical route, unified inference API design, NPC-brain combination pattern.

---

[Category]Company/Product (Big-co self-built NPC)
[Title]NetEase Fuxi: AI Agent Drives Gameplay Innovation (Justice Online smart NPC / Naraka voice AI teammate)
[Link/FilePath]https://fuxi.netease.com/database/2694 (Naraka AI teammate https://www.163.com/dy/article/KA7TFQ5M053469RG.html ; Justice Online iteration https://www.163.com/dy/article/KO0AII1605268BP2.html ; DeepSeek connection https://www.163.com/dy/article/JPH70QFQ05129QAF.html )
[One-line summary]NetEase uses AOP (Agent-Oriented Programming) framework to deploy smart NPCs and voice AI teammates, China's most mature AI NPC case. Relevance to Macha: validates "perception—cognition—decision—execution" closed loop and "long-term memory + multimodal" playability, but its solution is not open; it is what Macha wants to "standardize and open-source."
[Key conclusions]
1. AOP framework achieves perception—cognition—decision full loop; smart NPCs have memory, multimodal, affect plot direction.
2. Naraka voice AI teammate: ASR + command understanding + knowledge Q&A + persona dialogue + TTS, pathfinding 77%→99%, 300M+ social views.
3. Justice Online: 200+ smart NPCs → DeepSeek-driven "Shen Qiusuo" → 5 domestic large models forming NPC girl group; retainer system Agent-ized won 2025 Image and Graphics Society Science and Technology Progress First Prize.
4. Post-training model selection with Alibaba Cloud Tongyi, optimizing inference efficiency.
[Reusable]AOP architecture paradigm, voice AI teammate engineering chain, RLHF persona-dialogue training method.

---

[Category]Company/Product (Big-co AI-native game)
[Title]Anuttacon (Cai Haoyu) "Whispers from the Star" — AI-native interactive narrative
[Link/FilePath]https://store.steampowered.com/app/3730100/Whispers_from_the_Star/ (background https://game.xiaomi.com/viewpoint/1393220466_1742277236646_100 ; compliance https://m.moegirl.org.cn/Whispers_from_the_Star )
[One-line summary]miHoYo founder Cai Haoyu's new work, full-voice real-time AI dialogue with stranded astronaut Stella, AI-native game pioneer. Relevance to Macha: benchmark and warning of AI-native gameplay — validates demand, also exposes "lacks game framework / compliance constrained."
[Key conclusions]
1. Released Steam 2025-08-14, 82% positive (~1,557 reviews), ~30K copies.
2. Full voice/text/video real-time open dialogue, every line affects plot and character fate.
3. Controversy: reviewed as "like a big C.AI toy," lacks game framework; deactivated mainland social accounts because domestic AI model unfiled (~2025-12).
4. Cloud-gaming model, low ¥33.99 price, suspected of collecting AI data through play.
[Reusable]AI-native gameplay paradigm, compliance-risk warning (B5 real case).

---

[Category]Product case (AI GM pioneer / cost negative example)
[Title]AI Dungeon / Latitude – Open text adventure and the pain of cost
[Link/FilePath]https://app.dealroom.co/companies/latitude_1_1 (profitability status https://m.huxiu.com/article/4694133.html ; wiki http://en.m.wiki2.org/wiki/AI_Dungeon )
[One-line summary]Earliest AI GM text adventure, validated open-narrative demand, also nearly bankrupt from GPT-3 API costs. Relevance to Macha: earliest blood-and-tears evidence of B1 cost bottleneck, directly shows "standard skeleton must have cost control built in."
[Key conclusions]
1. Launched 2019, 100K in a week, 1.5M users in half a year; 2021 raised $3.3M seed (NFX led).
2. Early on, OpenAI API cost exploded exponentially, nearly bankrupt; later introduced low-cost models + context limits to stop bleeding.
3. Delisted from Steam 2024; 2025 reached ~$7M annual revenue profitable with 12-person team.
4. Once sparked moderation/ethics controversy as 31% of generated content involved violence/porn (insufficient GPT-3 constraints).
[Reusable]Cost-runaway case, content-moderation/guardrail necessity evidence.

---

[Category]Product case (AI-native party game)
[Title]Suck Up! (Proxima) — Zero-marketing 100M-view AI NPC game
[Link/FilePath]https://www.huafengwang.net/djgl/68029.html (review https://www.howtogeek.com/these-games-prove-theres-a-right-way-to-use-modern-ai-in-gaming ; team retrospective https://www.linkedin.com/posts/nicholasozak_we-developed-and-released-suck-up-quietly-activity-7158155765583659008-Hycz )
[One-line summary]Vampire knocks on doors, each door an AI NPC driven by ChatGPT, zero-budget YouTube 100M+ views. Relevance to Macha: proves "AI just makes a shareable interactive structure happen faster," Macha should serve "interactive structure" not just "dialogue."
[Key conclusions]
1. Launched 2023-12 with zero promotion, 20M+ YouTube views in a month, 100M+ cumulative across platforms.
2. Only reached full 1.0 on Steam 2025-10-01 (achievements/workshop/challenge mode).
3. Core is not "used AI" but "an interactive structure that can be infinitely copied, watched, spread."
4. Each NPC has personality/doubt/unpredictable reactions; player's only tool is "a mouth."
[Reusable]AI-native game design methodology (structure > model), viral-spread mechanism.

---

[Category]Product case (AI-native reasoning / crash contrast)
[Title]Vaudeville and Square Enix "Port Town Serial Murder" AI version
[Link/FilePath]Vaudeville: https://www.howtogeek.com/these-games-prove-theres-a-right-way-to-use-modern-ai-in-gaming ; Square Enix: https://www.vice.com/en/article/square-enixs-ai-tech-demo-is-a-staggering-failure (Chinese https://www.sohu.com/a/669770907_121143647 )
[One-line summary]Two "open-dialogue NPC" cases: Vaudeville stunning concept but unstable AI quality; Square Enix crashed outright (8–12% positive). Relevance to Macha: negative example of B3 controllability + B2 latency/performance + B1 cost triple failure.
[Key conclusions]
1. Vaudeville: cookie-cutter characters, non-sequiturs, self-contradictions, can't sustain complex murder mystery.
2. Square Enix: local NLP took 10GB, needed 5GB VRAM, GPU froze; NPCs poor comprehension, became "word-guessing game."
3. SE disabled NLG (natural language generation) due to ethical concerns, making AI "not smart."
4. Only 8–12% positive, among "lowest ever"; players said "worse than original text parser."
[Reusable]Negative checklist for controllable generation / validation layer / performance budget (Macha guardrail module must-haves).

---

[Category]Product case (AI-native semantic adjudication)
[Title]Infinite Craft (Neal Agarwal) — LLaMa-driven "combination" sandbox
[Link/FilePath]https://leedsjournal.co.uk/infinite-craft (AI-native game classification https://arxiv.org/html/2607.00527v1 )
[One-line summary]Browser sandbox, uses LLM for "semantic adjudication" (whether combining items is valid / what to generate). Relevance to Macha: more stable AI-native paradigm than "chat NPCs," echoes AI-Native paper "semantic adjudication" axis, expands Macha's view of "AI gameplay beyond NPCs."
[Key conclusions]
1. Launched 2024-01, from four elements infinite combinations, ~300M recipes/day.
2. Uses LLaMa backend to ensure combination consistency yet surprising.
3. 2025-05 added "Combo Archive," community-driven, has Story Mode plan.
4. AI-Native paper classifies it as "Sandbox/craft + Semantic adjudication."
[Reusable]"Semantic adjudication" as a stable AI gameplay paradigm (Macha evaluation/design-theory layer reference).

---

[Category]Engineering practice (cost/latency/architecture)
[Title]LLMs in Games: 5 Studio-Killing Problems & Async Dynamic Narrative Service Layer
[Link/FilePath]Gladecore: https://www.gladecore.com/blog/llms-in-games ; ByteDance architecture: https://youthcamp.bytedance.com/post/7584073390694547471 ; CSDN brainstorm: https://adg.csdn.net/696f265b437a6b4033697da1.html
[One-line summary]Front-line teams summarize five LLM-in-games deadly problems (cost model/latency/customization/integration friction/compliance), propose "async dynamic narrative service layer" and "generative NPC behavior system" architecture. Relevance to Macha: almost the engineering-version evidence of Macha's architecture blueprint.
[Key conclusions]
1. Five problems: token billing punishes success, cloud 1–3s latency, customization limited, SDK friction, offline/privacy/GDPR.
2. ByteDance solution: wrap LLM as async/queueable/cacheable independent service layer + smart routing (cache/light model/cloud large model) + narrative state store + safety gateway.
3. CSDN solution: local small model + cloud async + pre-gen cache + behavior framing + strong-constraint prompt + structured output + validation layer + FSM/behavior-tree fallback.
[Reusable]**Can be directly converted to Macha architecture modules**: tiered routing, cache, narrative-state DB, safety gateway, validation layer, degradation strategy, behavior-tree fallback.

---

[Category]Academic paper (AI-native game classification)
[Title]AI Native Games: A Survey and Roadmap (arXiv 2607.00527v1)
[Link/FilePath]https://arxiv.org/html/2607.00527v1
[One-line summary]Systematically reviews 53 AI-native games, proposes trends and classification axes of "hybridization" and "from dialogue agents to world/mechanic-level AI." Relevance to Macha: provides AI-native game design ontology and classification system, supports Macha design-theory layer.
[Key conclusions]
1. Three current trends: pure-text continuation → task-oriented gameplay; AI-native increasingly "hybrid" (generative model + authored goals/constraints/validation/cache); field still uneven (consistency/latency/evaluation/moderation/cost/replay-depth common hard problems).
2. Most common pattern is not fully-automatic world simulation but "constrained gameplay loop," AI plays specific role (suspect/referee/GM/character/generator).
3. Lists 53 games with Suck Up!/Vaudeville/Infinite Craft etc. by year and type axis.
[Reusable]AI-native game classification table, hybrid design paradigm, "constrained loop" methodology.

---

[Category]Review (2025 industry culture tug-of-war)
[Title]Generative AI in Gaming 2025: Human vs. Machine Game Design Review
[Link/FilePath]https://www.nexaspecs.com/2025/12/generative-ai-in-gaming-2025-human-vs.html
[One-line summary]Reviews 2025 generative AI moving from tech curiosity to industry pillar yet sparking "soul/employment/ethics" controversy tug-of-war. Relevance to Macha: reminds Macha standard to include "transparency/labeling/human oversight" dimensions to respond to community resistance (B7).
[Key conclusions]
1. 2025 is the turning year where GenAI went from curiosity to industry pillar but was highly controversial.
2. Players doubt "AI narrative lacks thematic depth and intent," "hand-crafted" becomes a quality label.
3. Industry pushes AI-use transparency disclosure.
4. Technical challenges: consistency, performance, evaluation remain core.
[Reusable]Community-acceptance dimensions (transparency/labeling), "human + AI" hybrid positioning.

---

## Appendix: Sources Not Obtained Primary / Pending Verification (Honest Disclosure)

- **Newzoo original paid report**, **Toulie Research original report**: this time only obtained secondary data via a CSDN blogger's compilation; market-size numbers suggest tracing primary sources.
- **a16z Game Fund ONE scale (~$600M)**: from a Chinese long-form article (URL missing), could not obtain a16z official page corroboration; please verify before citing.
- **Game AI NPC Market's $1.25B→$5.19B**: from pmarketresearch vendor estimate, not neutral third party, magnitude reference only.
- **miHoYo "Anuttacon $500M" "Glossa large model"** and other details: from Chinese media reviews, partly unconfirmed officially, suggest using miHoYo/Anuttacon official disclosures.
- **Whispers from the Star domestic account deactivation**: from a Chinese wiki-style entry, timeline (2025-12) needs secondary confirmation.

---

> **Compilation note**: All external links in this brief are pages actually hit during this search. If Macha later needs to cite specific numbers for external materials, please prioritize tracing the "pending verification" primary sources in the table.

---

## 5. Deepening Supplement: Quantified Market and Domestic Special (2025–2026 Additive Update)

> This section is an **additive deepening** of the original framework, not changing any conclusion above. The goal is to ground the qualitative judgment "five/eight bottlenecks = Macha white space" in **citable numbers, real funding, cost magnitudes, and the domestic special**. All numbers are labeled with source and caliber; secondary/vendor estimates are explicitly noted.

### 5.1 Market Size and Growth (Quantified, with CAGR, Multi-Caliber Comparison)

> ⚠️ Caliber-difference reminder: different institutions define and bound "games AI / generative-AI games / AI NPC" very differently (see table below); **do not directly add numbers of different calibers**. But all calibers point to one conclusion: the overall games market growth has peaked (single digits), while AI-related segments maintain **20%–35% magnitude high CAGR**.

| Metric / caliber | Value and growth | Source | Note |
|---|---|---|---|
| Global games market (2025) | **$188.8B**, **+3.4%** YoY; players **3.58B** | Newzoo "Global Games Market Report 2025" | Mobile $103.0B / console $45.9B / PC $39.9B |
| Global games market (2028 forecast) | **$206.5B**, 2025–2028 **CAGR +3.0%** | Newzoo (same) | "Mature but not stagnant," growth from retention and ecosystem |
| China games market (2025) | Actual sales ¥350.79B, **+7.68%** YoY; users **683M** | "2025 China Games Industry Report" (GPC/CGIGC) | Growth significantly above global |
| Generative AI games market | 2025 **$1.79B** → 2026 **$2.21B** (**CAGR 23.1%**) → 2030 **$5.09B** (**CAGR 23.2%**) | The Business Research Company / ResearchAndMarkets "Generative AI in Gaming Market 2026" | 2025 Asia-Pacific largest region |
| Generative AI in games (narrow caliber) | 2024E 15 → 2025E 18 → 2026E 22 → 2030E 55 → 2033E **$11B** (~**25% CAGR**) | market.us / Open Source Securities Research | Small caliber, magnitude reference |
| AIGC games | 2025 **$4.54B**, 2025–2033 **CAGR 33.57%** | DataInsightsMarket | Includes assets/levels/narrative generation, wider scope |
| Game AI NPC segment | 2025 **$1.25B** → 2032 **$5.19B**, **CAGR 22.58%** (LLM dialogue 59.7%) | pmarketresearch (cited §1.2) | Vendor estimate, magnitude reference |
| NPC AI market (independent research) | 2029 **$5.51B** | Research & Markets (via industry report) | Trace primary |

**Interpretation**: Regardless of caliber, the CAGR of AI-games segments (22%–34%) is **5–10×** that of the overall games market (3%–7%). The "AI NPC / agent interaction" Macha targets is one of the largest-share, most-certain-growth directions within it — this is the key to turning "white space" from vision into "calculable TAM."

### 5.2 Funding Map (Real Amounts, 2021–2026)

> Units are USD unless otherwise noted. Valuations and rounds per company announcements / mainstream databases (Crunchbase-class, PitchBook-class citations); items marked "verify" please trace primary.

| Company | Round | Time | Amount | Valuation/cumulative | Lead / key investors | Note |
|---|---|---|---|---|---|---|
| **Inworld AI** | Seed | 2021-11 | $7M | — | KPCB, CRV, M12, etc. | Absolute NPC-brain leader |
| Inworld AI | Series A | 2023-08 | **$50M** | Valuation **$500M** ("halficorn") | Lightspeed led; Meta, Disney, Intel, Samsung, M12, Founders Fund | Among best-funded AI×games startups |
| Inworld AI | Cumulative | to 2023 | **≈$100–130M** | 5 rounds | — | startupintros lists $133M; industry report lists $125.7M |
| Inworld AI | Strategic | 2023– | Non-equity | — | **Microsoft Xbox** (multi-year) | AI design Copilot + in-game AI engine |
| **Convai** | Seed | Late 2022 | **$2.5M** | — | — | Embodied dialogue NPC engine |
| Convai | Valuation (secondary) | 2022-12 | — | Valuation **$21M** (UpMarket model) | Mostly self-funded | 2024 revenue ~**$6.5M** (UpMarket, verify); Unity store installs 270K+ |
| **Volley** | Series C | 2024-07 | **$55M** | Cumulative **>$75M** | **Microsoft M12 + Lightspeed** led | Voice AI games (Jeopardy!/Wheel of Fortune on Alexa/Fire TV) |
| Volley | Operations | 2024 | ARR **>$30M** (2× YoY) | MAU **5M** | — | Charges $9.99–12.99/month |
| **Altera** (now Fundamental Research Labs) | Pre-seed | 2023-12 | $2M | — | a16z led | Minecraft thousand-agent civilization Project Sid |
| Altera | Seed | 2024-05 | **$9M** | — | First Spark + Patron (a16z Speedrun, Eric Schmidt) | |
| Altera | Series A | 2025-08 | **$33M** | Cumulative **>$40M** (fundbat lists $44M) | **Prosus** led; a16z Speedrun, Patrick Collison | From game agents to general digital-human / office agents |
| **NVIDIA** | Strategic | ongoing | Not this round | — | Invested in Luma AI, Inworld, etc. | ACE ecosystem expands via tech + hardware binding, not funding race |
| **miHoYo** | Strategic | 2026-05 | Three-year max **¥100B** AI investment | — | Own | Anuttacon (¥500M) incubated; full-stack self-developed route |
| **Kaiying Network** | Strategic | 2025-07 | Introduced Brilliant (Stephen Chow) group investment | — | Brilliant subsidiary | Incubated "Xingyi" large model and AI game-engine company Jiyi (SOON platform) |
| **Giant Network** | Filing | 2025-12 | GiantGPT completed generative-AI filing | — | Own | **First vertical large-model filing in domestic games industry** (character acting / scenario reasoning / long-term memory) |

**Interpretation**: Global AI×games funding is highly concentrated in the "NPC brain / platform" layer (Inworld, Volley, Altera), and **strategic capital (Microsoft M12, Prosus, a16z, Lightspeed, Disney, Meta) is deeply in the game** — meaning big companies are either self-building or staking claims; investment in the independent third-party "standard skeleton" layer is still blank, exactly Macha's fundraising/ecosystem narrative space. On the domestic side it is **big-company own investment + vertical large-model filing race** (Giant, Kaiying, 37 Interactive "Xiaoqi", Perfect "Tiangong"), with no open standard layer yet appearing.

### 5.3 Cost Structure Breakdown: Cloud-Hosted NPC $/month/player Magnitude Estimate

> Below is a **magnitude summary** of public engineering/investment estimates (not Macha measured). Core conclusion is highly consistent: **pure-cloud token billing is unsustainable at scale**, must go "local small model + cloud fallback + high cache hit" hybrid architecture — exactly the engineering basis for Macha "Gap Two: cost/latency as first-class citizens."

| Cost dimension | Magnitude ($/month/player or equiv) | Source | Condition |
|---|---|---|---|
| **Per-turn dialogue cost** | **$0.001–$0.10** (GPT-4o mini single exchange ≈ $0.0075–$0.015) | theneuralbase (cost-per-conversation) | Depends on model and cache; 100K concurrent chatting once/day ≈ $22K–$45K/month |
| **Pure-cloud inference (heavy dialogue)** | **$10–$50 / MAU / month** (200–400 API calls/session) | theneuralbase (latency-optimization) | Cloud-dominant; 1M-player game burns **$500K–$2M/month** |
| **Edge/on-device inference** | **$0.50–$2.00 / player / month** (regional inference cluster) | theneuralbase (same) | Local/edge, key to profitability |
| **VC framework estimate** | $0.30–$2.25/session (10 calls/min × 30 min × 500 tok × $2–15/M) → $3–$22.5/player/month; 100K MAU = **$300K–$2.25M/month** | Dre Dyson (VC diligence framework) | vs. mobile ARPU $0.5–2/month → **AI cost can exceed revenue 10×** |
| **Hybrid cost reduction proof** | A combo went from **$1.80 → $0.12 / player / month** (≈$18M saved over 3 years) | Dre Dyson (same) | Local + cloud hybrid |
| **Model price gap (output token)** | GPT-4o $10.00/M vs GLM-4 Plus $0.80/M = **12.5×**; 400M output tokens/month = **$3.6M/month** gap | dev.to production test (2026) | Domestic models (DeepSeek/GLM/Qwen) stand out on cost-performance |

**Conclusive formula (for Macha architecture)**:
- Cost ≈ `call volume × (local share × near-zero + cloud share × unit price) × (1 − cache hit rate)`
- To make AI NPCs profitable at million-level MAU, **cache hit rate must be >70%** (real-session test after one week), **local/edge must carry >80% of routine dialogue**, cloud only falls back for complex generation. This perfectly matches the "tiered routing + pre-gen cache + behavior-tree fallback" proposed in §2.5/§3.

### 5.4 China-Market Special: Domestic AI NPC and Platform Deep Cases

#### 5.4.1 NetEase Fuxi (AOP framework, most mature domestically, strongly internally bound)
- **Technical route**: AOP (Agent-Oriented Programming) — perception→cognition→decision→execution closed loop; persona-dialogue large model via RLHF; reinforcement learning optimizes pathfinding (77%→99%).
- **Deployed products/games**:
  - Justice Online mobile: smart NPCs (long-term memory/emotion/dynamic plot), retainer system (**whole-server player-built AI retainers exceed 40M**), film-crew mode (in-game 3D short video), AI crayfish (2026-07 gold smooth-play server launch, offline hosting auto-tasks, official compliant anti-bot).
  - Naraka: Bladepoint mobile: industry-first voice AI teammate; **PC version became first domestic game with ACE + large model on-device AI teammate** (2025-03-27).
  - All-Star Street Ball Party: AI agent "tactics brain," RL-trained basketball bots of different styles.
- **Investment and results**: 2025 R&D investment **¥17.7B** (over ¥10B for six consecutive years, over ¥80B cumulative in 5 years); AI gameplay raised users' average daily interaction time **+40%**.
- **For Macha**: strongest "brain" proof, but **strongly internally bound, not standardized for external use** — exactly what Macha wants to "open-source, engine-agnostic."

#### 5.4.2 miHoYo / Anuttacon (dream-building faction, 2026 strategic-retraction living textbook)
- **In-game AI**: Honkai: Star Rail "Pam AI assistant" real-time dialogue, Star Burst Valley second-beta AI NPCs (can serve multiple players simultaneously, with complete memory/identity/social capability).
- **Flagship bet**: next-gen urban open world Varsapura (Cai Haoyu as producer himself), 2026-05 announced **three-year max ¥100B AI investment**, full-stack self-developed.
- **Anuttacon real lessons (2026)**:
  - Whispers from the Star positive rating fell from 82% **to ~35%**, subsequent development slowed.
  - AI companion product **AnuNeko shut down within a year of launch**; **BSide: Olivia Lin shut down within a month of launch**.
  - Cai Haoyu LinkedIn identity updated to "Independent LLM + Agent Developer," shifting from general AI apps to **LLM/Agent**.
- **For Macha**: negative-evidence chain — confirms **B3 controllability** (open generation can't sustain long-term goals/plot), **B5 compliance** (domestic model filing), "**lacks game framework = like a big C.AI toy**". miHoYo's ¥100B investment shows the direction is right, but its trajectory of "frequent application-layer trial-and-error, retraction to foundation models" precisely proves the industry lacks a reusable **standard skeleton**, not another Demo.

#### 5.4.3 Tencent (Hunyuan / GiiNEX / GameMate, most aggressive at scale)
- **Technical route**: Hunyuan large model (Xiaotian driven by **Hunyuan 3 preview**) + GameMate 1.0 framework + GiiNEX dual engine + Hunyuan 3D; strategy model trains same-day with same-day feedback agile production-research.
- **Deployed products/games**:
  - Peacekeeper Elite AI teammate "Jidi Zhihui": **cumulative experience users 110M, peak weekend DAU 17.7M**; star teammate "Xiaotian" (2026-05-28) industry-first emotional-companion AI teammate; **mic open rate ≈75%, 70 interaction messages per match**; AI war dog "Bruce" tactical coordination.
  - Oasis Genesis (UGC): industry-first "UGC full-chain AI creation assistant," **Spring Festival DAU broke 58M, 200K online maps**, players land ideas in 15 minutes.
  - Honor of Kings AI teammate system player satisfaction **+35%**; Delta Force AI-generated maps **cut dev cycle 40%**.
  - Code Craft (SPARK 2026): natural-language game generation, one-click export to Unity; **GDC 2026 led all vendors with 21 sessions**; over 40 games already deployed AI.
- **For Macha**: proves AI NPC commercial loop works under "large DAU + high concurrency + low latency" (retention glue), but its capability is **locked in Tencent's ecosystem**; Macha can borrow its "scenario packaging + knowledge base + strategy model" engineering paradigm.

#### 5.4.4 Kaiying Network (Xingyi / Zhimeng / SOON, most complete AI-industrialization pipeline)
- **Technical route**: "Xingyi" large model covers animation/scene/numerics/code/UI/map generation; "Zhimeng" large model (Transformer, story script) completed filing; **deeply connected to DeepSeek R1**; Jiyi company SOON AI full-process dev platform (art→code deployment automation, dev cycle **from months down to hours**).
- **Capital/layout**: 2025-07 introduced Brilliant (Stephen Chow) group investment; invested in Natural Selection pushing 3D AI digital companion "EVE", Dapeng (DPVR) AI glasses.
- **For Macha**: represents "AI industrialization efficiency" route (stock efficiency gains + incremental companionship), complementary to Macha "Gap Two/Three" — Macha can absorb its "full-process generation" as an upper-layer tool, while the underlying cognitive architecture is still defined by the standard skeleton.

#### 5.4.5 Other domestic vertical models (breadth supplement)
- **Giant Network GiantGPT**: completed generative-AI filing 2025-12, **first vertical large model in domestic games industry** (character acting / scenario reasoning / long-term memory), already tested in the Zhengtu series; "AI dummy" gameplay Q1 2026 participation broke 400M matches, generated over 2.9B AI dummies.
- **37 Interactive "Xiaoqi"**: employee AI coverage 100%, 2D art AI share >80%, ad-video AI participation >70%; incubated Mingyue Gongxin AI-native mini-game (2–3 people, 10 days per game).
- **Perfect World "Tiangong"**: self-developed games large model, deeply embedded in R&D and experience.
- **ByteDance**: public materials mainly the **async dynamic narrative service layer** architecture paradigm (tiered routing + cache + narrative-state store + safety gateway, see §4 Gladecore/ByteDance sources); independent external NPC product not yet at scale, suggest engineering paradigm not product benchmark.

### 5.5 Quantified Bottleneck Map: Each Player's Tech Route × Eight Bottlenecks Comparison

| Player | Model strategy | Deployment | Long-term memory | Controllability/guardrails | Compliance (filing) | Open standard | Cost structure | Main bottleneck |
|---|---|---|---|---|---|---|---|---|
| **Inworld** | Multi-model orchestration (self+external) | Cloud-dominant | Strong (Character Engine) | Medium (self-managed) | Weak (cross-border) | No (ecosystem lock) | High (B1) | B1/B2/B5 |
| **Convai** | External LLM + knowledge base | Cloud/local | Medium | Strong (KB+guardrails) | Medium (ISO27001/On-Prem) | No | Medium | B1/B3 |
| **Volley** | GPT-4o-class voice stack | Cloud | Weak (single match) | Weak (open gen) | Weak | No | High (subsidy via subscription) | B1/B3 |
| **Altera** | Self-built Agent | Cloud | Strong (civilization-level) | Medium | Weak | No | High | B1/B4 |
| **NetEase Fuxi** | Self-built large model (AOP) | Cloud+edge (ACE) | Strong | Strong (RLHF+BT) | Strong (domestic) | No (internal) | Medium (big-co amortized) | B6 (integration) |
| **Tencent Hunyuan** | Self-built Hunyuan + strategy model | Cloud+edge | Strong (Xiaotian memory) | Strong (KB+switch) | Strong (filed) | No (ecosystem) | Medium (big-co amortized) | B2 (high concurrency) |
| **miHoYo** | Glossa + self-built | Cloud-dominant | Medium | Weak (trial-retract) | Medium (unfiled constrained) | No | High (own investment) | B3/B5 |
| **Kaiying Xingyi** | Self-built vertical + DeepSeek | Cloud | Medium (script gen) | Medium | Strong (filed) | No | Low (efficiency) | B8 (production) |
| **NVIDIA ACE** | Distilled SLM + multi-model | **Edge-first** | Medium | Strong (toolchain) | Medium | Half (IGI SDK API) | Low (edge) | B2/B1 |
| **Macha (target)** | Pluggable / open-source | **Local-first + cloud fallback** | **Structured memory** | **Built-in guardrails + validation layer** | **Local-first compliance** | **Yes (MCP-style protocol)** | **Lowest hybrid** | All B1–B8 |

**One-line conclusion**: Existing players made trade-offs on almost all seven dimensions of "model self-build, deployment, memory, guardrails, compliance, open standard, cost," and **no one occupies all simultaneously**; NVIDIA ACE is closest on "edge cost-down/latency-down" but still locks the hardware stack. **The only unoccupied cell is the bottom-right "open-source + engine-agnostic + cost/latency/memory/control/compliance as default-capability standard skeleton" — this is Macha's quantified white space.**

### 5.6 Re-confirmation for Macha (continuing §3)

1. **TAM calculable**: using "game AI NPC segment 2025 $1.25B → 2032 $5.19B (CAGR 22.58%)" as conservative floor, plus the generative-AI-games 23% CAGR macro trend, Macha as a "standard skeleton" should extract the **middleware/platform take-rate layer**, not compete with the application layer for profit.
2. **Cost argument closed loop**: §5.3 magnitude estimates prove "AI NPC without built-in cost control = the more successful, the more you lose"; Macha's "local-first + cache >70% + hybrid architecture" is not optional, it is a **life-or-death line**.
3. **Domestic window**: Giant/Kaiying/37 vertical-model filings, Tencent/NetEase scale deployment, show the domestic market is already overheated and **strongly ecosystem-locked**; if Macha takes the "open standard + domestic-model-friendly (DeepSeek/GLM/Qwen cost-performance 12.5×)" route, it can become the de-facto interface layer in the fragmented domestic landscape.
4. **Warning assets**: miHoYo Anuttacon's 2026 retraction, Whispers positive 82%→35%, are the hardest negative examples for Macha "Gap Three/Four (controllability, guardrails)," and should be written into the evaluation benchmark.

---

### 5.7 Source Collection (Deepening Supplement, Per Team Six-Field Format)

> Below are pages actually hit during this deepening search; vendor estimates / secondary valuations all marked "verify."

---

[Category]Industry report (primary, Newzoo)
[Title]Global Games Market Report 2025 — Market to hit $189 billion in 2025
[Link/FilePath]https://newzoo.com/articles/global-games-market-189-billion-2025
[One-line summary]Newzoo 2025 flagship report: global games market 2025 reaches $188.8B (+3.4%), 2028 forecast $206.5B (CAGR 3.0%), players 3.58B. Relevance to Macha: provides overall games-market growth (single digit) as baseline contrasting AI-segment high CAGR.
[Key conclusions]
1. 2025 global games $188.8B (+3.4%); mobile $103.0B, console $45.9B, PC $39.9B.
2. 2028 forecast $206.5B, 2025–2028 CAGR only 3.0%, market mature.
3. Players 3.58B (+4.4%), mobile 3.0B.
4. US and China each ~$49.8B / $49.6B in 2025, together half the global.
5. Growth from retention, multi-device, UGC ecosystem, not new players.
[Reusable]Overall-market CAGR baseline, platform split, player base (feeds Macha market chapter).

---

[Category]Industry report (primary, GPC/CGIGC)
[Title]2025 China Games Industry Report
[Link/FilePath]Cited via Tanwan annual report (https://www1.hkexnews.hk/listedco/listconews/sehk/2026/0327/2026032703488.pdf )
[One-line summary]2025 China domestic games market actual sales ¥350.79B (+7.68%), users 683M (+1.35%). Relevance to Macha: China market size and growth significantly above global, important foundation for Macha domestic route.
[Key conclusions]
1. 2025 China games actual sales ¥350.79B, +7.68% YoY.
2. Game users 683M, +1.35% YoY.
3. 2025 state issued "Network Publishing Tech-Innovation Leadership Plan" supporting AI/big-data/cloud/blockchain R&D.
4. "15th Five-Year" plan encourages cultural-tech enterprises' international operations, digital empowerment.
5. Domestic market growth is 2×+ the global (3%).
[Reusable]China-market size hard data, policy-tailwind signal (supports Macha domestic-compliance route).

---

[Category]Industry report (vendor / research institute)
[Title]Generative AI in Gaming Market Report 2026
[Link/FilePath]https://www.thebusinessresearchcompany.com/report/generative-ai-in-gaming-global-market-report (mirror https://www.researchandmarkets.org/report/global-generative-ai-in-gaming-market )
[One-line summary]Generative AI games market 2025 $1.79B → 2026 $2.21B (CAGR 23.1%) → 2030 $5.09B (CAGR 23.2%), Asia-Pacific largest. Relevance to Macha: provides quantified CAGR of "generative AI games" track, corroborates high growth.
[Key conclusions]
1. 2025 $1.79B, 2026 $2.21B (CAGR 23.1%), 2030 $5.09B (CAGR 23.2%).
2. 2025 Asia-Pacific largest region.
3. Drivers: AI content-creation adoption, cloud gaming, VR/AR, personalized experience, metaverse readiness.
4. Trends: procedural levels, real-time character-behavior modeling, adaptive gameplay, dynamic content personalization, AI testing.
5. Key players include Microsoft, EA, Square Enix, Ubisoft, Unity, Tencent, NetEase, etc.
[Reusable]Generative AI games CAGR, feature split (NPC is a sub-item).

---

[Category]Industry estimate (broker / third-party, narrow caliber)
[Title]Global generative AI in games market size 2024–2033 (US$100M)
[Link/FilePath]Open Source Securities Research / market.us, via ima knowledge base (https://ima.qq.com/wiki/?shareId=d548021a437cf2f7992008afcfebd3b361bece8d8d19985a0e0f5c4acc91de31 )
[One-line summary]Narrow-caliber estimate: generative AI games 2024E 15 → 2025E 18 → 2033E 110 (≈25% CAGR). Relevance to Macha: as another caliber cross-validating high growth, but small caliber, cite with note.
[Key conclusions]
1. 2024E 15, 2025E 18, 2026E 22, 2027E 28, 2028E 35, 2029E 45, 2030E 55, 2031E 70, 2032E 88, 2033E 110 (US$100M).
2. ~25% CAGR over nine years.
3. Caliber clearly smaller than The Business Research Company's $1.79B (2025), showing large definition-boundary differences.
4. Need to trace market.us primary report to confirm scope.
[Reusable]Long-period forecast curve (magnitude reference, note caliber).

---

[Category]Company/Product (NPC Brain, funding)
[Title]Inworld AI Funding, Team & Investors (cumulative $133M, $500M valuation)
[Link/FilePath]https://startupintros.com/orgs/inworld-ai (Industry Report summary https://simonaking.com/blog/ai-interactive-film-game-report )
[One-line summary]Inworld AI cumulative funding ~$100–130M, 2023-08 Series A $50M, $500M valuation ("halficorn"), multi-year Microsoft Xbox partnership. Relevance to Macha: strongest NPC-brain-layer competitor, funding and valuation numbers can go into Macha competitive-map comparison.
[Key conclusions]
1. 5 rounds cumulative ~$133M; 2023-08 Series A $50M (Lightspeed led), $500M valuation.
2. Investors include Meta, Disney, Intel, Samsung, M12, Founders Fund, etc.
3. Character Engine orchestrates 30+ ML models; Runtime bridges prototype→production.
4. Microsoft multi-year partnership: Xbox AI design Copilot + in-game AI engine.
5. Industry report lists cumulative $125.7M, $500M valuation, best-funded AI-games startup.
[Reusable]Funding amount/valuation, customer and partner list (competitive-map data).

---

[Category]Company/Product (NPC engine, funding/operations)
[Title]Convai — Seed $2.5M, mostly self-funded, 2024 revenue ~$6.5M
[Link/FilePath]https://businessmodelcanvastemplate.com/blogs/brief-history/convai-brief-history (secondary valuation https://www.upmarket.co/private-markets/pre-ipo/convai-zh/ )
[One-line summary]Convai late-2022 Seed $2.5M, mostly self-funded, UpMarket model valuation $21M (secondary, verify), 2024 revenue ~$6.5M. Relevance to Macha: embodied-dialogue NPC engine competitor, component split (Mind/Avatar/Deploy) reference.
[Key conclusions]
1. Late-2022 Seed $2.5M; mostly self-funded, no large VC.
2. UpMarket secondary valuation model $21M (Seed, 2022-12), verify.
3. 2024 revenue ~$6.5M (UpMarket tracking, verify).
4. Unity store installs 270K+; CES 2024 NVIDIA keynote appearance.
5. Multimodal perception (visual/voice/text) + knowledge base + NPC2NPC.
[Reusable]Three-stage component split, self-funded path reference (Macha open-source route contrast).

---

[Category]Company/Product (voice AI games, funding)
[Title]Volley Raises $55 Million (Series C, Microsoft M12 + Lightspeed led)
[Link/FilePath]https://www.orrick.com/zh-TW/News/2024/07/Artificial-Intelligence-and-Gaming-Volley-Raises-55-Million (Chinese https://new.qq.com/rain/a/20240712A0ACJS00 )
[One-line summary]Volley 2024-07 Series C $55M (Microsoft M12 + Lightspeed led), cumulative >$75M, ARR >$30M, MAU 5M. Relevance to Macha: most commercially successful voice-AI-game startup, subscription-cost-subsidy model contrast.
[Key conclusions]
1. Series C $55M, Microsoft M12 and Lightspeed led, cumulative >$75M.
2. ARR >$30M (2× YoY), MAU 5M, charges $9.99–12.99/month.
3. Products: Jeopardy!/Wheel of Fortune/Song Quiz etc. Alexa/Fire TV voice games.
4. Uses GPT-4o-class multimodal model replacing "transcribe→LLM→TTS" multi-step pipeline, 3× faster.
5. Experimenting with LLM-driven personalized virtual characters (AI companion direction).
[Reusable]Voice AI games commercial model, subscription-cost-subsidy idea.

---

[Category]Company/Product (Agent, funding)
[Title]Fundamental Research Labs (formerly Altera) Secures $33M Series A (Prosus led)
[Link/FilePath]https://cbg.com.cy/fundamental-research-labs-secures-over-30m-to-expand-ai-agent-development-across-industries (data https://fundbat.com/company/altera )
[One-line summary]Altera/Fundamental Research Labs: Pre-seed $2M (2023, a16z), Seed $9M (2024), Series A $33M (2025-08, Prosus led), cumulative >$40M; Project Sid thousand-agent civilization. Relevance to Macha: long-term autonomous-agent route reference, but its game integration not yet productized.
[Key conclusions]
1. Pre-seed $2M (2023-12, a16z led); Seed $9M (2024-05, First Spark+Patron, a16z Speedrun, Eric Schmidt); Series A $33M (2025-08, Prosus led, cumulative >$40M).
2. Project Sid: 1000+ autonomous agents form civilization (economy/governance) in Minecraft.
3. Products expanded from game bots to Fairies (general agent), Shortcut (Excel agent).
4. Founder Robert Yang (MIT), positioned as "digital humans."
5. Game side still research/demo, no commercial game integration proven.
[Reusable]Long-term autonomous-agent architecture idea, multi-agent civilization experiment data.

---

[Category]Engineering practice (cost magnitude estimate)
[Title]Cost per conversation / Latency optimization for live NPC inference
[Link/FilePath]https://theneuralbase.com/ai-for-gaming/learn/beginner/cost-per-conversation (latency/edge https://theneuralbase.com/ai-for-gaming/learn/intermediate/latency-optimization/ )
[One-line summary]Quantifies cloud NPC inference cost: per-turn dialogue $0.001–$0.10; pure-cloud heavy dialogue $10–$50/MAU/month; edge $0.50–$2.00/player/month; 1M players cloud-only burns $500K–$2M/month. Relevance to Macha: directly supports "Gap Two: cost as first-class citizen" magnitude argument.
[Key conclusions]
1. Single exchange GPT-4o mini ≈ $0.0075–$0.015; cache can cut cost 60–80%.
2. Cloud heavy dialogue $10–$50/MAU/month; edge $0.50–$2.00/player/month.
3. 1M players pure-cloud monthly cost $500K–$2M, on-device nearly mandatory.
4. Quantified 1–3B model local inference 15–40ms; cache pre-gen dialogue 0.1ms lookup.
5. Hybrid: on-device combat/movement, edge dialogue, cloud async narrative generation.
[Reusable]Cost formula, hybrid-deployment architecture paradigm (directly feeds Macha architecture decisions).

---

[Category]Investment analysis (VC cost framework)
[Title]Why VCs Should Care About AI in Game Development (per-player cost model)
[Link/FilePath]https://dredyson.com/why-vcs-should-care-about-ai-in-game-development-gamedev-tips-tools-techniques-and-gpt-llm-agent-integration-a-startup-valuation-perspective-the-hidden-truth-about-technical-due-diligence-in-seed-f/
[One-line summary]VC diligence framework: per-player monthly cost $3–$22.5 (10 calls/min×30 min×500 tok×$2–15/M), 100K MAU = $300K–$2.25M/month, can exceed mobile ARPU 10×; hybrid architecture brought a combo from $1.80 to $0.12/player/month. Relevance to Macha: proves in capital language "no cost control = uninvestable," strengthens Macha cost-control narrative.
[Key conclusions]
1. Per session $0.30–$2.25, monthly $3–$22.5/player; 100K MAU = $300K–$2.25M/month.
2. Vs. mobile ARPU $0.5–2/month, AI cost can exceed revenue 10×.
3. Hybrid local/cloud brought a combo from $1.80 → $0.12/player/month, ≈$18M saved over 3 years.
4. AI-native architecture company valuation can be 3–5× higher.
5. Tech-maturity tiers: API glue ↔ infrastructure ↔ data flywheel.
[Reusable]Unit-economics model, valuation-multiple argument (Macha fundraising/whitepaper use).

---

[Category]Engineering test (model price gap)
[Title]Building AI Game NPCs From Scratch: What Nobody Tells You (2026 production test)
[Link/FilePath]https://dev.to/fiercedash/building-ai-game-npcs-from-scratch-what-nobody-tells-you-4k4c
[One-line summary]2026 production test: 184 models on global API, token price $0.01–$3.50/M; GPT-4o output $10.00/M vs GLM-4 Plus $0.80/M = 12.5×, 400M output tokens/month = $3.6M gap. Relevance to Macha: argues "model-workload matching" and domestic-model cost-performance, supports Macha multi-model routing.
[Key conclusions]
1. Huge model price gap: output token $0.80 (GLM-4 Plus) ~ $10.00 (GPT-4o)/M.
2. Domestic/open models (DeepSeek V4, Qwen3-32B, GLM-4) stand out on cost-performance.
3. NPC workload uneven, needs latency-tolerance bucketed routing.
4. Multi-region deployment (us/eu/ap) cuts p99 latency.
5. After cache hit >70%, real cost significantly below theoretical.
[Reusable]Model routing strategy, domestic-model cost-performance evidence (Macha defaults to favoring local/domestic).

---

[Category]Company/Product (Toolchain, NVIDIA ACE 2025–2026)
[Title]NVIDIA RTX Advances with Neural Rendering and Digital Human Technologies at GDC 2025 / 2026
[Link/FilePath]GDC2025 https://developer.nvidia.com/blog/nvidia-rtx-advances-with-neural-rendering-and-digital-human-technologies-at-gdc-2025/ (GDC2026 https://www.linkedin.com/pulse/advancing-state-path-tracing-ai-neural-rendering-gdc-2026-spitzer-3gyzc ; Naraka on-device https://game.xiaomi.com/viewpoint/1098536009_1743083895028_16 )
[One-line summary]NVIDIA ACE landed inZOI "Smart Zoi" (500M-param SLM Mistral-Nemo-Minitron on-device) at GDC2025, Naraka mobile became first domestic ACE on-device AI teammate; GDC2026 expanded to PUBG co-playable ally, Creative Assembly dynamic AI advisor, Nemovision-4B VLM. Relevance to Macha: strongest reference for edge cost-down/latency-down, IGI SDK unified inference API is Macha interoperable-interface prototype.
[Key conclusions]
1. inZOI first ACE autonomous NPC "Smart Zoi", 500M-param SLM on-device RTX-accelerated.
2. Naraka mobile PC version: first domestic game ACE+LLM on-device AI teammate.
3. GDC2026: PUBG co-playable Ally, Creative Assembly dynamic AI advisor, Nemovision-4B VLM.
4. ACE suite includes ASR/Avatar/Animation/VLM, cloud+edge unified.
5. Wemade MIR 5 introduces ACE+NIM for AI Boss "Astrion."
[Reusable]On-device SLM route, unified inference API design (Macha interface reference).

---

[Category]Company/Product (Big-co, Tencent Peacekeeper Elite / Hunyuan)
[Title]Tencent Peacekeeper Elite AI teammate "Xiaotian" and Oasis Genesis (Hunyuan 3 preview driven)
[Link/FilePath]https://cloud.tencent.com/developer/article/2681949 (deep https://t.cj.sina.cn/articles/view/7294209083/1b2c4cc3b00101s4hu )
[One-line summary]Tencent Peacekeeper Elite AI teammate cumulative experience 110M, peak DAU 17.7M; "Xiaotian" industry-first Hunyuan 3 preview emotional-companion AI teammate; Oasis Genesis UGC AI creation DAU broke 58M; GDC 2026 Tencent led with 21 sessions. Relevance to Macha: benchmark of AI NPC commercial loop under large DAU high concurrency, engineering paradigm (knowledge base + strategy model + switch) borrowable.
[Key conclusions]
1. AI teammate cumulative 110M experience, peak weekend DAU 17.7M; mic open rate ≈75%, 70 interactions/match.
2. "Xiaotian" driven by Hunyuan 3 preview + GameMate 1.0, with emotional companionship and long-term memory.
3. Oasis Genesis UGC AI creation: Spring Festival DAU 58M, 200K online maps, 15-minute idea landing.
4. Honor of Kings AI teammate satisfaction +35%; Delta Force AI maps -40% cycle.
5. Over 40 games deployed AI; GDC 2026 led with 21 sessions.
[Reusable]High-concurrency AI NPC engineering paradigm, UGC+AI creation loop (Macha case library).

---

[Category]Company/Product (Big-co, NetEase Fuxi AOP)
[Title]NetEase Fuxi AI Agent Drives Gameplay Innovation (CGDC 2025 / Justice Online review)
[Link/FilePath]CGDC https://www.cnblogs.com/wyfx/p/19021186 (Justice Online review https://blog.51cto.com/u_10819805/14755008 )
[One-line summary]NetEase uses AOP framework to deploy smart NPCs (Justice Online retainers exceed 40M, Naraka voice AI teammate on-device ACE, All-Star Street Ball tactics AI, AI crayfish offline hosting); 2025 R&D ¥17.7B. Relevance to Macha: most mature domestic "brain" proof, but strongly internally bound, not standardized for external use, is what Macha open-sources.
[Key conclusions]
1. AOP loop: perception→cognition→decision→execution; RLHF persona dialogue; pathfinding 77%→99%.
2. Justice Online: smart NPCs, retainer system (whole-server self-built AI retainers exceed 40M), film-crew mode, AI crayfish (2026-07 gold smooth-play server offline hosting).
3. Naraka mobile: industry-first voice AI teammate; PC version first domestic ACE on-device AI teammate.
4. All-Star Street Ball Party: RL basketball AI bots (solo/coop styles).
5. 2025 R&D ¥17.7B, AI gameplay raised users' avg daily interaction +40%.
[Reusable]AOP architecture paradigm, voice AI teammate engineering chain, UGC creation tools (Macha reference).

---

[Category]Company/Product (Big-co, miHoYo/Anuttacon 2026 retraction)
[Title]Cai Haoyu Anuttacon Strategic Retraction: AnuNeko/BSide shut down, Whispers positive fell to 35%
[Link/FilePath]https://www.toutiao.com/article/7671440711262142991 (industry https://www.163.com/dy/article/L455VVSN0519DDQ2.html ; ¥100B investment https://www.toutiao.com/a7669342971933901375 )
[One-line summary]2026 Anuttacon multi-line retraction: AnuNeko shut down within a year, BSide:Olivia Lin within a month, Whispers positive 82%→35%; Cai Haoyu shifted to LLM+Agent; miHoYo simultaneously announced three-year max ¥100B AI investment. Relevance to Macha: hardest negative example of AI-native "lacks game framework / controllability / compliance."
[Key conclusions]
1. AnuNeko (AI companion cat) shut down within a year; BSide:Olivia Lin shut down within <1 month.
2. Whispers from the Star positive fell from 82% to ~35%, development slowed.
3. Cai Haoyu LinkedIn updated to "Independent LLM + Agent Developer," shifting to Agent.
4. miHoYo 2026-05 announced three-year max ¥100B AI investment, full-stack self-developed, paving way for Varsapura.
5. Star Rail "Pam AI assistant", Star Burst Valley second-beta AI NPCs (multi-player concurrency + complete memory) already deployed.
[Reusable]Negative checklist (B3 controllability / B5 compliance / lacks framework), big-co long-term investment contrast (Macha evaluation benchmark).

---

[Category]Company/Product (Big-co, Kaiying Xingyi/Zhimeng/SOON)
[Title]Kaiying Network "Xingyi" large model and SOON AI full-process dev platform (incl. Brilliant investment)
[Link/FilePath]Semi-annual report https://static.cninfo.com.cn/finalpage/2025-08-30/1224623698.PDF (research https://stock.finance.sina.com.cn/stock/view/paper.php?symbol=sh000001&reportid=809963044912 ; concept https://www.toutiao.com/article/7667875040730137122 )
[One-line summary]Kaiying self-built "Xingyi" large model (animation/scene/numerics/code/UI), "Zhimeng" large model filed and connected to DeepSeek R1; Jiyi SOON platform brings game dev from months to hours; 2025-07 introduced Brilliant (Stephen Chow) group investment. Relevance to Macha: represents "AI industrialization efficiency" route, complementary to Macha "Gap Two/Three."
[Key conclusions]
1. Xingyi covers animation/scene/numerics/code/UI/map generation; Zhimeng (Transformer) story-script filed.
2. Deeply connected to DeepSeek R1, capabilities significantly enhanced.
3. SOON (Jiyi) AI full-process dev platform: art→code deployment automation, cycle months→hours.
4. 2025-07 Brilliant (Stephen Chow) subsidiary signed investment MOU.
5. Invested in Natural Selection pushing 3D AI digital companion "EVE", Dapeng VR AI glasses.
[Reusable]AI industrialization pipeline paradigm, vertical-model filing path (Macha domestic-compliance reference).

---

[Category]Industry review (domestic vertical-model breadth)
[Title]A-share Games Industry AI Application Review (Giant GiantGPT / 37 Xiaoqi / Perfect Tiangong)
[Link/FilePath]https://baike.baidu.com/item/A%E8%82%A1%E6%B8%B8%E6%88%8F%E8%A1%8C%E4%B8%9A/68330059
[One-line summary]Domestic games-enterprise AI penetration 86%, top-50 revenue enterprises 80% already laid out; Giant GiantGPT (2025-12 filed, first games vertical), 37 "Xiaoqi" (art AI>80%), Perfect "Tiangong" and other vertical models densely emerging. Relevance to Macha: domestic "vertical-model filing race" already formed momentum, but none open a standard layer, leaving white space for Macha.
[Key conclusions]
1. Games-enterprise AI penetration 86%; top-50 revenue enterprises 80% disclose AI layout.
2. Giant GiantGPT 2025-12 filed, first vertical large model in domestic games industry (long-term memory / scenario reasoning).
3. 37 "Xiaoqi": employee AI coverage 100%, 2D art AI>80%, Mingyue Gongxin 10 days per game.
4. Perfect "Tiangong" self-built games large model, embedded in R&D and experience.
5. Giant "AI dummy" Q1 2026 participation broke 400M matches, generated over 2.9B AI dummies.
[Reusable]Domestic AI-games landscape panorama, vertical-model filing list (competitive-map expansion).

---

> **Deepening note**: §5 is all additive content, no conclusion in §0–§4 changed. New numbers all bring source and caliber; vendor/secondary valuations (Convai $21M, Inworld $125.7M, Volley ARR, etc.) suggest tracing primary before citing. miHoYo Anuttacon 2026 retraction, Whispers positive etc. timeline and values are from Chinese media, need secondary confirmation.
