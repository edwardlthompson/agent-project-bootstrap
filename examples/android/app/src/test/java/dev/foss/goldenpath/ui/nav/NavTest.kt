package dev.foss.goldenpath.ui.nav

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class NavTest {
    @Test
    fun pushSameTopIsNoOp() {
        val about = Nav.push(Nav.home(), GpRoute.About)
        assertEquals(about, Nav.push(about, GpRoute.About))
    }

    @Test
    fun openingAPanelPushes() {
        val next = Nav.push(Nav.home(), GpRoute.Settings)
        assertEquals(GpRoute.Settings, Nav.current(next))
        assertTrue(Nav.canPop(next))
    }

    @Test
    fun popOneLevelNeverGoesBelowHome() {
        val settings = Nav.push(Nav.home(), GpRoute.Settings)
        assertEquals(GpRoute.Home, Nav.current(Nav.pop(settings)))
        assertEquals(Nav.home(), Nav.pop(Nav.home()))
        assertFalse(Nav.canPop(Nav.home()))
    }

    @Test
    fun aboutThenReportBugPushesFeedbackBackReturnsToAboutThenHome() {
        val about = Nav.push(Nav.home(), GpRoute.About)
        val feedback = Nav.push(about, GpRoute.Feedback, FeedbackKind.Bug)
        assertEquals(listOf(GpRoute.Home, GpRoute.About, GpRoute.Feedback), feedback.stack)
        assertEquals(FeedbackKind.Bug, feedback.feedbackKind)
        val backAbout = Nav.pop(feedback)
        assertEquals(GpRoute.About, Nav.current(backAbout))
        assertEquals(listOf(GpRoute.Home, GpRoute.About), backAbout.stack)
        assertEquals(GpRoute.Home, Nav.current(Nav.pop(backAbout)))
    }

    @Test
    fun popDismissesLaunchPromptBeforePoppingARoute() {
        val prompted = Nav.setPrompt(Nav.push(Nav.home(), GpRoute.About), true)
        val dismissed = Nav.pop(prompted)
        assertFalse(dismissed.promptOpen)
        assertEquals(GpRoute.About, Nav.current(dismissed))
        assertEquals(GpRoute.Home, Nav.current(Nav.pop(dismissed)))
    }

    @Test
    fun serializeDeserializeRoundtripKeepsStackKindScrollAndPrompt() {
        var state = Nav.recordScroll(
            Nav.push(Nav.push(Nav.home(), GpRoute.About), GpRoute.Feedback, FeedbackKind.Feature),
            GpRoute.About,
            80,
        )
        state = Nav.setPrompt(state, true)
        val restored = NavJson.deserialize(NavJson.serialize(state))
        assertEquals(listOf(GpRoute.Home, GpRoute.About, GpRoute.Feedback), restored.stack)
        assertEquals(FeedbackKind.Feature, restored.feedbackKind)
        assertEquals(80, Nav.restoreScroll(restored, GpRoute.About))
        assertTrue(restored.promptOpen)
    }

    @Test
    fun deserializeInvalidOrEmptyReturnsHome() {
        assertEquals(Nav.home(), NavJson.deserialize(""))
        assertEquals(Nav.home(), NavJson.deserialize("{"))
        assertEquals(Nav.home(), NavJson.deserialize("null"))
    }

    @Test
    fun restoreScrollReadsSettingsAboutFeedbackAndIgnoresHome() {
        val withScroll = Nav.recordScroll(Nav.recordScroll(Nav.home(), GpRoute.Settings, 12), GpRoute.Home, 99)
        assertEquals(12, Nav.restoreScroll(withScroll, GpRoute.Settings))
        assertEquals(0, Nav.restoreScroll(withScroll, GpRoute.Home))
        assertEquals(0, Nav.restoreScroll(Nav.home(), GpRoute.About))
    }
}
