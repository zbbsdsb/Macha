package dev.macha.layer.runtime

import dev.macha.layer.runtime.port.ClockPort

/**
 * action id ↔ action_result 关联与超时（04 §3.2）。
 * v0 用同步返回 + 超时即可，允许真实的异步结果（01 §8-4）。
 * 详情：真实 Layer 里 ResultCorrelator 负责把异步回传的 action_result 与请求 id 对上。
 */
class ResultCorrelator(
    private val clock: ClockPort,
    private val timeoutMillis: Long = 5_000,
) {
    private val pending = HashMap<String, Long>()

    /** 登记一个尚未完成的 action id。 */
    fun track(actionId: String): Long {
        val ts = clock.nowMillis()
        pending[actionId] = ts
        return ts
    }

    /** 是否该 action 已超时。 */
    fun isExpired(actionId: String): Boolean {
        val start = pending[actionId] ?: return true
        return clock.nowMillis() - start > timeoutMillis
    }

    fun resolve(actionId: String): Boolean = pending.remove(actionId) != null

    fun pendingCount(): Int = pending.size
}