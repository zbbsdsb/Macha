package dev.macha.layer.testclient

import dev.macha.layer.protocol.Envelope
import dev.macha.layer.protocol.ErrorCode
import dev.macha.layer.protocol.HelloPayload
import dev.macha.layer.protocol.MessageTypes
import dev.macha.layer.protocol.ProtocolRange
import dev.macha.layer.protocol.ProtocolV0
import dev.macha.layer.protocol.RuntimeRef
import kotlinx.serialization.json.decodeFromJsonElement
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
 * 服务器不在时优雅报错退出。
 *
 * `mode`：默认 `happy`（期望 hello_ack）；`bad-version` 发不兼容的协议范围，期望 `error(bad_version)`。
 */
fun main(args: Array<String>) {
    val host = args.getOrNull(0) ?: "127.0.0.1"
    val port = args.getOrNull(1)?.toIntOrNull() ?: 8766
    val mode = args.getOrNull(2)?.lowercase() ?: "happy"
    val uri = URI("ws://$host:$port/ws")
    val done = CountDownLatch(1)
    var exit = 0

    fun helloEnvelope(): Envelope {
        val range = if (mode == "bad-version") ProtocolRange(min = "1", max = "2") else ProtocolRange("0", "0")
        val payload = HelloPayload(
            runtime = RuntimeRef(name = "macha-testclient", version = "0.1.0", lang = "kotlin"),
            protocol = range,
            subscribe = listOf("all"),
        )
        return Envelope(
            version = ProtocolV0.CURRENT,
            type = MessageTypes.HELLO,
            id = "probe-${System.currentTimeMillis()}",
            ts = System.currentTimeMillis(),
            payload = ProtocolV0.json.encodeToJsonElement(HelloPayload.serializer(), payload),
        )
    }

    val client = object : WebSocketClient(uri) {
        override fun onOpen(handshakedata: ServerHandshake) {
            send(ProtocolV0.json.encodeToString(Envelope.serializer(), helloEnvelope()))
            println("-> hello sent (mode=$mode)")
        }

        override fun onMessage(message: String) {
            val env = ProtocolV0.json.decodeFromString(Envelope.serializer(), message)
            println("<- ${env.type}")
            when {
                env.type == MessageTypes.HELLO_ACK && mode == "happy" -> {
                    println("handshake ok")
                    exit = 0
                    done.countDown()
                }
                env.type == MessageTypes.ERROR && mode == "bad-version" -> {
                    val error = ProtocolV0.json.decodeFromJsonElement(
                        dev.macha.layer.protocol.ErrorPayload.serializer(), env.payload,
                    )
                    println("got error: code=${error.code} ${error.message}")
                    if (error.code == ErrorCode.BAD_VERSION) {
                        exit = 0
                    } else {
                        println("unexpected error code ${error.code}")
                        exit = 1
                    }
                    done.countDown()
                }
                else -> {
                    println("unexpected ${env.type} for mode=$mode")
                    exit = 1
                    done.countDown()
                }
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
        System.err.println("timeout waiting for ${if (mode == "bad-version") "error(bad_version)" else "hello_ack"}; " +
            "is the Layer ws://$host:$port up?")
        exit = 1
    }
    println("probe exit=$exit")
    kotlin.system.exitProcess(exit)
}