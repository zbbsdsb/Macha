package dev.macha.layer.protocol

import kotlinx.serialization.Serializable

/**
 * 能力清单（01 §3.2）：是**探测结果**，不是愿望清单。
 * Layer 只能声明自己实测能执行的动作。
 *
 * `args` 用"参数名 -> 形状描述字符串"（可扩展为 JSON Schema）；不用 Java 类名/枚举名，
 * 以便其他语言实现的 Layer 也能对齐（红线 G.2-3）。
 */
@Serializable
data class Capability(
    val name: String,
    val args: Map<String, String> = emptyMap(),
    val preconditions: List<String> = emptyList(),
    val expectedEffect: String? = null,
    val verifiability: String = "checked",
    val cost: String? = null,
)