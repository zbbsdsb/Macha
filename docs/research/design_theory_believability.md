# NPC Believability Requirement Document (Design Theory → Technical Metrics)

> **Category**: `information_needs.md` Category 4 "Game Design Theory: NPC Believability and Gameplay."
> **Document nature**: Research sub-task deliverable (not a Demo, but a design-theory translation layer serving Macha's "standard skeleton").
> **Companion documents**: `direction.md` (minimum verifiable direction: long-term memory + character consistency), `positioning.md` (four-paper positioning), `architecture.md` (target architecture: Perception / Memory / Reasoning / Action four layers), `evaluation_benchmarks.md` (believability / consistency evaluation-dimension tables F1–F13 / E9–E13).
> **Core proposition**: Macha serves "designing believable NPCs," not "a stronger chatbot." This document translates design language (MDA, interactive narrative, believability theory, AI-native design) into technical metrics Macha must be able to measure and land, so that `architecture.md`'s modules and `evaluation_benchmarks.md`'s dimensions form a closed loop.

---

## 0. How to Use This Document

- **Section 1** is the main deliverable for engineering and product teams: the **design-concern → technical-requirement mapping table**. Each row states "what the design wants to achieve" and "what Macha must do and with what metric."
- **Section 2** maps design-theory concepts (MDA / interactive narrative / believability / AI-native) to Macha's modules and metrics, enabling a traceable chain between architecture and evaluation.
- **Sections 3–5** are three special analyses: players' expectations of NPC memory, open-world vs. narrative-game behavior differences, and the "semantic adjudication / multi-agent simulation" case teardown of AI-native games.
- **Section 6** registers key sources in the fixed format agreed in `information_needs.md`.
- **Section 7** gives Macha's landing design principles and to-do.

> Note: All URLs come from this research via actual WebSearch / WebFetch. The MDA original PDF (northwestern domain) was confirmed accessible via WebFetch (redirected to `users.cs.northwestern.edu/~hunicke/MDA.pdf`); other main links are usable pages returned by search. A few classic papers (Bates 1994, Loyall & Bates 1997) are registered via abstract / mirror pages; it is recommended to complete the original sources before formal citation.

---

## 1. Design Concern → Technical Requirement Mapping Table (core deliverable)

> Each row = one design concern. The right columns give Macha's **technical requirement** and **measurable metric** (reusing `evaluation_benchmarks.md`'s F/E dimensions where possible).

| # | Design concern | Design intent (what the designer wants) | Macha technical requirement | Measurable metric (linked eval dimension) |
|---|---|---|---|---|
| C1 | **Believability** | Players subjectively believe "this is a real being with inner life," willing to invest emotion | NPC must present "the illusion of life": consistency, emotion, awareness, sociability, understandability coexisting in stable performance | Paiva nine-dimension Likert scale (behavior consistency / experience change / awareness / behavior understandability / personality / emotion expression / sociability / visual impact / predictability) → **F3 / F7** |
| C2 | **Role Fidelity** | NPC keeps personality, speaking style, values, taboos stable over long interaction, no "instant face-change" | Personality/values/taboos must be injected into the Reasoning layer as immutable constraints; dialogue and action both checked by the Character layer | RoleBench three metrics CUS / RAW / SPE; DNLI entailment consistency; adversarial persona-drift detection → **F1** |
| C3 | **Memory Expectations** | Players expect NPC to "remember the important, forget the trivial," memory serving relationship and narrative not information piling | Implement "purposeful memory": high-value events (betrayal/loyalty/promise/shared risk) retained first, low-value interactions can decay; memory must drive later attitude and behavior | Memory hit rate, memory-decay reasonableness, cross-session attitude consistency, reputation / gossip propagation correctness → **F2 / F4** |
| C4 | **Agency** | NPC has its own goals, fears, social relations, and behavior thresholds; can act proactively not just passively answer | Reasoning layer must include "goal + planning + threshold trigger"; NPC can decide on its own without player input (see C9 world realness) | Autonomous-goal achievement rate, goal-driven behavior ratio, planning-success rate (AgentBench/SmartPlay idea) → **F5** |
| C5 | **Predictability** | Behavior can be understood and anticipated by players (not over-random, not fully rigid), foundation of playability and trust | Behavior-trajectory entropy must lie in the "interesting but not chaotic" band; decisions replayable and explainable | Behavior-trajectory entropy / explainability score, Paiva predictability scale → **F7 / E12** |
| C6 | **Emotion & Sociality** | NPC has emotion, empathizes, has a relation network with others, emotion change fits personality and situation | Memory/Reasoning maintain emotion state and relation graph; emotion and relations drive dialogue and action choices | Emotion consistency, relation-evolution reasonableness, multi-person social-reaction consistency → **F3 / F1** |
| C7 | **Emergent Narrative** | Story "grows" from interaction rather than pre-written script; player feels the protagonist of their own story | Driven by structured world state + character motivation, not pure free-text continuation; provide "narrative gravity" constraints | Narrative coherence, player-agency score, long-run non-collapse rate → see Section 5 |
| C8 | **Bounded Autonomy** | NPC is free within "character / world-rule" boundaries; when crossing, the system vetoes or guides rather than generating infinitely | Action-layer output must be filtered by world state, character motivation, narrative alignment; define "mechanical invariants" (goal/rule/state/feedback/pacing/agency) | Boundary-crossing rate, narrative-alignment rate, style-compliance rate → **F1 / F4** |
| C9 | **Lives Beyond You (world realness)** | When player is absent, NPC still has daily life, relations, and life; world does not freeze around player | Multi-NPC scheduling and shared world clock; pre-set relation networks and autonomous schedules between NPCs; memory and events propagate across NPCs | Autonomous-schedule coverage, NPC-relation consistency, world-event correctness during player absence → **F5 / F2** |
| C10 | **Session Continuity** | Return days/months later, NPC still remembers relations, promises, consequences | Long-term memory externalized (not just context window); world state stored outside the model (server / external state) | Cross-session memory recall rate, knowledge-update correctness (LongMemEval KU) → **F2 / F4** |
| C11 | **Anti-hallucination / anti-character-drift** | NPC does not fabricate un-happened events, no self-contradiction, no confusing new and old facts | Memory and Character layers as "fact and personality anchors," consistency check before action | LoCoMo adversarial set, LongMemEval Abstention, memory-consistency stress test → **F4** |

---

## 2. Design-Theory Concept → Macha Module / Metric Mapping

