import org.jetbrains.kotlin.gradle.dsl.JvmTarget

// :simulator —— 假环境（纯 JVM，C4 对照条件）。
// 依赖规则（04 §2）：可依赖 :protocol/:runtime/:transport；禁止 paper-api。
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
    // F4：simulator 是 C4 对照环境（叶子），无外部消费者；:kit:* 改为 implementation，
    // 不把共享内核 API 传递性暴露给（不存在的）消费者，拆仓时边界更清晰。
    implementation(project(":kit:protocol"))
    implementation(project(":kit:runtime"))
    implementation(project(":kit:transport"))
    testImplementation(platform(libs.junit.bom))
    testImplementation(libs.junit.jupiter)
    testImplementation(libs.kotlin.test)
    testRuntimeOnly(libs.junit.platform.launcher)
}

application {
    mainClass.set("dev.macha.layer.simulator.SimulatorMainKt")
}

tasks.test { useJUnitPlatform() }