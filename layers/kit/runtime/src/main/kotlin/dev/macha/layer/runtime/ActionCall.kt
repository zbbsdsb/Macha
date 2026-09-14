package dev.macha.layer.runtime

import dev.macha.layer.protocol.ActionPayload
import dev.macha.layer.protocol.Provenance
import kotlinx.serialization.json.JsonElement

/**
 * 一次动作调用（Runtime → Layer），已从协议信封解码、与传输解耦。
 *
 * `args` 承接协议侧 `ActionPayload.args` 的不透明 JSON（`Map<String, JsonElement>`），
 * **无损**保留数组（`move{target:[20,64,-3]}`）与嵌套对象（`interact{target:{id:...}}`）。
 * Minecraft 适配器取参数时直接消费 [JsonElement]，不需要再 parse 字符串（F1）。
 * 具体动词的参数形状由 [dev.macha.layer.protocol.ActionVocabulary]/Capability 约定。
 */
data class ActionCall(
    val agent: String,
    val action: String,
    val args: Map<String, JsonElement> = emptyMap(),
    val provenance: Provenance? = null,
) {
    companion object {
        /** 协议 `action` 负载 → 运行时动作调用。字段与类型一对一映射，保证保真。 */
        fun from(payload: ActionPayload): ActionCall = ActionCall(
            agent = payload.agent,
            action = payload.action,
            args = payload.args,
            provenance = payload.provenance,
        )
    }
}