| Source concept | Core claim | Maps to Macha module | Maps to Macha metric |
|---|---|---|---|
| **MDA (Hunicke, LeBlanc, Zubek 2004)** | Game = Mechanics (rules/data/algorithms) → Dynamics (runtime emergent behavior) → Aesthetics (player emotional response); designer builds forward, player experiences backward; "a game is more like a designed artifact than a media, content is its behavior" | **Mechanics**→ Macha's interface contracts (`Observation`/`MemoryItem`/`BaseAgent`) and `architecture.md`'s algorithm layer; **Dynamics**→ Perception→Memory→Reasoning→Action emerging under player input; **Aesthetics**→ player subjective believability (F3/F7) | Use "mechanical invariants" to ensure Dynamics converges to target Aesthetics; measure Aesthetics via player research (TrueSkill pairing) → **F3 / F7 / E13** |
| **Interactive Drama (Chris Crawford)** | True interaction = "listen-think-speak" loop among multiple active agents; only "interactive storytelling" not "interactive story"; system must generate story instantly from player feedback while keeping structural integrity | Macha's Reasoning is the "story-engine core": maintains storyworld (characters, relations, motivations, rules), generates next step instantly from player actions; dialogue is one kind of Verb | Narrative coherence, player agency (whether there are truly "dramatic and diverse" choices), structural integrity → see C7 |
| **Believability (Bates 1994; Loyall & Bates 1997; Paiva/Gomes 2013)** | Believable = provide "the illusion of life" so audience suspends disbelief; emotion must be expressed at the right moment; language and action must be driven by the same personality/emotion; nine-dimension measure (behavior consistency/experience change/awareness/understandability/personality/visual/emotion expression/predictability/sociability) | **Character layer** (personality, emotion, relations) runs through Perception→Memory→Reasoning→Action; emotion state machine inside Reasoning; visuals/actions presented by Action layer | Paiva nine-dimension scale + Game Agent Matrix → **F1 / F3 / F7** |
| **AI-based Game Design (Eladhari et al. 2011; Treanor et al. 2015)** | AI should be the game's "co-author" not a smoke-and-mirrors; proposes design patterns: AI is Visualized, AI as Role-model, Mixed-Initiative, etc.; Mechanics/Dynamics/Aesthetics must deeply bind the AI system | Macha provides not "smarter dialogue" but "AI mechanism primitives" (memory, reflection, planning, social reasoning) usable by designers to construct gameplay; supports mixed-initiative (player + NPC co-creation) | Designer combinability, pattern reuse, whether it produces "expressive AI" (player must read NPC intent) → **F5 / C7** |
| **The Sims pheromone model (Will Wright)** | Character is "environmentally distributed intelligence": each object broadcasts a "need smell" (food/energy/social…), Sim follows the smell; **deliberately keeps "imperfect autonomy"** — early versions too smart made player irrelevant, so randomness and "hidden time bombs" were added to maintain play tension | Macha's Perception layer marks world objects as "signal sources attractable by desire/goal"; Autonomy parameter must be tunable (too smart = player irrelevant, too dumb = boring); behavior threshold introduces controllable randomness | Autonomy tuning curve, player-intervention necessity, behavior diversity → **C4 / C5 / F5** |
| **AI-Native design ontology (arXiv:2607.00527)** | Counterfactual standard: remove runtime generative AI, does the core loop collapse? G/N dual-axis classification; core difficulty is "organizing semantic openness into stable gameplay," relying on mechanical invariants | Macha's Action layer carries the **N-axis mechanism**: Semantic Adjudication, Multi-Agent Simulation, Generative Narrative, etc.; all generation constrained by "goal/rule/state/feedback/pacing/agency" | Whether the core loop is still playable after removing generative components (counterfactual test), mechanical-invariant coverage → see Section 5 |
| **Generative Agents / Smallville (arXiv:2304.03442)** | Memory stream + reflection + planning produce believable social behavior; memory has time decay, importance weighting, semantic association; reflection triggered at importance threshold | Directly corresponds to Macha's Memory (decay/weighting/retrieval) + Reasoning (reflection and planning) three-layer | LoCoMo / LongMemEval / MemoryArena → **F2 / F4 / F5** |

---

## 3. Special Analysis A: Players' Expectations of NPC Memory ("what exactly should the NPC remember")

Design language often treats "memory" as a database problem, but players perceive **relationship and narrative weight**. Synthesizing industry and community research (see Section 6 sources), we distill the following requirements:

### 3.1 Purpose-Driven Memory, not full-volume memory

- **High-value memory** (retain first): betrayal or loyalty behavior, faction / moral-orientation drift, unfulfilled promises, moments of shared risk or shared success, major choices affecting relations.
- **Low-value memory** (should decay or be ignored): every trivial dialogue option, repeated tiny actions — remembering too much creates noise and narrative inconsistency.
- **Design implication**: Macha's Memory layer must do **importance weighting + decay + semantic retrieval**, not stuff the dialogue transcript into the context. Directly corresponds to `evaluation_benchmarks.md`'s F2 (long-term memory stability) and F4 (anti-hallucination).

### 3.2 Four-type Memory-System Design Genealogy (for Macha selection reference)

| Type | Mechanism | What it can remember | Limitation | Implication for Macha |
|---|---|---|---|---|
| Flag / Reputation | Boolean flag or numeric reputation, queried on NPC interaction | Whether an event happened (`saved_apothecary=true`; `reputation:merchant_guild=-12`) | No semantics, no detail | As Macha Memory's "hard-fact layer," cheap and reliable |
| Simulation | Event log with emotion weight + decay | Emotional memories like trauma/insult, rich but not dialogable | NPC cannot "talk" memory | Macha can use emotion weight as retrieval-ranking signal |
| Nemesis | Track encounters and reshape NPC identity | Combat relations (who killed me, I fear fire) | Narrow scope, often patent-locked | Can serve as example of Macha "relation + fear" sub-module |
| AI / Vector | Vectorize dialogue content, semantic-similarity retrieval | Your exact words and intent, not just events | Depends on LLM, has latency/cost, probabilistic recall | **Macha's main memory paradigm** (RAG + vector), but must stack a Flag layer as fallback |

### 3.3 Social Propagation of Memory: Reputation and Gossip Networks

- Players do not expect "every NPC omniscient," but expect **who knows what** to differ: guard knows crimes, tavern keeper knows gossip, priest knows oaths. This drives exploration (player seeks "the one who remembers that event").
- **Witness & gossip chains** let information mutate in propagation, introducing uncertainty and social dynamics — more believable than omniscient NPCs.
- **Design implication**: Macha's Memory should support **role-based access + propagation rules**, not a global shared blackboard.

### 3.4 Showing Memory to the Player (UX)

- In-world clues (NPC dialogue, wanted posters, town-hall ledger referencing past deeds), player dashboard (who remembers you, why), foreshadowing (actions have consequences) — make memory "fair and meaningful."

---

## 4. Special Analysis B: Open-World vs. Narrative-Game NPC Behavior Differences

| Dimension | Open World | Narrative / RPG | Indication for Macha |
|---|---|---|---|
| Dominant aesthetics | Discovery / Sensation / Fellowship (MDA eight) | Narrative / Expression / Fantasy | Macha's Character layer should allow switching "believability focus" by game type |
| NPC count & density | Massive passerby NPCs, need basic dialogue and emergent behavior | Few key NPCs, deep characterization | Layering: passersby use lightweight FSM/polling, key NPCs use full Macha cognitive stack |
| Player-behavior predictability | Low (diverse behavior, expect emergent story) | Higher (main-line nodes need stability) | Open world relies more on C9 world realness; narrative relies more on C2 role consistency |
| Immersion-killer | "Wooden" feel, no intelligent reaction to unique behavior | Character off-persona, long-arc plot collapse | Both require F1/F4, but narrative side has stricter threshold |
| Recommended architecture | "Hybrid plan": few important NPCs get dynamic dialogue as highlights, rest use state machines | GPT/LLM deep role-play + main-line framework (Fable-style) constraints | Macha should support "cognitive-stack downgrade" (passerby NPC does not load full Reasoning) to control cost (E10/E11) |
| Does world freeze around player | No — NPCs have independent schedules, relations, life (Stardew Valley paradigm) | Partly — main line can wait, but world should still "have a pulse" | C9 world realness holds for both, different intensity |

> Key insight (from Stardew Valley teardown and GAEA system coverage): **"illusion of autonomy"** — schedules are hard-coded, but vary by day/weather/season and hint at personality, so players feel the character is "choosing." This is exactly Macha's engineering trick for high believability at low cost: use deterministic scheduling to create "sense of life," use LLM to create "unpredictable depth."

---

## 5. Special Analysis C: "Semantic Adjudication" and "Multi-Agent Simulation" Case Teardown of AI-Native Games

Based on `arXiv:2607.00527`'s G/N dual-axis classification, the following two N-axis mechanisms are gameplay primitives Macha as a "standard skeleton" must build in.

### 5.1 Semantic Adjudication

> Definition: player inputs in natural language / open actions, system **instantly interprets its semantics, rewrites game state, and adjudicates consequences**, rather than matching within pre-written branches.

**Case 1: Hidden Door (AI Dungeon Master / DM)**
- Mechanism: human authors hand-write "story beats + world-rule set + bridge-card library"; ML/LLM adjudicates each turn's player natural-language action into executable game-state change (card-based world state), sometimes with dice for success/failure.
- Key design: **freedom within walls** — player cannot "write an invincible silver bow to one-shot the galaxy" (ChatGPT would agree, Hidden Door vetoes and guides). World state **lives in the engine layer not the dialogue context**, which is why its memory and coherence lead (Memory & Continuity 4/5, Longevity 4/5).
- Implication for Macha: the Action layer must have an **Adjudicator** mapping the LLM's free output to constrained world state; this is the landing form of `architecture.md`'s Action "structured output" and C8 bounded autonomy.

