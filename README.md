# Macha

**Revolutionizing game NPCs!**

Macha 是一个面向下一代游戏 NPC 的研究与工程仓库。我们的目标不是做一个“会聊天的 NPC”，而是构建具备 **长期记忆、可信反思、动态规划、多智能体协作** 的 LLM 驱动 NPC 框架。

> 当前状态：仓库初始化阶段。  
> 研究基础：`reference/` 中的四篇核心论文。

---

## 为什么叫 Macha？

Macha 代表我们想做的三件事：

- **Memory**：让 NPC 记住经历、关系和因果。
- **Architecture**：用可扩展的模块化架构替代“Prompt 堆砌”。
- **Character**：让每个 NPC 有稳定、可信、可成长的“人格”。

---

## 仓库结构

```text
Macha/
├── README.md
├── LICENSE
├── .gitignore
├── requirements.txt
├── pyproject.toml
├── reference/                 # 四篇核心论文 PDF
├── papers/                    # 团队自己撰写的论文与思想草案
├── docs/
│   ├── research/
│   │   ├── positioning.md     # 四篇论文的定位与我们的切入点
│   │   └── direction.md       # 初步技术方向与立项建议
│   ├── architecture.md        # 目标架构草图
│   └── roadmap.md             # 开发路线图
├── src/
│   └── macha/
│       ├── __init__.py
│       └── core/              # 核心模块骨架
│           ├── __init__.py
│           ├── agent.py
│           ├── memory.py
│           ├── perception.py
│           ├── reasoning.py
│           └── action.py
├── examples/
│   └── hello_agent.py
└── tests/
    └── test_smoke.py
```

---

## 快速开始（占位）

```bash
# 创建虚拟环境
python -m venv .venv
source .venv/bin/activate  # Windows: .venv\Scripts\activate

# 安装依赖
pip install -r requirements.txt

# 运行冒烟测试
pytest
```

> 具体可运行示例将在第一阶段 MVP 完成后补充。

---

## 文档导航

- [仓库初始化清单](docs/initialization.md)
- [研究定位与论文差异](docs/research/positioning.md)
- [初步技术方向](docs/research/direction.md)
- [团队信息收集清单](docs/research/information_needs.md)
- [原型画像](docs/prototype_portrait.md)
- [目标架构](docs/architecture.md)
- [开发路线图](docs/roadmap.md)

---

## License

[MIT](LICENSE)
