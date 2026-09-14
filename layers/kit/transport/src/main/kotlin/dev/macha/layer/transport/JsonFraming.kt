package dev.macha.layer.transport

import dev.macha.layer.protocol.Envelope
import dev.macha.layer.protocol.ProtocolCodec

/**
 * 文本帧编解码（04 §3.3）：唯一知道"消息以 JSON 文本传输"的地方。
 * 语义与传输解耦（01 原则①）：换 HTTP/gRPC/IPC 时仅此层变化。
 */
object JsonFraming {
    const val DELIMITER = '\n'

    /** 编码为一帧文本（以换行结尾）。 */
    fun encode(envelope: Envelope): String = ProtocolCodec.encode(envelope) + DELIMITER

    /** 解码一帧文本。 */
    fun decodeFrame(text: String): Envelope = ProtocolCodec.decode(text.trim())
}