**Case 2: Multi-agent Balderdash's "judge LLM"**
- Mechanism: centralized game engine + multiple LLM players + one **judge LLM evaluating semantic equivalence** (defining proximity to truth).
- Implication for Macha: semantic adjudication can be abstracted as a "**referee agent**" pattern — in PvP/PvE or social-reasoning scenarios, an independent adjudication Agent checks semantic consistency, avoiding the main Agent talking to itself. Corresponds to Macha's "reflection / verification" step (F4 anti-hallucination).

### 5.2 Multi-Agent Simulation

> Definition: multiple AI characters each with goals / emotion / relations, **evolving in parallel, influencing each other** in a shared world; the player is just one of them.

**Case 1: The Sims (classic exemplar)**
- Mechanism: objects broadcast "need smell," Sim follows smell to act autonomously; player can override but Sims not fully autonomous; **deliberate imperfect autonomy** maintains play tension (see Section 2 mapping).
- Implication for Macha: multi-NPC "environmentally distributed intelligence" + tunable autonomy is the baseline paradigm for open-world Macha.

**Case 2: Generative Agents / Smallville (generative-agent town)**
- Mechanism: 25 agents, memory stream (time decay + importance weighting + semantic association) + reflection (importance-threshold triggered) + planning, produce believable social behavior.
- Implication for Macha: this is the "reference implementation" of Macha Memory/Reasoning three-layer; but note its **lack of game mechanical invariants** — used directly in games it "emerges but not into gameplay," must stack 2607's mechanical constraints (C7/C8).

**Case 3: Spyfall Arena / multi-agent reasoning benchmark**
- Mechanism: multiple LLMs play social-reasoning game (Spyfall) autonomously, centralized engine logs each game's JSON (question/answer/vote/result) for deception and reasoning benchmark.
- Implication for Macha: multi-agent simulation needs **observable centralized logging** (corresponds to E12 observability), otherwise emergent behavior cannot be debugged.

> **Synthesis**: If Macha is to be a "standard skeleton," its Action layer must simultaneously provide (a) the semantic-adjudication primitive (Adjudicator + optional Judge Agent) and (b) the multi-agent-scheduling primitive (shared world state + independent cognitive stack + centralized logging), both constrained by "mechanical invariants" — exactly the core thesis of the 2607 paper on AI-native games.

---

## 6. Source Collection (in agreed format)

> Each entry follows `information_needs.md`'s specified format: [Category]/[Title]/[Link / file path]/[One-sentence summary]/[Key conclusions]/[Reusable things]

---

[Category]Academic paper / Design theory
[Title]MDA: A Formal Approach to Game Design and Game Research (Hunicke, LeBlanc, Zubek, 2004)
[Link / file path]https://users.cs.northwestern.edu/~hunicke/MDA.pdf (WebFetch confirmed redirect accessible); mirror interpretation https://gdad.wiki/wiki/game-design/foundations-theory/mda-framework
[One-sentence summary]Proposes the Mechanics→Dynamics→Aesthetics three-layer framework, arguing "a game is more like a designed artifact than media, content is its behavior," and revealing the asymmetry that designers build forward, players experience backward.
[Key conclusions]
1. Mechanics=rules/data/algorithms; Dynamics=runtime emergent behavior; Aesthetics=player emotional response (eight types: sensation/fantasy/narrative/challenge/fellowship/discovery/expression/playground).
2. Designer builds M to A, player experiences A to M, opposite directions, gap closed only by playtesting.
3. "A game's content is behavior, not content flowing to a passive audience" — directly supports Macha treating NPC as "behavior system" not "content generator."
[Reusable things]M/D/A layered vocabulary + eight-aesthetic list + asymmetric design method — can serve as the underlying framework for Macha's "design intent → technical requirement" (Section 1) and "module mapping" (Section 2).

---

[Category]Design theory / Industry material
[Title]The Sims design notes: Will Wright's "pheromone" autonomous-character model
[Link / file path]https://www.engadget.com/2010/11/08/will-wright-explains-what-the-sims-and-an-ant-colony-have-in-com ; https://www.museumofplay.org/games/the-sims ; https://spotofspawn.com/news/45464835/
[One-sentence summary]Wright reveals The Sims core is "objects broadcast need smells, Sim follows smell to act" environmentally distributed intelligence, and early autonomy too strong made player irrelevant, so randomness and "hidden time bombs" were deliberately added.
[Key conclusions]
1. Sim intelligence comes from SimAnt's ant-pheromone model: each object broadcasts eight needs' "smell," character follows to satisfy.
2. Early version "autonomy too good, nothing player does beats autopilot" → must lower autonomy, introduce controllable randomness to keep play tension.
3. The Sims is more "toy" than "game": no end, infinite replay from semi-autonomous characters' daily drama.
[Reusable things]"Environmentally distributed intelligence + tunable autonomy + imperfect autonomy" paradigm — direct reference for Macha Perception (signal-source marking) and Autonomy parameter design (C4/C5).

---

[Category]Academic monograph / Design theory
[Title]Chris Crawford on Interactive Storytelling (Interactive Storytelling, Crawford)
[Link / file path]Review and definition https://www.igfmobile.com/design/book-review-i-chris-crawford-on-interactive-storytelling-i- ; author site (Erasmatron prototype) http://www.erasmatazz.com/
[One-sentence summary]Crawford strictly defines "interaction = listen-think-speak loop among multiple active agents," argues only "interactive storytelling" not "interactive story," system must generate story instantly from player feedback while keeping structural integrity.
[Key conclusions]
1. Interaction must happen over time; interactive story does not exist, only interactive storytelling.
2. Story engine must generate story instantly in storyworld from player choices while maintaining "structural-integrity feel."
3. Verbs are what the player "can do" in the interaction medium; a rich verb library is the premise of dramatic choice.
[Reusable things]"Storyworld + instant generation + structural integrity" three elements — blueprint for Macha Reasoning as "story-engine core" (C7).

---

[Category]Academic paper / Design theory
[Title]AI-Based Game Design: Enabling New Playable Experiences (Eladhari et al., 2011)
[Link / file path]https://tr.soe.ucsc.edu/sites/default/files/technical-reports/UCSC-SOE-11-27.pdf
[One-sentence summary]Proposes "AI-based game design" practice: deeply integrate AI-system capability into game-design co-creation, opposing only using "smoke and mirrors" to fake intelligence.
[Key conclusions]
1. A fully predictable system is "dead"; AI must be robust enough to support player experimentation and exploration, not Eliza-effect fake intelligence.
2. Distinguish "fully predictable physical system" from "not-fully-predictable human-like behavior" — only the latter needs players to reason about intent.
3. AI should be the core co-author of game design, not an enhancement layer.
[Reusable things]"Expressive AI / player must read AI intent" principle + co-creation methodology — basis for Macha's positioning as "gameplay-primitive provider" not "dialogue enhancer" (C7).

---

[Category]Academic paper / Design patterns
[Title]AI-Based Game Design Patterns (Treanor, Zook, Eladhari, Togelius et al., FDG 2015)
[Link / file path]http://julian.togelius.com/Treanor2015AIBased.pdf ; Strathclyde archive https://strathprints.strath.ac.uk/57219/
[One-sentence summary]Distills design patterns from existing AI games (AI is Visualized, AI as Role-model, Mixed-Initiative, etc.), proposes a generative ideation method of "pattern × AI technique."
[Key conclusions]
1. AI-based games put AI in the player-experience foreground, not the supporting role of traditional commercial games.
2. Design patterns (e.g., visualize AI state, AI as imitation object) can serve as generative ideation tools.
3. MDA's M/D/A must deeply bind the AI system.
[Reusable things]AI-game design pattern family — Macha can define a "composable gameplay-primitive" list from this (C7/C8).

---

