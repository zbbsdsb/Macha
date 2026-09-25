# Target Architecture (Draft)

> Status: **DRAFT — Layer calibration applied 2026-09-13.**
> This revision adds the **Environment Integration Layer** (the boundary between Macha and an
> external world). It is a document-only revision: no code was modified.
> Sections marked **[PENDING]** are calibration proposals awaiting team ratification.
> **Sequencing (decided 2026-09-13): Layer-first, Core later** —
> [`../papers/notes/accepted/decision-layer-first-sequencing.md`](../papers/notes/accepted/decision-layer-first-sequencing.md).
> Reasoning, audit answers and open questions live in
> [`../papers/notes/drafts/environment-integration-layer.md`](../papers/notes/drafts/environment-integration-layer.md).

---

## 0. Two Systems, One Contract

Macha is not one system with game support bolted on. It is **two separable systems joined by a
single contract**:

| System | What it is | Home |
|---|---|---|
| **Macha Core** | the cognitive core: observation intake, memory, reasoning, reflection, planning, action generation, guardrail | this repository, `src/macha/` |
| **Environment Integration Layer** (short: **Layer**) | an adapter that connects **exactly one** external environment to Macha Core | a separate project (`macha-minecraft/`, `macha-skyrim/`, …) |
| **External Environment** | the world itself plus its native interfaces (engine, server, API, robot bus) | not ours; we do not own it |

```text
                External Environment
                        │
                        │  Environment Boundary  (the world's native interface)
                        ▼
                      Layer
                        │
                        │  Layer Boundary  (the Layer Protocol)
                        ▼
                   Macha Core
```

Three hard rules follow from this split:

1. **Macha Core must not know which environment it runs in.** No engine import, engine type,
   engine id, tick semantic, or engine permission concept may appear in Core.
2. **A Layer must not think.** It may translate, observe, declare, and refuse — it may not
   remember, judge, plan, or hold persona.
3. **Minecraft is a test case, not the identity of the framework.** Macha must not become a
   Minecraft-oriented framework because Minecraft was the first environment connected.
   The same rule will apply to Skyrim, Cyberpunk 2077, Unreal, Unity, simulations, robotics.

> **Falsification test of this whole document:** if adding a second Layer (a second game, or a
> simulator) requires changing Macha Core, then the Layer Protocol below is wrong — fix the
> protocol, not the Core's identity.
>
> Because the agreed sequencing is Layer-first, this test is run **before** the real Core exists,
> against a **Stub Core**: a non-cognitive, rule-based counterpart that consumes observations and
> emits `ActionCall`s, with no memory, persona, or planning. The stub's action vocabulary must
> contain only the common capability classes (see §5) — if `place_block` appears on the Core side,
> the boundary has already leaked. The real Core later replaces the stub and re-runs the same test
> **without changing the Layer**.

---

## 1. What Macha Core Is

### 1.1 Current state of the core (audit, 2026-09-13)

Verified against `src/macha/`:

| File | Content |
|---|---|
| `core/agent.py` | `Observation` / `ActionResult` dataclasses; `BaseAgent.perceive/think/act` — all `NotImplementedError` |
| `core/memory.py` | append + `all()`; `retrieve()` returns the last *N* items (`TODO: proper scoring`) |
| `core/perception.py` | `process_text(text, source)` → `Observation` |
| `core/reasoning.py` | `decide()` returns one hardcoded sentence (`TODO: call LLM`) |
| `core/action.py` | `execute(decision: str)` → `ActionResult` (pass-through) |
| `tests/test_smoke.py` | one assert that is structurally always true |

Two facts matter for this document:

- **There is no environment concept in the code at all.** Nothing in `src/macha/` knows about
  Minecraft, a tick, a socket, or a block.
- **There is an *implicit* environment already:** `Perception.process_text` and
  `Action.execute(decision: str)` hard-code a **text channel** as the world. The Layer
  abstraction is precisely the extraction of that implicit assumption into a named, typed,
  replaceable boundary.

