import org.gradle.api.file.DuplicatesStrategy
import org.jetbrains.kotlin.gradle.dsl.JvmTarget

// :minecraft —— Minecraft Layer；仓库内唯一允许依赖 paper-api 的模块（00 §A.3 规则 4）。
// 依赖规则（04 §2）：可依赖 :protocol/:runtime/:transport + paper-api(compileOnly)。
plugins {
    alias(libs.plugins.kotlin.jvm)
    alias(libs.plugins.kotlin.serialization)
    alias(libs.plugins.shadow)
}

kotlin {
    jvmToolchain(25)
    compilerOptions { jvmTarget.set(JvmTarget.JVM_25) }
}

dependencies {
    // F4：:minecraft 是叶子插件模块，无外部消费者；:kit:* 只需自己的编译/运行期 classpath，
    // 不向（不存在的）消费者传递性暴露协议/运行时 API，改为 implementation 语义更诚实。
    implementation(project(":kit:protocol"))
    implementation(project(":kit:runtime"))
    implementation(project(":kit:transport"))

    // paper-api 只能 compileOnly：运行期由 Paper 服务器提供，打进 jar = 类冲突（红线）。
    compileOnly(libs.paper.api)
    // Paper 不提供 Kotlin/serialization/websocket 运行时，须随插件分发（shadow + relocate）。
    implementation(libs.kotlin.stdlib)
    implementation(libs.kotlinx.serialization.json)
    implementation(libs.java.websocket)

    testImplementation(platform(libs.junit.bom))
    testImplementation(libs.junit.jupiter)
    testImplementation(libs.kotlin.test)
    testRuntimeOnly(libs.junit.platform.launcher)
}

tasks.test { useJUnitPlatform() }

// shadow 打包：让 KotlinModuleMetadata 转换器看到全部重复项再合并（否则 silently dropped）。
// TODO(scaffold): relocate（kotlin/kotlinx/java.websocket → dev.macha.layer.shadow.*）在产出可分发
// 插件 jar 时打入（03 §3），避免与其它插件捆绑库类冲突；届时需同步更新 plugin.yml main 与 ServiceLoader 元数据。
tasks.shadowJar {
    mergeServiceFiles()
    duplicatesStrategy = DuplicatesStrategy.INCLUDE
}