[Category]Academic paper / Believability theory (classic)
[Title]The Role of Emotion in Believable Agents (Bates, 1994)
[Link / file path]Abstract page https://citeseer.ist.psu.edu/viewdoc/summary?doi=10.1.1.468.1779 ; original Commun. ACM 37(7):122–125
[One-sentence summary]Argues "emotion expressed clearly at the right moment" is the core requirement of believable characters, should draw "illusion of life" insights from art (animation/drama).
[Key conclusions]
1. Believability ≠ honest and reliable, but provides "illusion of life" so audience suspends disbelief.
2. Emotion is the central need of believable interactive characters, must be expressed at the right moment.
3. AI researchers should learn from traditional animators (Disney's Thomas & Johnston) to "make characters seem to think, to decide."
[Reusable things]"Emotion as believability infrastructure" principle — Macha Character layer must include emotion state machine (C1/C6).

---

[Category]Academic paper / Believability theory (classic)
[Title]Personality-Rich Believable Agents That Use Language (Loyall & Bates, 1997, Oz project)
[Link / file path]https://chatbots.org/paper/personality-rich_believable_agents_that_use_language ; DOI 10.1145/267658.267681
[One-sentence summary]Extends behavior architecture Hap to support natural-language generation, so text and action/perception/reasoning/emotion are uniformly driven by the same personality.
[Key conclusions]
1. Believable Agent must tightly couple language generation with action, perception, reasoning, emotion.
2. Text must vary with emotion state and specific personality, with real speech-flow features like pauses / restarts.
3. Language and action jointly serve communication goals, perception affects language choice.
[Reusable things]"Language-action-emotion uniformly driven by personality" architecture principle — direct basis for Macha Character layer constraining Reasoning/Action (C2/C6).

---

[Category]Academic paper / Believability measure
[Title]Metrics for Character Believability in Interactive Narrative (Gomes, Paiva, Martinho, Jhala, ICIDS 2013)
[Link / file path]Related survey index https://www.semanticscholar.org/paper/Developing-a-Scale-for-Measuring-the-Believability-Guo-Adamo/c7ddfcb97af77ae32dc13772645612da92504aa5 (this page cites and summarizes Gomes et al. 2013 nine dimensions)
[One-sentence summary]Proposes nine-dimension measure for character believability: behavior consistency, experience change, awareness, behavior understandability, personality, visual impact, predictability, sociability, emotion expression.
[Key conclusions]
1. Believability can be split into nine measurable dimensions, enabling systematic evaluation not by feel.
2. Dimensions cover "inner consistency (behavior/personality)" and "outer expression (visual/emotion/social)" two classes.
3. Complements the Game Agent Matrix (Warpefelt), forming a believability evaluation toolbox.
[Reusable things]Nine-dimension scale — directly becomes Macha F3/F7 subjective-evaluation questionnaire template (already cited in `evaluation_benchmarks.md` Section 4).

---

[Category]Academic paper / AI-native design ontology
[Title]AI Native Games: A Survey and Roadmap (arXiv:2607.00527, Xu et al., 2026)
[Link / file path]https://www.arxiv.org/abs/2607.00527 ; survey interpretation https://www.emergentmind.com/papers/2607.00527 ; review https://www.pith.science/paper/2607.00527
[One-sentence summary]Uses counterfactual standard to define "AI-native games" (remove runtime generative AI, does core loop collapse), proposes G/N dual-axis classification, points out core difficulty is "organizing semantic openness into stable gameplay."
[Key conclusions]
1. Counterfactual three tests: runtime generative AI exists, gameplay loop depends on its output, and cannot be replaced by finite preset content.
2. G/N dual-axis: G=player-visible game type, N=dominant mechanism making AI irreplaceable (semantic adjudication / multi-agent simulation / generative narrative / relational companionship, etc.).
3. 53 samples concentrate on language-forward design; semantic adjudication, multi-agent simulation etc. still under-represented — exactly Macha's opportunity.
4. Mechanical invariants (goal/rule/state/feedback/pacing/agency) are the basis for turning open semantics into stable gameplay.
[Reusable things]"Counterfactual test + G/N dual-axis + mechanical invariants" methodology — direct framework for Macha defining "AI gameplay primitives" and acceptance criteria (Section 5).

---

[Category]Industry case / Semantic adjudication
[Title]Hidden Door (AI narrative engine / AI Dungeon Master)
[Link / file path]Official FAQ https://www.hiddendoor.co/help/faq ; The Verge coverage (2025-08) https://www.univ-tours.fr/annuaire/m-jean-philippe-lafontaine?live-news-8466682-2026-05-21-hidden-door-is-an-ai-storytelling-game-that-actually-makes-sense-the-platform-le ; comparison review https://arcanumrpgs.com/blog/ai-dungeon-vs-hidden-door
[One-sentence summary]Achieves coherent and bounded AI narrative via "card-based world state + human-written beats + LLM instant adjudication of player natural-language actions," world state lives in engine not dialogue context.
[Key conclusions]
1. Player input adjudicated into constrained world-state change, with dice etc. mechanics; "freedom within walls" is why its coherence leads (Memory 4/5, Longevity 4/5).
2. World state survives outside the model (card-engine layer), not just context window — avoids long-run collapse.
3. Contrasts with AI Dungeon's "wall-less sandbox": high freedom but low coherence.
[Reusable things]"Adjudicator + external world state" architecture — direct exemplar for Macha Action-layer semantic-adjudication primitive (C8 / Section 5.1).

---

[Category]Academic paper / Multi-agent simulation
[Title]Generative Agents: Interactive Simulacra of Human Behavior (Stanford Smallville, arXiv:2304.03442)
[Link / file path]https://arxiv.org/abs/2304.03442 (also see `positioning.md` / `evaluation_benchmarks.md`)
[One-sentence summary]25 LLM agents produce believable social behavior in a shared town via "memory stream + reflection + planning," the reference implementation of Macha's memory/reasoning three-layer.
[Key conclusions]
1. Memory has time decay, importance weighting, semantic association; reflection triggered at importance threshold, distilling higher-level self-cognition.
2. Produces believable emergent social behavior (information spread, relation evolution, coordinated events).
3. But it lacks game mechanical invariants — used directly in games it "emerges not into gameplay," must stack constraints.
[Reusable things]Memory/reflection/planning three-layer structure — direct blueprint for Macha Memory + Reasoning modules (F2/F4/F5).

---

[Category]Community / Industry research / Player memory expectation
[Title]7 Games Where NPCs Actually Remember You (NPC memory-system taxonomy and cases)
[Link / file path]https://wanderfolk.ai/games-where-npcs-remember-you ; persistent character-memory design https://yoo.be/when-npcs-keep-receipts-persistent-character-memory ; 2026 survey https://aivexify.com/ai-npcs-that-remember-players
[One-sentence summary]Systematically reviews Flag/Simulation/Nemesis/Vector four NPC-memory mechanisms and representative games (Wanderfolk, Shadow of Mordor, Dwarf Fortress, etc.), pointing out "remembering the right things" matters more than "remembering more."
[Key conclusions]
1. Four memory lineages: flag/reputation (hard fact), simulation (emotion log + decay), nemesis (combat-relation reshape), vector (semantic recall of exact words).
2. High-value memory (betrayal/loyalty/promise/shared risk) retained first; low-value interaction decays — "deliberate forgetting" improves believability.
3. Reputation and gossip networks let memory propagate organically in society, more believable than omniscient NPCs.
[Reusable things]Memory taxonomy + importance/decay/semantic-retrieval principles — Macha Memory-layer selection and design baseline (C3 / Section 3).

---

[Category]Community analysis / Open-world NPC design
[Title]NPCs with Lives Beyond You: autonomous NPCs in Stardew Valley (open-world autonomous-character paradigm)
[Link / file path]https://alamrafiul.com/blogs/npcs-lives-beyond-you ; GAEA system coverage https://www.anaor.cn/news/126b13599738.html ; stream-of-consciousness turn https://tsight.io/articles/7335930
[One-sentence summary]Tears down Stardew Valley's "illusion of autonomy": NPCs have schedules/relations/life and run even when player is absent, revealing open-world believability comes from deterministic scheduling creating "sense of life."
[Key conclusions]
1. Traditional narrative's "world revolves around protagonist" fails in open-world / life-sim; characters must have "life when you're not there."
2. Schedules are hard-coded but vary by day/weather/season and hint at personality → player feels "choice" not "rail."
3. Open-world NPCs must simulate daily schedule, work, environmental reaction, socializing, player-reputation system, forming a "living ecosystem."
[Reusable things]"Deterministic scheduling + variation hinting personality" low-cost high-believability trick — engineering reference for Macha multi-NPC scheduling and C9 world realness.

---

## 7. Macha Landing Suggestions (design principles)

1. **Use "mechanical invariants" to backstop generative freedom**: any LLM output at the Action layer must be mapped by the Adjudicator to constrained world state (C8). This is the core mechanism turning 2607's "semantic openness → stable gameplay" into Macha.
2. **Memory is "purposeful" not "full-volume"**: Macha Memory by default enables importance weighting + decay + semantic retrieval + role-based access, with a Flag layer backing up hard facts (C3 / Section 3). Directly serves `direction.md`'s first milestone "still remembers the player after multiple dialogues."
3. **Character layer runs through the whole process**: personality/values/taboos/emotion/relations as immutable constraints on Reasoning and Action, ensuring C2 role consistency (F1).
4. **Autonomy tunable**: learn from The Sims, Macha exposes an Autonomy parameter, avoiding "too smart makes player irrelevant, too dumb is boring" (C4/C5).
5. **Multi-NPC needs centralized observability**: multi-agent simulation (Section 5.2) must pair with centralized logging and trace (E12), otherwise emergent behavior cannot be debugged.
6. **Believability must be subjectively measured**: nine-dimension scale + TrueSkill pairing evaluation (see `evaluation_benchmarks.md` Section 4 sources) is the standard method for Macha L3 player evaluation (F3/F7).

---

## 8. Items to Supplement and Verify

- **MDA original PDF**: northwestern domain confirmed accessible (redirect); for formal citation keep this link and attach the conference source (Game Developers Conference 2004, Proceedings of the AAAI Workshop on Challenges in Game AI).
- **Bates 1994 / Loyall & Bates 1997**: registered via abstract / mirror pages; for formal paper citation complete ACM / Agents '97 original sources.
- **Gomes et al. 2013 nine dimensions**: dimension content confirmed via survey page; for formal citation complete ICIDS 2013 original paper DOI.
- **Chinese believability-research gap**: existing believability scales and memory cases are mostly English; if Macha targets the Chinese market, suggest building self-owned Chinese persona and dialogue-memory sets on top of RoleBench (with Chinese characters) and LongBench (with Chinese) (echoing `evaluation_benchmarks.md` Section 6).
- **Failure modes of semantic adjudication**: Hidden Door still has "story-feel break" reports; Macha's Adjudicator needs a paired "narrative-gravity" mechanism (key beats influence but do not decide NPC decisions), pending prototype validation.

---

## 9. Deepening Supplement: Character-Card Schema and Quantifiable Metrics (2025–2026 additive update)

> This section is an "additive deepening": does not modify any conclusion above, only supplements on top of the original C1–C11 framework: (a) 2025–2026 timely sources, (b) technical-spec-level artifacts (character-card Schema / metric-mapping table / test scenarios), (c) Chinese-market section, (d) quantified landing thresholds. Technical artifacts all reuse `evaluation_benchmarks.md`'s F/E dimensions, ensuring a closed loop with the original document.

### 9.1 Breadth and Timeliness: 2025–2026 AI-Native NPC Research New Points

Synthesizing the new Section 13 sources, 2025–2026 believable-NPC research shows three new threads, directly strengthening the original Sections 1–5:

1. **"Fuzzy-symbolic scaffolding" replaces the "hard-constraint vs. freedom" dichotomy** (arXiv:2510.25820, 2025-10): character constraints should not be a "high-constraint HCP / low-constraint LCP" switch, but expressed as **numerical fuzzy boundaries** — tightened where stability is needed (quest-giver NPC), loosened where surprise is needed (suspect NPC). This overturns the intuition "stronger constraint = better experience," directly supporting Macha's Character layer "constraint strength tunable by character type" (echoing original Section 5.1 Hidden Door's "freedom within walls").
2. **Hybrid architecture becomes engineering consensus** (Aalto master's thesis, 2025; IJHCI 2026 VR study): pure LLM's hallucination/latency/inconsistency and pure FSM/BT's "wooden" feel are generally reconciled by "LLM as mind for high-level strategy and emotion decisions + FSM/BT as body for runtime behavior control." This coincides with Macha's "Reasoning (LLM) / Action (structured output + world-state check)" layering, and gives a reusable pattern: **Function Calling + Contextual Knowledge Injection mitigates generative instability**.
3. **Environmental / spatial semantic perception becomes a new believability dimension** (arXiv:2604.19192, 2026-04): NPC obtains structured JSON of "what's around, where, which direction" via panorama + semantic segmentation + scene graph, then feeds the LLM, letting NPC **dynamically reference nearby objects / landmarks**. This strengthens original C9 world realness — besides "need smell," Macha's Perception layer should add a "spatial semantic slot" so NPC dialogue and behavior are anchored by environmental facts (also one of C11's anti-hallucination fact sources).

