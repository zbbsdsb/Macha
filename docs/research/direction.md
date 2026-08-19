# Preliminary Technical Direction

## Problem Definition

What the team lacks right now is not "more papers," but a **minimum verifiable direction** we can start coding against.

We propose taking the following question as the first milestone:

> **How can a game NPC still remember the player after multiple conversations, while maintaining a stable persona and behavior logic?**

## Core Hypothesis

A believable NPC needs at least:

- **Perception**: extract structured observations from game events / player input.
- **Memory**: store short-term context and long-term experiences, and retrieve them by relevance.
- **Reflection**: periodically abstract scattered experiences into higher-level persona / relationship / world cognition.
- **Planning**: generate the next action based on current goals, memory, and reflection.
- **Action**: translate decisions into instructions or dialogue executable by the game engine.

## First MVP (Suggested)

- Implement a "minimal cognitive core" in Python.
- Do not bind to any specific game engine; validate first in a command-line / text environment.
- Provide an `Agent` interface, internally composed of four modules: `Memory`, `Reasoning`, `Perception`, `Action`.
- Test with a simple simulation scenario: the NPC conducts 5 rounds of dialogue with the player, then converses again after an interval, and the NPC can still recall key facts.

## Technology Selection Suggestions

- **Language**: Python 3.10+
- **LLM access**: first wrap an `LLMClient` interface; specific models can be plugged in later (OpenAI, local models, etc.).
- **Memory storage**: early stage can use JSON / SQLite, later upgraded to a vector database or knowledge graph.
- **Configuration**: YAML to manage NPC persona and world settings.

## Non-Goals (Not in the First Version)

- No full game engine integration.
- No large-scale multi-agent network.
- No production-grade inference cost optimization.
- No complex visual perception.

First, get "single-NPC long-term memory and character consistency" working.
