# 01 — Formal Models of Social Relations & Intersubjectivity

Status: STORED (Batch 1 · Domain 1)
Serves paper claim: §6 computational model — turn the 3+2 primitives (continuity / contingency /
independence + expression / reciprocity) into provable, comparable, computable objects.

> Source discipline: every claim below carries its retrieved source. `[CONTEXT]` = background,
> not usable as citation evidence. `[UNRESOLVED]` = question not fully answered.

## What must be known (hard questions)
1. Existing formal systems for dynamic social relation as structured state (kind/valence/commitment/expectation/salient history).
2. Type-theoretic / dependent-type treatment of event→relational-state update.
3. Computational appraisal theory (OCC, Scherer CPM) as an operational function.
4. Computational intersubjectivity / ToM under bounded memory.
5. Relational invariants that are maintained, not prompt-patched.

## Findings

### 1. Dynamic social relation as structured state
- **Westermann & Banisch (2024), "A Formal Model of Affiliative Interpersonality" (Clinical Psychological Science)** — models a relationship as a *state-space trajectory*, where the relational state space is the set of "ways of relating" and interaction drives trajectories within it. Dynamics derived from approach/avoidance motives of both interactants. Reports three qualitatively distinct attractor regimes: global stability (one attractor), bistability (two mutually exclusive attractors), and friendliness↔distance cycles.
  [<Westermann & Banisch 2024>](https://journals.sagepub.com/doi/10.1177/21677026241229663)
  - **Consume:** closest formal prototype for a *typed relational state space*; a relationship = point in that space, interaction = trajectory. Not yet a component-level type for each relation, and the full matrix update equations were not retrieved.
- **Mascarenhas, Marques, Campos & Paiva (2013), "A Model of Social Dynamics for Social Intelligent Agents" (AAAI FSS)** — Social Importance Dynamics (SID): augments BDI with social dynamics; built from SI *Attribution Rules*, *Conferrals*, *Claims* grounded in status-power theory.
  [<SID 2013>](https://cdn.aaai.org/ocs/7612/7612-32588-1-PB.pdf)
  - **Consume:** demonstrates insertion of a social dimension into a BDI agent with formally titled attribution rules; full predicate signature not fully legible in retrieved excerpt.
- **Ensemble / Scheherazade's Tavern (2020)** — game-implementation social simulation: NPCs carry relationship values (`friendship` = closeness, `respect` = how much NPC values another's opinion), `volitions` drive action selection.
  [CONTEXT — game arch, not peer-reviewed formal calculus; useful inspiration only]

### 2. Type-theoretic event→state coupling
- **Kovalev & Angiuli (2026), "A dependently-typed calculus of event telicity and culminativity" (Math. Structures in Computer Science)** — extends intensional MLTT; telic events typed so the undergoer type depends on event type; formalized in **Agda**.
  [<Kovalev & Angiuli 2026>](https://www.cambridge.org/core/journals/mathematical-structures-in-computer-science/article/dependentlytyped-calculus-of-event-telicity-and-culminativity/0C40346FC2A20D9B3A4F694618A7E0AE)
  - **Consume:** candidate type-theoretic layer where the *type of an update depends on the interpreted event*. Does not itself define social-relation types.
- **DEKL 2.0 (2026), "Trace-Indexed Knowledge Evolution in Dependent Type Theory" (arXiv:2604.22530v1)** — traces as first-class terms; knowledge as a presheaf over the finite-trace category; separates monotone proof theory from non-monotone knowledge dynamics; non-monotonicity characterized via non-surjective restriction maps.
  [<DEKL 2.0>](https://arxiv.org/html/2604.22530v1) — preprint; design-informing, not citation-grade for formal claims
  - **Consume:** provides trace-indexed, constructively-typed knowledge evolution — a candidate layer for relational-state revision with proof-checked witnesses.
- **Etas (2026), "An Effect-Typed Language for Agent Systems" (arXiv:2607.17780)** — types values via spec conformance; computations checked with escaping effect rows + a persistent abstraction of the typed action trace.
  [<Etas>](https://arxiv.org/html/2607.17780) — preprint
  - **Consume:** for *enforcing* relational invariants through effect/spec typing, though not a relational thesis itself.

### 3. Computational appraisal (OCC / Scherer CPM)
- **Ortony, Clore & Collins (1988), *The Cognitive Structure of Emotions*** — the OCC model: 22 emotion types; appraisal variables (desirability, likelihood, agent responsibility, goal relevance).
  [<OCC 1988>](https://www.semanticscholar.org/paper/Ortony-Clore-Collins-The-Cognitive-Structure-of-Emotions/4804e01b825d13c47a78d76f8e763d4c35278932)
  - **Consume:** target taxonomy to operationalize, not yet executable on its own.
- **Adam, Herzig & Longin (2009), "A logical formalization of the OCC theory of emotions" (Synthese 168:201–248)** — modal logic (Logic of Emotions) formalizing 20 of 22 OCC emotions, connecting to belief, goal, responsibility.
  [<Adam/Herzig/Longin 2009>](https://hal.science/hal-03474451/file/SYNTH1139_camera_ready_final__HAL_version_.pdf)
  - **Consume:** strongest bridge from appraisal-as-taxonomy to *logic we can pattern-match against*; emotion triggers coupled to belief/goal.
- **Adam, Herzig & Longin (2011), "A logic of emotions: from appraisal to coping"** — extends OCC toward *coping* (action selection); four emotion types given logical forms. Full formulas not fully retrieved. [partial]
- **Scherer (2009), "Emotions are emergent processes" (Phil. Trans. R. Soc. B 364:3247–3261)** — positions CPM; emotion as multi-component emergent process (appraisal→motivation→physiology→expression→feeling) needing a dynamic computational architecture.
  [<Scherer 2009>](https://pmc.ncbi.nlm.nih.gov/articles/PMC2781886/)
  - **Consume:** CPM is the correct multi-component spine; NOT a finished equation-level implementation — we must operationalize it ourselves.
- **AppraisalCloudPCT (2023, Comput. Intell. Neuroscience)** — OCC-based appraisal for social robots (autistic rehab); discretizes valence appraisal (e.g., praiseworthiness, familiarity, likelihood).
  - **Consume:** example of OCC appraisal variables → robot-emotion update; application-specific, not a general relational-state framework.
- **CPM-Grounded Appraisal Multi-Agent (2026, arXiv:2607.07824v1)** — dialogue persona system: multi-agent CPM-style pipeline (trigger→relevance→implication→coping-potential appraisal).
  - **Consume:** useful pipeline shape; but uses prompts/agents for appraisal checks — NOT a provable relational calculus. **[UNRESOLVED] whether any appraisal theory has a formally verified updating function**

### 4. Computational intersubjectivity / ToM under bounded memory
- **Baker, Saxe & Tenenbaum (2009), "Action Understanding as Inverse Planning" (Cognition)** — goal inference as Bayesian inverse planning over planned action.
  [<Baker 2009>](https://www.semanticscholar.org/paper/Action-understanding-as-inverse-planning.-Baker-Saxe/7dd51cef9bd43d495a12d10b7d0846f9bd60d9fa)
- **Baker, Jara-Ettinger, Saxe & Tenenbaum (2017), "Rational quantitative attribution of beliefs, desires and percepts in human mentalizing" (Nature Human Behaviour 1:0064)** — joint Bayesian inference of belief/desire/percept from movement.
  [<Baker 2017>](https://www.nature.com/articles/s41562-017-0064)
- **Baker, Saxe & Tenenbaum (2011), "Bayesian Theory of Mind" (CogSci)** — expresses belief-and-desire-dependent action as a **POMDP**; reconstructs joint belief state + reward via Bayesian inference.
  [<BToM 2011>](https://www.researchgate.net/publication/228727729_Bayesian_Theory_of_Mind_Modeling_Joint_Belief-Desire_Attribution)
- **Zettlemoyer, Milch & Kaelbling (2008), "Multi-Agent Filtering with Infinitely Nested Beliefs" (NIPS)** — formally defines infinite nested beliefs; gives a **finite representation** from which nested beliefs can be generated; updates exact in constant time in some cases, with an approximation scheme as complexity grows.
  [<Zettlemoyer/Milch/Kaelbling 2008>](https://people.csail.mit.edu/milch/papers/nips08filtering.pdf)
  - **Consume (key):** the strongest finite-context, bounded-memory ToM model — the direct answer to "how is I-know-you-know-I-know maintained/compressed under bounded memory." Caveat: assumes cooperative settings with commonly-known policies; extending to adversarial/partial-cooperation NPCs is our open problem.

### 5. Relational invariants / conservation-law formalisms
- **Noether's theorem** — every continuous symmetry of a system's action ↔ a conserved quantity. Sources found are lecture notes / PoC, not peer-reviewed social-agent invariants.
  [CONTEXT — general physics principle; principled analog only]
- **Noether-style agent PoC + "Formal Axiomatization of Emergent Laws (agent-based)" (preprint 2025)** — apply Lagrangian/symmetry reasoning to agent dynamics to derive conserved quantities (energy/momentum/strategy-diversity).
  [CONTEXT — preprint + PoC; NOT citation-grade for social relations]
  - **Consume:** the *method* (symmetry→conservation) is portable; but no peer-reviewed source identifies a continuous symmetry of *social* relation states. The invariant must be treated as a **formal hypothesis to derive**, not borrowed.

## Formal/operational takeaways for Macha
1. **Adopt a typed relational state space** (per Westermann & Banisch): relation = typed object (kind/valence/commitment/expectation/salient-history) occupying a point in a relataional space, dynamics = trajectory.
2. **Use event calculus + dependent typing for event→state coupling** (Kovalev & Angiuli for typing; DEKL for trace-indexing).
3. **Implement appraisal as a conditional inference function** — OCC variables (what), Adam/Herzig/Longin modal logic (how it maps to belief/goal), BToM POMDP (goal/belief inference). Appraisal = f(event, beliefs, goals, social-context) → updated valence/expectation/commitment, NOT prompting.
4. **Use finite nested belief filtering for bounded intersubjectivity** (Zettlemoyer/Milch/Kaelbling) as the bounded-memory ToM layer.
5. **Relational invariants must be derived from symmetry or trace-invariance** — treat as formal hypotheses to be proven, never prompt-patched.

## Pitfalls / avoid
- Don't cite game implementations (Ensemble) as formal theory.
- Don't overstate preprints (DEKL/Etas/Noether-agent).
- Don't treat CPM / OCC as already-executable — they're targets to operationalize.
- Don't conflate prompting with formal update rules (CPM-dialogue agent).

## Bibliography
Top sources retrieved (see inline links). Preprints flagged as such.

## Open questions
1. Exact relational state-space algebra + update equations of Westermann & Banisch need extraction from the full paper.
2. Full SID predicate signatures not readable from excerpt.
3. No ready-made social-relation dependent-type family exists — Macha must design relation-dependent event types and prove consistency.
4. No complete, verified CPM equation set; must be derived or formally implemented.
5. BToM requires our own POMDP observation/reward model + filtering step.
6. No peer-reviewed *social* symmetry — the relational invariant is an open theoretical derivation.
7. Zettlemoyer's model assumes cooperation; extending to adversarial/partial-cooperation NPCs is open.