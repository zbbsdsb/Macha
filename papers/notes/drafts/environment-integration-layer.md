# The Environment Integration Layer as an Architectural Primitive

> Status: **Discussion draft — PENDING team review.**
> Origin: Layer architecture calibration (2026-09-13). Audit of the current repository, not a
> new implementation plan; no code was changed.
> Normative companion: [`../../../docs/architecture.md`](../../../docs/architecture.md) holds the
> definitions and the boundary diagram. This note holds the **audit reasoning** behind them.
> Related: [`../archive/npc-world-boundary.md`](../archive/npc-world-boundary.md) (the NPC/world
> boundary in experiential terms), [`../accepted/paper-goal-and-world-architecture.md`](../accepted/paper-goal-and-world-architecture.md)
> (the "world-state Provider" engineering suggestion), [`../../../research/plans/roadmap-rework-draft.md`](../../../research/plans/roadmap-rework-draft.md).

---

## 0. The Question Being Calibrated

Not "how do we connect Minecraft", and not "what is Macha Core". The question is:

> **How should Macha and a concrete external world be connected through an independent Layer?**

The answer must hold for environments that do not exist yet:

```text
Macha
├── Minecraft Layer
├── Skyrim Layer
├── Cyberpunk 2077 Layer
├── Unreal Layer
├── Unity Layer
├── Simulation Layer
└── ...
```

These are **independent Environment Integration Layers**, not submodules of Macha Core. Macha must
not become a Minecraft-oriented framework merely because Minecraft is connected first.

---

## A. What Is Macha Today?

Audited 2026-09-13 across `README.md`, `docs/`, `papers/`, `research/`, `src/`, `tests/`,
`examples/`, `site/`, `announcements/`.

**Macha today is three things, none of them an environment integration:**

1. **A research position** — the paper project (`papers/`, `docs/research/`) about the
   player–NPC–world relationship; its core judgment is that the gap is a *missing field*, not
   missing information.
2. **A prototype target** — `docs/prototype_portrait.md`: Macha Spec v0.1 + Macha Core v0.1 +
   Elara tavern probe + Macha Conformance v0, explicitly out of scope for Unity/Unreal plugins,
   graphics, voice, vector DBs.
3. **A code skeleton** — `src/macha/` (~140 lines): `Observation`/`ActionResult` dataclasses;
   `BaseAgent.perceive/think/act` all `NotImplementedError`; `Memory` append + last-*N* retrieve;
   `Reasoning.decide()` returning one hardcoded sentence; `Action.execute(decision: str)`
   pass-through; a smoke test whose assertion is structurally always true.

### The finding that matters

**The code has no environment concept at all — but it has an implicit one.** `Perception.process_text`
and `Action.execute(decision: str)` presume a **text channel** as the world. Today's "environment
layer" is the type `str`.

So the audit answer to A is not "Macha Core is missing a Layer module." It is:

> Macha Core today is (i) cognition, (ii) an implicit text environment smuggled in through
> `str`-shaped method signatures, and (iii) no boundary at all. The Layer calibration's job is to
> name and type the third thing **without** moving cognition out of Core and **without** letting
> the first real environment into Core.

Boundary-relevant items that already exist elsewhere in the repo (and therefore are *not* new
inventions of this calibration):

- `roadmap-rework-draft.md` step ⑨ "Adapter / Capability Probe" — capability probing rather than
  an engine checklist, unified event protocol;
- `roadmap-rework-draft.md` step ② "Permeability Contract" and step ① "World Reconnaissance" —
  what a world allows an outside intelligence to write;
- `paper-goal-and-world-architecture.md` §3 — reserve a **world-state Provider** interface, do not
  build a large world simulation first;
- `research/world view taxonomy/draft-01.md` §8 — `register_world() / grant_agency() /
  validate_action() / commit_transition()` and the claim that Macha is closer to a *runtime that
  lets an existing world accept autonomous intelligence* than to an "NPC AI SDK".

This calibration is consistent with all four; it supplies the missing boundary definition.

---

## B. What Should a Layer Be?

> **A Layer is the boundary artifact that connects exactly one external environment to Macha
> Core, translating in both directions without either side knowing the other's implementation.**

It is a horizontal **Adapter / Integration**, not a vertical business-logic tier inside Macha.

