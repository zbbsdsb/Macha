# Determinate Status of the Paper

> Updated: 2026-08-16
> Note: Here we distinguish three states: "already written into the paper body and basically stable," "already formed a working conclusion but not yet entered the body," and "completely undecided."

---

## I. Already Written Into the Paper Body, Basically Stable

1. **The overall question**
   > Not analyzed from a technical-implementation angle, but asked from the player's perspective: what is the game agent we desire?

2. **Research stance**
   > The paper proceeds from the player experience, not along the FSM/BT/LLM technical-evolution line.

3. **The basic distinction of "sender / receiver"**
   - Source-domain decomposition deals with the sending end of information;
   - Field superposition deals with the receiving end of information;
   - One sends outward, one receives inward.

4. **The field difference between player and NPC**
   - The player simultaneously possesses the in-game field and the out-of-game field;
   - The NPC is usually only in the in-game field.

5. **Core judgment: the gap is a missing field, not missing information**
   > Adding perception, memory capacity, or behavior-tree nodes cannot automatically cross this gap.

6. **The preliminary direction of "authenticity"**
   > Authenticity is not to let the NPC know more, but to let the NPC possess a cognitive field that is clearly bounded, internally consistent, and understandable to the player.

---

## II. Drafted, But Needs Team Confirmation

1. **The position of field superposition in the paper**
   - Currently appears as the "first slice";
   - Whether to keep this position, or demote it to a smaller sub-mechanism, is not yet confirmed.

2. **The degree of formalization of field superposition**
   - The current body uses formulas and definitions;
   - The team may prefer a more conversational, less formula-heavy style.

3. **The transition from field superposition to "the necessity of authenticity"**
   - A transition paragraph is already written;
   - But the argumentative direction of "the necessity of authenticity" itself still needs confirmation.

---

## III. Already Formed a Working Conclusion, But Not Yet Formally Entered the Paper

These contents exist in `papers/notes/archive/conclusions-desired-agent.md` and have not yet been written into the paper body:

1. What the player desires is not an agent, but the world's response;
2. What the player desires is a "believable, changeable other that leaves consequences";
3. The five conditions: sees me, remembers me, is itself, is changed by me, exceeds me;
4. The player's desire for the agent is a tension system, not a capability list;
5. The failure of existing agents is relationship breakage, not insufficient intelligence;
6. The classification must add a "relationship axis";
7. The four relationship archetypes: witness, relation-holder, resistor, other.

These currently count only as "internal team-stage conclusions," not yet as determinate content of the paper.

---

## IV. Completely Undecided

1. How to write the "necessity of authenticity" section;
2. Whether the paper adopts "relationship gap" as the overall framework;
3. Whether the four relationship archetypes enter the paper, and how to name them;
4. Whether to write "the necessary tension";
5. Whether to write "the five guarantees of the standard skeleton";
6. Whether to add game-case slices;
7. Whether to add a formal dialogue with the four papers;
8. Whether the paper ultimately leans toward design theory or architecture standard;
9. Whether the paper title is finally retained;
10. Whether the core terms are all finalized (field superposition, cognitive field, relationship axis, relationship archetype, etc.).

---

## V. One-Sentence Summary

At present, only two things about the paper are truly determined:

1. We proceed from a player-perspective question;
2. "Field superposition," as the first slice, points out that the gap between player and NPC is a missing field, not missing information.

The rest remains in the state of "working notes" or "discussion drafts," and needs team confirmation before entering the body.

---

## VI. Literature Intelligence Layer (STORED)

> Updated: 2026-08-24
> The seven-domain literature sweep is complete. All dossiers live in
> `research/literature/` and are mapped to paper claims in
> `../../research/literature/00-literature-map-paper-gaps.md`. This layer is evidence, not yet paper content.

| Dossier | Domain | Serves paper claim | Status |
|---|---|---|---|
| [00-literature-map-paper-gaps.md](../../research/literature/00-literature-map-paper-gaps.md) | Synthesis | claim→dossier map + gap analysis | STORED |
| [01-formal-models-social-relations.md](../../research/literature/01-formal-models-social-relations.md) | Formal models | §6 computational model | STORED |
| [02-longitudinal-measurement.md](../../research/literature/02-longitudinal-measurement.md) | Measurement | §9 falsifiability | STORED |
| [03-HRI-relationship-tradition.md](../../research/literature/03-HRI-relationship-tradition.md) | HRI tradition | gap positioning | STORED (HOLD: RE-VERIFY tier pending) |
| [04-BDI-modern-agent-architecture.md](../../research/literature/04-BDI-modern-agent-architecture.md) | BDI + agent arch | §6 R↔S coexistence | STORED |
| [05-game-studies-interactive-narrative.md](../../research/literature/05-game-studies-interactive-narrative.md) | Game studies | §7 formal properties | STORED |
| [06-philosophy-phenomenology-relation.md](../../research/literature/06-philosophy-phenomenology-relation.md) | Philosophy | §8 projection objection | STORED |
| [07-failure-modes-negative-results.md](../../research/literature/07-failure-modes-negative-results.md) | Failure modes | §10 self-attack | STORED |

**Key findings that move Section IV items:**
- IV.2 (relationship gap as framework): strongly supported — dossier 05 corrects the "Façade failed on NLU" misreading; dossier 04 shows no system uses R as a control variable (Macha's slot).
- IV.4 (necessary tension): supported by dossier 06 (Buber I-It / Levinas refusal) and dossier 07 (randomness ≠ independence).
- IV.5 (five guarantees): the 3+2 primitives must survive the dossier-07 pre-destruction matrix before being fixed.
- IV.8 (design theory vs architecture standard): unresolved — dossier 04's Gap A (R as control variable) vs Gap B (R as drama control) is exactly this fork.

**Open action:** resolve RE-VERIFY tiers in dossiers 03/05/06/07 (secondary/aggregator sources → primary) before any citation.
