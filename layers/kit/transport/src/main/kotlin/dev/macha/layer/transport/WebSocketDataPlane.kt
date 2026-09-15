package dev.macha.layer.transport

import dev.macha.layer.protocol.Envelope
import dev.macha.layer.protocol.HelloPayload
import dev.macha.layer.protocol.MessageTypes
import dev.macha.layer.protocol.ProtocolV0
import org.java_websocket.WebSocket
import org.java_websocket.handshake.ClientHandshake
import org.java_websocket.server.WebSocketServer
import java.net.InetSocketAddress
import kotlinx.serialization.json.decodeFromJsonElement

/**
 * WebSocket 数据面（04 §3.3）：`ws://…/ws` 数据推送 + 往返。
 *
 * Java-WebSocket 1.6.0 起服务端；收帧 → [JsonFraming.decodeFrame] → 交给
 * [onMessage] 回调；`hello` 由 [SessionHandshake] 就地回 `hello_ack`/`error(bad_version)`。
 * `send` 广播给所有已连接会话。绑定独立端口（分端口，00 §H-D5）。
 */
class WebSocketDataPlane(
    private val bind: String = "127.0.0.1",
    private val port: Int = 8766,
    private val handshake: SessionHandshake,
) : TransportServer {

    private val sessions = java.util.Collections.synchronizedSet(mutableSetOf<WebSocket>())

    @Volatile
    private var running = false
    private var server: WebSocketServer? = null

    val isRunning: Boolean get() = running

    override fun onMessage(handler: (Envelope) -> Unit) {
        inboundHandler = handler
    }

    @Volatile
    private var inboundHandler: ((Envelope) -> Unit)? = null

    override fun start() {
        if (running) return

        val s = object : WebSocketServer(InetSocketAddress(bind, port)) {

            override fun onOpen(conn: WebSocket, hs: ClientHandshake) {
                sessions.add(conn)
            }

            override fun onClose(conn: WebSocket, code: Int, reason: String, remote: Boolean) {
                sessions.remove(conn)
            }

            override fun onMessage(conn: WebSocket, message: String) {
                val env = JsonFraming.decodeFrame(message)
                inboundHandler?.invoke(env)
                if (env.type == MessageTypes.HELLO) {
                    decodeHello(env)?.let { body ->
                        val reply = handshake.onHello(env.id, body)
                        conn.send(JsonFraming.encode(reply))
                    }
                }
            }

            override fun onStart() = Unit

            override fun onError(conn: WebSocket?, ex: Exception) {
                // 连接级错误不影响其它会话；绑定失败会回调到这里的 conn=null。
            }
        }

        s.start()
        server = s
        running = true
    }

    override fun stop() {
        running = false
        try {
            server?.stop()
        } catch (_: Exception) {
            // 未就绪/已停的连接，忽略以便幂等。
        }
        server = null
        sessions.clear()
        inboundHandler = null
    }

    /** 广播一条数据面消息（所有已连接会话）。 */
    override fun send(envelope: Envelope) {
        val frame = JsonFraming.encode(envelope)
        synchronized(sessions) {
            sessions.forEach { session -> session.send(frame) }
        }
    }

    private fun decodeHello(env: Envelope): HelloPayload? = try {
        ProtocolV0.json.decodeFromJsonElement(HelloPayload.serializer(), env.payload)
    } catch (_: Exception) {
        null
    }
}