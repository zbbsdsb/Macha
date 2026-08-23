# Thesis Selection
## Macha Directional Research — Phase I.5

**Status:** Draft for analyst review · **Date:** 2026-08-22
Three candidate theses, scored honestly, one selected. Each thesis is stated in its strongest form; weaknesses and likely reviewer objections are given equal weight.

---

## Thesis A — The Conservative / Empirical Thesis

> **Perceived player–NPC relationship is robustly explained by a small set of structural conditions — continuity, player-contingency, independence, expression, reciprocity — that are largely independent of agent capability at matched surface quality. We provide the model, a case-based test, and a measurement protocol.**

- **Novelty:** Low-to-moderate. Builds on Oz believability, Sims relationship mechanics, and parasocial measurement; the new part is the *minimal formal model* (3+2) and its use as an *independent variable* in evaluation.
- **Explanatory power:** High for the "alive but simple / dead but capable" contrast; moderate for the "why now."
- **Evidence:** Strong existing evidence (Nemesis, Sims, Undertale, Hades vs. AI-Dungeon/LLM-demos); no new experiments required to *argue*, though a validation study is implied.
- **Weaknesses:** Can be dismissed as "a taxonomy of things game designers already know"; no architectural claim means no clear engineering contribution; the projection objection is handled but the thesis doesn't *need* the relational-gap diagnosis to stand.
- **Falsifiability:** Good — the A/B/C/D experiment's null is crisp.
- **Likely reviewer objections:** "This is descriptive folk-theory formalized"; "the primitives are not operationalized tightly enough to be falsifiable in practice"; "why is this AI research rather than game design?"

## Thesis B — The Relational-Gap Thesis (recommended)

> **There is a relational gap in NPC intelligence: as NPC behavior becomes open-ended, the perceived player–NPC relationship is determined not by agent capability but by structural conditions current agent architectures neither compute nor guarantee (continuity, player-contingency, independence, expression, reciprocity). We formalize the minimal dyadic model, show it predicts which existing systems feel alive or dead, and derive the architectural consequence — a player-indexed, persistent, interpretive relational state ("a relational save file") that generative-NPC frameworks should guarantee. We specify the controlled experiments that could falsify this.**

- **Novelty:** Moderate — an *intersection gap* (agent architecture × game design × player psychology × HCI relational agents). Not "no one has said NPCs need relationships" but "no one has made the relationship a first-class computational object with guarantees for open-ended generative agents, and connected the four literatures under one model."
- **Explanatory power:** Highest. Explains (i) why simple systems feel alive, (ii) why capable systems feel dead, (iii) why scripted craft worked and why it cannot scale, (iv) why LLM companions plateau, (v) why the problem is *newly* visible and *newly* solvable.
- **Evidence:** Converging (design cases, industry reports, companion-market data, academic antecedents). The load-bearing new evidence is the planned controlled experiment.
- **Weaknesses:** (a) Risk of "Oz/Bickmore already said it" — mitigated only by the open-endedness argument and the guarantee framing; (b) the perceived-vs-computational distinction must be held rigorously or the paper collapses into projection theory; (c) requires an experiment to earn its keep.
- **Falsifiability:** Explicit — if at matched surface quality a capability-only condition (stronger model, longer context, RAG memory) moves perceived relationship as much as the relational condition, the thesis is wrong. Also each primitive has an ablation prediction.
- **Likely reviewer objections:** Objections 1–10 of the protocol, with 7 (script suffices) and 8 (projection) as the lethal pair. The paper's §Discussion must defeat both: 7 by the bounded/unbounded argument, 8 by the illusion-maintenance argument.

## Thesis C — The Radical / Agenda-Setting Thesis

> **Player–NPC relationship, not agent intelligence, should be the organizing principle of NPC frameworks: capability is a resource the relational layer spends, and relationship is the "save file" of social agents. NPC intelligence research should be re-founded on the relational dyad.**

- **Novelty:** High as an agenda claim; the field-level reframing ("invert the priority") is genuinely provocative.
- **Explanatory power:** Same as B plus a normative claim about research priorities.
- **Evidence:** Same as B; the normative claim adds no evidence.
- **Weaknesses:** The normative claim is unfalsifiable as stated ("should be the organizing principle"); it invites the "revolutionary/paradigm-shift" language the protocol forbids; reviewers will rightly demand to know what *breaks* under the old paradigm. It also over-reaches: capability plainly matters for the *content* of relationships.
- **Falsifiability:** The *descriptive* core is as falsifiable as B, but the *prescriptive* layer is not.
- **Likely reviewer objections:** "Overclaim"; "relational primacy is a design stance, not a scientific result"; "capability is entangled with relational quality (bad writing kills relationships) — the dichotomy is false"; "this reads as a manifesto, not a paper."

---

## Selection: **Thesis B**

Rationale: A is safe but not directional; C is directional but overclaims. B has the protocol's required profile — a real problem, a precise mechanism, an intersection gap, falsifiable predictions, and an architectural consequence that can be *derived* (Macha's role). B also satisfies the "Reviewer #2 test" in its strongest form: it claims to have found something previously unnamed — **that the missing computational object between AI agents and the relationships players expect is a guaranteed dyadic relational state, and that this is what separates "alive" from "dead" NPCs in the open-ended era** — not "NPCs should have memory/personality."

**Concessions locked in for the paper (per the protocol's honesty requirements):**
1. F_in / F_meta is discarded (dossier §10, Model A).
2. The seven-dimension taxonomy is reduced to 3 structural primitives + 2 enactment conditions (dossier §10, Model C).
3. Novelty is claimed as an intersection gap with explicit credit to Oz, Bickmore, The Sims, and Ochs et al.
4. The paper will not claim NPCs "have" relationships (perceived vs. computational, held rigorously).
5. H4 is softened to the matched-surface-quality formulation.
6. If the A/B/C/D experiment's null obtains, the thesis fails — stated in the paper.

---

*End of Thesis Selection. Proceeding to Phase II: Full Paper (Thesis B).*
