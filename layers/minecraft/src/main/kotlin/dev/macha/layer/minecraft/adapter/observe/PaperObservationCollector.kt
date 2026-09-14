package dev.macha.layer.minecraft.adapter.observe

import dev.macha.layer.protocol.ObservationPayload

/**
 * 主线程采集 → 纯 DTO（04 §3.4 ★）。采集逻辑环境特有，DTO 共享（04 §4 observation 落点）。
 * TODO(scaffold): 调用 NearbyEntityScanner / NearbyBlockScanner / WorldStateReader 组装快照。
 */
class PaperObservationCollector {

    fun collect(agentId: String): ObservationPayload? {
        TODO("scaffold: observation collector not wired")
    }
}