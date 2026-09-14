package dev.macha.layer.runtime

/**
 * 观测窗口编排（04 §3.2）：push 间隔、无变化跳过（02 §4）。
 * v0 默认每 N tick 采样一次（N 可配置，建议 20≈1 秒），或由 Runtime 用 `observation_request` 拉取。
 */
class ObservationScheduler(
    private val intervalTicks: Int = 20,
) {
    @Volatile
    private var lastEmittedAtTick: Long = Long.MIN_VALUE

    /**
     * 询问"当前 tick 是否应推送一次 observation"。
     * 返回 true 表示需要采样；随后调用方应报告当前 tick 以推进内部状态。
     */
    fun shouldSample(tick: Long): Boolean {
        if (tick - lastEmittedAtTick >= intervalTicks) {
            lastEmittedAtTick = tick
            return true
        }
        return false
    }
}