# Subsection Research: From Arbitrary Actions to Grounded Compositional Agency

> Status: research output for a single paper subsection.
> Scope: only the conceptual issue of "arbitrary actions" vs "open-ended task execution over a constrained world action space."
> This document does NOT propose a full Macha architecture.

---

## A. Conceptual Diagnosis

The original objective—“NPCs can perform arbitrary actions”—is not merely hard to implement; it is conceptually ill-posed in a game context.

1. **Game actions are not unconstrained.** Every action in a game is mediated by the engine, physics, animation system, object model, interaction API, and world rules. An “arbitrary action” with no defined world effect is not an action; it is an ungrounded utterance. If an LLM outputs “the NPC flies to the moon,” this is only an action if the world has a corresponding capability, state transition, and consequence.

2. **Action-space cardinality is not behavioral generality.** Exposing 10,000 primitive actions does not imply that an agent can solve 10,000 tasks. A system can have a large action API and still fail at open-ended tasks if it lacks planning, state tracking, affordance filtering, failure recovery, and task decomposition. Conversely, a small set of well-structured primitives can support a very large task space when composed appropriately.

3. **The “arbitrary action” framing conflates interface with competence.** It asks “what can the agent directly do?” rather than “what goals can the agent accomplish?” The former is an interface question; the latter is a competence question. Macha’s real interest is not interface breadth, but whether an agent can autonomously accomplish goals in a world whose action space is necessarily finite and structured.

4. **The naive objective imposes an unbounded authoring burden.** For an arbitrary action to be meaningful, a developer must implement its preconditions, effects, failure modes, and world consistency. An “arbitrary action space” is therefore either vacuous (no world effect) or equivalent to asking developers to author an infinite set of behaviors. Neither is a defensible research objective.

5. **The meaningful problem is task-level generality, not action-level flexibility.** The relevant question is: can an agent solve unseen tasks by composing feasible, world-grounded actions—without requiring a developer to pre-author a scripted procedure for every task? This is a different and more precise objective.

---

## B. Literature Map

| Approach | Abstraction | What it generalizes over | What remains developer-authored | Limitations |
|---|---|---|---|---|
| FSM | States and transitions | Explicitly specified behavior sequences | Every state, transition, trigger | Poor scaling; no task-level autonomy |
| Behavior Trees | Tree of conditions/actions | Reactive combinations of authored behaviors | Node behavior and tree structure | Good for control, not task-level planning |
| GOAP (F.E.A.R.) | Goal + primitive actions with preconditions/effects | Action sequencing for a given goal | Action schemas, world state model, goals | Planning unpredictability; action model authoring |
| HTN | Hierarchical tasks and methods | Task decomposition along authored methods | Methods and domain knowledge | Reduces search but still requires authored decomposition |
| Utility AI | Weighted action selection | Continuous motivation-based choice | Actions, considerations, curves | No long-horizon planning or task decomposition |
| Classical Planning (STRIPS/PDDL) | Symbolic actions with preconditions/effects | Goal-directed action sequences | Domain model, action schemas, state predicates | Symbolic grounding bottleneck; scalability |
| RL | Policy from state to action | Behavior within training distribution | Reward, environment interface, training pipeline | Task-specific; sample inefficient; poor transfer |
| LLM agents (ReAct, Reflexion) | Language-based reasoning + tool calls | Semantic flexibility over tools/APIs | Tools, environment interface, verification | Grounding, validity, world consistency not guaranteed |
| Voyager | Code as actions + skill library | Reusable skills in Minecraft | Environment API, skill verification | Domain-specific; depends on rich code interface |
| Affordance-based embodied AI (VirtualHome, ALFRED) | Agent-object-state-context action possibilities | Task planning over grounded interactions | Environment simulator, action definitions, affordance labels | Often simulation-specific; limited game-engine transfer |
| Game-playing agents (AgentBench, MineDojo) | Broad task benchmarks | Generalization across many tasks | Environment APIs, evaluation protocols | Demonstrates breadth, not a reusable NPC standard |

**What is already solved:** GOAP, HTN, and classical planning already demonstrate that a finite set of primitives can be composed to solve many tasks. LLM agents already demonstrate semantic flexibility and skill reuse in constrained environments.

**What remains open:** a portable, engine-agnostic abstraction for *grounded, compositional, controllable* agency that (a) reduces developer-authored behavioral pathways, (b) preserves world consistency, and (c) works across games with different engines, object models, and interaction APIs.

---

## C. Conceptual Distinction

