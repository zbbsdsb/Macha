# Development Roadmap

> Updated 2026-09-13 (revision 2): sequencing inverted to **Layer-first** per
> [`../papers/notes/accepted/decision-layer-first-sequencing.md`](../papers/notes/accepted/decision-layer-first-sequencing.md).
> The Layer definition lives in [`architecture.md`](architecture.md); the full-roadmap rework
> proposal (still `PENDING`) is [`../research/plans/roadmap-rework-draft.md`](../research/plans/roadmap-rework-draft.md).

## Phase Order Change

| Old | New | Why |
|---|---|---|
| Phase 1 Minimal Cognitive Core | **Phase 3** | Cognition can be iterated in place; a wrong boundary cannot |
| Phase 3 Layer Protocol + First Layer | **Phase 1–2** | The Layer is testable without cognition and produces capability facts earlier |
| Phase 2 Character Consistency | **Phase 4** | Depends on a real Core |
| Phase 4 Multi-Agent | **Phase 5** | Unchanged position relative to the rest |

---

## Phase 0: Repository Initialization (Current)

- [x] README, LICENSE, .gitignore
- [x] Basic project structure
- [x] Research document organization
- [x] Calibrate the Layer concept: Macha Core vs. Environment Integration Layer (`docs/architecture.md`)
- [x] Confirm the sequencing: Layer-first, Core later (decision record, 2026-09-13)
- [ ] Initialize Git and push to remote (if not yet executed)

## Phase 1: Layer Protocol v0 + Stub Core

The gate before any Layer code. Exit = the protocol is frozen for v0 **and** something dumb exists
to talk it.

### 1A. Layer Protocol v0 (specification, no engine)

- [ ] Specify the five exchange categories: Observation, Event, Action, Action Result, Capability
      (and decide whether State is a separate category or a query form)
- [ ] Specify the capability manifest: name, args schema, preconditions, expected effects,
      observability, cost, permission scope
- [ ] Specify refusal and side-effect reporting (an inexpressible action is a normal result)
- [ ] Specify provenance on every observation and event (actor / place / time / source)
- [ ] Specify the verifiability report per capability (deterministic check vs. trusted outcome)
- [ ] Specify the **transport**: language-agnostic, JSON-RPC-shaped, MCP-compatible preferred
      (Core is Python; a Mineflayer Layer is JS/Node — the transport must not bind either side)
- [ ] Write the conformance kit stub: what an independent author must pass to call a project "a Layer"

### 1B. Stub Core (the non-cognitive counterpart)

- [ ] Rule-based, no LLM, no memory, no persona: consume observations, emit `ActionCall`s
- [ ] Action vocabulary drawn from the **common capability classes only** — no `place_block`,
      `craft`, or any other environment verb may appear on the Core side
- [ ] Scriptable scenarios (recorded observation sequences → asserted action sequences)
- [ ] Explicitly disposable: it must not grow into the real Core (see decision record C5)

### 1C. Environment Reconnaissance (can run in parallel, starting immediately)

- [x] Fix the interface stack — **baseline set 2026-09-13 (tentative): Paper plugin in Kotlin**
      (Minecraft 26.2 / Java SE 25 / Kotlin 2.4.20 / Gradle 9.7.1 / HTTP+WS transport).
      Mineflayer stays documented as the out-of-process alternative.
      Technical plan: [`../research/plans/minecraft-layer/00-technical-foundation.md`](../research/plans/minecraft-layer/00-technical-foundation.md)
- [ ] Review the technical foundation before any implementation starts: boundary-hazard list
      (`00-technical-foundation.md` §G) + file-level structure
      ([`../research/plans/minecraft-layer/04-project-structure.md`](../research/plans/minecraft-layer/04-project-structure.md))
- [ ] Stand up the smallest live connection: world state + event stream from a real server
- [ ] Produce the **probed** capability list (not copied from documentation)
- [ ] Produce the verifiability report (what can be checked against real state vs. taken on trust)
- [ ] Produce the write-permission boundary (permeability) for this world

## Phase 2: Simulator Layer + Minecraft Layer (falsification of the abstraction)

- [ ] Build the trivial simulator Layer implementing Protocol v0 (control condition)
- [ ] Build the Minecraft Layer: the minimal Layer of `architecture.md` §6 (M1–M9)
- [ ] Probe capabilities instead of assuming them; publish the probed manifest
- [ ] Produce replayable transcripts (observations + actions + results) into `research/experiments/`

### Exit criteria — the abstraction is proven only if

- [ ] **V1** Connecting Minecraft required **zero** changes to Core (a protocol gap counts as failure)
- [ ] **V2** No Minecraft concept appears in Core (no block / chunk / tick / entity id)
- [ ] **V3** No cognition appears in the Layer (no memory, persona, motivation, planning, judgment)
- [ ] **V4** The same Stub Core runs on both the simulator Layer and the Minecraft Layer unchanged
- [ ] **V5** A second author can implement a Layer from the spec + conformance kit without reading
      the first Layer's code

> If any criterion fails, the fix is the **Protocol**, not the Core's identity.

## Phase 3: Minimal Cognitive Core

Replaces the stub. This is where the boundary earns its keep: the real Core must run against the
already-built Layers **without changing them**, and without learning any environment vocabulary.

- [ ] Define `Agent`, `Memory`, `Perception`, `Reasoning`, `Action` interfaces
- [ ] Implement long-term memory based on JSON/SQLite
- [ ] Implement a simple LLM call wrapper
- [ ] Pass a smoke test that "still remembers key facts after 5 rounds of dialogue"
- [ ] Run unchanged on both the simulator Layer and the Minecraft Layer (re-run V1/V4 with the real Core)
- [ ] Any Core-side environment assumption discovered here is filed as a protocol issue, not patched locally

## Phase 4: Character Consistency and Reflection

- [ ] Implement a reflection mechanism: generate persona summaries from experiences
- [ ] Add importance scoring and memory retrieval
- [ ] Add "character consistency" test scenarios
- [ ] Introduce human evaluation / automated evaluation scripts

## Phase 5: Multi-Agent and Evaluation

- [ ] Multi-NPC communication and collaboration
- [ ] Long-term stress testing
- [ ] Reasoning cost optimization
- [ ] Release a demonstrable v0.1 version

---

## Current Recommendation

1. **Start with Phase 1C recon today** — it is the only item with no dependency and it de-risks both
   other Phase 1 workstreams.
2. **Do not start Layer coding before 1A + 1B exist.** Without a frozen protocol the Layer invents
   the interface; without a stub counterpart there is nothing to test the boundary against.
3. **Do not build a Layer framework before a Layer exists.** Designing for Skyrim, Cyberpunk,
   Unreal, Unity and robotics now is abstraction with nothing to test it against.
4. **Do not let the first Layer shape the Core.** Minecraft validates the Layer abstraction; it
   does not define Macha.
5. **Do not let the stub become the Core.** Its action vocabulary staying environment-free is what
   keeps Phase 3 honest.
