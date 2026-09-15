package dev.macha.layer.transport

import com.sun.net.httpserver.HttpServer
import java.net.InetSocketAddress
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.buildJsonObject
import kotlinx.serialization.json.put
import kotlinx.serialization.json.encodeToJsonElement
import dev.macha.layer.protocol.ActionResultPayload
import dev.macha.layer.protocol.ActionStatus
import dev.macha.layer.protocol.Envelope
import dev.macha.layer.protocol.MessageTypes
import dev.macha.layer.protocol.ProtocolCodec
import dev.macha.layer.protocol.ProtocolV0
import dev.macha.layer.protocol.RefusalReason

/**
 * HTTP 控制面（04 §3.3 / 01 §5）：健康检查 / 协议版本 / 能力清单 / 单发动作。
 *
 * 用 JDK 内置 `com.sun.net.httpserver`，零第三方依赖（00 §D，避免为 HTTP 引 Web 框架）。
 * 默认绑定 127.0.0.1（不外网暴露）。`/action` 接收一个 action 信封，返回 action_result 信封——
 * 具体拒绝/分发由外部注入的 [actionHandler] 决定（transport 不认识动作语义）。
 */
class HttpControlPlane(
    private val bind: String = "127.0.0.1",
    private val port: Int = 8765,
    private val capabilityJson: () -> String = { "[]" },
    private val actionHandler: (Envelope) -> Envelope = { env ->
        // 默认：一切动作都拒绝（尚未接线）；由装配方替换为真实环境执行。
        val result = ActionResultPayload(
            status = ActionStatus.REFUSED,
            reason = RefusalReason.NOT_SUPPORTED,
            detail = "action execution not wired",
        )
        Envelope(
            version = ProtocolV0.CURRENT,
            type = MessageTypes.ACTION_RESULT,
            id = env.id,
            ts = System.currentTimeMillis(),
            payload = ProtocolV0.json.encodeToJsonElement(ActionResultPayload.serializer(), result),
        )
    },
) {
    private var server: HttpServer? = null

    fun start() {
        val s = HttpServer.create(InetSocketAddress(bind, port), 0)

        s.createContext("/action") { ex ->
            if (ex.requestMethod != "POST") {
                ex.sendResponseHeaders(405, -1)
                ex.close()
                return@createContext
            }
            val body = ex.requestBody.readBytes().toString(Charsets.UTF_8)
            val result = try {
                ProtocolCodec.encode(actionHandler(ProtocolCodec.decode(body)))
            } catch (e: Exception) {
                ProtocolV0.json.encodeToString(
                    buildJsonObject {
                        put("error", "bad_action")
                        put("detail", e.message ?: "unparseable action envelope")
                    },
                )
            }
            respond(ex, result)
        }

        s.createContext("/healthz") { ex ->
            val body = ProtocolV0.json.encodeToString(
                buildJsonObject {
                    put("ok", true)
                    put("protocol", ProtocolV0.CURRENT)
                },
            )
            respond(ex, body)
        }

        s.createContext("/capabilities") { ex ->
            respond(ex, capabilityJson())
        }

        s.start()
        server = s
    }

    fun stop() {
        server?.stop(0)
        server = null
    }

    private fun respond(exchange: com.sun.net.httpserver.HttpExchange, body: String) {
        val bytes = body.toByteArray(Charsets.UTF_8)
        exchange.responseHeaders.add("Content-Type", "application/json")
        exchange.sendResponseHeaders(200, bytes.size.toLong())
        exchange.responseBody.use { it.write(bytes) }
    }
}