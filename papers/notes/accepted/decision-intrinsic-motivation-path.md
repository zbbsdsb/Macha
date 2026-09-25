# Decision: Macha's Intrinsic-Motivation Path (Identity–Desire + Existence Conditions as Core)

> Status: **RATIFIED — decision record.** Decided 2026-09-25 by the project owner.
> Recorded per [`../../../docs/team-workflow.md`](../../../docs/team-workflow.md): this is a **project design
> decision**, not a paper conclusion. It defines **no data structures and no APIs**, and it records
> **no implementation** — nothing described here exists in code yet.
>
> Related: [`../../../docs/architecture.md`](../../../docs/architecture.md) §1.5 (where a drive lives) ·
> [`../../../research/paths/02-intrinsic-motivation/README.md`](../../../research/paths/02-intrinsic-motivation/README.md) ·
> [`../../../research/questions/Q-01-drive-signal.md`](../../../research/questions/Q-01-drive-signal.md) ·
> report survey (research material, not our choice):
> [`../../../research/paths/02-intrinsic-motivation/report-four-build-paths.md`](../../../research/paths/02-intrinsic-motivation/report-four-build-paths.md)

---

## 1. Decision

**Macha's intrinsic motivation is built from persistent internal state and existence conditions.**

### 1.1 Path selection (vs. the four paths surveyed in the report)

| Report path | Macha status |
|---|---|
| **1. Intrinsic reward / information-theoretic** (curiosity, novelty, empowerment, learning progress) | **Research reference only — not V1 core.** Kept as a future extension. |
| **2. Cognitive architecture / Identity–Desire** | **Core** |
| **3. Existence conditions / homeostasis** | **Core** |
| **4. Social intrinsic motivation** | **Important auxiliary** — an extension of the *same* system, not a second system beside it |

The report's four-path survey stays in the repo as research material; this table is Macha's *choice*
and must not be read as a finding of that survey.

### 1.2 Core chain

```text
World → Perception → Internal State → Drive/Tension → Goal Generation → Planning → Action → World Change → Internal State
```

The NPC's internal state carries **Belief, Desire, Intention and Identity**. Internal state produces
**Drive / Tension**; Drive/Tension — **not** an external task — drives **Goal Generation**.

### 1.3 Second core path: existence conditions

Part of the drive comes from the pressure to keep existing and to keep its own state stable: safety,
resources, health, hunger, social relations. These are **not tasks**; they are continuously present
internal tension.

### 1.4 Drive ≠ Goal

**A drive is a sustained internal pressure. A goal is what the NPC generates in order to relieve that
pressure.** The two must never be written as the same thing (see §2).

### 1.5 Statement to quote verbatim

> Macha 的 NPC 不是"因为系统要求它探索，所以它探索"，也不是简单通过 curiosity reward 驱动行为。
> Macha 希望建立的是一种由持久内部状态产生的长期张力（long-term tension），张力经过 Desire、
> Identity、Social Relations 等结构转化为可能的目标，再进入规划与行动。

**One sentence:**

> **Macha 通过持久内部状态与存在条件产生长期张力，再由认知、身份和社会关系将张力转化为目标与行为。**

## 2. Term boundaries (must not be conflated)

| Term | What it is in this decision | What it is **not** |
|---|---|---|
| **Drive / Tension** | sustained internal pressure arising from persistent state (incl. existence conditions) | not a goal · not a task · not a reward signal |
| **Desire** | an internal-state structure that holds a preference | not a goal · not yet a plan |
| **Identity** | persistent structure (who this NPC is) that decides which tensions matter | not a persona prompt |
| **Intention** | a committed direction inside the internal state | not an executed action |
| **Goal** | generated in order to relieve a drive | not the source of the drive · not the drive itself |
| **Intrinsic reward** (curiosity / novelty / empowerment / learning progress) | a Path-1 mechanism, deferred | **not** the definition of Macha's drive |

