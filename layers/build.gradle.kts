// 根构建脚本：只做元信息与仓库共享。插件与依赖在各模块 build.gradle.kts 各自声明，
// 以便模块依赖边界（04 §2）在编译期逐模块可见、可审查。
plugins {
    alias(libs.plugins.kotlin.jvm) apply false
    alias(libs.plugins.kotlin.serialization) apply false
    alias(libs.plugins.shadow) apply false
}

allprojects {
    group = "dev.macha.layer"
    version = "0.1.0"
    repositories {
        mavenCentral()
        maven("https://repo.papermc.io/repository/maven-public/")
    }
}

// ==================== 边界守护（03 §7）====================
// 第一道防线是 Gradle 模块依赖（编译期）；这里是第二道：import / 标识符扫描，挂到 check。
private fun rel(p: File): String = p.relativeTo(rootDir).invariantSeparatorsPath

// 扫描前剔除注释，避免把"说明不暴露 Material/World"的文档注释误判为真违规（03 §7-2）。
// 逐文件遍历、保留行号映射；用"是否处于 /* */ 块注释中"的状态跨行剔除（F6）——
// 块注释里的 // 与 /* 不再被误当注释边界，跨行 KDoc 不会误报。
private fun stripComments(lines: List<String>): List<String> {
    val cleaned = ArrayList<String>(lines.size)
    var inBlock = false
    for (line in lines) {
        val sb = StringBuilder()
        var i = 0
        val n = line.length
        while (i < n) {
            if (inBlock) {
                val end = line.indexOf("*/", i)
                if (end < 0) { i = n } else { inBlock = false; i = end + 2 }
            } else if (i < n - 1 && line[i] == '/' && line[i + 1] == '*') {
                inBlock = true
                i += 2
            } else if (i < n - 1 && line[i] == '/' && line[i + 1] == '/') {
                break
            } else {
                sb.append(line[i])
                i++
            }
        }
        cleaned.add(sb.toString())
    }
    return cleaned
}

private fun scanBanned(
    files: List<File>,
    banned: List<Regex>,
    out: MutableList<String>,
) {
    for (f in files) {
        val lines = f.readLines()
        val code = stripComments(lines)
        code.forEachIndexed { i, line ->
            for (r in banned) {
                if (r.containsMatchIn(line)) {
                    out += "${rel(f)}:${i + 1}: ${lines[i].trim()} [${r.pattern}]"
                }
            }
        }
    }
}

val boundaryDir = rootDir
val ktSources: FileTree = fileTree(boundaryDir) {
    // kit/ 收拢后共享模块深一层（layers/kit/*/src/...），用 **/ 匹配任意层，否则会漏扫。
    include("**/src/main/kotlin/**/*.kt")
}

// ① Paper 范围检查：除 minecraft 的 plugin/ 与 adapter/ 外，任何 src/main/kotlin
//    出现 import org.bukkit / io.papermc / net.minecraft → 失败。
tasks.register("verifyPaperScope") {
    group = "verification"
    description = "03 §7-1·Paper 范围检查：Paper import 只允许出现在 minecraft plugin/ 与 adapter/"
    val banned = listOf(
        Regex("^\\s*import\\s+(org\\.bukkit|io\\.papermc|net\\.minecraft)\\b"),
    )
    doLast {
        val bad = mutableListOf<String>()
        val allowed = { p: File -> p.path.contains("src${File.separator}main${File.separator}kotlin") && (p.path.contains("${File.separator}plugin${File.separator}") || p.path.contains("${File.separator}adapter${File.separator}")) }
        val scanned = (ktSources.minus(ktSources.filter { allowed(it) })).toList()
        if (scanned.isEmpty()) throw GradleException(
            "verifyPaperScope: 扫描到 0 个 src/main/kotlin 文件——ktSources 路径可能写错，拒绝静默通过",
        )
        scanBanned(scanned, banned, bad)
        if (bad.isNotEmpty()) throw GradleException(
            "边界守护 ① Paper 范围违规（共 ${bad.size} 处）：\n" + bad.joinToString("\n"),
        )
    }
}

// ② 协议洁净检查：protocol/runtime/simulator 的 src 禁止出现环境专有标识。
tasks.register("verifyEnvClean") {
    group = "verification"
    description = "03 §7-2·协议洁净检查：protocol/runtime/simulator 不得出现环境专有标识"
    val banned = listOf(
        Regex("\\borg\\.bukkit\\b"),
        Regex("\\bMaterial\\b"),
        Regex("\\bBlockData\\b"),
        Regex("\\bWorld\\b"),
    )
    val dirs = listOf("kit/protocol", "kit/runtime", "simulator").map { file(it) }
    doLast {
        val bad = mutableListOf<String>()
        val files = dirs.flatMap { d ->
            if (!d.exists()) emptyList()
            else fileTree(d) { include("src/**/*.kt") }.files
        }
        if (files.isEmpty()) throw GradleException(
            "verifyEnvClean: 扫描到 0 个 .kt 文件——目录列表可能写错，拒绝静默通过",
        )
        scanBanned(files, banned, bad)
        if (bad.isNotEmpty()) throw GradleException(
            "边界守护 ② 环境标识渗入共享模块（共 ${bad.size} 处）：\n" + bad.joinToString("\n"),
        )
    }
}

// ③ Core 洁净检查（V2）：仓库根的 src/macha/** 不得出现环境/构建标识。
tasks.register("verifyCoreClean") {
    group = "verification"
    description = "03 §7-3·Core 洁净检查：src/macha（Python Core）不出现环境/构建标识"
    val banned = listOf(
        Regex("\\borg\\.bukkit\\b"),
        Regex("\\bio\\.papermc\\b"),
        Regex("\\bnet\\.minecraft\\b"),
        Regex("\\borg\\.gradle\\b"),
        Regex("\\borg\\.jetbrains\\.kotlin\\b"),
    )
    doLast {
        val coreDir = rootDir.parentFile.resolve("src").resolve("macha")
        if (!coreDir.exists()) {
            logger.info("verifyCoreClean: 没有 src/macha，跳过（Core 尚未就位）")
            return@doLast
        }
        val bad = mutableListOf<String>()
        val files = fileTree(coreDir) { include("**/*.py") }.files.toList()
        scanBanned(files, banned, bad)
        if (bad.isNotEmpty()) throw GradleException(
            "边界守护 ③ Core 洁净违规（共 ${bad.size} 处）：\n" + bad.joinToString("\n"),
        )
    }
}

// 根 `check`：跑三个边界守护；子项目各自的 check 仍由 `gradlew check` 一并触发。
tasks.register("check") {
    group = "verification"
    description = "03 §7 边界守护：聚合 verifyPaperScope / verifyEnvClean / verifyCoreClean"
    dependsOn("verifyPaperScope", "verifyEnvClean", "verifyCoreClean")
}