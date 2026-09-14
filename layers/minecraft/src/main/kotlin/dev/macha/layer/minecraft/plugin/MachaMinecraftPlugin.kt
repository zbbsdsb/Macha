package dev.macha.layer.minecraft.plugin

import dev.macha.layer.minecraft.adapter.PaperEnvironmentPort
import dev.macha.layer.minecraft.plugin.config.LayerConfig
import dev.macha.layer.protocol.Capability
import dev.macha.layer.runtime.LayerRuntime
import dev.macha.layer.transport.HttpControlPlane
import org.bukkit.plugin.java.JavaPlugin

/**
 * JavaPlugin 入口（04 §3.4 ★）：onEnable/onDisable，装配 runtime+transport+adapter。
 * 唯一允许 import Paper 的另一处是 `adapter/`（其余模块由 Gradle 编译期强制）。
 */
class MachaMinecraftPlugin : JavaPlugin() {

    private lateinit var config: LayerConfig
    private lateinit var runtime: LayerRuntime
    private var http: HttpControlPlane? = null

    override fun onEnable() {
        saveDefaultConfig()
        config = LayerConfig.from(getConfig())

        val port = PaperEnvironmentPort(declaredCapabilities())
        runtime = LayerRuntime(port, port.declaredCapabilities)

        http = HttpControlPlane(
            bind = config.bind,
            port = config.port,
            capabilityJson = { capabilityManifestJson(port.declaredCapabilities) },
        ).also { it.start() }

        logger.info(
            "Macha Minecraft Layer v%s up — protocol v0, transport %s:%d".format(pluginVersion(), config.bind, config.port),
        )
    }

    override fun onDisable() {
        http?.stop()
        runtime.stop()
        logger.info("Macha Minecraft Layer down")
    }

    private fun declaredCapabilities(): List<Capability> = listOf(
        Capability(name = "move", args = mapOf("target" to "vec3"), preconditions = listOf("chunk_loaded"), expectedEffect = "position change", verifiability = "checked"),
        Capability(name = "look", args = mapOf("yaw" to "number", "pitch" to "number"), verifiability = "checked"),
        Capability(name = "interact", args = mapOf("target" to "entity|block"), preconditions = listOf("in_range"), verifiability = "trusted"),
        Capability(name = "spawn_agent", args = mapOf("type" to "string", "position" to "vec3"), verifiability = "checked", cost = "moderate"),
    )

    @Suppress("DEPRECATION") // Bukkit Plugin#getDescription → Paper 26.x 已弃用；scaffold 期沿用
    private fun pluginVersion(): String = description.version

    private fun capabilityManifestJson(caps: List<Capability>): String =
        "[" + caps.joinToString(",") {
            """{"name":"${it.name}","args":{},"expected_effect":"${it.expectedEffect ?: ""}"}"""
        } + "]"
}