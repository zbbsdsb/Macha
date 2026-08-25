# In-Depth Discussion: What Is the Game Agent We Desire

> Status: Open discussion note, for the team to discuss later.
> Premise: Tentatively keep "field superposition" as one of the slices, not as the whole picture.
> Goal: Return to the paper's overall question — "from the player's perspective, what is the game agent we desire?" — and discuss the classification mechanism itself.

---

## 1. First, Doubt an Implicit Assumption in the Question

The question "what kind of agent do we desire" easily leads people toward a capability list like "smarter, more memory, more autonomous."

But if we re-ask from the player's perspective, the player rarely desires "an agent." What the player desires is:

> **Something that will see me, remember me, evaluate me, be changed by me, and thereby produce consequences in the world.**

The agent is merely the interface through which the world becomes "responsive."

So the more accurate question is not "what capabilities should the agent have," but:

> **Where, and in what way, does the player want the world to respond to them?**

---

## 2. All Existing Classification Mechanisms Are Merely Slices

### Technical Classification (FSM / BT / GOAP / Utility / LLM)

Classifies "how the system makes decisions." It does not answer how the player will feel about the character.

### Source Classification (Natural Information / Social Information)

Classifies "where the information comes from." It is the sender perspective, not the receiver perspective.

### Role Classification (Player / NPC / GM / Designer)

Classifies "what job AI performs in game production." It solves who does what, not what happens between player and character.

### Mechanism-Dependence Classification (AI-augmented / AI-native)

Classifies "does the gameplay hold up after removing AI." It answers whether the technology is core, not whether the player cares.

### Field Superposition

Classifies "in whose cognitive field the information is interpreted." It is closer to the player than the previous ones, but still mainly explains the single slice of "perspective difference."

**Common problem**: These classifications all start from the external observer or system designer. They all ask "what is this agent," while the player's real problem is "what is happening between it and me."

---

## 3. Six Questions Starting from the Player's Desire

### 3.1 Does It See Me?

The player does not only need the NPC to react, but needs the reaction to be **directed at themselves**.

- Good example: The player returns to town covered in blood; the guard takes a second look, and the tavern keeper does not greet them like other customers.
- Failed example: The player just killed the dragon, yet the whole village uses the same welcome line.

"Being seen" is not the same as information perception. It means the NPC's reaction contains an understanding of the player's current state.

### 3.2 Does It Remember Me?

Memory is not a database. The player's expectation of memory is **moral and relational**:

- Remembering a promise matters more than remembering "you bought three potions last time";
- Remembering a betrayal matters more than remembering dialogue text;
- Letting small talk fade is reasonable; forgetting a debt is unforgivable.

The player does not want the NPC to remember more, but to remember **what should be remembered**.

### 3.3 Who Is It?

The player wants the NPC to have boundaries. This boundary is not "what the character setting wrote," but **what it will refuse**.

- A merchant who refuses a trade is more real than one who sells everything.
- A character who refuses to help the player out of stance has more presence than an on-call assistant.

The essence of identity is not a persona label, but "the part that cannot be arbitrarily rewritten by the player."

### 3.4 Can I Change It?

The player needs their own actions to leave traces on the NPC.

- Having saved it, it will hesitate later;
- Having deceived it, it will be wary later;
- Having helped it, it may repay unintentionally.

Changeability cannot be without cost. If the NPC can be infinitely farm-grinded for favorability, and relationships infinitely restored by apology, change loses its meaning.

### 3.5 Does It Exceed Me?

The player occasionally needs the NPC to do something "not prepared for the player."

- Two NPCs argue when the player is absent;
- An NPC has its own schedule and is not here today;
- A character rejects the player's invitation because it has something it would rather do.

This creates a feeling that "the world does not revolve around me." An NPC that revolves entirely around the player will eventually be like furniture.

### 3.6 Is It Connected to the World?

The NPC cannot be a dialogue window floating in the scene. It should be constrained by space, time, economy, organization, weather, and events.

- When war breaks out, the merchant raises prices;
- Shops close at night;
- Rumors travel from one town to another.

The player's trust in the NPC comes from the causal consistency of its reactions with the world.

---

## 4. These Six Questions Point Not to Capabilities, but to Relationships

They can be combined into one sentence:

> **What the player desires is not a smarter character, but an other that can be believed, changed, and will leave consequences.**

This "other" simultaneously possesses:

- Reactivity: it is sensitive to the player;
- Independence: it does not belong entirely to the player;
- Persistence: it exists in time;
- Readability: the player can understand its patterns;
- Malleability: the player can leave influence;
- Worldliness: it is constrained by the world.

Each pair here naturally contains a contradiction: too sensitive loses independence, too independent becomes unreadable, too persistent seems repetitive, too malleable loses identity.

So the "best agent" is not the highest on some metric, but one that maintains stability among these tensions.

---

## 5. A New Proposal for the Classification Mechanism Itself

The existing classifications can continue to exist, but Macha needs to add a **classification axis starting from the player relationship**:

> Not asking "how is this agent implemented," but asking "which desire of the player is this agent satisfying."

We can initially propose four relationship archetypes:

1. **Witness**: Makes the player feel "the world has seen me."
2. **Relation-holder**: Makes the player feel "my actions have left a history on others."
3. **Resistor**: Makes the player feel "the world has rules, costs, and refusals."
4. **Other**: Makes the player feel "there is a life here that does not revolve entirely around me."

A concrete NPC can be several archetypes at once, in different proportions.

The value of this classification is: technical selection should be reverse-derived from the relationship archetype. For example, a "resistor" needs rule adjudication and boundary consistency; a "relation-holder" needs long-term memory and attitude updating; an "other" needs an independent schedule and autonomous goals.

---

## 6. Relationship with "Field Superposition"

Field superposition remains a powerful slice, but what it mainly explains is:

> When the player and NPC interpret the same event, they stand in different positions.

Placed among the six questions, it is closest to the interpretive layer between "does it see me" and "is it connected to the world."

But it does not directly explain:

- Why the NPC should remember something;
- Why the NPC should refuse;
- How the NPC is changed by the player;
- How the NPC exceeds the player.

Therefore the suggested progression of the paper is:

1. Overall question: What kind of agent does the player desire?
2. Field superposition: Point out one slice — the perspective difference between player and NPC.
3. Then expand: This perspective difference is only one layer of the more general "relationship gap." The relationship gap also includes memory, identity, malleability, independence, and world causality.
4. Finally propose: Crossing the gap is not to give the agent all capabilities, but to let the agent have stable boundaries and feedback on the six relationship dimensions.

---

## 7. Questions Left for Team Discussion

1. "Does the player desire an other, or the world's response?" These two definitions lead to completely different architectures.
2. Should the six questions be merged, ordered, or renamed?
3. Are the four relationship archetypes sufficient as a classification starting point?
4. Is "authenticity" one of the relationship dimensions, or the joint result of all dimensions?
5. Should field superposition be written first as the paper's "first slice," or should a larger relationship framework be established first, then field superposition placed within it?