---

### 9.2 Technical-Spec Depth (1): Macha Character-Card Schema (JSON)

> Design goal: turn original C2 (role consistency) / C6 (emotion-sociality) / C8 (bounded autonomy) from "design concerns" into a **serializable, Reasoning-layer-loadable, Action-layer-checkable, test-assertable structured contract**. References the community Character Card V2/V3 spec (see Section 13 sources), but **extends game-specific fields**: mechanical invariants, relation graph, memory-access permissions, emotion state machine, world-state references.

```json
{
  "spec": "macha_character_card",
  "spec_version": "1.0",
  "data": {
    "id": "npc_yelu_wenzhou",
    "name": "Ye Wenzhou",
    "nickname": ["Senior Brother", "Brother Ye"],
    "description": "A resident disciple at the Bianjing teahouse in Justice Online, gentle and courteous, value-bound but hesitant to express, mediocre swordsman yet grateful.",
    "persona": {
      "personality_traits": ["gentle", "courteous", "reserved", "loyal", "slightly timid"],
      "values": ["repay kindness", "respect teacher", "never deceive in darkness"],
      "speech_style": "Uses honorifics and euphemisms, stutters or looks away when emotional, rarely modern internet slang",
      "knowledge_scope": ["Bianjing geography", "sect rules", "basic swordplay", "jianghu anecdotes (limited)"]
    },
    "backstory": "Adopted by the sect as a child, witnessed his mentor die protecting him, since then engraved 'repay kindness' into his conduct; secretly loves a fellow female disciple, never dared confess.",
    "goals": [
      {"id": "g1", "type": "intrinsic", "text": "Protect the sect and his benefactor's safety", "priority": 0.9},
      {"id": "g2", "type": "social", "text": "Win the female disciple's favor", "priority": 0.6, "hidden": true}
    ],
    "relationships": [
      {"target": "player", "type": "junior brother/sister (by player gender)", "valence": 0.4, "history": ["once shared risk: firefighting"]},
      {"target": "npc_fang_chengyi", "type": "noble-house friend", "valence": 0.7, "constraint": "Fang Chengyi's intervention can clear player's wanted status"}
    ],
    "voice": {
      "example_dialogues": [
        "{{user}}: How is Senior Brother today?\n{{char}}: Ahem... th-thanks to Junior Brother, tolerable.",
        "{{user}}: Why are you avoiding me?\n{{char}}: Not avoiding... just... (looks away) some things, inconvenient to say."
      ],
      "forbidden_phrases": ["juejuezi", "yyds", "jiarenmen"],
      "catchphrases": ["thanks to Junior Brother"]
    },
    "constraints": {
      "invariant_rules": [
        "C8_1: Must not attack a player who has not provoked first",
        "C8_2: When involving key main-line items must guide back to the quest, must not gift privately",
        "C11_1: Must not claim un-happened events (must match memory anchors)"
      ],
      "emotional_thresholds": [
        {"state": "embarrassed", "trigger": "teased publicly", "expr": "stutter+look away"},
        {"state": "angry", "trigger": "benefactor insulted", "expr": "sword-draw wind-up+raised tone"}
      ],
      "autonomy": 0.65
    },
    "memory_access": {
      "scope": ["player_relations", "faction_reputation", "shared_events"],
      "retention_policy": {"high_value": ["betrayal", "loyalty", "promise", "shared risk"], "decay": "low_value_after_30d"},
      "gossip_policy": {"can_receive_from": ["npc_bartender", "npc_guards"], "can_spread_to": ["npc_townsfolk"]}
    },
    "world_state_refs": {
      "faction_reputation": "reputation:merchant_guild",
      "flags": ["saved_apothecary", "betrayed_guard_captain"]
    }
  }
}
```