| Term | Definition |
|---|---|
| **Primitive action** | Atomic executable operation exposed by the environment, with defined preconditions/effects (e.g., `open(door)`). |
| **Composite action** | A sequence or conditional combination of primitives (e.g., `unlock_and_open(door)`). |
| **Skill** | A reusable, parameterized, named procedure/policy that composes primitives or composites, often with preconditions, effects, and failure handling. |
| **Affordance** | A relation indicating that an action is possible/meaningful for a specific agent, on a specific object, under a specific world state/context. |
| **Goal** | A desired world state or condition. |
| **Task** | A goal instantiated in a particular context, often with success criteria. |
| **Plan** | A sequence of actions/skills intended to achieve a goal. |
| **Policy** | A mapping from state to action/skill, reactive or learned. |
| **Execution** | Grounding a plan in the environment, issuing actions, and monitoring outcomes. |
| **Replanning** | Revising a plan after failure, unexpected state change, or new information. |
| **Open-ended task completion** | Solving unseen tasks by composing known capabilities and adapting to context. |
| **Action-space generality** | Breadth of primitive actions exposed to the agent. |
| **Task-space generality** | Breadth of goals/tasks the agent can accomplish. |
| **Behavioral autonomy** | Degree to which the agent selects and executes behavior without developer-authored pathways. |
| **Developer authoring burden** | Amount of hand-authored behavior/scripting required to achieve a desired task coverage. |

**Relationships:**

- A small primitive set can support a large task space **if** actions have explicit preconditions/effects, the agent can plan, the world is observable enough, affordances are discoverable, and execution feedback enables replanning.
- A large primitive set can still fail at open-ended tasks **if** actions are not composable, not world-grounded, not filtered by affordances, or not embedded in a planning/execution loop.
- **Affordance** is the mediating relation between action space and task space: it determines which actions are *possible for this agent on this object in this state*, rather than what actions exist globally.
- **Skills** sit between primitives and tasks: they are reusable chunks that reduce planning search and authoring cost.
- **Task space** is not a subset of action space; it is a product of goals, contexts, and available capabilities.

**Key analytical result:** Macha’s value is more plausibly located in *capability/task/behavior space* than in *raw action-space cardinality*. The action space is a necessary substrate, but it is not the right abstraction for autonomy.

---

## D. Adversarial Challenge

Could the proposed direction be unnecessary or already solved?

1. **GOAP already composes actions from a finite set to achieve goals.** It reduces developer-authored sequences. If the claim is only “composition is good,” it is not new.
2. **HTN already performs hierarchical task decomposition.** If the claim is only “decompose tasks,” it is not new.
3. **Behavior Trees and Utility AI already handle many task combinations reactively.** If the claim is only “avoid scripting every path,” part of it is established.
4. **LLM agents such as Voyager already demonstrate skill composition and open-ended task execution in Minecraft.** If the claim is only “LLMs can compose actions,” the evidence is already strong.
5. **Classical planning and RL already formalize action models, goals, and policies.** If the claim is only “planning matters,” it is textbook.

**What would actually be new about Macha?**

The unresolved problem is not “can an agent compose actions.” It is:

> Can we define a **portable, game-engine-agnostic, developer-controllable abstraction** that lets an agent compose grounded actions to solve open-ended tasks, while keeping the developer’s authoring burden low and preserving world consistency across different games?

GOAP, HTN, BT, Utility AI, and RL each solve a slice, but they are either tied to a specific game, require heavy per-game action modeling, or lack semantic flexibility. LLM agents add semantic flexibility but do not by themselves guarantee grounding, validity, failure recovery, or controllability.

If Macha merely claims “we use LLMs to compose actions,” it is redundant. If Macha claims “we provide a standard capability/affordance interface that makes compositional autonomy portable and controllable across engines,” then there is a meaningful, if difficult, research gap.

---

## E. Strongest Reformulation

The strongest formulation is not one of the hypotheses alone, but a precise combination:

> **NPCs do not need an unbounded action space. They need a grounded, compositional capability space through which they can autonomously decompose and execute open-ended tasks, with closed-loop execution and failure recovery, without requiring developers to pre-author every behavioral trajectory.**

More specifically:

- **Capabilities** are the developer-authored building blocks.
- **Affordances** determine which capabilities are available to which agent, on which object, under which state/context.
- **Task decomposition** is the agent’s responsibility.
- **Execution and replanning** close the loop.
- **Controllability and world consistency** are preserved by explicit preconditions/effects, constraints, and verification.

This reformulation elevates **Hypotheses B, C, D, E, and F** as mutually supporting, and **rejects Hypothesis A** as the core objective.

The central research problem is therefore:

> How should a game define an agent’s capability interface so that the agent can generalize over tasks, not just over actions, while keeping developer authoring cost and world inconsistency low?

---

## F. Falsifiable Hypotheses

