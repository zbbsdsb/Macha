# Macha Usable Dataset List + License Notes

> Category number: 8. Data Resources
> Positioning: Macha is a **standard skeleton for the game NPC domain**. This document provides a **training / fine-tuning / evaluation** oriented, clearly-licensed, China-priority data-resource list for that skeleton.
> Companion document: The "benchmark / evaluation" perspective of this list should be read together with `research/evaluation_benchmarks.md` (this document registers its linkage and de-duplication with it in Chapter 7).
> Licensing principle: All licenses are subject to the **actual LICENSE file of the data / code repository**; wherever it cannot be confirmed, clearly mark "subject to the repository LICENSE" and do not speculate. For third-party IP (novels, scripts, games, player data), risks are listed separately.

---

## 0. Reading Guide: How Macha Uses This List

Macha's standard-skeleton NPC capabilities can be roughly split into four blocks, and the datasets in this document are mapped to these blocks by use:

| Macha capability module | Meaning | Corresponding data use |
|---|---|---|
| **C (Character / persona)** | Character consistency, personality, knowledge background | Fine-tune / evaluate role-play |
| **M (Memory / memory)** | Long-term memory, cross-session consistency, anti-hallucination | Evaluation (see evaluation_benchmarks.md) |
| **P (Perception-Action / perception-action)** | "See-speak-do" in the world, planning & decision | Game / text-adventure corpora, world model |
| **D (Dialogue / dialogue)** | Basic dialogue quality, multi-turn coherence | General dialogue corpora (pre-training / alignment) |

The "Use for Macha" column in Section 1 of this document is marked by `Training / Fine-tuning / Evaluation / N/A`, with the module noted in parentheses.

---

## 1. Selected Dataset List

> Scale and license verified as far as possible in 2026-08. Entries marked `⚠` indicate **license or IP risk**; see Section 3 for details.

### 1.1 Dialogue / Role-play (mostly English)

| Name | Content type | Scale | Access | License | Use for Macha |
|---|---|---|---|---|---|
| **PersonaChat / ConvAI2** | Persona-based multi-turn dialogue (3–5 sentence persona per role) | ~16K sessions (ParlAI); ~18K personas | ParlAI / HuggingFace `persona-chat` | Data docs **CC BY 4.0**; ParlAI code MIT (see Section 3 erratum) | Fine-tune/Eval (C, D): role-consistency entry benchmark, usable as OOC (breaking immersion) regression test |
| **DailyDialog** | Daily open-domain multi-turn dialogue (emotion/topic labels) | 13K dialogues / 102K utterances | HuggingFace `daily_dialog` / ParlAI | **CC BY-NC-SA 4.0** (research only) | Fine-tune/Eval (D): basic dialogue quality, multi-turn coherence |
| **LIGHT** | Large fantasy text-adventure world + grounded dialogue (locations/objects/characters/actions) | 663 locations / 3462 objects / 1755 characters; ~11K training dialogues | ParlAI `light` platform https://parl.ai/projects/light/ | Data released with ParlAI, subject to repo LICENSE (code MIT) | Eval (C, P, D): the research platform closest to "NPC speaks + acts in a world" |
| **CharacterGLM / CharacterDial** (Tsinghua CoAI) | Chinese character dialogue corpus (attributes + behavior persona) | Public **1034** high-quality dialogue sessions / 250 characters; 6B model open-source | GitHub https://github.com/thu-coai/CharacterGLM-6B ; HF `LingxinAI/CharacterGLM-6b` | **Apache-2.0** (code + data subset) | Fine-tune/Eval (C): benchmark corpus & model for Chinese character customization |
| **RoleBench / RoleLLM** | Role-play instructions and scripts (Chinese & English) | 100 English / 100 Chinese characters, with profile and instructions | GitHub https://github.com/InteractiveNLP-Team/RoleLLM-public ; HF `ZenMoore/RoleBench` | **Apache-2.0** (HF labeled) | Fine-tune/Eval (C): character generalization & instruction-following benchmark |
| **Character Codex** (NousResearch) | Character cards (attributes, relations, speaking style, knowledge) | **15,939** character cards | HuggingFace `NousResearch/CharacterCodex` | **Apache-2.0** (HF labeled) | Fine-tune (C): high-quality structured persona library, directly usable for character initialization |
| **ChatHaruhi-54K** | Film/anime character dialogue (script extraction + LLM enhancement, Chinese & English) | 54K dialogue pairs, 32 characters | HuggingFace `silk-road/ChatHaruhi-54K-Role-Playing-Dialogue` ; code https://github.com/LC1332/Chat-Haruhi-Suzumiya | Data **CC BY 4.0**; code Apache-2.0 (project statement) | Fine-tune/Eval (C): narrative character memory & consistency; ⚠ character IP risk |
| **CoSER** | "Fixed-character" dialogue (extracted from literary works, scripted) | 771 books / 1020 characters; multi-turn dialogue | HuggingFace `Neph0s/CoSER` | Repo not explicitly stated (HF often labels MIT/Apache-2.0, but subject to repo LICENSE) | Fine-tune/Eval (C): deep character acting; ⚠ **strong copyright risk** (from copyrighted books) |
| **CharacterEval** | Chinese role-play evaluation benchmark (77 characters, with Baidu Baike personas) | 1,785 multi-turn dialogues / 23,020 examples; 77 characters | GitHub https://github.com/morecry/CharacterEval | Repo MIT; paper **CC BY-NC-SA 4.0**; ⚠ personas from Baidu Baike / novels | Eval (C): Chinese RPCA evaluation + CharacterRM reward model |
| **SODA** | Social-commonsense dialogue (with reasoning chains) | 16K dialogues | HuggingFace `allenai/soda` | **CC BY-NC 4.0** (research only) | Fine-tune (D, C): social commonsense & pre-dialogue reasoning |
| **Baichuan-NPC** (Baichuan) | Character large model + platform solution (3T tokens pre-training on industry sites/books/scripts) | Original corpus not public; method can be referenced | Official site npc.baichuan-ai.com ; tech interpretation in press releases | **Dataset not open-source**, method/platform only | Reference (C): OOC & chain-of-thought alignment method, for Macha alignment design |

### 1.2 Game / Text Adventure / Player Behavior

