# Observation 字段与最小事件集（v0）

> **STATUS: PENDING — 草案。** 配套 [`01-protocol-v0.md`](01-protocol-v0.md)。
> 目标：定义 Layer 能够读出的**最基础**世界信息，以及 Minecraft → Layer 的第一版事件管线。
> **不构建复杂 World Model**：这里只负责"把 Minecraft 中实际存在的信息读取出来"。

---

## 1. 选字段/选事件的三条判据

任何字段或事件进入 v0，必须同时满足：

| # | 判据 | 说明 |
|---|---|---|
| **J1** | **Paper 公开 API 可稳定获得** | 不碰 NMS、不解析包、不猜测内部结构 |
| **J2** | **携带完整 provenance** | 至少能回答 who / what / where / when（actor、target、position、world、tick） |
| **J3** | **第二个环境（Simulator Layer）也能产生同类** | **这是最重要的一条**：模拟器产生不了的东西，说明它是 Minecraft 特性而不是 Layer 抽象的一部分，放进协议就会污染边界 |

> J3 是"不要过度统一"与"不要被 Minecraft 绑架"之间的分界线：字段要保留 Minecraft 的真实信息
> （原则 ③ environment-aware），但**类别**必须是任何世界都有的。

---

## 2. Observation：观测窗口（Observation Window）

Observation 是**快照**，不是全知视图。窗口参数由 Runtime 请求 / Layer 配置决定：

| 参数 | 建议默认 | 作用 |
|---|---|---|
| `radius` | 16.0 | 只返回 agent 附近的实体（不是整个世界） |
| `max_entities` | 16 | 截断，超出时 `truncated: true` |
| `max_blocks` | 32 | 只返回**非空气**且在半径内的方块，按距离升序取前 N |
| `include_blocks` | true | 允许关闭以省带宽 |
| `push_interval` | 每 N tick 或按变化触发 | 见 §4 节流 |

**不返回**：整块区块数据、未加载区域、其他维度的信息、世界的"真相"（只返回这个 agent 的观察窗口）。

---

## 3. Observation 字段表

### 3.1 `agent`（自己）

| 字段 | 类型 | 必需 | 说明 |
|---|---|---|---|
| `id` | string | ✅ | Layer 内部 agent id（不使用 Minecraft UUID 作为主键） |
| `world` | string | ✅ | 命名空间世界名，如 `minecraft:overworld` |
| `position` | vec3 | ✅ | 世界坐标 |
| `rotation` | `{yaw, pitch}` | ✅ | 朝向 |
| `velocity` | vec3 | ⬜ | 可省；对"移动是否生效"有用 |
| `health` | number | ⬜ | 实体存在且有生命值时 |
| `alive` | boolean | ✅ | 存在性最直接的表征 |
| `extras` | object | ⬜ | Minecraft 特有补充（如 `gamemode`、`uuid`），**上层不得依赖** |

### 3.2 `nearby_entities[]`

`id` · `type`（命名空间字符串，如 `minecraft:player`）· `position` · `distance` · `alive` · `extras?`

### 3.3 `nearby_blocks[]`

`position`（整数格）· `type`（命名空间字符串，如 `minecraft:oak_log`）· `distance`

> 方块用**字符串 id** 而不是 Material 枚举名，是为了让 Simulator Layer 也能产生同样的字段
> （J3），同时不丢失 Minecraft 的真实材质信息。

### 3.4 `world`

`time_of_day`（0–24000，若环境有）· `day`（可选）· `extras?`（天气、难度等）

> 世界状态"读出来"即可，不做解释、不做推演。

### 3.5 `meta`

`tick` · `window{...}` · `truncated` · `sampled_at` · `verifiability`（`checked` / `trusted`）

---

## 4. 观测节奏与截断（v0 的务实策略）

| 情况 | 策略 |
|---|---|
| 默认 | 每 N tick 采样一次（N 可配置，建议 20 = 约 1 秒），或由 Runtime 用 `observation_request` 拉取 |
| 无变化 | 允许跳过推送（位置/健康/附近实体集合都没变） |
| 超限 | 按距离截断，置 `truncated: true`；**不静默丢弃而不标记** |
| 带宽 | v0 不做压缩、不做差分；先测出真实体积再优化 |

---

## 5. 事件最小集合（8 类）与选择理由

### 5.1 选定集合

