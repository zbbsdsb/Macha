package dev.macha.layer.transport

import dev.macha.layer.protocol.AgentRef
import dev.macha.layer.protocol.Capability
import dev.macha.layer.protocol.EnvironmentInfo
import dev.macha.layer.protocol.ErrorCode
import dev.macha.layer.protocol.ErrorPayload
import dev.macha.layer.protocol.HelloAckPayload
import dev.macha.layer.protocol.HelloPayload
import dev.macha.layer.protocol.MessageTypes
import dev.macha.layer.protocol.ProtocolRange
import dev.macha.layer.protocol.ProtocolV0
import dev.macha.layer.protocol.RuntimeRef
import dev.macha.layer.protocol.WorldTimeRef
import kotlinx.serialization.json.decodeFromJsonElement
import kotlin.test.Test
import kotlin.test.assertEquals

class SessionHandshakeTest {

    private val handshake = SessionHandshake(
        layerName = "macha-minecraft",
        layerVersion = "0.1.0",
        environment = EnvironmentInfo(
            kind = "minecraft",
            versions = mapOf("paper" to "26.2-123", "minecraft" to "26.2"),
            worlds = listOf("minecraft:overworld"),
        ),
        time = WorldTimeRef(tick = 148213, worldTime = 6000, unit = "tick"),
        capabilities = listOf(Capability(name = "move", args = mapOf("target" to "vec3"))),
        agents = listOf(AgentRef(id = "agent_001", entity = "minecraft:zombie")),
    )

    private fun hello(range: ProtocolRange) = HelloPayload(
        runtime = RuntimeRef(name = "probe", version = "0.1.0", lang = "kotlin"),
        protocol = range,
    )

    @Test
    fun `compatible hello yields hello_ack with environment and capabilities`() {
        val reply = handshake.onHello(requestId = "c1", body = hello(ProtocolRange("0", "0")))

        assertEquals(MessageTypes.HELLO_ACK, reply.type)
        assertEquals("c1", reply.id)
        assertEquals(ProtocolV0.CURRENT, reply.version)

        val ack = ProtocolV0.json.decodeFromJsonElement(HelloAckPayload.serializer(), reply.payload)
        assertEquals("macha-minecraft", ack.layer.name)
        assertEquals("0.1.0", ack.layer.version)
        assertEquals("0", ack.protocol)
        assertEquals("minecraft", ack.environment?.kind)
        assertEquals(listOf("minecraft:overworld"), ack.environment?.worlds)
        assertEquals(148213L, ack.time?.tick)
        assertEquals("move", ack.capabilities.single().name)
        assertEquals("agent_001", ack.agents.single().id)
    }

    @Test
    fun `incompatible hello yields error bad_version`() {
        val reply = handshake.onHello(requestId = "c1", body = hello(ProtocolRange("1", "2")))

        assertEquals(MessageTypes.ERROR, reply.type)
        assertEquals("c1", reply.id)

        val error = ProtocolV0.json.decodeFromJsonElement(ErrorPayload.serializer(), reply.payload)
        assertEquals(ErrorCode.BAD_VERSION, error.code)
        assertEquals("hello", error.where)
    }
}