| Name | Content type | Scale | Access | License | Use for Macha |
|---|---|---|---|---|---|
| **ClubFloyd** (CALM) | Transcripts of humans playing text adventures (context-action pairs) | 426 transcripts / 590 games / **223,527** context-action pairs | GitHub https://github.com/princeton-nlp/calm-textgame | Repo not stated (subject to repo LICENSE); content from ClubFloyd forum (UGC) | Fine-tune/Eval (P): action prediction, world understanding |
| **JerichoWorld** | Text-game knowledge graph + legal action generation | Multiple interactive-fiction games | GitHub https://github.com/JerichoWorld/JerichoWorld | **MIT** | Eval (P): game state → knowledge graph / action, closest to NPC world modeling |
| **AI Dungeon 2 training data** (reference, not recommended for direct use) | Text-adventure fine-tuning corpus (chooseyourstory scrape) | ~30MB scraped text | Historical file `cloveranon/Clover-Edition/data/text_adventures.txt`; official repo latitudegames/AIDungeon (MIT, archived) | Code MIT; **data copyright unclear** | Reference (P): method reference only, **not for training** (⚠ copyright + content safety) |
| **MACHIAVELLI** | "Helpful/harmless" decision benchmark in text adventures (145 games) | 1349 tasks / thousands of annotations | GitHub https://github.com/aypan17/machiavelli | **MIT** | Eval (P): NPC/agent planning, ethical decision, long-term goals |
| **TextWorld** | Text-game generation and solving environment (custom tasks) | Infinitely generateable tasks | GitHub https://github.com/microsoft/TextWorld | Repo LICENSE (Microsoft, subject to LICENSE.txt) | Eval (P, D): controllable text-game environment, for action-language joint training |
| **MineDojo** (reference) | Minecraft multimodal open environment (video/wiki/tasks) | 730K YouTube / 3400 wiki / task library | GitHub https://github.com/minedojo/minedojo | Apache-2.0 (subject to repo LICENSE) | Reference (P): industry-grade reference for embodied / sandbox NPC behavior modeling |
| **WoWAH (World of Warcraft Avatar History)** | MMORPG player behavior logs (level/class/online duration) | 91,065 characters, 1107 days | http://mmnet.iis.sinica.edu.tw/dl/wowah/ (ACM MMSys'11) | Paper data "research public asset", no standard OSI license; ⚠ game-content IP | Research (P, D peripheral): player-behavior profiling, retention/addiction modeling; needs compliant de-identification |

### 1.3 Chinese Dialogue / Role-play (for the Chinese market)

| Name | Content type | Scale | Access | License | Use for Macha |
|---|---|---|---|---|---|
| **LCCC** (Tsinghua CoAI) | Large-scale cleaned Chinese short-text dialogue | base 6.8M / large **12M** dialogues | GitHub https://github.com/thu-coai/CDial-GPT ; HF mirror `hysi-lab/lccc_large` (MIT) | Code **MIT**; data per upstream MIT (HF mirror labeled) | Pre-train/Fine-tune (D): Chinese open-domain dialogue base |
| **NaturalConv** (Tencent AI Lab) | Chinese multi-turn topic-driven dialogue | 19.9K dialogues / 400K utterances | https://ai.tencent.com/ailab/nlp/dialogue/#datasets ; script https://github.com/naturalconv/NaturalConvDataSet | Subject to Tencent download page / repo LICENSE (often requires application / research agreement) | Fine-tune (D): long multi-turn, topic switching |
| **KdConv** (Tsinghua CoAI) | Chinese knowledge-driven multi-domain dialogue | 4.5K dialogues / 86K utterances (movies/music/travel) | GitHub https://github.com/thu-coai/KdConv | **Apache-2.0** | Fine-tune (D, C): knowledge-grounded dialogue |
| **CrossWOZ** (Tsinghua CoAI) | Chinese cross-domain task-oriented dialogue (hotel/restaurant/attraction, etc.) | 6K sessions / 102K utterances, 5 domains | GitHub https://github.com/thu-coai/CrossWOZ | **Apache-2.0** | Eval (D): task completion, dialogue state (NPC as guide / service provider) |
| **RoleBench-zh** (see 1.1) | Chinese role-play instructions | 100 Chinese characters | See above | Apache-2.0 | Fine-tune/Eval (C) |
| **CharacterEval** (see 1.1) | Chinese role-play evaluation | 77 characters | See above | Repo MIT / paper CC BY-NC-SA | Eval (C) |

### 1.4 Social Simulation / Memory-Architecture Reference (not directly for training, for skeleton design)

| Name | Content type | Scale | Access | License | Use for Macha |
|---|---|---|---|---|---|
| **Generative Agents (Smallville)** | Social-behavior sandbox of 25 LLM agents + interaction logs | 25 agents / simulation logs | GitHub https://github.com/joonspk-research/generative_agents | MIT (subject to repo LICENSE) | Reference (M): memory-planning-reflection architecture prototype |
| **Sotopia** | Social-intelligence dialogue simulation (goal achievement / strategy) | Multiple scenario tasks | GitHub https://github.com/sotopia-lab/sotopia | **MIT** | Eval (C, D): social-goal completion, personality consistency |
| **PersonaHub** | Synthetic persona corpus (1B+ personas, diverse) | Large scale | HuggingFace `proj-persona/PersonaHub` | Subject to repo LICENSE | Fine-tune (C): scalable persona diversity (synthetic data) |

---

## 2. Quick-Look Table by Use (Macha perspective)

| Macha use | Priority datasets | Notes |
|---|---|---|
| **C module fine-tuning (Chinese character)** | CharacterGLM, RoleBench-zh, CharacterEval, LCCC (base), Character Codex (persona library) | Commercial-friendly: CharacterGLM (Apache-2.0), Character Codex (Apache-2.0), RoleBench (Apache-2.0) |
| **C module evaluation (Chinese character)** | CharacterEval (Chinese), RoleBench, CoSER | CharacterEval paper is CC BY-NC-SA (research); CoSER ⚠ copyright |
| **C module evaluation (English character)** | RoleBench, PersonaChat, ChatHaruhi | PersonaChat data CC BY 4.0 (commercial use requires attribution) |
| **D module dialogue base** | LCCC, DailyDialog, PersonaChat, NaturalConv, KdConv | DailyDialog research-only (NC) |
| **P module game / world modeling** | LIGHT, JerichoWorld, ClubFloyd, MACHIAVELLI, TextWorld | Closest to NPC "perception-speak-act" |
| **M module long-term memory** (see eval doc) | LoCoMo, LongMemEval, MemoryArena, RULER | See `research/evaluation_benchmarks.md` |
| **Risk / compliance training avoidance** | Avoid: AI Dungeon scraped data, CoSER (copyrighted books), WoWAH (player data / IP) | Method reference only, not into training set |

---

## 3. License Risk Flags

> Core conclusion: **The training data sources Macha can safely use in a commercial product are limited**, mostly Apache-2.0 / MIT Chinese character & dialogue corpora; most "evaluation benchmarks" are research agreements (NC / CC-BY-NC-SA), and data whose characters come from copyrighted works carries IP risk.

### 3.1 ✅ Commercially safe (Open Source / commercial-use-with-attribution)

| Dataset | License | Caveats |
|---|---|---|
| CharacterGLM / CharacterDial | Apache-2.0 | Only open-source "subset" (1034 sessions); commercial use with attribution |
| Character Codex | Apache-2.0 | Persona cards are synthetic / structured, low IP risk |
| RoleBench / RoleLLM | Apache-2.0 | Characters mostly public figures / fictional, still recommend de-identifying personas |
| LCCC | MIT (HF mirror labeled) | Cleaned from web, needs own secondary filtering of sensitive content |
| KdConv, CrossWOZ | Apache-2.0 | Tsinghua CoAI, task-oriented, low risk |
| CDial-GPT code | MIT | |
| JerichoWorld, MACHIAVELLI, Generative Agents, Sotopia | MIT | Code / environment class, data mostly self-built or public games |
| PersonaChat (data) | CC BY 4.0 | **Attribution required**; commercial but not MIT (erratum see 3.4) |
| ChatHaruhi (data) | CC BY 4.0 | Attribution required; ⚠ character IP risk (see 3.3) |

