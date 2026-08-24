# 02 — Longitudinal Human-Agent Relationship Measurement

Status: STORED (Batch 1 · Domain 2)
Serves paper claim: §9 falsifiability — evaluation must survive "measurement failure"; a
directional paper must predict how measurement will fail, and design ablation/violation
experiments that can kill or confirm claims.

> Source discipline: claims carry retrieved sources. `[CONTEXT]` = background, not citation
> evidence. `[UNRESOLVED]` = question not fully answered.

## What must be known (hard questions)
1. Psychometric core: construct/discriminant validity, measurement invariance, response bias — how they fail in open-ended generative long-term contexts.
2. Longitudinal design & survival analysis beyond Bickmore month-scales.
3. Behavioral & implicit measures (language-style matching, latency, physiology, triangulation).
4. Ablation & violation-injection design for causal attribution.

## Findings

### 1. Psychometric core failures
- **Self-report validity is weak for LLM agents.** Zou et al. (COLM 2025) built 500 LLM chatbots with distinct personality designs; self-report scores aligned only weakly with human-perceived personality and weakly with human-rated interaction quality — i.e., poor criterion + predictive validity.
  [<Zou et al. 2025>](https://arxiv.org/abs/2412.00207)
  - **Consume:** self-report alone cannot confirm a primitive produces its intended relational effect.
- **Discriminant validity is weak across PSI/PSR/anthropomorphism.** PP-SS work shows parasocial scales correlate strongly with theoretically-relevant criteria but remain distinct from EPSI; tools may tap overlapping constructs rather than cleanly separating "social presence" / "narrative engagement" / "mind attribution".
  [<PP-SS>](https://www.tandfonline.com/doi/pdf/10.1080/15213269.2026.2621710) [<PRISM invariance>](https://journals.plos.org/plosone/article/file?id=10.1371%2Fjournal.pone.0300356&type=printable)
- **Measurement invariance is unestablished for long-term generative contexts.** Existing invariance evidence is cross-platform (PRISM) or narrow cross-sectional (CEIA, emotional trust in AI, metric/partial scalar invariance by gender).
  [<CEIA>](https://www.frontiersin.org/journals/psychology/articles/10.3389/fpsyg.2026.1755160/full)
  - Mechanism: if an LLM's output depends on conversation history, early/mid/late measurements may be non-comparable even with unchanged design. PTCBench (39,240 personality records, 12 contexts) shows external scenarios trigger significant LLM personality shifts; conversation-history effects increase self-report variability.
  [<PTCBench>](https://arxiv.org/abs/2602.00016) [<AAAI personality instability>](https://ojs.aaai.org/index.php/AAAI/article/download/41133/45094)
- **Response bias is the most important unmeasured threat.** Reeves & Nass (CHI 1996) "Computers are Social Actors": people apply social rules to computers; media-politeness test — participants rated a self-praising computer more positively, especially on the same computer.
  [<Reeves & Nass 1996>](https://dl.acm.org/doi/pdf/10.1145/191666.191703)
  - "I want it to be real" is best modeled as a demand/expectation effect (not a formally named construct in retrieved evidence). LLM social-desirability research shows LLMs skew toward desirable trait ends when evaluation context is inferred; desirability-matched graded forced-choice formats can reduce socially desirable responding.
  [<LLM SDR>](https://arxiv.org/abs/2602.17262)
  - **[UNRESOLVED] the specific player-to-agent "I want it to be real" mechanism has not been tested in open-ended generative-agent studies.**

### 2. Longitudinal design & survival analysis
- **Bickmore, Schulman & Yin (2010)** — 24-month virtual lab, 51 older adults, 10,000+ conversations with animated exercise counselor; agent-behavior *variability* increased engagement/desire-to-continue but did NOT increase exercise (participants walked less with more variability).
  [<Bickmore 2010>](https://www.tandfonline.com/doi/10.1080/08839514.2010.492259)
- **Guingrich & Graziano (2025)** — 21-day longitudinal RCT, N=183, companion chatbot vs text-word-game control; no significant overall impact on social health/relationships; anthropomorphism *mediated* perceived impacts; desire-to-socially-connect predicted anthropomorphism.
  [<Guingrich & Graziano 2025>](https://arxiv.org/abs/2509.19515)
- **Observational long-window studies (the strongest empirical windows):**
  - **De Freitas et al. (HBS WP 25-018)** — Replika app-update (removal of erotic role-play) as natural experiment: users reported feeling closer to the AI than to their best human friend; the update triggered mourning, mental-health deterioration, negative welfare outcomes. *Identity discontinuity*.
    [<De Freitas et al.>](https://www.hbs.edu/ris/Publication%20Files/25-018_bed5c516-fa31-4216-b53d-50fedda064b1.pdf)
  - **Aalto University (CHI 2026)** — ~2,000 active Replika Reddit users over 2 years (quasi-experimental + 18 interviews): short-term comfort, but long-term use coincided with more loneliness/depression/suicidal-thought signals in language; users sometimes stopped reaching out to humans.
    [<Aalto CHI 2026>](https://www.aalto.fi/en/news/ai-companions-can-comfort-lonely-users-but-may-deepen-distress-over-time)
  - **Pi & Hunter (IJHCI)** — structured survey of longitudinal social-AI companion studies; cites Lopez Torres' 12-month Replika analysis (authenticity is dynamic, shaped by shared history; high emotional investment → vulnerability to change).
    [<Pi & Hunter>](https://www.tandfonline.com/doi/pdf/10.1080/10447318.2026.2670529)
- **No survival-analysis framework for agent relationships exists.** Closest analogue: rupture/repair in therapy — Eubanks-Carter et al. describe V-shaped alliance shifts (high→low→high) after rupture+repair.
  [<V-Episodes alliance>](https://scholars.mssm.edu/en/publications/v-episodes-in-the-alliance-a-single-case-application-of-multiple-)
  - **Consume:** operationalize rupture as a drop in return rate / self-disclosure / perceived relatability after a specific agent behavior; rebound as recovery after a repair event. **[UNRESOLVED] no controlled longitudinal study measures return + dialogue quality + self-disclosure + attachment + anthropomorphism while manipulating agent primitives over months.**

### 3. Behavioral & implicit measures
- **Language-style matching (LSM):** mixed evidence. One line: LSM in groups reflects coordination but is unrelated to rated interaction quality (participants + judges). Another: style-matched chatbots → higher communication satisfaction (p<.001). Agents adapt more than users, esp. in individualistic cultures.
  [<LSM groups>](https://www.researchgate.net/publication/358643594_Capturing_the_Temporal_Dynamics_of_Language_Style_Matching_in_Groups_and_Teams) [<accommodation AAAI>](https://ojs.aaai.org/index.php/AAAI/article/download/35241/37396)
  - **[UNRESOLVED] no evidence LSM alone predicts attachment/relatability in game agents.**
- **Response latency:** no retrieved source shows latency alone is a validated relational indicator. High responsiveness without relatability is a known failure mode. [CONTEXT]
- **Physiology/EEG:** emerging but correlational. IEEE TAC study (contextual human-AI interaction) used Relative Sensorimotor Rhythm / Relative Alpha as correlational indicators; perceived affective alignment predicted contextual fit + reuse intention. Social-presence work shows presence mitigates distrust but no isolated physiological signal.
  [<IEEE TAC EEG>](https://www.computer.org/csdl/journal/ta/2026/01/11278705/2cjDRF2jxOU) [<social presence trust>](https://www.nature.com/articles/s41598-023-44354-6)
  - **Consume:** EEG/affective alignment = correlational, NOT causal; cannot stand alone.
- **Qualitative triangulation:** strongest examples are the Aalto (Reddit + 18 interviews) and De Freitas (quasi-experiment + interviews) studies. Relationship-science perspective (Smith, Bradbury & Karney, Persp. Psychol. Sci.) argues chatbots may simulate relational functions without satisfying close-relationship constraints.
  [<Smith/Bradbury/Karney>](https://pmc.ncbi.nlm.nih.gov/articles/PMC12575814/)
- **Return rate is insufficient alone:** can be driven by habit/novelty/reward/task necessity. Bickmore 2010 shows variability increases desire-to-continue — but that's engagement, not relational depth.

### 4. Ablation & violation-injection design
- **Attribution is the hardest problem.** User traits (loneliness, desire-to-connect, personality) influence anthropomorphism and relationship reports — must measure user traits pre-interaction and test whether agent design predicts outcomes above and beyond them.
- **Violation experiments can establish mediation, not always causation.** Guingrich & Graziano: anthropomorphism is a *mediator*, not proven causal primitive.
- **Replika update = quasi-experimental violation signal** (capability removal → rupture), but not a clean controlled ablation (confounded by prior attachment/identity loss).
- **Recommended design:** isolate ONE primitive (e.g., self-disclosure reciprocity, personality consistency, memory, social repair, style adaptation); active control that preserves engagement+fluency (so loss isn't explained by boredom); DVs = return rate + session length + self-disclosure depth + perceived relatability + anthropomorphism + attachment/PSR; triangulate survey + behavioral + linguistic. Violation-injection must produce a *falsifiable rupture* visible in behavior/language, and repair must be distinguishable from mere return-to-baseline.

## Formal/operational takeaways for Macha
1. **Self-report scales are insufficient as the only relational measure** — prompt sensitivity, history effects, demand effects undermine direct interpretation.
2. **Discriminant validity is weak** across PSI/PSR/anthropomorphism — don't claim clean separation without evidence.
3. **Measurement invariance is unestablished** for long-term generative contexts — treat early/mid/late scores as non-comparable by default.
4. **Strongest longitudinal evidence is observational/quasi-experimental** (Aalto 2yr, Replika update) — use as empirical windows, not controlled proof.
5. **Behavioral measures alone are not enough** — always triangulate.
6. **Falsifiability must be stronger than "the agent feels real"** — predict when anthropomorphism fails to predict attachment, when return-rate decouples from self-disclosure, when violation-injection produces rupture without repair.

## Pitfalls / avoid
- Don't rely on single self-report scales (SDR/demand effects).
- Don't treat anthropomorphism = relational depth (it's a mediator).
- Don't treat return rate = relational evidence.
- Don't treat EEG/affective alignment as standalone proof.
- Don't treat qualitative themes as causal evidence.
- Don't assume generative agents behave like rule-based relational agents.
- Don't leave "I want it to be real" as an unmeasured demand effect.

## Bibliography
See inline links. Key primary sources: Zou et al. 2025; Reeves & Nass 1996; Bickmore 2010; Guingrich & Graziano 2025; De Freitas et al.; Aalto CHI 2026; Pi & Hunter; Smith/Bradbury/Karney.

## Open questions
1. Causal weight of anthropomorphism vs personality-consistency vs reciprocity in genuine attachment [UNRESOLVED].
2. How "I want it to be real" operates in open-ended game-agent interactions [UNRESOLVED].
3. How to operationalize rupture/rebound in open-ended agent games [UNRESOLVED].
4. Can self-report scales be stabilized across long-term open-ended interaction [UNRESOLVED].
5. Can return rate be separated from habit/reward-driven engagement [UNRESOLVED].
6. Can EEG/physiology serve as relational-depth indicators [UNRESOLVED].