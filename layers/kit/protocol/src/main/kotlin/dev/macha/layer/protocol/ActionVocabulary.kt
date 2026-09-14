package dev.macha.layer.protocol

/**
 * 动作词表与命名空间规则（01 §4 / 原则②③，边界红线 G.1-3）。
 *
 * 无前缀动词 = 共同能力类（`move`/`look`/`interact`/`spawn_agent`）；
 * 带命名空间动词 = 环境特有（`minecraft:place_block`）。
 * Core 侧词表只允许无前缀动词；环境动词必须带前缀——此规则可自动检查。
 */
object ActionVocabulary {

    /** v0 共同能力类（01 §4 表）。 */
    val COMMON_VERBS: Set<String> = setOf("move", "look", "interact", "spawn_agent")

    /** 环境特有词必须形如 `ns:verb`，如 `minecraft:place_block`。 */
    private val NAMESPACED = Regex("^[a-z0-9_]+:[a-z0-9_.]+$")

    /** 是否共同能力类（无前缀）。 */
    fun isCommon(verb: String): Boolean = verb in COMMON_VERBS

    /** 是否环境特有（带命名空间前缀）。 */
    fun isNamespaced(verb: String): Boolean = NAMESPACED.matches(verb)

    /** 综合合法动词：共同能力类 或 带命名空间的环境词。 */
    fun isValidVerb(verb: String): Boolean = isCommon(verb) || isNamespaced(verb)
}