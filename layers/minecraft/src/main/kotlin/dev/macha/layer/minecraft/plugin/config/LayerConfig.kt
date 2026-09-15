package dev.macha.layer.minecraft.plugin.config

/** config.yml 映射（03 §5）。 */
data class LayerConfig(
    val bind: String = "127.0.0.1",
    val port: Int = 8765,
    val wsPort: Int = 8766,
    val token: String = "",
    val agentDefaultBinding: String = "nearest_zombie",
    val observationRadius: Double = 16.0,
    val observationMaxEntities: Int = 16,
    val observationMaxBlocks: Int = 32,
    val observationPushIntervalTicks: Int = 20,
    val eventsSubscribeDefault: String = "all",
    val logLevel: String = "INFO",
) {
    companion object {

        /** 从 Bukkit 配置读取（用稳定公开 API）。 */
        fun from(config: org.bukkit.configuration.file.FileConfiguration): LayerConfig {
            fun str(vararg path: String) = config.getString(path.joinToString("."))
            fun int(vararg path: String, def: Int) = config.getInt(path.joinToString("."), def)
            fun dbl(vararg path: String, def: Double) = config.getDouble(path.joinToString("."), def)

            return LayerConfig(
                bind = str("transport", "bind") ?: "127.0.0.1",
                port = int("transport", "port", def = 8765),
                wsPort = int("transport", "ws_port", def = 8766),
                token = str("transport", "token") ?: "",
                agentDefaultBinding = str("agent", "default_binding") ?: "nearest_zombie",
                observationRadius = dbl("observation", "radius", def = 16.0),
                observationMaxEntities = int("observation", "max_entities", def = 16),
                observationMaxBlocks = int("observation", "max_blocks", def = 32),
                observationPushIntervalTicks = int("observation", "push_interval_ticks", def = 20),
                eventsSubscribeDefault = str("events", "subscribe_default") ?: "all",
                logLevel = str("log", "level") ?: "INFO",
            )
        }
    }
}