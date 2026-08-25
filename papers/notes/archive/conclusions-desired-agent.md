# Current Conclusions on the "Game Agent We Desire"

> Version: v0.1 (tentative conclusions, for the team to continue testing)
> Status: Active
> Prerequisites:
> - [what-we-desire-in-game-agents.md](what-we-desire-in-game-agents.md)
> - [four-papers-boundary-and-fusion.md](four-papers-boundary-and-fusion.md) (archived)

---

## 1. Conclusions That Can Be Written Down at the Current Stage

### Conclusion One: What the Player Desires Is Not an "Agent," but the "World's Response"

We shifted the question from "what capabilities should an agent have" to "how does the player want the world to treat them."

The agent is merely the interface through which the world becomes responsive. What the player truly needs is:

- The world has seen me;
- The world has remembered me;
- The world has evaluated me;
- My actions have changed the world;
- The world does not revolve entirely around me.

Therefore, the primary question for evaluating an agent is not "is it smart," but "has it made the world respond?"

### Conclusion Two: What the Player Desires Is a "Believable, Changeable Other That Leaves Consequences"

This sentence can be broken into five conditions:

1. **It sees me**: Its reaction targets my current state, not a generic template.
2. **It remembers me**: It remembers what matters in the relationship, and allows trivialities to be forgotten.
3. **It is itself**: It has boundaries, can refuse, and cannot be arbitrarily rewritten by me.
4. **It can be changed by me**: My actions leave traces on it, and change has a cost.
5. **It exceeds me**: It has its own schedule, relationships, and behavior, and does not exist entirely for me.

Lacking any one of these, the player will feel the character is "not real."

### Conclusion Three: The Player's Desire for the Agent Is a Tension System, Not a Capability List

These requirements conflict with one another:

| Tension | Consequence of Over-Leaning to One Side |
|---|---|
| Responds to me vs. independent of me | If it only responds to me, it becomes furniture; if it is only independent, I cannot build a relationship with it |
| Remembers me vs. allows forgetting | If it remembers everything, it seems a database; if it forgets the key things, it seems a betrayal |
| Stable vs. malleable | If completely stable, it has no life; if arbitrarily malleable, it has no self |
| Predictable vs. surprising | If completely predictable, it is a mechanism; if completely surprising, it is incomprehensible |
| Belongs to the world vs. serves gameplay | If it belongs entirely to the world, the game cannot proceed; if it serves gameplay entirely, it is just a quest button |

So a "good agent" is not one with the highest score on some metric, but one that maintains stability among these tensions. This is also why no single technological upgrade alone can solve the "sense of authenticity."

### Conclusion Four: The Failure of Existing Agents Is Essentially "Relationship Breakage," Not "Insufficient Intelligence"

We re-describe common failures in the language of relationships:

- "It didn't see me": The player's state changed, but the NPC's reaction did not.
- "It remembered the wrong things": The NPC remembers trivial dialogue but forgets a key promise.
- "It has no self": The player can arbitrarily make the NPC change its stance or forget its taboos.
- "It exists only for me": When the player is absent, the NPC has no life; the moment the player appears, all NPCs start serving the player.
- "It has nothing to do with the world": What the NPC says has no causal connection to space, time, economy, or war state.

This is closer to the player's actual experience than "model hallucination," "insufficient context," or "too-weak reasoning."

### Conclusion Five: The Classification Must Add a "Relationship Axis"

The existing classification axes all have value, but they are all external perspectives:

- Technical axis: how it is implemented;
- Source axis: where the information comes from;
- Role axis: what function it serves in production;
- Mechanism axis: whether the gameplay holds up after removing AI.

We advocate adding an axis that starts from the player:

> Which relationship need of the player is this agent satisfying?

We initially propose four relationship archetypes:

1. **Witness**: Makes the player feel "the world has seen me."
2. **Relation-holder**: Makes the player feel "my actions have left a history on others."
3. **Resistor**: Makes the player feel "the world has rules, costs, and refusals."
4. **Other**: Makes the player feel "there is a life here that does not revolve entirely around me."

These four archetypes are not mutually exclusive labels, but relationship attributes that the same NPC can possess simultaneously in different proportions.

### Conclusion Six: "Field Superposition" Is a Slice, Not a Total Framework

Field superposition is currently best at explaining:

> When the player and NPC interpret the same event, they stand in different positions.

It belongs to an interpretive mechanism between "seeing" and "worldliness."

But it cannot alone explain:

- Why the NPC should remember something;
- Why the NPC should refuse;
- How the NPC is changed;
- How the NPC exceeds the player.

Therefore, it should be retained as an important slice of the paper, not elevated into the whole picture.

---

## 2. Tentative Definition at the Current Stage

> **The game agent the player desires is not an object that is "more human-like," but an other constrained by world rules, possessing its own boundaries, able to leave understandable consequences from the player's actions, and thereby making the world seem responsive.**

This definition has three key points:

1. **Constrained by world rules**: It cannot be a floating dialogue window.
2. **Possessing its own boundaries**: It must be able to refuse and maintain itself.
3. **Leaving understandable consequences**: The player can understand how their actions affected it and the world.

---

## 3. Direct Implications of These Conclusions

### For the Paper

The paper should no longer write "how to make the agent smarter," but should write:

> How to redefine and cross the game-agent gap starting from the player relationship.

"Field superposition" can enter the paper as the first slice, but afterward it needs to expand into a more complete relationship gap.

### For the Macha Architecture

The goal of the standard skeleton is no longer "to do memory, reasoning, and action modules well," but to provide five kinds of relationship guarantees:

1. The guarantee of being seen;
2. The guarantee of being remembered;
3. The guarantee of having boundaries;
4. The guarantee of being changeable;
5. The guarantee of not belonging entirely to the player.

The technical modules are merely the means to deliver these guarantees.

### For Evaluation

We should not only ask "is the NPC's answer correct," but should ask:

- Did it react specifically to my state change?
- Did it remember what matters in the relationship?
- Did it refuse when it should have refused?
- Did it undergo observable change because of my actions?
- Does it have behavior that does not exist entirely for me?

---

## 4. What We Still Have No Conclusion On

1. Which is the more fundamental concept: "the world's response" or "the other"?
2. Are the four relationship archetypes sufficient? Do we need to add "judge" or "guide," etc.?
3. Must all five conditions exist simultaneously, or do different game types only activate part of them?
4. Should "field superposition" be the first slice of the paper, or a sub-mechanism of a larger relationship framework?
5. How to turn the "relationship axis" into an operable, measurable classification system, rather than another pile of pretty words?

---

## 5. Next-Step Suggestions

Rather than writing the paper body first, run a small experiment:

> Pick 3–5 game NPC cases that players universally consider "authentic" or "inauthentic," and use the "five conditions + four relationship archetypes" to explain why they succeed or fail.

Only if this relationship language can clearly explain concrete cases will our conclusions truly stand; if it cannot, we will know where revision is needed.
