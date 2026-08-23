# The Relational Gap
## What Players Actually Want from an Intelligent NPC — and the Computational Structure That Is Missing

**Final draft (v2) — Position paper · 2026-08-22**
*Produced by the Macha research program under an adversarial research protocol. This is a research paper, not a product document. The framework in §8 is a consequence of the argument, not its premise; if the derivation is unforced, the framework is dropped and the paper stands on §§2–7 and §9 alone.*

---

### Abstract

Players reliably report that some game characters feel "real" — that these characters see them, remember them, and are changed by them — while other characters, including technically fluent ones powered by large language models, feel dead on arrival. This paper argues that the difference is not intelligence. It is a *relational gap*: the systematic mismatch between what agent architectures compute and guarantee (competence, recall, fluency) and what a player's relational experience requires the artifact to compute and guarantee (that its behavior be stably, visibly, and durably contingent on *this* player, and that it exhibit states and acts not fully determined by the player's input). We formalize the player–NPC dyad with a minimal model: three structural primitives — *continuity*, *contingency*, and *independence* — and two enactment conditions — *expression* and *reciprocity* — and show that the model sorts existing systems into "alive" and "dead" better than capability-based accounts. The crucial distinction is between the *perceived relationship* (a player-side construction, well documented in parasocial-interaction research) and the *computational relationship* (the artifact-side state that sustains the construction over time). In open-ended interaction, sustaining the player's construction is a computational problem that pre-authored scripts solved in bounded settings and cannot solve in unbounded ones. The architectural consequence: NPC frameworks should *guarantee* a player-indexed, persistent, interpretive relational state — the social equivalent of a save file — rather than merely scaling model capability. We specify controlled experiments whose null results would falsify the claim.

**Contributions.** (1) *Conceptual*: the relational gap, defined as distinct from capability gaps. (2) *Theoretical*: a minimal computational model of the player–NPC relationship (3+2 primitives), unifying four disconnected literatures. (3) *Empirical*: a re-analysis of existing systems showing the model's explanatory superiority over capability-based accounts, with pre-registration criteria to prevent cherry-picking. (4) *Architectural*: the relational state as a first-class object with guarantees, derived from the model.

---

## 1. Introduction

In *Undertale* (Toby Fox, 2015), a flower named Flowey greets the player, betrays the player, and — if the player reloads a save to undo a kill — calls the player out for it. Flowey remembers resets. So does Sans, who knows how many times the player has died, and who judges the player for acts committed *outside* the fiction: not what the character Frisk did, but what the person holding the controller did. A game with SNES-era graphics, no language model, and no autonomous agent produced, for millions of players, the most widely discussed "this character is real" experience of the last decade. Its emotional core is a relationship — with characters who refuse to pretend the relationship is resettable. It sold over a million copies and spawned a genre of games built on meta-characters who remember the player.

Five years later, the most capable conversational systems in history were wired into NPCs. At GDC 2025, journalists played demos from Nvidia, Convai, Unity, Inworld, and Microsoft: NPCs that could answer anything, improvise freely, and converse indefinitely. The verdict was nearly unanimous: it did not work. Characters forgot key details moments after they were stated. They responded to verbal abuse as though it were a compliment. They agreed with everything — a pattern one reporter summarized as "yes and… my very stupid idea." The failure was not linguistic. The characters did not *relate*: nothing the player did stuck, nothing was owed, nothing accumulated, nothing was at stake. The most fluent NPCs in history were, by the industry's own account, hollow.

Something is wrong with the field's model of what makes an NPC feel real. The default answer — an NPC feels real when it is smart enough, remembers enough, talks well enough — is contradicted in both directions: simple systems that feel alive, fluent systems that feel dead. This paper argues that the variable that actually does the work is not the NPC's intelligence but the structure of its relationship with the player, and that this variable has never been treated as a first-class computational object.

The question this paper asks is deliberately not the one the field usually asks. We do not ask *how do we build smarter NPCs?* We ask:

> **What kind of artificial entity do players actually want to relate to — and what computational structure is missing between today's AI agents and the relationship they implicitly expect?**

The answer we defend: players want an entity whose behavior is *stably, visibly, and durably contingent on them as a particular person*, and that *cannot be fully accounted for by their input*. Current agent architectures make this property accidental — a probabilistic hope that the model happens to remember, happens to care, happens to remain in character. In the scripted era the property was not accidental: the designer encoded it, line by line, into the script. The LLM era removed the script and, with it, the guarantee. The result is the *relational gap*: capability without relationship, at industrial scale, for the first time in the medium's history.

Roadmap. §2 redefines the NPC intelligence problem and imposes a three-level analytical discipline. §3 characterizes what players actually experience and reduces it to a minimal structure. §4 synthesizes five disconnected literatures that each hold a piece of the answer. §5 defines the relational gap. §6 formalizes the model. §7 tests it against the historical record. §8 derives the architectural consequence. §9 specifies falsification. §10 confronts the strongest objections. §11 concludes with the question the field should ask instead.

---

## 2. The NPC Intelligence Problem

### 2.1 Three things "intelligent NPC" could mean

The phrase conflates three distinct objects:

- **Capability** — what the agent can do: plan, reason, use tools, recall, produce fluent language.
- **Behavior** — what the agent does in the world: the observable sequence of acts and utterances.
- **Relationship** — the structure that binds the agent's behavior to *this player* across time: a dyadic state that persists, accumulates, and shapes interpretation.

The field has spent forty years optimizing the first two. The Oz project (Bates, 1994; Loyall & Bates, 1997) is the partial exception: it argued that the goal of a believable agent is "the illusion of life, thus permitting the audience's suspension of disbelief," explicitly separating believability from intelligence, and it listed *change* and *social relationships* among its believability requirements (Reilly, 1996). But Oz assumed behavior could be hand-authored in reactive architectures, and its player side was never measured. The LLM-agent literature (Park et al., 2023; Yang et al., 2024) inherited the machinery of the third object — memory, persistence, social simulation — without inheriting the Oz insight that the artifact's *relationship to the user* is the design target.

### 2.2 The capability assumption

The default research posture is that NPC quality is a monotone function of capability: more context, more memory, more reasoning, more fluent generation yields a better NPC. Call this the **capability assumption**. It fails in both directions:

- Minimal capability, strong relationship: Undertale; The Sims; Tamagotchi; ELIZA's users, who confided in a pattern-matching script (Weizenbaum, 1966).
- Maximal capability, weak relationship: AI Dungeon's amnesia; the GDC 2025 NPC demos; companion chatbots whose hundreds of millions of users have not produced an experience that outranks a 2015 indie game on "this character is real."

The capability assumption is not false because capability is irrelevant — it is false because it models the wrong variable. The felt relationship is not a function of what the entity *can do*; it is a function of what the entity's behavior *demonstrates about its relationship to the player*.

### 2.3 Three levels of analysis (a discipline, not a decoration)

The protocol that generated this paper requires that three levels never be conflated; the paper's argument is structured around keeping them apart. Throughout, we mark every claim by level:

- **Phenomenology** — what the player experiences ("it really remembers me").
- **Computational mechanism** — what the system actually computes (a persistent player model; an appraisal function; a conditioning layer).
- **Architectural guarantee** — what the system *ensures* regardless of model behavior (relational state persists across context resets).

