# Decision: Layer-First Sequencing (Minecraft Layer before Macha Core)

> Status: **RATIFIED — decision record.** Decided 2026-09-13 by the project owner.
> Recorded here per `../../docs/team-workflow.md` ("deviation requires a recorded decision in
> `papers/notes/` first"). This is a **project-sequencing decision**, not a paper conclusion.
> Related: [`../drafts/environment-integration-layer.md`](../drafts/environment-integration-layer.md)
> · [`../../../docs/architecture.md`](../../../docs/architecture.md)
> · [`../../../research/plans/minecraft-layer-validation-plan.md`](../../../research/plans/minecraft-layer-validation-plan.md)

---

## 1. Decision

**Build the first Environment Integration Layer (Minecraft) before building Macha Core.**

The first verifiable milestone is no longer "a minimal cognitive core." It is:

> **Layer Protocol v0 + a non-cognitive Stub Core + one real Minecraft Layer + a simulator Layer,
> with the abstraction's falsification criteria (V1–V5) evaluated.**

The real Macha Core (memory, appraisal, reasoning, reflection, planning, guardrail) is developed
**after** the Layer boundary has been shown to hold, and must then run against the same Layers
**unchanged**.

## 2. Why

1. **The boundary is the riskier half.** Cognition can be iterated in place; a boundary that is
   wrong is expensive to undo — by the time Core exists, every environment assumption has already
   leaked into it if no protocol was frozen first.
2. **The Layer is testable without cognition.** Observation encoding, capability probing, action
   execution, refusals and state deltas are all verifiable against a dumb counterpart. None of it
   needs memory or persona.
3. **Minecraft has the shortest path to real facts.** `docs/research/engineering_npc_architectures.md`
   §4.1 already identifies Mineflayer / `minecraft-protocol` as a ready-made "turn the game
   protocol into a programmable agent interface" layer — one that provides perception/action
   primitives and **no cognition**. That is exactly the shape of the thing we need to build.
4. **Capability facts arrive earlier.** What a real world will refuse (permeability, verifiability)
   is useful input to Core design rather than something Core discovers late.
5. **Reversible cost.** If the Layer track stalls, the loss is a protocol draft plus a stub — not
   a half-built cognitive core with the wrong interfaces.

## 3. What This Decision Does Not Change

- The calibration in `docs/architecture.md` stands: Core must not know which environment it runs
  in; **a Layer must not think** (no memory, persona, motivation, planning, social cognition).
- **V1 remains the falsifier**: if connecting an environment requires changing Core, the
  *protocol* is wrong. Layer-first makes this *harder* to satisfy, not easier — the temptation to
  hide cognition in the Layer is strongest when there is no Core.
- Minecraft remains a **Concrete Layer Test Case**, not the framework's identity.

## 4. Binding Constraints Introduced by the Reordering

| # | Constraint | Why it is binding now |
|---|---|---|
| C1 | **A Stub Core must exist before Layer coding starts.** Non-LLM, rule-based, consumes observations, emits `ActionCall`s. | Without a counterpart there is no boundary to test, only a bot to demo. It is also the discipline device that keeps cognition out of the Layer. |
| C2 | **The protocol must be transport- and language-agnostic** (JSON-RPC-shaped; MCP-compatible preferred). | Core is Python; a Mineflayer Layer is JS/Node. Otherwise the Layer language choices bind Core. Aligns with `docs/research/standards_interop.md` §188 (converge `ActionCall` on the Tool-Use shape). |
| C3 | **The Stub Core's action vocabulary must not contain environment verbs.** It emits common capability classes (`interact`, `move`, `communicate`, `query`); `place_block` belongs to the Minecraft Layer's manifest. | Otherwise the real Core inherits Minecraft's ontology through the stub. |
| C4 | **The simulator Layer is not optional.** | With Minecraft going first, the simulator is the only control condition; without it, three weeks of work proves "a bot runs," not "the abstraction holds." |
| C5 | **No real Core work until Phase 2 exits.** The stub may grow scripts and recordings, but not memory, persona, or reasoning. | Prevents the stub from silently becoming the Core, which would freeze the wrong interface by accident. |

## 5. New Phase Order (old → new)

| Old | New | Phase content |
|---|---|---|
| Phase 0 | Phase 0 | Repository initialization; Layer calibration |
| — | **Phase 1** | **Layer Protocol v0 + Stub Core + environment reconnaissance** |
| Phase 3B/3C | **Phase 2** | **Simulator Layer + Minecraft Layer + falsification (V1–V5)** |
| Phase 1 | **Phase 3** | Minimal Cognitive Core (must run unchanged on both Layers) |
| Phase 2 | Phase 4 | Character consistency and reflection |
| Phase 4 | Phase 5 | Multi-agent and evaluation |

Full detail: [`../../../docs/roadmap.md`](../../../docs/roadmap.md).

## 6. Known Risks and Mitigations

| Risk | Mitigation |
|---|---|
| The Layer over-fits to Minecraft because Minecraft defines the first manifest | Simulator Layer + C3 (Core-side vocabulary drawn from common capability classes) |
| The stub Core quietly becomes the Core | C5; the stub is explicitly disposable and its scripted policy is not promoted |
| Recruiting/demo pressure pushes the team to skip the protocol | The milestone is defined by V1–V5, not by in-game visuals; a playable MC bot is an accepted *by-product*, not the deliverable |
| Protocol churns once real Core needs appear | Protocol is versioned; Core-side needs are recorded as protocol questions rather than patched into Core (`environment-integration-layer.md` §I falsifiers) |

## 7. Revisit Conditions

This ordering is revisited if any of the following occurs:

1. The simulator Layer cannot be made cheap (its cost exceeds the Minecraft work it de-risks).
2. Environment reconnaissance shows Minecraft's exposed surface cannot support the minimal Layer
   (M1–M9) at all — i.e., the chosen interface stack is a dead end.
3. The protocol does not stabilize after two rounds of iteration against the Layer, in which case
   the abstraction claim itself, not the ordering, is what needs re-examination.

## 8. Documents Updated Under This Decision

- `docs/roadmap.md` — reordered phases (with the old → new mapping table)
- `research/plans/minecraft-layer-validation-plan.md` — gates G0–G2, Stub Core, timeline, transport constraint
- `docs/architecture.md` — Stub Core as the counterpart, language-agnostic transport note
- `docs/research/direction.md` — first milestone restated
- `README.md` — current sequencing
- `papers/notes/README.md` — index entry
