package dev.macha.layer.protocol

/**
 * 默认能力目录（01 §3.2 / M0-A）。
 *
 * 抽离为**不 import Paper** 的纯协议对象：在 `:kit:protocol` 里既服务插件装配，
 * 又可无环境依赖地单测。能力是"Layer 实测能执行的动作" 清单，不是愿望清单。
 */
object CapabilityCatalog {

    fun declared(): List<Capability> = listOf(
        Capability(
            name = "move",
            args = mapOf("target" to "vec3"),
            preconditions = listOf("chunk_loaded"),
            expectedEffect = "position change",
            verifiability = "checked",
        ),
        Capability(
            name = "look",
            args = mapOf("yaw" to "number", "pitch" to "number"),
            verifiability = "checked",
        ),
        Capability(
            name = "interact",
            args = mapOf("target" to "entity|block"),
            preconditions = listOf("in_range"),
            verifiability = "trusted",
        ),
        Capability(
            name = "spawn_agent",
            args = mapOf("type" to "string", "position" to "vec3"),
            verifiability = "checked",
            cost = "moderate",
        ),
    )
}