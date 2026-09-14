package dev.macha.layer.runtime

import dev.macha.layer.protocol.ActionResultPayload
import dev.macha.layer.protocol.ActionStatus
import dev.macha.layer.protocol.ActionVocabulary
import dev.macha.layer.protocol.Capability
import dev.macha.layer.protocol.RefusalReason

/**
 * 动作校验（04 §3.2 ★）：能力存在性 + 词表 → 产生 `refused`（含 reason）。
 *
 * 这是边界红线 G.1-3 的落点：未声明的能力（含未登记的 `minecraft:*`）一律 `refused(not_supported)`，
 * **不是** error。
 */
class ActionValidator(
    private val capabilities: List<Capability>,
) {

    /** 返回 null 表示校验通过可执行；否则返回 refused 结果。 */
    fun validate(call: ActionCall): ActionResultPayload? {
        val verb = call.action

        if (!ActionVocabulary.isValidVerb(verb)) {
            return refused(RefusalReason.NOT_SUPPORTED, "verb '$verb' is not a valid verb")
        }

        val capability = capabilities.firstOrNull { it.name == verb }
            ?: return refused(RefusalReason.NOT_SUPPORTED, "capability '$verb' not declared by this layer")

        // v0：前置条件校验留待真实环境动作时实现；scaffold 阶段能力声明即视为可用。
        @Suppress("UNUSED_VARIABLE")
        val preconditions = capability.preconditions

        return null
    }

    private fun refused(reason: String, detail: String) =
        ActionResultPayload(status = ActionStatus.REFUSED, reason = reason, detail = detail)
}