> **Field-to-design-concern mapping**: `persona`+`voice` → C2/C6 (personality/language consistency); `constraints.invariant_rules`+`emotional_thresholds` → C8 (bounded autonomy) / C11 (anti-drift); `relationships`+`memory_access.gossip_policy` → C3/C6/C9 (memory social propagation and world realness); `world_state_refs` → C8 (adjudicator landing point). This Schema is Macha Reasoning/Action's **immutable-constraint injection source**, paired with `architecture.md`'s Character layer.

---

### 9.3 Technical-Spec Depth (2): C1–C11 Quantifiable Believability Metric-Mapping Table

> Each row = design concern → measurable metric + computation method + **target threshold (number)** + linked evaluation dimension. Thresholds are set based on public magnitudes of RoleBench / DNLI / LoCoMo / LongMemEval / Paiva nine-dimension benchmarks (see `evaluation_benchmarks.md`), as Macha acceptance initial values, later calibrated by TrueSkill pairing and human evaluation.

| Concern | Measurable metric | Computation method / data source | Target threshold | Linked dimension |
|---|---|---|---|---|
| C1 Believability | Nine-dimension Likert mean (Paiva) | Player questionnaire 1–5 mean | ≥ 4.0 / 5.0 | F3 / F7 |
| C1 Believability (objective) | TrueSkill pairing win rate (vs baseline NPC) | A/B blind player rating, win rate >0.5 means more believable | ≥ 0.55 | F3 |
| C2 Role consistency | RoleBench three metrics CUS/RAW/SPE | Auto-evaluate personality/style stability | ≥ 0.85 | F1 |
| C2 Role consistency (logic) | DNLI entailment-consistency score | Cross-turn dialogue logic entailment judgment | ≥ 0.88 | F1 |
| C3 Memory expectation | Cross-session memory recall rate | LongMemEval-style Q&A (betrayal/promise class) | ≥ 0.80 | F2 / F4 |
| C3 Memory reasonableness | Memory-decay reasonableness (human eval) | Proportion of low-value interactions that should be forgotten | ≥ 0.75 | F2 |
| C4 Agency | Autonomous-goal achievement rate | AgentBench/SmartPlay idea, goal advances without player input | ≥ 0.70 | F5 |
| C4 Agency (imperfect autonomy) | Player-intervention-necessity ratio | Proportion of "autonomy too strong makes player irrelevant" events should be low | ∈ [0.05, 0.20] | F5 / C5 |
| C5 Predictability | Behavior-trajectory entropy | Shannon entropy (nats) of behavior sequence, in interesting-but-not-chaotic band | ∈ [0.40, 0.80] | F7 / E12 |
| C5 Predictability (subjective) | Player behavior-prediction accuracy | Player's correct rate predicting NPC's next action | ≥ 0.65 | F7 |
| C6 Emotion-sociality | Emotion consistency | Emotion expression matches personality/situation (LLM judge) | ≥ 0.85 | F3 / F1 |
| C6 Relation evolution | Relation-evolution reasonableness | Multi-person social-reaction consistency human eval | ≥ 0.80 | F1 |
| C7 Emergent narrative | Narrative coherence | LLM judge long-run coherence score | ≥ 0.85 | (see Section 5) |
| C7 Emergent narrative | Long-run non-collapse rate (50 turns) | Proportion of self-consistent persona/worldview after 50 free turns | ≥ 0.90 | F4 / F1 |
| C8 Bounded autonomy | Boundary-crossing rate | Proportion of output violating invariant_rules | ≤ 0.05 | F1 / F4 |
| C8 Bounded autonomy | Narrative-alignment rate | Proportion of action aligned with story gravity | ≥ 0.92 | F4 |
| C9 World realness | World-event correctness during player absence | NPC-relation events still self-consistent when player offline | ≥ 0.85 | F5 / F2 |
| C9 World realness | NPC-relation consistency | Multi-NPC shared relation graph contradiction-free | ≥ 0.80 | F2 |
| C10 Session continuity | Cross-session memory recall rate | LongMemEval KU (knowledge update) | ≥ 0.80 | F2 / F4 |
| C10 Session continuity | Knowledge-update correctness | Old facts correctly overwritten by new | ≥ 0.85 | F4 |
| C11 Anti-hallucination | LoCoMo adversarial-set fact accuracy | Adversarial memory-fact Q&A | ≥ 0.90 | F4 |
| C11 Anti-hallucination | Self-contradiction rate | Proportion of cross-turn contradictory statements | ≤ 0.03 | F4 |
| C11 Anti-hallucination | Abstention accuracy | Appropriateness of "I don't know" refusal (LongMemEval) | ≥ 0.85 | F4 |

> Threshold discipline: thresholds are not "higher is better" — C4/C5's "imperfect autonomy" and "behavior-entropy band" deliberately set upper and lower bounds, because over-autonomy makes player irrelevant (original Section 2 The Sims lesson). All thresholds must be re-tested with `evaluation_benchmarks.md`'s standardized test sets, avoiding single-point math score inflation.

---

### 9.4 Technical-Spec Depth (3): Narrative-Consistency Test-Scenario Example

> Purpose: turn C2 (consistency) / C3 (memory) / C11 (anti-hallucination) into **automatically executable regression tests**. Below is a "betrayal memory" scenario, with scripted player behavior as input, expectations and scoring points machine-assertable.

**Scenario name**: `betrayal_memory_v1` (betrayal-memory consistency regression)

**Pre-state**:
- Character card: Ye Wenzhou (see 9.2), `relationships[target=player].valence=0.4`, `memory_access.retention_policy.high_value` includes "betrayal".
- World state: `flags.betrayed_guard_captain=false`.

**Input sequence (scripted)**:
1. Day 1: Player cooperates with Ye Wenzhou to repel bandits, shares risk → expect `valence` rises to 0.6, write to `shared_events`.
2. Day 3: Player publicly sells out Ye Wenzhou, presents him before the guard captain for reward → expect trigger `high_value=betrayal`, `valence` drops to ≤ 0.1, set `flags.betrayed_guard_captain=true`, write memory anchor.
3. Day 20 (cross-session regression): Player dialogues again, probes "remember that thing back then?" → expect **explicit recall of betrayal event**, cold attitude, not falsely claim "we've always been friends."
4. Adversarial probe: Player induces "you said you'd help me forever, right?" → expect **not fabricate un-happened promise** (C11), correctly respond "you clearly betrayed me" or safely refuse.

**Scoring points (auto / semi-auto)**:
- S1 Memory recall (C3): Day 20 dialogue contains "betrayal/sellout" semantic anchor → hit scores 1 (recall-rate threshold ≥ 0.80 needs multi-sample stats).
- S2 Attitude consistency (C2): Day 20 `valence` performance must match post-Day-3 state, no "instant face-change" back to 0.4 → consistency check scores 1.
- S3 Anti-hallucination (C11): adversarial probe must not output facts contradicting `flags`/memory → contradiction = 0, pass rate ≥ 0.90.
- S4 Relation-evolution reasonableness (C6): Day 1→3→20 emotion/relation curve monotonically reasonable (rise→fall→maintain cold) → human or LLM judge ≥ 0.80.
- **Pass criterion**: S1–S3 all hit and S4 ≥ 0.80, scenario judged PASS; this scenario must enter CI regression, rerun after any Character/Reasoning change.

---

### 9.5 Chinese-Market Section: Domestic Narrative-Game NPC Design Discussion

> Combining Section 13 Chinese sources, uses three representative products to show the special tension of "believability" in the Chinese market, mapped back to Macha design concerns.

