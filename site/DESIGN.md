# site/DESIGN.md — 视觉与信息架构说明

> 本文件是 `site/` 的实现说明，随实现更新。
> 上游依据：[`research/macha-site-refactor-report/macha-site-refactor-report.html`](../research/macha-site-refactor-report/macha-site-refactor-report.html)（重构调研报告，含全部调研结论与规划）。
> 本文件不重复报告里的调研过程，只记录**已经落地的东西**与**还没落地的东西**。

---

## 1. 这是什么

`site/` 是 Macha 官网的部署源，零构建、零 CDN、零运行时依赖：打开任意 `.html` 即可运行。

它取代了旧版的三维漫游站点（Three.js + 六个场景模块 + `main.js` / `rig.js` / `content.js` / importmap）。旧站点的问题不是不好看，而是叙事框架过时：它把「认知架构四层」与「Minecraft / inZOI 两条赛道」放在中心，而这两样在随后的时间里都改变了身份。新版把叙事换成**关系缺口**，把视觉从表达性手绘换成克制冷静的近单色风格。

---

## 2. 信息架构

三层结构：主序列两页承担叙事，技术细节五页承担纵深，辅助两页承担检索与参与。

| 路径 | 文件 | 类型 | 状态 |
|---|---|---|---|
| `/` | `index.html` | 主序列 · 愿景 | 有内容 |
| `/sepmay` | `sepmay.html` | 主序列 · SEPMAY 路径 | 有内容 |
| `/architecture` | `architecture.html` | 技术细节 | 占位 |
| `/operators` | `operators.html` | 技术细节 | 占位 |
| `/drive` | `drive.html` | 技术细节 | 占位 |
| `/evaluation` | `evaluation.html` | 技术细节 | 占位 |
| `/experiments` | `experiments.html` | 技术细节 | 占位 |
| `/glossary` | `glossary.html` | 辅助 · 术语表 | 初稿 |
| `/about` | `about.html` | 辅助 · 关于与参与 | 有内容（A04/A05 待补） |

**导航**：顶部只放四项——愿景、SEPMAY、技术、论文。技术细节五页收在「技术」之下，用页内索引（`.page-index`）互链，避免导航随页面增加而膨胀。页脚列出全部九个页面，作为完整目录。

**占位页原则**：占位页不做 404，也不写「敬请期待」。每页回答三个问题——这页将回答什么问题（hero 的一句话定位）、它将包含哪些章节（结构大纲）、相关文档现在在哪里（`.doc-links` 指向仓库真实路径）。第三条让空页面依然可用。

---

## 3. 视觉令牌

近单色：白底、近黑字、一条极细的分隔线。**强调色就是正文色本身**，层级靠字号与字重建立，不靠颜色。无阴影、无渐变、无泛光。完整令牌定义在 [`assets/css/site.css`](assets/css/site.css) 顶部，以下为要点：

| 类别 | 令牌 | 值 |
|---|---|---|
| 表面 | `--bg` / `--surface` / `--surface-muted` | `#FFFFFF` / `#FAFAFA` / `#F4F4F4` |
| 分隔线 | `--rule` / `--rule-strong` | `#E6E6E6` / `#C4C4C4` |
| 文字 | `--ink` / `--ink-secondary` / `--ink-muted` | `#0D0D0D` / `#3C3C3C` / `#6B6B6B` |
| 语义（仅表示真实状态） | `--ok` / `--warn` / `--bad` | `#1A7F37` / `#9A6700` / `#B42318` |
| 间距 | `--space-1` … `--space-9` | 4 / 8 / 12 / 16 / 24 / 32 / 48 / 64 / 96 px |
| 圆角 | `--radius-sm` / `-md` / `-lg` / `-pill` | 4 / 8 / 12 / 999 px |
| 阅读栏 | `--max-narrow` / `--max-wide` | 760px / 900px |

深色模式由 `prefers-color-scheme` 覆盖同一组令牌，不新增组件样式。

**字体**（两套，自托管，Latin 部分已随站提交；CJK 走系统回退）：

- 无衬线 `Instrument Sans` —— 正文、标题。
- 等宽 `Geist Mono` —— 路径、版本号、标签、代码、`.kicker`、`caption`。

**动效**：页面上唯一会动的东西是 hover 时的 0.15s 短过渡；`prefers-reduced-motion` 下全部关闭。

---

## 4. 组件清单

样式全部在 `site.css`，页面只组合 class，不写内联样式：

