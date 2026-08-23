# Phase I — Research Dossier
## Macha Directional Research: What Do Players Actually Want from an Intelligent NPC?

**Status:** Draft for analyst review · **Date:** 2026-08-22 · **Working language:** English
**Cover note:** This dossier is the output of a multi-role skeptical review (game-AI researcher, interactive-narrative researcher, HCI/agent researcher, player-psychology researcher, philosophy-of-mind researcher, hostile reviewer). It does not defend Macha. It tests Macha's hypotheses, discards what fails, and lets the recommended thesis emerge from evidence. All figures are sourced to public filings, peer-reviewed literature, or clearly attributed third-party reporting; anything unverifiable is marked `[UNSOURCED]`.

---

## 1. Core question

**Restated, per protocol:** not "How do we build smarter NPCs?" but:

> **What kind of artificial entity do players actually want to relate to, and what computational structure is missing between today's AI agents and the relationship players implicitly expect?**

Two sub-questions that the whole program turns on:

1. Is there a measurable distinction between **agent capability** (what the NPC can do) and what we provisionally call **relational responsiveness** (how the NPC's behavior is caused by, and visible to, *this particular player* over time)?
2. If that distinction holds, is the gap *architectural* (a missing computational object that must be guaranteed) or merely *artisanal* (better writing, better prompts, better game design)?

The second sub-question is the one that separates a research contribution from a product critique. The dossier's conclusion: **the gap is real, partially named in scattered literatures, and becomes an architectural problem precisely when interaction becomes open-ended (the LLM era). It is an intersection gap, not an absolute novelty.**

---

## 2. Current Macha hypotheses (as received, tested)

| # | Hypothesis | Initial verdict after research |
|---|---|---|
| H1 | NPC "fakeness" is not primarily about how little the NPC knows, but about the player and NPC using different cognitive/interpretive frames. | **Partially supported but mis-specified.** The literature supports an *interpretive asymmetry* (player holds a relational/meta frame; the artifact often does not), but the F_in / F_in⊕F_meta notation is the wrong tool (see §4, §10). |
| H2 | Players don't primarily want more capable NPCs; they want "the world to respond to my behavior." | **Supported** — this is the psychological construct of *agency* (Murray 1997; Wardrip-Fruin et al. 2009) plus *contingency*; it also matches mind-perception findings that people value the *experience* dimension (being affected) at least as much as the *agency* dimension (competence) (Gray, Gray & Wegner 2007). |
| H3 | Players expect NPCs to: see me / remember me / have a self / be changed by me / surprise me / maintain continuity / act beyond script. | **Supported as a phenomenology, but not as a taxonomy.** Seven items collapse to three structural primitives + two enactment conditions (§10). Keeping all seven as independent dimensions would be a category error. |
| H4 | Scaling model, context, and reasoning mainly improves single-encounter performance, not the player–NPC relationship. | **Supported by converging evidence** — behavioral (AI-Dungeon/LLM-NPC failure reports), theoretical (illusion maintenance requires guarantees, not fluency), and market (companion apps scale users but not relationship depth). This is the paper's load-bearing empirical claim and the one that most needs a controlled experiment (§Falsifiability). |

**Macha's genuinely new ingredient (candidate):** the claim is not "NPCs should have memory/personality/autonomy" (that is a feature list, and it is decades old), but that **the player–NPC relationship should be a first-class, persistent, player-indexed, interpretive computational object with architectural guarantees** — and that the *LLM era makes this necessary* because it made unbounded behavior possible and pre-authored scripts insufficient. The historical record shows the first half of this was glimpsed repeatedly (Oz, The Sims, relational agents); the second half (why it must be computational *now*) is the defensible contribution.

---

## 3. Evidence supporting each hypothesis

### H1 (interpretive asymmetry, not information deficit)

- **Horton & Wohl (1956)** define parasocial interaction as a "simulacrum of conversational give and take"; **Horton & Strauss (1957)** add that the experience "is immediate, personal, and reciprocal, but these qualities are illusory and are presumably not shared by the speaker." The felt relationship is generated in the perceiver's interpretive frame — the artifact need not "know" anything for the *experience* to occur. This is direct evidence that the player-side frame does massive work.
- **Hartmann & Goldhoorn (2011, EPSI scale, N=198):** parasocial *experience* is intensified by the performer's *addressing* behavior (bodily and verbal address of the audience). Interpretation responds to *displayed contingency*, not to stored knowledge. An NPC can "know" nothing and still trigger the experience if it *addresses the player*.
- **Mind perception (Gray, Gray & Wegner 2007, *Science*):** people perceive minds along two independent dimensions — *Experience* (hunger, fear, pain, pleasure; 88% of variance) and *Agency* (self-control, planning, memory, thought; 8%). Crucially, "desire to avoid harming" tracks Experience (r=.85) more than Agency (r=.26). Players want the NPC to *be affected by them* — an experiential, relational property — not primarily to be a competent planner. This is the strongest empirical anchor for "relationship > capability."
- **Dennett's intentional stance (1987):** players adopt an interpretive stance that treats the artifact as an intentional agent; the stance is justified by predictive usefulness, not by internal structure. The player's frame supplies the mind; the artifact's job is to keep the stance *predictively tenable*.

### H2 (response / contingency, not capability)

- **Agency theory:** Murray (1997) defines agency as "the satisfying power to take meaningful action and see the results of our decisions and choices"; Wardrip-Fruin, Mateas, Dow & Sali (2009) refine it as the experienced coupling of action and consequence. "The world responds to me" is the canonical formulation of what players want from interactivity — not "the world is smart."
- **Player motivation research:** Yee (2006) finds *relationship* is a primary motivation component in online games; Self-Determination Theory applied to games (Ryan, Rigby & Przybylski 2006) lists **relatedness** alongside competence and autonomy as a core psychological need that games can satisfy. There is a measurable, theory-backed demand for relational experience.
- **Case evidence (below, §6):** systems that maximize contingency with minimal intelligence (The Sims' dyadic relationship state; Undertale's history-tracking; Hades' run-indexed dialogue) produce stronger felt relationship than far more capable systems that lack it.

### H3 (the seven expectations as phenomenology)

- Each of the seven items has an independent empirical footprint in player research: recognition → Psycho Mantis (MGS) reading the memory card (canonical "the system perceives me"); continuity → save-import continuity in Mass Effect; being-changed-by-me → Black & White's learned creature; self → Sims' autonomous wants; surprise → emergent-narrative literature (Aylett 1999; Louchart & Aylett 2004); beyond-script → Undertale's meta-characters; reciprocity → player-norm adherence in parasocial studies (Hartmann & Goldhoorn 2011 found stronger parasocial experience → greater commitment to social norms).
- **But:** as §10 shows, these reduce. Recognition = contingency indexed on identity; continuity = persistence; transformation = contingency over time; surprise = emergent from independence×contingency. The taxonomy's *content* is supported; its *structure* is not.

### H4 (capability scaling does not buy relationship)

- **Direct industry reports:** GDC 2025 hands-on coverage of AI-NPC demos from Nvidia, Convai, Unity, Inworld, and Microsoft (Aftermath): "in broad strokes, it did not work"; NPCs "yes and…" the player, misunderstand abuse as compliments, and the fun available was "the sheer absurdity" — an anti-relationship mode. Skyrim-ChatGPT mod reviews: "Characters forgot key details moments later. And after a while, it wasn't fun anymore" (The Hake). One reporter's summary of the failure mode: generative NPCs are "mostly convincing and occasionally break character in ways that are jarring precisely because the rest of the interaction felt so natural" — the *relational* uncanny: violation is worse than absence.
- **Industry practitioners:** Ubisoft's Mélanie Lopez Malet: "These characters do not have free will" and the model's job is "I must impersonate this character" — i.e., the industry itself frames LLM NPCs as *impersonation* (surface) layered on authored character sheets, with guardrails — not as entities with relationships. Larian's Swen Vincke reports AI experiments in their pipeline "were not successful" and the upcoming Divinity title will contain none. CD Projekt's Paweł Sasko: "a gigantic, really long way to go" before AI NPCs match authored characters.
- **Companion-market scale vs. depth:** Character.AI ~20M MAU (late 2025, company-disclosed); Replika 40M+ cumulative installs but ~2M MAU — the largest AI-relationship products in history, and their persistent complaint (documented in user forums and press) is exactly H4's failure mode: generic, sycophantic, forgetful responses. **Hundreds of millions of dollars and users have not produced a relationship experience that outranks a 2015 indie game with SNES graphics.**
- **Academic:** generative agents (Park et al. 2023) — even in a *simulation-only* setting, reviewers noted the alignment bias: "Isabella… never refuses absurd suggestions… even changes her own self-concept" — the sycophancy failure appears in agent architectures too (corroborated by sycophancy literature: Perez et al. 2022; Sharma et al. 2023; Irvine et al. 2023).

---

## 4. Evidence against each hypothesis

### Against H1 (the asymmetry claim, as literally stated)

- **The player also lacks "true" meta-cognition in the sense required.** The F_in / F_in⊕F_meta notation implies the NPC has no meta-layer and the player does. But modern agents can be given self-models, world-models, and system-awareness trivially by prompting; and players are *not* continuously meta-aware (they oscillate between game-frame and fiction-frame — Juul's "half-real," 2005). The asymmetry is not "NPC lacks F_meta" — it is that the *artifact has no representation of the relationship itself*, while the player inevitably does. **The correct target is a dyadic relational model, not "meta-cognition." The F_in/F_meta formalism should be discarded** (see §10, Model C).
- **Alternative explanation with better evidence:** "fakeness" may be partly a *fluency-expectation mismatch* — the uncanny valley generalized to behavior (Mori 1970; Gray & Wegner 2012 on mind perception and the uncanny). High surface realism raises expectations of relational fidelity; violation is then more jarring. This is a *perceptual* account that competes with the interpretive-frame account; both are probably true, and the paper must test them apart.

### Against H2 (if "response" is read as "no capability needed at all")

- **Scripted systems produce response without intelligence — trivially.** RDR2 (~500,000 lines of authored dialogue, third-party reported), BG3 (companion reactivity at massive authoring cost; >20M copies sold by end-2025), Hades (300k+ words; ~305,443 words of dialogue per Supergiant's infographic). If contingency alone sufficed, the conclusion would be "just write more," and the research problem dissolves into craft. **This is the strongest objection to the whole program (Objection 7).** The paper's escape: scripted contingency is *bounded* — every contingency is enumerated; the LLM era's open-ended input space makes enumeration impossible, so the relational structure that scripts used to encode *implicitly* must become an *explicit computational object*. The Sims/Undertale/Hades cases prove the *phenomenon*; the LLM-NPC failures prove the *necessity*.
- **Players demonstrably do not need response from the artifact at all.** Parasocial research is built on one-sided bonds (readers, viewers, players of pure narrative games, visual novels). Tamagotchi, ELIZA (Weizenbaum 1966), and grief over robotic pets (AIBO funerals, 2015, Japan) show relationship experience with near-zero computational reciprocity. **This is the projection objection (Objection 8), and it is the deepest threat.** It is handled in §8 and in the model (the artifact's function is *sustaining the conditions of projection* — a computational problem of *robustness*, not of *simulation*).

### Against H3 (the taxonomy)

- **The seven dimensions are not orthogonal.** (i) "Perceive me" and "remember me" and "be changed by me" are the same variable — contingency — measured at different timescales/objects. (ii) "Surprise" is produced as often by *randomness and hallucination* as by genuine otherness — in LLM NPCs, surprise and error are indistinguishable to the player; surprise is therefore a *consequence* to be regulated, not a primitive. (iii) "Act beyond script" is independence, but independence without continuity reads as incoherence, not agency. A seven-dimensional taxonomy would fail construct validity; a three-primitive model survives it.

### Against H4 (capability does nothing for relationship)

- **Capability is a necessary substrate.** Undertale's relationship magic works because the *writing* is superb; Nemesis works because the *system* is legible; Hades works because 21,000+ lines are *authored*. No relational state makes bad prose feel alive. The honest formulation: **capability (incl. language quality) is necessary but not sufficient; relational structure is the differentiator at matched surface quality.** This is exactly the controlled-comparison design of §Falsifiability — and it means H4 as stated ("mainly improves single-encounter performance") is too strong; it should read "improves it *disproportionately little* and, at matched surface quality, *relational structure moves perceived relationship more than capability does*."
- **Companion apps contradict H4 partially:** Replika and Character.AI users report genuine long-term attachment (the market exists); the *mechanism* of attachment there is partly relational framing (explicit relationship modes) plus *investment* — evidence that even degenerate relational structure (a "how should we relate?" prompt + memory) beats none.

---

## 5. Closest existing theories (the field already has the pieces)

| Theory / concept | Source | What it already says | Where it stops short |
|---|---|---|---|
| **Believable agents** | Bates (1994); Loyall & Bates (1991, 1997); Reilly (1996) — Oz project | Agents must "provide the illusion of life, thus permitting the audience's suspension of disbelief"; believability list explicitly includes *self-motivation*, *change*, and *social relationships* ("characters engage in detailed interactions with others in a manner consistent with their relationship. In turn, these relationships change as a result of the interaction") | Assumed hand-authored reactive architectures; never faced open-ended generation; the player side (measurement) was thin. The LLM-agent field did not inherit this literature. |
| **Relational agents (HCI)** | Bickmore & Picard (2005, *TOCHI*); Bickmore (2003) | "Relational agents are computational artifacts designed to establish and maintain long-term social-emotional relationships with their users"; relationship as "a persistent construct, incrementally built and maintained"; 101-user, month-long controlled experiment showing relational > task-only on respect/liking/trust | Domain is health/behavior-change assistants; relationships are utilitarian; the *player* (fiction, agency, fun) is absent; no LLM-era open-ended case. **But the experimental template is directly transferable.** |
| **Social relations for NPCs** | Ochs, Sabouret & Corruble (2009, *IEEE TCIAIG*); Paiva group (FAtiMA; FearNot) | Dynamic socio-emotional state for NPCs: personality → emotion → social-relations dynamics (OCC-based); relationships as evolving state influencing behavior | State is scalar/typed and hand-modeled; no player-indexed dyad; no open-ended language; evaluated on plausibility, not perceived relationship. |
| **Drama management / interactive narrative** | Weyhrauch (1997); Mateas & Stern (2003, Façade); Riedl & Young (2010); Aylett (1999); Louchart & Aylett (2004) | "Dramatic agency"; narrative as emergent from character; plot-character balance; the player's experience is the design target | Drama managers steer *plot*, not *relationship as state*; Façade's failure (repetition, shallow interpretation) pre-dates LLMs and is instructive: *interpretation* (understanding what an action means for the relationship) is the hard part. |
| **Parasocial interaction / character attachment** | Horton & Wohl (1956); Hartmann & Goldhoorn (2011); Lewis, Weber & Bowman (2008); Banks & Bowman (2016); Bopp, Mekler & Opwis (2016) | One-sided bonds are real, measurable, and consequential; *addressing* drives the experience; attachment correlates with enjoyment, play time, and even addiction risk | These are measurement theories of the *player side*; they do not specify the *artifact side* (what state/update structure sustains the bond). |
| **Generative agents / social simulacra** | Park et al. (2023); Yang et al. (2024, OASIS) | Memory stream + reflection + planning yields believable social behavior; relationships *emerge* from memory (e.g., "I and Bob are good friends"); OASIS scales social simulation to 1M agents | Relationships are *derived from memory*, not first-class; **there is no player** — the dyad is agent–agent or agent–platform; no guarantee that relationship state survives, is player-indexed, or is expressed. |
| **Mind perception / anthropomorphism** | Gray, Gray & Wegner (2007); Epley, Waytz & Cacioppo (2007) | Two dimensions of perceived mind (Experience, Agency); anthropomorphism is perceiver-driven, motivated by sociality needs | Says nothing about what the artifact must *compute*; if anything, it tempts the wrong conclusion (it's all in the player's head). |
| **Agency / ergodic literature** | Murray (1997); Aarseth (1997); Wardrip-Fruin et al. (2009); Tanenbaum & Tanenbaum (2009) | Meaningful action + visible consequence; the reader/player does interpretive work | Agency is about *world* consequences; the *relationship* as a distinct consequence class is under-theorized. |
| **Fictionality / make-believe** | Walton (1990); Juul (2005); Iser (1978); Eco (1989) | Characters are underdetermined props; the reader fills gaps; games are "half-real" (rules + fiction held simultaneously) | Provides the philosophical frame for perceived-vs-computational but has not been connected to agent architecture. |

**Synthesis claim (the intersection gap):** every field holds one piece — craft (Oz), mechanics (Sims), measurement (parasocial/attachment), HCI method (Bickmore), agent machinery (Park), fictionality (Walton/Juul) — but **no existing work treats the player–NPC relationship as a first-class, persistent, player-indexed, interpretive computational object with architectural guarantees, for open-ended generative NPCs, evaluated on perceived relationship.** That is the defensible gap.

---

## 6. Closest existing systems (already-built evidence)

**Systems that produce strong felt relationship with minimal intelligence ("alive but simple"):**
- **The Sims (2000–):** dyadic relationship state as a *gameplay object* — two relationship channels per pair (daily, lifetime), asymmetric (crushes are not reciprocal), jealousy, memories, autonomous wants. Relationship is first-class; intelligence is trivial. Decades of "the sims feel alive."
- **Undertale (2015):** minimal tech, maximal relationship. Characters (Flowey, Sans) *remember across the player's resets* — meta-continuity beyond the fiction; the game's save file is *read and written by characters*; sparing vs. killing is a relational act with relational consequences; the true ending is a relationship reward. 1M+ copies sold (Toby Fox, announced); still discussed a decade later.
- **Hades (2020):** scripted-but-reactive at scale — dialogue is a function of your exact run history, gifts, and relationships; ~305,443 words of dialogue, 21,000+ lines, 30 voiced characters (Supergiant, 2020); Hypnos alone has 75 death reactions. The *density of contingency* is the craft.
- **Nemesis System (Shadow of Mordor, 2014; Shadow of War, 2017):** procedural orcs with player-indexed history — "memories mean each encounter influences the next"; enemies remember killing you, get promoted, taunt you with *your* history; the hierarchy makes history *visible and social* (de Plater: "make scarring and memory and that relationship into a personal nemesis"). Patented (Warner Bros., granted Feb 2021). Design genealogy: sports-game commentary recapping rivalries + pen-and-paper "recurring villain."
- **Black & White (2001):** the creature's morality/personality is a visible, cumulative function of *your* teaching — ownership and transformation ("my creature").
- **Tamagotchi (1996) / Nintendogs / Creatures (1996):** care → attachment; the creature *depends on you* — contingency plus stakes with near-zero state.
- **Psycho Mantis (Metal Gear Solid, 1998):** the system *reads your memory card* and names your other games — a one-shot, canonical "the system perceives me" event.
- **Portal (2007) — GLaDOS:** scripted relational antagonist; the whole character is *defined by* its (one-sided, toxic) relationship to you, including its change at the end. Zero autonomy, total relationship.
- **Disco Elysium (2019):** no NPC AI at all; the *world and the protagonist's own skill-voices* respond to your ideological choices; Kim Kitsuragi is one of the most-beloved companions in the medium — pure authored contingency.

**Systems with high capability that feel "dead" ("capable but fake"):**
- **AI Dungeon (2019–):** the first mass LLM narrative; famous for emergent surprise and famous for *not remembering* — the illusion collapses at the first contradiction. Capability high, relational continuity absent.
- **LLM NPC demos (2023–2025):** Inworld/Convai/Nvidia/Unity/Microsoft GDC demos — fluent, open-ended, and widely reported as hollow, forgetful, sycophantic ("yes and…"); the failure is *relational*, not linguistic (Aftermath; The Hake; The Verge's "nakedly chatbot").
- **Character.AI / Replika (2022–):** billions of messages; the largest real-world relational experiment in history; persistent user complaints of genericness, sycophancy, and memory loss — relationship *framing* without computational relationship *guarantees*.
- **Skyrim's Radiant AI / generic guards:** "I took an arrow to the knee" — looped, non-contingent; a standing cultural joke about NPC deadness.
- **Starfield (2023):** technically modern Bethesda NPCs; widely described as soulless.
- **Generative agents (Smallville, Park et al. 2023):** in-simulation agents are believable to *observers* — but the authors' own alignment-bias observation (Isabella never refuses; her self-concept drifts to please) shows the sycophancy failure is architectural in the LLM-agent paradigm.

**The pattern:** *felt relationship tracks (visible player-contingent continuity) × (independence), not capability.* The "dead but capable" set is exactly the set with unbounded fluency and no relational structure; the "alive but simple" set is exactly the set with relational structure and bounded fluency.

---

## 7. Historical lineage (the problem is old; the vocabulary is new)

- **1966 — ELIZA (Weizenbaum):** minimal script, maximal projection; Weizenbaum's alarm is the first "it's not real understanding" debate. The illusion works; it is also *fragile* (repetition gives it away) — foreshadowing the robustness problem.
- **1970 — Uncanny valley (Mori):** perceptual mismatch framework; generalized later to minds (Gray & Wegner 2012).
- **1980s — Interactive fiction:** parsers force the player to do the interpretive work (ergodic literature, Aarseth 1997).
- **1991–1997 — Oz project (Bates; Loyall & Bates; Reilly):** the field's founding statement that *believable* (illusion of life) ≠ *intelligent*; includes change and social relationships in its believability requirements. **The single most important antecedent — and one the LLM-agent community has not read.**
- **1993–1996 — Ethological creatures (Blumberg; Perlin & Goldberg's Improv):** learning from user feedback, procedural social actors.
- **2000 — The Sims:** relationship as gameplay object; Will Wright's bottom-up philosophy (the player's imagination completes the sims).
- **2001 — Black & White:** learned creature as "changed by me."
- **2003 — Façade (Mateas & Stern):** drama management + natural language; the first explicit attempt at an *emergent relational experience* — and its limits (repetition, shallow interpretation) are the limits of pre-LLM interpretation.
- **2005 — Relational agents (Bickmore & Picard):** HCI formalizes long-term HCI relationships and *measures* them (the 101-user, month-long study).
- **2007 — Mass Effect:** save-import continuity — *the save file as relationship carrier across titles.*
- **2009 — Ochs et al.:** social relations as dynamic computational state for NPCs (IEEE TCIAIG).
- **2009–2016 — Affinity-system era:** Dragon Age approval, Fire Emblem supports, Persona confidants, Stardew hearts — relationship-as-progression with mechanical payoff; players demonstrably grind relationships.
- **2014 — Nemesis System:** procedural player-indexed relational history; patent proves the industry considers it a *technical* invention.
- **2015 — Undertale:** meta-characters who remember the player across resets — the ceiling of scripted relational design.
- **2019 — AI Dungeon; 2022 — Character.AI/Replika scale-up; 2023 — generative agents (Park et al.), BG3's companion phenomenon (10M players by Feb 2024, 15M by Nov 2024, 20M+ by end-2025), MemGPT/memory-as-industry; 2024–25 — OASIS, memory infra (Mem0, LangMem), and the GDC 2025 wave of LLM-NPC demos with the industry's own "hollow" verdict.**
- **The through-line:** every capability jump (parsers → scripted state → affinity systems → LLMs) re-exposes the same gap because *the gap was never about capability*. It was masked by craft in bounded systems and exposed by unbounded systems. The LLM era is the first time the masking is impossible at scale.

---

## 8. Contradictory evidence (the strongest counter-cases)

1. **The projection objection, in full strength:** all NPC relationship is parasocial; the player does *all* the relational work (Horton & Wohl 1956; Walton 1990). Evidence: players cry at books; ELIZA's success; Tamagotchi; AIBO funerals. Under this view, "computational relationship" is a category error, and the correct research is *craft + presentation*, not architecture. **Reply (adopted):** concede the ontology — the felt relationship is player-constructed; we never claim the NPC "has" a relationship (other-minds questions bracketed; intentional-stance framing). But the *durability* of the player's construction is a property of the artifact, and in open-ended interaction that property *requires* computational structure: a generative NPC destroys the projection the moment it contradicts the shared history; a book cannot. The research question becomes: **what minimal state/update structure keeps an open-ended artifact *consistent with the player's evolving projection*?** This is real computation (conservation of an inferred invariant), not craft.
2. **The craft objection, in full strength:** BG3/RDR2/Disco Elysium prove authored contingency suffices; players demonstrably prefer it (BG3 >20M copies vs. AI-NPC products). **Reply:** bounded systems can pre-enumerate contingency; open-ended systems cannot. BG3's *scale* of authoring (€249M profit year; hundreds of writers/performers) is exactly what cannot generalize to every NPC in every game. The relational layer is what scripts *were* — made computational.
3. **"Players don't actually want relational NPCs":** large player segments skip dialogue, play for challenge; the industry's best-selling games (Fortnite, Minecraft, GTA) are not relationship-centric. **Reply (scoping):** the claim is not universal; it is that *for the large, commercially validated segment that does* (companion apps: 220M cumulative downloads by July 2025, ~20M MAU at Character.AI, 72% of US teens 13–17 having used an AI companion per Common Sense Media), current agent architecture is misaligned. The paper must scope, not universalize.
4. **A bug as counter-evidence:** BG3's launch had a documented bug where companions "react with relationship-ending anger to a decision and forget shortly thereafter" (Digital Spy, cited via Wikiwand) — even the best scripted relational system breaks its own continuity; players noticed. This cuts *both* ways: it proves continuity violations are noticed (supporting the fragility thesis) and that scripted systems also fail (weakening "craft always wins").
5. **Smallville's believability result:** generative agents *with memory* were rated more believable than humans role-playing the agents — capability + memory does produce *observer* believability. This is the best evidence *against* H4 in the simulation setting — and it is why the paper must distinguish *observer-rated believability* from *player-experienced relationship* (they are different dependent variables; Smallville has no player).
6. **Replika's attachment:** users with genuinely long-term bonds to a *degenerate* system show that relational *framing* + investment can carry a relationship with minimal state — constraining how strong the "guarantees" claim can be.
7. **Uncanny valley of conversation (industry term in use):** "mostly convincing and occasionally break character… jarring precisely because the rest felt so natural" — the perceptual account competes with the interpretive account (both likely true; must be disambiguated experimentally).
8. **Cost and latency:** LLM NPCs fail *also* for non-relational reasons (latency, cost, hallucination of facts) — the paper must not attribute every failure to the relational gap.
9. **The market counter:** companion apps monetize poorly (top 10% of apps = 89% of category revenue; Replika's ARR ~$14–35M on 40M+ installs) — evidence that *demand* for relationship is real but *willingness to pay* is unresolved; the paper should not claim commercial validation for the *architecture*.
10. **Skeptic's strongest form:** "You have just re-described good game writing." **Final reply:** good game writing *is* the specification of a relational structure — authored contingency, continuity, expression. The paper's claim is that this structure, which writing encodes *implicitly and per-content*, can be made *explicit and per-architecture*, so that unbounded generative content inherits it without per-content authoring. If that is impossible to demonstrate, the thesis fails — and the failure condition is explicit (§Falsifiability).

---

## 9. Important terminology (existing terms, adopted with care)

- **Parasocial interaction / experience** — Horton & Wohl (1956); Hartmann & Goldhoorn (2011, EPSI).
- **Character attachment** — Lewis, Weber & Bowman (2008); Banks & Bowman (2016).
- **Believable agents / illusion of life** — Bates (1994); Loyall & Bates (1997).
- **Relational agents** — Bickmore & Picard (2005).
- **Agency / dramatic agency** — Murray (1997); Mateas & Stern (2003); Wardrip-Fruin et al. (2009).
- **Mind perception: Experience vs. Agency** — Gray, Gray & Wegner (2007).
- **Anthropomorphism** — Epley, Waytz & Cacioppo (2007).
- **Intentional stance** — Dennett (1987).
- **Half-real** — Juul (2005). **Make-believe / prop** — Walton (1990). **Gap-filling (reader-response)** — Iser (1978); Eco's open work.
- **Emergent narrative** — Aylett (1999); Louchart & Aylett (2004).
- **Uncanny valley / valley of mind / (industry) "uncanny valley of conversation"** — Mori (1970); Gray & Wegner (2012); GDC 2025 press usage.
- **Sycophancy** — Perez et al. (2022); Sharma et al. (2023); Irvine et al. (2023).
- **Relational uncanny** — candidate new term; NOT yet claimed (§13 discipline): it must survive evidence and distinctness tests before naming. Currently it fails "is it observable/falsifiable distinctly?" until a perceptual experiment is run.

**Terms the paper must *avoid* inventing:** any synonym for memory, personalization, affinity, or believability. The only justified new object is the *relational state* with its guarantees — and even that must be positioned as the computationalization of what The Sims/Oz/affinity systems already encoded partially.

---

## 10. Candidate conceptual models

### Model A — "More meta" (Macha's F_in / F_in⊕F_meta)
**Status: rejected.** The notation (a) falsely implies the player has a strictly higher-order frame the NPC lacks (agents can trivially be given meta-prompts; players are not continuously meta-aware — half-real oscillation), (b) has no dynamics (no update rule, no persistence, no player-indexing), and (c) yields no predictions. Per the protocol's own rule — if F_in/F_meta is not a good theoretical expression, discard it — **it is discarded.**

### Model B — "Relationship = memory + affinity score"
**Status: rejected as insufficient, retained as the degenerate baseline.** A scalar score + event log captures continuity and a slice of contingency but has no *interpretation* (no theory of what an event means for the relationship), no *independence* (score doesn't drive the NPC's own goals), and no *expression* requirement. It cannot explain why Undertale's Flowey feels more real than an affinity bar, nor why Nemesis' taunts (displayed history) hit harder than a stored log. It is the null hypothesis the paper compares against.

### Model C — "The dyadic relational state" (adopted, candidate)
Let p = player, n = NPC, H = interaction history, x = current input, S = NPC's other state (beliefs/goals/values), B = behavior. Define the **relational state** R_t^n(p): a persistent, player-indexed, interpretive model of the relationship held by n, with:
- **Persistence** (R survives sessions and context resets) → *Continuity*;
- **Player-indexing** (R differs by player; identity is an argument, not a filter) → *Recognition*;
- **Update by interpreted events** (R_{t+1} = U(R_t, e_t), where e_t is a typed, *evaluated* interaction event — "this action meant X for us") → *Transformation / Contingency*;
- **Causal conditioning** (B = f(S, x, R): R shapes interpretation, not just recall) → the state *matters*;
- **Independence** (∃ behavior driven by S — n's own goals/values — not requested by p) → *Otherness / Self*;
- **Expression** (changes in R are *displayed* in B — referenced, enacted, performed) → *Visibility* (the player's only evidence);
- **Reciprocity** (B, via R, changes p's future actions — the loop closes; partly a design property: the relationship must *matter* mechanically).

Structural primitives: **Continuity, Contingency, Independence.** Enactment conditions: **Expression, Reciprocity.** The felt relationship = the player's sustained interpretation of the conjunction of all five. "Surprise" = emergent from Independence×Contingency under Expression; "perceive me" = Contingency on identity; "be changed by me" = Contingency over time. **This is the minimal model**; it survives the construct-validity objection (7 → 3+2) and explains the case pattern in §6.

**Key theoretical move (perceived vs. computational):** R is *not* claimed to be a real relationship. The claim is **conditional and testable**: *if* the player's projection is to be sustained across open-ended interaction, the artifact's behavior must be stably contingent on the player's history, and that stability requires an architectural guarantee — exactly as world-continuity requires a save file rather than the engine's goodwill. **"We do not trust the LLM to remember the world — we keep a save file. We should not trust it to remember the relationship — we need a relational save file."** This is the paper's sharpest sentence and its architectural bridge.

**Why capability doesn't substitute (mechanisms, all testable):**
1. **Wrong invariant:** agent research optimizes task competence and surface fluency; players detect *relational contingency* ("is this about me/us?"). Orthogonal invariants.
2. **Asymmetric error salience:** one continuity violation can collapse the illusion ("the spell broke") — bad is stronger than good (Baumeister et al. 2001); capability is blind to the illusion's fragility.
3. **Demonstration over storage:** players experience *displayed* history, not stored history — memory without expression is invisible ("it has memory but feels memoryless").
4. **Sycophancy as fake contingency:** models trained to please produce apparent responsiveness that is not player-contingent; the player's detector reads it as inauthentic intimacy — worse than none (relational uncanny).
5. **Fidelity trap:** high fluency raises expectations of relational fidelity; violation is disproportionately jarring.

---

## 11. Candidate novelty (honest inventory)

**Not new (must not claim):** players value characters with memory/continuity (game studies; Replika); believable ≠ intelligent (Oz/Bates 1994); relationship mechanics (The Sims, affinity systems, Ochs et al. 2009); relational agents (Bickmore & Picard 2005); memory for agents (Park et al. 2023); parasocial/attachment measurement (Horton & Wohl; Lewis et al. 2008).

**Intersection gap (the defensible claim):**
1. **Formal minimal model:** the 3+2 relational primitives as a *computational object*, unifying game-design knowledge (affinity, nemesis, supports) with agent architecture and player psychology — to our knowledge no existing work treats the player–NPC dyad this way for *open-ended generative agents*.
2. **Diagnosis + mechanism:** why capability scaling has weak, non-monotonic effects on perceived relationship (five mechanisms above), with the *relational uncanny* as a named (but not yet claimed) failure mode distinct from the perceptual uncanny valley.
3. **Guarantee-based reframing:** NPC frameworks should specify *what must be guaranteed about the relationship* (continuity, player-contingency, expression) rather than *what capabilities the model should have* — with the save-file analogy as the operational intuition.
4. **Evaluation protocol:** a controlled A/B/C/D comparison (capability vs. long-context vs. memory vs. relational structure) on validated perceived-relationship instruments — none exists in the LLM-NPC literature, which evaluates fluency, role-play accuracy, or task success.

**Honest risk:** items 3 and 4 could be framed as "applying Bickmore's relational-agent methodology to games with LLMs." The paper must foreground item 1 (the model) and item 2 (the mechanism) as the theoretical contribution, with 3–4 as consequences — otherwise it is an engineering demo.

---

## 12. Major risks (ranked)

1. **Novelty inflation / "Oz said it" rebuttal** — mitigated by honest framing: the contribution is the re-specification for open-ended agents + the minimal model + guarantees + measurement, not "believable agents matter."
2. **Measurement validity** — perceived-relationship scales are self-report; need behavioral triangulation (session persistence, return rate, gift-giving, save-scumming to preserve a relationship, modding), optional physiology; and the *confound* of content quality in any A/B/C/D comparison must be engineered out (matched dialogue quality, matched model family).
3. **The craft confound** — if all variance is explained by writing quality, the thesis is vacuous; the failure condition must be pre-registered.
4. **Cherry-picking cases** — the "alive"/"dead" case sets must be selected by pre-registered criteria, not post-hoc.
5. **Philosophy-of-mind scope creep** — the paper must bracket whether the NPC "really" has a relationship; intentional-stance framing only.
6. **Over-claiming the market** — companion-app scale shows demand, not that relational architecture monetizes.
7. **H4 overstatement** — H4 must be softened to the matched-surface-quality formulation or it is falsifiable-by-tautology.
8. **Term inflation** — "relational uncanny" and any new term must pass the §13 discipline (phenomenon → evidence → distinction → definition → name) or be dropped.

---

## 13. Unresolved questions

1. Does relationship require **stakes / the possibility of loss** (Tamagotchi's mortality, BG3 companion death, Nemesis killing you)? Can there be relationship without risk?
2. Is **player effort** load-bearing (ergodic work — Undertale's restraint, Nemesis' deaths, grinding confidants)? Does relationship need to be *earned*?
3. Is **fictionality** load-bearing (safe relationship — the "comfort" function)? DDLC's horror works by *violating* the safety of fiction; what does that imply for relational guarantees?
4. Is **voice/embodiment** required, or is text sufficient (text-only Undertale vs. voiced Hades)?
5. What is the **minimal expressive channel** for Expression (dialogue reference? world-state change? UI? social display by other NPCs — Nemesis' hierarchy)?
6. Does the relational state need to be **symmetric** (the NPC has a model of the player's model — recursive social cognition) or is a one-sided interpretive model sufficient for the experience?
7. **Cultural variation** in relational expectations (e.g., otome/visual-novel cultures vs. Western AAA) — is the model universal or segment-specific?
8. What is the correct **update rule** for R (event → interpretation)? OCC-style appraisal (Ochs et al. 2009), LLM-interpreted events, learned embeddings, or authored policies — and which is *guaranteeable*?
9. **Interplay with narrative control:** does a relational layer *serve* the drama manager or fight it (autonomy vs. authored beats)?
10. Does the paper's thesis survive the **"players don't care" segment** — what is the boundary condition?

---

## 14. Recommended thesis (derived from the above, not from Macha's brief)

> **There is a relational gap in NPC intelligence: as NPC behavior becomes open-ended (the LLM era), the perceived player–NPC relationship is determined not by agent capability but by a small set of structural conditions — continuity, player-contingency, independence, expression, and reciprocity — that current agent architectures do not compute or guarantee. We formalize these as a minimal model of the player–NPC dyad, show that the model predicts which existing systems feel "alive" and which feel "dead" (with the projection objection handled by reframing the artifact's function as sustaining the conditions of the player's relational interpretation), and derive the architectural consequence: NPC frameworks should guarantee a player-indexed, persistent, interpretive relational state — a "relational save file" — rather than merely scaling model capability. We specify the controlled experiments that could falsify this.**

This thesis: (a) names a real problem with a precise mechanism; (b) claims an intersection gap, not absolute novelty; (c) yields falsifiable predictions; (d) makes Macha (if it survives) a *derived* architectural consequence, not the paper's premise. If the controlled experiment shows that at matched surface quality, capability scaling moves perceived relationship as much as relational structure does, the thesis falls to the null hypothesis — and the paper will say so.

---

*End of Phase I Dossier. Next: Thesis Selection (Phase I.5), then the Full Paper (Phase II).*
