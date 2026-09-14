package dev.macha.layer.simulator

import dev.macha.layer.protocol.ActionResultPayload
import dev.macha.layer.protocol.ActionStatus
import dev.macha.layer.protocol.ObservationPayload
import dev.macha.layer.protocol.RefusalReason
import dev.macha.layer.runtime.ActionCall
import dev.macha.layer.runtime.port.EnvironmentPort

/**
 * EnvironmentPort 的假实现（04 §3.5 ★）——C4 对照条件：与 Minecraft 共用同一份
 * kit/protocol 与 kit/runtime，用于验证协议/运行时可移植性。当前为最小可编译骨架。
 */
class SimulatorEnvironmentPort : EnvironmentPort {

    override fun collectObservation(agentId: String): ObservationPayload? {
        // TODO(scaffold): 网格世界快照；暂不返回任何观察。
        return null
    }

    override fun execute(call: ActionCall): ActionResultPayload {
        // TODO(scaffold): 假环境动作执行（含 SimWorld/SimEntities 推进）。
        // 先拒绝，避免在接线前"看似成功"。
        return ActionResultPayload(
            status = ActionStatus.REFUSED,
            reason = RefusalReason.NOT_SUPPORTED,
            detail = "simulator action execution not wired yet (scaffold)",
        )
    }

    override fun onEvent(handler: EnvironmentPort.EventHandler) {
        // TODO(scaffold): 事件桥接；先保留 handler 供 future 使用（比对 J3 事件 kind）。
        eventHandler = handler
    }

    private var eventHandler: EnvironmentPort.EventHandler? = null
}