### 1.2 The cognitive loop

```text
Environment-derived Observations
        │
        ▼
┌─────────────────┐
│  Perception     │  Structured observations (who / what / where / when / provenance)
└────────┬────────┘
         ▼
┌─────────────────┐
│  Memory         │  Short-term context + long-term experiences + reflection summaries
└────────┬────────┘
         ▼
┌─────────────────┐
│  Reasoning      │  Goal parsing, planning, decision-making, reflection
└────────┬────────┘
         ▼
┌─────────────────┐
│  Action         │  Emit structured ActionCalls (never engine calls)
└─────────────────┘
```

**[PENDING]** Additions already proposed elsewhere in the repo and not yet reflected above:
an **Appraisal** step between perception and memory (relationship meaning before storage), an
in-loop **Reflection** trigger, and a **Guardrail** stage (see
[`../research/plans/roadmap-rework-draft.md`](../research/plans/roadmap-rework-draft.md), which
notes that `aetherflow-review.md` carries a five-stage skeleton while this document carries
four). This revision does not decide that question; it only fixes the outer boundary.

### 1.3 Core module responsibilities

- **Perception** — input: observations delivered by the Layer **only** (never by reading game
  memory or engine callbacks directly). Output: `Observation` with provenance.
- **Memory** — short-term session context; long-term facts, relationships, reflections;
  retrieval ranked by relevance, recency, importance. Early storage: SQLite/JSON.
- **Reasoning** — decisions from observations + memory; planning (goal decomposition) and
  reflection; LLM-backed with rule-based fallback.
- **Action** — emits structured `ActionCall` objects (capability name + typed args + provenance).
  It does **not** know how they are executed; the Layer decides representability and reports back.

### 1.4 Interface conventions (draft, unchanged)

```python
@dataclass
class Observation:
    content: str
    timestamp: float
    source: str

@dataclass
class MemoryItem:
    content: str
    importance: float
    timestamp: float
    metadata: dict

class BaseAgent:
    def perceive(self, observation: Observation) -> None: ...
    def think(self) -> str: ...
    def act(self) -> str: ...
```

> The `str`-shaped signatures above are the text-channel assumption of §1.1. They are kept until
> the Layer Protocol is ratified; the Protocol, not an ad-hoc signature change, is what should
> widen them (see §3).

### 1.5 The reception domain (from the SepMay path)

`research/paths/01-sepmay-ivy/` is a **frozen Core-side path**; its **接收域 / reception domain**
(`外部信息源 + 内部信息源 → 运算域`) is Core's intake boundary. This section fixes what it maps to,
so the mapping does not live only in conversation.

| SepMay element | Artifact here | Written by | Read by |
|---|---|---|---|
| 外部信息源 external source | observations/events **after admission** | Layer produces → Runtime **admits** | operators (computing domain) |
| 内部信息源 internal source | Core's committed state (memory / relations / persona) | **only** IC's send-back at chunk close | operators |
| 算子集合 operators | Core operators (incl. future appraisal / guardrail) | — | — |
| 输出域 Chunk/Thread | IC — the data-organization layer | — | — |
| actions | `ActionCall` → runtime → Layer → environment | computing domain | Layer |

Three properties follow:

1. **Admission, not reception.** The reception domain decides what enters *this agent's* world
   model, at what granularity, with what uncertainty (`window`, `truncated`, `verifiability`).
   Its product is **gated facts, not a copy of the world**.
2. **No meaning here.** Appraisal ("what does this mean for me") belongs to the computing domain's
   operators. Facts may cross; meaning may not — the same line as §3.1.
3. **Two write rules, never one pool.** The external source is append-only facts; the internal
   source is written **only** by IC's send-back (facts / the agent's own version / weights).
   Mixing the two pools is the entry point of false memory.

