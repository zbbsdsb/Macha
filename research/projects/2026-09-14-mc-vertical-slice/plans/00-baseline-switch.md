# 计划零：P0 基线切换（本地 → 1.20.1；构建 → 下界；传输 → 可配）

> **STATUS: READY — 可执行。** 预估 **≤1 人日**（含一次云端冒烟）。
> 决策依据：[`../../../../papers/notes/accepted/decision-arclight-cloud-environment.md`](../../../../papers/notes/accepted/decision-arclight-cloud-environment.md)
> 上游：项目 [`README.md`](../README.md) §5（两个环境）· §7（外部信息源验收定义）
> 下游：[`01-server-and-handshake.md`](01-server-and-handshake.md)（M1）

---

## 0. 现状实测基线（2026-09-15 逐项核对，不是回忆）

| 项 | 现状 | 位置 / 证据 |
|---|---|---|
| 编译期 API | `io.papermc.paper:paper-api` **26.2.build.123-stable** | `layers/gradle/libs.versions.toml` |
| JVM 目标 | `jvmToolchain(25)` + `JvmTarget.JVM_25`，**6 个模块全有** | `layers/{kit/protocol,kit/runtime,kit/transport,minecraft,simulator,testclient}/build.gradle.kts` |
| 插件声明 | `api-version: '26.2'` | `layers/minecraft/src/main/resources/plugin.yml` |
| 本地服务器 pin | Paper **26.2 build 123**，sha256 `7b7b3b43…fecd08` | `layers/scripts/run-server.ps1` |
| 传输 | 只有 `listen`；WS 数据面仍是 stub；HTTP 只有 `/healthz` + `/capabilities` | `kit/transport/WebSocketDataPlane.kt` 等 |
| 边界守护 | `verifyPaperScope` / `verifyEnvClean` / `verifyCoreClean` + 聚合 `check` | `layers/build.gradle.kts` |
| **`import io.papermc.*` 引用** | **0 处**（现在只用 `org.bukkit.*`） | 全仓 grep 实测 → **守护任务加上不会立刻变红** |
| 服务器家目录 | `layers/run/minecraft/`，`level-name=macha_world`（**26.2 世界**） | 已被 `.gitignore` 的 `run/` 覆盖 |
| M0 | ✅ `Done (9.701s)` + 插件日志 + `/healthz` 实测 | `plans/01` §M0 遗留修正 |

## 1. 目标与判据

**目标（一句话）**：**一份 jar，两个环境**——本机可复现回路与云端实验环境跑同一产物；且本地换到与云端**同版本**。

四条硬判据（缺一不可）：

1. `./gradlew check` 全绿（含新增守护）；
2. `grep -rn "import io.papermc" layers` → **0 处**；
3. 本地 Paper **1.20.1-196** 上加载成功 + `/healthz` → `{"ok":true,"protocol":"0"}`；
4. 云端 Arclight **1.20.1** 上加载成功（原始日志行）+ **同一 jar sha256**。

**为什么本地也换 1.20.1**：云端是 **Arclight**（Bukkit 实现是子集、事件行为可能不同）。
两边**同版本、不同实现** → "行为差异"只可能来自实现，而不是版本；这也是 V4/E3 想要的对照。

## 2. 步骤（顺序即执行顺序）

> 顺序不是随意的：**S0 先加纪律**（当前 0 违规，加了必绿；若红说明现状就违规，必须先暴露）；
> **S1–S3 一起改完再编译**（依赖/JVM/声明是同一件事的三面）；**S4 换服务器**（要重新下载并起新世界）；
> **S5 传输**与版本无关但云端必需；**S6 云端冒烟**放最后（只验加载，不验功能）。

### S0 新增守护任务 `verifyBukkitOnly`（先做）

- 文件：`layers/build.gradle.kts`
- 内容：新任务，挂在 `check` 上；**禁止** `import io.papermc.`（含 `:minecraft`）；沿用
  `scanned == 0 就抛错` 的防呆；错误信息指到文件:行。
