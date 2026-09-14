package dev.macha.layer.transport

import com.sun.net.httpserver.HttpServer
import java.net.InetSocketAddress
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.buildJsonObject
import kotlinx.serialization.json.put
import dev.macha.layer.protocol.ProtocolV0

/**
 * HTTP 控制面（04 §3.3 / 01 §5）：健康检查 / 协议版本 / 能力清单 / 单发动作。
 *
 * 用 JDK 内置 `com.sun.net.httpserver`，零第三方依赖（00 §D，避免为 HTTP 引 Web 框架）。
 * 默认绑定 127.0.0.1（不外网暴露）。
 */
class HttpControlPlane(
    private val bind: String = "127.0.0.1",
    private val port: Int = 8765,
    private val capabilityJson: () -> String = { "[]" },
) {
    private var server: HttpServer? = null

    fun start() {
        val s = HttpServer.create(InetSocketAddress(bind, port), 0)

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