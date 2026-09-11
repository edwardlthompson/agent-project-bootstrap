package dev.foss.goldenpath.ui.screenshot

import org.junit.Assert.assertTrue
import org.junit.Test
import java.io.File

/** Documents the instrumented edge-to-edge inset regression screenshot set (#166). */
class InsetScreenshotSetTest {
    @Test
    fun insetUiTestAndStackScreenshotPresent() {
        val roots = listOf(
            File("src/androidTest/java/dev/foss/goldenpath"),
            File("app/src/androidTest/java/dev/foss/goldenpath"),
        )
        val dir = roots.first { it.isDirectory }
        assertTrue(File(dir, "NavBarInsetUiTest.kt").isFile)
        assertTrue(File(dir, "StackScreenshotUiTest.kt").isFile)
    }
}
