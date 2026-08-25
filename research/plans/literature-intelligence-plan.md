# Macha Literature Intelligence Plan

Status: **PROPOSED** — awaiting team calibration before dispatch.
Purpose: gather deep knowledge across 7 domains to make the paper a **top directional** work.

Goal of every domain: turn a currently-vague part of the paper into something that can
*prove*, *compare*, or *kill* a claim. Not "collect references" — collect **load-bearing
material** that a reviewer cannot dismiss.

---

## 0. Methodological Ground Rules

1. **Explore agents are read-only.** They search + synthesize + return structured findings.
   The orchestrator (main agent) writes the `research/literature/<NN>-<domain>.md` dossier.
   This enforces provenance discipline at the **write** layer, not the search layer.

2. **Source ledger discipline.** Every claim that could be *cited* carries inline provenance:
   `[<short name>](<stable URL>)`. Un-sourced assertions are tagged `[CONTEXT]` and are NOT
   usable as evidence by the paper. No fabricated URLs — only what the agent actually retrieved.

3. **Batching respects the ≤3-concurrent-Explore constraint.**
   - Batch 1 (highest priority): domains 1, 2, 3
   - Batch 2: domains 4, 5, 6
   - Batch 3: domain 7 (synthetic sweep over batches 1–2 outputs)

4. **Dossier output schema (each domain file) — mandatory sections:**
   ```
   <NN> <domain name>
   ## Reason this domain exists (which paper claim/quang it serves)
   ## What must be known (the 3–6 hard questions that must be answered)
   ## Findings (numbered; each = claim + optional source)
   ## Formal/operational takeaways (how Macha consumes this)
   ## Direct pitfalls / what to avoid
   ## Bibliography (all retrieved sources, stable URLs)
   ## Open questions (everything still unknown)
   ```
   The "Which paper claim it serves" line is mandatory — a domain with no mapped claim is cut.

5. **No half-satisfied questions.** Each hard question (section 2) must end the dossier either
   answered-with-source or explicitly marked `[UNRESOLVED: what is missing to answer it]`.
   Nothing dangles silently.

---

## 1. Domain → Paper-Claim Mapping (the spine)

| # | Domain | Paper claim / question it serves | Batch |
|---|---|---|---|
| 1 | Formal models of social relation / intersubjectivity | §6 computational model: turn 3+2 primitives into provable computational objects | 1 |
| 2 | Longitudinal human-agent relationship measurement | §9 falsifiability: make evaluation survive "measurement failure" | 1 |
| 3 | HRI / companion-system research tradition | Gap positioning: prove we extend 20yr HRI line, not reinvent it | 1 |
| 4 | BDI + modern agent-architecture structure | R↔S coexistence: where relational state fits / collides with cognitive arch | 2 |
| 5 | Game studies / interactive-narrative theory thickness | Move from "case collection" to transferable formal properties | 2 |
| 6 | Philosophy / phenomenology of perceived-vs-computed relation | Kill the sharpest objection: "if it's all projection, what does computation guarantee?" | 2 |
| 7 | Negative results / failure modes | Pre-destroy our own variants; inoculate against standard attacks | 3 |

---

## 2. Domain Definitions (the hard questions each agent MUST answer)

> Note: these are the questions, not the answers. The agent returns evidence per question;
> the dossier is written only when every question is answered-with-source or marked `[UNRESOLVED]`.

### 1 — Formal models of social relation & intersubjectivity
- What formal systems already exist for **dynamic social relation as a structured state**
  (kind / valence / commitment / expectation / salient history)? Names + the actual axioms/update rules.
- Is there a **type-theoretic / dependent-type** treatment of how "interpreted events" update
  relational state? Where is event→state coupling already formalized?
- What are the **computational versions of appraisal theory** (OCC, Scherer's CPM, recent
  computational appraisal)? Can any be written as an operational `appraisal` function today,
  and how does it couple to belief/goal update?
- Computational **intersubjectivity / ToM in finite context**: how is "I know that you know
  that I know" maintained, compressed, recovered under bounded memory? Concrete models.