- 布局：`.wrap` / `.wrap--narrow`、`main > section` 的章节节奏（96px 上间距 + 1px 顶线）
- 头部：`.site-header` / `.brand` / `.site-nav`
- 首屏：`.hero` / `.hero__lede` / `.hero__meta` / `.hero__actions` / `.btn`
- 文字块：`.section-head` / `.kicker` / `.lede`
- 表格：`.table-wrap` + `table.stackable`（窄屏转为卡片式，不依赖横向滚动条）
- 块：`.card` / `.callout` / `blockquote` / `.grid-2` / `.grid-3` / `.rowlist` / `.tag`
- 技术页专用：`.page-index`（五页互链）、`.doc-links`（指向仓库路径）
- 页脚：`.site-footer` / `.site-footer__grid` / `.site-footer__base`

---

## 5. 文案板块状态

全站 32 个板块，编号沿用调研报告。**可提取**＝仓库文档已有可直接改写的内容；**待起草**＝按结构先写一版交确认；**需你撰写**＝对外承诺性质，需项目作者定调。

### 5.1 愿景页（H01–H11）—— 已实现

| 编号 | 板块 | 状态 |
|---|---|---|
| H01–H06 | 标题、一句话主张、玩家想要什么、最小关系模型、缺口分析、架构落点 | 可提取 |
| H07 | 缺口说明段 | **需你撰写** |
| H08 | 当前状态 | 可提取 |
| H09 | 主张引用 | **需你撰写** |
| H10 | 下一步 | 可提取 |
| H11 | 页脚 | **需你撰写** |

### 5.2 SEPMAY 页（S01–S08）—— 已实现

| 编号 | 板块 | 状态 |
|---|---|---|
| S01–S08 | 标题、一句话主张、结构说明、三层不越界、已定基线、状态徽章、未定决策与解冻条件、与 Layer 的关系 | 可提取 |

### 5.3 技术细节页（T01–T05）—— 五页共用模板，已实现

T01 页面标题 · T02 一句话定位 · T03 筹备中说明 · T04 结构大纲 · T05 相关文档与参与入口。

| 页面 | 状态 | 正文来源 |
|---|---|---|
| 架构与契约 | 占位（结构已定） | `docs/architecture.md` |
| 算子空间 | 占位（结构已定） | `research/paths/01-sepmay-ivy/operator-space.md` |
| 内驱力与长期张力 | 占位（结构已定） | `research/paths/02-intrinsic-motivation/README.md` |
| 评测与一致性 | 占位（结构已定） | `docs/research-methodology.md`、`docs/prototype_portrait.md` |
| 实验赛道 | 占位（结构已定） | `announcements/`、`research/plans/minecraft-layer-validation-plan.md` |

### 5.4 辅助页（A01–A05）—— 已实现

| 编号 | 板块 | 状态 |
|---|---|---|
| A01 | 术语表标题与说明 | 待起草（已出初稿） |
| A02 | 术语条目 | 待起草（已出初稿，**口径待统一**） |
| A03 | 关于与参与标题 | 可提取 |
| A04 | 参与方式 | **需你确认** |
| A05 | 联系方式 | **需你撰写** |

### 5.5 全局（G01–G03）

| 编号 | 板块 | 状态 |
|---|---|---|
| G01 | 顶部导航（四项） | 已实现 |
| G02 | 元信息（title / description / og） | **需你确认**；当前每页已写 title 与 description，og 标签未加 |
| G03 | 语言切换 | 未实现（旧站有 i18n.js，新版暂只做中文） |

**需要项目作者定调的六块**：H07、H09、H11、A04、A05、G02。

---

## 6. 阻塞风险

1. **论文未定稿**。愿景页的主张引用（H09）与元信息（G02）最终应锚定论文正文；论文定稿前，相关文案保持可替换状态。
2. **术语口径未统一**。同一概念在仓库里存在多种写法（「玩家条件性」/「玩家依赖性」、「关系存档」/ relational save file）。`glossary.html` 已给出初稿，**定稿前全站译法以该页为准**；仓库规范文本确定口径后需同步更新全站。

---

## 7. 静态校验

改动后按以下项自查（不启动浏览器）：

- 所有 `href="./*.html"` 指向的文件存在。
- 所有 `href="./assets/*"` 与 CSS 内 `url('../fonts/*')` 指向的文件存在。
- 无遗留三维资源引用（`three` / `importmap` / `main.js` / `rig.js` / `content.js` / `scenes/`）。
- 每个技术细节页都含 `.page-index`（五页互链）与 `.doc-links`（至少一条真实仓库路径）。
- 每页 `title` 与 `meta description` 非空。