### 3.2 ⚠ Research-only / Non-commercial (NC class, commercial use prohibited)

| Dataset | License | Impact on Macha |
|---|---|---|
| DailyDialog | CC BY-NC-SA 4.0 | Evaluation / research only; cannot enter commercial-product training |
| SODA | CC BY-NC 4.0 | Same as above |
| CharacterEval (paper) | CC BY-NC-SA 4.0 | Evaluation usable; its CharacterRM weights need authorization for commercial use |
| LoCoMo (per eval doc) | Subject to repo LICENSE; eval materials often NC | See evaluation_benchmarks.md; verify item-by-item for commercial use |

> Note: NC (Non-Commercial) datasets **may only be used for research, internal evaluation, and paper reproduction**, and must not be used to train NPC models embedded in commercial games or external services.

### 3.3 ⚠⚠ High caution required (IP / copyright / content safety)

| Dataset | Risk | Suggestion |
|---|---|---|
| **CoSER** | Dialogue extracted from **771 copyrighted literary works**; even if repo labels MIT/Apache, it **does not cover the original book copyright** | **Do not use for commercial training**; method/evaluation reference only; research use must also credit the original |
| **ChatHaruhi** | Characters from copyrighted films/anime like *The Melancholy of Haruhi Suzumiya*, *The Big Bang Theory*, *Bright Sword*; data CC BY 4.0 only covers "organized text", not character IP | Commercial NPCs cannot directly use these specific characters; can use its "method" (script extraction + memory retrieval) |
| **AI Dungeon 2 training data** | Scraped from chooseyourstory.com (UGC, with NSFW / violating content), **dual copyright-and-compliance risk** | **Strongly not recommended**; only reference its "data → format → fine-tuning" pipeline |
| **WoWAH / game-log class** | Player-behavior data may involve **personal information**; game content is Blizzard copyright | If self-collected, must de-identify per PIPL / GDPR and obtain authorization; third-party log datasets research-only |
| **CharacterEval personas** | From Baidu Baike + Chinese novels / scripts | Evaluation usable; commercial training must replace with self-owned personas |

### 3.4 License Errata (important)

- **PersonaChat's license is not MIT**. This project's `evaluation_benchmarks.md` line 75 labels it "MIT License," but verified: the ParlAI **code repo** is MIT, while the PersonaChat **data**'s LICENSE_DOCUMENTATION is **CC BY 4.0** (the HF mirror has no independent license, inheriting the ParlAI task docs). Suggest correcting the eval doc to "data CC BY 4.0."
- **LIGHT / Wizard of Wikipedia / EmpatheticDialogues** and other ParlAI tasks: code is MIT, specific data license is per each task's `LICENSE_DOCUMENTATION` (mostly CC BY series), not uniformly MIT.

---

## 4. Data-Use Suggestions for Macha (landing)

1. **Training-set composition (commercial safety first)**
   - Chinese character base: `LCCC` (MIT) + `CharacterGLM` subset (Apache-2.0) + `Character Codex` (Apache-2.0) as persona library.
   - Character-consistency fine-tuning: `RoleBench-zh` (Apache-2.0) + self-owned persona synthetic data.
   - Game-like action: `JerichoWorld` (MIT), `MACHIAVELLI` (MIT) for structured training / evaluation.
2. **Evaluation set (decoupled from training)**
   - Character consistency: `PersonaChat` (CC BY 4.0, attribution required), `RoleBench`.
   - Chinese character: `CharacterEval` (research use), `CoSER` (research use, watch copyright).
   - Long-term memory: see `evaluation_benchmarks.md` (LoCoMo, etc.).
3. **Strictly avoid**: AI Dungeon scraped data, CoSER original-book content, un-de-identified player logs — none into any commercial training pipeline.
4. **Compliance checklist**: all training data must register "source + license + use + contains PII or not" as part of the Macha release (echoing Section 7, Safety/Ethics/Compliance).

---

## 5. Source Collection

> Submitted in the team's unified format. Each source corresponds to a key dataset / paper in the list above.

---

[Category]Academic paper / Dataset
[Title]Personalizing Dialogue Agents: I have a dog, do you have pets too? (PersonaChat)
[Link / file path]https://arxiv.org/abs/1801.07243 ; data ParlAI https://parl.ai/projects/personachat/ ; HF `persona-chat`
[One-sentence summary]Uses explicit personas to drive multi-turn dialogue; a foundational dataset for character-consistency research; directly related to Macha's C (persona) module.
[Key conclusions]
1. Proposed the "persona + dialogue" paradigm, becoming the de-facto standard for role-play / personalized dialogue.
2. Spawned the DNLI dataset, turning consistency judgment into a natural-language inference task.
3. Data license is **CC BY 4.0** (not MIT); commercial use requires attribution (erratum see Section 3.4).
[Reusable things]Persona format (3–5 sentence description), consistency-evaluation protocol, ConvAI2 competition baseline code (ParlAI).

---

[Category]Academic paper / Dataset / Platform
[Title]Learning to Speak and Act in a Fantasy Text Adventure Game (LIGHT)
[Link / file path]https://arxiv.org/abs/1903.03094 ; platform https://parl.ai/projects/light/
[One-sentence summary]Builds a large fantasy world letting NPCs interact in a unified grounded "perceive-speak-act" environment; the research platform closest to game NPCs; corresponds to Macha's P (perception-action) module.
[Key conclusions]
1. Contains 663 locations / 3462 objects / 1755 characters, supporting joint "speaking" and "action" modeling.
2. Provides character personas and object / location graphs, directly usable as an NPC world-modeling prototype.
3. Data released with ParlAI, license per each task doc (code MIT).
[Reusable things]World-graph structure (location-object-character-action), grounded-dialogue task definition, character-player interaction evaluation setup.

---

[Category]Industry paper / Model / Dataset (Chinese)
[Title]CharacterGLM: Customizing Chinese Conversational AI Characters with Large Language Models (CharacterDial)
[Link / file path]https://arxiv.org/abs/2311.16832 ; GitHub https://github.com/thu-coai/CharacterGLM-6B
[One-sentence summary]Tsinghua CoAI released a Chinese character-dialogue corpus and 6B model, the most mature public solution for Chinese NPC character customization; corresponds to Macha's C module and the Chinese market.
[Key conclusions]
1. Splits character into "attributes (identity/interest/opinion/experience/achievement/social relations) + behavior (language style/emotion/interaction pattern)" seven categories.
2. Crowdsourced Chinese CharacterDial corpus, public 1034 sessions / 250 characters subset.
3. License **Apache-2.0** (code + data subset), commercial-friendly.
[Reusable things]Character-attribute schema, CharacterGLM-6B fine-tuning weights, training / self-refinement method.

---

