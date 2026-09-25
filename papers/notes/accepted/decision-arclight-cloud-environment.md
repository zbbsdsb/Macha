# Decision: 实验环境改为云端 Arclight（Layer 保持 plugin 形态）

> Status: **RATIFIED — decision record.** Decided 2026-09-15 by the project owner.
> Recorded per `../../docs/team-workflow.md`（偏离已批准基线必须留档）。
> 相关：[`../../../research/plans/minecraft-layer/00-technical-foundation.md`](../../../research/plans/minecraft-layer/00-technical-foundation.md) §C/§D ·
> [`../../../research/plans/minecraft-layer/01-protocol-v0.md`](../../../research/plans/minecraft-layer/01-protocol-v0.md) §5/§9 ·
> [`../../../research/projects/2026-09-14-mc-vertical-slice/`](../../../research/projects/2026-09-14-mc-vertical-slice/)

---

## 1. 决定

1. **实验环境 = `play.simpfun.cn:15463`**（`43.248.103.155`，Minecraft **1.20.1**，protocol **763**，
   **Forge + Arclight 混合端**，面板**最大权限**）。这台机器**就是实验环境**，不是演示服。
2. **Minecraft Layer 保持 plugin 形态**（不做 mod）。
3. 因此所需的连带决定：
   - **构建目标取两环境下界**：Bukkit/Spigot API **1.20.1** + **Java 17** → 一份 jar 同时能跑
     云端 Arclight 1.20.1 与本地 Paper 26.2；**禁用任何 Paper 专有 API**。
   - **传输方向可配**：`transport.mode: listen|dial`。云端必须用 **dial**（Layer 主动拨出），
     因为托管面板不会为插件开放任意 TCP 端口；本地 dev loop 继续用 **listen**。
   - **dial 模式下 token 必填**，且不得明文跨公网（TLS 或隧道）。
4. **本地 pinned Paper 26.2 服务器保留**，作为**可复现的研发/调试回路**；云端作为实验环境。
   两者跑同一份 Layer 构建 = **跨环境复现（E3）** 的现成素材。

## 2. 事实依据（实测，2026-09-15）

```
play.simpfun.cn:15463 → 43.248.103.155
MOTD: SFE4-SERVER   在线: 是   玩家: 0/20
版本: forge arclight/Trials 1.20.1   protocol 763
```

对照已锁基线（`00` §C.1）：Paper **26.2** / protocol **776** / **Java 25**。
→ 四个维度全部不同：**版本、Java、API 栈、网络位置**。

## 3. 为什么不是 mod 形态

| 理由 | 说明 |
|---|---|
| 平台不需要 | Arclight 是**混合端**，本来就能同时跑 Forge mod 与 Bukkit 插件 |
| 能力面用不到 | v0 需要的全部能力（位置/朝向/生命、附近实体与方块、世界时间、move/look/interact/spawn）**都在 Bukkit 层** |
| 代价高 | 1.20.1 的 ForgeGradle 与我们的 Gradle 9.7.1 存在兼容摩擦；引入 NMS/Mojang mappings；把「薄层」锁进 mod loader + 版本映射（正是 `00` §C.3 当初拒绝 Forge/Fabric 的理由） |
| 重做面大 | M1–M6 的事件 API、注册方式、打包都要重做，换来的效果与插件相同 |

**唯一正当的 mod 触发条件**：需要与某个 Forge mod **深度交互**（读写其生物/机制），且 Bukkit 层无法表达。
届时按"plugin + 薄 mod 适配器"评估，而不是把整个 Layer 改成 mod。

## 4. 连带影响（必须做的改动）

| # | 改动 | 位置 |
|---|---|---|
| A | 依赖 `io.papermc.paper:paper-api` → **`1.20.1-R0.1-SNAPSHOT`**（或 `org.spigotmc:spigot-api:1.20.1`，取决于可解析性）；**新增守护任务 `verifyBukkitOnly` 禁止 `import io.papermc.*` 与 Paper 专有类** | `layers/gradle/libs.versions.toml`、`layers/minecraft/build.gradle.kts`、`layers/build.gradle.kts`、`00` §D |
| B | `jvmToolchain(17)` / `JvmTarget.JVM_17`（Gradle 缓存**已有** Temurin 17） | 各模块 `build.gradle.kts`、`00` §C.1 |
| C | `plugin.yml`：`api-version` 改 `'1.20'`（不再是 `'26.2'`） | `layers/minecraft/src/main/resources/plugin.yml`、`03` §4 |
| D | 新增 `transport.mode: listen\|dial` + `runtime.endpoint` + 强制 token（dial） | `01` §5（已登记）、`config.yml`、`transport/` |
| E | 实验环境的**确定性控制**：whitelist 打开、固定世界与种子、跑批期间无第三方玩家、上传 jar 记 sha256、重启纪律写进 README | `layers/README.md`、项目 `handover-checklist.md` |
| F | 本文与 `00` §C.1 的两环境对照表 | 已完成 |

## 5. 实验环境的确定性要求（因为它**是**实验环境）

- [ ] `white-list=true` + 只放团队成员；跑批期间无旁观者
- [ ] 固定世界（`level-type=flat` 或固定种子）并在跑批前备份
- [ ] **上传的 jar 记 sha256**（云端的"版本 pin"就是它）
- [ ] 重启纪律：跑批前清空世界或恢复到基线快照；每次跑批记录 jar sha + 世界快照 id
- [ ] 事件/动作的原始证据落 transcript（M9），不要只依赖面板日志

## 6. 被拒绝的方案

| 方案 | 理由 |
|---|---|
| Layer 改为 Forge mod | §3 |
| 只保留 listen 模式 | 托管面板不开放任意 TCP 端口 → 云上根本连不上 |
| 云端替代本地环境 | 会丢掉可复现性（服务器不归我们管、无法 pin、world 会被动过）；本地 loop 必须保留 |
| 现在就分两套构建（legacy/modern） | 过度设计；**升级信号**：当 1.20.1 API 无法表达某个必需动作时再评估 |

## 7. 回退与重访条件

| 触发 | 动作 |
|---|---|
| 云端面板其实**能**开放 TCP 端口 | listen 模式在云端也可用（但仍建议 dial，少一个入站面） |
| 1.20.1 Spigot API 无法表达某个必需动作 | 评估"plugin + 薄 mod 适配器"，而不是整体改 mod |
| 云端版本升级（如到 1.21） | 重跑 vertical slice；`api-version`/`spigot-api`/JVM target 一并重锁 |
| 需要与某个 Forge mod 深交互 | 同上第 2 条 |
| 实验环境被第三方玩家污染且无法限制 | 回到本地环境做正式实验，云端只做演示 |

## 8. 受影响文档

- `research/plans/minecraft-layer/00-technical-foundation.md`（§C.1 两环境对照、§D 依赖）
- `research/plans/minecraft-layer/01-protocol-v0.md`（§5 连接方向、§9 变更 #001）
- `research/plans/minecraft-layer/03-build-and-module-layout.md`（§2 版本目录、§4 plugin.yml、§10 升级策略）
- `research/plans/minecraft-layer/06-next-step-plan.md`（§4 环境事实与风险）
- `research/projects/2026-09-14-mc-vertical-slice/`（README 环境段、`handover-checklist.md` §B、`plans/01`）
- `layers/README.md`（部署到云端 + dial 模式 + 确定性控制）
