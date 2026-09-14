package dev.macha.layer.transport

/** 连接状态（04 §3.3）。 */
sealed interface ConnectionState {
    object Disconnected : ConnectionState
    object Connected : ConnectionState

    /** 心跳/关闭原因。 */
    data class Closed(val reason: String) : ConnectionState
}

/** 连接：状态、心跳、关闭原因。 */
class Connection {
    private var state: ConnectionState = ConnectionState.Disconnected

    val current: ConnectionState get() = state

    fun markConnected() {
        state = ConnectionState.Connected
    }

    fun close(reason: String) {
        state = ConnectionState.Closed(reason)
    }

    val isOpen: Boolean get() = state == ConnectionState.Connected
}