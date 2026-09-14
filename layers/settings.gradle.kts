// Macha Layers — 独立 Gradle 构建根（不放在仓库根，仓库根是 Python 项目）。
// 共享内核 + 环境模块统一在这里；未来拆仓时整目录移出即可。
pluginManagement {
    repositories {
        gradlePluginPortal()
        mavenCentral()
    }
}

plugins {
    // 允许按 toolchain 自动下载 JDK（本机无 JDK 25 时由 foojay 抓取 Temurin 25）
    id("org.gradle.toolchains.foojay-resolver-convention") version "1.0.0"
}

rootProject.name = "macha-layers"

include(":kit:protocol", ":kit:runtime", ":kit:transport", ":minecraft", ":simulator", ":testclient")