package dev.foss.goldenpath.settings

import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class SettingsSearchTest {
    @Test
    fun blankQueryShowsEverySection() {
        assertTrue(SettingsSearch.matches("  ", "Appearance", "Theme"))
    }

    @Test
    fun matchesAnyLabelIgnoringCase() {
        assertTrue(SettingsSearch.matches("THEME", "Appearance", "Theme"))
        assertFalse(SettingsSearch.matches("privacy", "Appearance", "Theme"))
    }
}