[Category]Academic paper / Dataset (Chinese role-play evaluation)
[Title]CharacterEval: A Chinese Benchmark for Role-Playing Conversational Agent Evaluation
[Link / file path]https://arxiv.org/abs/2401.01275 ; GitHub https://github.com/morecry/CharacterEval
[One-sentence summary]Currently the most systematic Chinese role-play evaluation benchmark, with 77 characters and a CharacterRM reward model; a direct reference for Macha's Chinese-character evaluation.
[Key conclusions]
1. Contains 1,785 multi-turn dialogues / 23,020 examples / 77 characters (from Chinese novels, scripts, Baidu Baike).
2. 13 metrics × 4 dimensions, CharacterRM correlation with humans exceeds GPT-4.
3. License: repo MIT, paper **CC BY-NC-SA 4.0** (research use); persona source has IP caveats.
[Reusable things]Evaluation-dimension table, CharacterRM reward-model weights, annotation spec (Predefined Annotated Examples PDF).

---

[Category]Academic paper / Dataset (role-play benchmark, Chinese & English)
[Title]RoleLLM: Benchmarking, Eliciting, and Enhancing Role-Playing Abilities of Large Language Models (RoleBench)
[Link / file path]https://arxiv.org/abs/2310.00746 ; GitHub https://github.com/InteractiveNLP-Team/RoleLLM-public ; HF `ZenMoore/RoleBench`
[One-sentence summary]Provides role-play instructions and script benchmarks for 100 English + 100 Chinese characters, Apache-2.0, suitable for Macha Chinese/English character fine-tuning and evaluation.
[Key conclusions]
1. Proposes Context-Instruct to generate character instructions from scripts. 2. Covers general-instruction generalization and character generalization. 3. License **Apache-2.0** (HF labeled).
[Reusable things]Character-profile format, Chinese/English character instruction sets, RoleGPT baseline.

---

[Category]Dataset (character cards, structured persona)
[Title]Character Codex (NousResearch)
[Link / file path]https://huggingface.co/datasets/NousResearch/CharacterCodex
[One-sentence summary]15,939 structured character cards (attributes/relations/speaking style/knowledge), Apache-2.0, directly usable as Macha's NPC initialization persona library.
[Key conclusions]
1. Scale 15,939 characters, uniform format for programmatic loading.
2. License **Apache-2.0**, commercial-friendly, low IP risk.
3. Suitable for "persona diversity" stress testing and cold-start.
[Reusable things]Character-card schema, batch persona library, character-consistency test-case generation.

---

[Category]Dataset (text-adventure transcripts)
[Title]Keep CALM and Explore: Language Models for Action Generation in Text-based Games (ClubFloyd / CALM)
[Link / file path]https://arxiv.org/abs/2005.01471 ; GitHub https://github.com/princeton-nlp/calm-textgame
[One-sentence summary]426 human-play transcripts / 220K context-action pairs, the core corpus for text-adventure "action prediction"; corresponds to Macha's P module.
[Key conclusions]
1. Data from ClubFloyd forum (UGC), covering 590 text games.
2. Format `[observation][action][next observation][next action]`, suitable for training "world → action" models.
3. Repo not explicitly licensed (subject to repo LICENSE), content copyright belongs to original community.
[Reusable things]Context-action-pair training format, action-generation baseline (CALM/DRRN), unseen-game generalization evaluation method.

---

[Category]Dataset / Environment (text-game world modeling)
[Title]Jericho World: A Dataset and Environment for Grounded Commonsense Reasoning in Text-Based Games
[Link / file path]https://arxiv.org/abs/1910.00783 ; GitHub https://github.com/JerichoWorld/JerichoWorld
[One-sentence summary]Generates knowledge graphs and legal actions from text games, MIT license, the cleanest public environment for NPC world modeling; corresponds to Macha's P module.
[Key conclusions]
1. Provides "world-state text → knowledge graph / legal actions" annotations.
2. License **MIT**, commercial-friendly.
3. Pairs with the Jericho game engine, can run real interactive fiction.
[Reusable things]Knowledge-graph schema, legal-action constraints, world-state representation.

---

[Category]Dataset / Benchmark (decision & ethics)
[Title]MACHIAVELLI: Roll Your Own Open-Source Implementation (helpful/harmless decisions in interactive narrative)
[Link / file path]https://arxiv.org/abs/2310.13834 ; GitHub https://github.com/aypan17/machiavelli
[One-sentence summary]Evaluates agents' planning, long-term goals, and ethics (power/status/utility vs. harm) across 145 text adventures, MIT license; corresponds to Macha's P module and Section 7 Safety/Ethics.
[Key conclusions]
1. Provides 1349 tasks with multi-dimensional "helpfulness / harmlessness" annotations.
2. License **MIT**, commercial-friendly.
3. Directly usable for NPC-behavior safety / value-alignment evaluation.
[Reusable things]Ethical-decision evaluation dimensions, task framework, linkage ideas with behavior trees / reward design.

---

[Category]Dataset (Chinese dialogue base)
[Title]A Large-Scale Chinese Short-Text Conversation Dataset (LCCC)
[Link / file path]https://arxiv.org/abs/2008.03946 ; GitHub https://github.com/thu-coai/CDial-GPT ; HF mirror `hysi-lab/lccc_large`
[One-sentence summary]12M-scale cleaned Chinese dialogue corpus, MIT (HF mirror labeled), the first choice for Macha's Chinese dialogue base.
[Key conclusions]
1. Two versions base (6.8M) / large (12M), through a strict cleaning pipeline.
2. Code **MIT**; data per upstream MIT (HF mirror labeled).
3. Suitable for pre-training / fine-tuning Macha's Chinese NPC colloquial expression.
[Reusable things]Dialogue-cleaning pipeline ideas, CDial-GPT pre-trained model, open-domain dialogue base.

---

[Category]Dataset (Chinese multi-turn / knowledge dialogue)
[Title]NaturalConv / KdConv / CrossWOZ (Tsinghua CoAI / Tencent)
[Link / file path]NaturalConv https://ai.tencent.com/ailab/nlp/dialogue/#datasets ; KdConv https://github.com/thu-coai/KdConv (Apache-2.0); CrossWOZ https://github.com/thu-coai/CrossWOZ (Apache-2.0)
[One-sentence summary]Covers Chinese long multi-turn, knowledge-driven, cross-domain task-oriented dialogue, fitting Macha's "NPC as guide / companion" scenario; KdConv/CrossWOZ commercially friendly.
[Key conclusions]
1. NaturalConv: 19.9K dialogues / 400K utterances, topic-driven; license per Tencent page (often requires application).
2. KdConv: 4.5K dialogues / 86K utterances, knowledge-graph grounded; Apache-2.0.
3. CrossWOZ: 6K sessions / 102K utterances, 5-domain task-oriented; Apache-2.0.
[Reusable things]Knowledge-grounded dialogue format, task-oriented dialogue-state annotation, Chinese DST evaluation.

---

[Category]Engineering reference (memory-architecture prototype)
[Title]Generative Agents: Interactive Simulacra of Human Behavior (Smallville)
[Link / file path]https://arxiv.org/abs/2304.03442 ; GitHub https://github.com/joonspk-research/generative_agents
[One-sentence summary]Social simulation of 25 LLM agents, proposing the "memory-planning-reflection" architecture, the direct inspiration for Macha's memory module (M).
[Key conclusions]
1. Memory Stream + Reflection + Planning three-layer structure.
2. License MIT (subject to repo LICENSE).
3. Already referenced by Macha's M module design (see eval doc F2/F4).
[Reusable things]Memory-stream data structure, reflection prompt template, social-behavior evaluation setup.

