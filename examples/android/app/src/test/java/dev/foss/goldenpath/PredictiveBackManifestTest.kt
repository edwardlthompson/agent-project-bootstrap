package dev.foss.goldenpath

import org.junit.Assert.assertTrue
import org.junit.Test
import java.io.File

/** Predictive Back / OnBackInvokedCallback must stay enabled for system Back parity. */
class PredictiveBackManifestTest {
    @Test
    fun mainActivityEnablesOnBackInvokedCallback() {
        val candidates = listOf(
            File("src/main/AndroidManifest.xml"),
            File("app/src/main/AndroidManifest.xml"),
        )
        val manifest = candidates.first { it.isFile }.readText()
        assertTrue(manifest.contains("""android:enableOnBackInvokedCallback="true""""))
    }
}
