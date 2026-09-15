# Failures（失败与负结果归档）

> 规范：[`../../docs/research-methodology.md`](../../docs/research-methodology.md) §7。
> 目的：团队必须能随时回答——**"我们到底知道了什么不能工作？"**
> 失败是研究资产。这里的记录**不是**"未来工作"，也不是道歉。

---

## 分类（F1–F7）

| 类型 | 含义 | 性质 |
|---|---|---|
| **F1 Hypothesis Failure** | 预测没出现 → 机制可能错 | 研究资产 → 新 Question |
| **F2 Model Failure** | 预测出现，但机制解释不了别的现象 / 内部不一致 | 研究资产 |
| **F3 Implementation Failure** | 产物没按规格工作 | **工程问题，不算研究结论**（修完重跑） |
| **F4 Experimental Failure** | 设计缺陷（混淆、无 control、样本不足、事后改预测） | **作废重设计** |
| **F5 Measurement Failure** | 指标测的不是想测的东西 | 修指标；历史数字作废 |
| **F6 Generalization Failure** | 在 A 成立、在 B 不成立 | 研究资产 → 界定边界 |
| **F7 Boundary-condition Failure** | 只在特定条件成立 | **不是失败，是发现边界**——必须记录 |

**硬规则**：**F3/F4/F5 不得当作负面研究结论使用**（必须先修再进 Gate 3）；
**F1/F2/F6/F7 必须写成记录**。

## 命名

`F-NN-<slug>.md`（NN 两位序号）。**短小为准**：一页以内，六项写完就结束。

## 六项必填

```markdown
# F-NN <一句话：我们试了什么>

type: F1..F7
date: YYYY-MM-DD
related: Q-NN / Experiment / Claim

## 1. 我们试了什么
## 2. 期望什么（引用预注册块）
## 3. 实际什么（原始产物路径）
## 4. 类型判定（F1–F7 + 为什么是这一类而不是别的类）
## 5. 我们现在知道什么不能工作
## 6. 它生成了哪个 Question（或明确写"无"）
```

## 反模式

- 把失败写成"未来工作"；
- 把 F3/F4（工程/设计问题）包装成 F1（假设失败）——**这是最有害的一种**，它会把工程债伪装成科学发现；
- 失败只存在于聊天记录里、PR 评论里、或某个人的记忆里；
- 写"没有产生新问题"却也不解释为什么。

## 与其它目录的关系

- 现象来自实验：`../experiments/`（或 `../projects/` 里的工程验收，但工程验收**不进这里**）
- 生成的问题：`../questions/`
- 文献里的失败（别人的）：`../literature/07-failure-modes-negative-results.md`（**不是**本目录）
