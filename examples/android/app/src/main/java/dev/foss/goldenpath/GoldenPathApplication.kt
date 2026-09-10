package dev.foss.goldenpath

import android.app.ActivityManager
import android.app.Application
import android.os.Build
import android.util.Log
import dev.foss.goldenpath.crashcapture.CrashCapture
import dev.foss.goldenpath.memory.MemoryBudget

class GoldenPathApplication : Application() {
    override fun onCreate() {
        super.onCreate()
        CrashCapture.install(this)
        recordLimiterExit()
    }

    override fun onTrimMemory(level: Int) {
        super.onTrimMemory(level)
        val hint = MemoryBudget.trimHint(level)
        if (hint != MemoryBudget.TrimHint.NONE) {
            Log.d(TAG, "trim $hint")
        }
    }

    private fun recordLimiterExit() {
        if (Build.VERSION.SDK_INT < Build.VERSION_CODES.R) return
        runCatching {
            val am = getSystemService(ActivityManager::class.java) ?: return
            val hints = am.getHistoricalProcessExitReasons(packageName, 0, 5).map { exit ->
                MemoryBudget.ExitHint(exit.reason, exit.description)
            }
            if (MemoryBudget.firstLimiterKill(hints) != null) {
                Log.w(TAG, "prior session hit Android memory limiter")
            }
        }
    }

    companion object {
        private const val TAG = "GpMemory"
    }
}
