# Boundary Probing of Four Papers and Idea Fusion

> Status: Discussion draft.
> Goal: Without overturning the four papers or piling their conclusions together, first probe where each paper "stops explaining," then attempt to fuse their boundaries with Macha's own problem.
> Our own question: From the player's perspective, what is the game agent we desire?

---

## 1. Method of Boundary Probing

For each paper, ask only four questions:

1. What does it define an agent as?
2. Which part of the player's desire does it answer?
3. Where does it stop?
4. What can it give us? What can it not give us?

---

## 2. Paper One: Generative Agents (2304, Smallville)

### What It Defines an Agent As

A generative agent with a memory stream, reflection, and planning capabilities, living continuously in a shared sandbox.

### Which Part of the Player's Desire It Answers

- **It has its own life**: The agent has a schedule, relationships, and spontaneous behavior.
- **It remembers things**: The memory stream and reflection give behavior temporal continuity.
- **It is connected to the world**: The relationships among 25 agents emerge into information propagation and social coordination.

### Where It Stops

- It is an "observed sandbox," not a "relationship field between player and NPC."
- The player is not the center; in fact the player is basically absent.
- There is no win/lose, goal, or rule adjudication; social emergence is not the same as gameplay.
- The evaluation criterion is "does the observer believe," not "does the player feel responded to."

### What It Gives Us

It proves one thing: **if an agent has memory, reflection, and planning, the player may indeed treat it as a continuously existing other.**

What it cannot give is: how this other responds to me, refuses me, remembers me, or is changed by me. It provides half of "the other," missing the other half of "the relationship."

---

## 3. Paper Two: Hu et al. (2404, LLM Game-Agent Survey)

### What It Defines an Agent As

A system composed of memory, reasoning, and a perception-action interface, which can be decomposed, combined, and evaluated.

### Which Part of the Player's Desire It Answers

- It provides the engineering base for "it sees me, it remembers me, it acts."
- The challenge-centered taxonomy indirectly acknowledges: in different games, the player's core requirements for the agent differ.
  - Action games need speed;
  - RPGs need character fidelity;
  - Adventure games need world state;
  - Sandboxes need self-directed goals.

### Where It Stops

- It is a system perspective: everything is reduced to components and challenges.
- It does not answer "why character fidelity matters," only says "RPGs need character fidelity."
- It takes game genre as the highest classification, but does not take the type of relationship between player and NPC as a classification.

### What It Gives Us

It gives Macha a "body": memory, reasoning, perception, action.

It cannot give the "soul": what do these components serve? What experience does the player want from them?

Fusion point: We can keep its four modules, but add a relationship-goal layer above the modules — the same memory system serves a "witness" or a "resistor" with different implementation strategies.

---

## 4. Paper Three: Gallotta et al. (2402, LLM and Games Survey)

### What It Defines an Agent As

A functional unit assuming some role in the game ecosystem: player, NPC, GM, judge, designer, analyst, etc.

### Which Part of the Player's Desire It Answers

- It acknowledges that an agent can stand in different positions in the game.
- It expands the NPC from "enemy" to richer ecosystem roles such as GM, assistant, mechanism, commentator, etc.

### Where It Stops

- It answers "what work AI can do in the game," not "what relationship occurs between the player and it."
- The NPC role is severely compressed internally: a witness, a resistor, and an other are completely different relationships, yet in this paper they are all called NPC.
- Its breadth makes it hard to keep probing downward into experience.

### What It Gives Us

It provides a "position": where the agent stands in the game ecosystem.

It cannot give "relationship": two NPCs standing in the same position may have completely different relationships with the player.

Fusion point: Keep the role axis, but cut one more slice — a relationship axis — beneath the role. The NPC is not the endpoint, but the container where relationship archetypes occur.

---

## 5. Paper Four: AI-Native Games (2607)

### What It Defines an Agent As

It does not define an agent; it defines gameplay: whether the core loop collapses after generative AI is removed.

### Which Part of the Player's Desire It Answers

- **The world has rules**: It emphasizes semantic adjudication; AI can judge whether the player's open-ended behavior conforms to world rules.
- **The world does not revolve entirely around the player**: Multi-agent simulation and AI GM both create the player's sense of "non-centrality."
- **Gameplay needs stability**: Mechanical invariants and a generate-verify pipeline ensure the player can build a mental model of world rules.

### Where It Stops

- It cares about "does this gameplay depend on AI," not "what relationship exists between player and NPC."
- The G/N axis is a mechanism axis, not a relationship axis. N4 semantic adjudication and N5 multi-agent simulation differ greatly mechanistically, yet the player desire they serve may overlap.
- It basically does not discuss long-term memory and character consistency; it cares about mechanical stability, not relationship history.

### What It Gives Us

It provides "rules" and "worldliness": only when an agent is embedded in a rule system that can be adjudicated, verified, and has consequences, will it not degrade into a chat window.

It cannot give "relationship memory": it knows semantic adjudication matters, but does not ask "must the adjudication be understood, remembered, and believed by the player."

Fusion point: Its "removal test" can be transformed into a "relationship removal test" — if the NPC's memory, refusal ability, or own life is removed, will the player's trust in the world collapse?

---

## 6. Conclusions of the Boundary Probing

The four papers respectively cover:

| Paper | What It Provides | Where It Stops |
|---|---|---|
| 2304 | An agent that can live continuously, remember, and reflect | Sandbox observation, not player relationship |
| 2404 | A decomposable cognitive system and engineering challenges | System perspective, not experience perspective |
| 2402 | The agent's position in the game ecosystem | Functional role, not relationship type |
| 2607 | The rule conditions for AI as the gameplay core | Mechanism ontology, not relationship history |

Together they answer one question:

> **What should a believable game agent be composed of, where should it stand, and what rules should it depend on?**

But they do not answer:

> **What does the player want to happen between themselves and this agent?**

This is where Macha can enter.

---

## 7. A Cautious Fusion Attempt

Without overturning any paper, put them into the same structure:

```text
Player-relationship layer (what Macha must supply)
  The player wants to be seen, remembered, refused, changed, exceeded
        ↑
Gameplay-rule layer (2607)
  Is this agent embedded in the core loop? Is it adjudicated by world rules?
        ↑
Ecosystem-position layer (2402)
  What role does this agent assume in the game?
        ↑
Cognitive-architecture layer (2404)
  How are memory, reasoning, perception, action assembled?
        ↑
Prototype-evidence layer (2304)
  Can this assembly produce continuously believable behavior?
```

### A Tentative Definition of "Game Agent" After Fusion

> A game agent is an entity whose body is cognitive architecture, whose position is an ecosystem role, whose boundary is gameplay rules, and which must prove its existence within the player relationship.

- 2304 proves the "body" can run;
- 2404 specifies how to build the "body";
- 2402 says where the "body" stands;
- 2607 says what rules the "body" must be embedded in;
- Macha must explain: **the "body" must ultimately make the player feel they are being responded to by the world.**

---

## 8. How to Proceed Next

1. First use these four papers to test our six desire questions: which are covered, which are not.
2. Then decide which layer of the fusion structure "field superposition" belongs to — the preliminary judgment is that it is an interpretive mechanism within the player-relationship layer.
3. Finally form the paper's boundary statement: we are not writing a fifth survey, but continuing to ask forward from where the four papers jointly stop.