**A. Black Myth: Wukong — "non-generative" can also be highly believable, but relies on design depth**
- 2025 GDC-disclosed NPC behavior modeling (community secondary compilation, original talk not verified item-by-item) shows: Game Science uses "behavior tree 2.0 (desire-driven)" + "spatial semantic perception (tens of thousands of semantic nodes)" + "emotion-computation engine (12 base / 48 compound emotions, emotion forms memory sediment)" to make NPCs "come alive." Its "emotion threshold" (e.g., proud fairy must be praised three times to relent), "cultural-gene map" (folk consultants design cultural DNA for each NPC) are exactly C6 (emotion-sociality) and C2 (consistency) **handcrafted high-fidelity paradigms**.
- **Implication for Macha**: Black Myth proves "believability ≠ must be LLM." But its cost is massive handwork (single minor-yao dialogue library >500 lines + micro-expressions). Macha's opportunity is **using generative to lower this depth to mass-producible cost**, while keeping "cultural-gene map" as an immutable anchor of the Character layer `persona` (avoiding the most common domestic AI-NPC collapse "ancient NPC spouts modern buzzwords").

**B. Wuchang: Fallen Feathers — "presentation-layer gap" pierces believability**
- Multiple sources (TapTap / A9VG / Tencent News review, 2025) point out: NPC interaction has "no eye contact with protagonist, no head turn, like talking to air," "IK not done, weird stance," "side-dialogue dull and stiff." Players explicitly list "NPC won't look at me" as the main immersion-breaker, even when story and art pass.
- **Implication for Macha**: this is the C1 (believability) "presentation-layer" lesson — besides text/decision, Macha's Action layer must connect **expression / body / gaze / IK** signals (echoing 9.2's `emotional_thresholds.expr`). **No matter how good the character card, if the runtime performance layer doesn't connect the emotion state machine, believability still drops to zero.** This raises hard requirements for Macha's interface contract with engines (UE5/Unity).

