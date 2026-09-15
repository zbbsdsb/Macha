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

Paper 26.2 需要 **Java 25**，本机默认 PATH/JAVA_HOME 是 JDK 21，因此脚本显式使用 Temurin 25：

```
C:\Users\chkev\.gradle\jdks\eclipse_adoptium-25-amd64-windows.2\bin\java.exe
```

```powershell
cd layers

# 第一次：联网下载 Paper 26.2 build 123 → 校验 sha256 → 写 eula/server.properties → 前台起服
.\scripts\run-server.ps1

# 托管模式（自动化）：后台启 → 等 "Done" 写 .ready → 等 .stop 标记后停服
.\scripts\run-server.ps1 -Managed -SkipDownload

# 服务器"家"目录固定为 layers/run/minecraft/（不入库）
# 插件装入：把 build/libs/minecraft-0.1.0-all.jar 复制到 layers/run/minecraft/plugins/
```

脚本职责：下载/校验 jar、写 `eula.txt`（UTF-8 无 BOM，见下）、写最小 `server.properties`、起服。
不包含任何协议/插件逻辑。

### 关键点

- **`level-name=macha_world`**：绕开 Windows 上无法删除的老 `world/` 目录及其
  `java.nio.file.NoSuchFileException: .\world\data\minecraft` 崩溃。
- **EULA BOM 坑**：`eula.txt` 首行必须是无 BOM 的 `eula=true`；带 BOM 会被 Paper 判为"未同意"。
- **minimal props**：`online-mode=false`、`level-type=flat`、`spawn-protection=0`、`view-distance=6`。

## 验证

```powershell
# 插件加载后（控制台）：
#   [MachaMinecraftLayer] Macha Minecraft Layer v0.1.0 up — protocol v0, transport 127.0.0.1:8765
#   Done (12.761s)! For help, type "help"
curl.exe http://127.0.0.1:8765/healthz        # → {"ok":true,"protocol":"0"}
curl.exe http://127.0.0.1:8765/capabilities    # → 4 条能力 move/look/interact/spawn_agent
```

`layers/run` 不入库：`git status --porcelain --untracked-files=all -- layers/run` 应为空。

## 已知限制

- **Shadow relocate 未做**：fat jar 未配置 Shadow 的 relocate（relocation prefix 尚未定），
  `minecraft-0.1.0-all.jar` 直接打包类与依赖。见 `03-build-and-module-layout.md` §3 与待回答 #3。
- **v0 无数据面**：WebSocket 观测/事件/动作执行尚未实现（M1+）；当前仅 HTTP 控制面
  （healthz / capabilities）。