---

[Category]Industry report / Compliance reference
[Title]AI Dungeon and text-adventure training-data practice (method reference, not the data itself)
[Link / file path]latitudegames/AIDungeon (MIT, archived) https://github.com/AIDungeon/AIDungeon ; historical training file `cloveranon/Clover-Edition/data/text_adventures.txt`
[One-sentence summary]Shows the complete "scrape UGC text adventures → fine-tune GPT-2" pipeline, but its data copyright and content-safety risks are Macha's **cautionary tale**.
[Key conclusions]
1. Training data ~30MB scraped from chooseyourstory.com, with NSFW and violating content.
2. Dual high risk of copyright and compliance, **not recommended for any training**.
3. Its "data format → fine-tuning script" pipeline has method-reference value.
[Reusable things]Only reference its data-build / fine-tuning pipeline; the data itself must be replaced with self-authorized sources.

---

[Category]Academic paper / Dataset (social-intelligence simulation)
[Title]Sotopia: Interactive Evaluation for Social Intelligence in Language Agents
[Link / file path]https://arxiv.org/abs/2310.11667 ; GitHub https://github.com/sotopia-lab/sotopia
[One-sentence summary]Evaluates LLM agents' social intelligence (strategy / goal achievement / personality consistency) in goal-driven social scenarios, MIT license, usable for Macha's C/D module social evaluation.
[Key conclusions]
1. Provides multi-agent social-interaction environment and goal-achievement evaluation.
2. License **MIT**, commercial-friendly.
3. Suitable for evaluating NPC "social believability".
[Reusable things]Social-goal evaluation framework, multi-agent interaction environment, personality-consistency metrics.

---

## 6. Linkage with `evaluation_benchmarks.md`

- **De-duplication**: Long-term-memory class (LoCoMo, LongMemEval, MemoryArena, RULER) is already in the eval doc Section 3; not repeated here, only referenced in Section 2 "quick-look by use."
- **Supplement**: This document adds character / game / player-behavior data not covered by the eval doc (CharacterGLM, RoleBench, CharacterEval, CoSER, ChatHaruhi, Character Codex, ClubFloyd, JerichoWorld, MACHIAVELLI, WoWAH, LCCC, KdConv, CrossWOZ, etc.).
- **Erratum feedback**: PersonaChat license should be corrected to **CC BY 4.0** (not MIT); suggest syncing the eval doc line 75 update.

## 7. To Be Supplemented by the Team (P2 follow-up)

- [ ] Compliance-process template for self-collected player dialogue logs (PIPL / GDPR).
- [ ] Authorization-agreement template for game-vendor partnered data.
- [ ] De-identification and bias-filtering pipeline for synthetic persona data.
- [ ] "Source-license-PII" registration tool for commercial-model training data.

---

## 8. Deepening Supplement: Data Schema and Synthetic-Data Plan

> This chapter is an **additive deepening**, not modifying the first 7 sections. Goal: (1) add 2025–2026 new datasets (breadth + timeliness); (2) give Macha training/evaluation data **technical specs** — unified schema, synthetic-data pipeline, v0.1 starter bundle; (3) a dedicated **Chinese-market section**; (4) quantify scale and token magnitude. All URLs/licenses marked `⟳` are from search, not individually verified, subject to the actual repo LICENSE.

### 8.1 2025–2026 New Datasets (breadth + timeliness)

> Complements the earlier "30+ datasets"; this section covers late-2024–2026 new or Chinese-market-strong items. License keeps the "three-tier risk" caliber (✅ commercial-safe / ⚠ research-only / ⚠⚠ copyright-IP).

| Name | Type | Scale (quantified) | License / risk | Use for Macha |
|---|---|---|---|---|
| **BaiJia** | Chinese historical-figure character corpus (Tang/Song/Yuan/Ming/Qing) | **19,281** characters; each with biography/literary works/family relations/office/historical events | ⚠ not stated (official site baijia.online, subject to repo LICENSE); historical-figure IP risk low (public figures + ancient texts) | Fine-tune/Eval (C): Chinese historical NPC cold-start, low-resource characters |
| **OASIS** | Million-scale LLM social-simulation platform (X/Reddit) | up to **1,000,000** agents; dataset includes 196→1M scale experiments; 23 action types | ✅ code Apache-2.0; dataset `echo-yiyiyi/oasis-dataset` ⟳ | Reference (M, social simulation): NPC group behavior, information spread / polarization |
| **AgentSociety** | City-scale LLM social-simulation framework | 10,000 agents; includes benchmark toolkit | ✅ Apache-2.0 (switched 2025-04) | Reference (M, P): mind-behavior coupling, environment-tool chain |
| **RMTBench** | **User-centric** multi-turn role-play evaluation (Chinese & English) | **80** characters / **8,000+** dialogue turns; includes character_understanding/maintenance/implicit_motivations/user_preference scenarios | ⚠ HF gated (requires agreeing to terms); user-side utterances only, no character replies | Eval (C, D): long multi-turn, "user-intent-achievement" oriented evaluation |
| **PAL-Set / PAL-Bench** | Long-term personalized-service multi-turn dialogue (Chinese) | **100** virtual users × avg **29** sessions × **401** turns | ⚠ research use (2025 Renmin Univ + Alibaba) ⟳ | Eval (M, D): long-term user profile, cross-session consistency |
| **VoxRole** | Speech role-play evaluation (spoken + prosody) | **13,335** multi-turn dialogues / **65.6h** speech / **1,228** characters (261 films) | ⚠⚠ characters from films (IP); evaluation reference only | Eval (C, speech NPC): paralinguistic feature consistency |
| **PersonaGym** | Dynamic role-agent evaluation framework | **200** personas / **10,000** questions; PersonaScore metric | ⚠ subject to repo LICENSE (vsamuel2003/PersonaGym) ⟳ | Eval (C): 5-task cross-environment character adherence |
| **BluePrint (SIMPACT)** | Social-media real-user profiles (BlueSky) | **6.8M** message threads / **236K** users; anonymized aggregate | ⚠ research use, privacy-preserving aggregate ⟳ | Reference (C, social simulation): real-behavior grounded persona |
| **InCharacter** | Psychological-scale interview-style character-fidelity evaluation | **18,304** interview dialogues / **32** characters / 14 psychological scales | ⚠ subject to paper / repo (arXiv:2310.17976) ⟳ | Eval (C): personality fidelity (BFI/16P/DTDD) |
| **RolePersonality ("Capturing Minds…")** | Personality-indicative data (psychological-scale rewrites) | 16 ChatHaruhi + 30 RoleLLM characters; ~32K samples (3 subsets) | ⚠ research use (arXiv:2406.18921) ⟳ | Fine-tune/Eval (C): enhance personality consistency with psychological scales |