| # | `kind` | 代表什么 | 为什么必须在这一版 |
|---|---|---|---|
| 1 | `minecraft:player_join` | 有人进入世界 | 世界**存在性**变化 + 会话边界；后续一切"谁在场"的前提 |
| 2 | `minecraft:player_quit` | 有人离开世界 | 与 join 成对；缺少它，上层会以为玩家永远在场（沉浸感失败模式） |
| 3 | `minecraft:entity_spawn` | 实体出现 | 世界在**无 agent 参与**时也会变化（"世界有自己的生活"的最小证据） |
| 4 | `minecraft:entity_despawn` | 实体消失（含原因） | 存在性变化的另一半；`data.reason` 只记事实，不解释 |
| 5 | `minecraft:entity_move` | 位置变化 | **vertical slice 的回环验证**；也是"玩家在移动"的唯一来源 |
| 6 | `minecraft:entity_damage` | 伤害事件（actor → target） | 第一个**有方向的状态改变**（关系认知的最小原料）；字段只放事实 |
| 7 | `minecraft:block_break` | 方块被破坏 | 世界**突变** + 明确的 actor/position；最能检验 environment-aware 字段设计 |
| 8 | `minecraft:block_place` | 方块被放置 | 与 break 成对；玩家对世界的写入 |

再加上**交互事件**（与上表并列的必选一类，因语义不同单列）：

| 9 | `minecraft:interaction` | 玩家右键实体/方块 | 代表**意图事件**（不是结果事件）；与 damage 区分开 |

> 计数说明：核心 8 类 + `interaction` = 9；若按"存在性 / 状态变化 / 世界突变 / 意图"四族归类，
> 则是 4 族 9 类。**第一版不必全部实现**，但实现顺序建议 = 上表顺序（1→9），因为 5/7/9 是
> vertical slice 必需的，1/2 最便宜，6 为后续关系认知铺路。

### 5.2 四族覆盖（为什么这 9 类"够代表性"）

```text
存在性   player_join / player_quit / entity_spawn / entity_despawn
状态变化 entity_move / entity_damage
世界突变 block_break / block_place
意图     interaction
```

四族分别对应 Core 未来需要的四类输入：**谁在 / 谁变了 / 世界被改成什么样 / 谁想干什么**。
缺少任意一族，Core 都会在某一类推理上瞎猜。

### 5.3 暂不纳入（及理由）

| 不纳入 | 理由 |
|---|---|
| 聊天 / 说话 | 涉及社会语义与隐私；且**极易诱导 Layer 做语义解释**（红线 G.1-4）。等 Core 需要时再以独立消息引入 |
| 物品栏 / 合成 / 容器 | 属于"世界内部的复杂状态"，v0 用不到；纳入会立刻把 World Model 拉进来 |
| 红石 / 爆炸 / 天气变化 | 有价值但非最小集；等 M4 能力清单稳定后按需扩展 |
| 实体朝向变化、动画、音效 | 属于表现层，不构成世界状态变化 |
| 死亡本身 | 用 `entity_despawn` + `data.reason="death"` 表达，不新增类型（避免事件爆炸） |

---

## 6. 事件字段通用形状

```json
{
  "kind": "minecraft:entity_damage",
  "actor":  { "id": "player:steve", "type": "minecraft:player" },
  "target": { "id": "agent_001",    "type": "minecraft:zombie" },
  "position": [12.5, 64.0, -3.2],
  "world": "minecraft:overworld",
  "tick": 148230,
  "data": { "amount": 3.0, "source": "minecraft:player_attack" },
  "verifiability": "checked"
}
```

- `actor` / `target` 可为 `null`（例如自然生成 → 无 actor）；
- `data` 是**不透明**的：环境特有信息放这里，上层不得依赖内部结构才能工作；
- **禁止**在事件里放：情绪、关系、意图推断、善恶判断（"他偷了我的木头，所以我不信任他"
  属 Core 的 appraisal）。

---

## 7. 事件与 Observation 的分工

| | Observation | Event |
|---|---|---|
| 性质 | **快照**（现在是什么样） | **事实流**（发生了什么） |
| 起点 | 主动采样 / 定时 / 请求 | Paper 事件回调（主线程） |
| 视角 | **agent 的观察窗口** | **世界视角**（事件本身没有视角，是事实） |
| 归 Core 做什么 | 赋义、记住、决定 | 赋义、记住、决定 |

正因为 Event 是世界视角、Observation 是 agent 视角，二者**不能互相替代**：
Observation 回答"我能看到什么"，Event 回答"世界发生了什么（即使我没看到）"。
这个区分正是 `npc-world-boundary.md` 里"半透膜"的工程体现。

---

## 8. 待回答

1. `entity_move` 的触发方式：每 tick 都发会刷屏，按"距离阈值 + 节流窗口"还是按"每 N tick 采样"？
2. `nearby_blocks` 是否需要"只返回与上次相比发生变化的方块"（差分）？v0 建议先不做。
3. `player_join/quit` 是否需要携带玩家列表快照（避免上层自己做集合维护）？
4. 事件是否需要在 Layer 侧落盘（可回放 transcript M9）？v0 建议：写到本地 NDJSON 文件，供测试回放。
