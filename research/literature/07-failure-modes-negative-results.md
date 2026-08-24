# 07 — Negative Results / Failure Modes (Synthetic Sweep)

Status: STORED (Batch 3 · Domain 7)
Serves paper claim: §10 pre-destroy our own variants; inoculate against standard attacks.
This dossier is the paper's self-attack layer — every naive Macha variant is killed here
before a reviewer can.

> Source discipline: claims carry provenance as `[dossier NN]` (internal) or `[URL]` (newly
> retrieved). `[CONTEXT]` = background. `[UNRESOLVED]` = open. Secondary/aggregator sources
> flagged `[RE-VERIFY]`.

## What must be known (hard questions)
1. Degeneration paths: scalarization / retrieval-ization / prompt-persona / randomness-impersonating-independence.
2. Ability-scaling worsens relational failure (fluency raises expectation → single violation more damaging).
3. Measurement false positives (report "feels real", invest behaviorally zero).
4. Cross-cutting attacks a reviewer would mount, and the strongest grounded defense.

## Findings

### 1. Degeneration paths

**1a. Scalarization (R as a single number)**
- Mechanism: reduce R to one float (`friendship = 0.73`).
- Why it fails: GAMA/BEN's relation is a structured tuple R_i,j(L, D, S, F, T) — multidimensional, not scalar [dossier 04]. A scalar strips commitment structure (no reason to act against short-term convenience), expectation state (what the NPC expects next), and salient history (a snapshot, not a trajectory) [dossier 01].
- **Minimal constraint:** R must be a typed tuple with commitment + expectation + salient history. Display scores are readouts, not decision state.

**1b. Retrieval-ization (faking via retrieval)**
- Mechanism: store interactions as a memory stream, retrieve relevant episodes at runtime.
- Why it fails: Generative Agents' relationships emerge as observed behavior with no commitment mechanism [dossier 04]. Ricoeur: being-remembered requires causal effectiveness, not exposition [dossier 06]. New evidence: TrustMem shows memory systems introduce omission/corruption/hallucination that become persistent system-state failures [<TrustMem, arXiv:2606.25161>](https://arxiv.org/abs/2606.25161); ID-RAG shows identity drift, ignoring established beliefs, hallucination propagation over long horizons [<ID-RAG, arXiv:2509.25299>](https://arxiv.org/abs/2509.25299). [RE-VERIFY: both are arXiv preprints]
- **Minimal constraint:** retrieval may populate short-term context, but durable R must feed back into belief revision, desire selection, intention reconsideration. If R doesn't affect planning, the system retrieves facts but does not remember relationally.

**1c. Prompt-persona (faking via system prompt)**
- Mechanism: prompt says "you remember the player"; no formal state update.
- Why it fails: appraisal must be a formal update, not prompting [dossier 01]; R must be first-class, not appended [dossier 04]. Each turn can be re-evaluated; prior interactions overwritten by recency/convenience.
- **Minimal constraint:** any claim of remembering/commitment/independent-will must be tied to a state-update function: R_{t+1} = f(R_t, event, beliefs, goals, social-context).

**1d. Randomness impersonating independence**
- Mechanism: stochastic output labeled "independent will."
- Why it fails: independence requires goals/constraints that can conflict with the player's script (Buber I-It, Levinas refusal) [dossier 06]; the intentional stance is abandoned when the system is erratically unreliable [dossier 05]. HRI's "Won't, Not Can't" refusal agent shows guarded independence is about refusing feasible requests from internal state, not pretending unpredictability is autonomy [dossier 03].
- **Minimal constraint:** independence = persistent goals/preferences/constraints that sometimes conflict with player input. Randomness is bounded noise around intentional behavior, not a substitute for will.

