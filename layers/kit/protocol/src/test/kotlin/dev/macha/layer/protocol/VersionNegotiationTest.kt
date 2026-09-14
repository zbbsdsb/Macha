package dev.macha.layer.protocol

import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertNull

class VersionNegotiationTest {

    @Test
    fun `matching version negotiates to current`() {
        assertEquals("0", ProtocolCodec.negotiate(ProtocolRange("0", "0")))
    }

    @Test
    fun `overlapping range negotiates`() {
        assertEquals("0", ProtocolCodec.negotiate(ProtocolRange("0", "1")))
    }

    @Test
    fun `incompatible future-only range yields null`() {
        // 与 {0} 无交集 → 应触发 error(bad_version)，协商返回 null
        assertNull(ProtocolCodec.negotiate(ProtocolRange("1", "2")))
    }
}