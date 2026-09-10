package dev.foss.goldenpath.memory

/**
 * Android 17+ per-app memory limits and trim signals.
 *
 * Detect limiter kills via [ApplicationExitInfo] without polling
 * [android.app.ActivityManager.getMemoryInfo]. Trim only on UI_HIDDEN and BACKGROUND.
 */
object MemoryBudget {
    /** [android.app.ApplicationExitInfo.REASON_OTHER] */
    const val REASON_OTHER = 13

    const val LIMITER_MARKER = "MemoryLimiter:AnonSwap"

    /** [android.content.ComponentCallbacks2.TRIM_MEMORY_UI_HIDDEN] */
    const val TRIM_UI_HIDDEN = 20

    /** [android.content.ComponentCallbacks2.TRIM_MEMORY_BACKGROUND] */
    const val TRIM_BACKGROUND = 40

    enum class TrimHint { NONE, UI, BACKGROUND }

    data class ExitHint(val reason: Int, val description: String?)

    fun isLimiterKill(reason: Int, description: String?): Boolean {
        val text = description?.trim().orEmpty()
        if (text.isEmpty()) return false
        return reason == REASON_OTHER && text.contains(LIMITER_MARKER)
    }

    fun firstLimiterKill(exits: List<ExitHint>): ExitHint? =
        exits.firstOrNull { isLimiterKill(it.reason, it.description) }

    fun shouldReleaseUi(level: Int): Boolean = level >= TRIM_UI_HIDDEN

    fun shouldReleaseBackground(level: Int): Boolean = level >= TRIM_BACKGROUND

    fun trimHint(level: Int): TrimHint = when {
        shouldReleaseBackground(level) -> TrimHint.BACKGROUND
        shouldReleaseUi(level) -> TrimHint.UI
        else -> TrimHint.NONE
    }
}