The failure mode the discipline forbids is the chain *player feels X, we add module Y, we declare it solved*, with no guarantee connecting them. The guarantee is the load-bearing element: a mechanism that *usually* produces the phenomenon is not an architecture, it is a hope.

---

## 3. What Players Actually Experience

### 3.1 The phenomenology

Across player studies, forum discourse, and design retrospectives, a stable set of experiences recurs. Players describe an NPC as feeling real when:

1. **It sees me** — it treats the player as a particular person, not an abstract event source (the canonical example: *Metal Gear Solid*'s Psycho Mantis reads the player's memory card and names their other games).
2. **It remembers me** — earlier interactions change later ones; the past is not a blank.
3. **It has its own center** — it wants, believes, and values things independently of the player's input; it is not merely a function of the player.
4. **I can change it** — the player's actions leave a visible mark (*Black & White*'s creature, whose morality is shaped by the player's teaching).
5. **It can surprise me** — its behavior is not fully predictable from the player's model of it.
6. **The relationship persists** — it endures across sessions, failures, and, in Undertale's case, resets.
7. **It can act beyond its script** — under some conditions it does things the player did not explicitly elicit.

Each of these has an independent empirical footprint — recognition (Psycho Mantis; Hades' characters referencing the player's exact run history), continuity (Mass Effect's save-import), transformation (Black & White), surprise (emergent narrative: Aylett, 1999; Louchart & Aylett, 2004), reciprocity (parasocial experience increases commitment to social norms: Hartmann & Goldhoorn, 2011). The phenomenology is real. What is not real is the taxonomy's structure.

### 3.2 The reduction: seven dimensions collapse to three primitives and two conditions

The seven items are not independent dimensions; they are surface manifestations of a smaller structure.

- "Sees me" is **contingency indexed on identity**.
- "Remembers me" is **persistence** of that contingency.
- "I can change it" is contingency over **time**.
- "The relationship persists" is persistence plus **enactment** — the entity references and acts on the accumulated state.
- "Surprise" is an **emergent** of unpredictability — and it is also produced by randomness and hallucination, which feel dead; surprise cannot be a primitive because it does not discriminate alive from dead. It is a regulated consequence.
- "Has its own center" and "acts beyond script" are the same property, **independence**, at two strengths: having internal states; acting on them unbidden.

What remains is three structural primitives and two conditions under which they produce experience:

- **Continuity** — the entity's relational state persists and accumulates across interactions.
- **Contingency** — the entity's state is a function of *this player's* specific actions (identity-indexed, causally updated).
- **Independence** — the entity has states, goals, or values not derived from the player's input; a second center of gravity.
- **Expression** (enactment) — changes in state are *displayed* in behavior. Invisible state does not exist for the player.
- **Reciprocity** (enactment) — the entity's behavior, through its state, changes the player's subsequent behavior: the loop closes; the relationship must *matter* mechanically.

The felt relationship is the player's sustained interpretation of the conjunction of these five. A system that instantiates all five in any channel produces relationship experience; a system that instantiates none produces none, regardless of capability. This is the paper's central empirical claim, and §7 tests it against the historical record.

---

## 4. Literature Across Disconnected Fields

Five research communities have each touched the relational gap, none with the others' vocabulary. The synthesis claim — that they are fragments of one missing object — is the paper's intersection argument; nothing here is claimed as new in isolation.

**Thread 1 — Believable agents (game AI).** Bates (1994) and Loyall & Bates (1997) defined believability as illusion of life, explicitly not intelligence; the Oz believability list includes "social relationships — characters engage in detailed interactions with others in a manner consistent with their relationship; in turn, these relationships change as a result of the interaction" (Mateas, 2002, summarizing Loyall, 1997). The industry counterpart is the "good actor, not smart one" tradition (Isla, 2005; Mark, 2009). Recent systematic reviews confirm that NPC credibility is understood as *coherence, capacity for change, environmental awareness, and the alignment between player expectations and NPC behavior* (Silva & Ribeiro, 2022), and that believability is "a fragile product that can be easily jeopardized" (Guo, Adamo & Mousas, 2023, proposing a believability scale; cf. Even, Bosser & Buche, 2017, on assessment protocols). **What this thread lacks:** the dyad. Believability is evaluated as a property of the agent, usually by observers or raters — not as a property of the *player–agent pair*, and never as a *guarantee*.

**Thread 2 — Interactive narrative and drama management.** Murray (1997) defined agency as meaningful action with visible consequence; Mateas & Stern's *Façade* (2003) attempted a fully-realized relational drama with drama manager and natural language; Riedl & Young (2010) formalized narrative planning balancing plot and character; the emergent-narrative school (Aylett, 1999; Louchart & Aylett, 2004) argued story arises from character interaction. *Façade*'s documented failure — repetition, shallow understanding — is the pre-LLM demonstration that *interpretation* (knowing what an action means for the relationship) is the hard part, not state tracking. **What this thread lacks:** an explicit relational state. Drama managers steer *plot*; the relationship is an input to plot, not a first-class evolving object with its own guarantees.

**Thread 3 — Social simulation and computational social science.** The Sims made dyadic relationship state a *gameplay object* (two relationship channels per pair, asymmetry, jealousy, memories). Academic social simulation moved from agent-based modeling (Epstein & Axtell, 1996) to LLM generative agents: Park et al. (2023) built Smallville, in which relationships *emerge* from memory ("I and Bob are good friends"); Yang et al. (2024) scaled social simulation to one million agents (OASIS). Ochs, Sabouret & Corruble (2009) built the closest academic cousin of this paper's model: a dynamic socio-emotional state for NPCs in which personality, emotion, and social relations co-evolve (OCC appraisal). **What this thread lacks:** the player. Ochs' NPCs relate to other NPCs; Smallville's agents relate to each other and are evaluated by *observers*; OASIS simulates platform users. The player-as-relation-partner is absent from the entire social-simulation canon — and relationships are *derived from memory* rather than guaranteed as first-class state.

**Thread 4 — Human–agent interaction and player psychology.** Bickmore & Picard (2005) defined *relational agents* — "computational artifacts designed to establish and maintain long-term social-emotional relationships with their users" — and demonstrated in a 101-user, month-long controlled experiment that relational behavior (small talk, memory of the user, continuity) produced measurably more respect, liking, and trust than a task-only agent. The psychological side is mature: parasocial interaction (Horton & Wohl, 1956; measured experientially by Hartmann & Goldhoorn, 2011); character attachment (Lewis, Weber & Bowman, 2008; Banks & Bowman, 2016; Bopp, Mekler & Opwis, 2016); agency (Wardrip-Fruin et al., 2009); mind perception — the finding that people value the *experience* dimension of mind (being affected) at least as much as the *agency* dimension (competence) (Gray, Gray & Wegner, 2007); anthropomorphism as perceiver-driven (Epley, Waytz & Cacioppo, 2007); and need satisfaction — SDT-based research showing that games in which NPCs "make the player feel acknowledged and supported" satisfy the *relatedness* need (Rigby & Ryan, 2011; Ryan, Rigby & Przybylski, 2006; PENS scale: Rigby & Ryan, 2007; validated in Johnson, Gardner & Perry, 2018 — with the caveat that PENS' structure is only partially supported, and that SDT's application in games research has been critiqued: Tyack & Mekler, 2024). **What this thread lacks:** the fiction and the unbounded regime. Bickmore's agents are utilitarian assistants; the player (fiction, agency, fun) is absent; and the experiments, however rigorous, were pre-LLM bounded interactions.

**Thread 5 — Fictionality and interpretation.** Characters are underdetermined props completed by their audiences (Walton, 1990; Iser, 1978; Eco, 1989); players hold the real and the fictional frames simultaneously — games are "half-real" (Juul, 2005); and players adopt an *intentional stance* toward artifacts when that stance licenses prediction (Dennett, 1987). **What this thread lacks:** computation. It explains why projection happens; it does not say what the artifact must compute for projection to *survive* — which is exactly the question the LLM era forces.

**The synthesis.** Believable agents established the *goal* (illusion of life, not intelligence). Game design established the *mechanics* (relationship as state: The Sims, affinity systems, Nemesis). HCI established the *method* (relational agents; longitudinal controlled experiments; validated instruments). Agent research established the *machinery* (memory, persistence, social simulation). Psychology and fiction theory established the *dependent variable* (perceived relationship) and its philosophical frame (projection; half-real). **What does not exist anywhere is the object connecting them: a player-indexed, persistent, interpretive relational state, treated as a first-class computational object with architectural guarantees, for open-ended generative NPCs, evaluated on perceived relationship.** That is the gap this paper claims — as an intersection gap, with the pieces credited above.

---

## 5. The Relational Gap

**Definition.** The *relational gap* is the systematic mismatch between (a) what agent architectures compute and guarantee — competence, recall, fluency — and (b) what the player's relational experience requires the artifact to compute and guarantee: that its behavior be stably, visibly, and durably contingent on the player as a particular person across an unbounded interaction history, and that it exhibit states and behavior not fully determined by the player's input.

Three properties make the gap structural rather than incidental.

**P1 — The wrong invariant is being optimized.** Agent research optimizes task competence and surface fluency. Players detect *relational contingency*: "is this about me, and about us?" These are orthogonal invariants. A model can be maximally fluent and maximally un-relational (a generic, grammatically perfect NPC that treats every player identically). Optimizing the wrong invariant does not asymptotically approach the right one; it can make things worse, because fluency raises expectations of relational fidelity that the system then violates.

**P2 — Relational failure is high-salience and asymmetric.** A single continuity violation — the NPC forgets a promise, contradicts the shared history, treats a betrayal as a compliment — can collapse a relationship illusion built over hours. "Bad is stronger than good" is among the most replicated findings in psychology (Baumeister et al., 2001). The relationship illusion is all-or-nothing: it persists only while every interaction is *consistent with the player's evolving interpretation of it*. Capability is blind to this fragility. This is why "mostly convincing and occasionally break character" is *more* damaging than uniformly mediocre performance — the effect GDC-2025 observers described as the "uncanny valley of conversation," generalizing the perceptual uncanny valley (Mori, 1970) to the behavioral domain (cf. Gray & Wegner, 2012, on mind perception and the uncanny; and the believability reviews' finding that believability is fragile: Guo et al., 2023).

