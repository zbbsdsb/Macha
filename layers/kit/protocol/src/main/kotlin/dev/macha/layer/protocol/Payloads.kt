package dev.macha.layer.protocol

import kotlinx.serialization.Serializable
import kotlinx.serialization.json.JsonElement

/**
 * v0 消息的负载结构（01 §3、02 §3）。
 *
 * 坐标约定：所有坐标均为世界坐标浮点 `vec3 = [x, y, z]`（01 §4）。
 * 事件与字段只用**事实**，不放情绪/关系/意图（红线 G.1-4）。
 */
typealias Vec3 = List<Double>

@Serializable
data class Rotation(val yaw: Double, val pitch: Double)

/** 自身视角（02 §3.1）。id 用 Layer 内部主键；UUID 等进 extras，上层不得依赖。 */
@Serializable
data class AgentView(
    val id: String,
    val world: String,
    val position: Vec3,
    val rotation: Rotation = Rotation(0.0, 0.0),
    val velocity: Vec3? = null,
    val health: Double? = null,
    val alive: Boolean = true,
    val extras: Map<String, JsonElement> = emptyMap(),
)

/** 周围实体（02 §3.2）。type 用命名空间字符串，如 `minecraft:player`。 */
@Serializable
data class EntityView(
    val id: String,
    val type: String,
    val position: Vec3,
    val distance: Double? = null,
    val alive: Boolean = true,
    val extras: Map<String, JsonElement> = emptyMap(),
)

/** 周围方块（02 §3.3）。位置用整数格；type 用命名空间字符串（不暴露 Material 枚举名）。 */
@Serializable
data class BlockView(
    val position: Vec3,
    val type: String,
    val distance: Double? = null,
)

/** 世界信息（02 §3.4）：只读、不解释、不推演。 */
@Serializable
data class WorldView(
    val timeOfDay: Int? = null,
    val day: Int? = null,
    val extras: Map<String, JsonElement> = emptyMap(),
)

/** 观测窗口参数（02 §2）。 */
@Serializable
data class ObservationWindow(
    val radius: Double = 16.0,
    val maxEntities: Int = 16,
    val maxBlocks: Int = 32,
    val includeBlocks: Boolean = true,
)

/** 观测元信息（02 §3.5）。 */
@Serializable
data class ObservationMeta(
    val tick: Long,
    val window: ObservationWindow,
    val truncated: Boolean = false,
    val sampledAt: Long? = null,
    val verifiability: String = "checked",
)

/** observation 负载（01 §3.3）。 */
@Serializable
data class ObservationPayload(
    val agent: AgentView,
    val nearbyEntities: List<EntityView> = emptyList(),
    val nearbyBlocks: List<BlockView> = emptyList(),
    val world: WorldView? = null,
    val meta: ObservationMeta,
)

/** 事件引用的实体（02 §6）。actor/target 可为 null（如自然生成→无 actor）。 */
@Serializable
data class ActorRef(
    val id: String,
    val type: String? = null,
    val position: Vec3? = null,
)

/** event 负载（01 §3.4）：kind 用命名空间；data 不透明；无解释。 */
@Serializable
data class EventPayload(
    val kind: String,
    val actor: ActorRef? = null,
    val target: ActorRef? = null,
    val position: Vec3? = null,
    val world: String? = null,
    val tick: Long? = null,
    val data: Map<String, JsonElement> = emptyMap(),
    val verifiability: String = "checked",
)

/** provenance：只记录谁决定的，可审计；Layer 无需理解 reason 含义（01 §3.5）。 */
@Serializable
data class Provenance(
    val decidedBy: String,
    val reason: String? = null,
)

/** action 负载（01 §3.5）。args 为不透明 JSON——不同动词参数形状不同。 */
@Serializable
data class ActionPayload(
    val agent: String,
    val action: String,
    val args: Map<String, JsonElement> = emptyMap(),
    val provenance: Provenance? = null,
)

/** action_result 负载（01 §3.6）。 */
@Serializable
data class ActionResultPayload(
    val status: String,
    val reason: String? = null,
    val detail: String? = null,
    val delta: Map<String, JsonElement>? = null,
    val verifiability: String = "checked",
)

/** error 负载（01 §3.7）。 */
@Serializable
data class ErrorPayload(
    val code: String,
    val message: String,
    val where: String? = null,
)

// ---- hello / hello_ack（01 §3.1 / §3.2）----

@Serializable
data class RuntimeRef(val name: String, val version: String, val lang: String? = null)

@Serializable
data class ProtocolRange(val min: String, val max: String)

@Serializable
data class HelloPayload(
    val runtime: RuntimeRef,
    val protocol: ProtocolRange,
    val subscribe: List<String> = listOf("all"),
)

@Serializable
data class LayerRef(val name: String, val version: String)

@Serializable
data class EnvironmentInfo(
    val kind: String,
    val versions: Map<String, String> = emptyMap(),
    val worlds: List<String> = emptyList(),
)

@Serializable
data class WorldTimeRef(
    val tick: Long? = null,
    val worldTime: Long? = null,
    val unit: String? = null,
)

@Serializable
data class AgentRef(val id: String, val entity: String? = null, val bound: Boolean = true)

@Serializable
data class HelloAckPayload(
    val layer: LayerRef,
    val protocol: String,
    val environment: EnvironmentInfo? = null,
    val time: WorldTimeRef? = null,
    val capabilities: List<Capability> = emptyList(),
    val agents: List<AgentRef> = emptyList(),
)