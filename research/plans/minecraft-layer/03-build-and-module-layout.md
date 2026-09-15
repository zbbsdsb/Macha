# 构建、模块与边界守护（Gradle / Paper / Kotlin）

> **STATUS: PENDING — 草案。** 配套 [`00-technical-foundation.md`](00-technical-foundation.md)。
> 本文件只定义**工程骨架与规则**；不含实现代码。所有版本来自 2026-09-13 官方来源（见 00 §C）。

---

## 1. 目录与构建根

```text
Macha/                                  # 仓库根（Python 项目，禁止放 Gradle 文件）
└── layers/                             # 【新增】独立 Gradle 构建根
    ├── settings.gradle.kts             # include(":kit:protocol", ":kit:runtime", ":kit:transport",
    │                                   #         ":minecraft", ":simulator", ":testclient")
    ├── build.gradle.kts                # 共享配置 + 边界守护任务（§7）
    ├── gradle.properties
    ├── gradle/{libs.versions.toml, wrapper/}
    ├── .gitignore                      # build/ .gradle/ .kotlin/ run/
    ├── kit/                            # 共享内核（纯 JVM，零环境依赖）
    │   └── protocol/  runtime/  transport/
    ├── minecraft/                      # 唯一依赖 paper-api（环境子树）
    ├── simulator/                      # 假环境（C4 对照条件）
    ├── testclient/                     # 垂直切片测试客户端
    └── run/                            # 运行期产物（gitignored）
```

**为什么不在仓库根建 Gradle**：根是 Python 项目（`pyproject.toml`）；根级 `settings.gradle.kts`
会把整仓声明为 Gradle 项目，未来拆仓要拆两次（`00` §A.3）。

`settings.gradle.kts`：

```kotlin
rootProject.name = "macha-layers"
include(":kit:protocol", ":kit:runtime", ":kit:transport", ":minecraft", ":simulator", ":testclient")
```

**为什么共享内核收进 `kit/`**：让"共享内核 vs 环境实现"在磁盘上可见——`layers/minecraft/` 与
整个 `layers/kit/` 并列，而不是与 `protocol/` 平级。纯构建布局改动，Kotlin 包名不变
（决策记录 `decision-layers-directory-layout.md`）。

**为什么从第一天就是多模块**：`:kit:protocol` / `:kit:runtime` / `:kit:transport` 会被**两个环境
模块**（`:minecraft`、`:simulator`）共用，这是 V4 的前提；而把 `paper-api` 限定在 `:minecraft`，
使"Paper 不得渗入协议与运行时"成为**编译期**约束，而不是靠 lint 提醒（`04` §2）。

包根统一 `dev.macha.layer.*`；完整文件清单见 [`04-project-structure.md`](04-project-structure.md)。

---

## 2. 版本锁定（Version Catalog）

`gradle/libs.versions.toml` 中集中锁定（数值见 `00-technical-foundation.md` §C.1）：

| key | 值 | 备注 |
|---|---|---|
| `minecraft` | `26.2` | 仅作文档/日志，不参与编译 |
| `paper` | `26.2-123`（jar sha256 记录在案） | 服务端 pin |
| `java` | `25`（toolchain） | 若 KGP 不支持 → 21（`00` §H-D2） |
| `kotlin` | `2.4.20` | 与 KGP 同版本 |
| `gradle` | `9.7.1`（wrapper） | 备选 8.14.5 |
| `paperApi` | `26.2-R0.1-SNAPSHOT` 或对应 release 坐标 | scaffold 时以仓库实际坐标为准 |
| `kotlinxSerialization` | 当前最新稳定 | scaffold 时从 Maven Central 取 |
| `javaWebsocket` | `1.6.0` | 已验证存在 |
| `junit` | 5.x 当前稳定 | scaffold 时确认 |
| `shadow` | 8.x/9.x 当前稳定 | scaffold 时确认 |

规则：
- **任何版本不得散落在 `build.gradle.kts` 里**；
- 仓库坐标：Paper 用 `https://repo.papermc.io/repository/maven-public/`；
- 构建可复现：启用 Gradle **dependency verification / lockfile**，并把 Paper server jar 的
  sha256 写进 `docs`（不是仓库）。

---

## 3. 打包策略（Shadow，relocate）

```kotlin
dependencies {
    compileOnly(paperApi)                       // 运行期由服务器提供 → 禁止打包
    implementation(kotlinStdlib)                // Paper 不提供 Kotlin
    implementation(kotlinxSerializationJson)
    implementation(javaWebsocket)
}
```

| 项 | 规则 |
|---|---|
| `paper-api` | **只能 `compileOnly`**；若被打进 jar = 类冲突（红线） |
| Kotlin stdlib / serialization / websocket | 必须随插件分发；用 Shadow 打成 fat jar 并 **relocate** 到 `dev.macha.layer.libs.*` |
| Paper 自带库（Gson、Netty、Adventure 等） | **禁止依赖**：版本随服务器漂移；也避免与插件自带库冲突 |
| 服务端 jar | **不进仓库**；由脚本按 pin 版本 + sha256 下载 |

