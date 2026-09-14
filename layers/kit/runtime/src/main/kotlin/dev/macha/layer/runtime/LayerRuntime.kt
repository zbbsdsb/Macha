package dev.macha.layer.runtime

import dev.macha.layer.protocol.ActionResultPayload
import dev.macha.layer.protocol.Capability
import dev.macha.layer.protocol.ObservationPayload
import dev.macha.layer.runtime.port.ClockPort
import dev.macha.layer.runtime.port.EnvironmentPort

/**
 * Layer 运行时（04 §3.2 ★）：生命周期、消息入口、能力清单、动作派发。
 *
 * 只认 [EnvironmentPort]，不认识任何具体环境。`:minecraft`/`:simulator` 各自实现端口接入。
 */
class LayerRuntime(
    private val environment: EnvironmentPort,
    capabilities: List<Capability>,
    private val clock: ClockPort = ClockPort.system,
) {
    private val dispatcher = ActionDispatcher(environment, ActionValidator(capabilities))

    @Volatile
    private var running = false

    /** Layer 声明的能力清单（探测结果）。 */
    val declaredCapabilities: List<Capability> = capabilities.toList()

    val isRunning: Boolean get() = running

    fun start() {
        if (running) return
        running = true
    }

    fun stop() {
        running = false
    }

    /** 处理一条入站动作 → 校验/执行/回传结果。 */
    fun onAction(call: ActionCall): ActionResultPayload = dispatcher.dispatch(call)

    /** 采集一次 agent 视角观察。 */
    fun observe(agentId: String): ObservationPayload? = environment.collectObservation(agentId)

    /** 注册环境事件订阅（透传给 EnvironmentPort）。 */
    fun onEvent(handler: EnvironmentPort.EventHandler) = environment.onEvent(handler)
}