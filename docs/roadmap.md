# Development Roadmap

## Phase 0: Repository Initialization (Current)

- [x] README, LICENSE, .gitignore
- [x] Basic project structure
- [x] Research document organization
- [ ] Team confirms the first MVP direction
- [ ] Initialize Git and push to remote (if not yet executed)

## Phase 1: Minimal Cognitive Core

- [ ] Define `Agent`, `Memory`, `Perception`, `Reasoning`, `Action` interfaces
- [ ] Implement long-term memory based on JSON/SQLite
- [ ] Implement a simple LLM call wrapper
- [ ] Pass a smoke test that "still remembers key facts after 5 rounds of dialogue"

## Phase 2: Character Consistency and Reflection

- [ ] Implement a reflection mechanism: generate persona summaries from experiences
- [ ] Add importance scoring and memory retrieval
- [ ] Add "character consistency" test scenarios
- [ ] Introduce human evaluation / automated evaluation scripts

## Phase 3: Environment Integration

- [ ] Select the first target environment (e.g., text adventure, Minecraft-like sandbox, or a self-built Demo)
- [ ] Implement Perception/Action adapters
- [ ] Connect to concrete game state

## Phase 4: Multi-Agent and Evaluation

- [ ] Multi-NPC communication and collaboration
- [ ] Long-term stress testing
- [ ] Reasoning cost optimization
- [ ] Release a demonstrable v0.1 version

## Current Recommendation

Do not rush into writing a complex system. First build the Phase 1 "minimal cognitive core," then adjust the architecture based on actual results.
