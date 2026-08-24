# 04 — BDI + Modern Agent-Architecture Structure

Status: STORED (Batch 2 · Domain 4)
Serves paper claim: §6 R↔S coexistence — where a first-class relational state (R) fits or
collides with classic cognitive state (S); how R becomes a control variable rather than
more generated text.

> Source discipline: claims carry retrieved sources. `[CONTEXT]` = background, not citation
> evidence. `[UNRESOLVED]` = question not fully answered. Secondary/aggregator sources are
> flagged `[RE-VERIFY]` and must be replaced by primary sources before citation.

## What must be known (hard questions)
1. In SOAR / ACT-R / BDI: how are state persistence + goal competition actually implemented?
2. Where does a relational state fit as a first-class citizen vs. collide with the rational-goal machinery?
3. Modern generative-agent / MemGPT-family memory stacks: their real limits — how retrieval *fakes* relationship, where the faking breaks.
4. Drama manager / narrative planning interface: how relational state becomes the control variable.

## Findings

### 1. State persistence + goal competition in classical architectures
- **BDI (Belief-Desire-Intention):** beliefs = info about environment/others/self; desires/goals = states of affairs to achieve; intentions = commitments to goals. A BDI program = initial beliefs/goals + plan-rules (when a plan can achieve a goal or respond to an event).
  [<de Silva, Meneguzzi & Logan 2020, IJCAI survey>](https://www.ijcai.org/proceedings/2020/0684.pdf)
- **Philosophical source:** Bratman (1987) on practical reasoning — intention as commitment. [<Bratman 1987>](https://onlinelibrary.wiley.com/doi/pdf/10.1111/j.1475-4975.1987.tb00539.x)
- **Logic:** Rao & Georgeff formalized BDI on branching-time semantics. [<Wooldridge overview>](http://www.cs.ox.ac.uk/people/michael.wooldridge/pubs/ker95/subsubsectionstar3_2_6_3.html) — the original 1991/1993 papers are the primary citations; this is a stable secondary index. [RE-VERIFY: replace with Rao & Georgeff 1991 primary PDF]
- **Revision postulates:** Grant, Kraus, Perlis & Wooldridge (2010) — postulates for revising beliefs/desires/intentions (adding/removing, updating costs/values).
  [<Grant et al. 2010, Synthese>](http://www.cs.ox.ac.uk/people/michael.wooldridge/pubs/synthese2010.pdf)
- **Commitment strategies:** blind / single-minded / open-minded / reactive commitment modes; intention reconsideration (when to drop/adopt intentions).
  [<Schut & Wooldridge, Intention Reconsideration>](https://www.cs.vu.nl/~schut/pubs/Schut/2002.pdf)
- **SOAR:** working memory + impasse resolution + chunking. When knowledge is insufficient to choose/apply an operator, SOAR reaches an impasse and creates a substate; reasoning in the substate is compiled into chunks that later fire directly (deliberative → procedural).
  [<Laird 2022, arXiv:2205.03854>](https://arxiv.org/pdf/2205.03854) [<Soar Manual — procedural learning>](https://soar.eecs.umich.edu/soar_manual/04_ProceduralKnowledgeLearning/) [<Chunking in Soar>](https://files.eric.ed.gov/fulltext/ED275301.pdf)
- **ACT-R:** declarative memory (facts + active goals) vs procedural memory (productions); among matching productions, select highest utility U = P·G − C + ε (probability × goal value − cost + noise).
  [<ACT-R modeling paradigms>](http://act-r.psy.cmu.edu/wordpress/wp-content/uploads/2012/12/570SDOC4697.pdf) [<National Academies — modeling human behavior>](https://www.nationalacademies.org/read/6173/chapter/5) — the utility formula as retrieved from a secondary encyclopedia page. [RE-VERIFY: confirm formula against Anderson & Lebiere primary source]

### 2. Where relational state (R) fits or collides
- **EBDI (Jiang, Vidal & Huhns 2007):** extends BDI with primary/secondary emotions; merges emotion theory with reasoning while keeping practical reasoning separate from the emotion mechanism.
  [<EBDI 2007>](https://jmvidal.cse.sc.edu/papers/jiang07a.pdf)
- **Probabilistic emotional BDI (Gluz & Jaques):** OCC-based emotion intensity from desirability; event-generated emotions with consequences for self.
  [<Gluz & Jaques>](https://pdfs.semanticscholar.org/dfc4/fba6ea8a35f7ca7366296d5d1788b7532c32.pdf)
- **GenIA³ (ACM):** BDI + personality/emotion/mood layered on top; actions still decided by goals, affective traits layered on.
  [<GenIA³>](https://dl.acm.org/doi/pdf/10.1145/3001584)
- **GAMA/BEN simple BDI — the closest formal precedent:** social relation as a formal structure R_i,j(L, D, S, F, T), where L ∈ [−1, 1] = degree of liking (−1 hated, 1 liked); emotions OCC-based and explicitly include the agent causing them: Em_i(P, Ag, I, De).
  [<GAMA wiki — Using BEN simple BDI>](https://github.com/gama-platform/gama/wiki/Using-BEN-simple-bdi)
- **ARIS (Datta et al. 2026):** agentic social-robot framework with a Social World Model as a knowledge graph — maps/updates relationships between users, supports re-identification across encounters; N=23 robot-mediated dyadic study: significantly higher perceived intelligence/animacy/anthropomorphism/likeability vs LLM baseline. [RE-VERIFY: arXiv preprint 2605.00943]
  [<ARIS 2026>](https://arxiv.org/html/2605.00943v1)
- **Sentipolis (Fu et al. 2026):** identifies *long-horizon emotional continuity* as a missing design target; names "emotional amnesia" as a concrete failure mode of missing emotion carryover; continuous PAD representation + dual-speed emotion dynamics + emotion-memory coupling. [RE-VERIFY: lab page preprint]
  [<Sentipolis 2026>](https://lab-msp.com/MSP/publications/Fu_2026_2.pdf)
  - **Consume (key):** R as a stored property exists (GAMA/BEN, ARIS), but NO retrieved system lets R drive intention reconsideration / goal competition / long-horizon conflict. That is Macha's gap.

### 3. Modern generative-agent memory stacks — real limits
- **Generative Agents (Park et al. 2023):** memory stream (natural-language experiences) + retrieval (relevance/recency/importance scoring) + reflection (synthesize higher-level inferences). Agents "form relationships" as *observed emergent behavior* — no dedicated relationship data structure or commitment mechanism.
  [<Park et al. 2023, arXiv:2304.03442>](https://arxiv.org/pdf/2304.03442.pdf) [<Stanford AI Index summary>](https://stanford.io/48OBs4v) [<memoryforagents summary>](https://www.memoryforagents.com/research/generative-agents) — the last two are secondary summaries. [RE-VERIFY: cite primary paper]
  - Documented limits (from secondary summary): compute-intensive, small-scale, untested long-term coherence, unbounded memory growth. [RE-VERIFY]
- **MemGPT (Packer et al. 2023):** OS-style virtual memory — hot data in context window, rest in slower storage; LLM manages its own paging (queue eviction, memory-pressure warnings, tools to store/retrieve). Creates the *illusion* of unbounded context.
  [<MemGPT, arXiv:2310.08560>](https://arxiv.org/pdf/2310.08560)
- **MemoryOS (Kang et al. 2025):** short/mid/long-term memory tiers; FIFO dialogue-chain updates + segmented page organization; reported +49.11% F1 / +46.18% BLEU-1 over baselines. No social-relationship modeling in design.
  [<MemoryOS, arXiv:2506.06326>](https://arxiv.org/pdf/2506.06326.pdf)
- **Retrieval ≠ remembering:** agents with working-memory infrastructure can progressively stop using it ("fading") — a behavioral failure mode of retrieval-based memory across context boundaries. [CONTEXT — GitHub protocol doc, not peer-reviewed]
  [<Dream Weaver Protocol>](https://github.com/wipcomputer/dream-weaver-protocol/blob/main/DREAM-WEAVER-PROTOCOL.md)
- **Emotion-memory coupling is open:** Sentipolis argues treating emotion as a transient cue → emotional amnesia → weak long-horizon continuity. Sustained social/emotional state stays fragile unless integrated into memory AND decision-making.
  [<Sentipolis 2026>](https://lab-msp.com/MSP/publications/Fu_2026_2.pdf)
  - **Consume (key):** retrieval/reflection can fake conversational continuity but cannot fake *commitment* — no expectation state, no reason to act against short-term convenience because of prior trust. Macha's R must be a persistent structure that affects planning, not a retrieval artifact.

### 4. Drama manager / narrative planning interface
- **Façade (Mateas & Stern 2005):** drama manager coordinates story beats in real time; beat = smallest architectural unit of dramatic value change (preconditions, values changed, success/failure conditions, joint behaviors).
  [<Mateas & Stern 2005, AIIDE>](https://eis.ucsc.edu/papers/MateasSternAIIDE05.pdf) [<Mateas 2004, preliminary poetics>](https://users.soe.ucsc.edu/~michaelm/publications/mateas-first-person-2004.pdf)
- **Drama manager as control:** observes story state + character state, selects beats to advance a planned tension arc. [<Game Developer — Story of Facade>](https://www.gamasutra.com/design/the-story-of-facade-the-ai-powered-interactive-drama) — secondary case study. [RE-VERIFY]
- **Narrative planning + believability:** Riedl & Young (2006) — drama manager as disembodied agent managing the world for narrative experience; combining autonomous character agents with drama management.
  [<Riedl & Young 2006>](https://faculty.cc.gatech.edu/~riedl/pubs/tidse06b.pdf)
- **Distributed Drama Management (Wheatlands et al. 2012):** inverse of Fabulist — start from believable actions, select the one best serving dramatic structure.
  [<Wheatlands et al. 2012>](https://www.macs.hw.ac.uk/~ruth/Papers/narrative/WheallansEtAl2012.pdf)
- **Emotion-inspired narrative planning (Fisher, Siler & Ware 2022):** VR police de-escalation training; narrative planner generates a story graph, prunes less-believable NPC actions; emotional planning (fear of bad outcomes / hope for good ones); experience management delays commitment to hidden settings.
  [<Fisher et al. 2022>](https://cs.uky.edu/~sgware/reading/papers/fisher2022deescalation.pdf)
- **Data-driven personalized drama management (AAAI):** models players, manipulates story space to maximize probability of design-aligned choices.
  [<Data-driven personalized DM>](https://cdn.aaai.org/ojs/12665/12665-52-16182-1-2-20201228.pdf)
  - **Consume (key):** drama managers control via story beats / tension / believability / emotional planning — NONE uses a first-class relational state (seen/remembered/independent-will) as the control variable. Macha's R-as-drama-control-variable is unoccupied.

## Formal/operational takeaways for Macha
1. **R must be first-class, not appended.** BDI shows the pattern: a decision-relevant state must be available to belief revision, desire selection, and intention reconsideration — not stored as passive memory.
2. **R needs commitment/expectation, not just retrieval.** Generative-agent memory fakes continuity; Macha's R must include expectations and commitments that make the NPC act against short-term convenience.
3. **R as a formal structure has precedent (GAMA/BEN R_i,j) but no decision-cycle integration.** Macha can be the first to make R drive goal competition.
4. **ACT-R's utility competition is a concrete mechanism:** relational value can enter plan competition (U = P·G − C + ε), making NPC behavior sensitive to being seen/remembered/dismissed.
5. **R must be visible to the drama manager:** relational state as input to beat selection / plan pruning — narrative tension depends on whether the player was acknowledged and remembered.
6. **Independence must be operationalized:** NPCs need goals that can diverge from the player's, intentions that persist, and relational states that change on inconsistency.

## Pitfalls / avoid
- Don't confuse memory retrieval with relationship state (a system can remember facts without remembering how they changed the relation).
- Don't treat R as a static attribute (GAMA/BEN liking/trust values) — R must evolve through commitments, expectations, failures.
- Don't let retrieval-faking replace commitment.
- Don't embed R only as a BDI *belief* — it must constrain/motivate intention reconsideration.
- Don't treat emotion as a transient cue (Sentipolis's emotional amnesia).
- Don't cite secondary/aggregator pages (lobehub, cstopics, memoryforagents, gamasutra) as primary — replace with primary sources.

## Bibliography
See inline links. Primary anchors: de Silva et al. 2020 (IJCAI); Grant et al. 2010 (Synthese); Laird 2022 (arXiv); Park et al. 2023 (arXiv); Packer et al. 2023 (arXiv); Mateas & Stern 2005 (AIIDE); Riedl & Young 2006; GAMA/BEN wiki. Preprints flagged [RE-VERIFY]: ARIS 2026, Sentipolis 2026, MemoryOS 2025.

## Open questions
1. [UNRESOLVED] Formal definition of R as a first-class BDI component that reweights goal/intention selection — no retrieved source defines it.
2. [UNRESOLVED] Commitment-based relationship persistence — no explicit commitment/expectation mechanism in generative-agent memory.
3. [UNRESOLVED] Drama-manager control variable for social state — how R drives beat selection is unspecified in the literature.
4. [UNRESOLVED] NPC independent will under social friction — relationship-driven divergence of NPC goals from player goals.
5. [UNRESOLVED] General model of how R affects long-horizon social conflict resolution.
