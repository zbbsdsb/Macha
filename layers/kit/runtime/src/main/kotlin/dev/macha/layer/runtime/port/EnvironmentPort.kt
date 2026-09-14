package dev.macha.layer.runtime.port

import dev.macha.layer.protocol.ActionResultPayload
import dev.macha.layer.protocol.EventPayload
import dev.macha.layer.protocol.ObservationPayload
import dev.macha.layer.runtime.ActionCall

/**
 * 环境侧唯一接口（04 §3.2 ★）——本结构里最重要的接口。
 *
 * `:minecraft` 与 `:simulator` 各自实现它，`:runtime` 只认这个契约。
 * 这就是"环境接入被压缩成一个可被第二个环境复用的接口"的具体形态。
 */
interface EnvironmentPort {

    /** 采集一次 agent 视角的观察（快照）；返回 null 表示该 agent 当前不可见/不存在。 */
    fun collectObservation(agentId: String): ObservationPayload?

    /**
     * 执行一个动作；返回结果（ok/refused/failed + delta）。
     * 返回 null 表示环境根本无法处理该动作——由 runtime 包成 `failed(internal)` 回传。
     * 注意：能力"是否已声明/允许"由 runtime 先校验；此处的 refused 表示环境在**执行时**拒绝。
     */
    fun execute(call: ActionCall): ActionResultPayload?

    /** 环境把后续事件经此注册的 handler 投递上来（线程由环境保证安全）。 */
    fun onEvent(handler: EventHandler)

    fun interface EventHandler {
        fun onEvent(event: EventPayload)
    }
}