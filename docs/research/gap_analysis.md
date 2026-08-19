# Preliminary Collection Acceptance and Information Gap Analysis

> Date: 2026-08-16
> Accepted objects: 8 research documents submitted by the team (academic_cognitive_models / engineering_npc_architectures / industry_landscape / design_theory_believability / evaluation_benchmarks / standards_interop / safety_compliance / data_resources)

---

## 1. Acceptance Conclusion: Passed (may proceed to the next phase, but "hard materials" need to be supplemented)

**The 8 categories of information covered**:

| Category | Document | Quality Judgment |
|---|---|---|
| 1 Academic cognitive models | academic_cognitive_models.md | Excellent: has comparison tables, fusion suggestions, and well-formatted sources |
| 2 Existing engineering architectures | engineering_npc_architectures.md | Excellent: FSM/BT/GOAP/HTN/Utility boundaries are clear, Replace/Wrap conclusions are usable |
| 3 Industry status | industry_landscape.md | Good: bottleneck list is excellent; some data comes from secondary citations and needs primary-source tracing |
| 4 Design theory | design_theory_believability.md | Excellent: design language → technical metric translation table is actionable |
| 5 Evaluation benchmarks | evaluation_benchmarks.md | Excellent: L1/L2/L3 layering is reasonable, benchmark list is complete |
| 6 Standards and ecosystem | standards_interop.md | Excellent: MCP/A2A/OpenAI API/ECS interface shapes are clearly organized |
| 7 Safety & compliance | safety_compliance.md | Excellent: China's Anthropomorphic Interaction Measures, AI Act, COPPA, etc. are turned into compliance switches |
| 8 Data resources | data_resources.md | Excellent: license-risk labeling is honest, commercial vs. research use is clearly distinguished |

**Overall assessment**: The team has completed the collection at the "literature and public-information layer," which is sufficient to support Macha entering architecture design. But if the goal is truly a "standard skeleton that disrupts the industry," three types of materials are still missing: **primary industry evidence, code-level interface facts, and requirement validation from real developers.**

---

## 2. Information to Be Supplemented (by priority)

### P0-1 Primary industry data / authorized reports

**Status**: Most of the scale data in industry_landscape.md comes from CSDN reposts and pmarketresearch vendor estimates; the author has honestly noted "primary sources need to be traced."

**To supplement**:

- [ ] Newzoo original report or official press release (global game market, AI game segment).
- [ ] Niko Partners "China Gamer Behaviour and Market Insights 2025" original report or official summary.
- [ ] a16z Games original research (73%/88% adoption rate, OpenRouter traffic study).
- [ ] CNG (Gama Data) "China Game Industry AI Development Report" original report.
- [ ] Any citable GDC 2025/2026 game AI talk (e.g., AI NPC deployment cost, retention data).

**Why**: The basis for initiating the standard skeleton cannot rest on secondary blogs. Otherwise external pitches, paper citations, and open-source community endorsement will all be discounted.

**Delivery format**: report PDF + source page screenshot + key-number summary.

---

### P0-2 Code-level teardown: "interface facts" of existing frameworks

**Status**: The engineering document summarizes well, but not to the granularity of "directly copyable interface signatures."

**To supplement** (goal: one page of interface teardown per repo):

- [ ] `joonspk-research/generative_agents`: actual data structures and function signatures of the memory stream, reflection, and plan tree.
- [ ] `letta-ai/letta` (MemGPT): state machine and API of main context / external storage / autonomous paging.
- [ ] `OpenBMB/Voyager` or similar: skill library schema, environment interface.
- [ ] `SkyrimNet`: Papyrus and MCP tool list, prompt-template hot-reload structure.
- [ ] `RimAI Core`: IOrchestrationService / IPersonaService / IToolRegistryService interfaces.
- [ ] `mineflayer`: plugin interface and event model (as a template for the Perception/Action adaptation layer).
- [ ] NVIDIA ACE NIM / Inworld / Convai **public API documentation fields** (even if some require registration).

**Why**: Macha must define standard interfaces; it cannot rely only on paper abstracts. We need "interface facts": field names, call order, error handling, state lifecycle.

**Delivery format**: one `reference/teardowns/<name>.md` per repo, containing: architecture diagram, key interface signatures, data model, reusable points, non-reusable points.

---

### P0-3 Model capability and inference cost / latency benchmarks