Deliberately **not** the answer: "an API wrapper." An API wrapper exposes callable functions. A
Layer additionally (a) declares what the environment can actually do, (b) normalizes state and
events into one protocol, (c) carries the world's *answers* — refusals, side effects, state deltas
— back to the agent, and (d) reports how verifiable each capability is. Those four duties are what
make the boundary usable by a cognitive core rather than by a script.

---

## C. Where Is the Macha ↔ Layer Boundary?

Full exchange table in `docs/architecture.md` §3. The audit-level summary:

| Crosses into Core | Crosses out of Core | Never crosses |
|---|---|---|
| facts with provenance, environment events, permitted state, capability manifest, action results | typed `ActionCall` intent, state-queries the manifest allows | engine handles/ids/ticks; raw input events; pre-interpreted meaning; persona/memory/goals/plans |

Two hard lines define the boundary:

1. **Facts may cross; meaning may not.** "A player broke this block at X" is a Layer statement.
   "Player stole my wood, therefore I distrust him" is Core's. The second is built from the first
   plus memory, appraisal and persona — all Core-side.
2. **Intent may cross; mechanism may not.** Core sends *what it wants to do*; it never sends key
   presses, packets, or engine calls, and it never assumes the action is representable. The
   Layer's refusal is part of the protocol, not an error.

What the Layer must not absorb (otherwise it *is* an NPC framework): memory, persona, motivation,
reasoning, long-term planning, social cognition/appraisal.

---

## D. Where Is the Layer ↔ Environment Boundary?

Everything environment-native stops here, on the environment side of the Layer's translation:

- engine objects, handles, entity refs, block coordinates, item ids, component pointers;
- callbacks, event loops, ticks, scheduling, save/load, sessions, networking;
- identity, authentication, permission models;
- and the environment's own opaqueness — what it refuses to expose.

The Layer owns translation, connection, capability probing, state normalization, refusal
reporting, and the verifiability report. It is the **only** place in the stack where
environment-specific code is allowed to exist.

Consequence worth stating explicitly: because we do not own these worlds (Minecraft and InZOI are
existing commercial games — see `roadmap-rework-draft.md` §1), an action the world cannot express
is a **normal outcome**. The Core must be able to receive "no" and choose another intent.

---

## E. Should a Layer Be a Separate Repository?

Proposed shape:

```text
macha/                 Macha Core + Layer Protocol specification + conformance kit
macha-minecraft/       Minecraft Layer — independent project, independent release cycle
macha-sim/             trivial simulator Layer (in-repo control condition)
macha-skyrim/ etc.     later, independent
```

Arguments **for** separation:

1. **The protocol, not the code, is the coupling point.** If Layers live in the Core repo, the
   cheapest way to make a Layer work is to edit Core — which is exactly the failure this
   calibration exists to prevent.
2. **Different release cadences.** A Minecraft Layer tracks game/mod-loader versions; Core tracks
   cognition. Coupling them forces the slower one to gate the faster one.
3. **It makes the proof conditions checkable.** "A second author implements a Layer from the spec"
   is only meaningful if the second author's project is not the same repository.
4. **It keeps the paper's claim honest.** Macha's claim is a standard skeleton, analogous to
   `prototype_portrait.md` §5's acceptance criterion that someone can implement *only* the spec
   without Core and still pass conformance.

Arguments **against** (and the mitigation):

1. **Protocol churn across repositories is expensive.** Mitigation: the specification lives with
   Core (single owner), is versioned separately from Core, and a **simulator Layer stays in-repo**
   so the protocol can be falsified cheaply without crossing a repository boundary.
2. **A tiny team pays coordination cost.** Mitigation: start as one repository with strict package
   boundaries; split into sibling repositories when the second Layer is actually attempted. The
   *organizational* decision can be deferred; the *boundary* decision cannot.

Audit answer to E: the three-part org (`Macha` / `Macha Layer Protocol` / `Macha Minecraft Layer`)
is reasonable, with the Protocol specification co-located with Core and implementations separate.

---

## F. What Is the Minimal Layer?

The full M1–M9 list and proof conditions are in `docs/architecture.md` §6; the operational plan is
[`../../../research/plans/minecraft-layer-validation-plan.md`](../../../research/plans/minecraft-layer-validation-plan.md).
The audit-level essence — the question "what does *any* Environment Layer need, if only Minecraft
were connected today?":

