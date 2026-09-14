package dev.macha.layer.transport

import dev.macha.layer.protocol.ProtocolCodec
import dev.macha.layer.protocol.ProtocolRange

/**
 * 会话握手（04 §3.3）：hello / hello_ack 与版本协商。
 * 版本无交集时应由上层回 `error(bad_version)` 并断开（01 §6）。
 */
class SessionHandshake {

    /** 返回协商采用的版本；null 表示不兼容（→ bad_version）。 */
    fun negotiate(range: ProtocolRange): String? = ProtocolCodec.negotiate(range)
}