The following hypotheses are designed to distinguish the proposed direction from “just add more actions” and from “just use an LLM.”

**H1 — Composition over cardinality.**  
Given the same number of primitives, a compositional agent with planning, affordance filtering, and replanning will achieve higher unseen-task completion than a flat action-selection agent with a much larger action set, on a held-out task benchmark.

**H2 — Task-space scaling.**  
For a fixed environment, task-space coverage grows combinatorially with the number of composable primitives for a compositional system, but at most linearly for a scripted/flat system. This can be measured by counting how many distinct tasks are solvable as primitives are added.

**H3 — Authoring burden reduction.**  
For a fixed set of N tasks, a goal-directed compositional system requires fewer developer-authored behavior pathways (states, transitions, scripts, methods) than an FSM/BT system to reach the same task coverage, measured in authoring units or lines of authored behavior.

**H4 — Robustness through closed-loop execution.**  
A compositional agent with failure detection and replanning recovers from injected environmental perturbations at a higher rate than an open-loop scripted or BT baseline.

**H5 — Affordance grounding reduces invalid actions.**  
When objects expose agent-dependent affordances, an agent using an explicit affordance model will have higher action validity and fewer impossible-action attempts than an agent using a flat global action list.

**H6 — Skill transfer.**  
A skill library acquired in one set of tasks transfers to unseen tasks in the same environment better than a flat action policy or an action API with no reusable skills.

**Measurement caution:** To avoid confusing “genuine generalization” with “larger prompt/library/API,” experiments must use held-out tasks, controlled primitive sets, ablations over planning/affordance/replanning, and authoring-cost measurements that are independent of model size.

---

## G. Evidence Matrix

| Claim | Type | Evidence needed | Existing evidence | Confidence | Risk |
|---|---|---|---|---|---|
| “Arbitrary actions” is ill-posed in games | Supported inference | Conceptual analysis; game-engine constraints | Engine/API/world-rule constraints are well known | High | Low |
| Action-space cardinality ≠ task-space generality | Supported inference | Controlled benchmarks comparing action count vs task coverage | GOAP/HTN/LLM-agent literature strongly suggests this | High | Medium |
| Finite primitives can generate a large task space | Supported inference / empirical in specific domains | Compositional planning benchmarks | GOAP, HTN, Voyager, classical planning | High | Medium |
| Compositional skills improve open-endedness | Supported inference / empirical in specific domains | Skill-library transfer experiments | Voyager, skill-based RL | Medium-High | Medium |
| Affordances improve grounding and reduce invalid actions | Supported inference from embodied AI | Affordance-based planning studies | VirtualHome, ALFRED, Gibson-inspired work | Medium | Medium |
| GOAP/HTN reduce authored action sequences | Established by prior work | Game AI literature and production use | F.E.A.R., Horizon | High | Low |
| LLM agents add semantic flexibility but not grounding/verification | Established by prior work | Analysis of LLM tool-use failures | ReAct, Reflexion, Voyager limitations | High | Low |
| A standard capability/affordance interface can reduce developer burden across games | Design hypothesis | Cross-engine prototype and authoring-cost study | No direct existing evidence | Low-Medium | High |
| Closed-loop replanning improves robustness | Supported inference / empirical in planning | Replanning comparisons | Classical planning and RL literature | Medium-High | Medium |
| Macha’s proposed abstraction is novel as a portable standard | Design hypothesis | Literature search for cross-engine capability standards | No established equivalent known | Low-Medium | High |

---

## H. Proposed Paper Subsection Outline

**Title:**  
*From Arbitrary Actions to Grounded Compositional Agency*

**Paragraph 1 — Opening problem.**  
The naive design target is “NPCs can perform arbitrary actions.” This appears to maximize freedom, but it is not a well-formed objective in a game world.

**Paragraph 2 — Why arbitrary is ill-posed.**  
Action spaces are bounded by engine, physics, animation, object models, APIs, and world rules. An “arbitrary action” without world effect is not an action.

**Paragraph 3 — Cardinality is not generality.**  
Action-space size is not the same as task-space coverage. Introduce the distinction between action-level flexibility and task-level generality.

**Paragraph 4 — Capability/task/behavior/narrative spaces.**  
Define the relevant spaces and argue that Macha’s value is located in capability/task/behavior space, not raw action cardinality.

**Paragraph 5 — Finite primitives and composition.**  
A finite primitive set can generate a large task space under composition, planning, affordances, and feedback. Discuss the conditions and the limits.

**Paragraph 6 — What existing game AI already solves.**  
FSM, BT, GOAP, HTN, and Utility AI each reduce some authoring burden but leave important parts developer-authored.

