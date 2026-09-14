package dev.macha.layer.runtime

import dev.macha.layer.protocol.ActionResultPayload
import dev.macha.layer.protocol.ActionStatus
import dev.macha.layer.protocol.FailureReason
import dev.macha.layer.runtime.port.EnvironmentPort

/**
 * 动作派发（04 §3.2 ★）：action → 校验 → 执行 → 结果回传。
 *
 * 纯 JVM，不阻塞网络线程；真实环境里 `execute` 回主线程执行的部分由
 * `:minecraft` 的 `adapter/action/ActionExecutor` 承担（见 03 §6 线程规则）。
 */
class ActionDispatcher(
    private val environment: EnvironmentPort,
    private val validator: ActionValidator,
) {

    fun dispatch(call: ActionCall): ActionResultPayload {
        validator.validate(call)?.let { return it }
        return environment.execute(call)
            ?: ActionResultPayload(status = ActionStatus.FAILED, reason = FailureReason.INTERNAL, detail = "environment returned no result")
    }
}