- How have prior systems formalized a **relational invariant** that must be *maintained*, not
  patched by prompting? Any "conservation law"-style formalism?

### 2 — Longitudinal human-agent relationship measurement
- Psychological measurement core: **construct/validity/discriminant validity, measurement
  invariance, response bias** (esp. social desirability & "I want it to be real" demand effect) —
  how do these fail open-ended generative long-term contexts?
- **Longitudinal design & survival analysis**: how to model relationship as duration /
  rupture point / rebound-after-repair. Beyond Bickmore's month-scales.
- Behavior & implicit measures: beyond modding/save-scumming/gifting — language-style matching,
  response-latency patterns, physiology, qualitative-code triangulation.
- Measurement-theory loop: how to design **ablation & violation-injection** experiments so a
  missing primitive is attributable, not post-hoc explained.

### 3 — HRI / companion-system research tradition
- The 20-year **long-term human-robot relationship experiments** that actually ran for months:
  which, what they measured, what they concluded.
- **Continuity / repair / trust-breach-and-rebuild** computational + design models.
- How HRI architectures preserve **otherness / independence** (why robots must not be fully
  submissive). Concrete mechanism examples.
- **Ethics & dark patterns of companion systems** — documented side-effects of strengthening
  the bond; how an ethical boundary is set in the architecture.

### 4 — BDI + modern agent-architecture structure
- In SOAR / ACT-R / BDI: how is **state persistence + goal competition** handled? Where does a
  relational state fit as a first-class citizen vs. collide?
- Generative-agents / MemGPT-family / hierarchical memory+planning: their **real limits** — how
  they use retrieval to *fake* relationship, and where that faking necessarily breaks.
- **Drama manager / narrative planning interface**: how relational state becomes the drama
  manager's control variable rather than more generated text.

### 5 — Game studies / interactive-narrative theory
- **Half-real** (Juul), **agency redefinition** (Wardrip-Fruin), **intentional stance in games**.
- **Interpretation as the computational bottleneck** of interactive narrative — why Façade failed
  (not NLU, but that relational meaning couldn't be computed reliably).
- How players **actively maintain relationship illusion** (projection + repair); when system must
  cooperate vs. refuse.

### 6 — Philosophy / phenomenology of perceived-vs-computed relation
- The **other-minds problem in its artificial form**: not "can a machine have a mind", but
  "what behavioral consistency is enough to sustain the intentional stance".
- Phenomenology of **being-seen / being-remembered / being-changed**, and how tech objects
  destroy or sustain it.
- **Fictionality (Walton's make-believe, Iser's blanks)** in open generative systems — the limit:
  why a book survives on blanks but a generative NPC dies on violating history.

### 7 — Negative results / failure modes (synthetic sweep over batches 1–2)
- Degeneration paths: **scalarization** (reduce R to a number), **retrieval-ization** (fake via
  retrieval), **prompt-persona** (fake via prompting), **randomness impersonating independence**.
- **Ability-scaling worsens relational failure**: fluency raises expectation → a single violation
  is more damaging. Evidence/mechanism.
- **Measurement false positives**: players report "feels real" but invest behaviorally zero.

---

## 3. Dispatch & Storage

**Dispatch (per the ≤3-concurrent rule):**
- Batch 1 → domains 1, 2, 3 (three agents in parallel)
- Batch 2 → domains 4, 5, 6 (three agents in parallel)
- Batch 3 → domain 7 (one synthetic agent, given batches 1–2 dossiers + before writing)

**Storage mapping (where each dossier lands):**
- Every dossier → `research/literature/<NN>-<domain>.md`
- Batches 1–2 dossiers → marked `STORED` in `papers/notes/paper-status.md reinforce link`
- Any newly-collected primary PDFs we want to keep → `reference/` under the A-rule:
  provenance + `papers/notes/papers/<id>.md` companion, per `docs/team-workflow.md` §A.

**Reuse pipeline (not just archive):** batch-3 (domain 7) reads batches 1–2 before writing;
the final synthesis doc integrates all seven into a "literature-map → paper-gap" file.