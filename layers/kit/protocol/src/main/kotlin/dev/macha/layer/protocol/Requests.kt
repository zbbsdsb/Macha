package dev.macha.layer.protocol

import kotlinx.serialization.Serializable

/** observation_request：Runtime 主动拉取一次观察（01 §3 配套请求）。 */
@Serializable
data class ObservationRequest(
    val agentId: String? = null,
    val window: ObservationWindow? = null,
)

/** event_subscribe：Runtime 选择订阅全部或按 kind 列表（01 §3 配套请求）。 */
@Serializable
data class EventSubscribe(
    val kinds: List<String> = listOf("all"),
)