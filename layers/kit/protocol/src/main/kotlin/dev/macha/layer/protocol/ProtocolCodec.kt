package dev.macha.layer.protocol

import kotlinx.serialization.encodeToString
import kotlinx.serialization.json.Json

/** 协议 v0 编解码与版本常量（01 §5 / §6）。 */
object ProtocolV0 {
    const val CURRENT = "0"
    const val MIN = "0"
    const val MAX = "0"

    /** 严格模式：多余字段即视为 schema_violation；默认值全部写出，保证往返一致。 */
    val json: Json = Json {
        ignoreUnknownKeys = false
        explicitNulls = false
        encodeDefaults = true
    }
}

object ProtocolCodec {

    fun encode(envelope: Envelope): String = ProtocolV0.json.encodeToString(Envelope.serializer(), envelope)

    fun decode(text: String): Envelope = ProtocolV0.json.decodeFromString(Envelope.serializer(), text)

    /**
     * 版本协商（01 §6）：返回本 Layer 实际接受并采用的版本；无交集返回 null → `error(bad_version)`。
     */
    fun negotiate(range: ProtocolRange): String? {
        val cur = ProtocolV0.CURRENT
        return if (cur < range.min || cur > range.max) null else cur
    }
}