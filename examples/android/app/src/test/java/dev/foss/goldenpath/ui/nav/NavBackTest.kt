package dev.foss.goldenpath.ui.nav

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Test

class NavBackTest {
    @Test
    fun backFromSettingsGoesHomeAndDoesNotFinish() {
        val settings = Nav.push(Nav.home(), GpRoute.Settings)
        val result = NavBack.onSystemBack(settings)
        assertEquals(GpRoute.Home, Nav.current(result.next))
        assertFalse(result.finishActivity)
    }

    @Test
    fun secondBackAtHomeDoesNotFinish() {
        val first = NavBack.onSystemBack(Nav.push(Nav.home(), GpRoute.Settings))
        val second = NavBack.onSystemBack(first.next)
        assertEquals(Nav.home(), second.next)
        assertFalse(second.finishActivity)
        assertFalse(Nav.canPop(second.next))
    }

    @Test
    fun backDismissesLaunchPromptOnly() {
        val prompted = Nav.setPrompt(Nav.push(Nav.home(), GpRoute.About), true)
        val result = NavBack.onSystemBack(prompted)
        assertFalse(result.next.promptOpen)
        assertEquals(GpRoute.About, Nav.current(result.next))
        assertFalse(result.finishActivity)
    }
}
