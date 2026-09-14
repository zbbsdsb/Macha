package dev.macha.layer.runtime

import dev.macha.layer.protocol.ActionResultPayload
import dev.macha.layer.protocol.ActionStatus
import dev.macha.layer.protocol.Capability
import dev.macha.layer.protocol.EventPayload
import dev.macha.layer.protocol.ObservationPayload
import dev.macha.layer.runtime.port.EnvironmentPort
import kotlin.test.Test
import kotlin.test.assertEquals

/** 派发与结果关联：合法动作 → 环境执行 → ok；未声明 → refused。 */
class DispatchOrderTest {

    private fun fakeEnv(result: ActionResultPayload) = object : EnvironmentPort {
        override fun collectObservation(agentId: String): ObservationPayload? = null
        override fun execute(call: ActionCall): ActionResultPayload = result
        override fun onEvent(handler: EnvironmentPort.EventHandler) {}
    }

    @Test
    fun `valid action dispatches to environment and returns ok`() {
        val runtime = LayerRuntime(
            environment = fakeEnv(ActionResultPayload(status = ActionStatus.OK)),
            capabilities = listOf(Capability(name = "move")),
        )
        val result = runtime.onAction(ActionCall(agent = "a1", action = "move"))
        assertEquals(ActionStatus.OK, result.status)
    }

    @Test
    fun `undeclared action is refused without touching environment`() {
        val runtime = LayerRuntime(
            environment = fakeEnv(ActionResultPayload(status = ActionStatus.OK)),
            capabilities = emptyList(),
        )
        val result = runtime.onAction(ActionCall(agent = "a1", action = "jump"))
        assertEquals(ActionStatus.REFUSED, result.status)
        assertEquals("not_supported", result.reason)
    }
}