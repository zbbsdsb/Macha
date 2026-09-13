# Macha ↔ Environment Protocol — v0（草案）

> **STATUS: PENDING — 协议 v0 草案。这是 Layer 与 Macha Runtime 之间的最小连接协议，不是最终协议。**
>
> 适用范围：`macha-minecraft` 与 Macha Runtime 之间。**不修改 Macha Core**；本文件只定义边界上的
> 消息形状。上游依据：`docs/architecture.md` §3（五类交换）、
> `papers/notes/accepted/decision-layer-first-sequencing.md`（C2 跨语言传输）。
> 本阶段**不设计完整 Macha Protocol**，只建立能验证连接的最小 message types。

---

## 1. 四条设计原则（可检验）

| 原则 | 含义 | 违反时的信号 |
|---|---|---|
| **① Transport independent** | 协议是**消息语义**，不是 WebSocket 的形状。未来换 HTTP / gRPC / IPC / MQ，语义不变 | 出现"因为是 WS 所以字段长这样"的设计；消息里含连接对象 |
| **② Runtime independent** | 不假设 Runtime 是 Python / Rust / TS；不假设同进程、不假设共享类型 | 出现进程内对象引用、序列化 Java 对象、依赖 GC/线程模型 |
| **③ Environment-aware** | 不把 Minecraft 语义抹平。保留真实世界信息（位置/材质/实体/维度/世界时间），并允许环境特有扩展 | 上层拿不到真实世界信息；协议被压成 `move/talk/attack` |
| **④ Minimal** | 现在宁愿少：6 种消息、4 个动作、8 类事件 | 为"以后可能需要"预先加字段 |

**命名空间规则（同时服务于 ② 与 ③）**

```text
不带命名空间的动词 = 共同能力类   move · look · interact · spawn_agent
带命名空间的动词   = 环境特有       minecraft:place_block · minecraft:craft
```

这条规则是**可自动检查的**：Core 侧词表只允许无前缀动词；Minecraft 动词必须带前缀。
（与决策记录约束 C3 一致。）

---

## 2. 信封（Envelope）

所有消息共用同一信封：

```json
{
  "v": "0",
  "type": "observation",
  "id": "req-7f3a",
  "ts": 1789000000123,
  "payload": { }
}
```

| 字段 | 类型 | 必需 | 说明 |
|---|---|---|---|
| `v` | string | ✅ | 协议版本，v0 固定 `"0"` |
| `type` | string | ✅ | 消息类型（见 §3） |
| `id` | string | 条件 | 请求/响应对的关联 id；事件与推送型 observation 用 `null` 或省略 |
| `ts` | integer | ✅ | 发送方本地毫秒时间戳（**wall clock，不承担世界时间语义**） |
| `payload` | object | ✅ | 类型相关字段 |

**世界时间不进信封**：tick / 世界时间属于环境信息，放在 `payload` 里，避免把 Minecraft 的时间
语义提到协议顶层（红线 G.1-2）。

---

## 3. 消息类型 v0

| # | type | 方向 | 回答的问题 |
|---|---|---|---|
| 1 | `hello` | Runtime → Layer | 我是谁、我要什么版本 |
| 2 | `hello_ack` | Layer → Runtime | 我在哪个世界、我**实际**能做什么 |
| 3 | `observation` | Layer → Runtime（可 push，也可作 `observation_request` 的响应） | 此刻这个 agent 能感知到什么 |
| 4 | `event` | Layer → Runtime（流式） | 环境里发生了什么 |
| 5 | `action` | Runtime → Layer | 我想做什么 |
| 6 | `action_result` | Layer → Runtime | 世界对这件事的答复（含拒绝） |
| 7 | `error` | 双向 | 协议级错误 |

配套的**请求类**消息（v0 允许，但不属于"7 类"核心）：
`observation_request`（Runtime → Layer）、`event_subscribe`（Runtime → Layer）。
`ping` / `pong` 若实现，属 transport 层，不进协议语义。

### 3.1 `hello`

```json
{ "v":"0","type":"hello","id":"c1","ts":1789000000000,
  "payload": {
    "runtime": { "name": "macha-runtime", "version": "0.0.1", "lang": "python" },
    "protocol": { "min": "0", "max": "0" },
    "subscribe": ["all"]
  } }
```

### 3.2 `hello_ack`

