/**
 * Copy deck. Every string lives here, keyed by `data-i18n` in index.html.
 * Filling in an empty scene means editing ONLY this file + the matching
 * panel markup's "pending" flag — no 3D code changes.
 */

export const STRINGS = {
  // ---- boot -------------------------------------------------------------
  'boot.title': { en: 'Macha', zh: 'Macha' },
  'boot.tagline': {
    en: 'An open cognitive skeleton for game NPCs.',
    zh: '面向游戏 NPC 的开放式认知骨架。',
  },
  'boot.enter': { en: 'Enter the space', zh: '进入空间' },
  'boot.hint': {
    en: 'Drag to travel · scroll to drift · 1–6 to jump',
    zh: '拖拽移动 · 滚动漂移 · 按 1–6 直达',
  },
  'boot.webgl': {
    en: 'WebGL is unavailable — showing the text-only route.',
    zh: '当前环境不支持 WebGL，已切换为纯文本模式。',
  },

  // ---- hud --------------------------------------------------------------
  'hud.nav': { en: 'Scenes', zh: '场景' },
  'hud.prev': { en: 'Previous scene', zh: '上一场景' },
  'hud.next': { en: 'Next scene', zh: '下一场景' },
  'hud.hint': {
    en: 'Scroll or drag to travel · ← → to step · 1–6 to jump',
    zh: '滚动或拖拽移动 · ← → 逐场景 · 1–6 直达',
  },
  'hud.telemetry': { en: 'CAM', zh: '摄像机' },
  'hud.back': { en: 'Back to repo', zh: '返回仓库' },

  // ---- scene 01 · origin ------------------------------------------------
  's1.kicker': { en: 'Scene 01 — Origin', zh: '场景 01 — 起源' },
  's1.title': { en: 'Design Goals', zh: '设计目标' },
  's1.lead': {
    en: 'Macha is not an NPC that can chat. It is a standard skeleton for NPCs that remember, stay themselves, and can be tested.',
    zh: 'Macha 不是"会聊天的 NPC"，而是一套标准骨架：让 NPC 能够记住、保持自我，并且可被检验。',
  },
  's1.p1': {
    en: 'We start from the player, not from the model. What breaks immersion is rarely a weak answer — it is an NPC that forgets, contradicts itself, or has no reason to refuse.',
    zh: '我们从玩家出发，而不是从模型出发。破坏沉浸感的往往不是"答得不好"，而是 NPC 会遗忘、会自相矛盾、或者从不拒绝。',
  },
  's1.p2': {
    en: 'So the first deliverable is not a game. It is a spec, a reference implementation, and a conformance suite small enough for one or two people to finish.',
    zh: '因此第一个交付物不是游戏，而是一份规范、一份参考实现，以及一套小到一两个人就能完成的符合性测试。',
  },
  's1.p.memory': { en: 'Memory', zh: '记忆' },
  's1.p.memory.d': {
    en: 'Experiences, relationships and causality that survive across sessions.',
    zh: '跨会话存续的经验、关系与因果。',
  },
  's1.p.arch': { en: 'Architecture', zh: '架构' },
  's1.p.arch.d': {
    en: 'An extensible, modular architecture instead of piled-up prompts.',
    zh: '以可扩展的模块化架构，取代不断堆叠的提示词。',
  },
  's1.p.char': { en: 'Character', zh: '人格' },
  's1.p.char.d': {
    en: 'A stable, believable, evolving persona for every NPC.',
    zh: '让每个 NPC 拥有稳定、可信且会演化的人格。',
  },
  's1.li1': {
    en: 'Standard, not product — open, engine-agnostic and model-agnostic.',
    zh: '是标准而非产品 —— 开源、不绑定引擎、不绑定模型。',
  },
  's1.li2': {
    en: 'Measurable — memory, character consistency, latency, cost and observability are all testable.',
    zh: '可度量 —— 记忆、人格一致性、延迟、成本与可观测性都可被测试。',
  },
  's1.li3': {
    en: 'Swappable — change the model or the memory backend and the conformance tests still pass.',
    zh: '可替换 —— 换模型或换记忆后端，符合性测试依然通过。',
  },
  's1.li4': {
    en: 'Finishable — 1–2 developers, a few weeks, no engine plugin required.',
    zh: '可完成 —— 1–2 名开发者、数周时间，无需任何引擎插件。',
  },

  // ---- scene 02 · horizon ----------------------------------------------
  's2.kicker': { en: 'Scene 02 — Horizon', zh: '场景 02 — 地平线' },
  's2.title': { en: 'Industry Goals & Vision', zh: '行业目标与愿景' },
  's2.lead': {
    en: 'Redefine the relationship between player, NPC and world — and make that definition public.',
    zh: '重新定义玩家、NPC 与世界之间的关系，并让这个定义保持公开。',
  },
  's2.p1': {
    en: 'Today every studio re-invents NPC cognition from scratch. There is no shared vocabulary for what a game agent is, and no shared way to prove one works.',
    zh: '如今每个工作室都在从零重造 NPC 认知。行业既没有关于"游戏智能体是什么"的共同语汇，也没有证明它可用的共同方法。',
  },
  's2.p2': {
    en: 'Macha aims to be that vocabulary: a thin, open standard that any engine and any model can implement, with evidence published in the open.',
    zh: 'Macha 想成为这套语汇：一层任何引擎、任何模型都能实现的轻量开放标准，并把证据公开出来。',
  },
  's2.li1': {
    en: 'A shared vocabulary: what a game agent is, and what it must guarantee.',
    zh: '共同语汇：游戏智能体是什么，以及它必须保证什么。',
  },
  's2.li2': {
    en: 'A semi-permeable membrane: the world shapes the NPC, the NPC keeps its own interpretation.',
    zh: '半透膜：世界可以影响 NPC，NPC 保留自己的解读。',
  },
  's2.li3': {
    en: 'One standard, many worlds — the same interfaces across engines and models.',
    zh: '一套标准，诸多世界 —— 跨引擎、跨模型的同一套接口。',
  },
  's2.li4': {
    en: 'Public evidence: experiments, results and failures published in the open.',
    zh: '公开证据：实验、结果与失败全部公开。',
  },
  's2.quote': {
    en: 'We are not trying to prove we can build a complex world. We are trying to prove what kind of relationship should exist between a player and an NPC — and why existing technology has never satisfied it.',
    zh: '我们要证明的不是"我们能造出复杂的世界"，而是"玩家与 NPC 之间本应存在什么样的关系，以及既有技术为何始终没能满足它"。',
  },
  's2.quote.by': { en: 'Macha Team', zh: 'Macha 团队' },

  // ---- scene 03 · core --------------------------------------------------
  's3.kicker': { en: 'Scene 03 — Core', zh: '场景 03 — 内核' },
  's3.title': { en: 'Core Architecture', zh: '核心架构' },
  's3.lead': {
    en: 'Perception, Memory, Reasoning, Action — four layers, one contract.',
    zh: '感知、记忆、推理、行动 —— 四层结构，一份契约。',
  },

  // ---- scene 04 · descent ----------------------------------------------
  's4.kicker': { en: 'Scene 04 — Descent', zh: '场景 04 — 下沉' },
  's4.title': { en: 'Deep Dive', zh: '深度解析' },
  's4.lead': {
    en: 'Field superposition, mental LOD, and the removal test.',
    zh: '场叠加、心智 LOD，以及移除测试。',
  },

  // ---- scene 05 · field -------------------------------------------------
  's5.kicker': { en: 'Scene 05 — Field', zh: '场景 05 — 试验场' },
  's5.title': { en: 'Application Plan', zh: '应用计划' },
  's5.lead': {
    en: 'Where Macha gets tested. Three slots are open.',
    zh: 'Macha 的落点。三个位置仍然空着。',
  },

  // ---- scene 06 · archive -----------------------------------------------
  's6.kicker': { en: 'Scene 06 — Archive', zh: '场景 06 — 档案馆' },
  's6.title': { en: 'Glossary', zh: '术语表' },
  's6.lead': {
    en: 'Every term Macha defines, in one ring.',
    zh: 'Macha 定义的每一个术语，都在这座环里。',
  },

  // ---- shared -----------------------------------------------------------
  'pending.badge': { en: 'Content in preparation', zh: '内容筹备中' },
  'pending.body': {
    en: 'This scene is staged and ready. The writing is still in review — the structure below shows what will land here.',
    zh: '本场景的舞台已经搭好。文案仍在审校 —— 下面的结构即为此处将要呈现的内容。',
  },
  'pending.cta': { en: 'Help write this scene', zh: '参与撰写本场景' },
  'stack.label': { en: 'Structure', zh: '结构' },
  'scroll.label': { en: 'Travel', zh: '移动' },
};

