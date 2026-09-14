package dev.macha.layer.protocol

import kotlin.test.Test
import kotlin.test.assertFalse
import kotlin.test.assertTrue

/**
 * 词表规则（01 §4）：`place_block` 等环境动词**不得**通过通用词校验；
 * 只有带命名空间前缀（`minecraft:place_block`）才是合法的环境动词。
 */
class VocabularyRuleTest {

    @Test
    fun `common verbs pass common check`() {
        for (verb in setOf("move", "look", "interact", "spawn_agent")) {
            assertTrue(ActionVocabulary.isCommon(verb), "expected common: $verb")
        }
    }

    @Test
    fun `environment verbs must NOT pass common check`() {
        for (verb in listOf("place_block", "break_block", "craft", "attack", "minecraft:place_block")) {
            assertFalse(ActionVocabulary.isCommon(verb), "must not be common: $verb")
        }
    }

    @Test
    fun `namespaced environment verb is valid`() {
        assertTrue(ActionVocabulary.isNamespaced("minecraft:place_block"))
    }

    @Test
    fun `bare environment verb without namespace is invalid`() {
        // 未带命名空间的环境动词既不是共同能力类、也不带前缀 → 非法
        assertFalse(ActionVocabulary.isValidVerb("place_block"))
        assertTrue(ActionVocabulary.isValidVerb("minecraft:place_block"))
    }
}