1. **perspective** — which entity/agent window this Core instance sees through;
2. **a typed, uninterpreted event stream** — what happened, with provenance;
3. **a bounded state query** — the agent's observation window, not world truth;
4. **a probed capability manifest** — what this world can actually do;
5. **an action executor + structured result** — including refusal and state delta;
6. **session lifecycle** — connect/disconnect/timeout/reconnect;
7. **a verifiability report** — deterministic check vs. trusted outcome;
8. **a replayable transcript** — so the boundary itself is auditable.

Anything beyond this list (universal abstraction layers, engine-plugin systems, robotics buses) is
abstraction with nothing to test it against, and is explicitly **out of scope** for the calibration.

**Minecraft's role:** a **Concrete Layer Test Case**. The current goal is not "build Macha for
Minecraft" but "*build one concrete Layer to validate the Layer abstraction*." If the Layer design
is right, a Skyrim Layer should be implementable independently later without redesigning Macha.

---

## G. The Boundary Diagram, and Who Owns What

```text
Macha
   │   owns: memory · persona · motivation · reasoning · planning · appraisal ·
   │         guardrail · decision log · agent's own state
   │
   │  ── Layer Boundary (Layer Protocol) ──────────────────────────────
   │     ▼ ActionCall (typed intent, may be refused)
   │     ▲ Observation · Event · State · Capability · Action Result
   ▼
Layer
   │   owns: translation · connection · capability probing · state normalization ·
   │         refusal reporting · verifiability report · all environment-specific code
   │
   │  ── Environment Boundary (native interface) ───────────────────────
   ▼
External Environment
        owns: rules · state · history · entities · causality · the right to refuse
```

Responsibilities in one line each:

- **Macha** decides *what it means and what to do*; it never learns which world it is in.
- **Layer** decides *how the world becomes intelligible and executable*; it never learns why the
  agent wants anything.
- **Environment** decides *what is true and what is permitted*; it never learns the agent's
  reasons.

---

## H. What This Means for the Paper

Two connections, both load-bearing:

1. **The Layer is the engineering form of the paper's "semi-permeable membrane."**
   `npc-world-boundary.md` §5: the world can enter the NPC's experience but must pass through its
   stance; the NPC's intent can change the world but must be filtered by world rules. The Layer
   Protocol is that membrane made concrete: facts in (uninterpreted), intent out (refusable).
2. **It answers `paper-goal-and-world-architecture.md`'s reserved interface.** That note asked for
   a "world-state Provider" without building a world simulation; the Layer is the Provider, and its
   capability manifest + verifiability report are what let the paper claim a standard can guarantee
   the world↔character interface holds across engines.

What it must **not** become: a section about Minecraft. The paper's subject stays the
player–NPC–world relationship; the Layer is cited as the standard's implementation boundary.

---

## I. What Would Prove This Wrong (Falsifiers)

1. A second Layer (or the simulator) cannot be implemented without changing Core.
2. The five exchange categories turn out to be insufficient in a real environment — for example,
   Core must be able to *push* structured knowledge into the world (lore, relationship state,
   persistent agent state) and no category carries it.
3. Capability probing cannot be made honest in a real environment (the world's exposed surface is
   not enumerable), making the manifest a fiction.
4. The refusal channel proves unusable because environments return ambiguous failures, so Core
   cannot distinguish "impossible" from "died trying".
5. Minecraft-specific concepts leak into Core anyway because the Core's action vocabulary is
   defined from Minecraft's verbs.

Each of these is a **protocol bug**, not a reason to make Core environment-aware.

---

## J. Open Questions for the Team

1. Is **State** a separate exchange, or a query answered as an Observation?
2. Who owns the agent's own state (position, inventory, status) — Core, Layer, or field-split?
3. Does the Protocol need **time** (engine tick vs. agent time), and in what units?
4. Is a simulator Layer an acceptable second environment for proving generality, or does the
   Protocol only count as validated against a second *real* world?
5. What is the minimum conformance kit that lets an independent author implement a Layer from the
   spec alone?
6. Does the Layer Protocol belong in the paper as a standard artifact, or only in `docs/` as
   engineering? (Interacts with question tree fork 3: design theory vs. architecture standard.)
