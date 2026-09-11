package dev.foss.goldenpath

import android.provider.Settings
import androidx.test.platform.app.InstrumentationRegistry
import org.junit.rules.TestWatcher
import org.junit.runner.Description

/**
 * Best-effort animation disable for instrumented UI (mirrors CI `disable-animations: true`).
 * Requires a debug/test harness that can write secure settings; otherwise no-ops.
 */
class DisableAnimationsRule : TestWatcher() {
    private val keys = listOf(
        Settings.Global.WINDOW_ANIMATION_SCALE,
        Settings.Global.TRANSITION_ANIMATION_SCALE,
        Settings.Global.ANIMATOR_DURATION_SCALE,
    )
    private val previous = mutableMapOf<String, Float>()

    override fun starting(description: Description) {
        val resolver = InstrumentationRegistry.getInstrumentation().context.contentResolver
        for (key in keys) {
            runCatching {
                previous[key] = Settings.Global.getFloat(resolver, key, 1f)
                Settings.Global.putFloat(resolver, key, 0f)
            }
        }
    }

    override fun finished(description: Description) {
        val resolver = InstrumentationRegistry.getInstrumentation().context.contentResolver
        for ((key, value) in previous) {
            runCatching { Settings.Global.putFloat(resolver, key, value) }
        }
        previous.clear()
    }
}
