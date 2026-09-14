package dev.macha.layer.protocol

import kotlinx.serialization.json.buildJsonObject
import kotlinx.serialization.json.put
import kotlin.test.Test
import kotlin.test.assertEquals

class EnvelopeRoundTripTest {

    @Test
    fun `envelope round-trips through codec`() {
        val envelope = Envelope(
            version = "0",
            type = MessageTypes.HELLO,
            id = "c1",
            ts = 1_789_000_000_000L,
            payload = buildJsonObject { put("who", "macha-runtime") },
        )
        val text = ProtocolCodec.encode(envelope)
        val decoded = ProtocolCodec.decode(text)

        assertEquals(envelope, decoded)
        assertEquals("0", decoded.version)
        assertEquals("c1", decoded.id)
    }
}