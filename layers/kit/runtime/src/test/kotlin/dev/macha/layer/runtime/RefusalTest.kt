package dev.macha.layer.runtime

import dev.macha.layer.protocol.ActionStatus
import dev.macha.layer.protocol.Capability
import dev.macha.layer.protocol.RefusalReason
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertNull

/**
 * 拒绝语义（04 §3.2 ★ / 01 §3.6）：未声明能力 / 未登记的环境动词 →
 * 必须是 `refused`（含 reason），**不是** error。
 */
class RefusalTest {

    private fun validator(vararg caps: Capability) = ActionValidator(caps.toList())

    @Test
    fun `undeclared common-looking verb is refused`() {
        val v = validator(Capability(name = "move"))
        val r = v.validate(ActionCall(agent = "a1", action = "fly"))
        assertEquals(ActionStatus.REFUSED, r!!.status)
        assertEquals(RefusalReason.NOT_SUPPORTED, r.reason)
    }

    @Test
    fun `namespaced verb not registered is refused`() {
        val v = validator(Capability(name = "move"))
        val r = v.validate(ActionCall(agent = "a1", action = "minecraft:place_block"))
        assertEquals(RefusalReason.NOT_SUPPORTED, r!!.reason)
    }

    @Test
    fun `bare environment verb without namespace is refused as invalid`() {
        val v = validator(Capability(name = "move"))
        val r = v.validate(ActionCall(agent = "a1", action = "place_block"))
        assertEquals(RefusalReason.NOT_SUPPORTED, r!!.reason)
    }

    @Test
    fun `declared capability validates to null (allowed)`() {
        val v = validator(Capability(name = "move"))
        assertNull(v.validate(ActionCall(agent = "a1", action = "move")))
    }
}