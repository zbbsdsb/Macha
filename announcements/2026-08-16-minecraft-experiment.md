# Macha Experimental Track I: Minecraft

**Date:** 2026-08-16  
**Project:** [Macha](../README.md) — an open, engine-agnostic standard skeleton for game NPCs  
**Status:** Announced

## What we are announcing

The Macha team is launching its first experimental track in **Minecraft**. We will use Minecraft as a controlled, open-ended testbed for NPC cognition: long-term memory, stable identity, reflection, planning, bounded action, and world coupling.

This is not a commercial mod. It is an open research experiment to validate whether a standard, reusable NPC cognitive skeleton can work across engines and models.

## Why Minecraft

Minecraft gives us a unique combination:

- An open world with deterministic rules, so NPC actions can be grounded in real world state.
- A mature bot/modding ecosystem that lets us separate cognition from rendering and engine internals.
- A well-established research lineage, from Generative Agents to Voyager and Project Sid.
- Natural pressure tests for memory, spatial behavior, tool use, and multi-agent interaction.

## What we are not doing

- We are not building a production Minecraft mod yet.
- We are not claiming to replace existing NPC frameworks.
- We are not affiliated with Mojang, Microsoft, or any Minecraft server project.

## Collaboration

If you work on NPC architectures, Minecraft agents, game AI research, or modding, we welcome feedback and collaboration. The results of this track will be published openly in this repository.

---

## Update — 2026-09-13: what this track is for

One clarification of scope, after calibrating our architecture.

**Minecraft is not part of Macha.** This track is a **Concrete Layer Test Case**: we build one
real *Environment Integration Layer* against Minecraft in order to validate the Layer abstraction
itself — that a world can be connected through an independent Layer without changing Macha Core.

- Target: `Macha Core + Minecraft Layer = a Minecraft-connected Macha`, with **zero Core changes**.
- Not the target: a Minecraft-oriented Macha, or "Macha for Minecraft."
- Success is measured by the boundary holding (capability probing, actions that can be refused,
  consequences returned), not by how impressive the NPC looks in-game.
- Future environments (Skyrim, Cyberpunk 2077, Unreal, Unity, simulations) should each be their own
  Layer, implemented independently.

Definitions: [Target Architecture](../docs/architecture.md) · validation plan:
[`research/plans/minecraft-layer-validation-plan.md`](../research/plans/minecraft-layer-validation-plan.md).

---

*Macha Team*