替代方案（若 Shadow 与 Gradle 9 组合不顺）：用 `plugin.yml` 的 `libraries:` 让 Paper 在启动时
从 Maven Central 拉依赖。取舍：省去 shade，但**首次启动需联网**，且版本解析不在本地可复现。
**建议：Shadow**（离线可复现优先）。

---

## 4. `plugin.yml`（最小）

```yaml
name: MachaMinecraftLayer
version: '0.1.0'
main: dev.macha.minecraft.plugin.MachaMinecraftPlugin
api-version: '26.2'      # scaffold 时按 Paper 实际要求填写
description: Macha Environment Integration Layer for Minecraft (v0)
authors: [Macha Team]
```

v0 不放 `commands`、不放 `permissions`（除非调试需要一条 `/macha status`；那也属于 `plugin/`，
不属于协议）。

---

## 5. `config.yml`（最小）

| key | 默认 | 说明 |
|---|---|---|
| `transport.bind` | `127.0.0.1` | 默认只回环，不外网暴露 |
| `transport.port` | `8765` | HTTP 控制面（healthz/capabilities/action）；分端口见 00 §H-D5 |
| `transport.ws_port` | `8766` | WebSocket 数据面（`ws://…/ws`）；分端口（M1 定案） |
| `transport.token` | 空 | 可选；v0 允许无鉴权（本地） |
| `agent.default_binding` | `nearest_zombie` | v0 用现成生物作被测对象（00 §H-D4） |
| `observation.radius` | `16.0` | 观测窗口 |
| `observation.max_entities` / `max_blocks` | `16` / `32` | 截断上限 |
| `observation.push_interval_ticks` | `20` | 推送间隔 |
| `events.subscribe_default` | `all` | 可改为 kind 列表 |
| `log.level` | `INFO` | 协议日志与业务日志分开 |

---

## 6. 线程与调度规则（写死，避免崩服与卡 tick）

| 场景 | 规则 |
|---|---|
| 读世界状态（采集 observation） | **主线程**；采集后立刻转换为纯数据 DTO，再交给网络线程发送 |
| 执行 action | 网络线程解码 → `runtime` 校验 → `runTask` 回**主线程**调用 Paper API → 结果写回结构 → 网络线程回传 |
| 事件监听 | 主线程回调里**只做归一化 + 入队**；禁止在监听器里做 IO/序列化/网络发送 |
| 背压 | 队列有界；溢出时按策略丢弃并置 `truncated`/计数（v0 不做完整流控） |
| 关服 | `onDisable` 里关闭 WS/HTTP、停队列、flush transcript（M9 回放文件） |
| 超时 | action 在 N tick 内未完成 → `action_result(status=failed, reason=internal)` 或 `pending`（见 01 §8-4） |

---

## 7. 边界守护（Boundary Guard）

**第一道防线是 Gradle 模块依赖（编译期）**：`paper-api` 只出现在 `:minecraft` 的 `build.gradle.kts`
里，因此 `:kit:protocol` / `:kit:runtime` / `:kit:transport` / `:simulator` 一旦引用 Bukkit 类型就
**编译不过**。这比"扫描 import 再报警"强一个量级（`04` §2）。

**第二道防线是 import 扫描任务**（捕获模块内不该出现的环境字面量与类型引用）：

1. **Paper 范围检查**：扫描 `layers/*/src/main/kotlin`，除 `minecraft/src/main/kotlin/**/plugin/`
   与 `**/adapter/` 之外，出现 `import org.bukkit` / `io.papermc` / `net.minecraft` → **构建失败**。
2. **协议洁净检查**：扫 `layers/kit/protocol/src`、`layers/kit/runtime/src`、`layers/simulator/src`，
   禁止出现环境专有标识（`org.bukkit`、`Material`、`BlockData`、`World` 类型引用）；
   `minecraft:<verb>` 这类命名空间**字符串常量**允许存在（词表校验需要），但必须集中在
   `ActionVocabulary` / `ActionMapping` 两处。
3. **Core 洁净检查**：扫仓库根的 `src/macha/**`，禁止出现任何 Minecraft/Kotlin/Gradle 相关
   标识（V2 的可自动检查部分）。
4. 三个任务挂到 `check`（并建议在 CI 上跑）。
   **已更新（commit `ead3a3d`）**：`ktSources` 改为 `**/src/main/kotlin/**/*.kt`，
   `verifyEnvClean` 目录列表改为 `kit/protocol`、`kit/runtime`、`simulator`，
   并给两个任务加了"扫到 0 个文件即抛异常"防呆；`stripComments` 已支持跨行块注释。

