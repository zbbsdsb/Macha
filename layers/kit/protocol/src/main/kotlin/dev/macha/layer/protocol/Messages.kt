package dev.macha.layer.protocol

/**
 * 消息类型（01 §3）：7 类核心 + 2 类配套请求。
 * `ping`/`pong` 属 transport 层，不在此列。
 */
object MessageTypes {
    const val HELLO = "hello"
    const val HELLO_ACK = "hello_ack"
    const val OBSERVATION = "observation"
    const val EVENT = "event"
    const val ACTION = "action"
    const val ACTION_RESULT = "action_result"
    const val ERROR = "error"

    // 配套请求（v0 允许，但不属于 7 类核心）
    const val OBSERVATION_REQUEST = "observation_request"
    const val EVENT_SUBSCRIBE = "event_subscribe"

    val CORE: Set<String> = setOf(HELLO, HELLO_ACK, OBSERVATION, EVENT, ACTION, ACTION_RESULT, ERROR)

    fun isCore(type: String): Boolean = type in CORE
}