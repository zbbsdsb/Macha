# 目标架构（初稿）

## 高层视图

```text
Game Engine / Environment
        │
        ▼
┌─────────────────┐
│  Perception     │  把环境状态、玩家输入转成结构化 Observation
└────────┬────────┘
         ▼
┌─────────────────┐
│  Memory         │  短期上下文 + 长期经历 + 反思摘要
└────────┬────────┘
         ▼
┌─────────────────┐
│  Reasoning      │  目标解析、规划、决策、反思
└────────┬────────┘
         ▼
┌─────────────────┐
│  Action         │  生成对话、游戏指令或 API 调用
└─────────────────┘
```

## 核心模块职责

### Perception（感知）

- 输入：游戏状态、玩家消息、事件。
- 输出：`Observation`（结构化描述）。
- 初期可用文本模板，后期可接视觉/API。

### Memory（记忆）

- 短期记忆：当前会话上下文。
- 长期记忆：跨会话的重要事实、关系和反思。
- 检索：按相关性、新近度、重要性排序。
- 初期用 SQLite/JSON，后期可接向量检索。

### Reasoning（推理）

- 基于当前观察和记忆做决策。
- 包含规划（目标分解）和反思（从失败/成功中学习）。
- 初期可调用 LLM，也可用规则兜底。

### Action（行动）

- 把决策转换为游戏内动作或自然语言回复。
- 应支持“结构化输出”，方便游戏引擎解析。

## 接口约定（草案）

```python
@dataclass
class Observation:
    content: str
    timestamp: float
    source: str

@dataclass
class MemoryItem:
    content: str
    importance: float
    timestamp: float
    metadata: dict

class BaseAgent:
    def perceive(self, observation: Observation) -> None: ...
    def think(self) -> str: ...
    def act(self) -> str: ...
```

> 详细接口在 `src/macha/core/` 中逐步实现。