### 2. Ability-scaling worsens relational failure
- Mechanism: fluency raises expectations of coherence/memory/agency; once the player adopts the intentional stance, a history violation is a betrayal, not a bug. The **Violation-Expectation Paradox**: higher relational capability amplifies the cost of a single broken promise/forgotten fact/overwritten history.
- Evidence: intentional stance is abandonable on inconsistency [dossier 05]; Waltonian prop violation destroys make-believe [dossier 06]. New: Manhaes et al. (2025) define the "Quasi-Creature" and "Uncanny Valley of Agency" — superhuman fluency meets absurd failures in common-sense/consistency; highly agentic but erratically unreliable AI drops user comfort (N=37 "Move 78" study, negative correlation between perceived efficiency and frustration).
  [<Manhaes et al. 2025, arXiv:2508.18563>](https://arxiv.org/abs/2508.18563) [RE-VERIFY: preprint]
- **Design constraint:** Macha must prove higher fluency is paired with higher relational fidelity. If fluency rises but R is only retrieved/prompted, predict increased frustration after violations, not increased trust.

### 3. Measurement false positives
- Problem: players report "feels real" but invest behaviorally zero.
- Evidence: self-report validity weak for LLM agents (Zou et al. 2025) [dossier 02]; demand effects (Reeves & Nass) [dossier 02]; return-rate insufficiency (Bickmore variability paradox) [dossier 02]; anthropomorphism as mediator not causal primitive (Guingrich & Graziano) [dossier 02].
- **Strongest falsifiable prediction:** predict *decoupling under control, coupling under Macha R*. In a high-fluency control without durable R, return rate stays high while self-disclosure depth stays flat; under Macha R, return rate correlates with self-disclosure depth/frequency and session persistence after history-consistent interaction.

### 4. Cross-cutting attacks + grounded defenses

**4a. Projection objection** — "if it's all projection, computation guarantees nothing."
- Defense: Dennett's intentional stance as rational predictive strategy; NPC-Relational-Sufficiency: persistent R + causal feedback → treating the NPC as intentional is rational [dossier 06]. Not "the NPC has feelings" — weaker but design-stronger.

**4b. "No prior art" attack** — "R is just BDI beliefs / just memory."
- Defense: GAMA/BEN R_i,j is precedent, but no retrieved system lets R drive intention reconsideration/goal competition/long-horizon conflict [dossier 04]. R is not a belief (it's a commitment/expectation state entering goal competition); not just memory (memory can be retrieved without changing intent).

**4c. "Measurement failure" attack** — "claims are unfalsifiable."
- Defense: ablation + violation-injection design isolating ONE primitive with active control; DVs = return rate + session length + self-disclosure depth + relatability + anthropomorphism + attachment; triangulate survey/behavioral/linguistic; predict rupture patterns distinguishable from engagement loss [dossier 02].

**4d. "Façade already failed" attack** — "Macha is Façade with LLMs."
- Defense: the supported lesson is dramatic meaning + social-state communication were the bottleneck, NOT NLU [dossier 05]. Macha's R is designed to be legible as a first-class object, not hidden in internal character states; reparative play makes repair possible (not guaranteed) [dossier 05].

**4e. "HRI already did it" attack** — "companion systems exist."
- Defense: HRI evidence is health/home-robot contexts, not game NPCs; effects weaken without sustained continuity design; bonding is ethically contested [dossier 03]. Macha extends relational state into game narrative, dramatic legibility, player-driven fiction — not repeating HRI.

## Variant pre-destruction matrix
| Naive variant | Minimal design constraint | Evidence |
|---|---|---|
| Scalar R | typed tuple (commitment/expectation/salient history); scores = readouts only | 01, 04 |
| Retrieval R | durable R feeds back into belief revision/desire selection/intention reconsideration | 04, 06; TrustMem, ID-RAG |
| Prompt R | formal update function R_{t+1} = f(R_t, event, beliefs, goals, context) | 01, 04 |
| Random R | independence = conflicting goals/preferences; randomness = bounded noise | 03, 05, 06 |

## Falsifiable predictions (pre-commitment)
1. **R-retention:** Macha-R NPC shows higher self-disclosure depth + longer return persistence after a minor history violation than a fluency/retrieval-matched control without first-class R.
2. **Return-rate decoupling:** high-fluency control keeps return rate high while self-disclosure depth stays flat; under Macha R, return rate correlates with self-disclosure depth.
3. **Fluency-expectation:** if fluency rises without relational fidelity, frustration/stance-abandonment increases; under Macha R, higher fluency yields higher satisfaction or a sharper-but-repairable rupture.
4. **R-as-control:** manipulating R changes action selection, not just dialogue style (high-R condition → more defensive/protective actions in a game crisis).
5. **Projection boundedness:** when player actions consistently contradict established relational history, the NPC eventually refuses/resists/reinterprets rather than always accommodating.

## Bibliography (new sources)
1. Manhaes, Miller & Schroeder, "The Quasi-Creature and the Uncanny Valley of Agency" (2025). https://arxiv.org/abs/2508.18563 [RE-VERIFY: preprint]
2. Platnick et al., "ID-RAG: Identity Retrieval-Augmented Generation for Long-Horizon Persona Coherence" (2025). https://arxiv.org/abs/2509.25299 [RE-VERIFY: preprint]
3. Yang et al., "TrustMem: Learning Trustworthy Memory Consolidation for LLM Agents" (2026). https://arxiv.org/abs/2606.25161 [RE-VERIFY: preprint]
4. "Artificial Intimacy: Companion AI and Risks to Adolescent Mental Health" (Stanford report coverage). https://pdfs.semanticscholar.org/7fcb/e512e4fd16f3a10e755b2e63087efcab32ae.pdf [RE-VERIFY: locate primary Stanford report]
5. "How AI and Human Behaviors Shape Psychosocial Effects of Chatbot Use" (2025). https://ar5iv.labs.arxiv.org/html/2503.17473 [RE-VERIFY]
6. "Illusions of Intimacy: Emotional Attachment and Psychological Risks in Human-AI Relationships" (2025). https://www.rivista.ai/wp-content/uploads/2025/08/2505.11649v3.pdf [RE-VERIFY]
7. "The Rise of AI Companions: How Human-Chatbot Relationships Influence Well-Being" (2025). https://arxiv.org/html/2506.12605v2 [RE-VERIFY]
8. "Effects of Empathetic Responses, Agent Identity, and Gender Match on Self-Disclosure of Depression" (IJHCI 2026). https://www.tandfonline.com/doi/full/10.1080/10447318.2026.2692012 [RE-VERIFY]

## Open questions
1. Can Macha's R be validated without self-report bias? (violation-injection + behavioral/linguistic/longitudinal) [dossier 02]
2. Minimum fidelity for the intentional stance — how much predictive/memory-driven/refusal-capable behavior suffices without claiming inner life [dossier 06].
3. How to separate factual from relational memory computationally [dossier 06].
4. How to avoid dark patterns in relational refusal — trust repair can increase unquestioning compliance; refusal must be visible/bounded/ethical [dossier 03].
5. End-of-life / offboarding design for persistent NPCs — companion attachment persists after retirement [dossier 03].
6. How to handle the "I want it to be real" demand effect [dossier 02].
7. Causal evidence that R, not fluency, drives attachment — hold fluency constant, manipulate R [dossier 02, 04].
