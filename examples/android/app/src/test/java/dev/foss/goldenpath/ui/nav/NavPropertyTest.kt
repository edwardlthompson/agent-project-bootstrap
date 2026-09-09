package dev.foss.goldenpath.ui.nav

import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import kotlin.random.Random

class NavPropertyTest {
    @Test
    fun randomWalkKeepsHomeRootAndDrainsToHome() {
        val rng = Random(42)
        val routes = listOf(GpRoute.Settings, GpRoute.About, GpRoute.Feedback, GpRoute.Home)
        val kinds = FeedbackKind.entries
        repeat(200) {
            var state = Nav.home()
            repeat(rng.nextInt(1, 12)) {
                state = when (rng.nextInt(4)) {
                    0 -> Nav.push(state, routes.random(rng), kinds.random(rng))
                    1 -> Nav.pop(state)
                    2 -> Nav.setPrompt(state, rng.nextBoolean())
                    else -> Nav.recordScroll(state, Nav.current(state), rng.nextInt(0, 400))
                }
                assertEquals(GpRoute.Home, state.stack.first())
                assertTrue(state.stack.isNotEmpty())
                assertEquals(state.stack, Nav.normalizeStack(state.stack))
            }
            var guard = 0
            while ((state.promptOpen || Nav.canPop(state)) && guard < 32) {
                state = Nav.pop(state)
                guard += 1
            }
            assertTrue(Nav.isHome(state))
            assertEquals(state, Nav.pop(state))
            assertTrue(!state.promptOpen)
        }
    }
}
