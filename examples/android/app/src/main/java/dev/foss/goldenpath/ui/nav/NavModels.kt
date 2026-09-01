package dev.foss.goldenpath.ui.nav

enum class GpRoute(val wire: String) {
    Home("home"),
    Settings("settings"),
    About("about"),
    Feedback("feedback");

    companion object {
        fun fromWire(raw: String): GpRoute? = entries.find { it.wire == raw }
    }
}

enum class FeedbackKind(val wire: String) {
    Bug("bug"),
    Feature("feature");

    companion object {
        fun fromWire(raw: String): FeedbackKind? = entries.find { it.wire == raw }
    }
}

data class NavState(
    val stack: List<GpRoute>,
    val feedbackKind: FeedbackKind? = null,
    val scroll: Map<GpRoute, Int> = emptyMap(),
    val promptOpen: Boolean = false,
)
