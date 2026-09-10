package dev.foss.goldenpath.memory

import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

class MemoryBudgetTest {
    @Test
    fun limiterKillRequiresReasonOtherAndMarker() {
        assertTrue(
            MemoryBudget.isLimiterKill(
                MemoryBudget.REASON_OTHER,
                "foo MemoryLimiter:AnonSwap bar",
            ),
        )
    }

    @Test
    fun nullOrBlankDescriptionIsNotLimiterKill() {
        assertFalse(MemoryBudget.isLimiterKill(MemoryBudget.REASON_OTHER, null))
        assertFalse(MemoryBudget.isLimiterKill(MemoryBudget.REASON_OTHER, "  "))
        assertFalse(MemoryBudget.isLimiterKill(MemoryBudget.REASON_OTHER, ""))
    }

    @Test
    fun otherReasonsAreNotLimiterKills() {
        assertFalse(MemoryBudget.isLimiterKill(10, "MemoryLimiter:AnonSwap"))
    }

    @Test
    fun firstLimiterKillSkipsEmptyExits() {
        assertNull(MemoryBudget.firstLimiterKill(emptyList()))
        val miss = MemoryBudget.ExitHint(1, "oom")
        val hit = MemoryBudget.ExitHint(MemoryBudget.REASON_OTHER, MemoryBudget.LIMITER_MARKER)
        assertEquals(hit, MemoryBudget.firstLimiterKill(listOf(miss, hit)))
    }

    @Test
    fun trimHintUsesUiHiddenAndBackgroundOnly() {
        assertEquals(MemoryBudget.TrimHint.NONE, MemoryBudget.trimHint(5))
        assertEquals(MemoryBudget.TrimHint.UI, MemoryBudget.trimHint(MemoryBudget.TRIM_UI_HIDDEN))
        assertEquals(
            MemoryBudget.TrimHint.BACKGROUND,
            MemoryBudget.trimHint(MemoryBudget.TRIM_BACKGROUND),
        )
        assertTrue(MemoryBudget.shouldReleaseUi(MemoryBudget.TRIM_BACKGROUND))
    }
}
