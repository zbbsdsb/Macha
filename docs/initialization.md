# 仓库初始化清单

## 1. 确认目录

```bash
cd "D:/github projects/Macha"
```

> 注意：路径中有空格，命令行中务必加引号。

## 2. 初始化 Git（如果还没有）

```bash
git init
git add .
git commit -m "chore: initialize Macha repository structure"
```

## 3. 创建远端仓库并推送

假设远端地址为 `git@github.com:your-org/Macha.git`：

```bash
git remote add origin git@github.com:your-org/Macha.git
git branch -M main
git push -u origin main
```

## 4. 安装开发环境

```bash
python -m venv .venv
# Windows:
.venv\Scripts\activate
# macOS / Linux:
source .venv/bin/activate

pip install -e ".[dev]"
```

## 5. 运行测试

```bash
pytest
```

## 6. 第一次团队对齐

- [ ] 阅读 `docs/research/positioning.md`，确认研究方向。
- [ ] 阅读 `docs/research/direction.md`，确认第一个 MVP 范围。
- [ ] 阅读 `docs/roadmap.md`，认领 Phase 1 任务。
