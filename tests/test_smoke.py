from macha.core.memory import Memory, MemoryItem


def test_memory_add_and_retrieve() -> None:
    memory = Memory()
    memory.add(MemoryItem(content="hello", importance=0.8))
    assert len(memory.all()) == 1
    assert memory.retrieve("hello")[0].content == "hello"
