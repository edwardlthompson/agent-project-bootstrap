pluginManagement {
    repositories {
        mavenCentral()
        gradlePluginPortal()
        google()
    }
}

dependencyResolutionManagement {
    repositoriesMode.set(RepositoriesMode.FAIL_ON_PROJECT_REPOS)
    repositories {
        mavenCentral()
        google()
    }
}

rootProject.name = "golden-path-android"
include(":app")

// Gradle's test-results binary writer fails when the project path contains spaces
// (NoSuchFileException / EOFException on in-progress-results-*.bin). Remap build/
// to a space-free cache when needed. Override: GOLDENPATH_ANDROID_BUILD_DIR.
gradle.beforeProject {
    val rootPath = settings.rootDir.absolutePath
    if (' ' !in rootPath) {
        return@beforeProject
    }
    val base =
        System.getenv("GOLDENPATH_ANDROID_BUILD_DIR")
            ?: "${System.getProperty("user.home")}/.cache/goldenpath-android-build"
    val leaf = path.replace(':', '_').ifEmpty { "root" }
    layout.buildDirectory.set(file("$base/$leaf"))
}
