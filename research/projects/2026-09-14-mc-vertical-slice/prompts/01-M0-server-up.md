# 提示词：M0 —— 让纸面变绿色（起服 + 加载插件 + `/healthz`）

> 用途：直接整段粘给本地 agent。**只做 M0**，不要顺手做 M1+。
> 上下文：[`../README.md`](../README.md) ｜ [`../handover-checklist.md`](../handover-checklist.md) ｜ [`../plans/01-server-and-handshake.md`](../plans/01-server-and-handshake.md)

```text
# 任务：M0 —— 起 Paper 服务器、加载 Macha Layer 插件、拿到第一行绿色

## 边界（违反即失败）
1. 只允许创建/修改：layers/scripts/**、layers/run/**（运行期，不入库）、
   layers/README.md（怎么 build/起服/验证）、必要时 layers/minecraft/src/main/resources/plugin.yml，
   以及把结论回写到 research/plans/minecraft-layer/ 下对应文档。
2. 不改 src/macha/**；不改协议语义；**不实现 WebSocket 数据面、不实现观测/事件/动作执行**（那些是 M1+）。
3. 不加任何依赖；不把服务器文件提交进 git。

## 环境事实（已实测，别重复摸索）
- 本机 PATH/JAVA_HOME = JDK 21；Paper 26.2 需要 Java 25 → 启动必须显式用：
  C:\Users\chkev\.gradle\jdks\eclipse_adoptium-25-amd64-windows.2\bin\java.exe   （实测 Temurin 25.0.4.1）
- 服务器 pin：paper 26.2 build 123
  sha256 = 7b7b3b43c009103e1971a0576c26f655a7dd9b56a0a2a4438e352c03a7fecd08
  下载地址：GET https://fill.papermc.io/v3/projects/paper/versions/26.2/builds
            取 build id=123 的 downloads["server:default"].url
- 插件产物：layers/minecraft/build/libs/minecraft-0.1.0-all.jar
  （不存在则先：cd layers && ./gradlew :minecraft:shadowJar）
- 首次启动需联网（服务器 jar + Paper 的 libraries/、versions/）

## 步骤
1. 建 layers/run/minecraft/（服务器"家"目录）与 layers/scripts/run-server.ps1（版本化）。
   脚本职责：
   a) paper-26.2-123.jar 不存在则下载 → 校验 sha256，不匹配则删除并报错退出；
   b) 写 eula.txt（eula=true）；
   c) 写最小 server.properties：online-mode=false, level-type=flat, spawn-protection=0, view-distance=6；
   d) 用上面那个 JDK 25 的 java.exe 启动（-Xms1G -Xmx2G），前台运行。
2. 首次启动到控制台出现 Done 后停服；把 minecraft-0.1.0-all.jar 复制到
   layers/run/minecraft/plugins/。
3. 再次启动，观察插件加载。
4. 验收（逐条贴原始输出）：
   - 控制台出现 Done
   - 插件日志出现：Macha Minecraft Layer v0.1.0 up — protocol v0, transport 127.0.0.1:8765
   - curl.exe http://127.0.0.1:8765/healthz        → {"ok":true,"protocol":"0"}
   - curl.exe http://127.0.0.1:8765/capabilities   → 4 条能力
   - git -C <repo> status --porcelain --untracked-files=all -- layers/run   → 输出为空
     （即 layers/run/**、eula.txt、server.properties、paper-*.jar 都没进 git）
5. 写 layers/README.md：怎么 build、怎么起服（含 JDK 25 路径）、怎么验证、
   以及已知限制（shadow relocate 未做，与其它插件共存可能冲突）。
6. 若 api-version: '26.2' 被服务器拒绝：按报错改 plugin.yml 的 api-version，重启验证，
   然后把结论回写 research/plans/minecraft-layer/03-build-and-module-layout.md §4，
   并在 06-next-step-plan.md 的 M0 行记一行。

## 不要做
- 不要实现 /action、WebSocket、observation、event、ActionExecutor（M1–M4 的事）。
- 不要为了让 curl 好测而改协议字段或加临时端点。
- 不要提交服务器目录；不要 git add layers/run。

## 汇报格式
1) 改动文件清单  2) 每步命令与输出摘要（含 healthz / capabilities 的原始 JSON）
3) 未做/不确定项及原因  4) 若被 api-version 卡住：贴完整报错与最终取值
```