- 为什么先做：把"下界构建"从**愿望**变成**可检查约束**。没有它，本地 Paper 跑得好好的、
  某天有人 import 一个 Paper 类，云端 Arclight 直接 `NoClassDefFoundError`。
- 绿判据：`./gradlew verifyBukkitOnly` 通过（当前 0 违规）。
- 时间盒：**15 分钟**

### S1 依赖降到 1.20.1

- 文件：`layers/gradle/libs.versions.toml`（`paperApi` → `1.20.1-R0.1-SNAPSHOT`；`java` → `"17"`）
- 坐标选择：优先 `io.papermc.paper:paper-api:1.20.1-R0.1-SNAPSHOT`（现有 papermc 仓库即可解析，
  不新增 `hub.spigotmc.org`）。它是 Bukkit API 的**超集**，唯一风险是误用专有类 → 由 S0 堵住。
- 退路：解析失败则改 `org.spigotmc:spigot-api:1.20.1-R0.1-SNAPSHOT` + 加 Spigot 仓库（守护不变）。
- 时间盒：**20 分钟**

### S2 JVM 降到 17

- 文件：**6 个** `build.gradle.kts`：`jvmToolchain(17)` + `JvmTarget.JVM_17`
- 好消息：Gradle 缓存里**已有** Temurin 17（`eclipse_adoptium-17-amd64-windows.2`），不需下载。
- 时间盒：**10 分钟**

### S3 插件声明对齐

- 文件：`layers/minecraft/src/main/resources/plugin.yml` → `api-version: '1.20'`（保留 `load: POSTWORLD`、`main`）
- **S1–S3 完成后统一编译**：`cd layers && ./gradlew check` → 必须全绿（含 20 例单测与四个守护任务）
- 时间盒：**10 分钟 + 一次构建**

### S4 本地回路换 Paper 1.20.1

- 文件：`layers/scripts/run-server.ps1`
  - 版本表化：`paper 1.20.1 / build 196 / sha256 234a9b32098100c6fc116664d64e36ccdb58b5b649af0f80bcccb08b0255eaea`
    （43,230,582 bytes）；
  - **jar 用带版本的文件名**（`paper-1.20.1-196.jar`），避免与旧 26.2 jar 同名时
    `Ensure-Jar` 走"sha 不匹配 → 删除并抛错"那条路（现有逻辑，安全但要多跑一次）；
  - `level-name` 换新名字（如 `macha_world_120`）——**26.2 的世界不能被 1.20.1 读**；
  - JDK 解析顺序里加 17（与云端一致）。
- 旧数据不动：`world_old/`、旧 `macha_world/` 留在 `run/` 里（已 gitignored）。
- 绿判据：`Done (...)` + 插件启动日志 + `curl /healthz` → `{"ok":true,"protocol":"0"}`
- 时间盒：**30 分钟**（含首次下载 43 MB）

### S5 传输方向可配（`transport.mode`）

- 文件：`kit/transport/`（新增 mode 分支）+ `layers/minecraft/src/main/resources/config.yml`（`mode`、`runtime.endpoint`、`token`）
- 语义：`listen`（默认，本地 Runtime→Layer）/ `dial`（云端 Layer→Runtime，**强制 token**）；
  **消息形状不变**（已在 `01` §5 与 §9 #001 登记）。
- 绿判据：`listen` 下 M1 未做也不影响——本步只需**配置可读、模式可选、dial 能发起连接尝试并给出明确日志**。
- 时间盒：**1–2 小时**

### S6 云端冒烟（**只验证"能加载"**，不验证功能）

- 人做：面板上传 `minecraft-0.1.0-all.jar` → 重启 → 抓插件启动日志行 → **记录上传 jar 的 sha256**（云端的版本 pin）
- 同时开启实验环境确定性控制：`white-list=true`、固定世界/种子
- 绿判据：云端控制台出现 `Macha Minecraft Layer v0.1.0 up — protocol v0, transport 127.0.0.1:8765`
  （`dial` 模式下日志应显示目标 endpoint 而非监听地址）
