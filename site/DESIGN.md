# Macha Site — 3D Camera Space Design

> 站点形态：**一个连续的三维空间**。用户的视角就是一台摄像机，沿一条飞行路径在 6 个"场景舞台"之间穿梭。
> 每个场景 = 一种视觉风格 + 一段叙事。场景之间没有页面跳转，只有雾、光、曝光与几何体的连续插值。

---

## 1. 核心体验定义

| 维度 | 定义 |
|---|---|
| 视角 | 用户 = 一台摄像机。位置由路径驱动，朝向由"焦点插值"驱动；鼠标提供 ±2° 的视差偏移（呼吸感） |
| 移动 | 连续量 `p ∈ [0, 5]`（0.0 = 场景 1 中心，1.0 = 场景 2 中心…）。整数=停靠，小数=在途中 |
| 转场 | 不做"切场景"。全局只有**一套**雾/半球光/主光/曝光，在相邻场景的 `env` 之间做 smoothstep 插值 —— 这是丝滑感的唯一来源 |
| 进入 | 启动遮罩 → 点击 Enter → 相机从 `p = -0.45` 缓入到 `p = 0`（1.6s 阻尼滑行） |

### 为什么这样设计

- **单雾单光** 避免了"场景 A 的天空盒突然变成场景 B"的硬切。所有过渡都是数值插值，天然连续。
- **路径保证对齐**：用分段 Catmull-Rom（而非全局曲线）保证 `p = i` 时相机精确落在第 i 个锚点，不会出现"停歪了"。
- **几何体淡入淡出**：每个场景有 `reveal = smoothstep(1 - |p - i| / 1.15)`，控制材质透明度/自发光/缩放。相邻场景在 `p = i+0.5` 时各占 ~56%，形成交叉溶解。

---

## 2. 场景清单与视觉母题

| # | 场景 | 内容状态 | 视觉母题 | 配色（accent / fog→bg） |
|---|---|---|---|---|
| 01 | **Origin** — Macha 的设计目标 | ✅ 可写 | 记忆图谱：球体分布的节点 + 连线，中心三枚旋转光环 = M/A/C | `#6EE7F9` 青 / 深靛 `0x070B1A` |
| 02 | **Horizon** — 行业目标与愿景 | ✅ 可写 | 地平线 + 远景巨石群（诸世界）+ 低垂的日出盘 + 连接诸世界的丝线 | `#FFB37A` 琥珀 / 暖石板 `0x120E14` |
| 03 | **Core** — Macha 核心架构 | ⬜ 空（舞台已搭） | 四层同心圆盘 Perception→Memory→Reasoning→Action，粒子沿轴向上流动 | `#7CF5C4` 翡翠 / 石墨 `0x08100E` |
| 04 | **Descent** — Deep Dive | ⬜ 空（舞台已搭） | 下行隧道：层层套环 + 叠加的半透明"场"（场叠加/干涉纹） | `#B69CFF` 紫罗兰 / 近黑 `0x0A0713` |
| 05 | **Field** — 应用计划 | ⬜ 空（舞台已搭） | 网格大地 + 3 座空置基座（等待实验世界落位）+ 悬浮标记与虚线 | `#A3E635` 青柠 / 夜绿 `0x0A1206` |
| 06 | **Archive** — 术语表 | ⬜ 空（舞台已搭） | 环形卡片档案馆：环绕相机的巨石卡册 + 尘埃微粒缓慢上浮 | `#E8D9B5` 羊皮纸 / 暗褐 `0x0E0B08` |

### 空场景的统一处理

四个"先空着"的场景不是留白，而是**可辨识的"舞台已就位"状态**：

- 3D 骨架完整运行（该有的几何、粒子、光照全都在）
- DOM 面板显示 `Content in preparation / 内容筹备中` + 该场景的结构化占位（如 Core 的四层芯片、Archive 的空卡片）
- 底部统一 CTA：`Help write this — open an issue`
- 填文案时只需改 `assets/js/content.js` 的一段数据，场景不需要动一行

---

## 3. 技术架构

```
site/
├── index.html                  # 静态 HTML（含 EN 全文，利于 SEO / 无 JS 可读）
├── DESIGN.md                   # 本文档
└── assets/
    ├── css/site.css
    └── js/
        ├── main.js             # 渲染器 / 主循环 / 输入 / env 插值 / DOM 联动
        ├── rig.js              # 分段 Catmull-Rom 相机路径 + 阻尼
        ├── i18n.js             # EN ⇄ ZH 切换（data-i18n 扫描）
        ├── content.js          # 文案字典 + 动态列表数据（术语 / 实验赛道）
        └── scenes/
            ├── index.js        # 场景注册表
            ├── _helpers.js     # 共用几何工具（星野 / 网格 / 粒子带）
            └── 0x-*.js         # 每个场景独立模块
```

### 关键模块契约

