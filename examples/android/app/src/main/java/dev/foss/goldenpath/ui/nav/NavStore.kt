package dev.foss.goldenpath.ui.nav

object NavStore {
    const val PREFS = "gp_nav"
    const val KEY = "gp.nav.v1"

    fun load(raw: String?): NavState = NavJson.deserialize(raw).copy(promptOpen = false)

    fun save(state: NavState): String = NavJson.serialize(state.copy(promptOpen = false))
}

object NavSession {
    fun boot(stored: NavState, crashPending: Boolean): NavState {
        var next = stored.copy(promptOpen = false)
        if (crashPending) {
            next = Nav.push(next, GpRoute.Feedback, FeedbackKind.Bug)
        }
        return next
    }
}
