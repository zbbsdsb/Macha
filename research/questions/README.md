# Questions（研究问题）

> 规范：[`../../docs/research-methodology.md`](../../docs/research-methodology.md)。
> 规则：**一个问题一个文件**；第一行是状态；末尾是 append-only 状态历史。
> 目的：任何人进入 repo，**30 秒内知道某个问题现在处于什么状态**。

---

## 什么时候在这里建文件

只在通过 **Gate 1（Question Gate）** 之后：

1. 它**反直觉或有冲突**（与现有 claim / 常识 / 另一个结果矛盾），或
2. 回答它会**改变设计或主张**，或
3. 它**可被判定**（存在能给出"是/否/方向"的观测）。

三条缺一 → 先记到 `../scratch/` 的观察笔记，**不要**升为 Question。

**不在这里放**：工程验收（8 步 vertical slice、V1–V5 之类）→ 那是 `../projects/`；
候选架构路线 → 那是 `../paths/`；文献证据 → 那是 `../literature/`。

## 命名与状态

- 文件名：`Q-NN-<slug>.md`（NN 两位序号）。
- 第一行状态（**只能取这些值**）：

```text
observed → questioned → pre-registered → tested → supported │ weakened │ falsified
                                                      ↓
                                          revised │ abandoned │ promoted
```

## 模板（复制即用，≈12 行，10 分钟内可写完）

```markdown
# Q-NN <一句话问句>

status: questioned          # 见上表；与证据同一次提交更新
owner: <name>
opened: YYYY-MM-DD
related: <paper section / claim / path / project>

## 1. Observation（触发它的现象 + 来源）
## 2. Question（可判定的一句话）
- 若答案是"是/否"，会改变什么：
- 已知文献是否已回答（链接 dossier 或 "no"）：
## 3. Hypotheses（≥2 个互相竞争；每个必须有机制 + 预测 + falsifier）
- H1 机制 … → 预测 … ｜ falsifier: …
- H2 机制 … → 预测 … ｜ falsifier: …
## 4. Pre-registration（**提交后不得修改**）
```yaml
prereg: <commit hash>
experiment: …
env: …
baseline: …        control: …
metrics: <计算脚本路径>
expected: <方向 + 量级>
falsification: <什么结果杀死哪个假设>
```
## 5. Experiments（链接 + 产物路径）
## 6. Evidence（等级 E0–E3 + provenance + 可重跑命令）
## 7. Failures（链接 ../failures/）
## 8. Status history（append-only：日期 · 状态 · 依据 · commit）
## 9. Next questions
```

## 探索性实验的合法通道

如果你**还不知道该问什么**，就先做探索：把结果记成 **E0**，并在文件里标注 `exploratory`。
**E0 永久不得升级为 claim**——但它可以生成一个正式的 Question（这是它唯一的用途）。

## 与 Gate 的关系

- Gate 1：问题值不值得问（进本目录前）
- Gate 2：预注册是否已提交（本目录文件的 `prereg:` 字段）
- Gate 3：结果与预测的对照是否明确（更新状态）
- Gate 4：claim 是否超过证据等级（→ `papers/notes/`）
