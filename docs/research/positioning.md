# Research Positioning: The Relationship Between Four Papers and Macha

## Hierarchical Differences Among the Four Papers

| Paper | Positioning | Implication for Macha |
|---|---|---|
| 2304.03442v2 (Smallville) | Concrete implementation prototype | NPCs need the three pillars of "memory stream + reflection + planning" to produce believable social behavior |
| 2404.02039v5 (Hu et al.) | System architecture survey | Design the NPC system using a unified "perception—memory—reasoning—action" framework |
| 2402.18659v5 (Gallotta et al.) | Applied-role survey | First clarify the role the NPC plays in the game, then decide on technology selection |
| 2607.00527v2 (AI-Native) | Design ontology | Use the "removal test" to judge which AI capabilities truly restructure gameplay |

## Macha's Preliminary Positioning

Macha should focus on:

- **Foundation**: a reusable NPC cognitive architecture (memory, reflection, planning).
- **Interface**: a perception / action layer that can connect to different game engines.
- **Evaluation**: not just task completion rate, but also character consistency, long-term memory stability, and player-perceived believability.

## The Core Positioning of the Paper

The core contribution of the paper is to **redefine the problem, not to deliver a final implementation**.

We are not writing a "game engine architecture paper," nor an "AetherFlow technical report." Our initial question is:

> Answer from the player's perspective: what is the game Agent we long for? Why do existing Agents break our immersion? What should a standard skeleton guarantee?

Therefore, the value of the paper lies in proposing a new way of looking at the "player—NPC—world" relationship, and in providing a theoretical direction for Macha. Questions at the implementation level (in-world embedded computation network vs. character extension, how to design the macro simulation layer, etc.) belong to later phases and should not become the main body of the paper.

## Our Suggested Entry Points

Looking across the intersection of the four papers, the most worthwhile things to do first are:

1. **Long-term world-model memory**: upgrade the dialogue transcript into structured causal memory.
2. **Character consistency**: let the NPC maintain a stable persona over long interactions.
3. **Pluggable architecture**: first provide clear Python interfaces, then gradually connect specific LLMs and game engines.

> See [direction.md](direction.md) for detailed direction.
