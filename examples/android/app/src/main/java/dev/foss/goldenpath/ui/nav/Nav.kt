package dev.foss.goldenpath.ui.nav

object Nav {
    fun home(): NavState = NavState(stack = listOf(GpRoute.Home))

    fun normalizeStack(raw: List<GpRoute>): List<GpRoute> {
        val out = mutableListOf<GpRoute>()
        for (item in raw) {
            if (out.isEmpty() && item != GpRoute.Home) out.add(GpRoute.Home)
            if (out.lastOrNull() == item) continue
            out.add(item)
        }
        if (out.isEmpty()) return listOf(GpRoute.Home)
        if (out.first() != GpRoute.Home) return listOf(GpRoute.Home) + out
        return out
    }

    fun current(state: NavState): GpRoute = normalizeStack(state.stack).lastOrNull() ?: GpRoute.Home

    fun isHome(state: NavState): Boolean =
        current(state) == GpRoute.Home && normalizeStack(state.stack).size <= 1

    fun canPop(state: NavState): Boolean = !isHome(state)

    fun setPrompt(state: NavState, open: Boolean): NavState =
        if (state.promptOpen == open) state else state.copy(promptOpen = open)

    fun push(state: NavState, route: GpRoute, kind: FeedbackKind? = null): NavState {
        if (route == GpRoute.Home) {
            if (isHome(state) && state.feedbackKind == null) return state
            return state.copy(stack = listOf(GpRoute.Home), feedbackKind = null)
        }
        if (current(state) == route) return state
        return state.copy(
            stack = normalizeStack(state.stack) + route,
            feedbackKind = if (route == GpRoute.Feedback) kind ?: FeedbackKind.Bug else null,
        )
    }

    fun pop(state: NavState): NavState {
        if (state.promptOpen) return state.copy(promptOpen = false)
        if (!canPop(state)) return state
        val next = normalizeStack(state.stack).dropLast(1).ifEmpty { listOf(GpRoute.Home) }
        val top = next.last()
        return state.copy(
            stack = next,
            feedbackKind = if (top == GpRoute.Feedback) state.feedbackKind else null,
        )
    }

    fun recordScroll(state: NavState, route: GpRoute, y: Int): NavState {
        if (route == GpRoute.Home) return state
        val n = y.coerceAtLeast(0)
        return state.copy(scroll = state.scroll + (route to n))
    }

    fun restoreScroll(state: NavState, route: GpRoute): Int =
        state.scroll[route]?.coerceAtLeast(0) ?: 0
}
