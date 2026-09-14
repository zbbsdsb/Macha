package dev.macha.layer.protocol

import kotlinx.serialization.SerialName
import kotlinx.serialization.Serializable
import kotlinx.serialization.json.JsonElement
import kotlinx.serialization.json.JsonObject

/**
 * 所有消息共用信封（01 §2）。
 *
 * 边界约束（红线 G.1-2）：世界时间 tick / 世界时间绝不进信封顶层，必须放进 `payload`。
 * `axios` 不承担世界时间语义，只是发送方本地 wall clock（毫秒）。
 */
@Serializable
data class Envelope(
    @SerialName("v") val version: String,
    val type: String,
    val id: String? = null,
    val ts: Long,
    val payload: JsonElement = JsonObject(emptyMap()),
)