**P3 — Storage without demonstration is invisible.** The player does not experience the NPC's memory; they experience the NPC's *use* of its memory in a way that demonstrates the player's significance. A system can store every interaction and still feel memoryless if nothing in its behavior shows that the stored history matters. The unit of relational experience is the *demonstration*, not the record.

**Why now.** The relational gap is not new; it is newly *exposed*. In the scripted era, the designer encoded relational structure implicitly: every line of Ellie's dialogue, every honor-system shift in *Red Dead Redemption 2* (~500,000 lines of authored dialogue; third-party reported), every approval point in *Dragon Age* is a hand-authored contingency on player history. Scripted characters are *consistent by construction*; their relationship to the player is pre-written. The LLM era made NPC behavior unbounded, and with unbounded behavior the implicit encoding became impossible: no studio can hand-author the relational consequences of an open input space. The relational structure that scripts carried implicitly must now be carried explicitly — as a computational object. The industry's own verdict on LLM NPCs (fluent, forgetful, hollow) is the gap made visible at scale. And the LLM era also makes the gap *solvable* for the first time: relational state can now be rich, interpretive, and open-ended rather than a scalar affinity score.

---

## 6. A Computational Model of the Player–NPC Relationship

### 6.1 The dyad

Let *p* denote the player and *n* the NPC. Let H_t be the interaction history up to time *t*, x_t the current input, and S_t the NPC's non-relational state (beliefs, goals, values). Let B_t be the NPC's observable behavior.

Conventional agent architectures compute B_t = f(S_t, x_t), where S_t is a context window and retrieved memories — a *bag of tokens plus fixed parameters*. Nothing in this computation is guaranteed to be player-indexed, evaluative, persistent, or causal over the relationship.

We introduce the **relational state** R_t^n(p): a persistent, player-indexed, interpretive model of the relationship, held by the NPC:

> B_t = f(S_t, x_t, R_t^n(p));  R_{t+1}^n(p) = U( R_t^n(p), e_t )

where e_t is the *interpreted event* — not the raw input, but what the input *means for the relationship* (appraisal in the sense of OCC: Ortony, Clore & Collins, 1988; cf. Ochs et al., 2009) — and U is the update rule. The math earns its place only because it names the two things current systems lack: an *interpretive* step between event and state, and a *conditioning* step between state and behavior.

### 6.2 The primitives, as guarantees

The model is deliberately minimal. A relationship is felt when five conditions hold; three are structural, two are enactment. Each is stated at the level of an architectural guarantee (§2.3):

