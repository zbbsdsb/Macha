# Scaffold Review — 2026-09-14（团队开工后的结构与边界检查）

> **STATUS: PENDING — 评审记录。** 对象：团队在 `layers/` 落下的第一批骨架代码。
> 方法：读 `settings.gradle.kts` / `libs.versions.toml` / 各模块 `build.gradle.kts` /
> `plugin.yml` / `layers/.gitignore` / 全部 `.kt` 文件，并核对 `04-project-structure.md` 与
> `01-protocol-v0.md`。**未执行 Gradle 构建**（需 JDK 25 与网络），以下"通过"结论由源码静态推断。

---

## 1. 通过项（与计划一致）

| 检查 | 结果 |
|---|---|
| 构建根位置 | `layers/` 单构建根，仓库根无 Gradle 文件 ✓ |
| 模块划分 | 6 模块齐全（protocol/runtime/transport/minecraft/simulator/testclient）✓ |
| 依赖方向 | `:runtime` 不依赖 `:transport` ✓；`:simulator`、`:testclient` 无 `paper-api` ✓ |
| `paper-api` 范围 | 仅 `minecraft/build.gradle.kts` 且为 `compileOnly` ✓ |
| 包名 | 统一 `dev.macha.layer.*` ✓ |
| 文件清单 | protocol 8 类 + 3 测试、runtime 8 类 + `port/`、transport 6 类，与 `04` §3 对应 ✓ |
| 边界守护 | `verifyPaperScope` / `verifyEnvClean` / `verifyCoreClean` 已注册并聚合到根 `check` ✓ |
| 版本锁定 | wrapper 9.7.1、Kotlin 2.4.20、`jvmToolchain(25)`、Java-WebSocket 1.6.0 ✓ |
| paper-api 坐标 | `26.2.build.123-stable` 已在 PaperMC Maven 元数据中核实存在，且与 server pin 的 build 123 对齐 ✓ |
| `plugin.yml` | `main` 指向 `plugin.MachaMinecraftPlugin`；`load: POSTWORLD`（需要世界）合理 ✓ |

## 2. 发现（按严重度）

### F1 ★ 参数模型不一致（`runtime/ActionCall.args`）

`runtime/.../ActionCall.kt`：

```kotlin
val args: Map<String, String> = emptyMap()
```

而协议侧 `protocol/.../Payloads.kt`：

```kotlin
val args: Map<String, JsonElement> = emptyMap()
```

后果：`move{target:[20,64,-3]}` 这类数组参数、`interact{target:{id:...}}` 这类嵌套对象**装不进去**；
若靠"字符串化后再解析"，等于凭空多出一套未写下来的转换规则，正是 `01` §8 与 `00` §G.1-3 要防的
协议漂移。建议二选一：

- 直接复用 `Map<String, JsonElement>`；或
- 定义显式 `ActionArgs` 值类型 + 文档化的编解码 + **往返测试**（`docs → runtime → adapter` 保真）。

判据：Minecraft 适配器拿到参数时**不需要自己 parse 字符串**。

### F2 `layers/.kotlin/` 未忽略

`layers/.kotlin/sessions` 实测**未被** `.gitignore` 覆盖（`build/`、`.gradle/`、`run/` 已正确忽略）。

准确表述：该目录**目前是空的**，所以此刻 `git add layers/` 不会带进垃圾；但 Kotlin 只要跑过一次构建
就会往里写缓存，届时会被提交。因此在 `layers/.gitignore` 补一行 `.kotlin/`——成本一行，优先级低但确定。

### F3 `gradle.properties` 注释与配置不符

注释写"严格校验插件/依赖，保证可复现（离线一致性优先）"，实际只有 `org.gradle.warning.mode=all`
——它是告警等级，不是依赖校验。`03` §2 要求的是 **dependency verification / lockfile**。
要么补上验证或 lockfile，要么把注释改成实情。（另：`org.gradle.daemon=false` 会显著拖慢日常构建，
若非 CI 专用建议重议。）

### F4 `api(project(...))` 用法偏宽

除 `:kit:protocol`（其公共 API 本身就是协议类型，用 `api` 合理）外，`:minecraft`、`:simulator`、
`:testclient` 建议改 `implementation`，避免把协议 API 传递性地暴露给消费者——目前无人消费，
但会把依赖图的语义搞糊，将来拆仓时更难判断真实边界。

### F5 空模块与缺失子包

- `simulator/`、`testclient/` 尚无任何 `.kt`（目录为空，git 不会记录 → 克隆后消失）；
- `minecraft/adapter/` 目前只有 `PaperEnvironmentPort.kt`，缺 `04` §3.4 的
  `agent/`、`observe/`、`events/`、`action/` 四个子包。

属早期正常现象。提醒：**空目录不会进版本库**，要么尽快落文件，要么先不建。

### F6 `stripComments` 处理不了跨行块注释

`layers/build.gradle.kts` 的边界守护用逐行正则剔除注释，多行 KDoc 里若出现 `World` / `Material`
会**误报**违规。建议改成带"是否处于块注释中"状态的扫描（按文件整体遍历、保留行号映射）。

## 3. 仓库状态

- 团队已提交 `c8a0cac "Add Layer-first architecture and hiring docs"`，包含前几轮落下的
  Layer-first 架构文档与 `recruitment/`（招聘材料）。
- **`layers/` 仍未跟踪**（`git status` 显示 `?? layers/`）——骨架尚未进版本库；在提交前把 F2
  的 `.gitignore` 补齐最省事。

## 4. 已按本次评审同步的文档

- 结构改为 `layers/kit/` + 环境子树：
  `04-project-structure.md`、`00-technical-foundation.md` §A.3/§E、`03` §1/§7、
  根 `README.md`、`docs/architecture.md` §7。
- 决策记录：`../../../papers/notes/accepted/decision-layers-directory-layout.md`
  （含迁移清单与升级触发条件 T1–T4）。

> **待执行**：`layers/kit/` 的物理迁移尚未做——完成前，`03` §7 的 `verifyEnvClean` 目录列表
> 与文档描述不一致，第二道防线会静默失守。迁移步骤见决策记录 §3。
