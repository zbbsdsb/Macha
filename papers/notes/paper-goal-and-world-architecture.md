# Clarifying the Paper's Goal and World Architecture

> Status: Directional note for the team.
> Purpose: Return to the most original purpose of writing the paper, and avoid being carried away by the engineering question of "world-embedded computation network vs. character extension."

---

## 1. Why We Originally Wrote This Paper

We are not writing a "game-engine architecture paper," nor an "AetherFlow technical report."

Our original purpose was:

> From the player's perspective, answer: what is the game agent we desire? Why do existing agents break immersion? What should a standard skeleton guarantee?

In other words, the core contribution of this paper is to **redefine the problem**, not to give a final implementation.

---

## 2. "World-Embedded Computation Network" vs. "Extension as a Character" Is a False Dichotomy

The team's current struggle is:

- Approach A: embed the computation network into the world itself;
- Approach B: first do Macha well (character cognition), then leave a large interface layer to connect to the natural world.

But if our ultimate goal is an "engaging world," these two approaches are not truly opposed.

In an engaging world:

- The world must have independent causal continuity (war, economy, rumor, natural change do not vanish just because the NPC is absent);
- The NPC must be a local interpreter of the world's causality (the same world event is experienced differently by different NPCs);
- The player feels the world through the NPC, but the world cannot exist only in the NPC's eyes.

So:

> The world is not "another system outside the character," and the character is not "an extension of the world." They are two expressions of a causal fabric at different scales.

The real design question is not "put the network in the world or in the character," but:

> Can the interface between world and character let causality flow bidirectionally, while preserving the character's stable self?

---

## 3. Pragmatic Suggestions for Macha

Although conceptually the two are inseparable, engineering must have a starting point.

Our suggestion is:

1. **Do Macha well first**: define the NPC's cognitive core, memory, identity, boundaries, and action interface.
2. **Meanwhile reserve a "world-state Provider" interface**: do not implement a large world simulation first; only define how the world provides information to the NPC and how the NPC exerts influence on the world.
3. **The world-embedded network can be a later experiment**: AetherFlow's "resource-rumor-organization" can serve as one implementation of this Provider, but it is not Macha's core.

This way, the paper will not become engine design, nor will Macha become an empty shell without a world.

---

## 4. How the Social World and the Natural World Collide

This question also needs re-examination.

The traditional approach treats "natural information" and "social information" as two independent sources, then fuses them with weights. We have pointed out in "field superposition" that this is the sender perspective, not the receiver perspective.

But from the world itself, the natural and the social are not two parallel worlds, but deeply entangled:

- Drought (natural) leads to famine (social);
- Famine leads to refugees (social);
- Refugees assault the border (social) and lead to war (social);
- War destroys the land (natural).

So:

> The collision of the natural world and the social world first occurs in the world's causal chain, and only then is interpreted within the cognitive fields of NPC and player.

Macha does not need to make the "natural world" and the "social world" into two independent systems. It needs a unified world-state description, so that the NPC can read both natural and social consequences simultaneously, and interpret them with its own stance.

---

## 5. How the Paper Should Be Written

Stop struggling over "world network vs. character extension." The paper should be written as:

1. **Overview**: What the player desires is not a smarter NPC, but a world that responds to them.
2. **Field superposition**: The player and NPC stand in different positions when interpreting the same event.
3. **The necessity of authenticity**: Authenticity comes from the semi-permeable membrane between NPC and world — the world can influence the NPC, the NPC retains its own interpretation; the NPC can influence the world, the world retains its own rules.
4. **Relationship gap**: The NPC needs to see, remember, refuse, be changed, exceed the player, and be causally connected to the world.
5. **The meaning of the standard skeleton**: Macha is not a world simulator, but a standard that guarantees the "world-character interface" holds.

AetherFlow can appear in the paper, but only as "one possible engineering direction," not as the paper's main body.

---

## 6. One Sentence for the Team

> We write the paper not to prove "we can build a complex world," but to prove "what kind of relationship should truly exist between player and NPC, and why existing technology has never satisfied it."

Whether the world-embedded network or character extension is a later implementation-stage question. At the paper stage, first answer: **what should that boundary be.**
