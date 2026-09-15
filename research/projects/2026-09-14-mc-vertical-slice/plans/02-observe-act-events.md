# 计划二：观测 · 动作 · 事件（M2–M4）

> 里程碑定义见 [`../../../plans/minecraft-layer/06-next-step-plan.md`](../../../plans/minecraft-layer/06-next-step-plan.md) §2。
> 预估：**M2 +1 天；M3 +1–2 天；M4 +1 天。** 依赖：计划一（握手通了）。
> 三件事**可并行**，但共用一条纪律：**Bukkit API 只在主线程**（`03` §6）。

---

## M2 · 能看见（observation）

**结果**：外部程序拿到 agent 视角快照，与游戏内一致。

### 步骤

1. `adapter/observe/PaperObservationCollector`（主线程采集 → 纯 DTO）：
   `agent{id, world, position, rotation, velocity?, health, alive}` +
   `nearby_entities[]`（`id/type/position/distance/alive`）+ `nearby_blocks[]`（`position/type/distance`，
   仅非空气）+ `world{time_of_day, day?}` + `meta{tick, window, truncated}`
2. `NearbyEntityScanner` / `NearbyBlockScanner`：按 `config.yml` 的 `radius` / `max_entities` / `max_blocks`
   **按距离升序截断**，超限置 `truncated: true`（**不得静默丢弃**）
3. `AgentRegistry`：agent id ↔ 实体绑定（主键用内部 id，Minecraft UUID 放 `extras`）
4. `ObservationScheduler`：按 `push_interval_ticks` 推送；**无变化可跳过**

### 验收

- [ ] `position` 与游戏内 `/tp` 对照 **±0.1**
- [ ] 30 秒内收到至少 1 条 push 的 `observation`，含 `tick`
- [ ] 站到 30 格外 → 实体列表为空且 `truncated` 语义正确（不是报错）

---

## M3 · 能动手（move / look + refused）

**结果**：外部指令真的改变世界；不可执行的动作被**拒绝而不是静默失败**。

### 步骤

1. `adapter/action/ActionExecutor`：网络线程收到 → `runTask` 回**主线程** → 执行 → 结果写回结构 → 网络线程回传
2. `ActionMapping`：通用词 → Paper 操作的唯一映射点（`move` → 走向目标；`look` → 设置朝向）
3. `refused` 分支：能力未声明 → `not_supported`；目标超出世界/加载范围 → `out_of_range`；
   前置条件不满足（区块未加载）→ `precondition_failed`
4. `spawn_agent`：生成被测实体（**armor stand 或 `setAI(false)` 的僵尸**，见 §风险）

### 验收

- [ ] 发 `move` → `action_result(ok)`，且游戏内实体真的位移
- [ ] 发超范围目标 → `action_result(refused, reason=out_of_range)`
- [ ] 未声明的动作名 → `refused(not_supported)`（与 M1 同一通道）
- [ ] 全程无异步改世界的调用（review 逐条对照 `03` §6）

---

## M4 · 能听见世界（事件）

**结果**：玩家的动作变成事件流。

### 步骤

1. `adapter/events/PaperEventBridge`：主线程监听 → **只做归一化 + 入队**（禁止 IO / 序列化 / 网络发送）
2. 先实现三类（`02` §5 的最小族：状态变化 / 世界突变 / 意图）：
   `entity_move` · `block_break` · `interaction`
3. `EventThrottle`：`entity_move` 按距离阈值 + 节流窗口合并，避免刷屏
4. `kind` 用命名空间（`minecraft:*`），`data` 不透明，附 `verifiability`

### 验收

- [ ] 玩家走一段 → 收到 `entity_move`（含 actor/position/world/tick）
- [ ] 玩家拆一个方块 → 收到 `block_break`（含 actor/target.position）
- [ ] 玩家右键实体 → 收到 `interaction`
- [ ] 连续快速移动 10 秒，事件条数 **明显少于** tick 数（节流生效）

---

## 风险

| 风险 | 处置 |
|---|---|
| 僵尸自身 AI 乱走，污染后续演示 | **M3 生成实体时就用 armor stand / `setAI(false)`**，不要等 M5 才改 |
| 事件在主线程里做 IO → 卡 tick | 监听器内只归一化 + 入队；发送在网络线程 |
| observation 里混入"解释"（谁是敌人） | 红线：只放事实。发现即回退（V3） |
| 截断未标记 → 上层以为世界很小 | `truncated` 必须真实反映是否被截断 |
