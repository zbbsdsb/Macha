package dev.macha.layer.runtime

import dev.macha.layer.protocol.ActionPayload
import dev.macha.layer.protocol.Envelope
import dev.macha.layer.protocol.MessageTypes
import dev.macha.layer.protocol.ProtocolCodec
import dev.macha.layer.protocol.ProtocolV0
import kotlinx.serialization.json.JsonArray
import kotlinx.serialization.json.JsonObject
import kotlinx.serialization.json.JsonPrimitive
import kotlinx.serialization.json.buildJsonArray
import kotlinx.serialization.json.buildJsonObject
import kotlinx.serialization.json.double
import kotlinx.serialization.json.encodeToJsonElement
import kotlinx.serialization.json.jsonPrimitive
import kotlinx.serialization.json.put
import kotlin.test.Test
import kotlin.test.assertEquals
import kotlin.test.assertIs

/** F1：协议 ActionPayload → ActionCall → 适配器视图，字段与类型保真、无需字符串再解析。 */
class ActionCallRoundTripTest {

    @Test
    fun `move target array survives ActionPayload to ActionCall`() {
        val payload = ActionPayload(
            agent = "agent_001",
            action = "move",
            args = mapOf("target" to buildJsonArray {
                add(JsonPrimitive(20.0)); add(JsonPrimitive(64.0)); add(JsonPrimitive(-3.0))
            }),
        )

        val call = ActionCall.from(payload)

        assertEquals(payload.agent, call.agent)
        assertEquals(payload.action, call.action)
        val target = call.args.getValue("target")
        assertIs<JsonArray>(target)
        assertEquals(listOf(20.0, 64.0, -3.0), target.map { it.jsonPrimitive.double })
    }

    @Test
    fun `interact nested object survives ActionPayload to ActionCall`() {
        val payload = ActionPayload(
            agent = "agent_001",
            action = "interact",
            args = mapOf("target" to buildJsonObject { put("id", "player:steve") }),
        )

        val call = ActionCall.from(payload)

        val target = call.args.getValue("target")
        assertIs<JsonObject>(target)
        assertEquals("player:steve", target.getValue("id").jsonPrimitive.content)
    }

    @Test
    fun `envelope encode-decode round trip keeps args lossless end to end`() {
        val payload = ActionPayload(
            agent = "agent_001",
            action = "move",
            args = mapOf("target" to buildJsonArray {
                add(JsonPrimitive(20.0)); add(JsonPrimitive(64.0)); add(JsonPrimitive(-3.0))
            }),
        )
        val envelope = Envelope(
            version = ProtocolV0.CURRENT,
            type = MessageTypes.ACTION,
            id = "req-1",
            ts = 1L,
            payload = ProtocolV0.json.encodeToJsonElement(ActionPayload.serializer(), payload),
        )

        val decoded = ProtocolCodec.decode(ProtocolCodec.encode(envelope))
        val replayed = ProtocolV0.json.decodeFromJsonElement(ActionPayload.serializer(), decoded.payload)

        val call = ActionCall.from(replayed)
        val target = call.args.getValue("target")
        assertIs<JsonArray>(target)
        assertEquals(listOf(20.0, 64.0, -3.0), target.map { it.jsonPrimitive.double })
    }
}