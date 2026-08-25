# Paper Additions: Possible Directions

> Paper: "Crossing the Game-Agent Gap"
> Existing content: Overview → Field Superposition → The Necessity of Authenticity (to be written)
> Goal: Propose possible directions for the new sections after "the necessity of authenticity" for the team to choose and order.

---

## Direction A: The Relationship Gap — From Perspective Difference to Multiple Breaks

**Suggested title**: "The Relationship Gap: Perspective Is Only the First Cut"

**Content**: Expand "field superposition" from a slice into a more complete relationship-gap framework. Field superposition explains that "the player and NPC stand in different positions when viewing the same event," but the relationship gap also includes:

1. The gap of seeing: Does the NPC react specifically to the player's current state?
2. The gap of memory: Does the NPC remember what matters in the relationship?
3. The gap of identity: Does the NPC have boundaries, can it refuse?
4. The gap of change: Does the NPC get traces left on it by the player?
5. The gap of the other: Does the NPC have a life that does not revolve entirely around the player?
6. The gap of the world: Is the NPC causally connected to space, time, economy, and events?

**Core claim**: The player feels the NPC is inauthentic not because of a deficiency in some single capability, but because the relationship chain breaks somewhere.

**Strength**: Directly continues "field superposition"; the logic is most natural.
**Risk**: Without restraint, it becomes a large checklist of problems rather than a sharp argument.

---

## Direction B: The Relationship Axis — Rebuilding the Classification Mechanism Itself

**Suggested title**: "From Technical Classification to Relationship Classification"

**Content**: Critique the existing classification mechanisms:

- Technical classification (FSM/BT/GOAP/Utility/LLM) answers "how to implement";
- Source classification (natural/social) answers "where the information comes from";
- Role classification (player/NPC/GM/designer) answers "what job it performs";
- Mechanism classification (AI-augmented / AI-native) answers "does it hold up after removing AI."

Then propose a new axis:

> Which relationship need of the player is this agent satisfying?

**Core claim**: Classification cannot have only a system perspective; the player-relationship perspective must be added. The relationship axis does not replace existing classifications, but lets technical selection be reverse-derived from player experience.

**Strength**: This is the part of the paper most able to form a "conceptual contribution."
**Risk**: Easily written as a survey-style critique; needs to land on concrete archetypes or cases soon.

---

## Direction C: The Four Relationship Archetypes

**Suggested title**: "Witness, Relation-holder, Resistor, Other"

**Content**: Expand the relationship axis into four archetypes:

1. **Witness**: The world has seen me;
2. **Relation-holder**: My actions have left a history on others;
3. **Resistor**: The world has rules, costs, and refusals;
4. **Other**: There is a life here that does not revolve entirely around me.

Pair each archetype with a set of game cases, and show they require different technical capabilities:

- Witness → perception and reaction;
- Relation-holder → memory and attitude updating;
- Resistor → rule adjudication and boundaries;
- Other → independent goals and schedule.

**Core claim**: A single NPC can belong to multiple archetypes simultaneously, but in different proportions; when designing an NPC, first fix the relationship archetype, then choose the technical architecture.

**Strength**: Most original, and easiest to translate into Macha's design language.
**Risk**: Whether the four archetypes are sufficient needs case testing; fixing them too early may limit later discussion.

---

## Direction D: The Necessary Tension

**Suggested title**: "The Necessary Tension: Why a Single-Capability Upgrade Cannot Cross the Gap"

**Content**: Argue that the player's desire for the agent is not a capability list, but a tension system:

- Responds to me vs. independent of me;
- Remembers me vs. allows forgetting;
- Stable vs. malleable;
- Predictable vs. surprising;
- Belongs to the world vs. serves gameplay.

**Core claim**: A good agent maintains stability among tensions, rather than maximizing some single metric.

**Strength**: Can explain why "bigger model, longer context, stronger reasoning" have not individually solved the authenticity problem.
**Risk**: Leans philosophical; needs to avoid becoming a collection of aphorisms, and must be supported by architecture or cases.

---

## Direction E: From Desire to Contract

**Suggested title**: "The Five Guarantees of the Standard Skeleton"

**Content**: Translate the relationship conclusions into a technical contract. The agent the player desires requires the standard skeleton to provide:

1. The guarantee of being seen;
2. The guarantee of being remembered;
3. The guarantee of having boundaries;
4. The guarantee of being changeable;
5. The guarantee of not belonging entirely to the player.

Then briefly explain which architecture modules and evaluation metrics correspond to each guarantee.

**Core claim**: Crossing the gap is not to make the agent more human-like, but to make the standard skeleton accountable for relationship quality.

**Strength**: Directly serves Macha, making the paper not pure speculation.
**Risk**: If too engineering-heavy, it breaks the philosophical tone of the paper's first half; suitable for a later position.

---

## Direction F: Case Slices

**Suggested title**: "Remembered and Seen Through: The Successes and Failures of Several NPCs"

**Content**: Pick 3–5 game NPC cases, and use the "relationship language" to explain:

- Why Shadow of Mordor's Nemesis is remembered;
- Why The Sims' characters feel alive;
- Why some AI NPCs are seen through at a glance;
- Candidates include Skyrim's Lydia, Hades' gods, Dwarf Fortress's dwarves, etc.

**Core claim**: The relationship language must be able to explain real game cases, otherwise it is just new vocabulary.

**Strength**: Most readable, can test the concepts.
**Risk**: If cases are poorly chosen, it will be challenged as "only picking favorable evidence."

---

## Direction G: Dialogue with the Four Papers

**Suggested title**: "We Stand Where They Stopped"

**Content**: Write the boundary probing of the four papers into a formal related-work / positioning section:

- 2304 gave the body;
- 2404 gave the system;
- 2402 gave the position;
- 2607 gave the rules;
- This paper must supply the player relationship.

**Core claim**: This paper is not a fifth survey, but continues to ask forward from where the four papers jointly stopped.

**Strength**: Clear academic positioning, convenient for submission.
**Risk**: If it only restates, the value is limited; it must form a genuine point of transcendence.

---

## Suggested Combined Order

If we keep only the sharpest main line of the paper, the suggested order is:

```text
Overview
  ↓
Field superposition (first slice)
  ↓
Relationship gap (Direction A: expand the slice into multiple breaks)
  ↓
Relationship axis and four archetypes (Direction B + C: propose a new classification)
  ↓
The necessary tension (Direction D: explain why single-capability cannot solve it)
  ↓
The five guarantees of the standard skeleton (Direction E: land on Macha)
  ↓
Case slices (Direction F: validate with game cases)
  ↓
Related work / dialogue with the four papers (Direction G: can come earlier or later)
```

Among these, **A, B+C, D** are the paper's "theoretical trunk"; **E** is the "engineering exit"; **F** is the "empirical evidence"; **G** is the "academic positioning."

---

## Three Questions the Team Must Answer First

1. Should the paper ultimately lean toward "design theory" or "architecture standard"? This decides the weight of E and F.
2. Should the four relationship archetypes be fixed first, or should we do cases first and then come back to revise them?
3. Does keeping "field superposition" as the "first slice" hold? Should it be demoted to a smaller subsection?
