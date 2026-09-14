package dev.macha.layer.minecraft.adapter.action

import dev.macha.layer.protocol.ActionResultPayload
import dev.macha.layer.runtime.ActionCall

/**
 * 主线程执行分发（04 §3.4 ★）——把 runtime 发来的动作回主线程执行的唯一入口（03 §6 线程规则）。
 * TODO(scaffold): 按词表映射到 MoveAction / LookAction / InteractAction / SpawnAgentAction。
 */
class ActionExecutor {

    fun execute(call: ActionCall): ActionResultPayload {
        TODO("scaffold: action executor not wired")
    }
}