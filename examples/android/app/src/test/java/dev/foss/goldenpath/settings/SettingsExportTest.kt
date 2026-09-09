package dev.foss.goldenpath.settings

import dev.foss.goldenpath.ui.theme.ThemeMode
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNull
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [26])
class SettingsExportTest {
    @Test
    fun roundtripsThemeAndSaveCrashes() {
        val json = SettingsExport.toJson(SettingsExport.snapshot(ThemeMode.Light, true))
        val parsed = SettingsExport.parse(json)
        assertEquals(SettingsBundle(1, ThemeMode.Light, true), parsed)
    }

    @Test
    fun acceptsWebWireThemeNames() {
        val parsed = SettingsExport.parse(
            """{"version":1,"theme":"dark","saveCrashes":false}""",
        )
        assertEquals(SettingsBundle(1, ThemeMode.Dark, false), parsed)
    }

    @Test
    fun rejectsInvalidPayload() {
        assertNull(SettingsExport.parse("{"))
        assertNull(SettingsExport.parse("""{"version":2,"theme":"dark"}"""))
        assertNull(SettingsExport.parse("""{"version":1,"theme":"neon"}"""))
    }
}