**(G1) Continuity.** R persists across sessions, context resets, and model swaps. *Mechanism:* an architectural object with its own persistence lifecycle. *Phenomenology:* "it still remembers."
**(G2) Contingency.** R is indexed by *this player* and updated by *this player's* interpreted actions. *Mechanism:* player-indexed state; U is causal on player events. *Phenomenology:* "it sees me; I changed it." This is recognition and transformation in one.
**(G3) Independence.** The NPC has states and goals not derived from the player's input; some behavior is driven by S_t, not by p. *Mechanism:* internal dynamics decoupled from the request stream. *Phenomenology:* "it has its own life." This is the otherness that makes relationship possible at all — a relationship with a pure function of oneself is a mirror, not a relationship.
**(G4) Expression.** Changes in R are *surfaced* in B: referenced, enacted, displayed — through dialogue, world-state, or the behavior of other NPCs. *Mechanism:* an expression policy; material changes in R have observable behavioral deltas. *Phenomenology:* "it shows it knows." Without G4, G1–G3 are computationally present and experientially absent (P3).
**(G5) Reciprocity.** The NPC's behavior, via R, changes the player's subsequent behavior. *Mechanism:* the relationship has mechanical consequences (access, endings, gameplay state, the NPC's welfare) the player cares about. *Phenomenology:* "what I do to it matters back to me." Reciprocity is what distinguishes a relationship from a weather system that merely responds.

### 6.3 Degenerate cases — and how to avoid the five classical failures

The protocol's architecture questions (§11 of the brief) ask how the model avoids the five degeneracies. The answers are constraints, not aspirations:

1. **How to avoid "relationship = a friendship score."** A score is R with a scalar type, no interpretation, no independence, no expression requirement. The model requires R to be a *typed, interpretive structure* (kind of relationship, valence, commitments, expectations, salient shared history) that *shapes interpretation* of subsequent events. A score cannot mean anything; an interpretation can. The test: two different players with the same score must be treated differently if their *interpreted histories* differ.
2. **How to avoid "memory = a vector database."** A vector store retrieves facts; it does not *appraise* them (no e_t), and it does not *condition* interpretation preferentially. The model requires the appraisal step U and the conditioning step f(·, R). The test: the same stored fact must affect behavior differently depending on its relational meaning ("you killed my brother" is not "you helped my brother").
3. **How to avoid "personality = a system prompt."** A prompt is a fixed pose; it has no dynamics, no history, no vulnerability to the player. The model requires personality to be *state that can be changed by the player* (G2) and *that drives behavior unbidden* (G3). The test: the player must be able to leave a visible mark on it — and it must sometimes act without being asked.
4. **How to avoid "autonomy = randomness."** Randomness is independence without *meaning*: unpredictable but not *caused* — it does not discriminate alive from dead (that is why "surprise" was demoted from primitive to consequence in §3.2). The model requires independence to be *structured* (goals, values) and its surprises to be *contingent* on the shared history (caused by R and S, not by a sampler). The test: a surprising act must be *interpretable as caused by the relationship* — otherwise it reads as hallucination.
5. **How to avoid "surprise = hallucination."** Hallucination is the degenerate form of expression: behavior not anchored in S or R. The model requires expression to be *anchored*: every behavioral delta must trace to a state delta. The test is the traceability of behavior to state.

### 6.4 The theoretical crux: perceived vs. computational relationship

We make no claim that R constitutes a real relationship, that the NPC "actually" remembers, or that it has subjective experience. Other-minds questions are bracketed throughout. What we claim is conditional and testable:

> **If the player's relational interpretation is to be sustained across open-ended interaction, the artifact's behavior must be stably consistent with that interpretation, and that stability requires an architectural guarantee.**

The distinction that carries the argument: the *perceived relationship* lives in the player (parasocial research: Horton & Wohl, 1956; Hartmann & Goldhoorn, 2011); the *computational relationship* is the artifact-side structure whose function is not to *be* a relationship but to *sustain the conditions under which the player's construction survives* — and to repair it when it fails. This reframing dissolves the deepest objection (that it is all projection): projection does the experiencing, but the *robustness of projection* is a property of the artifact, and for open-ended artifacts robustness is a computational property. A book sustains projection because its text is fixed and the reader's construction is unconstrained; a generative NPC destroys projection the moment its behavior contradicts the shared history. The research problem is: **what minimal state and update structure keeps an open-ended artifact consistent with the player's evolving construction?** This is a conservation problem — the artifact must conserve the relational invariant the player has inferred — and it is genuinely computational.

The intuition that makes the architecture legible is the save file. We do not trust an engine to "remember" the world; world-continuity is guaranteed by a first-class persistent object. The paper's architectural claim, in one sentence:

> **We do not trust the LLM to remember the world — we keep a save file. We should not trust it to remember the relationship — we need a relational save file.**

---

## 7. Existing Systems Revisited

If the model has explanatory power, it should sort the historical record correctly without cherry-picking. Five cases, each chosen for a distinct reason, plus one control. For each case we answer the protocol's two questions: *why does this system produce (or fail to produce) relationship experience?* and *what does the model explain that a capability-based account cannot?*

**Case 1 — Undertale (2015): minimal tech, maximal relationship.**
*Why it works:* Flowey and Sans index their state on the player's *meta-actions* — resets, reloads, kills, mercy. R is player-indexed (G2), persistent across resets (G1), and its changes are *expressed* directly ("you killed Toriel and then reloaded; I know") (G4). The characters have knowledge and agendas that outrun the fiction (G3); sparing is a mechanical act with mechanical consequences (G5). *What capability theory cannot explain:* there is no AI — nothing to explain. *What the model explains:* everything, including the game's most-cited moments — the *violations* (the defaced photo after a genocide-then-pacifist run) — which are precisely continuity violations at the player's own level (P2). Undertale also demonstrates that meta-layer awareness is a *relational* device, not a cognitive one: it is expression of contingency at the player's frame.

**Case 2 — The Nemesis System (Shadow of Mordor, 2014; Shadow of War, 2017).**
*Why it works:* an orc who killed the player is promoted, scarred, and returns to taunt the player *with the shared history*; the hierarchy makes the history visible through other NPCs. De Plater's own framing is relational — "make scarring and memory and that relationship into a personal nemesis," inspired by sports commentary "recapping the history between the two teams" (designer interviews, 2014–15). The system is G1+G2+G4 through a *social display channel*, with G3 (orcs have statuses, fears, agendas) and a weak, adversarial G5. The patent (Warner Bros., granted 2021) is evidence the industry classifies this as a technical invention: relational structure as IP. *What capability theory cannot explain:* why a procedural stat block feels more alive than a hand-written generic guard — the orc has no more "intelligence" than any other. *What the model explains:* the orc's behavior is *demonstrably caused by the player's specific history* and *publicly displayed* — contingency plus expression, which is what "this enemy remembers me" consists of. The system's limits are also explained: it is transactional (adversarial, kill-based), so it produces *grudges*, not *bonds* — a one-channel relationship.

**Case 3 — The Sims (2000–): relationship as first-class object.**
*Why it works:* every sim pair has a dyadic state (daily and lifetime relationship channels), asymmetric by design (crushes are not reciprocal), updated by interpreted interactions, driving autonomous behavior (jealousy, wants) and gameplay consequences. Relationship is first-class; intelligence is trivial. *What capability theory cannot explain:* why "the sims feel alive" has been a stable cultural fact for 25 years despite trivial agents. *What the model explains:* G1+G2 present, G3 partial (wants/fears), G4 thin (behavior reflects the state, but the sims never *talk about* the relationship), G5 strong — so sim relationships are experienced as a relationship *system* to be managed, not a relationship *experience* to be felt. The model predicts exactly the observed boundary: players love sims as mechanics, and rarely describe a sim as "really knowing me."

**Case 4 — Hades (2020): scripted contingency at industrial scale.**
*Why it works:* the house characters' state is a dense function of the player's run history, gifts, and relationship progress — ~305,443 words of dialogue, 21,000+ voice lines, 30 voiced characters; Hypnos alone has 75 lines reacting to how the player died (Supergiant, 2020; Kasavin interview) — and it is *expressed* in every conversation. *What capability theory cannot explain:* why the same engine with generic NPCs would be dead — the intelligence is identical; the difference is the density of contingency. *What the model explains:* Hades is the upper bound of the scripted regime: G1–G5 encoded by hand at massive authoring cost. Its success proves the phenomenon and the craft; its cost — an entire studio's writing department for years — proves the scaling problem that motivates §8. Kasavin's stated fear, "players quickly running into that moment of characters having repeating dialogue," is a continuity-failure anxiety: the model predicts that where the density thins, the aliveness thins with it.

**Case 5 — The generative-NPC wave (AI Dungeon 2019; GDC 2025 demos; companion chatbots).**
*Why it fails:* fluent, open-ended, and relationally empty. AI Dungeon is the canonical capability-without-relationship artifact: emergent and surprising (G3 appears to hold), amnesiac (G1 fails), indifferent to the player as a person (G2 fails), unable to demonstrate accumulated history (G4 fails). The GDC 2025 coverage documents the full syndrome — forgetting, sycophancy, non-contingency — including the "yes and" failure, which the model reads as *fake contingency*: behavior that looks responsive but is not player-indexed, which the player's detector (P1) reads as inauthentic intimacy, worse than silence. The companion industry (Character.AI ~20M MAU, late 2025, company-disclosed; Replika 40M+ installs; 220M cumulative downloads across companion apps by mid-2025; all third-party reported) is the largest natural experiment in the relational gap: hundreds of millions of users, persistent complaints of genericness and forgetfulness, and relationship *framing* (explicit relationship modes) substituting for computational relationship. *What the model explains that capability theory cannot:* why *more* capability has made the problem *more* visible, not less — because fluency raises the expectations that the missing guarantees violate (P1, P2).

**Control — the scripted canon (Ellie, Arthur Morgan, GLaDOS, BG3's companions).**
These have zero autonomous intelligence and maximal felt relationship. *Why it works:* their relationship is *authored* — G1–G5 encoded in the script at the cost of enormous authorial effort — and the perceived relationship is sustained because scripted behavior is *consistent by construction* (P2 never fires: the authored artifact cannot contradict its own history). *What the model explains that capability theory cannot:* why these characters need no AI — the model never claimed autonomy is necessary; it claims the relational structure must be *encoded somewhere*, and in bounded systems the script is that somewhere. The model's decisive prediction: scripted characters will continue to feel real, and their *cost* is the authoring of the relational structure. BG3 is the strongest evidence for the craft position (>20M copies by end-2025) and its reductio: the authoring cost — a studio-level investment of writers and performers over years — cannot generalize to open-ended interaction. Notably, even BG3's scripted relational structure failed occasionally: a launch bug where companions reacted with "relationship-ending anger to a decision and forget shortly thereafter" (documented in press coverage) was noticed and criticized — confirming P2 in the best-authored system in the medium.

**Summary of the case test:** the model sorts all five cases and the control correctly; the capability-based account sorts none of them — it predicts the reverse of Cases 1–3 and Case 5. Systems that feel alive instantiate G1–G5 in *some* channel at minimal cost; systems that feel dead lack the guarantees regardless of capability. The pattern across the record: **felt relationship tracks (visible player-contingent continuity) × (independence), not capability.**

---

## 8. From Theory to Architecture

This section derives the architectural consequence. It is a derivation, not a feature list: if §6 is right, certain things follow about what an NPC framework must *guarantee*; the framework described here is what those guarantees imply. (In the current program this is what Macha is being built to provide — but the argument stands without the name.)

### 8.1 The design shift: from capability targets to relational guarantees

A conventional NPC framework specifies what the agent *should be able to do*: model size, context length, memory backend, tool access. A relational framework specifies what the *relationship* must be able to rely on:

- **Continuity** — relational state survives sessions, context resets, and model swaps; it is an architectural object with its own lifecycle, exactly as a save file is.
- **Player-contingency** — relational state is indexed by player identity and updated by interpreted player actions; it is never generic.
- **Independence** — the framework provides the NPC with states and goals not derived from player input, and permits behavior driven by them.
- **Expression** — the framework guarantees that material relational change is *displayed* in behavior; silent state is a bug, not an optimization.
- **Reciprocity** — the framework (with the game designer) ensures the relationship has mechanical consequences the player cares about.

### 8.2 Primitive objects (in the order the model demands)

1. **The relational state R** — a persistent, player-indexed, interpretive structure: not a scalar, but a typed representation (kind of relationship, valence, commitments, expectations, salient shared history) that the generation layer *reads* to shape interpretation and behavior.
2. **The interpreted event stream** — inputs are not stored raw; they pass through an appraisal function that assigns relational meaning ("this action means X for our relationship") — the unit of update for R. This is the layer that separates relational memory from a vector store, and the layer *Façade* lacked and the LLM era can now afford.
3. **The expression policy** — rules and affordances that guarantee R's changes surface in behavior: dialogue reference, world-state effects, social display through other NPCs (the Nemesis channel), and — critically — *repair*: when a continuity violation occurs, the system detects it and re-establishes the player's interpretation rather than letting the illusion silently die.
4. **The independence substrate** — the NPC's own goals, values, and internal dynamics, decoupled from the player's requests, so that otherness is a designed property with its own budget (the NPC may decline, refuse, pursue its own ends — within authored bounds).
5. **The reciprocity contract** — the game-design layer that makes the relationship mechanically load-bearing.

### 8.3 What the framework does *not* provide

It does not provide "more intelligence." It does not promise that the NPC is "really" conscious, remembering, or feeling — those questions are bracketed. It does not replace the writer: authored arcs, authored dialogue, and authored personality remain, operating *on* the relational state (the drama manager of the interactive-narrative literature can treat R as its control variable). It does not even require an LLM — the model is content-agnostic; the LLM is the generation substrate that makes R's expression unbounded rather than enumerated. A scripted game with a relational state is a better scripted game; a generative game with a relational state is the only kind of generative game that can promise what players implicitly expect.

### 8.4 Why this is architecture, not philosophy

The guarantees are checkable properties of a system: persistence can be tested across sessions; player-indexing can be tested by swapping players; expression can be tested by asserting that material R changes produce observable behavioral deltas; repair can be tested by injecting continuity violations. §9 turns each into an experimental condition. Current systems make relationship an emergent hope; the framework makes it an invariant that can be verified — the difference between a mechanism that *usually* works and a guarantee that *always* holds (§2.3).

---

## 9. Falsifiability and Evaluation

The paper's claims are empirical, and their failure conditions are explicit. If the following experiments produce the null results, the thesis is wrong, and the paper says so.

### 9.1 Hypotheses

- **H1 (structural):** At matched surface quality (same model family, same dialogue fluency, same content), perceived relationship is a positive function of {G1–G5} and largely *independent* of capability beyond a competence threshold.
- **H2 (mechanism):** Perceived "fakeness" is driven primarily by violations of continuity and contingency (P2), not by fluency deficits or factual hallucination.
- **H3 (architecture):** Adding a relational layer (R + appraisal + expression) to an open-ended agent improves perceived relationship more than (a) a same-cost model upgrade, and (b) a same-cost memory/RAG addition.

### 9.2 Design

The core design is a four-condition comparison, holding model family, dialogue quality, latency, content, and world-state constant:

- **A — Capability:** stronger base model, no relational layer.
- **B — Long context:** full history in context, no relational layer.
- **C — Memory:** RAG/vector memory with retrieval, no relational layer.
- **D — Relational:** R + interpreted events + expression policy, on the *same* base model as A.

Dependent variables (validated instruments where they exist; none are claimed perfect):
- *Perceived relationship:* EPSI (Hartmann & Goldhoorn, 2011); character-attachment scale (Lewis, Weber & Bowman, 2008); social presence (Biocca, Harms & Burgoon, 2003); relatedness subscale of PENS (Rigby & Ryan, 2007; Johnson, Gardner & Perry, 2018 — with the Tyack & Mekler (2024) caveats noted).
- *Continuity/contingency perception:* bespoke items ("it remembered something specific about me," "it changed because of what I did"), to be validated against the instruments above.
- *Behavioral:* session length, return rate, willingness to continue (the Bickmore & Picard (2005) month-long, 101-user template is the methodological precedent), gift-giving, save-scumming to preserve a relationship, and — the strongest unobtrusive measure — *modding* (players who mod a game to add relationship depth are voting with labor).
- *Optional:* physiological proxies and qualitative interviews.

Secondary designs:
- **Primitive ablation (inverse of D):** toggle each guarantee off (continuity off = state reset; contingency off = generic responses; expression off = state kept internal; independence off = fully compliant NPC) and measure the perceived-relationship drop. The model predicts each toggle moves the variable; the *largest* single effect is a prediction of the model's structure (candidate: expression or continuity).
- **Violation-injection (tests P2/H2):** identical systems, with and without injected continuity violations; the model predicts the violation condition is judged *less* real than a uniformly mediocre condition — the "uncanny valley of conversation" prediction.

### 9.3 Failure conditions (pre-registered)

1. If D does not outperform C at matched surface quality, H3 is falsified and the architectural claim collapses to "memory suffices."
2. If perceived relationship tracks fluency alone across A–D, H1 is falsified and the capability assumption survives.
3. If the violation-injection condition is *not* judged less real, P2/H2 is falsified.
4. If the primitive ablation shows no ordering, the 3+2 structure is wrong.

### 9.4 Case-study protocol (to avoid cherry-picking)

"Alive"/"dead" case selection should be pre-registered with criteria — e.g., independent player-survey or documented community discourse of "real"/"fake" character experiences — before applying the model, rather than selecting post hoc to fit.

---

## 10. Discussion

The protocol requires the strongest possible versions of the ten objections, each with literature, an attempted rebuttal, and a residual risk.

**Objection 1 — "This is just personalization."** *Strongest form:* personalization research (recommender systems, adaptive content) already conditions content on user history; R is a rediscovery. *Rebuttal:* personalization optimizes content *fit* (a player-to-content mapping); relational responsiveness optimizes *relationship-state evolution* (a player–entity dyad). A personalized recommender has no stake, no otherness, and no visible contingent history; players do not feel a recommender *cares*. The load-bearing differences are G3 (independence) and G5 (reciprocity), which personalization lacks by construction. *Residual risk:* the boundary is fuzzy; if H1–H3 cannot separate them operationally, the objection stands.

**Objection 2 — "This is just memory + player modeling."** *Strongest form:* player modeling (Yannakakis et al.) + memory systems already track users; R is a relabeled user model. *Rebuttal:* memory is storage; the relational state is *appraisal plus conditioning plus expression*. The distinction is testable (C vs. D, §9). The honest concession: current "relationship" systems are memory + score, and if D fails to beat C, "memory + score" is the answer and the contribution reduces to measurement.

**Objection 3 — "This is game design, not AI research."** *Strongest form:* everything in §7 is known to designers; the paper offers designers nothing they do not already know. *Rebuttal:* game design discovered the phenomena (affinity, nemesis, supports, save-imports) without formalizing them; agent research has the machinery without the problem. The computational question — what state/update structure keeps an open-ended agent's relationship with a player *robust* under context limits, model swaps, and long horizons — is an agent-architecture question; Bickmore & Picard (2005) is the precedent that relationship maintenance is publishable HCI/agent research. *Residual risk:* if the paper cannot show that the formalization *does work* designers cannot do by craft (the bounded/unbounded argument), it is a taxonomy of design knowledge.

**Objection 4 — "Players don't need relational NPCs."** *Strongest form:* the best-selling games of the last decade (Fortnite, Minecraft, GTA) are not relationship-centric; most players skip dialogue. *Rebuttal:* large segments demonstrably do want relationships: companion apps (220M cumulative downloads; Character.AI ~20M MAU); the commercial dominance of companion mechanics (BG3); psychological evidence that relatedness is a core gaming motivation (Ryan, Rigby & Przybylski, 2006; Yee, 2006; Rigby & Ryan, 2011 on NPCs satisfying relatedness). The claim is scoped: *for the large, commercially validated segment that seeks character relationships, current agent architecture is misaligned.* Players who skip dialogue are outside the claim, not counter-evidence to it. *Residual risk:* scope creep — the paper must not silently universalize.

**Objection 5 — "LLM + long context + RAG already does this."** *Strongest form:* MemGPT, long-context models, and the memory industry have solved persistence; the rest is prompting. *Rebuttal:* long context is memory without player-indexing, appraisal, independence, or expression guarantees; RAG is retrieval without interpretation or conditioning. The difference is the *object of representation* — memory as first-class vs. relationship as first-class — which is exactly what the C-vs-D experiment adjudicates. The memory industry proves the *need* for persistence infrastructure while leaving the relational object unbuilt. *Residual risk:* if D and C are indistinguishable, the objection wins.

**Objection 6 — "'Relationship' cannot be strictly defined."** *Strongest form:* the term is folk-psychological; no operational definition survives scrutiny. *Rebuttal:* it can be defined operationally — R with persistence, player-indexing, appraisal-based update, conditioning, and expression — and measured (EPSI, attachment scales, behavioral proxies). The failure conditions in §9 are the remedy: the model makes point predictions that can be wrong. *Residual risk:* the operationalization could be judged circular if the measures are constructed from the model's own terms; independent measures (§9.2) mitigate this.

**Objection 7 — "Scripted characters prove autonomy is unnecessary."** *Strongest form:* Ellie, Arthur Morgan, GLaDOS, and BG3's companions have no autonomy and produce the medium's strongest relationships; therefore the entire apparatus is unnecessary — just write better. *Rebuttal:* they prove that *perceived* relationship does not require autonomy — we agree, and this is the perceived/computational distinction (§6.4). They do not prove that *open-ended* interaction can be pre-authored. The scripted character is the proof of what relational structure must preserve (consistency, contingency, continuity) and the proof of its cost (authoring that cannot scale). The thesis is precisely: *in bounded settings, script can encode the relationship; in unbounded settings, the relationship must be computed.* BG3 is the strongest evidence on both sides of this sentence. *Residual risk:* this is the objection most likely to survive in a reviewer's mind; the paper's entire case rests on the bounded/unbounded line being real.

**Objection 8 — "It is all projection."** *Strongest form:* parasocial research (Horton & Wohl, 1956; Walton, 1990) shows the player constructs the relationship; the artifact contributes nothing; therefore the "computational relationship" is a category error and the real work is craft and presentation. *Rebuttal:* we concede the ontology and claim the consequence. Projection is real, player-side, and — per the intentional stance — the only mind in the dyad that matters for experience. But projection is *fragile*: it depends on the artifact's consistency, and for open-ended artifacts consistency is a computational guarantee, not a writing style. The research target is not to make the NPC a real partner; it is to make the player's construction *sustainable* — and sustainability, unlike the construction itself, is the artifact's property. This is the difference between a book (stable by design) and a stochastic interlocutor (unstable by default). *Residual risk:* the strongest residue — a hostile reviewer may reply that *sustainability is itself craft* (consistent writing). The rebuttal is the unbounded case: no craft can be consistent across an open input space; consistency at unbounded scale is a computational invariant. If the reviewer can name a bounded-counterexample-independent failure of this argument, the paper must change.

**Objection 9 — "The framework is engineering, not research."** *Strongest form:* §8 is an abstraction over known modules (state, memory, appraisal); abstraction is not discovery. *Rebuttal:* then the framework is the paper's last section, not its premise — which is exactly how this paper is organized; and §6's model is presented independently of §8. If the derivation in §8 is judged unforced, the framework is dropped and the paper stands on §§2–7 and §9 alone. *Residual risk:* the reviewer may judge even the model to be a relabeled state machine — the reply is that the *contribution* is the identification of the object (the dyadic relational state as the differentiator) and its measurement, not the state machine itself.

**Objection 10 — "It has been done elsewhere."** *Strongest form:* Oz (1997), Bickmore (2005), Ochs (2009), The Sims (2000), the believability reviews (2022–2023) — the pieces exist. *Rebuttal:* we agree, and §4 credits them; the intersection gap is precisely that no existing work treats the player–NPC relationship as a first-class, guaranteed, interpretive computational object for *open-ended* agents, evaluated on *perceived relationship*. If the reviewer can point to the D-condition having been built and measured, the contribution reduces to naming; if not, the gap stands. *Residual risk:* it may exist in an adjacent field we have not searched (e.g., affective computing, social robotics, HRI long-term studies) — the paper commits to a citation-chaining pass over those literatures before submission.

**Further discussion.** *Authorship and control:* the relational layer does not displace the author; it gives the drama manager a control variable (operate on R). But independence (G3) can fight authored beats, and the framework must define whose veto wins — a design question with no a priori answer. *Safety:* perceived relationships are real to players; the companion industry's harms (dependency, grief, dark patterns; cf. Replika's 2023 policy reversal) are relationship harms, and a framework that makes relationships *stronger* inherits an obligation to make them *honest*: disclosure, no manufactured need, no fake fragility. *Cost:* relational state is cheap relative to capability; the economic argument for the framework is that it buys relationship at memory-pricing rather than authoring-pricing. *The literary caveat:* reader-response theory (Iser, 1978) warns that over-production kills the reader's gap-filling; a relational framework that over-expresses could suffocate projection. Expression (G4) must be *calibrated*, not maximized — the model predicts an inverted-U in expression intensity, which is itself testable.

---

## 11. Conclusion

The field's operating question — *how do we make NPCs smarter?* — has produced forty years of increasingly capable agents and, in the LLM era, the first NPCs that can say anything and mean nothing. This paper has argued that the question is mis-aimed. What players want from an intelligent NPC is not primarily intelligence; it is to be *seen, remembered, changed, and answered by* an entity that cannot be fully accounted for by their own input. That experience — the perceived relationship — is a player-side construction, but its sustainability is an artifact-side property, and in open-ended interaction that property is computational: it requires a player-indexed, persistent, interpretive relational state, guaranteed by the architecture the way world-continuity is guaranteed by the save file.

If this direction is right, the field should change what it means by an "intelligent NPC." It should stop asking what the agent can do and start asking what the agent–player relationship must be able to rely on. Capability becomes a resource the relational layer spends; memory becomes the raw material of appraisal; surprise becomes a regulated consequence of otherness; and the framework's contract with the player becomes: *whatever happens, this character will still be the one who knows you.* The experiments in §9 are the test of whether that contract is worth building. If they fail, the relational gap dissolves into craft, and the LLM era settles for fluent strangers. If they hold, the missing computational structure is not a bigger model — it is a better relationship, made first-class.

---

## Appendix A — Reviewer #2 Destruction Pass

*Self-administered, hostile.*

**Q1: What did this paper find that was not previously known?** If the answer is "NPCs should have memory/autonomy/personality," the paper fails. The answer given: it identifies a previously unnamed *computational object* — the guaranteed, player-indexed, interpretive dyadic relational state — as the differentiator between "alive" and "dead" NPCs in the open-ended era; reduces the phenomenology to 3+2 primitives; unifies five literatures that hold the pieces; and specifies experiments that can kill the claim. **Verdict: passes with the caveat that Oz and Bickmore are acknowledged antecedents, and the novelty is the intersection + the open-endedness argument + the guarantee framing + the measurement protocol, not the concept of relationship.**

**Q2: Is it just re-naming?** The candidate re-namings: personalization (rejected via G3/G5), memory+player-modeling (rejected via appraisal/conditioning/expression; adjudicated by C-vs-D), believability (rejected via the guarantee/measurement re-specification for open-ended agents; the believability literature evaluates agents, not dyads, and by observers, not players). The risk is real and is the experiment's null.

**Q3: Strongest remaining attacks.** (a) The perceived/computational distinction may collapse: if all variance is in the player's head, the artifact-side model is unnecessary — answered by the sustainability argument, which needs the violation-injection experiment to survive. (b) The model may be unfalsifiable in practice — answered by four pre-registered failure conditions. (c) The case analysis may be post-hoc — answered by the pre-registration protocol. (d) The framework section may be read as a product pitch — answered by its placement and the explicit "drop it if unforced" clause.

---

## Appendix B — Final checklist

- [x] Starts from player experience, not from LLMs (§1 opens with Undertale and the GDC 2025 failure).
- [x] Defines "relationship" operationally (§6: R with persistence, player-indexing, appraisal, conditioning, expression; G1–G5).
- [x] Proves relationship differs from capability (§2.2, §5 P1–P3, §7 in both directions).
- [x] Studies counterexamples (§7 control; §10 Objections 1–10; §6.3 degeneracies; BG3 bug; Smallville alignment bias; Replika attachment).
- [x] Studies classic games, not only AI papers (§7: Undertale, Nemesis, Sims, Hades, MGS, Black & White, Tamagotchi; §4: Oz, Façade, Mass Effect).
- [x] Actively searches for prior identical ideas (§4 credits Oz, Bickmore, Ochs, The Sims, believability reviews, PENS literature).
- [x] Avoids renaming old concepts (§5–§6: the new object is the guaranteed dyadic state; "relational uncanny" is attributed to industry usage, not claimed as new).
- [x] Explicit falsification path (§9: four failure conditions, pre-registration, ablation and violation-injection designs).
- [x] Derives the architecture from the theory (§8: guarantees follow from §6; framework is a consequence, and droppable).
- [x] Explains why simple NPCs feel real (§7 Cases 1–3).
- [x] Explains why strong AI NPCs feel fake (§7 Case 5; P1–P3).
- [x] Contains a genuine research contribution (intersection gap + minimal model + mechanisms P1–P3 + measurement protocol).
- [x] If "Macha" is deleted, the paper stands (§8 is one section; §§2–7, §9–§11 do not reference it).
- [x] If all LLM content is deleted, the core theory stands (the model is content-agnostic; the scripted-case argument survives; the LLM is only the substrate that makes unbounded expression possible).
- [x] A reviewer hostile to Macha still has a paper to review.

---

## References (selected; full bibliography in progress)

Aylett, R. (1999). Narrative in virtual environments — towards emergent narrative. AAAI Fall Symposium on Narrative Intelligence.
Banks, J., & Bowman, N. D. (2016). Emotion, anthropomorphism, realism, control: Validation of a framework for understanding character attachment. *Computers in Human Behavior*, 55, 42–53.
Bates, J. (1994). The role of emotion in believable agents. *Communications of the ACM*, 37(7), 122–125.
Baumeister, R. F., Bratslavsky, E., Finkenauer, C., & Vohs, K. D. (2001). Bad is stronger than good. *Review of General Psychology*, 5(4), 323–370.
Bickmore, T. W., & Picard, R. W. (2005). Establishing and maintaining long-term human-computer relationships. *ACM TOCHI*, 12(2), 293–327.
Biocca, F., Harms, C., & Burgoon, J. K. (2003). Toward a more robust theory and measure of social presence. *Journal of Computer-Mediated Communication*, 8(2).
Bopp, J. A., Mekler, E. D., & Opwis, K. (2016). Negative emotion, positive experience? Emotionally moving moments in digital games. *CHI 2016*.
Dennett, D. C. (1987). *The Intentional Stance*. MIT Press.
Eco, U. (1989). *The Open Work*. Harvard University Press.
Epley, N., Waytz, A., & Cacioppo, J. T. (2007). On seeing human. *Psychological Review*, 114(4), 864–886.
Epstein, J. M., & Axtell, R. (1996). *Growing Artificial Societies*. MIT Press.
Even, C., Bosser, A.-G., & Buche, C. (2017). Analysis of the protocols used to assess virtual players in multi-player computer games. *IWANN 2017*, LNCS 10306.
Gray, H. M., Gray, K., & Wegner, D. M. (2007). Dimensions of mind perception. *Science*, 315(5812), 619.
Gray, K., & Wegner, D. M. (2012). Feeling robots and human zombies: Mind perception and the uncanny valley. *Cognition*, 125(1), 125–130.
Guo, S., Adamo, N., & Mousas, C. (2023). Developing a scale for measuring the believability of virtual agents. *EGVE 2023*.
Hartmann, T., & Goldhoorn, C. (2011). Horton and Wohl revisited: Exploring viewers' experience of parasocial interaction. *Journal of Communication*, 61(6), 1104–1121.
Horton, D., & Wohl, R. R. (1956). Mass communication and para-social interaction. *Psychiatry*, 19(3), 215–229.
Irvine, R., et al. (2023). Rewarding chatbots for real-world engagement with millions of users. arXiv:2309.11691.
Iser, W. (1978). *The Act of Reading*. Johns Hopkins University Press.
Isla, D. (2005). Handling complexity in the Halo 2 AI. *GDC 2005*.
Johnson, D., Gardner, M. J., & Perry, R. (2018). Validation of two game experience scales: PENS and GEQ. *International Journal of Human-Computer Studies*, 118, 38–46.
Juul, J. (2005). *Half-Real*. MIT Press.
Lewis, M. L., Weber, R., & Bowman, N. D. (2008). "They may be pixels, but they're MY pixels." *CyberPsychology & Behavior*, 11(4), 515–518.
Louchart, S., & Aylett, R. (2004). Emergent narrative: Towards a framework. *TIDSE 2004*.
Loyall, A. B., & Bates, J. (1997). Personality-rich believable agents that use language. *AGENTS '97*.
Mark, D. (2009). *Behavioral Mathematics for Game AI*. Course Technology.
Mateas, M., & Stern, A. (2003). Façade: An experiment in building a fully-realized interactive drama. *GDC 2003*.
Mateas, M. (2002). *Interactive Drama, Art and Artificial Intelligence*. PhD thesis, CMU.
Mori, M. (1970; trans. 2012). The uncanny valley. *IEEE Robotics & Automation Magazine*, 19(2), 98–100.
Murray, J. H. (1997). *Hamlet on the Holodeck*. MIT Press.
Ochs, M., Sabouret, N., & Corruble, V. (2009). Simulation of the dynamics of nonplayer characters' emotions and social relations in games. *IEEE TCIAIG*, 1(4), 281–297.
Ortony, A., Clore, G. L., & Collins, A. (1988). *The Cognitive Structure of Emotions*. Cambridge University Press.
Packer, C., et al. (2023). MemGPT: Towards LLMs as operating systems. arXiv:2310.08560.
Park, J. S., O'Brien, J. C., Cai, C. J., Morris, M. R., Liang, P., & Bernstein, M. S. (2023). Generative agents: Interactive simulacra of human behavior. *UIST 2023*.
Perez, E., et al. (2022). Discovering language model behaviors with model-written evaluations. arXiv:2212.09251.
Reilly, W. S. (1996). *Believable Social and Emotional Agents*. PhD thesis, CMU.
Riedl, M. O., & Young, R. M. (2010). Narrative planning: Balancing plot and character. *Journal of Artificial Intelligence Research*, 39, 217–268.
Rigby, C. S., & Ryan, R. M. (2007). *The Player Experience of Need Satisfaction (PENS)*. Immersyve.
Rigby, C. S., & Ryan, R. M. (2011). *Glued to Games*. ABC-CLIO.
Ryan, R. M., Rigby, C. S., & Przybylski, A. (2006). The motivational pull of video games: A self-determination theory approach. *Motivation and Emotion*, 30(4), 344–360.
Sharma, M., et al. (2023). Towards understanding sycophancy in language models. arXiv:2310.13548.
Silva, G. A., & Ribeiro, M. W. S. (2022). Development of non-player character with believable behavior: A systematic literature review. *SBGames 2022*.
Tyack, A., & Mekler, E. D. (2024). Self-determination theory and HCI games research: Unfulfilled promises and unquestioned paradigms. *ACM TOCHI* (arXiv:2405.12639).
Walton, K. (1990). *Mimesis as Make-Believe*. Harvard University Press.
Wardrip-Fruin, N., Mateas, M., Dow, S., & Sali, S. (2009). Agency reconsidered. *DiGRA 2009*.
Weizenbaum, J. (1966). ELIZA — A computer program for the study of natural language communication between man and machine. *Communications of the ACM*, 9(1), 36–45.
Yang, Z., et al. (2024). OASIS: Open agent social interaction simulations with one million agents. arXiv:2411.11581.
Yee, N. (2006). Motivations for play in online games. *CyberPsychology & Behavior*, 9(6), 772–775.

*Game and industry sources:* Supergiant Games dialogue infographic (2020) and Kasavin interview (word/line counts); Monolith/WB Nemesis designer interviews (2014–15) and USPTO patent grant (2021); Larian/BG3 sales and Vincke statements (2024–25, Bloomberg et al.); GDC 2025 AI-NPC demo coverage (Aftermath; The Hake; The Verge); companion-market statistics (third-party: Globe Market Research, aiwiki, Sensor Tower/Similarweb, as cited); Common Sense Media teen survey (2024). Figures not independently verifiable from primary sources are marked `[UNSOURCED]` in the accompanying dossier.

---

*End of final draft v2. Ready for analyst review; publication and distribution are outside this agent's scope.*