/** Structural chips shown on the pending scenes — the "stage is ready" signal. */
export const STACKS = {
  core: [
    { k: 'Perception', en: 'Environment → Observation', zh: '环境 → 观察' },
    { k: 'Memory', en: 'Short-term / long-term / retrieval', zh: '短期 / 长期 / 检索' },
    { k: 'Reasoning', en: 'Planning + reflection', zh: '规划 + 反思' },
    { k: 'Action', en: 'Structured ActionCall', zh: '结构化 ActionCall' },
  ],
  descent: [
    { k: 'Field superposition', en: 'Same event, different standpoints', zh: '同一事件，不同立场' },
    { k: 'Mental LOD', en: 'How much mind a role needs', zh: '一个角色需要多少"心智"' },
    { k: 'Removal test', en: 'Does removing the AI break the game?', zh: '拿掉 AI，游戏是否还成立？' },
    { k: 'Dramatic realism', en: 'Believable, not accurate', zh: '可信，而非精确' },
  ],
  field: [
    { k: 'Slot 01', en: 'Open — call for a testbed', zh: '空缺 — 征集试验环境' },
    { k: 'Slot 02', en: 'Open — call for a testbed', zh: '空缺 — 征集试验环境' },
    { k: 'Slot 03', en: 'Open — call for a testbed', zh: '空缺 — 征集试验环境' },
  ],
  archive: [
    { k: 'Observation', en: 'Structured view of the world', zh: '对世界的结构化观察' },
    { k: 'MemoryItem', en: 'Content + importance + provenance', zh: '内容 + 重要性 + 来源' },
    { k: 'ActionCall', en: 'Tool + args + provenance', zh: '工具 + 参数 + 来源' },
    { k: 'Guardrail', en: 'Input / output / persona checks', zh: '输入 / 输出 / 人格校验' },
  ],
};

/** Right-rail scene labels. */
export const NAV_LABELS = [
  { en: 'Design Goals', zh: '设计目标' },
  { en: 'Industry Vision', zh: '行业愿景' },
  { en: 'Core Architecture', zh: '核心架构' },
  { en: 'Deep Dive', zh: '深度解析' },
  { en: 'Application Plan', zh: '应用计划' },
  { en: 'Glossary', zh: '术语表' },
];
