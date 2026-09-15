# Macha Layers

Macha 的 Gradle 多模块构建根（`kit` / `minecraft` / `simulator` / `testclient`）。

- 基础设施文档：`../research/plans/minecraft-layer/`
- 架构/roadmap：`../docs/`

> `layers/run/` 是**运行期产物**，不入库（由 `layers/.gitignore` 的 `run/` 忽略）。
> 版本化的只有"怎么起"的知识：`layers/scripts/` 与本文档。

## 目录

```text
layers/
├── settings.gradle.kts          # include :kit:protocol/:kit:runtime/:kit:transport/:minecraft/:simulator/:testclient
├── build.gradle.kts             # 共享配置 + 边界守护任务
├── gradle/libs.versions.toml    # 版本锁定（Paper 26.2-123、Kotlin、Gradle）
├── kit/                         # 共享内核（纯 JVM，零环境依赖）
├── minecraft/                   # Paper 插件（唯一依赖 paper-api）→ 产出 fat jar
├── simulator/ testclient/       # 假环境 / 垂直切片测试客户端
├── scripts/                     # 版本化脚本（run-server.ps1）
└── run/                         # 运行期，不入库
```

## 构建插件

```powershell
cd layers
.\gradlew :minecraft:shadowJar        # 产出 build/libs/minecraft-0.1.0-all.jar
# （完整本地校验：.\gradlew build --offline——含 F1 往返测试与边界守护任务）
```

## 起 Paper 服务器（M0）

Paper 26.2 需要 **Java 25**，本机默认 PATH/JAVA_HOME 是 JDK 21。脚本按以下顺序解析 JDK 25
（**不写死任何用户名路径**，M0-D）：

1. 环境变量 `$env:MACHA_JDK25`（指向某 JDK 25 的 `bin\java.exe`）；
2. 探测 `$env:USERPROFILE\.gradle\jdks\*\bin\java.exe` 中 `java -version` 带 `"25` 的那一版；
3. 常见安装目录（`Program Files\Eclipse Adoptium` 等）；
4. 都找不到 → 报错并给出操作指引。

```powershell
cd layers

# 第一次：联网下载 Paper 26.2 build 123 → 校验 sha256 → 确保 eula/server.properties → 前台起服
.\scripts\run-server.ps1

# 托管模式（自动化）：后台启 → 等 "Done" 写 .ready → 等 .stop → RCON 优雅停服
.\scripts\run-server.ps1 -Managed -SkipDownload

# 强制把 server.properties 按脚本默认重建（默认不会覆盖已存在文件的其它键）
.\scripts\run-server.ps1 -Managed -ResetConfig

# 服务器"家"目录固定为 layers/run/minecraft/（不入库）
# 插件装入：把 build/libs/minecraft-0.1.0-all.jar 复制到 layers/run/minecraft/plugins/
```

脚本职责：下载/校验 jar（**sha256 才是真正的锁**，文件名统一 `paper-server.jar`，M0-E）、
确保 `eula.txt`（UTF-8 无 BOM）、确保 `server.properties`（仅管理脚本自己的键，其余原样保留，
M0-C）、启动、`Managed` 下收到 `.stop` 后用 RCON 优雅停服（M0-B）。不包含任何协议/插件逻辑。

### 关键点

- **JDK 25 解析**：见上；`$env:MACHA_JDK25` 最优先。
- **优雅停服（RCON，M0-B）**：`server.properties` 打开 `enable-rcon=true` 并在 `.stop` 时发 `stop`，
  从而在 `console.log` 留下 `Stopping server` / `Saving players`。`Managed` 退出时清理 `.ready/.stop/.pid`（M0-F）。
- **`level-name=macha_world`**：绕开 Windows 上无法删除的老 `world/` 目录及其
  `java.nio.file.NoSuchFileException: .\world\data\minecraft` 崩溃。
- **`world_old/` 说明（M0-F）**：早期一次失败的 `world/` 残留目录（含无法删除的空
  `world/data/minecraft`）未强删，改由 `level-name` 绕开并在服务器目录留下 `world_old/` 孤儿；
  `layers/run/` 整目录不入库，无害，可随服务器目录一并清理。
- **EULA BOM 坑**：`eula.txt` 首行必须是无 BOM 的 `eula=true`；带 BOM 会被 Paper 判为"未同意"。
- **managed props（M0-C）**：脚本只会更新/补齐 `online-mode/level-type/spawn-protection/view-distance/
  level-name/enable-rcon/rcon.port/rcon.password` 这些键；`server.properties` 里其它键（如
  `difficulty`）即使手工改过也会保留。

## 验证

**期望输出（与本仓库当前锁定的协议/能力一致）**：

```powershell
# 期望：插件加载后控制台约含
#   [MachaMinecraftLayer] Macha Minecraft Layer v0.1.0 up — protocol v0, transport 127.0.0.1:8765
#   [MachaMinecraftLayer] WebSocket data plane up on 127.0.0.1:8766 (http control plane on 8765)
#   Done (...)!
curl.exe http://127.0.0.1:8765/healthz              # → {"ok":true,"protocol":"0"}
curl.exe http://127.0.0.1:8765/capabilities          # → 4 条能力，各带 args + verifiability
curl.exe -X POST -H "Content-Type: application/json" --data-binary "@body.json" http://127.0.0.1:8765/action
                                                     # → action_result status=refused reason=not_supported
# WS 数据面（分端口，00 §H-D5）：hello → hello_ack
.\gradlew :testclient:run --offline --args="127.0.0.1 8766 happy"        # → handshake ok, probe exit=0
.\gradlew :testclient:run --offline --args="127.0.0.1 8766 bad-version"  # → error code=bad_version
```

`layers/run` 不入库：`git status --porcelain --untracked-files=all -- layers/run` 应为空。

**实测（2026-09-15，M0 Part 1-A）**：

```json
# GET /healthz
{"ok":true,"protocol":"0"}

# GET /capabilities  （修复手写 JSON 后：args/preconditions/verifiability/cost 不再丢）
[{"name":"move","args":{"target":"vec3"},"preconditions":["chunk_loaded"],
  "expected_effect":"position change","verifiability":"checked"},
 {"name":"look","args":{"yaw":"number","pitch":"number"},"verifiability":"checked"},
 {"name":"interact","args":{"target":"entity|block"},"preconditions":["in_range"],
  "verifiability":"trusted"},
 {"name":"spawn_agent","args":{"type":"string","position":"vec3"},
  "verifiability":"checked","cost":"moderate"}]
```

> 上述 JSON 为单行压缩输出，此处换行仅为可读性。

## 已知限制

- **Shadow relocate 未做**：fat jar 未配置 Shadow 的 relocate（relocation prefix 尚未定），
  `minecraft-0.1.0-all.jar` 直接打包类与依赖。见 `03-build-and-module-layout.md` §3 与待回答 #3。
- **v0 数据面仅握手**（M1）：WebSocket 已能 `hello → hello_ack`（含版本协商，不兼容回
  `error(bad_version)`）；但观测采集/事件推送/动作执行仍留 M2+（Paper adapter 的
  `observe/events/actions` 未接线，动作统一 `refused(not_supported)`）。
- **Provenance 命名回差**（M1 记录，未修）：协议文档 `01 §3.5` 用 `provenance.decided_by`（snake_case），
  而 `Payloads.kt` 的 `Provenance.decidedBy`（camelCase）序列化后为 `decidedBy`——发带 provenance 的
  `action` 会被判 `schema_violation`。v0 内字段名改动需先在 `01` §9 登记，故列为待决项。