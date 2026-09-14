package dev.macha.layer.minecraft.adapter

import dev.macha.layer.protocol.ActionResultPayload
import dev.macha.layer.protocol.ActionStatus
import dev.macha.layer.protocol.Capability
import dev.macha.layer.protocol.EventPayload
import dev.macha.layer.protocol.ObservationPayload
import dev.macha.layer.runtime.ActionCall
import dev.macha.layer.runtime.port.EnvironmentPort

/**
 * EnvironmentPort 的 Paper 实现骨架（04 §3.4 ★）。
 *
 * TODO(scaffold): 观测采集/事件桥接/动作执行在 vertical slice 阶段接入
 * `adapter/observe`、`adapter/events`、`adapter/action` 时真正填空。
 * 当前：cector 尚未绑定 agent → collectObservation 返回 null；execute 一律 refused。
 * 能力清单先按词表声明（探测真正补全后以实测为准，01 §3.2）。
 */
class PaperEnvironmentPort(
    private val declared: List<Capability>,
) : EnvironmentPort {

    override fun collectObservation(agentId: String): ObservationPayload? {
        // 尚未完成 agent 绑定与采集：不返回任何观察。
        return null
    }

    override fun execute(call: ActionCall): ActionResultPayload {
        // 环境执行尚未接线：骨架阶段对任何一致动作先拒绝，避免"看似成功了"。
        return ActionResultPayload(
            status = ActionStatus.REFUSED,
            reason = "not_supported",
            detail = "Paper action execution not wired yet (scaffold)",
        )
    }

    override fun onEvent(handler: EnvironmentPort.EventHandler) {
        // 事件桥接未接线：仅保留 handler 引用（future）。
        eventHandler = handler
    }

    var eventHandler: EnvironmentPort.EventHandler? = null
        private set

    val declaredCapabilities: List<Capability> get() = declared
}