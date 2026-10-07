package dev.foss.goldenpath

import org.junit.Assert.assertTrue
import org.junit.Test
import java.io.File

/** Brand splash theme must stay wired for first-paint continuity (branding/BRANDING.md). */
class SplashThemeTest {
    @Test
    fun splashThemeAndManifestAreWired() {
        val themes = listOf(
            File("src/main/res/values/themes.xml"),
            File("app/src/main/res/values/themes.xml"),
        ).first { it.isFile }.readText()
        assertTrue(themes.contains("Theme.GoldenPath.Splash"))
        assertTrue(themes.contains("@drawable/ic_brand_mark"))
        assertTrue(themes.contains("postSplashScreenTheme"))

        val manifest = listOf(
            File("src/main/AndroidManifest.xml"),
            File("app/src/main/AndroidManifest.xml"),
        ).first { it.isFile }.readText()
        assertTrue(manifest.contains("""android:theme="@style/Theme.GoldenPath.Splash""""))
    }
}
