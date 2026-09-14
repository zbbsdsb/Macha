import org.jetbrains.kotlin.gradle.dsl.JvmTarget

// :protocol —— 协议 v0 参考实现（纯 JVM，零环境依赖）。
// 依赖规则（04 §2）：只许依赖 kotlinx-serialization；禁止一切环境/运行/传输模块。
plugins {
    alias(libs.plugins.kotlin.jvm)
    alias(libs.plugins.kotlin.serialization)
}

kotlin {
    jvmToolchain(25)
    compilerOptions {
        jvmTarget.set(JvmTarget.JVM_25)
    }
}

dependencies {
    api(libs.kotlinx.serialization.json)
    testImplementation(platform(libs.junit.bom))
    testImplementation(libs.junit.jupiter)
    testImplementation(libs.kotlin.test)
    testRuntimeOnly(libs.junit.platform.launcher)
}

tasks.test { useJUnitPlatform() }