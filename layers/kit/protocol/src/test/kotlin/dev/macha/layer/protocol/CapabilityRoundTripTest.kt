package dev.macha.layer.protocol

import kotlinx.serialization.builtins.ListSerializer
import kotlinx.serialization.decodeFromString
import kotlinx.serialization.encodeToString
import kotlin.test.Test
import kotlin.test.assertEquals

/**
 * M0-A：能力清单经 ProtocolV0.json 往返，args/preconditions/verifiability/cost 不丢。
 */
class CapabilityRoundTripTest {

    @Test
    fun `single capability round-trips with all fields`() {
        val capability = Capability(
            name = "move",
            args = mapOf("target" to "vec3", "speed" to "number"),
            preconditions = listOf("chunk_loaded"),
            expectedEffect = "position change",
            verifiability = "checked",
            cost = "moderate",
        )
        val text = ProtocolV0.json.encodeToString(Capability.serializer(), capability)
        val back = ProtocolV0.json.decodeFromString(Capability.serializer(), text)

        assertEquals(capability, back)
        assertEquals(mapOf("target" to "vec3", "speed" to "number"), back.args)
        assertEquals(listOf("chunk_loaded"), back.preconditions)
        assertEquals("checked", back.verifiability)
        assertEquals("moderate", back.cost)
    }

    @Test
    fun `declared catalog round-trips as a list filtered-capably`() {
        val caps = CapabilityCatalog.declared()
        assertEquals(4, caps.size)

        val text = ProtocolV0.json.encodeToString(ListSerializer(Capability.serializer()), caps)
        val back = ProtocolV0.json.decodeFromString(ListSerializer(Capability.serializer()), text)

        assertEquals(caps, back)
        // 每条都必须带 args 与 verifiability（M0-A 验收）
        caps.forEach { c ->
            val roundTrip = back.first { it.name == c.name }
            assertEquals(c.args, roundTrip.args)
            assertEquals(c.verifiability, roundTrip.verifiability)
        }
    }
}