**The loop and its gate.** The internal source is both an input to the computing domain *and* the
target of the send-back, so `output → internal source → computing` is a cycle. IC's **two-phase
commit at chunk close** is the gate for it; without that gate, operators read uncommitted
intermediate state — a memory shape a human cannot have.

**Consequences for the Layer side.**

- The **Layer is the producer** of the external half. It is not part of the reception domain, and it
  can neither read nor write the internal source (§0 rule 2: a Layer must not think).
- The reverse path (intent: `ActionCall` → runtime → Layer → environment) **does not pass through
  the reception domain** — only facts come back through it.
- A **plugin is not the Layer**: it is the deployment form of one Layer inside one environment
  (see [`../research/plans/minecraft-layer/04-project-structure.md`](../research/plans/minecraft-layer/04-project-structure.md)).
  Hence: a plugin must hold **no cross-session state** (configuration excepted), must lose **no
  memory** when restarted, and must contain **no logic that needs history**.

**Four review questions — which side does this code belong to?**

1. Needs block coordinates / entity UUID / tick → **Layer / plugin** side.
2. Needs "what the player did last month" → **Core side (reception domain)**.
3. Judges "what does this mean for me" → **computing domain** (not reception).
4. Writes "his version" → **only IC at chunk close** (internal source); a plugin never writes.

**Where drives live (intrinsic motivation).** A drive adds **no new box** — it occupies three existing
positions in the same picture: (**① storage**) a class of persistent state in the **internal source**, on the
**weights** leg of the send-back; (**② computation**) an **operator** in the computing domain that folds
recent history (setpoint deviation / learning progress / option growth) into drive change; (**③ use**) the
**output domain**, where a drive is what opens a Chunk when there is *no external stimulus* — and the
send-back then updates it, which is why the loop can run on its own.

> **The external source decides "the world makes me open a Chunk"; a drive decides "I open one myself."**
> It is the loop's only **endogenous** initiator — the exogenous entry is the world. Without a drive, this
> picture is static whenever nothing external arrives.

A drive belongs neither to the external source (facts) nor to the Layer (which only reports facts, executes
actions and refuses). Path, competing designs and open decisions:
[`../research/paths/02-intrinsic-motivation/README.md`](../research/paths/02-intrinsic-motivation/README.md).

**Open (not decided).** Admission has **no name or contract** on the Core side yet (the Layer side
has `EnvironmentPort`). A minimal `Intake` — admit → dedupe/order → stamp provenance & uncertainty
→ land in the external source — is a Phase-3 design item, tracked in
[`../research/paths/01-sepmay-ivy/open-decisions.md`](../research/paths/01-sepmay-ivy/open-decisions.md).

---

## 2. What a Layer Is

> **A Layer is the boundary artifact that lets one external environment be used by Macha Core
> without either side knowing the other's implementation.**

Properties a Layer must have:

1. **Bidirectional** — it translates the world inward (observations/events/state) *and* intent
   outward (actions), and carries the world's answer back (success, failure, refusal, side effect).
2. **Single-environment** — one Layer binds one environment. It is not a general-purpose engine
   abstraction and it is not part of the Core's module tree.
3. **Honest** — it reports what the environment actually exposed and what it could not
   (capability declaration + refusals), including the parts where the world is opaque.
4. **Non-cognitive** — see §3.3.
5. **Versioned independently** — a Layer can be updated or replaced without touching Core.

### 2.1 What a Layer is not

| Not this | Because |
|---|---|
| An "API wrapper" | An API wrapper exposes functions; a Layer also declares capabilities, normalizes state/events, and carries refusals and side effects back |
| A submodule of Macha Core | That is exactly how a framework becomes environment-oriented |
| An NPC framework | Memory, persona, motivation, reasoning, planning and social cognition stay in Core |
| The world simulator | Simulating the world is the environment's job; Macha ingests, it does not author |

---