```json
{ "v":"0","type":"hello_ack","id":"c1","ts":1789000000100,
  "payload": {
    "layer": { "name": "macha-minecraft", "version": "0.1.0" },
    "protocol": "0",
    "environment": {
      "kind": "minecraft",
      "versions": { "minecraft": "26.2", "paper": "26.2-123" },
      "worlds": ["minecraft:overworld"]
    },
    "time": { "tick": 148213, "world_time": 6000, "unit": "tick" },
    "capabilities": [
      { "name": "move",     "args": {"target":"vec3"}, "preconditions":["chunk_loaded","reachable"],
        "expected_effect":"position change", "verifiability":"checked", "cost":"cheap" },
      { "name": "look",     "args": {"yaw":"number","pitch":"number"}, "verifiability":"checked", "cost":"cheap" },
      { "name": "interact", "args": {"target":"entity|block"}, "preconditions":["in_range"],
        "expected_effect":"interaction", "verifiability":"trusted", "cost":"cheap" },
      { "name": "spawn_agent", "args": {"type":"string","position":"vec3"},
        "expected_effect":"entity exists", "verifiability":"checked", "cost":"moderate" }
    ],
    "agents": [ { "id": "agent_001", "entity": "minecraft:zombie", "bound": true } ]
  } }
```

`capabilities` 是**探测结果**，不是愿望清单：Layer 只能声明自己实测能执行的动作。
`verifiability`：`checked` = 结果可对着真实状态验证；`trusted` = 只能采信环境回报（供未来
Guardrail 决定确定性校验还是概率自洽）。

### 3.3 `observation`

```json
{ "v":"0","type":"observation","id":null,"ts":1789000002000,
  "payload": {
    "agent": { "id":"agent_001", "world":"minecraft:overworld",
               "position":[12.5,64.0,-3.2], "rotation":{"yaw":90.0,"pitch":0.0},
               "velocity":[0.0,0.0,0.0], "health":20.0, "alive":true },
    "nearby_entities": [
      { "id":"player:steve", "type":"minecraft:player", "position":[14.5,64.0,-3.0],
        "distance":2.06, "alive":true } ],
    "nearby_blocks": [
      { "position":[13,63,-3], "type":"minecraft:oak_log", "distance":1.4 } ],
    "world": { "time_of_day":6000, "day":3 },
    "meta": { "tick":148213, "window":{"radius":16,"max_entities":16,"max_blocks":32},
              "truncated":false, "verifiability":"checked" }
  } }
```

字段清单与取舍理由见 [`02-observation-and-events.md`](02-observation-and-events.md)。

### 3.4 `event`

```json
{ "v":"0","type":"event","id":null,"ts":1789000002500,
  "payload": {
    "kind": "minecraft:block_break",
    "actor": { "id":"player:steve", "type":"minecraft:player" },
    "target": { "position":[13,63,-3], "type":"minecraft:oak_log" },
    "world": "minecraft:overworld",
    "tick": 148230,
    "data": { "tool": "minecraft:iron_axe" },
    "verifiability": "checked"
  } }
```

`kind` 用命名空间；`data` 是不透明 JSON（环境特有信息可以放，但上层**不得**依赖其内部结构才能工作）。
事件**不含解释**：没有情绪、没有关系、没有"为什么"——那是 Core 的 appraisal。

### 3.5 `action`

```json
{ "v":"0","type":"action","id":"act-9","ts":1789000003000,
  "payload": {
    "agent": "agent_001",
    "action": "move",
    "args": { "target": [20.0, 64.0, -3.0] },
    "provenance": { "decided_by": "stub-core", "reason": "follow-player" }
  } }
```

`provenance` 只记录**谁决定的**（可审计），不要求 Layer 理解 `reason` 的含义。

### 3.6 `action_result`

```json
{ "v":"0","type":"action_result","id":"act-9","ts":1789000003400,
  "payload": {
    "status": "ok",
    "reason": null,
    "detail": null,
    "delta": { "position": { "from":[12.5,64.0,-3.2], "to":[20.0,64.0,-3.0] } },
    "verifiability": "checked"
  } }
```

| `status` | 含义 | `reason` |
|---|---|---|
| `ok` | 环境执行了 | — |
| `refused` | 环境**做不到/不允许**（能力不存在、前置条件不满足、超出写权限） | `not_supported` / `precondition_failed` / `out_of_range` / `no_permission` |
| `failed` | 尝试了但没成功（世界规则拒绝、目标消失） | `target_missing` / `blocked` / `internal` |
| `pending`（可选） | 已接受、尚未完成 | — |

