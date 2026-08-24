# 05 — Game Studies / Interactive-Narrative Theory

Status: STORED (Batch 2 · Domain 5)
Serves paper claim: §7 move from "case collection" to transferable formal properties — the
relational gap must be stated in game-theoretic terms a reviewer cannot dismiss.

> Source discipline: claims carry retrieved sources. `[CONTEXT]` = background, not citation
> evidence. `[UNRESOLVED]` = question not fully answered. Secondary/aggregator sources are
> flagged `[RE-VERIFY]` and must be replaced by primary sources before citation.

## What must be known (hard questions)
1. Juul's Half-Real thesis — how the rule layer and fictional layer interact.
2. Agency redefinition (Wardrip-Fruin / Mateas) — freedom of action vs freedom of interpretation.
3. Intentional stance applied to game characters — what consistency sustains belief.
4. Interpretation as the computational bottleneck — why Façade failed (NOT simply NLU).
5. Players actively maintaining the relationship illusion (projection + repair); when the system must cooperate vs refuse.

## Findings

### 1. Half-Real (Juul)
- **Juul (2005):** playing a video game is "to interact with real rules while imagining a fictional world." Games are simultaneously rule-based and fictional; rules are real constraints, the world is imagined; the two layers interact (fiction cues understanding of rules; rules cue imagining the world).
  [<Half-Real review, Games and Culture 2008>](https://hal.science/hal-00571578/file/PEER_stage2_10.1177%252F1367549408091320.pdf) [<Juul 2005 notes>](https://darcynorman.net/notes/2020/juul-half-real/) — the latter is a secondary reading. [RE-VERIFY: cite the MIT Press monograph]
- **Classic game model:** three levels (game as formal system; player and game; game and rest of world); rules, variable/quantifiable outcomes, value on outcomes, player effort, player attachment, negotiable consequences. Rules prohibit some actions but add meaning to allowed ones.
  [<Juul 2005 notes>](https://darcynorman.net/notes/2020/juul-half-real/) [RE-VERIFY]
- **Juul (2019), "Virtual Reality: Fictional all the Way Down":** virtual objects always selectively implement their source material and retain fictional aspects; even the most detailed virtual object is a human process of selection/interpretation.
  [<Juul 2019>](https://www.jesperjuul.net/text/fictionalalltheway/)
- **Chess-computer example (Björk & Juul 2012):** when a machine's strategy is complex enough, treating it as having beliefs/desires/goals becomes the most practical way to predict it — a direct bridge to the intentional stance in games.
  [<Björk & Juul 2012, zero-player games>](https://www.gamephilosophy.org/wp-content/uploads/confmanuscripts/pcg2012/Bjor%20Juul%202012%20-Zero-player-games-Exploring-the-distinction-between-Games-as-Artifacts-and-Games-as-Activities.pdf)
  - **Consume:** half-real legitimizes relational behavior as *rule-governed* inside an imagined world — Macha's R can be a rule-layer object that sustains the fictional layer.

### 2. Agency — Wardrip-Fruin and the field
- **Wardrip-Fruin, *Expressive Processing* (2009):** digital media express through computational processes and operational logics, not just output; analysis moves beyond output-focused interpretation to internal processes.
  [<Expressive Processing 2009>](https://rhetoricgrimes.wordpress.com/wp-content/uploads/2018/01/wardrip-fruin-expressive-procedures.pdf) — hosted PDF. [RE-VERIFY: confirm against MIT Press edition]
- **Mateas (2001), preliminary poetics:** agency as a balance between formal and material affordances, integrating Aristotle's poetics and Murray's agency discussion.
  [<Mateas 2001>](https://www.semanticscholar.org/paper/Agency-Reconsidered%2C-Again-Dow-Sali/445a63d103d0ca0ba8b7244852fdbdd45c9166e9) — Semantic Scholar record. [RE-VERIFY: cite primary PDF]
- **Playing with Words (FDG 2010, Sali/Wardrip-Fruin/Dow/Mateas et al.):** three dialogue interfaces (sentence selection, abstract response menu, natural-language input) over the same story content produce significantly different gameplay experience — sentence selection maximized story involvement; abstract menu maximized reasoning about game structures.
  [<FDG 2010 paper>](http://www.cs.cmu.edu/~spdow/files/Agency-FDG10.pdf)
  - **Consume (key):** agency is *interpretive*, not just mechanical — the dialogue interface shapes whether players read an NPC as a constrained system or as a character in a dramatic situation. Relational feeling depends on the NPC's responses being experienced as meaningful dramatic interaction.

### 3. Intentional stance in games
- **Dennett's intentional stance:** treat the entity as a rational agent with beliefs/desires/goals to interpret and predict behavior; attribute beliefs given its place and purpose, attribute desires, predict rational action. Used for complex systems such as AI opponents and game characters.
  [<Intentional stance discussion>](http://www.sci.brooklyn.cuny.edu/~schopra/ChopraWhiteChapter1.pdf) — book chapter PDF. [RE-VERIFY: cite Dennett 1987 primary]
- **The stance is not permanent:** it can be adopted, sustained, or abandoned depending on how reliably the system supports the interpretation. When an NPC breaks from established history/personality, the player may stop treating it as intentional.
  [<Intentional stance discussion>](http://www.sci.brooklyn.cuny.edu/~schopra/ChopraWhiteChapter1.pdf) [RE-VERIFY]
- **Believable NPC design patterns** treat characters as goal-directed, responsive entities. [<Gameplay design patterns for believable NPCs>](https://petrilankoski.com/2007/09/03/gameplay-design-patterns-for-believable-non-player-characters/) — blog. [CONTEXT — inspiration only]
  - **Consume (key):** NPC relational quality = *sustained intentional-state behavior*. Once the player adopts the stance, the NPC must maintain consistent beliefs/desires/remembered interactions or the stance collapses. This converts Dennett into a testable property: consistency + memory + responsiveness.

### 4. Interpretation as the computational bottleneck — why Façade failed
- **Façade (Mateas & Stern):** AI-based interactive drama; deconstructs narrative into story/behavior pieces, reconstructs a real-time dramatic performance; joint dialog behaviors + story beats + drama manager sequencing thousands of authored behaviors.
  [<Mateas & Stern 2005, AIIDE>](https://users.soe.ucsc.edu/~michaelm/publications/mateas-aiide2005.pdf) [<Façade GDC 2003 record>](https://www.semanticscholar.org/paper/Fac%CC%A7ade%3A-An-Experiment-in-Building-a-Fully-Realized-Mateas-Stern/a5d2af2a518e2c74761bdc3d976657ac48c9d2f8) — Semantic Scholar record. [RE-VERIFY: cite primary]
- **The supported lesson is NOT "NLU failed":** the identified challenge was *communicating the state of the social games to the player* — in Façade the "game" happens inside the characters' heads, so social state was hard to make legible. The evaluation (Knickmeyer & Mateas, CHI 2005) focused on interaction failure and the drama architecture's responsiveness.
  [<AIIDE 2005>](https://users.soe.ucsc.edu/~michaelm/publications/mateas-aiide2005.pdf) [<Knickmeyer & Mateas CHI 2005>](https://eis.ucsc.edu/papers/KnickmeyerMateasCHI2005.pdf)
- **The claim "Façade failed because of NLU" is NOT supported by retrieved evidence.** Evidence instead points to dramatic structure, social-state communication, authoring complexity, and interaction failure. What IS supported: dramatic meaning (not just surface dialogue) was hard to compute — hence the drama manager, story beats, authoring idioms.
  - **Consume (key):** this is a *vindication* of Macha's framing: the bottleneck was relational/dramatic meaning, not parsing. But do NOT overclaim — the evidence shows dramatic-beat communication and interaction failure were central; NLU may have contributed.
- **[UNRESOLVED]** No retrieved post-mortem of Beatrice/Trip character consistency, replay/tuning of "lowercase-c" content, or Andrew Stern retrospectives.

### 5. Players actively maintain the relationship illusion
- **Reparative play (Grinblat, Manning & Kreminski 2021):** reads emergent narrative through Sedgwick's paranoid/reparative framing. Reparative reading is "additive and accretive," "wants to assemble and confer plenitude on an object"; narrative sandbox systems produce deliberately incomplete artifacts that invite repair — "they invite repair by arriving in disrepair."
  [<Emergent Narrative and Reparative Play>](https://www.researchgate.net/publication/356755198_Emergent_Narrative_and_Reparative_Play) — ResearchGate record. [RE-VERIFY: locate primary venue copy]
  - **Consume (key):** players actively co-construct meaning in emergent systems. Macha can *design for repair*: present coherent relational state + history + narrative clues so the player keeps the NPC feeling like a persistent relationship.
- **[UNRESOLVED]** No retrieved evidence on "Ellie"/relational agents, tabletop/freeform RPG co-maintenance, "willing suspension of disbelief" as a game-studies concept, or the specific claim that history-violation breaks harder than underperformance.

## Formal/operational takeaways for Macha
1. **Half-real applies to NPCs:** treat NPCs as rule-governed agents inside an imagined relational world — rules govern memory/relationship/expression, fiction supplies imagined continuity.
2. **Agency is interpretive, not just mechanical:** dialogue form and available responses must support dramatic interpretation, not only valid commands.
3. **Sustained intentional-state consistency is the load-bearing property:** once the stance is adopted, the NPC must maintain consistency or the stance collapses — this is a formal, testable requirement.
4. **Dramatic/relational state must be legible:** Façade's supported lesson is that social state must be visible enough for the player to interpret — R must be *observable*, not just internal.
5. **Incomplete systems can be repaired by players:** Macha need not simulate every relational detail; deliberately incomplete history + reparative interpretation can sustain the illusion — but repair is a possibility, not a guarantee.

## Pitfalls / avoid
- Don't claim Façade failed *only* because of NLU — evidence points to dramatic-beat communication, social-state transparency, interaction failure.
- Don't overextend reparative-play evidence (emergent/sandbox systems ≠ all NPC relationships; repair is not inevitable).
- Don't treat the intentional stance as a formal implementation — it's descriptive; Macha still needs operational rules.
- Don't assume players will always repair broken history.
- Don't cite secondary/aggregator pages (darcynorman notes, Semantic Scholar records, ResearchGate, blogs) as primary — replace with primary sources.

## Bibliography
See inline links. Primary anchors: Juul 2005 (MIT Press); Juul 2019; Wardrip-Fruin 2009 (MIT Press); Mateas 2001/2004; Sali et al. FDG 2010; Mateas & Stern AIIDE 2005; Knickmeyer & Mateas CHI 2005; Björk & Juul 2012; Grinblat et al. 2021.

## Open questions
1. [UNRESOLVED] Giddings, "Gameplay and Intentionality" (Game Studies 2016) — no stable URL retrieved.
2. [UNRESOLVED] Willis / Akillian Castle emergent-narrative work — no stable URL retrieved.
3. [UNRESOLVED] Façade post-mortem on "lowercase-c" content, Beatrice/Trip consistency, replay/tuning.
4. [UNRESOLVED] Empirical work on players maintaining NPC relationship illusions (Ellie / relational agents).
5. [UNRESOLVED] Tabletop/freeform RPG research on co-maintained character consistency.
6. [UNRESOLVED] Whether history-violation breaks harder than underperformance; when the system must cooperate vs refuse projection.