## 3. Boundary A — Macha ↔ Layer: the Layer Protocol

The only thing Macha Core and a Layer share. **[PENDING]** — the five exchange categories below
(Observation, Event, Action, Action Result, Capability) plus the disputed sixth (**State**, see §10)
are the calibration result; naming and schemas are not frozen.

**Transport constraint.** The Protocol must be **transport- and language-agnostic** —
JSON-RPC-shaped, MCP-compatible preferred. Core is Python while a Minecraft Layer is likely
JS/Node (Mineflayer) or Java (a mod); no side may bind the other's language or process model.
This also converges with `../research/standards_interop.md` §188, which already proposes converging
`ActionCall` onto the Tool-Use shape. Concrete baseline binding for the first Layer (HTTP control
plane + WebSocket stream, JSON, protocol v0): [`../research/plans/minecraft-layer/01-protocol-v0.md`](../research/plans/minecraft-layer/01-protocol-v0.md).

| Exchange | Direction | Question it answers | Carries |
|---|---|---|---|
| **Observation** | Layer → Core | What can this agent perceive *now*? | agent-local, perspective-bounded view: entities, positions, affordances, incoming messages, with provenance and confidence |
| **Event** | Layer → Core | What happened in the environment? | uninterpreted facts with actor/target/place/time: `player_broke_block(pos, actor)`, `npc_attacked(victim)`, `time_changed(t)` |
| **Action** | Core → Layer | What does the agent want to do? | structured intent: capability name + typed args + provenance (who decided, why), never key presses or engine calls |
| **Action Result** | Layer → Core | What did the world do about it? | success / failure / refusal + reason + state delta + side effects |
| **State** *(disputed — see §10)* | both ways | What is the current state of agent and world? | agent state (Core-owned) and environment state (Layer-provided); Core reads, the environment writes |
| **Capability** | Layer → Core | What can this environment actually do? | the manifest: available operations, argument schemas, preconditions, expected effects, verifiability, cost/latency, permission scope |

### 3.1 The same event, two sides of the line

```text
Layer may say:   "player broke block at (X, Y, Z) at tick T."
Layer may NOT say: "player is hostile, therefore distrust him."
```

The second sentence is cognition: appraisal, memory of previous acts, persona, stance. It happens
in Core, on top of the fact. If a Layer writes it, the Layer has become an NPC framework.

### 3.2 What crosses the boundary

| Crosses into Core | Crosses out of Core | Never crosses |
|---|---|---|
| facts, with provenance | intent, as a typed `ActionCall` | engine objects, handles, ids, tick semantics |
| environment events (raw) | capability names the manifest declared | raw input events (key presses, packets) |
| state snapshots the agent is allowed to see | agent's own state to persist | pre-interpreted meaning ("he is lying") |
| capability manifest + refusals | queries for state the manifest allows | persona, memory, goals, plans, social judgment |

### 3.3 Cognition stays in Core — the Layer must not quietly absorb

- memory (including "who wronged me")
- persona / character consistency
- motivation and goal selection
- reasoning, planning, long-term planning
- social cognition, relationship state, trust/distrust
- appraisal of events into relationship meaning

A Layer may cache, index, or translate **for performance**; it may not decide **for meaning**.

---

## 4. Boundary B — Layer ↔ Environment

Where the world's own interfaces stop. Everything environment-native lives **behind** this line,
inside the Layer and the environment:

- engine objects and handles: entity refs, block coordinates, item ids, component pointers;
- engine callbacks and event loops, ticks, scheduling, save/load, session/network layers;
- engine-specific identity, authentication, and permission models;
- the environment's own opaqueness: anything the world refuses to expose.

Layer duties at this boundary:

1. **Translate** environment facts into protocol events/observations without interpretation.
2. **Map** `ActionCall`s onto real environment operations, or refuse.
3. **Probe and declare** capabilities instead of assuming them (the world is not ours to change).
4. **Return the world's answer**, including "this world cannot express that".
5. **Report verifiability**: whether an action's outcome can be checked against real state
   (deterministic) or must be taken on trust (probabilistic). This feeds guardrail design and
   the World View Taxonomy's Verifiability axis.

