"""Minimal example to show how the skeleton modules fit together.

This is not a working cognitive agent yet; it only demonstrates the intended flow.
"""

from macha.core.agent import Observation
from macha.core.memory import Memory, MemoryItem
from macha.core.perception import Perception
from macha.core.reasoning import Reasoning
from macha.core.action import Action


def main() -> None:
    memory = Memory()
    perception = Perception()
    reasoning = Reasoning(memory=memory)
    action = Action()

    obs = perception.process_text("Hello, do you remember me?")
    memory.add(MemoryItem(content="The player visited yesterday."))

    decision = reasoning.decide(obs.content)
    result = action.execute(decision)

    print(result.content)


if __name__ == "__main__":
    main()
