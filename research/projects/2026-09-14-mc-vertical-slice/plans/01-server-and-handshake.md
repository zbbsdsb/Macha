# 计划一：起服 + 加载 + 握手（M0–M1）

> 里程碑定义见 [`../../../plans/minecraft-layer/06-next-step-plan.md`](../../../plans/minecraft-layer/06-next-step-plan.md) §2。
> 预估：**M0 半天；M1 +1–2 天。** 依赖：无（本计划是全部后续的咽喉）。

---

## M0 · 服务器活着，插件加载成功（半天）

**结果**：控制台 `Done`；插件启动日志；`/healthz` 返回 `{"ok":true,"protocol":"0"}`。

### 步骤

1. 建目录与脚本（脚本**版本化**，服务器目录**不入库**）：
   - `layers/scripts/run-server.ps1` —— 职责：下载并 **sha256 校验** `paper-26.2-123.jar` → 写入 `eula.txt` →
     写最小 `server.properties`（`online-mode=false`、`level-type=flat`、`spawn-protection=0`、`view-distance=6`）→
     用 **JDK 25 路径**启动（`-Xms1G -Xmx2G`）
   - `layers/run/minecraft/` —— 服务器"家"目录（jar / eula / properties / world / logs / plugins / libraries）
2. 首次启动到 `Done`，停服；把 `layers/minecraft/build/libs/minecraft-0.1.0-all.jar` 放进
   `layers/run/minecraft/plugins/`
3. 再次启动，观察插件加载

### 验收（逐条贴原始输出）

- [ ] 控制台出现 `Done`
- [ ] 插件日志：`Macha Minecraft Layer v0.1.0 up — protocol v0, transport 127.0.0.1:8765`
- [ ] `curl http://127.0.0.1:8765/healthz` → `{"ok":true,"protocol":"0"}`
- [ ] `curl http://127.0.0.1:8765/capabilities` → 4 条能力
- [ ] `git status --porcelain --untracked-files=all -- layers/run` **为空**
- [ ] `layers/README.md` 已写：怎么 build / 怎么起服 / 怎么验证（含 JDK 25 路径与 relocate 限制）

### 常见失败

| 现象 | 原因 | 处置 |
|---|---|---|
| `UnsupportedClassVersionError` / 启动即崩 | 用了 PATH 上的 JDK 21 | 改用 §B 的 JDK 25 路径 |
| 插件 `Unknown/missing dependency` 或加载失败 | `api-version: '26.2'` 被拒 | 按报错改 `plugin.yml` 的 `api-version`，重启验证，**回写 `03` §4** |
| 端口占用 | 8765 被占 | 改 `config.yml` 的 `transport.port`，记录实际端口 |

### M0 遗留修正（2026-09-15 复核发现，**M1 必须一并处理**）

| # | 问题 | 证据 | 要求在 M1 之前/之内解决 |
|---|---|---|---|
| **A** | **能力清单在传输时被削平**：`/capabilities` 实测 `"args":{}` 全空，`preconditions` / `verifiability` / `cost` 全丢，`expected_effect` 仅 move 有值 | 原始 JSON：`[{"name":"move","args":{},"expected_effect":"position change"},{"name":"look","args":{},"expected_effect":""} …]`；`MachaMinecraftPlugin.capabilityManifestJson()` 是**手写 JSON 拼接** | 用已有的 `ProtocolV0.json` 序列化 `Capability`；补**往返测试**；`hello_ack` 不得沿用有损函数（否则违反 `01` §3.2 与 M4） |
| **B** | **托管停服是强杀**：console.log 无 `Stopping server` / `Saving players`，靠 `Stop-Process -Force` | 停服后 console.log 无优雅关服标记 | 重定向 stdin 并喂 `stop`（或 RCON）；至少在 `layers/README.md` 写明世界损坏风险与备份方式 |
| **C** | `server.properties` **每次启动被重写**，人工改动被静默丢弃 | `Ensure-Config` 无条件覆盖；盘上有 `server.properties.bak` | 改为"缺失时才写"，或加 `-ResetConfig` 开关 |
| **D** | JDK 25 路径**硬编码到单机用户目录**，脚本已入库 | `$Jdk25 = 'C:\Users\chkev\...'` | 探测候选路径 + 支持 `$env:MACHA_JDK25` 覆盖 |
| **E** | 命名漂移：脚本/盘上是 `paper-server.jar`，文档写 `paper-26.2-123.jar` | 对比 `00` §C.1 / `04` §3.7 | 统一（推荐文档向脚本看齐：sha256 才是真正的锁） |
| **F** | 残留 `world_old/`、`.ready/.stop/.pid` 标记散落 | 服务器 home 目录 | 脚本收尾清理标记；`world_old` 加一行说明 |

> `layers/README.md` §验证 目前把**期望输出**写在"验证"标题下；M1 起请区分**期望**与**实测**（附时间与原始 JSON）。

---

## M1 · 能握手（+1–2 天）

**结果**：外部程序连上 Layer，发 `hello` 收到 `hello_ack`（含能力清单、世界名、`tick` 基准）。

### 步骤

1. 实现 `WebSocketDataPlane`（`kit/transport`）：启动 `WebSocketServer`（Java-WebSocket 1.6.0）→ 收到帧 →
   `JsonFraming.decode` → 交给回调；`send(envelope)` 广播给订阅会话
2. 装配：`MachaMinecraftPlugin.onEnable` 里启动 WS（与 HTTP 同端口或分端口，记录进 `config.yml`）
3. 握手：`hello` → 校验 `protocol.min/max` → 回 `hello_ack`（能力清单 = `PaperEnvironmentPort.declaredCapabilities`，
   世界名与 `tick` 基准取自真实服务器）
4. 补 HTTP `/action`（`01` §5 要求；可先只做单发动作，不含推送）

### 验收

- [ ] `./gradlew :testclient:run` 连上 → 打印 `hello_ack` JSON（含 `capabilities`、`environment`、`time`）
- [ ] 协议版本不匹配时，收到 `error(bad_version)` 并断开
- [ ] `curl -XPOST /action` 用未声明的动作名 → `action_result(status=refused, reason=not_supported)`
      （**M1 只验证"拒绝通道"能通，不要求动作真的执行**）

### 风险

- 端口冲突 / WS 与 HTTP 同端口升级失败 → 分端口，写进 `config.yml`
- 不要顺手做观测、事件、动作执行（那是 M2–M4）
