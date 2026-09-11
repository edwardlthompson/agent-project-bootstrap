plugins {
    id("com.android.application")
    id("org.jetbrains.kotlin.plugin.compose")
}

kotlin {
    compilerOptions {
        jvmTarget.set(org.jetbrains.kotlin.gradle.dsl.JvmTarget.JVM_17)
    }
}

// Live donations.json / app-update.json are gitignored; copy exemplars when missing
// so local Gradle and CI instrumented tests never ship an empty About donate block.
val syncExemplarAssets = tasks.register("syncExemplarAssets") {
    val assetsDir = layout.projectDirectory.dir("src/main/assets")
    doLast {
        listOf("donations.json", "app-update.json").forEach { name ->
            val dest = assetsDir.file(name).asFile
            val example = assetsDir.file("$name.example").asFile
            if (!dest.exists() && example.exists()) {
                example.copyTo(dest)
                logger.lifecycle("Synced exemplar asset: ${dest.name}")
            }
        }
    }
}

tasks.named("preBuild").configure { dependsOn(syncExemplarAssets) }

fun readGoldenPathAppVersion(): String {
    val file = rootProject.file("../../schemas/golden-path/app-version.json")
    check(file.isFile) { "Missing Golden Path app version SoT: ${file.invariantSeparatorsPath}" }
    val match = Regex(""""version"\s*:\s*"([^"]+)"""").find(file.readText())
    val version = match?.groupValues?.get(1)?.trim().orEmpty()
    check(version.isNotEmpty()) { "schemas/golden-path/app-version.json missing version" }
    return version
}

android {
    namespace = "dev.foss.goldenpath"
    compileSdk = 37

    defaultConfig {
        applicationId = "dev.foss.goldenpath"
        minSdk = 26
        targetSdk = 37
        versionCode = 1
        versionName = readGoldenPathAppVersion()
        testInstrumentationRunner = "androidx.test.runner.AndroidJUnitRunner"
        testInstrumentationRunnerArguments["clearPackageData"] = "true"
    }

    buildTypes {
        release {
            isMinifyEnabled = true
            isShrinkResources = true
            proguardFiles(
                getDefaultProguardFile("proguard-android-optimize.txt"),
                "proguard-rules.pro",
            )
        }
    }

    val uploadStoreFile = System.getenv("GOLDENPATH_UPLOAD_STORE_FILE")
    if (!uploadStoreFile.isNullOrBlank()) {
        signingConfigs.create("upload") {
            storeFile = file(uploadStoreFile)
            storePassword = System.getenv("GOLDENPATH_UPLOAD_STORE_PASSWORD").orEmpty()
            keyAlias = System.getenv("GOLDENPATH_UPLOAD_KEY_ALIAS") ?: "upload"
            keyPassword = System.getenv("GOLDENPATH_UPLOAD_KEY_PASSWORD").orEmpty()
        }
        buildTypes.named("release").configure {
            signingConfig = signingConfigs.getByName("upload")
        }
    }

    compileOptions {
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }

    buildFeatures {
        compose = true
        buildConfig = true
    }
    testOptions {
        unitTests.isIncludeAndroidResources = true
        execution = "ANDROIDX_TEST_ORCHESTRATOR"
        animationsDisabled = true
    }

    lint {
        abortOnError = true
        lintConfig = file("lint.xml")
        error += "ContentDescription"
        error += "ClickableViewAccessibility"
        error += "LabelFor"
        error += "KeyboardInaccessibleWidget"
    }
}

dependencies {
    val composeBom = platform("androidx.compose:compose-bom:2026.08.00")
    implementation(composeBom)
    androidTestImplementation(composeBom)

    implementation("androidx.core:core-ktx:1.19.0")
    implementation("androidx.activity:activity-compose:1.13.0")
    implementation("androidx.compose.material3:material3")
    implementation("androidx.compose.ui:ui")
    implementation("androidx.compose.ui:ui-tooling-preview")
    implementation("androidx.compose.material:material-icons-extended")
    implementation("androidx.datastore:datastore-preferences:1.2.1")
    implementation("androidx.lifecycle:lifecycle-runtime-compose:2.11.0")
    implementation("org.jetbrains.kotlinx:kotlinx-coroutines-android:1.11.0")

    testImplementation("androidx.test:core:1.7.0")
    testImplementation("junit:junit:4.13.2")
    testImplementation("org.robolectric:robolectric:4.16.1")
    testImplementation("org.jetbrains.kotlinx:kotlinx-coroutines-test:1.11.0")

    androidTestImplementation("androidx.test.ext:junit:1.3.0")
    androidTestImplementation("androidx.test:runner:1.7.0")
    androidTestImplementation("androidx.test:rules:1.7.0")
    // Pin AndroidX Test line (no official test-bom). Espresso 3.7+ required on API 36+.
    androidTestImplementation("androidx.test.espresso:espresso-core:3.7.0")
    androidTestImplementation("androidx.compose.ui:ui-test-junit4")
    androidTestUtil("androidx.test:orchestrator:1.6.1")

    debugImplementation("androidx.compose.ui:ui-tooling")
    debugImplementation("androidx.compose.ui:ui-test-manifest")
    // FOSS ONLY: No proprietary Play Services or closed telemetry SDKs
}
