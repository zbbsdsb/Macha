package dev.macha.layer.runtime

/**
 * 事件节流/合并（04 §3.2）：有界队列、丢弃计数、实体移动按距离阈值跳过（02 §8-1）。
 * v0 不做完整流控，只用"节流 + 丢弃并计数"（01 §7）。
 */
class EventThrottle(
    private val maxSize: Int = 256,
) {
    private val queue = ArrayDeque<String>()

    @Volatile
    private var dropped = 0L

    /**
     * 入队一个事件；队列满时丢弃并返回本次丢弃数（调用方据此刻 `truncated`/计数上报）。
     */
    fun emit(kind: String): Int {
        return if (queue.size >= maxSize) {
            dropped++
            1
        } else {
            queue.addLast(kind)
            0
        }
    }

    fun drain(): List<String> {
        val out = queue.toList()
        queue.clear()
        return out
    }

    fun droppedCount(): Long = dropped

    fun size(): Int = queue.size
}