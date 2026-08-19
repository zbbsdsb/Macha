---
title: Crossing the Game-Agent Gap
status: draft
type: paper
---

# Crossing the Game-Agent Gap

## Overview

From finite state machines to behavior trees, and then to the sudden arrival of LLMs, in-game NPCs have evolved for decades. This brings us back to the most fundamental question: what kind of game agent do we actually need? Rather than analyzing this from a technical-implementation angle, we approach it from the player's perspective: what do we desire the in-game agent to be?

## Field Superposition

### 2.1 Two Perspectives Long Confused

When discussing game agents, the most common practice is to first classify environmental information by source: natural information and social information. Information released by the natural environment enters one computation domain, and information released by the social environment enters another. The system then assigns corresponding weights to different sources, forming the agent's overall judgment of the environment. This tradition can be traced back to the input design of perception systems, utility functions, and behavior trees.

For ease of discussion later, we collectively refer to such practices as **Source-Domain Decomposition**.

Let an event \(e \in E\) occur in the game world at some moment, with its information source marked as:

\[
s(e)\in\{N,S,M\}
\]

where \(N\) denotes a natural source, \(S\) denotes a social source, and \(M\) denotes a mixed source. Source-domain decomposition writes the information quantity of event \(e\) as:

\[
I(e)=\alpha(e)I_S(e)+\beta(e)I_N(e)
\]

\(\alpha\) and \(\beta\) are source weights. This model rests on three implicit assumptions: information is already decomposed before it enters the subject; its weight does not depend on who the receiver is; and the meaning of the information is mainly determined by its source.

We must acknowledge that source-domain decomposition is effective in engineering. It lets the agent distinguish between two completely different kinds of information — "it is raining" and "someone betrayed me" — and adjust behavior accordingly. However, the field superposition discussed in this paper is not this meaning. Source-domain decomposition deals with the **sending end** of information, while field superposition deals with the **receiving end**. The former answers "where does the information come from," while the latter answers "in whose cognition does the information become meaning." One sends outward, one receives inward; one is centered on the sender, the other on the receiver.

### 2.2 Cognitive Field

To formally discuss the receiving end, we introduce the **Cognitive Field**.

**Definition 1 (Cognitive Field)**: For any subject \(a\), its cognitive field \(F_a\) is a quadruple:

\[
F_a=(W_a,\Phi_a,T_a,V_a)
\]

where:

- \(W_a\) is the observation window, determining which events can enter the subject \(a\)'s cognition;
- \(\Phi_a\) is the interpretation function, mapping events into the subject's cognitive meaning;
- \(T_a\) is the temporal and memory layer, determining how events superpose with the subject's past;
- \(V_a\) is the value and persona layer, determining how events are evaluated within the subject's world.

Thus the subject's processing of an event is not simple weighting, but:

\[
m_a(e)=\Phi_a(e;T_a,V_a)
\]

\(m_a(e)\) is the meaning of event \(e\) after it is reconstructed within the subject \(a\)'s field.

The key property of the cognitive field is **subject- relativity**. The same piece of information entering different fields produces different meanings; it can even produce different meanings when entering two different fields of the same person.

### 2.3 Field Superposition

In the real world, every person has their own perspective, and these perspectives do not replace one another but coexist and superpose simultaneously. The player's state in a game is exactly like this.

**Definition 2 (Field Superposition)**: The player's cognitive field in a game is composed of the superposition of at least two fields:

\[
F_{player}=F_{in}\oplus F_{meta}
\]

- \(F_{in}\) is the in-game field: the player, as an actor within the game world, processes in-game information such as character, quests, combat, and economy.
- \(F_{meta}\) is the out-of-game field: the player, as an external observer who knows the system rules, gameplay goals, social context, and their own real-life experience.

The in-game agent typically only possesses:

\[
F_{npc}\subseteq F_{in}
\]

It must be emphasized here that \(\oplus\) is not scalar addition, but the simultaneous action of two reference frames upon the same event. The same event acquires meaning separately in the two fields, and these two meanings may conflict with each other. The player does not first perform a "natural/social" classification and then add the results; the player simultaneously understands everything that happens through two identities: "in-game character" and "out-of-game player."

For example, a player enters the same tavern three nights in a row and only speaks with the same NPC. In the in-game field, this event is interpreted as "I am building a relationship with this person"; in the out-of-game field, it is simultaneously interpreted as "I am grinding favorability, which may relate to quest rewards." The two interpretations do not cancel each other out, but rather superpose in every observation the player makes of the NPC.

### 2.4 Perspective Gap

Thus, the difference between player and NPC can be formalized as:

\[
G=F_{player}\setminus F_{npc}
\]

Since the NPC usually acts only within the in-game field, this gap is approximately:

\[
G\approx F_{meta}
\]

This means that the fundamental gap between the game agent and the player is not a difference in information quantity, but a difference in **information-processing fields**. The NPC does not "know less"; rather, it lacks an entire layer of means for receiving and interpreting information. Therefore, the gap cannot be filled by adding sensors, expanding perception range, or increasing natural/social information weights.

On this basis, we arrive at the first core judgments of this paper:

**Judgment 1**: Source-domain decomposition is receiver-independent, while field superposition is receiver-dependent. The former gives the same input representation to any subject, while the latter produces different meanings because of differences in each subject's observation window, interpretation function, memory, and persona.

**Judgment 2**: Source-domain decomposition is a degenerate form of field superposition. Only when all subjects share the same cognitive field can the meaning of information be replaced by a set of global weights. The failure of game NPCs precisely originates from the system's attempt to use a unified source-domain model to process meanings that should have been dispersed across different cognitive fields.

**Judgment 3**: The authenticity gap of the game agent is not missing information, but a missing field. The player understands the NPC within a superposed field, while the NPC processes information only within a single field.

### 2.5 From Field Superposition to "Authenticity"

The above analysis provides a new criterion for "authenticity." The reason an NPC seems fake is not that it has too little perception data, too small a language model, or too shallow a behavior-tree hierarchy, but that the player always interprets it within \(F_{in}\oplus F_{meta}\), while it is only accountable to \(F_{in}\). Any interpretation from the out-of-game field — such as "this is scripted," "it only has three lines of dialogue," "it is waiting for me to finish the quest" — directly punctures the NPC's sense of authenticity.

Therefore, the correct direction for crossing the gap is not to let the NPC acquire the player's out-of-game perspective, but to let the NPC possess a cognitive field that is **clearly bounded, internally consistent, and understandable to the player within their superposed field**. This is exactly the "necessity of authenticity" discussed in the next section.

## The Necessity of Authenticity

(To be written)

---

## Revision Log

- First draft: established the paper skeleton, wrote the "Overview" and "Field Superposition" sections.
- 2026-08-16: Expanded the "Field Superposition" section into a formal draft, adding formal definitions of source-domain decomposition, cognitive field, field superposition, and perspective gap, and connecting to the "necessity of authenticity."
