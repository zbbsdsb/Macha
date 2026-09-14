package dev.macha.layer.transport

import dev.macha.layer.protocol.Envelope

/** 传输服务器接口（04 §3.3 ★）：start/stop/onMessage/send。 */
interface TransportServer {

    fun start()

    fun stop()

    /** 把一条消息发给所有已连接的会话（或按订阅过滤）。 */
    fun send(envelope: Envelope)

    /** 注册入站消息回调（已解码为信封）。 */
    fun onMessage(handler: (Envelope) -> Unit)
}