## 3. Why

1. A curiosity-reward framing answers *"what should it explore next"*, not *"what does it want"*. Its
   signals (novelty, empowerment) have no natural satiation, which conflicts with a drive that must be
   **relievable** (the report itself notes the "noisy TV" problem and empowerment's conservative bias).
2. Paths 2 + 3 are the ones that give a **persistent internal state** and a **long-term tension** —
   the property our thesis cares about (`independence`).
3. Path 4 changes the *same* tensions (others' behaviour, cooperation, competition, norms feed the
   internal state and therefore the same Drive → Goal chain) instead of adding a parallel system.
4. Path 1 is **deferred, not rejected**: it is the cheapest to add later precisely because it plugs
   into goal scoring/selection rather than into the definition of a drive.

## 4. What this does not change

- **A Layer must not think** (`architecture.md` §0 rule 2): no motivation on the Layer side.
- **A drive adds no new box**: it stays a class of persistent state in the internal source, on the
  **weights** leg of IC's send-back, computed by an operator, used at output (`architecture.md` §1.5).
- Path 02's four boundary rules stand: drive lives in the Core-side internal source; self-generated
  goals pass IC's Chunk admission; a drive never changes facts; every drive is decayable, cappable,
  observable and killable.

## 5. Status — nothing here is implemented

`src/macha/` is still the non-cognitive skeleton (`architecture.md` §1.1 audit): there is **no**
persistent internal state, **no** drive, **no** goal generation, and no social-motivation mechanism.
This record fixes a direction only. Docs, PRs and demos must not describe any of it as existing.

## 6. Consequences and open items

1. **`Q-01` arms narrowed**: H-A (homeostasis) is core; H-D (connection) is auxiliary; H-B (learning
   progress) and H-C (empowerment) belong to Path 1 → **not V1 core** (kept for later). `Q-01`'s
   pre-registration block is still `<pending>`, so this decision narrows it before submission.
2. **Open — Path 2 has no hypothesis yet.** Every `Q-01` hypothesis is a *drive-signal source*; Path 2
   (cognitive architecture) is core but is a **holding/transformation structure, not a signal source**.
   Whether it needs its own hypothesis/arm must be decided **before** pre-registration.
3. **Open — "Internal State" is not yet located** in `architecture.md` §1.5, which names three
   send-back legs (facts / the agent's own version / weights) plus memory · relations · persona.
   Locating the internal state is an architecture question and is **not** settled by this record.
4. The report's Path-1 mechanisms remain in the survey (§1.1); they are not deleted from research.

## 7. Documents updated under this decision

- [`../../../docs/architecture.md`](../../../docs/architecture.md) — §1.5 states the adopted path
- [`../../../research/paths/02-intrinsic-motivation/README.md`](../../../research/paths/02-intrinsic-motivation/README.md) — §1.6 records the adopted path; §3 marks arm status
- [`../../../research/paths/02-intrinsic-motivation/report-four-build-paths.md`](../../../research/paths/02-intrinsic-motivation/report-four-build-paths.md) — survey separated from the choice (§10)
- [`../../../research/questions/Q-01-drive-signal.md`](../../../research/questions/Q-01-drive-signal.md) — arm status + Path-2 gap recorded
- [`../../../research/paths/README.md`](../../../research/paths/README.md) — path-02 index row
- [`../README.md`](../README.md) — notes index entry · [`../../../README.md`](../../../README.md) — navigation entry

## 8. Revisit conditions

1. A persistent internal state cannot be kept stable in practice (drift / instability) → re-examine
   whether Path 3's homeostatic tension alone is the implementable core.
2. V1 experiments show goal generation cannot be driven by tension **without** Path-1 progress signals
   → revisit the deferral of Path 1.
3. Social motivation turns out to need its own mechanism rather than feeding the same tensions →
   Path 4's "auxiliary" status is wrong.
