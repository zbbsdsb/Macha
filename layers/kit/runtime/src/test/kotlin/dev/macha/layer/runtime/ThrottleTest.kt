package dev.macha.layer.runtime

import kotlin.test.Test
import kotlin.test.assertEquals

/** 事件节流与截断标记（04 §3.2）。 */
class ThrottleTest {

    @Test
    fun `bounded queue drops overflow and counts`() {
        val throttle = EventThrottle(maxSize = 2)
        assertEquals(0, throttle.emit("minecraft:entity_move"))
        assertEquals(0, throttle.emit("minecraft:block_break"))

        val dropped = throttle.emit("minecraft:block_place")
        assertEquals(1, dropped) // 本次被丢弃
        assertEquals(1L, throttle.droppedCount())
        assertEquals(2, throttle.size())
    }

    @Test
    fun `drain empties queue`() {
        val throttle = EventThrottle(maxSize = 8)
        throttle.emit("a")
        throttle.emit("b")
        assertEquals(listOf("a", "b"), throttle.drain())
        assertEquals(0, throttle.size())
    }
}