> Core-facing consequence: an action the environment cannot express is a **normal outcome**, not
> an error. Core must be able to handle a refusal and choose another intent.

---

## 5. Capabilities: Common + Environment-Specific

Do **not** compress different worlds into one lowest-common-denominator interface. The Layer
Protocol defines a small common vocabulary and lets each Layer extend it:

```text
Macha-facing common capability classes
        ├── perceive / query state
        ├── move
        ├── interact (with an object or entity)
        └── communicate

Minecraft Layer adds        Skyrim Layer adds         Cyberpunk Layer adds
        ├── place_block             ├── cast_spell             ├── quickhack
        ├── break_block             ├── shout                  ├── cyberware
        └── craft                   └── equip                  └── vehicle
```

The goal is **not** to make different worlds the same world. It is to let Macha enter different
worlds through a stable boundary while each world keeps its own nature.

Capability manifest (minimum fields per operation): `name`, `args schema`, `preconditions`,
`expected effects`, `observability` (can the effect be verified?), `latency/cost`,
`permission scope`. The manifest is a **claim the Layer probes and then asserts**, not a wish list.

---

## 6. The Minimal Layer

If only Minecraft were connected today, this is the smallest thing that could prove the
abstraction is real (detail in
[`../research/plans/minecraft-layer-validation-plan.md`](../research/plans/minecraft-layer-validation-plan.md)):

| # | Deliverable | Why it is minimal |
|---|---|---|
| M1 | Agent binding: which entity/window this Core instance is | without it there is no perspective |
| M2 | Typed event stream (uninterpreted, with provenance) | without it Core cannot perceive anything |
| M3 | State query limited to the agent's observation window | without it the boundary leaks |
| M4 | Capability manifest with probed support | without it Core will hallucinate abilities |
| M5 | Action executor mapping `ActionCall` → environment op | the outward half of the boundary |
| M6 | Structured action result incl. refusal + state delta | makes consequences real |
| M7 | Session lifecycle (connect / disconnect / timeout / reconnect) | environments die and restart |
| M8 | Verifiability report per capability | sets guardrail strategy |
| M9 | Replayable transcript (observations + actions + results) | makes the boundary auditable and testable |

**Proof conditions (what "the abstraction holds" means):**

1. The same Core build runs against the Minecraft Layer **and** a trivial simulator Layer with no
   Core changes.
2. A second author can implement the Protocol from the specification plus the conformance kit,
   without reading the first Layer's code.
3. Replacing the Layer changes observations and executable actions, but never memory, persona,
   or decision logic.

**Explicitly not needed yet:** a universal Layer framework, multi-engine abstraction layers,
Unreal/Unity plugins, robotics buses, or an abstraction over capabilities that no connected
world has ever needed.

---

## 7. Repository Organization (Proposed)

```text
macha/                    Macha Core + the Layer Protocol specification + conformance kit
layers/                   in-repo Layer workspace — one build root
├── kit/                  shared, environment-agnostic
│   └── protocol/ runtime/ transport/
├── minecraft/            Minecraft Layer (only module with paper-api)
├── simulator/            fake environment — control condition
└── testclient/           vertical-slice test client
macha-minecraft/          later: layers/minecraft/ moved out as its own repo
macha-skyrim/             later, independent
```

> Layout decided 2026-09-14:
> [`../papers/notes/accepted/decision-layers-directory-layout.md`](../papers/notes/accepted/decision-layers-directory-layout.md)
> (`layers/kit/` grouping; split triggers T1–T4). The `kit/` regroup landed 2026-09-14
> (commit `ead3a3d`), with the boundary guards re-pointed to `kit/*`.