> 这三个检查直接对应验证计划的 **V1/V2/V3**："接入期间 Core 零改动""Core 内不出现 Minecraft 概念"
> "Layer 内不出现认知"。它们不是洁癖，而是让证伪判据可执行。

---

## 8. 测试策略

| 层 | 工具 | 覆盖 |
|---|---|---|
| 单元 | JUnit 5 + kotlin-test（**无 Paper 依赖**） | `protocol` 编解码往返、schema 校验、版本协商；`runtime` 能力校验与 refusal 分支；`observation` 截断策略 |
| 契约 | 录制回放 | 用 NDJSON transcript（M9）回放消息序列，断言 Layer 行为一致 |
| 集成 | **run-paper** 起真实 Paper 26.2 + 脚本化测试客户端 | vertical slice 8 步（00 §F），特别是 action → world change → event 闭环 |
| 边界 | Gradle 检查任务（§7） | 隔离规则 |

不引入 MockBukkit：mock 与真实 Paper API 漂移会给出假安全感；v0 用真服务器更便宜也更可信。

---

## 9. 开发循环（dev loop）

```text
./gradlew build              # 编译 + 单测 + 边界检查
./gradlew runPaper           # 启动本地 Paper 26.2（run-paper）
# 客户端连入 → /op 自己 → 手测 move/look
./gradlew test               # 单元 + 契约
```

测试客户端（外部程序）建议先用最短脚本：连 WS → `hello` → 收 `hello_ack` → 发一次 `move` →
断言 `action_result` → 等 `event`。这就是 Step 6–8 的自动化版本。

---

## 10. 版本升级策略

| 情况 | 做法 |
|---|---|
| Paper 26.2 出新的 build | 直接升 build 号；重跑 vertical slice 脚本；**协议 `v` 不变** |
| Minecraft 进入 26.3 | 单独一次升级任务：重跑 vertical slice + 事件字段回归；协议 `v` 仍不变（适配在 Layer 内部） |
| 26.2 线出现阻塞问题 | 回退到 26.1.2 基线（`00` §C.2 已记录） |
| Kotlin / Gradle 升级 | 只在有明确收益时做；先跑 boundary check + 单测 |
| 协议变更 | **先改 `01-protocol-v0.md`，再改代码**；版本号递增并记录 |

---

## 11. 待回答

1. ~~`paper-api` 的准确坐标与 `api-version` 取值~~（**M0 已确认**：`api-version: '26.2'` 在 Paper `26.2-123` 上被正常接受并加载，见下文附录）。paper-api 编译坐标以仓库实际发布为准。
2. Gradle 9.7.1 vs 8.14.5 的最终选择（KGP 兼容矩阵）。
3. Shadow 版本与 Gradle 9 的兼容性；relocate 前缀最终命名。
4. 是否需要 `kotlinx-coroutines`，还是简单队列足够（倾向后者，少一个依赖）。
5. transcript（M9）落盘格式与轮转策略。

---

## 附录：M0 起服实测注记（2026-09-15，Paper 26.2-123）

用 `layers/scripts/run-server.ps1` 起真实 Paper 服务器、加载插件、拿到 healthz，实测结论如下。

- **运行时 JDK**：Paper 26.2 需 **Java 25**；本机默认 PATH/JAVA_HOME 是 JDK 21，因此起服必须显式用
  `C:\Users\chkev\.gradle\jdks\eclipse_adoptium-25-amd64-windows.2\bin\java.exe`（Temurin 25.0.4.1）。
- **EULA 必坑（BOM）**：PowerShell 写 `eula.txt` 若带 UTF-8 BOM（`EF BB BF` 前缀），Paper 读首行 `eula=true`
  会误判"未同意 EULA"而拒启。脚本改为每次用 `UTF8Encoding($false)` 无 BOM 重写 `eula.txt`。
- **世界目录报错规避**：老/损坏的 `world/` 可能在 Windows 上无法删除且触发
  `java.nio.file.NoSuchFileException: .\world\data\minecraft`。脚本通过 `level-name=macha_world`
  让服务器用全新目录，彻底绕开该残留目录。
- **`api-version: '26.2'`**：在 Paper `26.2-123` 上被接受，插件正常加载（无 `incompatible` 报错），
  无需回退到旧 api-version。
- **Relocate 未做**：fat jar 未做 Shadow relocate（见 §3），作为已知限制记录。
- **验收输出**：
  - 控制台：`Done (14.340s)! For help, type "help"` / `Done (12.761s)!`
  - 插件：`Macha Minecraft Layer v0.1.0 up — protocol v0, transport 127.0.0.1:8765`
  - `curl http://127.0.0.1:8765/healthz` → `{"ok":true,"protocol":"0"}`
  - `curl http://127.0.0.1:8765/capabilities` → 4 条能力（move/look/interact/spawn_agent）
