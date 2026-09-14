# Decision: Layers Directory Layout — `kit/` + Environment Subtrees

> Status: **RATIFIED — decision record.** Decided 2026-09-14 by the project owner.
> Recorded per `../../docs/team-workflow.md`. Project-engineering decision, not a paper conclusion.
> Supersedes the flat module list in
> [`../../../research/plans/minecraft-layer/04-project-structure.md`](../../../research/plans/minecraft-layer/04-project-structure.md) §1–§2, which it amends.

---

## 1. Decision

Inside the Gradle build root `layers/`, **shared, environment-agnostic modules move under `kit/`**,
and each environment stays its own subtree:

```text
layers/                          # ONE Gradle build root
├── settings.gradle.kts
├── kit/                         # shared core — environment-agnostic
│   ├── protocol/                #   :kit:protocol
│   ├── runtime/                 #   :kit:runtime
│   └── transport/               #   :kit:transport
├── minecraft/                   # Minecraft Layer — only module with paper-api
├── simulator/                   # fake environment (control condition, C4)
├── testclient/                  # vertical-slice client
└── run/                         # runtime artifacts (gitignored)
```

Rejected alternatives:

| Option | Why not now |
|---|---|
| **A** keep flat (`layers/protocol` next to `layers/minecraft`) | Works, but shared core and environment implementation read as siblings; the architecture's central distinction ("Layer ≠ Core/adapter internals") is invisible on disk |
| **C** top-level `macha-minecraft/` + `macha-layer-kit/`, each its own build root, joined by composite build | Strongest independence, but costs a wrapper/settings per root, IDE imports per root, and multi-command builds; it is **paying the split cost before the split** — explicitly discouraged by the original phase brief ("不要为了'未来可能拆 repo'而进行不必要的工程操作") |

**Key clarification of intent:** creating a top-level directory does *not* make a Layer independent
— independence comes from (a) a stable protocol, (b) no Core changes when connecting. Conversely,
keeping it under `layers/` does not weaken it: `layers/minecraft/` already has its own build file,
its own source tree, and is the only module allowed to depend on `paper-api` (compile-time enforced).

## 2. Module / directory mapping

| Before | After | Gradle path |
|---|---|---|
| `layers/protocol/` | `layers/kit/protocol/` | `:kit:protocol` |
| `layers/runtime/` | `layers/kit/runtime/` | `:kit:runtime` |
| `layers/transport/` | `layers/kit/transport/` | `:kit:transport` |
| `layers/minecraft/` | **unchanged** | `:minecraft` |
| `layers/simulator/` | **unchanged** | `:simulator` |
| `layers/testclient/` | **unchanged** | `:testclient` |

Kotlin packages do **not** change (`dev.macha.layer.*`) — the regroup is a build-layout change only.

## 3. Migration Checklist (mechanical; not yet executed)

1. `git mv`-equivalent the three directories into `layers/kit/` (they are currently untracked, so a
   plain filesystem move suffices).
2. `layers/settings.gradle.kts`: `include(":kit:protocol", ":kit:runtime", ":kit:transport", ":minecraft", ":simulator", ":testclient")`.
3. Rewrite project references in dependent build files:
   `project(":protocol")` → `project(":kit:protocol")`; same for `:runtime`, `:transport`
   (affects `kit/runtime`, `kit/transport`, `minecraft`, `simulator`, `testclient`).
4. `layers/build.gradle.kts` boundary guards: the `verifyEnvClean` directory list
   `listOf("protocol", "runtime", "simulator")` → `listOf("kit/protocol", "kit/runtime", "simulator")`;
   `verifyPaperScope`'s allowed-path rule (contains `plugin/` or `adapter/`) is unaffected.
5. Re-import the Gradle project in the IDE; delete stale `layers/build` outputs.
6. Run `./gradlew check` (boundary guards) and `./gradlew build`.

## 4. Upgrade Triggers — when this decision is revisited in favour of Option C

Move to separate build roots / separate repositories when **any** of these becomes true:

| # | Trigger | Why it forces the split |
|---|---|---|
| T1 | Minecraft Layer and Kit need **independent release cadences** (Kit frozen at v0, MC Layer tracks Paper builds) | One build root implies one version graph |
| T2 | A **third-party environment implementation** appears (outside this repo) | The Kit must become a consumable artifact, not a project reference |
| T3 | Running the **V5 validation** ("a third party implements a Layer from the spec alone") | Our own second implementation should then live outside the repo, or the proof is weakened |
| T4 | Build configuration of the two starts to interfere (different Gradle/Kotlin/JDK requirements) | One root cannot serve two toolchains cleanly |

Until a trigger fires, Option B stands. Split mechanics remain as documented in
`04-project-structure.md` §6: `layers/minecraft/` → repo `macha-minecraft`; `layers/kit/*` →
published `macha-layer-kit`.

## 5. What This Does Not Change

- Module dependency rules (`04` §2) — only the module **paths** change, not the directions.
- `paper-api` remains `compileOnly` and confined to `:minecraft`.
- Plan documents stay in `research/plans/minecraft-layer/` until a Layer split (per `04` §6);
  the repo's maturity-based layering (`research/` / `papers/` / `docs/` / `site/`) is untouched.

## 6. Documents Updated Under This Decision

- `research/plans/minecraft-layer/04-project-structure.md` (§0 change log, §1 placement, §2 module graph, §3 headers, §4 mapping, §6 split path, §7 open items)
- `research/plans/minecraft-layer/00-technical-foundation.md` (§A.3 layout + isolation rules, §E module list, §H decisions D8/D9 marked decided)
- `research/plans/minecraft-layer/03-build-and-module-layout.md` (§1 build root, §7 guard paths)
- `README.md` (Where Layers Live), `docs/architecture.md` §7 (repository organization)
- `papers/notes/README.md` (index entry)