- 时间盒：**30 分钟**

## 3. 分工与时间盒

| 步骤 | 谁 | 时间盒 |
|---|---|---|
| S0 守护任务 | agent | 15 min |
| S1+S2+S3 依赖/JVM/声明 + 构建 | agent | 40 min |
| S4 本地服务器换版本 | agent（可自主跑） | 30 min |
| S5 `transport.mode` | agent | 1–2 h |
| S6 云端冒烟 + whitelist | **人**（面板权限/重启时机） | 30 min |
| 合计 | | **≤1 人日** |

## 4. 明确不做（本阶段边界）

- **不实现 M1** 的 WS 数据面 / `hello` / `hello_ack` / `/action`（那是下一步；`prompts/02` Part 2）。
- **不碰协议字段**；本阶段唯一协议相关动作是 S5 的**传输绑定**（已登记）。
- **不重构、不加依赖、不改包名、不动 `src/macha/**`、不提交 `layers/run/**`**。
- **不为 26.2 保留第二套构建**（升级信号见决策记录 §7）。
- **不修** M0 遗留 A–F 中与版本无关的项（能力清单削平、强杀停服、配置覆盖、JDK 硬编码、jar 命名、标记清理）
  —— 它们归 **M1 前置**，见 [`../prompts/02-M0-leftovers-and-M1-handshake.md`](../prompts/02-M0-leftovers-and-M1-handshake.md)
  Part 1；S4 会**顺带**解决其中的"JDK 硬编码"与"jar 命名"两条。

## 5. 证据清单（每条都要贴原始输出）

- [ ] `./gradlew verifyBukkitOnly` 输出（通过）
- [ ] `grep -rn "import io.papermc" layers` → 0 行
- [ ] `./gradlew check` 尾部（测试数 + 四个守护任务）
- [ ] 本地 `Done (...)` 行 + 插件 `up` 日志行
- [ ] `curl http://127.0.0.1:8765/healthz` 原始 JSON
- [ ] 云端插件加载日志行 + **上传 jar 的 sha256**
- [ ] `git status --porcelain --untracked-files=all -- layers/run` → 空

## 6. 风险与升级阈值

| 风险 | 触发信号 | 处置 |
|---|---|---|
| `paper-api:1.20.1-R0.1-SNAPSHOT` 解析失败 | S1 构建报 `Could not find` | 换 `org.spigotmc:spigot-api:1.20.1-R0.1-SNAPSHOT` + Spigot 仓库；守护不变 |
| `verifyBukkitOnly` 一加上就红 | S0 就报违规 | **停下来报告**（说明现有代码已有 Paper 专有用法）；不要为了变绿而放宽规则 |
| Kotlin/Gradle 在 JDK 17 下行为异常 | S3 构建失败 | 先记录完整报错；必要时把 Gradle 降到 8.14.5（`03` §2 备选） |
| Arclight 缺某个 Bukkit 事件 | M4 实测时 | 记 `research/failures/`（F-类：环境能力缺失），换等价事件；**不在本阶段处理** |
| 旧 26.2 世界与新版本冲突 | S4 起服报错 | 已用新 `level-name` 规避；旧目录留着不动 |
| 云端上传后插件不加载（Arclight 差异） | S6 日志无插件行 | 贴完整报错；可能是 `api-version` 或 Bukkit 子集问题 → 回写 `03` §4 |

## 7. 回滚点

- 每个 S 步单独提交；回滚 = `git revert <该步 commit>`。
- **S1–S3 必须同一个 commit**（依赖/JVM/声明是一体的，拆开会出现"半个版本"的中间态）。
- 旧 26.2 的 `paper-server.jar`、`macha_world/`、`world_old/` 留在 `layers/run/` 里不删 → 需要时可切回。

## 8. 完成之后

P0 全绿 → 直接进 **M1（握手）**：`plans/01-server-and-handshake.md`（含 M0 遗留 A–F）。
"外部信息源"的验收定义见 [`../README.md`](../README.md) §7 —— M2/M4 就是它的实装。
