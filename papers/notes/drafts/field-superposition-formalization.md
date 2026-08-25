# Field Superposition: Concept Formalization Notes

> Purpose: To provide formal definitions, notation, and examples for "field superposition" in the paper "Crossing the Game-Agent Gap" that can enter the paper.
> Status: Discussion draft, not directly equivalent to the paper body.

---

## 1. Understanding "Sender Perspective / Receiver Perspective"

- **Sender perspective = information-source perspective**. Traditional game AI first classifies information by source: natural information, social information, then assigns different weights. The question it answers is: "Where was this information sent from? What weight should I give it?"
- **Receiver perspective = information-processing perspective**. Field superposition answers a different question: "Which cognitive field does the same information fall into? What perspectives does this cognitive field superpose from? What is the information interpreted as here?"

One-sentence summary:

> The traditional approach is "decompose information by sender," while Macha's field superposition is "reconstruct information by receiver."

---

## 2. Proposed Formal Definitions

### 2.1 Events and Information Sources

Let an event occur in the game world:

\[
e \in E
\]

The **information-source marker** of the event is:

\[
s(e) \in \{N, S, M\}
\]

where \(N\) denotes a natural source (environment, physics, items), \(S\) denotes a social source (relations, reputation, organization), and \(M\) denotes a mixed source.

The traditional source-domain model can be written as:

\[
I(e) = \alpha(e) I_S(e) + \beta(e) I_N(e)
\]

where \(\alpha, \beta\) are source weights. The characteristics of this model are:

- It is completed before the information enters the subject;
- It does not depend on who the receiver is;
- It assumes the meaning of the information is mainly determined by its source.

### 2.2 Cognitive Field

For any subject \(a\), define its **cognitive field**:

\[
F_a = (W_a, \Phi_a, T_a, V_a)
\]

- \(W_a\): the subject's observable window, i.e. which events can enter its cognition;
- \(\Phi_a\): the interpretation function, mapping events into the subject's cognitive meaning;
- \(T_a\): the temporal and memory layer, affecting how events superpose with the past;
- \(V_a\): the value and persona layer, determining how events are evaluated within the subject's world.

The subject's processing of an event is not simple weighting, but:

\[
m_a(e) = \Phi_a(e; T_a, V_a)
\]

\(m_a(e)\) is the meaning of event \(e\) after it is reconstructed within the subject \(a\)'s field.

### 2.3 Field Superposition

The player's field is superposed from at least two layers:

\[
F_{player} = F_{in} \oplus F_{meta}
\]

- \(F_{in}\): the in-game perspective. The player as an actor within the game world.
- \(F_{meta}\): the out-of-game global perspective. The player as an external observer who knows the system, gameplay, quests, and social context.

The NPC's field is typically:

\[
F_{npc} \subseteq F_{in}
\]

That is, the NPC processes information only within the in-game perspective.

**Key point**: \(\oplus\) is not scalar addition, but two reference frames acting simultaneously on the same event. The same piece of information acquires meaning separately in the two fields, and may produce conflict. For example:

- \(F_{in}\) says: "This NPC is very stubborn."
- \(F_{meta}\) says: "This NPC is scripted and only repeats three lines."

The player always experiences both interpretations simultaneously, while the NPC experiences only the first.

### 2.4 Formalization of the Gap

Define the **perspective gap** between player and NPC:

\[
G = F_{player} \setminus F_{npc}
\]

More precisely:

\[
G \approx F_{meta}
\]

It is not that "the NPC receives less of some kind of information," but that "the NPC lacks a layer of information-processing field." Therefore, the gap cannot be filled by increasing input weights or increasing perception sources; it can only be addressed by redesigning the NPC's information-processing structure.

---

## 3. Two Key Propositions

**Proposition 1: Source-domain decomposition is receiver-independent; field superposition is receiver-dependent.**

\[
I(e) = \alpha I_S(e) + \beta I_N(e)
\]

is the same for any receiver; but

\[
m_a(e) = \Phi_a(e; T_a, V_a)
\]

differs depending on the subject.

**Proposition 2: When multiple perspective fields exist, the source-domain weight model degenerates into a special case of field superposition.**

Only when all subjects share the same \(F\) can the meaning of information be replaced by global weights. The failure of game NPCs is precisely because developers used a "unified source domain" to process "meanings that should have been dispersed across fields."

**Proposition 3 (core of this paper)**:

> The authenticity gap of the game agent is not missing information, but a missing field.

The difference between NPC and player lies not in the NPC not knowing enough, but in that the player processes information within a superposed field while the NPC processes information within a single field.

---

## 4. Comparison Table That Can Enter the Paper

| Dimension | Sender Perspective (Source-Domain Decomposition) | Receiver Perspective (Field Superposition) |
|---|---|---|
| Question answered | Where does the information come from | In whose cognition does the information become meaning |
| Object of operation | Information source | Cognitive field |
| Direction | Sender → receiver | Receiver → interpretation → action |
| Typical form | Weights, attention, multi-domain fusion | Fields, perspectives, interpretation function |
| Depends on subject | No | Yes |
| Failure mode | Weight mismatch | Missing field or field conflict |
| Corresponding game AI | Utility, perception weights, information filtering | Macha's memory / persona / reasoning structure |

---

## 5. A Concrete Example

Event \(e\): The player enters the same tavern three nights in a row and only speaks with the same NPC.

- **Source-domain model**:
  - Natural source: time, location, action frequency;
  - Social source: increased familiarity with the NPC;
  - Output: \(I(e) = 0.3 I_N + 0.7 I_S\), the NPC is friendlier to the player.

- **Field-superposition model**:
  - NPC field \(F_{npc}\): this is "a regular who comes every night," superposed with its own memory, debts, and wariness of strangers.
  - Player in-game field \(F_{in}\): this is "I want to raise this NPC's favorability."
  - Player out-of-game field \(F_{meta}\): "the quest system likely has hidden rewards; this NPC is a key character; I am making a resource investment."
  - The player evaluates the NPC simultaneously with \(F_{in} \oplus F_{meta}\). Any line of dialogue from the NPC is interpreted within the two layers. If the NPC can only process \(F_{npc}\), the player will feel "it is not like a real, existing person."

---

## 6. How to Connect with "The Necessity of Authenticity"

"Authenticity" is not that the NPC possesses more information, but:

1. The NPC has a clear and stable field boundary;
2. The interpretation, memory, and action within the field are mutually consistent;
3. The player's superposed field can understand the NPC's single field, and feel its behavior is "like real."

Therefore, the goal of crossing the gap is not to let the NPC acquire the player's out-of-game perspective, but to upgrade the NPC's cognitive architecture from "source-domain weighting" to "field processing," and to make this processing observable, understandable, and designable.
