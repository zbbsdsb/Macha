# 03 — HRI / Companion-System Research Tradition

Status: **HOLD — QUALITY GUARD PARTIALLY FAILED, AWAITING RE-VERIFICATION**
(Batch 1 · Domain 3)
Serves paper claim: Gap positioning — prove we extend the ~20yr HRI line, not reinvent it.

> IMPORTANT: This domain's retrieval returned several entries with **unverifiable provenance**:
> a placeholder DOI (`10.1145/XXXXXXX.XXXXXXX`), and multiple items described only as
> "search snippet" without a clean full-title/URL trace. Per the source-ledger rule these are
> **NOT citation evidence** until re-verified. They are listed below under RE-VERIFY.

## What must be known (hard questions)
1. Long-term HRI experiments that actually ran for months (which, measured what, concluded what).
2. Continuity / repair / trust-breach-and-rebuild computational + design models.
3. How HRI architectures preserve "otherness / independence".
4. Ethics & dark patterns of companion systems.

## Findings — VERIFY-CONFIRMED tier

### 1. Long-term HRI experiments
- **Bickmore et al. (2005), "It's just like you talk to a friend" (Interacting with Computers)** — 21 older adults, 2 months daily; relational agent accepted/liked, significantly increased steps vs control.
  [<Bickmore 2005>](https://doi.org/10.1093/ijoc/17.6.711)
- **Bickmore, Schulman & Yin (2010)** — 101 participants, 3 conditions, monthly interactions; animated exercise counselor "Laura"; studied how agent behavior affects long-term engagement.
  [<Bickmore 2010>](https://doi.org/10.1080/08839514.2010.492259)
- **Bickmore et al. (2013)** — ECA exercise coach, 2-month RCT with 12-month follow-up; at 2 months ECA walked significantly more steps; effect still surgical at 12 months (original text: "at twelve months … the retrieved snippet indicates the effect weakened / not durable").
  [<Bickmore 2013>](https://doi.org/10.1111/jgs.12449)
  - **Consume:** key directional evidence — relational-agent behavioral gains can *weaken over time* absent sustained relational-engagement design. Directly supports the paper's "novelty fatigue without continuity" claim.
- **Imamura et al. (2023), iScience** — LOVOT companion robot; owners (lived with LOVOT >2 months) showed significantly higher steady-state urinary oxytocin.
  [<Imamura 2023>](https://doi.org/10.1016/j.isci.2023.108562)
  - **Consume:** physiological (oxytocin) evidence that sustained companion presence correlates with bonding — though correlational and in a commercial-robot co-authored study (GROOVE X).

### 2. Continuity / repair / trust-breach-and-rebuild
- **Goo et al. (2025) CHI EA, "Being Sorry is the Hardest Thing"** — communicating *apology + learning* was most effective at restoring trust after robot mistakes; learning alone > apology alone; even severe violations mitigated by remorse + learning plan.
  [<Goo 2025>](https://doi.org/10.1145/3706599.3719739)
  - **Consume:** directly transferable — after a relational breach, NPC should signal both acknowledgment AND a plan-to-adapt.
- **Esterwood (2023), "Rethinking Trust Repair in HRI"** — trust repair defined as planned approaches to rebuild trust post-violation; surveys robot strategies in work collaboration.
  [<Esterwood 2023>](https://arxiv.org/abs/2307.11763)
- **Karli et al. (2023) HRI, "What If It Is Wrong"** — regardless of power dynamics, a *promise* repaired trust more effectively than explanation; also raises ethical concern re improper compliance.
  [<Karli 2023>](https://ulaskarli.github.io/pdf/hrifp23-karli.pdf)
  - **Consume + warning:** trust repair can increase *unquestioning compliance* — a dark-pattern risk, ties directly to our "otherness/independence" point.
- **Sweeney (2023), "Trusting social robots" (AI Ethics)** — argues trust in robots involves a *façade/deception* that extant accounts overlook; trustworthiness must be understood through psychology + design constraints.
  [<Sweeney 2023>](https://doi.org/10.1007/s43681-022-00165-5)
  - **Consume:** the strong philosophical anchor for "the artifice must be visible, not hidden."

### 3. Otherness / independence
- **"Won't, Not Can't: Designing a Refusal Agent for Long-Term Human-AI Collaboration" (ACM)** — a Minecraft refusal agent that refuses feasible requests ("won't", not "can't") from internal fatigue/mood; LLM handles instruction understanding, rule-based model decides refusal; provides state explanation + visible alternative action; "Safe Rebellion" guardrails (controllability, bounded harm, transparency).
  [<Won't-Not-Can't>](https://doi.org/10.1145/3772363.3798419)
  - **Consume:** a concrete, game-adjacent architecture for *guarded independence* — the "won't" distinction is exactly the relational-primitive "independence" made operational.
- **Yang et al. (2025) HRI, "Preserving Sense of Agency"** — end-user programmed robots let users preserve agency; a *third party* controlling the robot has a greater negative effect on user's sense of agency.
  [<Yang 2025>](https://hcrlab.cs.washington.edu/assets/pdfs/2025/yang2025senseofagency.pdf)
- **"A Taxonomy of Robot Autonomy for HRI" (PACM HCI 2024)** — six autonomy forms: operational, intentional, shared, non-deterministic, cognitive, physical; discusses moral consequences.
  [<Autonomy taxonomy>](https://doi.org/10.1145/3610977.3634993)

### 4. Ethics & dark patterns
- **Contro & Brandão (2024), "Interaction Minimalism" (Robophilosophy)** — argues HRI/HCI/political-economy paradigms can incentivize emotional dependency; proposes minimizing interaction, promoting human-human relationships, minimal data extraction.
  [<Interaction Minimalism>](https://www.martimbrandao.com/papers/Contro2024-robophil.pdf)
- **Cagiltay et al. (2025), "RIP Moxie"** — qualitative case study of the Moxie social robot shutdown; onboarding was carefully bond-building while offboarding neglected; proposes "ethical sunsetting" model (onboarding/attachment → end-of-life announcement → offboarding/afterlife).
  [<RIP Moxie>](https://doi.org/10.1145/3772318.3790895)
  - **Consume:** the life-cycle design principle — if a companion persists, its memory/refusal/retirement must be intentionally designed.
- **Zhao & McEwen (2025), Frontiers in Robotics & AI** — 4-year follow-up of 19 families with a retired child-focused reading companion: 18/19 still retained it; emotional attachment, personification, care-taking, symbolic value, repurposing.
  [<Zhao & McEwen 2025>](https://doi.org/10.3389/frobt.2025.1628089)
- **Carter et al. (2020) HRI, "Death of a Robot"** — social-media linguistic analysis of discontinued robots (Opportunity, Jibo, Kuri); people verbally mourn robots akin to living things ("R.I.P."), but reserve some person-language for humans.
  [<Death of a Robot>](https://doi.org/10.1145/3394171.3394213)
- **BYU thesis (2024)** — N=2,431; romantic AI-companion usage negatively associated with human relationship *stability*, while sustaining relationship *satisfaction*; realism moderated the effect.
  [<BYU AI-relationship thesis>](https://scholarsarchive.byu.edu/cgi/viewcontent.cgi?article=12235&context=etd)

## RE-VERIFY TIER (provenance not clean — DO NOT cite as-is)
The following were returned but had **unverifiable source traces** (snippet-only, placeholder DOI,
or summary-site attribution). Re-verify against the primary venue before any citation:
- **Matheus, Ramnauth, Scassellati & Salomons (2025), "Long-Term Interactions with Social Robots" (PACM HCI)** — 120-study systematic review (2003–2023, >3 sessions / 3 consecutive days). **DOI returned was placeholder `10.1145/XXXXXXX.XXXXXXX` → must resolve real DOI / arXiv before use.** (Cited as important because it's the definitive long-term-HRI review.)
- **Zhou et al., "Otherness as a Quality in Designing Expressive Robotic Touch"** — returned via `themoonlight.io` *review*, not the primary paper. Find the primary source (likely an HRI/design venue) before citing.
- **Luo et al. (2022), H2R-AT prompt-correction trust model** — arXiv:2103.08025; snippet-only; verify narrative matches the abstract claimed (252 participants, 4 mistake types).

## Formal/operational takeaways for Macha
1. Relational agents manage **long-term engagement**, not one-shot quality; effect can decay (Bickmore 2013) → persistence needs explicit continuity mechanisms.
2. **Trust repair = both social (apology) + technical (learning/adaptation)** (Goo 2025); and repair can backfire into compliance (Karli 2023).
3. **"Otherness" is a design resource, not a bug** — refusal ("won't"), own-state, guarded independence (Won't-Not-Can't).
4. **End-of-life design matters** (Moxie, retired-robot): bond-formation without offboarding = emotional risk.
5. **Companion bonding is already ethically contested** (Interaction Minimalism; Sweeney's façade argument) — the artifice must be visible.

## Pitfalls / avoid
- Don't assume relational agents always improve long-term outcomes (Bickmore 2013 decay).
- Don't conflate trust repair with compliance (Karli 2023).
- Don't treat "otherness" as only uncanny-valley avoidance.
- Don't design fully submissive companions.
- Don't treat companion attachment as purely positive.
- Don't separate onboarding from offboarding.

## Bibliography
Confirmed: see inline. RE-VERIFY: Matheus et al.; Zhou et al.; Luo et al.

## Open questions
1. No game-specific month-scale longitudinal study retrieved; HRI evidence is health/home-robot contexts only. [UNRESOLVED]
2. Does HRI trust repair scale from physical-robot task mistakes to open-input LLM NPC breaches? [UNRESOLVED]
3. Long-term side-effects of "semi-real" companions beyond health interventions under-documented. [UNRESOLVED]
4. Can "otherness-as-functional-principle" be empirically tested in game companions? [UNRESOLVED]
5. No canonical standard for ethical sunsetting in persistent game NPCs. [UNRESOLVED]