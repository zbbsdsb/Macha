import org.jetbrains.kotlin.gradle.dsl.JvmTarget

// :runtime —— Layer 运行时（纯 JVM，环境无关）。
// 依赖规则（04 §2）：可依赖 :protocol；禁止依赖 :transport/:minecraft/:simulator。
plugins {
    alias(libs.plugins.kotlin.jvm)
    alias(libs.plugins.kotlin.serialization)
}

kotlin {
    jvmToolchain(25)
    compilerOptions { jvmTarget.set(JvmTarget.JVM_25) }
}

dependencies {
    api(project(":kit:protocol"))
    testImplementation(platform(libs.junit.bom))
    testImplementation(libs.junit.jupiter)
    testImplementation(libs.kotlin.test)
    testRuntimeOnly(libs.junit.platform.launcher)
}

tasks.test { useJUnitPlatform() }