# Macha 官网（`site/`）

Macha 官网的部署源。零构建、零 CDN、零运行时依赖——打开任意 `.html` 即可运行。

新版把叙事换成**关系缺口**，视觉换成克制冷静的近单色风格，取代了旧版的三维漫游站点。视觉与信息架构的完整说明见 [`DESIGN.md`](DESIGN.md)；上游依据是[重构调研报告](../research/macha-site-refactor-report/macha-site-refactor-report.html)。

---

## 页面

| 文件 | 页面 | 类型 | 状态 |
|---|---|---|---|
| `index.html` | 愿景 | 主序列 | 有内容 |
| `sepmay.html` | SEPMAY 路径 | 主序列 | 有内容 |
| `architecture.html` | 架构与契约 | 技术细节 | 占位（结构已定） |
| `operators.html` | 算子空间 | 技术细节 | 占位（结构已定） |
| `drive.html` | 内驱力与长期张力 | 技术细节 | 占位（结构已定） |
| `evaluation.html` | 评测与一致性 | 技术细节 | 占位（结构已定） |
| `experiments.html` | 实验赛道 | 技术细节 | 占位（结构已定） |
| `glossary.html` | 术语表 | 辅助 | 初稿（口径待统一） |
| `about.html` | 关于与参与 | 辅助 | 有内容（A04/A05 待补） |

顶部导航只有四项：愿景、SEPMAY、技术、论文。五个技术细节页由页内索引互链；页脚列出全部九页。

---

## 本地预览

任选一种：

```bash
# 1) 直接打开文件
start index.html          # Windows
open  index.html          # macOS

# 2) 起一个本地静态服务器（推荐，行为更接近线上）
python -m http.server 8000
# 然后访问 http://localhost:8000/
```

---

## 部署

`site/` 是纯静态目录，可直接托管在任意静态主机（GitHub Pages、Cloudflare Pages、Netlify、任意对象存储 + CDN）。没有构建步骤，把目录内容原样发布即可。入口文件是 `index.html`。

仓库已配置 GitHub Actions：[`.github/workflows/pages.yml`](../.github/workflows/pages.yml)。当 `site/**` 或该 workflow 自身在 `main` 上发生变更时，它会把 `site/` 目录整体作为 Pages artifact 上传并发布；也可在 Actions 页手动触发（`workflow_dispatch`）。

首次启用需要人工设置一次：仓库 **Settings → Pages → Build and deployment → Source** 选 **GitHub Actions**。之后无需再动。

站点全部使用相对路径（`./index.html`、`./assets/...`），因此发布到项目页子路径 `https://zbbsdsb.github.io/Macha/` 与自定义域名根路径都能正常工作，不需要改路径。

---

## 编辑指南

**改文案**：直接改对应 `.html` 里的正文。文案板块的编号与状态清单在 [`DESIGN.md` §5](DESIGN.md)；需要项目作者定调的六块是 H07、H09、H11、A04、A05、G02。

**改样式**：只改 [`assets/css/site.css`](assets/css/site.css) 顶部的设计令牌，不要在页面里写内联样式。令牌含义见 [`DESIGN.md` §3](DESIGN.md)。

**加页面**：复制一个技术细节页作为模板，改 `title` / `meta description` / hero，并在**所有页面的页脚**与相关页的 `.page-index` 里补上链接。

**技术细节页的模板**：每页必须回答三个问题——这页将回答什么问题（hero 的 `.hero__lede`）、它将包含哪些章节（结构大纲 `<ol>`）、相关文档在哪里（`.doc-links`，指向仓库真实路径）。占位不等于空页。

---

## 依赖

无。字体（`Instrument Sans` / `Geist Mono`，Latin 部分）自托管在 `assets/fonts/`，中文走系统字体回退。

---

## 静态校验

改完后自查（无需浏览器）：

- 所有 `href="./*.html"` 指向的文件存在。
- `assets/css/site.css` 里的字体路径 `url('../fonts/*')` 指向的文件存在。
- 无遗留三维资源引用。
- 每个技术细节页都含 `.page-index` 与至少一条 `.doc-links`。
- 每页 `title` 与 `meta description` 非空。

---

## 许可

站点内容随仓库以 [MIT License](../LICENSE) 发布；文案改写自仓库文档，随项目演进而更新。