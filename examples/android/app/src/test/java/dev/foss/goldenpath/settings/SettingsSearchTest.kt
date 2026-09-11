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

    @Test
    fun matchesDiacriticsInsensitive() {
        assertTrue(SettingsSearch.matches("informacion", "Información"))
        assertTrue(SettingsSearch.matches("información", "Informacion"))
        assertTrue(SettingsSearch.matches("cafe", "Café"))
    }

    @Test
    fun fuzzyAllowsOneEditOnTokens() {
        assertTrue(SettingsSearch.fuzzyMatches("privcy", "Privacy", "crashes"))
        assertTrue(SettingsSearch.fuzzyMatches("theeme", "Appearance", "Theme"))
        assertFalse(SettingsSearch.fuzzyMatches("zzzz", "Appearance", "Theme"))
    }
}
