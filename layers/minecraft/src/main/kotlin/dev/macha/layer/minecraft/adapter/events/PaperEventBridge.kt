package dev.macha.layer.minecraft.adapter.events

import dev.macha.layer.protocol.EventPayload

/**
 * 监听器注册 + 只做归一化 + 入队（04 §3.4 ★）；回调内禁止 IO。
 * TODO(scaffold): 注册 Bukkit 监听器并桥接到 runtime 的事件 handler。
 */
class PaperEventBridge {

    fun publish(event: EventPayload) {
        TODO("scaffold: event bridge not wired")
    }
}