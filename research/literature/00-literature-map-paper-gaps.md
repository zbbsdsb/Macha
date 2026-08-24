# Literature Map → Paper-Gap Mapping

Status: STORED (Synthesis of dossiers 01–07)
Purpose: the single map that turns seven dossiers into load-bearing material for the paper —
which claim each dossier supports, what the literature already proves, and where Macha's
original contribution must live.

> Every claim below is grounded in a dossier (`[dossier NN]`) or the paper body
> (`[paper §2.x]`). This is a synthesis document, not new evidence.

---

## 1. The map: dossier → paper claim

| Dossier | Paper claim / section it serves | What it proves (load-bearing) | What it leaves OPEN (Macha's gap) |
|---|---|---|---|
| **01** Formal models | §6 computational model (3+2 primitives → provable objects) | Typed relational state space exists (Westermann & Banisch); event→state coupling has type-theoretic machinery (Kovalev & Angiuli, DEKL); OCC/CPM appraisal is formalizable (Adam/Herzig/Longin); bounded ToM has finite nested-belief filtering (Zettlemoyer); invariant method (Noether) is portable | No ready-made social-relation dependent-type family; no verified CPM equation set; no peer-reviewed *social* symmetry — the invariant is ours to derive |
| **02** Longitudinal measurement | §9 falsifiability | Self-report validity is weak for LLM agents (Zou); demand effects (Reeves & Nass); return-rate ≠ relational depth (Bickmore paradox); strongest windows are quasi-experimental (Aalto 2yr, Replika update); violation-injection + triangulation is the viable design | No controlled longitudinal study manipulating agent primitives over months; "I want it to be real" unmeasured; rupture/rebound not operationalized in open-ended games |
| **03** HRI tradition | Gap positioning (extend 20yr HRI line) | Long-term engagement (Bickmore series); trust repair (Goo 2025); refusal/independence (Won't-Not-Can't); ethics (Cagiltay) — all verified | HRI evidence is health/home-robot contexts, not game NPCs; effects weaken without continuity design; some sources in RE-VERIFY tier |
| **04** BDI + modern agent arch | §6 R↔S coexistence | BDI/SOAR/ACT-R state+competition machinery is precise (de Silva, Laird, ACT-R utility); GAMA/BEN R_i,j is a formal relational tuple; generative-agent memory fakes continuity (Park, MemGPT, MemoryOS); drama managers control via beats/tension, never via R (Façade, Riedl & Young) | NO system lets R drive intention reconsideration / goal competition / long-horizon conflict; no drama manager uses R as control variable — **this is Macha's architectural slot** |
| **05** Game studies | §7 transferable formal properties | Half-real legitimizes rule-governed relation (Juul); agency is interpretive (Wardrip-Fruin, FDG 2010); intentional stance is abandonable on inconsistency; Façade's bottleneck was social-state communication, NOT NLU (supported correction); reparative play invites repair (Grinblat) | No formal properties extracted from cases; no evidence on history-violation vs underperformance; tabletop/RPG co-maintenance unretrieved |
| **06** Philosophy | §8 kill the projection objection | Intentional stance = predictive utility, not inner life (SEP); being-seen (Sartre look), being-remembered (Ricoeur narrative identity), being-changed (Buber I-It, Levinas refusal) each have a computational correlate AND a destroyer; Waltonian props + Iser blanks frame the generative limit | Whether computation can satisfy Levinas's face; minimum fidelity for the stance; factual vs relational memory distinction |
| **07** Failure modes | §10 self-attack / inoculation | Four degeneration paths (scalar/retrieval/prompt/random) each have a minimal design constraint; ability-scaling worsens relational failure (Uncanny Valley of Agency); measurement false positives have a falsifiable decoupling prediction; five cross-cutting attacks each have a grounded defense | Validation without self-report bias; dark-pattern avoidance in refusal; NPC lifecycle/offboarding design |

---

## 2. What the literature already proves (Macha can stand on this)

1. **A relational state CAN be a formal object.** GAMA/BEN's R_i,j(L,D,S,F,T) and Westermann & Banisch's state-space trajectories prove the concept is not hand-waving [dossier 01, 04].
2. **Appraisal can be computed, not prompted.** OCC → modal logic (Adam/Herzig/Longin) gives a pattern-matchable update layer [dossier 01].
3. **Bounded intersubjectivity has a finite representation.** Zettlemoyer/Milch/Kaelbling's nested-belief filtering answers "how is I-know-you-know-I-know maintained under bounded memory" [dossier 01].
4. **Self-report alone cannot validate relational claims.** The measurement literature is unanimous on this [dossier 02].
5. **Façade's lesson is dramatic meaning, not NLU.** This corrects a common misreading and supports Macha's relational framing [dossier 05].
6. **The projection objection has a defensible answer.** NPC-Relational-Sufficiency: persistent R + causal feedback → intentional stance is rational [dossier 06].
7. **Every naive Macha variant has a known death.** Scalar/retrieval/prompt/random all degenerate in documented ways [dossier 07].

## 3. Where Macha's original contribution MUST live (the gaps)

**Gap A — R as decision-relevant, not stored.** No retrieved system lets relational state drive intention reconsideration, goal competition, or long-horizon conflict [dossier 04]. This is the architectural spine: R is a control variable, not a memory field.

**Gap B — R as the drama manager's control variable.** Drama managers control via beats/tension/believability; none uses seen/remembered/independent-will as the control variable [dossier 04]. This is the design-theory spine.

**Gap C — The relational invariant.** No peer-reviewed *social* symmetry exists; the Noether-style invariant must be derived by Macha, not borrowed [dossier 01].

**Gap D — Transferable formal properties from cases.** Game studies has rich cases but no formal properties extracted; Macha's 3+2 primitives are the candidate [dossier 05].

**Gap E — Falsifiable relational measurement.** No controlled longitudinal study manipulates agent primitives over months; Macha's violation-injection + decoupling prediction is the contribution [dossier 02, 07].

**Gap F — The generative-fictionality limit.** Why a book survives on blanks but a generative NPC dies on history violation is framed but not formalized [dossier 06]; Macha can formalize it as a prop-consistency constraint.

## 4. Paper-section implications (draft)

- **§2 Field Superposition** (existing) — unchanged; answers "why fake" (perspective). Dossier 05's half-real supports the rule/fiction framing.
- **§6 Computational model** — built on dossiers 01 + 04: typed R (Gap A), appraisal as formal update, bounded ToM, R↔S coexistence, R-as-drama-control (Gap B).
- **§7 Case → formal properties** — built on dossier 05: intentional-stance consistency as a testable property (Gap D).
- **§8 Projection objection** — built on dossier 06: NPC-Relational-Sufficiency + the three correlates/destroyers (being-seen/remembered/changed).
- **§9 Falsifiability** — built on dossier 02 + 07: violation-injection design, decoupling prediction, five falsifiable predictions.
- **§10 Self-attack** — built on dossier 07: variant pre-destruction matrix + cross-cutting defenses.

## 5. Next steps (what needs team discussion)

1. **Resolve RE-VERIFY tiers** in dossiers 03, 05, 06, 07 (secondary/aggregator sources → primary). Highest priority: 03's placeholder DOIs; 05's Semantic Scholar/ResearchGate records; 06's gradesaver/cliffsnotes replacements.
2. **Decide Gap A vs Gap B priority** — is the paper's spine the architecture (R as control variable) or the design theory (R as drama control)? The question tree's 岔路 1 (idea vs framework) decides this.
3. **Derive the relational invariant (Gap C)** — a formal hypothesis to prove, not borrow.
4. **Design the falsifiable experiment (Gap E)** — one primitive, active control, violation-injection, decoupling prediction.
5. **Confirm the 3+2 primitives** against the four degeneration paths (dossier 07 matrix) before fixing the 四原型 (question tree 岔路 4).
