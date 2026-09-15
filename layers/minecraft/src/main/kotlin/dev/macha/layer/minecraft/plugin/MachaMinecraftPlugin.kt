package dev.macha.layer.minecraft.plugin

import dev.macha.layer.minecraft.adapter.PaperEnvironmentPort
import dev.macha.layer.minecraft.plugin.config.LayerConfig
import dev.macha.layer.protocol.ActionPayload
import dev.macha.layer.protocol.ActionResultPayload
import dev.macha.layer.protocol.ActionStatus
import dev.macha.layer.protocol.Capability
import dev.macha.layer.protocol.CapabilityCatalog
import dev.macha.layer.protocol.Envelope
import dev.macha.layer.protocol.EnvironmentInfo
import dev.macha.layer.protocol.FailureReason
import dev.macha.layer.protocol.MessageTypes
import dev.macha.layer.protocol.ProtocolV0
import dev.macha.layer.protocol.WorldTimeRef
import dev.macha.layer.runtime.ActionCall
import dev.macha.layer.runtime.LayerRuntime
import dev.macha.layer.transport.HttpControlPlane
import dev.macha.layer.transport.SessionHandshake
import dev.macha.layer.transport.WebSocketDataPlane
import kotlinx.serialization.builtins.ListSerializer
import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.decodeFromJsonElement
import kotlinx.serialization.json.encodeToJsonElement
import org.bukkit.plugin.java.JavaPlugin

/**
 * JavaPlugin 入口（04 §3.4 ★）：onEnable/onDisable，装配 runtime+transport+adapter。
 * 唯一允许 import Paper 的另一处是 `adapter/`（其余模块由 Gradle 编译期强制）。
 */
class MachaMinecraftPlugin : JavaPlugin() {

    private lateinit var config: LayerConfig
    private lateinit var runtime: LayerRuntime
    private var http: HttpControlPlane? = null
    private var ws: WebSocketDataPlane? = null

    override fun onEnable() {
        saveDefaultConfig()
        config = LayerConfig.from(getConfig())

        val capabilities = CapabilityCatalog.declared()
        val port = PaperEnvironmentPort(capabilities)
        runtime = LayerRuntime(port, capabilities)

        // 环境信息（hello_ack 用）：从 Bukkit 实测读取，不编造（01 §3.2"探测结果"）。
        val environment = EnvironmentInfo(
            kind = "minecraft",
            versions = mapOf(
                "paper" to server.bukkitVersion,
                "minecraft" to server.version,
            ),
            worlds = server.worlds.map { it.key.asString() },
        )
        val time = WorldTimeRef(
            tick = server.currentTick.toLong(),
            worldTime = server.worlds.firstOrNull()?.time,
            unit = "tick",
        )

        val handshake = SessionHandshake(
            layerName = "macha-minecraft",
            layerVersion = pluginVersion(),
            environment = environment,
            time = time,
            capabilities = capabilities,
        )

        // HTTP 控制面：healthz / capabilities / action（动作走真实分发路径 → refused not_supported）。
        val onAction: (Envelope) -> Envelope = { env ->
            val result = try {
                val payload = ProtocolV0.json.decodeFromJsonElement(ActionPayload.serializer(), env.payload)
                runtime.onAction(ActionCall.from(payload))
            } catch (e: Exception) {
                ActionResultPayload(
                    status = ActionStatus.FAILED,
                    reason = FailureReason.INTERNAL,
                    detail = "unparseable action payload: ${e.message}",
                )
            }
            Envelope(
                version = ProtocolV0.CURRENT,
                type = MessageTypes.ACTION_RESULT,
                id = env.id,
                ts = System.currentTimeMillis(),
                payload = ProtocolV0.json.encodeToJsonElement(ActionResultPayload.serializer(), result),
            )
        }

        http = HttpControlPlane(
            bind = config.bind,
            port = config.port,
            capabilityJson = { ProtocolV0.json.encodeToString(ListSerializer(Capability.serializer()), capabilities) },
            actionHandler = onAction,
        ).also { it.start() }

        // WebSocket 数据面：独立端口（分端口，00 §H-D5）。
        try {
            ws = WebSocketDataPlane(
                bind = config.bind,
                port = config.wsPort,
                handshake = handshake,
            ).also { it.start() }
        } catch (e: Exception) {
            logger.warning("WebSocket data plane failed to start on ${config.bind}:${config.wsPort}: ${e.message}")
        }

        logger.info(
            "Macha Minecraft Layer v%s up — protocol v0, transport %s:%d"
                .format(pluginVersion(), config.bind, config.port),
        )
        if (ws?.isRunning == true) {
            logger.info("WebSocket data plane up on %s:%d (http control plane on %d)".format(config.bind, config.wsPort, config.port))
        }
    }

    override fun onDisable() {
        ws?.stop()
        http?.stop()
        runtime.stop()
        logger.info("Macha Minecraft Layer down")
    }

    @Suppress("DEPRECATION") // Bukkit Plugin#getDescription → Paper 26.x 已弃用；scaffold 期沿用
    private fun pluginVersion(): String = description.version
}