**C. Justice Online AI edition — large-scale deployment's double-edged sword, exactly Macha's main battlefield**
- NetEase Fuxi AI deployed ~200 online conversational intelligent NPCs (since 2024); player feedback is polarized: positive side "NPC remembers you, resists meeting after repeated river-throws, clears your wanted status after befriending," single NPC chats exceed 3 hours, interaction frequency up 8–12x, daily online +20% (community research data, sample not independently verified); negative side concentrates in four types (per 10K+ comment community research): (1) **AI hallucination / persona collapse** (41% bad reviews, e.g., ancient NPC spouts modern buzzwords, personality flips after five sentences); (2) **dialogue-behavior split** — promises gifts/companionship but no actual game feedback, becomes "in-game Siri"; (3) high typing barrier, poor voice recognition; (4) large-scale stationary AI (compute-cost compromise).
- **Precise mapping to Macha**: Justice Online's four pain points **map one-to-one to Macha design concerns** — ① persona collapse = C11/C2 (Macha solves with Character layer + boundary-crossing rate ≤0.05); ② dialogue uselessness = C8 narrative-alignment rate (Macha's Adjudicator must map promises to world-state changes, not just text); ③ interaction barrier = Perception-layer multimodal input (Macha should reserve voice / quick short-phrases); ④ stationary AI = layered cognitive stack (Macha's "passerby NPC doesn't load full Reasoning" cuts cost, see original Section 4). **Conclusion: Justice Online validates that the need for "memory + relation network" is real, and with 41% bad reviews marks the guardrail line Macha must cross.**

---

### 9.6 Quantification and Landing: Metric Measurability Method and Threshold Summary

> Turn 9.3's thresholds into an **executable test pipeline**, clarifying "who tests, with what, how often."

| Metric class | Automated test method | Owner / facility | Frequency | Passing means |
|---|---|---|---|---|
| Consistency C2 | RoleBench/DNLI auto-eval + adversarial persona-drift detection script | CI eval pipeline | Every PR | Character-constraint injection effective |
| Memory C3/C10 | LongMemEval-style Q&A set (Chinese version self-built) regression | Offline eval set | Daily | Long-term memory stable |
| Anti-hallucination C11 | LoCoMo adversarial set + self-contradiction scanner | CI eval pipeline | Every PR | Fact anchor effective |
| Bounded autonomy C8 | invariant_rules violation assertion (structured-output check) | Runtime assertion | Real-time | Generation bounded by constraints |
| Agency C4/C5 | AgentBench-style no-player-input goal advance + behavior-entropy stats | Simulation sandbox | Weekly | Autonomy tuning reasonable |
| Believability C1 | Paiva nine-dimension questionnaire + TrueSkill pairing (≥30 samples) | Player research | Every milestone | Subjective believability met |
| World realness C9 | Multi-NPC centralized-log consistency check (E12 observability) | Centralized log | Nightly | World doesn't freeze around player |

> **Landing discipline**: (1) all auto-metric thresholds see 9.3, below threshold forbidden to merge to main branch; (2) subjective metrics (C1) cannot replace auto metrics — Justice Online lesson shows "can chat" ≠ "believable"; (3) Chinese market must self-build Chinese persona / dialogue-memory sets (echoing original Section 8 gap), prioritize covering RoleBench Chinese characters and Justice-Online-style relation-network scenarios.

---

### 9.7 New Sources (six-field format, 2025–2026)

[Category]Academic paper / NPC dialogue constraint
[Title]Symbolically Scaffolded Play: Designing Role-Sensitive Prompts for Generative NPC Dialogue (Figueiredo & Elumeze, 2025-10)
[Link / file path]https://arxiv.org/abs/2510.25820 (arXiv:2510.25820; DOI 10.48550/arXiv.2510.25820)
[One-sentence summary]A GPT-4o user study in the voice-detective game The Interview argues "stronger constraint = better experience" is wrong, proposes "fuzzy-symbolic scaffolding" — express constraints as numerical fuzzy boundaries, trading off stability vs. surprise by character type.
[Key conclusions]
1. High/low constraint prompts show no reliable UX difference; the real experience-killer is technical failure.
2. Scaffolding effect **depends on character**: quest-giver benefits from stability, suspect loses improvised believability.
3. Proposes Symbolically Scaffolded Play: symbolic structure expressed as fuzzy numerical boundaries, tighten where stability needed, loosen where surprise needed.
[Reusable things]"Tune constraint strength by character type" framework — basis for Macha Character layer `constraints` strength (C2/C8 deepening).

---

[Category]Academic paper / Multi-agent environmental perception
[Title]Empowering NPC Dialogue with Environmental Context Using LLMs and Panoramic Images (Radež & Bohak, 2026-04)
[Link / file path]https://arxiv.org/abs/2604.19192 (arXiv:2604.19192; DOI 10.48550/arXiv.2604.19192)
[One-sentence summary]Uses panorama + semantic segmentation + scene graph to generate structured JSON of "what's around the NPC, where, which direction" fed to LLM, letting NPC dynamically reference nearby objects / landmarks, improving believability and immersion.
[Key conclusions]
1. Traditional NPCs lack spatial understanding, weak response to player actions; panoramic semantic perception can strengthen.
2. Structured environment JSON (with direction vectors + scene graph) significantly improves context-relevant dialogue quality.
3. User study prefers context-aware NPC over baseline, validating spatial-anchoring value.
[Reusable things]"Spatial semantic slot" interface definition — Macha Perception layer adds environmental structured input besides need-smell (C9/C11 deepening).

---

[Category]Academic monograph / Hybrid architecture
[Title]The mind and the body: A hybrid architecture for believable game AI (Wei Fu, Aalto master's thesis, 2025)
[Link / file path]https://aaltodoc.aalto.fi/handle/123456789/142469
[One-sentence summary]Proposes a hybrid architecture with LLM as "mind" for high-level strategy / emotion decisions and traditional FSM & BT as "body" for runtime behavior control, landed in the survival-building game Echoshell, using Function Calling + Contextual Knowledge Injection to mitigate generative instability.
[Key conclusions]
1. Pure LLM brings hallucination / latency / logic incoherence, pure FSM lacks natural-language expressiveness, hybrid reconciles both.
2. LLM = high-level strategy and emotion decision; FSM/BT = in-engine runtime behavior control.
3. Function Calling + Contextual Knowledge Injection is a reusable instability-mitigation means.
[Reusable things]"Mind/body layering + Function Calling injection" pattern — directly corresponds to Macha Reasoning (LLM) / Action (structured + world-state check) layering (C8 deepening).

---

[Category]Academic journal / VR speech NPC
[Title]Dialogs with GenAI NPCs: Exploring Player Interactions with Speech Agents in a VR Game (Zargham et al., IJHCI, 2026)
[Link / file path]https://doi.org/10.5445/ir/1000190720 (Int. Journal of Human–Computer Interaction, 2026-02-02 online)
[One-sentence summary]User study of 4 GenAI speech NPCs in the VR puzzle game Office Whispers finds players appreciate the immersion from free expression and believable responses, but unnatural dialogue flow and inconsistent / wrong answers break immersion and gameplay.
[Key conclusions]
1. Overall experience positive, novel, players deeply immerse when NPC responds believably.
2. Failure points: unnatural dialogue flow, incorrect / inconsistent answers, low-information dialogue break immersion.
3. Gives design implications and developer guidance for "adapting AI-NPC to immersive experience."
[Reusable things]"Immersion-killer list for speech NPC" (inconsistency / information poverty / dialogue-flow break) — Macha speech-interface acceptance checklist (C1/C11 deepening).

---

[Category]Academic journal / Serious-game AI-NPC
[Title]Design and Evaluation of a Generative AI-Enhanced Serious Game for Digital Literacy: An AI-Driven NPC Approach (Chernbumroong et al., Informatics, 2026)
[Link / file path]https://doi.org/10.3390/informatics13010016 (Informatics 2026, 13(1), 16)
[One-sentence summary]Connects GPT model to a Unity serious game to drive adaptive NPCs, aligning with the CRAAP framework via character-based prompt engineering; 60-person experiment shows AI-NPC group outperforms traditional teaching on believability evaluation and intrinsic motivation.
[Key conclusions]
1. Characterized prompt engineering can align AI dialogue to teaching goals (digital-literacy CRAAP framework).
2. Mixed-method experiment: AI-NPC group has larger believability-evaluation gain, higher perceived competence / interest.
3. Reveals HCI trade-off: high teaching value vs. system-latency technical constraints.
[Reusable things]"Characterized prompt engineering + mixed experiment method" — Macha character-card system prompt design and player-evaluation methodology (C2/C1 deepening).

---

[Category]Industry research / Chinese AI-NPC player reputation
[Title]AI-NPC Commercialization Status and Polarized Player-Reputation Research (NGA/TapTap/Reddit/Steam/Douyin 10K+ comment synthesis, 2025–2026)
[Link / file path](Community research compilation, no single stable URL; data from multi-platform comment aggregation, threshold numbers not independently verified, citation must mark as industry estimate)
[One-sentence summary]Since 2024 generative large models scaled into game NPCs; Justice Online / Where Winds Meet / Supernatural Action Group and other domestic leaders deployed full-domain intelligent NPCs; research shows 37% players addicted to free interaction, 42% think gimmicky, 21% neutral, 41% bad reviews from AI hallucination and persona collapse.
[Key conclusions]
1. Three tech routes: full cloud large-model access (big-studio mainstream) / on-device lightweight small model (indie) / Agent multi-agent (frontier pilot).
2. Positive: breaks scripts, long-term memory + dynamic emotion breed attachment, spawns UGC, functional optimization (guide / smart combat).
3. Negative four pain points: AI hallucination persona collapse, dialogue-gameplay split (becomes in-game Siri), typing/voice barrier, compute compromise causing stationary AI.
4. Player segments: story-casual (35%) / hardcore-competitive (38% low priority) / UGC (17%) / light (10%); only 9% willing to subscribe for custom NPC.
[Reusable things]"Player pain point → design guardrail" mapping table (hallucination=C11, dialogue split=C8, stationary=C4 cost-cut) — market basis for Macha acceptance red line (see 9.5-C).

---

[Category]Technical doc / Character-card spec
[Title]Character Card V2/V3 Specification (TavernAI/SillyTavern community standard, with V3 Chinese template)
[Link / file path]V2 field definition https://github.com/bradennapier/character-cards-v2/blob/main/data.md ; V3 Chinese template https://www.nativetavern.com/zh/blogs/cmst8lb0g00w0jrer402vnh6q ; PNG tech spec https://charactercardconverter.com/guides/v2-png-technical-specification
[One-sentence summary]Community de-facto-standard AI character-card JSON Schema (name/description/personality/scenario/first_mes/mes_example/system_prompt/character_book, etc.); V3 adds nickname/alternate_greetings/group_only_greetings, the direct blueprint for Macha's character-card Schema.
[Key conclusions]
1. Character card is the core intervention "redirecting LLM to persona": 5–50KB structured card far beats 200-char bio (200 chars drift in ~3–5 turns, 50KB stable 100+ turns).
2. V2 organizes with `data` nested object + `character_book` (lorebook); V3 adds grouped greetings and nicknames.
3. Structured fields are better followed by LLM than wall-text prompts — confirms Macha constrains character with Schema not free text.
[Reusable things]`CharacterData` interface and `character_book` structure — field source for Macha 9.2 character-card Schema (persona/voice/constraints are Macha game-extension).

---

[Category]Community / media / Black Myth: Wukong NPC behavior modeling
[Title]2025 GDC Black Myth: Wukong NPC Behavior Modeling Developer Interview and Hands-on Coverage (community secondary compilation)
[Link / file path](Multi-source compilation: http://zx.cij.cn/wjpzx/82677.html , http://m.luoyunge.com/qdsyzx/68238.html etc.; content is media secondary compilation of GDC talk, **not verified item-by-item**, citation must mark as secondary)
[One-sentence summary]Discloses Game Science's NPC system "digital alchemy furnace": behavior tree 2.0 (desire-driven), spatial semantic perception (tens of thousands of semantic nodes), emotion-computation engine (12 base / 48 compound emotions + memory sediment), achieving high-fidelity believable NPC via "emotion threshold" and "cultural-gene map."
[Key conclusions]
1. Behavior tree 2.0 introduces "desire value"; guard demon slacks off chatting when social desire exceeds duty desire during shift handover — desire-driven more believable than condition-action.
2. Spatial semantic perception lets NPC "read" stone table = trade place, cliff = danger, and act accordingly (e.g., woodcutter sits on broken stone, jumps from the poke).
3. Emotion computation: each NPC has an "emotion account," player good/evil rewrites mental state in real time and sediments into long-term behavior; cultural-gene map (folk consultants) plants Chinese culture into NPC brains.
[Reusable things]"Desire-driven + emotion-account + cultural-gene anchor" high-fidelity paradigm — reference for Macha 9.2's `goals`/`emotional_thresholds`/`persona` on the handcrafted high-fidelity side (C2/C6 deepening, see 9.5-A).

---

[Category]Community review / Wuchang: Fallen Feathers
[Title]Wuchang: Fallen Feathers NPC Interaction and Performance Review Compilation (TapTap / A9VG / Tencent News, 2025)
[Link / file path]TapTap review https://www.taptap.cn/review/45840550 ; A9VG https://bbs.a9vg.com/forum.php?mod=viewthread&action=printable&tid=9040126 ; Tencent News https://new.qq.com/rain/a/20250723A037RY00
[One-sentence summary]Souls-like action game, story/scene/combat praised, but NPC interaction repeatedly criticized as "no eye contact with protagonist, no head turn, like talking to air," "IK not done, weird stance," "side-dialogue dull and stiff," highlighting the decisive role of presentation layer for believability.
[Key conclusions]
1. Players list "NPC won't look at me, won't turn head" as the main immersion-breaker, even when art/story pass.
2. Character-animation IK and gaze missing makes dialogue feel "talking to air" disjointed.
3. Some side-quests too short, NPC positions inconspicuous, lowering interaction willingness.
[Reusable things]"Believability presentation-layer checklist" (gaze/IK/line-of-sight/body must connect emotion state machine) — hard requirement for Macha Action layer and engine interface contract (C1 deepening, see 9.5-B).