**Paragraph 7 — What LLM agents add and what they do not solve.**  
LLM agents add semantic flexibility and skill reuse, but grounding, validity, world consistency, and controllability remain open.

**Paragraph 8 — Affordances as the missing relation.**  
Affordance is not an action; it is a relation between agent, object, state, and context. It explains why the same object can afford different actions to different agents.

**Paragraph 9 — The unresolved gap.**  
The open problem is a portable, engine-agnostic, developer-controllable abstraction for grounded compositional agency. This is not solved by any single existing approach.

**Paragraph 10 — Macha’s research hypothesis.**  
Macha’s hypothesis is not “infinite actions” but “a grounded, compositional interface to the world through which agents pursue goals without pre-authored trajectories.”

**Paragraph 11 — Scope and limitations.**  
This subsection does not claim Macha has solved open-ended task execution. It only identifies the right problem and the conditions under which it is meaningful.

**Paragraph 12 — Testable predictions.**  
State the falsifiable hypotheses and the need for controlled evaluation distinguishing generalization from larger action sets, prompts, or skill libraries.

---

## I. Drafting Specification

### Terminology

**Use:**  
- primitive action  
- composite action  
- capability  
- skill  
- affordance  
- goal  
- task  
- plan  
- execution  
- replanning  
- task-space generality  
- capability space  
- grounded compositional agency  

**Avoid as positive terms:**  
- arbitrary actions  
- unlimited actions  
- open-ended actions  
- action mapping space  
- general action space  

If these terms appear, they should be explicitly identified as the rejected naive objective.

### Argument order

1. Reject “arbitrary actions” as ill-posed.
2. Separate action-space cardinality from task-space generality.
3. Introduce capability/task/behavior/narrative spaces.
4. Show how finite primitives can generate large task spaces under composition and planning.
5. Review what FSM/BT/GOAP/HTN/Utility already solve.
6. Review what LLM agents add and what remains unsolved.
7. Introduce affordances as the grounding relation.
8. Identify the portable-standard gap.
9. State Macha’s hypothesis.
10. Define falsifiable tests.

### Citations required

- Orkin (GOAP/F.E.A.R.)
- Champandard (Behavior Trees)
- Rabin (Game AI Pro, Utility AI)
- Erol et al. / Nau et al. (HTN)
- Fikes & Nilsson (STRIPS/PDDL)
- Yao et al. (ReAct)
- Shinn et al. (Reflexion)
- Wang et al. (Voyager)
- Sumers et al. (CoALA)
- Park et al. (Generative Agents)
- Gibson (affordance)
- VirtualHome / ALFRED / BEHAVIOR for embodied affordance planning
- MineDojo / AgentBench for broad agent benchmarks

### Claims that must be hedged

- “Composition reduces developer authoring burden” should be stated as a hypothesis, not an established fact.
- “LLM agents compose skills” should be limited to specific environments such as Minecraft.
- “Macha’s standard will reduce authoring burden across engines” is a design hypothesis with no direct evidence yet.
- “Finite primitives are sufficient for open-ended tasks” must be qualified by planning, observability, affordances, and failure recovery.

### Claims that must NOT be made

- Do not claim FSMs are obsolete.
- Do not claim LLMs “understand” actions.
- Do not claim Macha has implemented or solved open-ended task execution.
- Do not claim arbitrary actions are impossible in all possible systems; claim they are ill-posed as a game objective.
- Do not claim that a compositional system automatically guarantees open-endedness.

---

## Critical Final Question

**If Macha succeeds at this problem, what capability does the game developer gain that they do not already have with modern FSMs, Behavior Trees, GOAP, Utility AI, or LLM-based NPC systems?**

The answer is not “the agent can do more actions.” The capability is:

> **A developer would be able to specify a small set of grounded capabilities and constraints, and then have NPCs autonomously compose those capabilities to solve unseen tasks, recover from failures, and adapt to changing world state—without authoring a behavior tree, FSM, GOAP action model, or scripted procedure for each task, and without losing world consistency or controllability.**

Modern FSMs, BTs, and Utility AI give developers control but require explicit behavior pathways. GOAP/HTN reduce pathway authoring but require heavy per-game action modeling and can become unpredictable. LLM agents add flexibility but do not guarantee grounding, validity, or developer control.

Macha’s potential contribution is to make the *compositional, goal-directed, world-grounded* paradigm portable and controllable enough to be a standard game AI layer. If it only re-implements GOAP with LLMs, it is not worth a paper. If it defines a reusable abstraction that measurably reduces authoring burden while preserving world consistency across engines, it is a legitimate research direction. The evidence for this gap is currently conceptual and partial; the next step is a controlled cross-engine prototype with the falsifiable hypotheses above.
