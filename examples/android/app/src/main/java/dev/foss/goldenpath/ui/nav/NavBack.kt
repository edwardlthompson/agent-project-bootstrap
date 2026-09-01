package dev.foss.goldenpath.ui.nav

data class NavBackResult(
    val next: NavState,
    val finishActivity: Boolean,
)

object NavBack {
    /** System Back pops one overlay or route and never finishes the Activity. */
    fun onSystemBack(state: NavState): NavBackResult =
        NavBackResult(next = Nav.pop(state), finishActivity = false)
}