- The **specification** lives with Core (one owner, one source of truth) but is versioned
  separately from the Core implementation.
- **Layer implementations** live outside this repository so that Core cannot drift toward any
  one of them, and so a Layer can be released without a Core release.
- A **simulator Layer** stays in-repo: it is the cheapest way to test the boundary without
  Minecraft's dependencies, and it is the control condition for the proof conditions above.
- Early stage may keep everything in one repository with strict package boundaries; the split
  into separate repositories is a decision to revisit, not a day-one requirement. Full rationale:
  [`../papers/notes/drafts/environment-integration-layer.md`](../papers/notes/drafts/environment-integration-layer.md) §E.
  File-level structure for the first Layer (module graph, dependency rules, per-module files):
  [`../research/plans/minecraft-layer/04-project-structure.md`](../research/plans/minecraft-layer/04-project-structure.md).

> Note on the Layer-first sequence: until the real Core exists, `macha/` holds only the **Stub
> Core** (a test harness, not a product). A Layer is written against the **Protocol**, never
> against the stub's implementation — the stub is expected to be replaced wholesale in Phase 3.

---

## 8. The Canonical Boundary Diagram

```text
Macha
   │   owns: memory · persona · motivation · reasoning · planning · appraisal ·
   │         guardrail · decision log · the agent's own state
   │   must not contain: engine types, engine ids, ticks, sockets, block coordinates
   │
   │  ── Layer Boundary (the Layer Protocol) ──────────────────────────────
   │     downward: ActionCall (typed intent, may be refused)
   │     upward:   Observation · Event · State · Capability · Action Result
   │     never:    pre-interpreted meaning (down/up), engine handles (up)
   ▼
Layer
   │   owns: translation · environment connection · capability probing ·
   │         state normalization · refusal reporting · verifiability report ·
   │         the only environment-specific code in the stack
   │   must not contain: memory · persona · motivation · planning · social cognition
   │
   │  ── Environment Boundary (the world's native interface) ──────────────
   │     the environment's own API/handles/callbacks/tick/permissions stay here
   ▼
External Environment
       owns: rules · state · history · entities · causality · the right to refuse
```

| Side | Responsible for | Never responsible for |
|---|---|---|
| **Macha Core** | cognition, meaning, memory, intent, guardrail | environment quirks, engine calls, world rules |
| **Layer** | translation, connection, capability truth, consequences | thinking, interpreting, remembering |
| **Environment** | world rules, actual state, actual outcomes | understanding the agent's reasons |

---

## 9. Anti-Patterns

1. **Minecraft in the Core** — `if game == "minecraft": ...` anywhere in `src/macha/`.
2. **Cognition in the Layer** — trust, hostility, memory, "he stole from me" living in the Layer.
3. **Universal mega-interface** — collapsing all worlds into `move() / talk() / attack()` and
   losing each world's real expressive surface.
4. **Premature Layer framework** — designing abstraction for Skyrim, Cyberpunk, Unreal, Unity
   and robotics before one real Layer has been built.
5. **Manifest by assumption** — declaring capabilities from documentation instead of probing the
   running environment.
6. **Silent refusal** — the Layer discards an inexpressible action instead of returning it as a
   result; Core then believes a false world.

---

## 10. Open Questions for the Team

1. Is the exchange set (Observation / Event / Action / Action Result / Capability) minimal, or does
   one of them collapse into another?
2. Does **State** need to be a separate exchange, or is it just a query answered as an
   Observation?
3. Where does the **agent's own state** (position, inventory, status) live — Core, Layer, or split
   by field? Who is the source of truth?
4. What is the minimum form of the capability manifest that still prevents hallucinated abilities?
5. Should the Protocol carry **time** (engine tick vs. agent time), and if so in what units?
6. Is the simulator Layer an acceptable substitute for a second real environment when testing the
   Protocol's generality?
7. What is the smallest conformance kit that lets an independent author implement a Layer?
