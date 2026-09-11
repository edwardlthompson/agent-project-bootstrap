package dev.foss.goldenpath

import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.v2.createAndroidComposeRule
import androidx.compose.ui.test.onNodeWithContentDescription
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import androidx.test.core.app.ApplicationProvider
import dev.foss.goldenpath.feedback.FeedbackPrefs
import dev.foss.goldenpath.settings.SettingsBundle
import dev.foss.goldenpath.settings.SettingsExport
import dev.foss.goldenpath.ui.theme.ThemeMode
import dev.foss.goldenpath.ui.theme.ThemePreferences
import java.io.File
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.runBlocking
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Rule
import org.junit.Test
import org.junit.rules.RuleChain

/** Instrumented Settings Data export/import round-trip (JSON file + prefs apply). */
class SettingsExportImportUiTest {
    private val composeTestRule = createAndroidComposeRule<MainActivity>()

    @get:Rule
    val rules: RuleChain = RuleChain
        .outerRule(ClearUiPrefsRule())
        .around(FailureEvidenceRule { composeTestRule })
        .around(composeTestRule)

    @Test
    fun exportImportRoundTripRestoresThemeAndSaveCrashes() {
        val context = ApplicationProvider.getApplicationContext<android.content.Context>()
        val themePrefs = ThemePreferences(context)
        val feedbackPrefs = FeedbackPrefs(context)

        runBlocking {
            themePrefs.setThemeMode(ThemeMode.Dark)
            feedbackPrefs.setSaveCrashes(true)
        }
        composeTestRule.activityRule.scenario.recreate()
        composeTestRule.waitForIdle()
        composeTestRule.dismissLaunchPrompts()

        val exported = SettingsExport.toJson(
            SettingsExport.snapshot(
                runBlocking { themePrefs.themeMode.first() },
                feedbackPrefs.saveCrashes(),
            ),
        )
        val file = File(context.filesDir, "settings-export-roundtrip.json")
        file.writeText(exported)

        runBlocking {
            themePrefs.setThemeMode(ThemeMode.Light)
            feedbackPrefs.setSaveCrashes(false)
        }
        composeTestRule.activityRule.scenario.recreate()
        composeTestRule.waitForIdle()
        composeTestRule.dismissLaunchPrompts()
        assertEquals(ThemeMode.Light, runBlocking { themePrefs.themeMode.first() })
        assertEquals(false, feedbackPrefs.saveCrashes())

        val bundle = SettingsExport.parse(file.readText())
        check(bundle != null) { "import parse failed" }
        assertEquals(SettingsBundle(1, ThemeMode.Dark, true), bundle)
        runBlocking {
            themePrefs.setThemeMode(bundle.theme)
            feedbackPrefs.setSaveCrashes(bundle.saveCrashes)
        }
        composeTestRule.activityRule.scenario.recreate()
        composeTestRule.waitForIdle()
        composeTestRule.dismissLaunchPrompts()

        assertEquals(ThemeMode.Dark, runBlocking { themePrefs.themeMode.first() })
        assertTrue(feedbackPrefs.saveCrashes())

        composeTestRule.onNodeWithContentDescription("Settings").performClick()
        composeTestRule.onNodeWithTag("settings-panel").assertIsDisplayed()
        composeTestRule.onNodeWithTag("settings-export").assertIsDisplayed()
        composeTestRule.onNodeWithTag("settings-import").assertIsDisplayed()
        composeTestRule.onNodeWithText("Dark theme").assertIsDisplayed()
    }
}
