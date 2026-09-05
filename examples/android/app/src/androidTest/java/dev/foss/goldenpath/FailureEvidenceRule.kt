package dev.foss.goldenpath

import android.graphics.Bitmap
import android.util.Log
import androidx.compose.ui.test.junit4.ComposeTestRule
import androidx.compose.ui.test.onRoot
import androidx.compose.ui.test.printToString
import androidx.test.platform.app.InstrumentationRegistry
import org.junit.rules.TestWatcher
import org.junit.runner.Description
import java.io.File
import java.io.FileOutputStream

/**
 * On instrumented failure: log Compose semantics and write a PNG under the app files dir
 * (visible in logcat / `adb pull` when debugging emulator flakes).
 */
class FailureEvidenceRule(
    private val composeRule: () -> ComposeTestRule?,
) : TestWatcher() {
    override fun failed(e: Throwable, description: Description) {
        val tag = "GpUiTestFailure"
        val name = "${description.className}.${description.methodName}"
        runCatching {
            val semantics = composeRule()?.onRoot()?.printToString().orEmpty()
            if (semantics.isNotBlank()) {
                Log.e(tag, "Semantics dump for $name:\n$semantics")
            }
        }.onFailure { Log.e(tag, "Semantics dump failed for $name", it) }

        runCatching {
            val bitmap = InstrumentationRegistry.getInstrumentation().uiAutomation.takeScreenshot()
                ?: return@runCatching
            val dir = File(
                InstrumentationRegistry.getInstrumentation().targetContext.filesDir,
                "test-failures",
            )
            dir.mkdirs()
            val out = File(dir, "${description.methodName}.png")
            FileOutputStream(out).use { stream ->
                bitmap.compress(Bitmap.CompressFormat.PNG, 90, stream)
            }
            bitmap.recycle()
            Log.e(tag, "Screenshot for $name: ${out.absolutePath}")
        }.onFailure { Log.e(tag, "Screenshot failed for $name", it) }
    }
}
