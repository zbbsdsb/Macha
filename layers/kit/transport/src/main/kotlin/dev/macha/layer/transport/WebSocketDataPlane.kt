package dev.macha.layer.transport

import dev.macha.layer.protocol.Envelope

/**
 * WebSocket 数据面（04 §3.3）：`ws://…/ws` 数据推送 + 往返。
 *
 * TODO(scaffold): 运行期 WS 服务器引导（`org.java-websocket` 的 WebSocketServer 子类）
 * 与 Java-WebSocket 1.6.0 的 API 对齐留待 vertical slice 阶段接线。
 * 当前骨架只固定"它能做什么"（发/收到的信封），以保持 `:transport` 零环境依赖、可编译。
 */
class WebSocketDataPlane(
    private val bind: String = "127.0.0.1",
    private val port: Int = 8765,
) {
    @Volatile
    private var running = false

    val isRunning: Boolean get() = running

    fun start() {
        // TODO: 启动 WebSocketServer；收到帧 → decode → 交给 onMessage 回调。
        running = true
    }

    fun stop() {
        running = false
    }

    /** 广播一条数据面消息。 */
    fun send(envelope: Envelope) {
        // TODO: 写入订阅该类型的所有会话（JsonFraming.encode）。
    }
}