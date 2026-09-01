package dev.foss.goldenpath.ui.nav

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Test

class NavStoreTest {
    @Test
    fun saveLoadStripsPromptAndKeepsStackScroll() {
        val about = Nav.recordScroll(Nav.push(Nav.home(), GpRoute.About), GpRoute.About, 24)
        val prompted = Nav.setPrompt(about, true)
        val restored = NavStore.load(NavStore.save(prompted))
        assertEquals(listOf(GpRoute.Home, GpRoute.About), restored.stack)
        assertEquals(24, Nav.restoreScroll(restored, GpRoute.About))
        assertFalse(restored.promptOpen)
    }

    @Test
    fun bootPushesCrashFeedbackOnRestoredAbout() {
        val stored = Nav.push(Nav.home(), GpRoute.About)
        val booted = NavSession.boot(stored, crashPending = true)
        assertEquals(listOf(GpRoute.Home, GpRoute.About, GpRoute.Feedback), booted.stack)
        assertEquals(FeedbackKind.Bug, booted.feedbackKind)
        assertFalse(booted.promptOpen)
    }
}
