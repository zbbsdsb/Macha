package dev.macha.layer.testclient

import dev.macha.layer.protocol.Envelope
import dev.macha.layer.protocol.HelloPayload
import dev.macha.layer.protocol.MessageTypes
import dev.macha.layer.protocol.ProtocolRange
import dev.macha.layer.protocol.ProtocolV0
import dev.macha.layer.protocol.RuntimeRef
import kotlinx.serialization.decodeFromString
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.encodeToJsonElement
import org.java_websocket.client.WebSocketClient
import org.java_websocket.handshake.ServerHandshake
import java.net.URI
import java.util.concurrent.CountDownLatch
import java.util.concurrent.TimeUnit

/**
 * 垂直切片测试客户端（04 §3.6 ★）。最小实现：连 WS → 发一次 `hello` → 收 `hello_ack`；
 * 服务器不在时优雅报错退出。8 步闭环（00 §F：hello → ack → capability → observation →
 * action → result → event → transcript）留待后续。
 */
fun main(args: Array<String>) {
    val host = args.getOrNull(0) ?: "127.0.0.1"
    val port = args.getOrNull(1)?.toIntOrNull() ?: 8765
    val uri = URI("ws://$host:$port/ws")
    val done = CountDownLatch(1)
    var exit = 0

    val client = object : WebSocketClient(uri) {
        override fun onOpen(handshakedata: ServerHandshake) {
            val payload = HelloPayload(
                runtime = RuntimeRef(name = "macha-testclient", version = "0.1.0", lang = "kotlin"),
                protocol = ProtocolRange(min = "0", max = "0"),
                subscribe = listOf("all"),
            )
            val envelope = Envelope(
                version = ProtocolV0.CURRENT,
                type = MessageTypes.HELLO,
                id = "probe-${System.currentTimeMillis()}",
                ts = System.currentTimeMillis(),
                payload = ProtocolV0.json.encodeToJsonElement(HelloPayload.serializer(), payload),
            )
            send(ProtocolV0.json.encodeToString(Envelope.serializer(), envelope))
            println("-> hello sent")
        }

        override fun onMessage(message: String) {
            val env = ProtocolV0.json.decodeFromString(Envelope.serializer(), message)
            println("<- ${env.type}")
            if (env.type == MessageTypes.HELLO_ACK) {
                println("handshake ok")
                exit = 0
                done.countDown()
            }
        }

        override fun onClose(code: Int, reason: String, remote: Boolean) {
            println("session closed: $code $reason")
        }

        override fun onError(ex: Exception) {
            System.err.println("ws error: $ex (is the Layer server up? waiting off)")
            exit = 1
            done.countDown()
        }
    }

    println("connecting $uri …")
    try {
        client.connect()
    } catch (t: Throwable) {
        System.err.println("connect failed: $t")
        exit = 1
    }

    val finished = done.await(10, TimeUnit.SECONDS)
    try {
        client.close()
    } catch (_: Throwable) {
        // close 对未连接/已失败连接可能抛异常，忽略以便继续报 exit。
    }

    if (!finished) {
        System.err.println("timeout waiting for hello_ack; is the Layer (http://$host:$port) up?")
        exit = 1
    }
    println("probe exit=$exit")
    kotlin.system.exitProcess(exit)
}