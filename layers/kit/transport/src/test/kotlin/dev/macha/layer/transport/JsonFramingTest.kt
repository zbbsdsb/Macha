package dev.macha.layer.transport

import dev.macha.layer.protocol.Envelope
import dev.macha.layer.protocol.MessageTypes
import kotlinx.serialization.json.buildJsonObject
import kotlinx.serialization.json.put
import kotlin.test.Test
import kotlin.test.assertEquals

class JsonFramingTest {

    @Test
    fun `framing round-trips an envelope`() {
        val envelope = Envelope(
            version = "0",
            type = MessageTypes.ACTION,
            id = "act-9",
            ts = 1_789_000_000_000L,
            payload = buildJsonObject { put("agent", "agent_001") },
        )
        val frame = JsonFraming.encode(envelope)
        val decoded = JsonFraming.decodeFrame(frame)

        assertEquals(envelope, decoded)
    }
}