package dev.macha.layer.transport

import dev.macha.layer.protocol.AgentRef
import dev.macha.layer.protocol.Capability
import dev.macha.layer.protocol.EnvironmentInfo
import dev.macha.layer.protocol.Envelope
import dev.macha.layer.protocol.ErrorCode
import dev.macha.layer.protocol.ErrorPayload
import dev.macha.layer.protocol.HelloAckPayload
import dev.macha.layer.protocol.HelloPayload
import dev.macha.layer.protocol.LayerRef
import dev.macha.layer.protocol.MessageTypes
import dev.macha.layer.protocol.ProtocolCodec
import dev.macha.layer.protocol.ProtocolRange
import dev.macha.layer.protocol.ProtocolV0
import dev.macha.layer.protocol.WorldTimeRef
import kotlinx.serialization.json.encodeToJsonElement

/**
 * 会话握手（04 §3.3）：hello / hello_ack 与版本协商。
 *
 * 环境相关字段（environment/time/capabilities/agents）由环境适配器注入，
 * transport 不认识具体环境；当版本无交集时回 `error(bad_version)`（01 §6）。
 */
class SessionHandshake(
    private val layerName: String,
    private val layerVersion: String,
    private val environment: EnvironmentInfo,
    private val time: WorldTimeRef,
    private val capabilities: List<Capability>,
    private val agents: List<AgentRef> = emptyList(),
) {

    /** 版本协商：返回采纳版本；null = 不兼容。 */
    fun negotiate(range: ProtocolRange): String? = ProtocolCodec.negotiate(range)

    /**
     * 处理一条入站 `hello`（01 §3.1/§3.2）。
     *
     * 兼容 → `hello_ack`；无交集 → `error(bad_version)`。回包沿用原 hello 的 `id`（便于关联）、
     * 使用新 `ts`（发送方本地 wall clock）。
     */
    fun onHello(requestId: String?, body: HelloPayload): Envelope {
        val version = ProtocolCodec.negotiate(body.protocol)
        if (version == null) {
            val error = ErrorPayload(
                code = ErrorCode.BAD_VERSION,
                message = "protocol ${body.protocol.min}..${body.protocol.max} has no overlap with v${ProtocolV0.CURRENT}",
                where = "hello",
            )
            return errorEnvelope(requestId, error)
        }

        val ack = HelloAckPayload(
            layer = LayerRef(name = layerName, version = layerVersion),
            protocol = version,
            environment = environment,
            time = time,
            capabilities = capabilities,
            agents = agents,
        )
        return Envelope(
            version = ProtocolV0.CURRENT,
            type = MessageTypes.HELLO_ACK,
            id = requestId,
            ts = System.currentTimeMillis(),
            payload = ProtocolV0.json.encodeToJsonElement(HelloAckPayload.serializer(), ack),
        )
    }

    private fun errorEnvelope(requestId: String?, error: ErrorPayload): Envelope =
        Envelope(
            version = ProtocolV0.CURRENT,
            type = MessageTypes.ERROR,
            id = requestId,
            ts = System.currentTimeMillis(),
            payload = ProtocolV0.json.encodeToJsonElement(ErrorPayload.serializer(), error),
        )
}