**`refused` 是正常结果，不是错误**：Core 必须能接收"不"并改选意图（`architecture.md` §4）。
`delta` 只描述**可核验的状态变化**，不做解释。

### 3.7 `error`

```json
{ "v":"0","type":"error","id":"act-9","ts":1789000003500,
  "payload": { "code":"schema_violation", "message":"args.target must be vec3",
               "where":"action" } }
```

错误码最小集：`bad_version` · `unknown_type` · `schema_violation` · `unauthorized` · `internal`。

---

## 4. 动作词表 v0（只有 4 个）

| 动作 | 参数 | 备注 |
|---|---|---|
| `move` | `target: vec3` | 移动请求；**不承诺路径与时序**（导航复杂度不在 v0） |
| `look` | `yaw: number`, `pitch: number`，或 `target: entity` | 朝向 |
| `interact` | `target: {id}` 或 `{position}` | 交互（右键语义） |
| `spawn_agent` | `type: string`, `position: vec3` | 生成被测实体；仅用于建立 vertical slice |

**明确排除**：`place_block` / `break_block` / `craft` / `attack` / `use` / `create` / `destroy`。
它们属于 Minecraft 环境特有扩展，格式为 `minecraft:<verb>`，**不进 v0 核心词表**——先证明边界，
再扩能力。扩展的登记规则见 §6。

参数形状约定：`vec3 = [x, y, z]`（number）；所有坐标为**世界坐标浮点**；
`target` 用 `{id}` 或 `{position}`，不用环境内部句柄。

---

## 5. 传输绑定（绑定在 transport，不在协议）

本阶段建议形态（可在不改协议语义的前提下替换）：

| 通道 | 用途 | 端点（建议） |
|---|---|---|
| **HTTP** | 控制面：健康检查、协议版本、能力清单、单发动作（便于测试与非流式客户端） | `GET /healthz` · `GET /capabilities` · `POST /action` |
| **WebSocket** | 数据面：`event` 与 `observation` 推送、`action`/`action_result` 往返、`hello`/`hello_ack` | `ws://127.0.0.1:8765/ws` |

同一路 JSON 在两个通道上语义一致；`hello` 也可在 HTTP 上完成（无状态客户端）。
绑定地址默认 `127.0.0.1`（不外网暴露）。

**与 MCP 的关系**：v0 只**借形状**（JSON-RPC 风格、`tools/call` 式的动作调用），不追求 MCP 兼容。
`docs/research/standards_interop.md` §188 主张 `ActionCall` 收敛到 Tool-Use 形状——本草案与该方向
一致，但**现在不实现 MCP**。

---

## 6. 版本与演进

- `v` 字段即协议版本；`hello` 协商 `min`/`max`，无交集则 `error(bad_version)` 并断开。
- **字段只增不改**（v0 内）；删除或改语义 = 升 `v`。
- 环境特有扩展通过命名空间登记：`<namespace>:<verb>`，且必须出现在该 Layer 的 `capabilities` 中；
  未声明的动作一律 `refused(not_supported)`。
- 协议版本与 Minecraft/Paper 版本**解耦**：MC 升级由 Layer 内部适配，`v` 不变。

---

## 7. 明确不在 v0 内（防止过度设计）

- 世界模型 / 地图 / chunk 数据；记忆、人格、目标、规划相关字段；
- 多 agent 协商、社会结构、组织涌现；
- 流控与背压的完整方案（v0 只用节流 + 丢弃策略）；
- 鉴权与多租户（v0 仅本地回环 + 可选 token）；
- 时间同步协议（v0 只传 `tick` 作参考值）。

---

## 8. 待回答（写代码前需定）

1. `State` 是否作为**独立消息**？本草案的处理：状态通过 `observation`（agent 视角）暴露，
   **不设独立 State 消息**，直到出现"必须查询 agent 视角之外的世界状态"的真实需求。
2. `observation` 默认 push 频率与节流策略（按 tick？按变化？按请求？）。
3. `event_subscribe` 是否进 v0（见 `00-technical-foundation.md` §H-D7）。
4. `pending` 状态是否需要（真实动作有耗时，但 v0 可能用同步返回 + 超时即可）。
5. `agent` 标识用 Layer 内部 id，还是暴露 Minecraft 的 UUID？（建议：内部 id 为主，UUID 放 `extras`）

---

*v0 — PENDING。示意字段可能在实际实现时调整；调整须回写本文件，不得只改代码。*