```js
// 每个场景模块导出：
export default function create({ quality, reducedMotion }) {
  return {
    group,                       // THREE.Group，已定位到自己的世界坐标
    focus,                       // THREE.Vector3，相机停靠时看向的点
    env: { bg, fog, fogDensity, hemiSky, hemiGround, hemi, key, keyIntensity, exposure, accent },
    update(dt, elapsed, reveal), // reveal ∈ [0,1]
    dispose()
  };
}
```

`main.js` 在每帧：
1. `p` 阻尼趋近 `target`
2. 相机位置 = `rig.positionAt(p)` + 鼠标视差偏移
3. 相机朝向 = `lerp(focus[i], focus[i+1], smoothstep(f))`
4. `env = lerpEnv(env[i], env[i+1], smoothstep(f))` → 写入雾 / 光 / 曝光 / HUD 强调色
5. 每个场景 `update(dt, t, reveal_i)`，并同步 DOM 面板的 opacity / translate

### 依赖与部署

- **零构建**：ESM + importmap，Three.js 走 jsDelivr CDN
- **Bloom 可选**：动态 `import()` 后处理，失败或低端设备自动降级为直出渲染
- GitHub Pages：`Settings → Pages → Deploy from branch → /site` 即可

---

## 4. 交互

| 输入 | 行为 |
|---|---|
| 滚轮 / 触控板 | 连续推进 `p`（可停在两场景之间） |
| 拖拽 / 触摸滑动 | 同上（移动端主输入） |
| `↑ ↓ ← →` / `Space` / `PgUp PgDn` | 整场景步进 |
| `1`–`6` | 直达第 N 场景 |
| 右侧导航点 | 直达 + hover 显示场景名 |
| 鼠标移动 | 视差（reduced-motion 时关闭） |
| EN / 中文 | 右上角切换，`localStorage` 记忆 |

导航辅助：顶部进度条、右侧点轨、**左下角摄像机遥测 HUD**（POS / FOV / 实时帧率）—— 强化"你就是一台摄像机"的设定。

---

## 5. 性能预算

| 项 | 目标 |
|---|---|
| 首屏可交互 | < 1.5s |
| 帧率 | 60fps（DPR 上限 2，移动端自动降粒子数） |
| Draw call | 每场景 ≤ 12（大量使用 Points / InstancedMesh / LineSegments） |
| 降级 | WebGL 不可用 → 纯 CSS 渐变 + 静态 DOM 全文；`prefers-reduced-motion` → 关闭视差与旋转 |

---

## 6. 后续可挂载点

- Core 场景：接入 `docs/architecture.md` 的四层，做成可点击展开的立体剖面
- Deep Dive：接入 `papers/notes/` 的场叠加 / Mental LOD，用着色器做真正的干涉纹
- Field：填入 Minecraft / inZOI 两条已公开赛道（数据驱动，加一条即可）
- Archive：接入术语表 markdown，自动生成卡片环

---

## 7. 验收记录 · 2026-09-06

首版交付后用无头 Chromium 对六个场景逐一截图复查，发现并修复：

| # | 缺陷 | 根因 | 修复 |
|---|---|---|---|
| P0 | 站点完全黑屏，boot 遮罩永不消失 | `layoutStages()` 引用了不存在的 `st.group`（应为 `st.api.group`），`boot()` 抛异常，事件监听器全部未挂载 | 改为 `st.api.group`；`boot()` 外层加 try/catch，失败时降级到纯文本路由，不再留下死黑屏 |
| P1 | 右侧场景导航压在正文上 | rail 展开标签 `max-width:12rem`，与面板 padding-right 冲突 | 面板 `padding-right` 提到 `9.5rem`；标签展开时加毛玻璃底色 |
| P1 | 场景 02（Horizon）几乎全黑 | `FogExp2` 密度 0.019，而太阳在 109 单位外（雾化 99%） | 密度降到 0.0088，太阳从 -95 移到 -62，石柱半径收紧 |
| P1 | 跨场景时旧文案以 ~8% 透明度叠在新文案下，读作重影 | 面板与 3D 用同一条 reveal 曲线 | 文案改用更陡的窗口 `smoothstep((reveal-0.42)/0.4)`，旧文案先消失、新文案后出现 |
| P2 | 场景 03 的四层板糊成一团，粒子柱像一块板 | 相机与堆叠中段齐平，层板半径 11 超出视锥 | 整体缩放（半径 6.6、step 3.6），雾密度降低，粒子减量 |
| P2 | 场景 06 卡片环一半在相机身后，画面空 | 环半径 17 > 相机到中心距离 14 | 半径改 10.5，卡片全部落在相机前方；提灯辉光减半 |
| P2 | 移动端进入场景时标题在可视区外 | 面板 `justify-content: flex-end` | 改为 `flex-start` |

**方法论教训**：首版是在从未渲染的情况下交付的。此后所有 3D 改动必须先跑无头截图再汇报。
