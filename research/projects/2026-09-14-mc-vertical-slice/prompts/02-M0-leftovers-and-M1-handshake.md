# 提示词：M0 遗留修正（A–F）+ M1 握手

> 用途：整段粘给本地 agent。**分两部分，中间必须停下来贴证据**；Part 1 不通过，不要开始 Part 2。
> 上下文：[`../README.md`](../README.md) ｜ [`../plans/01-server-and-handshake.md`](../plans/01-server-and-handshake.md)（§M0 遗留修正）｜
> [`../../../plans/minecraft-layer/01-protocol-v0.md`](../../../plans/minecraft-layer/01-protocol-v0.md)（§3.2 / §5 / §9）

```text
# 任务：先修 M0 遗留 A–F，再做 M1（WS 握手）

## 硬边界（违反即失败）
1. 不改 src/macha/**；不改协议字段名/语义（要改先在 research/plans/minecraft-layer/01-protocol-v0.md §9 登记，再改代码）。
2. 不实现观测 / 事件 / 动作执行 / Stub Core（那些是 M2–M5）。
3. 不加依赖（Java-WebSocket 已在 :kit:transport 与 :testclient 里）。
4. 不提交 layers/run/**、eula.txt、server.properties、paper-*.jar。

## Part 1 — M0 遗留修正（做完停下，贴证据，等我确认再进 Part 2）

### A 能力清单被削平（最重要）
现状：GET /capabilities 返回 `[{"name":"move","args":{},"expected_effect":"position change"},{"name":"look","args":{},"expected_effect":""} …]`
—— args 恒为空，preconditions/verifiability/cost 全丢；根因是 MachaMinecraftPlugin.capabilityManifestJson() 手写 JSON 拼接。
要求：
1) 用已存在的 kotlinx 序列化（ProtocolV0.json）序列化 List<Capability>，禁止手写 JSON；
2) 把 declaredCapabilities() 抽成一个**不 import Paper** 的对象（如 CapabilityCatalog），便于测试；
3) 在 :kit:protocol 加往返测试：Capability(含 args/preconditions/verifiability/cost) → JSON → 对象，字段不丢；
4) 验收：curl http://127.0.0.1:8765/capabilities 的原始 JSON 里，4 条能力每条都带 args（move: target=vec3；
   look: yaw/pitch；interact: target=entity|block；spawn_agent: type/position）与 verifiability。
   （若 :minecraft 的 test classpath 拿不到 paper-api，就不要硬凑 minecraft 侧单测——以实测 JSON 为验收。）

### B 托管停服是强杀
现状：console.log 里没有 `Stopping server` / `Saving players`，靠 Stop-Process -Force。
要求（二选一，优先 1）：
1) 用 RCON 停服：server.properties 开 enable-rcon=true + rcon.password + rcon.port，managed 模式在收到 .stop
   后用 RCON 发 `stop`；
2) 若 30 分钟内做不完：停服前**自动备份 world**（复制到 world.bak-<时间戳>），并在 layers/README.md
   写明"强杀风险 + 恢复方式"。
验收：贴出 console.log 里出现 `Stopping server` 与 `Saving players` 的原始行（或备份目录清单 + README 段落）。

### C server.properties 每次被重写
要求：只在该文件**不存在**时写入；已存在则原样保留（必要时只做"补缺失键"，不要覆盖已有值）；
若要强制重置，加开关 -ResetConfig。
验收：手工改一个键（如 difficulty=hard）→ 再起服 → 该键仍在。

### D JDK 25 路径硬编码
要求：解析顺序 = $env:MACHA_JDK25 → 探测 "$env:USERPROFILE\.gradle\jdks\*\bin\java.exe" 中版本含 25 的 →
探测常见安装目录；都找不到时抛出**带操作指引**的错误。禁止出现具体用户名。
验收：在脚本里 grep 不到 "C:\Users\<名>"；并贴出解析到的 java -version 输出。

### E 文档命名漂移
脚本与盘上用 paper-server.jar，而 00 §C.1 / 04 §3.7 写 paper-26.2-123.jar。
要求：以脚本为准，改文档（说明 sha256 才是真正的锁），不要改脚本文件名。

### F 收尾清理
要求：managed 模式退出时删除 .ready/.stop/.pid；为 world_old/ 加一行说明（layers/README.md）。

### 另外
layers/README.md 的"验证"一节要把**期望输出**与**实测（附时间 + 原始 JSON）**分开写。

## Part 2 — M1：能握手（Part 1 验收通过后再做）

1) 实现 :kit:transport 的 WebSocketDataPlane：用 Java-WebSocket 1.6.0 起 WebSocketServer（绑定与端口取 config.yml），
   收到帧 → JsonFraming.decode → 交给 onMessage 回调；send(envelope) 广播给订阅会话。
2) 装配进 MachaMinecraftPlugin.onEnable（与 HTTP 同端口或 config 指定分端口；记录实际端口）。
3) 握手：`hello`（含 protocol.min/max）→ 校验 → 回 `hello_ack`：
   - protocol = "0"
   - capabilities = **Part 1 修好的**完整清单
   - environment = { minecraft: "26.2", paper: "26.2-123", worlds: [...] }
   - time = { tick: <真实服务器 tick>, world_time: <真实值>, unit: "tick" }
   - agents = []（M2 才有绑定）
   版本无交集 → 回 `error(bad_version)` 并断开。
4) 补 HTTP `POST /action`（01 §5）：未声明动作名 → action_result(status=refused, reason=not_supported)；
   不要求真的执行动作（M3 才做）。
5) testclient 的 VerticalSliceProbe：连 WS → 发 hello → 打印收到的 hello_ack 全文（JSON 原样）

### M1 验收（逐条贴原始输出）
- [ ] ./gradlew :testclient:run 打印 hello_ack 全文，4 条能力各带 args 与 verifiability
- [ ] 故意发 protocol.max="999" → 收到 {"type":"error","payload":{"code":"bad_version",…}} 并断开
- [ ] curl -X POST -d '{"type":"action","payload":{"action":"fly_to_moon"}}' /action
      → {"status":"refused","reason":"not_supported"}
- [ ] ./gradlew check 通过（含三个边界守护任务）
- [ ] git status --porcelain --untracked-files=all -- layers/run 为空

## 汇报格式
Part 1：A–F 逐条 = 改动文件 + 验收命令 + 原始输出摘要（A 必须贴 /capabilities 全文）
Part 2：四条验收逐条贴原始输出；未做/不确定项与原因
```

