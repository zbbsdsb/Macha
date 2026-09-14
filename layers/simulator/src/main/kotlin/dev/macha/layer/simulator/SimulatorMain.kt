package dev.macha.layer.simulator

import dev.macha.layer.protocol.ProtocolV0

/** 独立进程入口（04 §3.5）：打印协议 v0 版本，便于交叉验证。 */
fun main() {
    println("Macha Layer Simulator — protocol v${ProtocolV0.CURRENT}")
}