# 承接检查清单（handover checklist）

> 用途：**人和 agent 都用它接手这个项目**。全部打勾才算"承接成功"；缺任何一项，先补齐再动手。
> 项目：[`README.md`](README.md) ｜ 里程碑定义：[`../../plans/minecraft-layer/06-next-step-plan.md`](../../plans/minecraft-layer/06-next-step-plan.md)

---

## A. 读（10 分钟）

- [ ] 本目录 `README.md`（项目一句话、里程碑表、边界）
- [ ] `06-next-step-plan.md` §0（终点形态与演示脚本）与 §4（环境事实与风险）
- [ ] `05-scaffold-review-2026-09-14.md` §5（现状与证据）
- [ ] 当前里程碑对应的 `plans/0N-*.md`

## B. 环境核对（**必须先做，否则必然白折腾**）

- [ ] `PATH`/`JAVA_HOME` 是 **JDK 21**，不能用来起 Paper 26.2
- [ ] JDK 25 存在：`C:\Users\chkev\.gradle\jdks\eclipse_adoptium-25-amd64-windows.2\bin\java.exe`
      （实测 `openjdk version "25.0.4.1"`）
- [ ] 服务器 pin：`paper-26.2-123.jar`
      sha256 `7b7b3b43c009103e1971a0576c26f655a7dd9b56a0a2a4438e352c03a7fecd08`
- [ ] 插件产物存在：`layers/minecraft/build/libs/minecraft-0.1.0-all.jar`
      （若缺：`cd layers && ./gradlew :minecraft:shadowJar`）
- [ ] 首次启动需要联网（下载服务器 jar + Paper 的 `libraries/`、`versions/`）
- [ ] 有 **1.20.1 客户端**可用（云端实验环境是 Arclight 1.20.1；M5–M6 必须真人进服）
- [ ] 云端实验环境：`play.simpfun.cn:15463`（Arclight 1.20.1，protocol 763），面板**最大权限**（可上传 jar / 改配置 / 重启 / 看日志）
- [ ] 云端必须用 `transport.mode: dial`（Layer 主动拨出）+ token；本地继续 `listen`
- [ ] 实验环境确定性：whitelist 开、固定世界/种子、跑批期间无第三方玩家、上传 jar 记 sha256
- [ ] 构建取**下界**：Spigot API **1.20.1** + **Java 17**（一份 jar 同时跑云端与本地）

## C. 状态核对（"文档说的" vs "实际是"）

- [ ] `git log --oneline -3`：确认自己接的是哪个 commit
- [ ] `git status --short`：确认工作区没有别人的未提交改动
- [ ] 服务器目录未入库：`git status --porcelain --untracked-files=all -- layers/run` 为空
- [ ] `layers/run/minecraft/` 是否存在 = 服务器是否曾经启动过（**2026-09-14 起：已存在**；
      证据见 `logs/latest.log` 的 `Done` 与插件启动日志）
- [ ] 当前里程碑状态与 `README.md` §2 的表一致；不一致 → 先更新表再干活

## D. 硬边界（写进提示词，逐条不得违反）

- [ ] 不改 `src/macha/**`
- [ ] 不扩协议字段（要改 → 先在 `01-protocol-v0.md` §9 登记，再改代码）
- [ ] Layer 内零认知（无记忆/人格/规划/社交判断）
- [ ] `paper-api` 只 `compileOnly`、只在 `:minecraft`
- [ ] 不加依赖；不引入 Netty/Jetty/Ktor/MockBukkit
- [ ] 不把 `layers/run/**`、`eula.txt`、`server.properties`、`paper-*.jar` 提交进 git

## E. 已定决策（不要重新讨论）

- [ ] **P1** Stub Core = Python，`tools/stub-core/`（**不进** `src/macha/`）
- [ ] **P2** Paper 起服 = 手工 pin jar + 版本化脚本 `layers/scripts/run-server.ps1`
- [ ] **P3** 协议 v0 **边跑边冻**，跑完 8 步再冻结
- [ ] `layers/kit/` 布局与拆仓触发条件 T1–T4（决策记录 `decision-layers-directory-layout.md`）
- [ ] 路径一（IC 生命周期）**已冻结**，不得在 Layer 阶段实现它

## F. 验收命令（复制即用）

```powershell
# 1) 起服（脚本或手动）：注意用 JDK 25
# 2) 插件加载日志
#    期望：Macha Minecraft Layer v0.1.0 up — protocol v0, transport 127.0.0.1:8765
curl.exe http://127.0.0.1:8765/healthz        # 期望 {"ok":true,"protocol":"0"}
curl.exe http://127.0.0.1:8765/capabilities   # 期望 4 条能力
# 3) 构建与边界守护
cd layers ; ./gradlew check
```

- [ ] 我能独立跑出上面全部输出（**这是"承接成功"的判据**）

## G. 已知坑（踩过，别重踩）

- [ ] `plugin.yml api-version: '26.2'` 从未被真实服务器检验；被拒 → 改一行 + 回写 `03` §4
- [ ] 僵尸会自己乱走，会淹掉"它在回应我" → M5 用 armor stand 或 `setAI(false)`
- [ ] `WebSocketDataPlane` 是空壳（M1 才做），**M0 不要试图握手**
- [ ] `shadow relocate` 仍是 TODO：单插件测试可接受，与其它插件共存可能冲突
- [ ] Bukkit API 只能在主线程（`03` §6）

## H. 反向确认（交接失败的判定）

- [ ] 我能不看上文、只凭本清单 + 计划文件，说出"下一步第一件事是什么"
- [ ] 我知道卡住时该更新哪份文档（而不是只在代码里打补丁）

> 若 A–H 有任一项无法打勾 → **承接未完成**，先补齐；不要开始写代码。