---

## 执行完之后能看到什么

**立刻能看到的（Part 1）**

| 之前 | 之后 |
|---|---|
| `/capabilities` 里 `args` 全空、字段丢失 | 4 条能力各带 `args` / `preconditions` / `verifiability` / `cost`——**边界上第一份无损清单** |
| 停服是强杀，日志没有 `Stopping server` | 优雅停服（或至少自动备份 world + 风险写明） |
| 手工改的 `server.properties` 下次被抹掉 | 改动保留 |
| 脚本写死 `C:\Users\chkev\...` | 换台机器也能起服（自动定位 JDK 25） |
| README 把"期望"当"验证" | 期望 / 实测分开写 |

**M1 完成后能看到的**

- 你能**自己敲一条命令**连上 Layer 并拿到 `hello_ack` 全文：协议版本、世界名、真实 `tick`、4 条完整能力；
- 故意报一个不存在的协议版本 → 服务器回 `error(bad_version)` 并断开；
- `POST /action` 发一个没声明的动作 → `refused(not_supported)`——**"拒绝通道"第一次真的通了**。

**这时你还看不到的**

NPC 不会动、没有任何"它在回应我"。要看到那种效果还需要：M2 观测 → M3 动作 → M4 事件 → **M5 Stub Core**（`tools/stub-core/`，目前还没建）。

所以这个提示词的效果是：**边界活了，NPC 还没活。** 预计 Part 1 半天、Part 2 1–2 天。
