package dev.macha.layer.runtime.port

/**
 * 时间来源（04 §3.2）：避免 Layer 硬编码"环境 tick 语义"。
 * 环境字段里的 tick 仍是环境信息；此处的 `nowMillis()` 只用于协议信封的 wall clock 与超时判断。
 */
interface ClockPort {
    fun nowMillis(): Long

    companion object {
        val system: ClockPort = object : ClockPort {
            override fun nowMillis(): Long = System.currentTimeMillis()
        }
    }
}