**Status**: Multiple documents mention "local small model + cloud large model" and "1–3 second latency," but lack citable measured data.

**To supplement** (the team can run a small benchmark, or collect trustworthy third-party tests):

- [ ] Candidate small models: Qwen3-8B/14B, Llama 3.1 8B, Gemma 3, DeepSeek-R1-Distill, Mistral-Nemo, etc. Record: context length, Function Calling quality, Chinese capability, license.
- [ ] Local inference measurements: token/s, time-to-first-token, concurrency on 4090/5070/M-series Mac.
- [ ] Cost table: price per million tokens (cloud API vs. local depreciation).
- [ ] Structured output / JSON Schema support comparison (OpenAI, vLLM, llam.cpp, Ollama).
- [ ] A re-runnable latency / cost test script, incorporated into Macha's E9/E10/E11.

**Why**: If Macha treats "cost / latency as first-class citizens" by default, it needs its own engineering benchmarks rather than citing vendor marketing.

**Delivery format**: `docs/research/model_serving_benchmarks.md` + re-runnable script.

---

### P0-4 Real developer interviews / requirement validation

**Status**: The industry document proves "the market is interested," but does not prove "developers are willing to adopt an open-source standard skeleton."

**To supplement**:

- [ ] Interview 8–15 potential users: indie game teams, mod authors, AI programmers at small/medium studios, 3A-engine TAs.
- [ ] Fixed questions:
  1. What do you currently use to implement NPC dialogue / memory?
  2. What was the reason you last gave up on an LLM NPC solution?
  3. If there were an open-source skeleton, what would you least tolerate about it?
  4. How do you want it to cooperate with your existing engine / behavior tree?
- [ ] Summarize into "Jobs To Be Done + list of rejection reasons."

**Why**: Avoid building a standard that is "academically correct but nobody uses." A standard is ultimately about ecosystem adoption rate.

**Delivery format**: anonymous interview notes + JTBD cards + adoption-barrier list.

---

### P1-5 Standards organizations and industry-specification details

**To supplement**:

- [ ] ISO/IEC JTC 1/SC 42 (AI standards), ISO/IEC 23053 (AI framework) related documents.
- [ ] IEEE game-AI related standards / conferences (IEEE CoG papers, IEEE 7000 ethics).
- [ ] Khronos / O3DE / Godot Foundation's existing discussions on "AI game middleware."
- [ ] GDC 2025/2026 standard initiatives or industry consensus on AI NPCs.

**Why**: If Macha is to become a "standard," it cannot only be a de facto standard; it must also know the formal standard paths it may connect to in the future.

---

### P1-6 Semantic adjudication and multi-agent simulation "playable prototype" teardown

**To supplement**:

- [ ] Hidden Door design docs / developer interviews (how world state exists at the engine layer, how player actions are adjudicated).
- [ ] Infinite Craft's synthesis-cache mechanism implementation analysis.
- [ ] Suck Up!'s interaction structure and LLM call boundary.
- [ ] A gameplay teardown of a minimal playable "semantic adjudication" demo (the team can playtest it and write an experience report).

**Why**: Macha's Action layer must have a built-in "adjudicator"; it needs design rules extracted from playable products, not just derived from paper taxonomies.

---

## 3. Issues Found (to be corrected)

1. `data_resources.md` line 133 claimed "evaluation_benchmarks.md line 75 is labeled MIT," but it has actually been corrected to CC BY 4.0 — this erratum entry can be updated or deleted.
2. The "Tencent 18%, NetEase 12%, miHoYo 8% share" figures in `industry_landscape.md` are self-marked "caliber questionable" and must be traced or deleted before entering external materials.
3. The index in `information_needs.md` has not been updated (team members added documents without backfilling the index).

---

## 4. Conclusion

- **Can be accepted**: The literature / public-information layer is already qualified, and some documents (cognitive-model fusion, design-theory translation, standard-interface draft) already directly guide architecture design.
- **Cannot stop yet**: To support the "standard skeleton" positioning, supplement primary industry data, code-level teardown, model benchmarks, and developer interviews per P0-1 → P0-4.
- **Suggestion**: First let the team take P0-2 (code teardown) and P0-3 (model benchmarks) as this week's tasks; P0-1 (primary reports) handled by one person dedicated to procurement / retrieval; P0-4 (interviews) can start in parallel, first interviewing mod authors and indie teams (easiest to schedule).
