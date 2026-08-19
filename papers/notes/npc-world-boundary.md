# Where Is the Boundary Between the NPC and the World

> Status: Open discussion note.
> Question: Isn't the NPC part of the world? If so, why do we still need to discuss a boundary?
> Goal: Advance this boundary question from "spatial position" to the level of "experience and architecture."

---

## 1. Why This Question Matters

If we ask "where is the boundary between the NPC and the world," the most common answer is:

> The NPC is inside the world; the world is the environment, and the NPC is an entity within the environment.

This answer holds spatially, but is almost meaningless experientially. The player does not consider an NPC real just because it has coordinates.

The real question is:

> When does the player feel "this NPC is just a prop of the world," or "this NPC has melted into the world and lost itself"?

So the boundary between NPC and world is not a geometric line, but an **experiential boundary and a causal boundary**.

---

## 2. Four Possible Boundaries

### 2.1 Spatial Boundary

The NPC is an entity with a position and a body, visible and touchable.

This is the shallowest boundary. It only solves "where is the NPC," not "who is the NPC."

### 2.2 Informational Boundary

What the NPC knows, and what the world knows.

In traditional games, the NPC's informational boundary is usually very rigid: the NPC only knows what the script tells it; even if the world state has turned upside down, the NPC may know nothing.

This boundary is too thick, and will isolate the NPC from the world.

### 2.3 Intentional Boundary

The NPC has its own goals, desires, and stance; the world has only rules, no desires.

This is an important basis for "the NPC is an other." Without an intentional boundary, the NPC is just an executor of world rules.

But the intentional boundary cannot be too strong: if the NPC's goals are completely detached from the world state, it becomes a floating ghost.

### 2.4 Experiential Boundary

The player can perceptually detect where "the NPC's life" ends and "the world's machinery" begins.

This is the most critical boundary.

- When the NPC says something completely unrelated to war, economy, or weather, the player feels the boundary is too thick: the NPC is isolated from the world.
- When the NPC is just a price tag, just a projection of a panic value, the player feels the boundary is too thin: the NPC is dissolved by the world, with no self.

---

## 3. The Boundary We Advocate: A Transformation Layer / Interface

Rather than seeing the boundary as the "NPC's shell," it is better to see it as:

> The transformation layer between world state and character experience, and the transformation layer between character intent and world effect.

More concretely, the boundary between NPC and world is two things:

1. **Perception interface**: how the world becomes the NPC's experience.
2. **Action interface**: how the NPC's intent becomes the world's consequences.

If these two interfaces are transparent and consistent, the player cannot perceive the boundary; if they break, the player sees "the NPC and the world are not the same thing."

---

## 4. Two Failure Modes

### Mode One: Boundary Too Thick — the NPC Is Isolated from the World

Typical manifestations:

- A war has broken out, yet the merchant still sells at peace-time prices;
- The player just slaughtered the village, yet the village-gate NPC still says "what nice weather today";
- The NPC's memory exists only in dialogue, and does not enter the world state.

This is the failure of traditional scripted NPCs. Its problem is not "not smart enough," but a boundary too thick — the world cannot pass through it into the NPC.

### Mode Two: Boundary Too Thin — the NPC Is Dissolved by the World

Typical manifestations:

- The NPC is just a projection of a panic value, with no stable persona;
- The NPC's memory can be completely overwritten by the world state;
- The NPC has no ability to refuse, no private stance;
- The player feels "this NPC is just an expression of the world."

This is the failure that AetherFlow-style "macro collapse" may produce. Its problem is not "not real enough," but a boundary too thin — the NPC loses itself.

---

## 5. The Correct Position

The boundary between NPC and world should lie at:

> The world state can enter the NPC's experience, but must pass through the NPC's stance, memory, and persona for interpretation; the NPC's intent can change the world, but must be constrained by world rules and consequences.

In other words:

- The world cannot directly "pass through" the NPC;
- The NPC cannot "float" detached from the world;
- The boundary should be like a semi-permeable membrane: world information can come in, but is colored by the NPC; the NPC's actions can go out, but are filtered by world rules.

---

## 6. Relationship with AetherFlow and Macha

### AetherFlow's Inspiration

AetherFlow turns "NPC present / absent" into a dynamic boundary:

- When absent, the NPC dissolves into the world;
- When present, the NPC collapses out of the world.

This idea is clever, but it places the boundary on the "player's field of view," not on the "NPC's self." If handled poorly, the NPC becomes a temporary projection of the world, losing continuity.

What AetherFlow should truly retain is:

> The world's information propagates non-uniformly; the NPC's experience is local and delayed.

What should not be retained is:

> The NPC only exists when it is seen.

### Macha's Inspiration

Macha's core is to give the NPC a stable cognitive nucleus:

- Private memory;
- Stable persona;
- Bounded action;
- Observable decision-making.

All of these build a correct boundary between "the world too thick" and "the world too thin."

Macha's interfaces (Perception / Memory / Reasoning / Action) are essentially the engineering expression of this boundary:

- Perception: how the world enters the NPC;
- Memory: how it is preserved and interpreted after entering;
- Reasoning: how the NPC forms its own intent;
- Action: how intent returns to the world.

---

## 7. Significance for the Paper

The question "where is the boundary between the NPC and the world" can become the core argument of the "necessity of authenticity" section:

> An authentic NPC is neither an independent entity unrelated to the world, nor a projection completely dissolved by the world. Between the authentic NPC and the world there is a transparent semi-permeable membrane: the world can influence it, but it retains its own interpretation; it can influence the world, but the world retains its own rules.

This exactly echoes the "tension system" we proposed earlier:

- The NPC needs to be connected to the world, otherwise it is a puppet;
- The NPC needs to have a boundary with the world, otherwise it has no self.

---

## 8. Questions for the Team

1. Is the "semi-permeable membrane" metaphor precise enough, or does it need a more formal definition?
2. How much of the NPC's private memory should be allowed to "leak" into the world? For example, would the NPC's fear automatically become the world's panic field?
3. In multiplayer games, should the NPC boundary seen by each player be consistent?
4. Can AetherFlow's "dissolve when absent" only be a performance optimization, not an authenticity design?
5. Are Macha's interfaces already sufficient to express this boundary, or is a "world-state Provider" standard needed?
