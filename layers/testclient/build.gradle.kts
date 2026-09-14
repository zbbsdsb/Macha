import org.jetbrains.kotlin.gradle.dsl.JvmTarget

// :testclient —— 垂直切片测试客户端（纯 JVM，非 Paper 插件，是独立程序）。
// 依赖规则（04 §2）：只可依赖 :protocol；不得依赖 :runtime/:transport/环境模块
// （客户端只按协议在线上发声，不进入 Layer 内部）。
plugins {
    alias(libs.plugins.kotlin.jvm)
    alias(libs.plugins.kotlin.serialization)
    application
}

kotlin {
    jvmToolchain(25)
    compilerOptions { jvmTarget.set(JvmTarget.JVM_25) }
}

dependencies {
    // F4：testclient 是独立 application（叶子），无消费者；:kit:protocol 取 implementation。
    // java-websocket 是第三方 WS 客户端库（非 :kit 模块），供 VerticalSliceProbe 在线上发声，
    // 不违反"只依赖 :protocol 模块"的规则（04 §2）。
    implementation(project(":kit:protocol"))
    implementation(libs.kotlinx.serialization.json)
    implementation(libs.java.websocket)
    testImplementation(platform(libs.junit.bom))
    testImplementation(libs.junit.jupiter)
    testImplementation(libs.kotlin.test)
    testRuntimeOnly(libs.junit.platform.launcher)
}

application {
    mainClass.set("dev.macha.layer.testclient.VerticalSliceProbeKt")
}

tasks.test { useJUnitPlatform() }