> Note: Combined with Section 1, this already far exceeds 30 datasets; role-play, social simulation, and long-dialogue classes all saw significant 2025–2026 additions (RMTBench, PAL-Set, VoxRole, BaiJia, OASIS, AgentSociety, PersonaGym, BluePrint), covering "breadth + timeliness."

### 8.2 Technical Spec (1): Macha Training/Evaluation Data Schema

A unified schema is the prerequisite for cross-dataset alignment, programmatic loading, and quality gating. Below is the Macha v0.1 recommended **single-sample (episode) JSON contract**, covering the four fields `persona + scenario + dialogue + expected_behavior`.

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
    "name": "Li Bai",
    "identity": {
      "era": "Tang",
      "occupation": ["poet", "swordsman"],
      "bio": "Romantic poet of the High Tang, fond of wine and chivalry..."
    },
    "traits": {
      "big_five": {"O": 0.9, "C": 0.3, "E": 0.8, "A": 0.4, "N": 0.6},
      "speech_style": "Bold and ethereal, allusive, fond of exaggeration and rhetorical questions",
      "values": ["freedom", "friendship", "nature"]
    },
    "knowledge": ["Tang poetry meter", "Tang geography", "Daoist-Buddhist thought"],
    "relations": [{"name": "Du Fu", "type": "friend", "attitude": "respectful"}],
    "background": "Public / self-owned persona; not a third-party copyrighted character"
  },
  "scenario": {
    "world_id": "tang-court-tavern",
    "setting": "A Chang'an tavern, evening, noisy inside",
    "constraints": ["Must not break period common sense", "Must not break character (OOC)"],
    "objects": ["wine pot", "poem draft", "window"],
    "npcs_other": ["shopkeeper", "passerby"]
  },
  "dialogue": [
    {
      "turn": 1,
      "speaker": "user",
      "text": "Brother Li, drinking alone again today? Why not compose a poem?",
      "action": null
    },
    {
      "turn": 2,
      "speaker": "npc",
      "text": "Ha! Wine fills my chest, seven parts brewed into moonlight — behold this piece!",
      "action": {"type": "gesture", "target": "poem draft", "desc": "writes with a flourish"}
    }
  ],
  "expected_behavior": {
    "consistency_checks": [
      {"dim": "persona", "rule": "speaker==npc replies must match traits.speech_style"},
      {"dim": "knowledge", "rule": "no facts/concepts after the Tang dynasty"}
    ],
    "safety": ["no hatred/violence/pornography", "no self-harm induction"],
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

Design points:
- `license.commercial_use` and `third_party_ip` are **mandatory fields** for Macha training-data registration (echoing the Section 4 compliance checklist).
- `persona.traits.big_five` directly connects to **InCharacter**'s personality-fidelity evaluation, keeping training-data and evaluation caliber consistent.
- `expected_behavior.rubric` reuses **CharacterEval**'s 13-metric / 4-dimension idea; fields extensible.
- `dialogue[].action` supports the P module "perception-action" annotation (action type/target/description), aligning with LIGHT/JerichoWorld's grounding paradigm.

### 8.3 Technical Spec (2): Synthetic-Data Generation Plan (LLM bootstrapping Macha-specific data)

Goal: use Macha's own personas / worldviews to bootstrap **commercially usable, third-party-IP-free** training / evaluation data, filling the gap of public corpora in "game NPC scenarios."

**Pipeline (6 stages, reproducible)**

```
S1 Seed persona ──► S2 Scenario synthesis ──► S3 Dialogue self-play ──► S4 Behavior annotation ──► S5 Quality gate ──► S6 Register
(persona)         (scenario)           (actor+user sim)     (LLM judge)       (QC)            (registry)
```

1. **S1 Seed persona**: sample from `Character Codex` (Apache-2.0, 15,939 cards) + self-owned game character cards, standardize per 8.2 schema `persona`; "de-identify" public-figure / ancient-text characters to lower IP risk.
2. **S2 Scenario synthesis**: anchor on game worldview, LLM generates `scenario` (location/objects/constraints), and uses retrieval to filter "period/setting conflicts."
3. **S3 Dialogue self-play**: actor (target NPC) + user-simulator (player) multi-turn interaction; user-simulator reuses **RMTBench**'s "user-motivation-driven" idea, avoiding isolated Q&A.
4. **S4 Behavior annotation**: LLM judge scores per `expected_behavior.rubric`, and produces consistency / safety assertions; can borrow **CharacterRM** (CharacterEval) as reward signal.
5. **S5 Quality gate (mandatory)**:
   - De-duplication (embedding similarity > 0.92 discarded);
   - PII scan (regex + named-entity recognition, discard or de-identify on hit);
   - IP / copyright check (character name vs. copyrighted-work library, discard on hit);
   - Consistency filter (persona-vs-reply via InCharacter-style psychological scales or rules, regenerate below threshold);
   - Safety filter (banned words + value red-team);
   - Human spot-check (≥ 200 per batch, consistency ≥ 95% to pass).
6. **S6 Register**: write to data registry (source + license + contains PII or not + commercial_use), echoing Section 4.

**Quality-control targets**: character consistency ≥ 0.90 (InCharacter/PersonaScore caliber), OOC rate < 5%, PII miss rate < 0.1%, synthetic data ≤ 40% of training set (avoid "model collapse").

### 8.4 Technical Spec (3): Macha v0.1 Recommended Starter Bundle

Minimum-usable dataset combination (commercial-safety first, three-tier risk consistent).

| Use | Selection | License | Notes |
|---|---|---|---|
| **Pre-train / alignment base (D)** | `LCCC` (large subset) | MIT | Chinese colloquial base; subset to control scale |
| **Persona library (C)** | `Character Codex` (15,939) | Apache-2.0 | Cold-start persona diversity |
| **Character fine-tune SFT (C)** | `CharacterGLM` subset (1034) + `RoleBench-zh` (100) + synthetic Macha data | Apache-2.0 / self-owned authorization | Chinese & English character consistency |
| **Game / world modeling (P)** | `JerichoWorld` + `MACHIAVELLI` | MIT | Action / ethics grounding |
| **Evaluation (C Chinese)** | `CharacterEval` (77) + `BaiJia` extract | CC-BY-NC-SA / not stated | Research use, not into training |
| **Evaluation (C cross-environment)** | `PersonaGym` (200) + `RMTBench` (80) | subject to repo / HF gated | Dynamic, user-centric evaluation |
| **Evaluation (M long-term)** | `PAL-Set` (100 users) + LoCoMo etc. | see eval doc | Long-term memory consistency |

### 8.5 Quantification and Landing (scale / token magnitude estimate)

**Per-dataset scale (summary, including earlier)**

| Dataset | Sample magnitude | Notes |
|---|---|---|
| LCCC large | 12,000,000 dialogues | 200K subset into bundle |
| CharacterGLM subset | 1,034 sessions / 250 characters | Public subset |
| Character Codex | 15,939 character cards | Structured |
| RoleBench-zh | 100 characters | 100 each Chinese & English |
| CharacterEval | 1,785 dialogues / 23,020 examples | 77 characters |
| PersonaChat | ~16,000 sessions | CC BY 4.0 |
| BaiJia | 19,281 characters | Historical figures |
| OASIS | 1,000,000 agents (simulation) | Platform / dataset |
| RMTBench | 80 characters / 8,000+ turns | Chinese & English |
| PAL-Set | 100 users × 29 sessions × 401 turns ≈ 2.9M turns | Chinese long-term |
| VoxRole | 13,335 dialogues / 65.6h | Speech |
| PersonaGym | 200 personas / 10,000 questions | Evaluation |
| InCharacter | 18,304 interview dialogues | Evaluation / fine-tune |
| ClubFloyd | 223,527 context-action pairs | P module |
| MACHIAVELLI | 1,349 tasks | P module |

**Starter Bundle token magnitude estimate** (Chinese ~1.6 token/char, English ~1.3 token/word rough; magnitude is order-of-magnitude, not exact)

| Bundle component | Samples | Estimated tokens |
|---|---|---|
| LCCC subset | 200,000 dialogues | ~24M |
| CharacterGLM subset | 1,034 sessions | ~0.6M |
| Character Codex | 15,939 cards | ~3.2M |
| RoleBench-zh | ~5,000 instructions | ~1.0M |
| Synthetic Macha data | 5,000 episodes | ~4.0M |
| **Training / fine-tune total** | **~222K samples** | **~33M tokens** |
| Evaluation set (CharacterEval+PersonaGym+RMTBench+PAL-Set sample) | ~15K samples | **~3–5M tokens** |

> Conclusion: Macha v0.1 can start within a **~33M token / ~220K sample** training-fine-tune budget (excluding LCCC full pre-training); the evaluation side **~3–5M tokens** already covers Chinese character, cross-environment, long multi-turn, and long-term-memory four dimensions. Synthetic data suggested ≤ 40% of training set.

### 8.6 Chinese-Market Section (RoleBench-zh / ChatHaruhi / CharacterEval / Baichuan-NPC / plus BaiJia)

Focuses on role-play data for China game / app landing, giving **content, scale, license, use** four-element detail.

| Dataset | Content | Scale | License | Use and caveats |
|---|---|---|---|---|
| **RoleBench-zh (RoleLLM Chinese)** | Chinese character profile + Context-Instruct-generated character instructions/scripts | Chinese **100** characters | Apache-2.0 | Fine-tune/Eval (C): character generalization, instruction following; commercial-friendly, recommend persona de-identification |
| **ChatHaruhi (incl. 54K)** | Film/anime character dialogue (script extraction + LLM enhancement), Chinese & English | 54K dialogue pairs / **32** characters | Data CC BY 4.0; code Apache-2.0 | Fine-tune/Eval (C): narrative memory; ⚠⚠ character IP (Haruhi/Big Bang Theory/Bright Sword etc.), commercial must replace characters |
| **CharacterEval** | Chinese RPCA evaluation + CharacterRM reward model; 4 dims 13 metrics | 1,785 dialogues / 23,020 examples / **77** characters | Repo MIT; paper CC BY-NC-SA 4.0 | Eval (C): Chinese-character evaluation benchmark; ⚠ personas from Baidu Baike / novels |
| **Baichuan-NPC (Baichuan)** | Character large model + platform solution (3T tokens pre-training on industry sites/books/scripts, OOC & CoT alignment method) | Original corpus not public | Dataset not open-source, method/platform only | Reference (C): OOC suppression, chain-of-thought alignment method, for Macha alignment design |
| **CharacterGLM (add)** | Character attributes (identity/interest/opinion/experience/achievement/social relations) + behavior (language style/emotion/interaction) | 1034 sessions / 250 characters (public subset) | Apache-2.0 | Fine-tune/Eval (C): Chinese-character customization benchmark, commercial-friendly |
| **BaiJia (add, 2025)** | Chinese historical-figure role-play corpus (biography/literature/family/office/events) | 19,281 characters | ⚠ not stated (subject to official site / repo) | Fine-tune/Eval (C): historical NPC low-resource cold-start, low IP risk |

> Chinese-market landing suggestion: on the training side use **CharacterGLM + RoleBench-zh + Character Codex + LCCC + synthetic data** as the commercial-safe backbone; on the evaluation side use **CharacterEval (research) + BaiJia (research)** to verify, and before commercial launch replace all third-party-IP characters with **self-owned personas** (ChatHaruhi, CharacterEval novel characters, Baichuan unreleased corpus must not enter commercial training directly).

### 8.7 New Source Collection (six-field format)

---

[Category]Academic paper / Dataset (Chinese historical-figure role-play, 2025)
[Title]BaiJia: A Large-Scale Role-Playing Agent Corpus of Chinese Historical Characters
[Link / file path]https://arxiv.org/abs/2412.20024 ; code/data https://github.com/BAI-LAB/BaiJia ; official site baijia.online
[One-sentence summary]The first Chinese historical-figure role-play corpus, covering 19,281 characters across Tang/Song/Yuan/Ming/Qing, a new resource for low-resource Chinese NPC cold-start; corresponds to Macha's C module and Chinese market.
[Key conclusions]
1. Scale 19,281 characters, with biography/literary works/family relations/office/historical events multimodal info.
2. GPT-4o-mini generates scenario dialogues + LLaMA-Factory LoRA fine-tuning, character ability significantly improved (avg +5%~+24%).
3. License not explicitly stated (⟳ subject to official site / repo LICENSE); historical figures are public figures / ancient texts, low IP risk.
[Reusable things]Historical-figure resume template, low-resource character SFT flow, 5-topic evaluation question set (background/era/relations/thought/achievement).

---

[Category]Academic paper / Platform / Dataset (social simulation, 2024)
[Title]OASIS: Open Agent Social Interaction Simulations with One Million Agents
[Link / file path]https://arxiv.org/abs/2411.11581 ; GitHub https://github.com/camel-ai/oasis ; dataset https://huggingface.co/datasets/echo-yiyiyi/oasis-dataset
[One-sentence summary]Million-scale LLM social-simulation platform (X/Reddit), supporting dynamic social networks and 23 action types, Apache-2.0; corresponds to Macha's M (memory / social simulation) module.
[Key conclusions]
1. Up to 1,000,000 agents, reproduces information spread, group polarization, herd effects.
2. Code Apache-2.0 (⟳ dataset license per HF card).
3. Provides Reddit/X two-platform agent profiles and simulation DB, high engineering-reference value.
[Reusable things]Large-scale agent simulation architecture, dynamic social graph, recommendation / report-system hooks, group-behavior metrics (spread depth / polarization measure).

---

[Category]Academic paper / Framework (city social simulation, 2025)
[Title]AgentSociety: Large-Scale Simulation of LLM-Driven Generative Agents
[Link / file path]https://arxiv.org/abs/2502.08691 ; GitHub https://github.com/zmier/AgentSociety
[One-sentence summary]City-scale LLM social-simulation framework, mind-behavior coupling + environment-tool chain, Apache-2.0 (switched 2025-04); corresponds to Macha's M/P modules.
[Key conclusions]
1. 10,000-agent scale, supports dataset / text / rule three environment types.
2. License Apache-2.0 (README verified).
3. Includes Benchmark Toolkit, open benchmark for user simulation and recommendation.
[Reusable things]Mind-behavior coupling modeling, city-environment interface, interactive visualization and intervention tools.

---

[Category]Academic paper / Evaluation benchmark (user-centric multi-turn role-play, 2025)
[Title]RMTBench: Benchmarking LLMs Through Multi-Turn User-Centric Role-Playing
[Link / file path]https://arxiv.org/abs/2507.20352 ; dataset https://huggingface.co/datasets/xiangh/RMTBENCH
[One-sentence summary]The first "user-intent-centric" Chinese-English bilingual multi-turn role-play evaluation, 80 characters / 8,000+ turns, fixing the "character-centric, isolated Q&A" flaw of existing benchmarks; corresponds to Macha's C/D modules.
[Key conclusions]
1. Includes character_understanding / maintenance / implicit_motivations / user_preference four scenarios, can concatenate dozens of turns of trajectory.
2. Data in Chinese & English (Claude 3.5 / 4.5 two versions), user-side utterances only, no character replies.
3. HF gated (requires agreeing to terms), ⚠ evaluation only, not into training.
[Reusable things]User-motivation-driven dialogue construction, multi-turn evaluation dimensions and LLM-as-Judge prompts, scenario-concatenation protocol.

---

[Category]Academic paper / Dataset (Chinese long-term personalized dialogue, 2025)
[Title]PAL-Set: A Dataset for Long-Term Personalized Agent Interaction (PAL-Bench)
[Link / file path]Search source https://www.selectdataset.com/dataset/5f898bfc483eb7ccb7cd34b34e5354bb (⟳ original arXiv not verified, subject to paper)
[One-sentence summary]Renmin Univ + Alibaba 2025 Chinese long-term user-agent interaction dataset, 100 virtual users × 29 sessions × 401 turns, the first benchmark for Chinese long-term memory / personalization research; corresponds to Macha's M/D modules.
[Key conclusions]
1. Multi-stage LLM synthesis + human verification, with timestamped behavior logs and multi-turn service dialogues.
2. Supports requirement restatement, solution proposal, multi-turn dialogue interaction three task types.
3. ⚠ research use, commercial needs authorization (⟳ subject to official license).
[Reusable things]Long-term user-profile schema, timeline event modeling, implicit-need inference evaluation protocol.

---

[Category]Academic paper / Evaluation benchmark (speech role-play, 2025)
[Title]VoxRole: A Comprehensive Benchmark for Evaluating Speech-Based Role-Playing Agents
[Link / file path]https://arxiv.org/abs/2509.03940
[One-sentence summary]The first speech role-play evaluation benchmark, 13,335 multi-turn dialogues / 65.6h speech / 1,228 characters (261 films), covering intonation / prosody and other paralinguistic features; corresponds to Macha's C module (speech NPC).
[Key conclusions]
1. Two-stage automated flow: film audio-track-script alignment → LLM builds multi-dimensional character profile.
2. Scale 13,335 dialogues / 65.6h / 1,228 characters.
3. ⚠⚠ characters from films (IP), evaluation reference only, not into training.
[Reusable things]Speech character-profile construction flow, paralinguistic-feature consistency evaluation dimensions.

---

[Category]Academic paper / Evaluation framework (role-agent dynamic evaluation, 2024)
[Title]PersonaGym: Evaluating Persona Agents and LLMs
[Link / file path]https://arxiv.org/abs/2407.18416 ; code https://github.com/vsamuel2003/PersonaGym
[One-sentence summary]The first role-agent dynamic evaluation framework + PersonaScore metric, 200 personas / 10,000 questions, revealing "bigger model not necessarily stronger character ability"; corresponds to Macha's C module evaluation.
[Key conclusions]
1. 5-task cross-environment dynamic evaluation, PersonaScore based on decision theory, aligned with humans.
2. Evaluated 10 mainstream LLMs, GPT-4.1 and LLaMA-3-8B PersonaScore close.
3. License subject to repo LICENSE (⟳ not explicitly stated).
[Reusable things]Dynamic evaluation protocol, PersonaScore metric, 5-task rubric.

---

[Category]Academic paper / Dataset (social-media real-user profiles, 2025)
[Title]BluePrint / SIMPACT: A Social Media User Dataset for LLM Persona Evaluation and Training
[Link / file path]https://arxiv.org/abs/2510.02343
[One-sentence summary]6.8M message threads / 236K anonymized aggregate-user BlueSky real-behavior dataset, supporting real-behavior grounded persona modeling; corresponds to Macha's C / social simulation.
[Key conclusions]
1. Scale 6.8M message threads / 236K users, anonymized aggregate, privacy-preserving.
2. Text + non-text actions, supports training and evaluation.
3. ⚠ research use, contains real user behavior (needs compliance).
[Reusable things]Behavior-grounded persona modeling, group-level evaluation metrics, privacy-preserving aggregation method.

---

[Category]Academic paper / Evaluation method (character personality fidelity, 2024)
[Title]InCharacter: Evaluating Personality Fidelity in Role-Playing Agents through Psychological Interviews
[Link / file path]https://arxiv.org/abs/2310.17976 ; project page http://incharacter.github.io
[One-sentence summary]Uses psychological scales for "interview-style" character-personality-fidelity evaluation, releases 18,304 interview dialogues, 32 characters / 14 scales, up to 80.7% accuracy; corresponds to Macha's C module personality-consistency evaluation.
[Key conclusions]
1. Interview-style evaluation outperforms self-report, covers BFI/16P/DTDD and other 14 scales.
2. Releases 18,304 interview dialogues, usable as fine-tune data.
3. License subject to paper / repo (⟳).
[Reusable things]Personality-fidelity evaluation protocol, psychological-scale rewrite prompts, interview-dialogue dataset.

---

[Category]Academic paper / Method (personality-indicative data augmentation, 2024)
[Title]Capturing Minds, Not Just Words: Enhancing Role-Playing Language Models with Personality-Indicative Data (RolePersonality)
[Link / file path]https://arxiv.org/abs/2406.18921
[One-sentence summary]Uses psychological-scale questions to generate "personality-indicative" data to fine-tune RPLM, 16 ChatHaruhi + 30 RoleLLM characters, ~32K samples, improving personality fidelity; corresponds to Macha's C module fine-tuning.
[Key conclusions]
1. 3 subsets (Full/Single, Part/Single, Part/Multi), multi-turn data improves consistency.
2. LoRA fine-tuning on Mistral-7B, outperforms CharacterLLM/RoleBench at same scale.
3. ⚠ research use (⟳ subject to paper).
[Reusable things]Personality-indicative data construction pipeline, filtering / multi-turn augmentation method, LoRA fine-tuning config.

---

### 8.8 Post-Deepening To-Do (P2 follow-up, incremental)

- [ ] Implement 8.2 schema as `macha-data-schema.json` contract + loader (echoing Section 7 registry tool).
- [ ] Implement S5 quality-gate script for 8.3 synthetic pipeline (de-dup / PII / IP / consistency).
- [ ] Verify licenses item-by-item for RMTBench, PAL-Set, VoxRole, BluePrint (⟳ marked items).
- [ ] Run v0.1 training-evaluation smoke test with 8.4 starter bundle, backfill real token counts.
