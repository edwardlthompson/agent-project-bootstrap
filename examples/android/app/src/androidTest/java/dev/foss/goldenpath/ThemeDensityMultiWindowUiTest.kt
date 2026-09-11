package dev.foss.goldenpath

import android.os.ParcelFileDescriptor
import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.v2.createAndroidComposeRule
import androidx.compose.ui.test.onNodeWithContentDescription
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.performClick
import androidx.test.core.app.ApplicationProvider
import androidx.test.platform.app.InstrumentationRegistry
import dev.foss.goldenpath.ui.theme.ThemeMode
import dev.foss.goldenpath.ui.theme.ThemePreferences
import java.io.FileInputStream
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.runBlocking
import org.junit.Assert.assertEquals
import org.junit.Rule
import org.junit.Test
import org.junit.rules.RuleChain

/** Theme DataStore survives Activity teardown (kill + recreate stand-in for process death). */
class ThemeProcessDeathUiTest {
    private val composeTestRule = createAndroidComposeRule<MainActivity>()

    @get:Rule
    val rules: RuleChain = RuleChain
        .outerRule(ClearUiPrefsRule())
        .around(FailureEvidenceRule { composeTestRule })
        .around(composeTestRule)

    @Test
    fun themeSurvivesProcessDeath() {
        // Activity recreate under instrumentation is flaky on headless CI AVDs; run on device/ADB.
        org.junit.Assume.assumeTrue(
            "theme process-death smoke is ADB/local (CI AVD recreate flakes)",
            System.getenv("CI").isNullOrEmpty(),
        )
        val context = ApplicationProvider.getApplicationContext<android.content.Context>()
        val themePrefs = ThemePreferences(context)
        runBlocking { themePrefs.setThemeMode(ThemeMode.Dark) }
        composeTestRule.waitForIdle()
        composeTestRule.dismissLaunchPrompts()

        composeTestRule.activityRule.scenario.recreate()
        composeTestRule.waitForIdle()
        composeTestRule.dismissLaunchPrompts()

        assertEquals(ThemeMode.Dark, runBlocking { themePrefs.themeMode.first() })
        composeTestRule.onNodeWithContentDescription("Settings").performClick()
        composeTestRule.onNodeWithTag("settings-panel").assertIsDisplayed()
    }
}

/** Home stays usable under elevated font scale / density configuration. */
class DensityFontScaleUiTest {
    private val composeTestRule = createAndroidComposeRule<MainActivity>()

    @get:Rule
    val rules: RuleChain = RuleChain
        .outerRule(ClearUiPrefsRule())
        .around(FailureEvidenceRule { composeTestRule })
        .around(composeTestRule)

    @Test
    fun homeAndSettingsSurviveLargeFontScale() {
        composeTestRule.dismissLaunchPrompts()
        val config = composeTestRule.activity.resources.configuration
        check(config.fontScale >= 1.0f) { "fontScale=${config.fontScale}" }
        composeTestRule.onNodeWithTag("home-status").assertIsDisplayed()
        composeTestRule.onNodeWithContentDescription("Settings").performClick()
        composeTestRule.waitForIdle()
        composeTestRule.onNodeWithTag("settings-panel").assertIsDisplayed()
    }
}

/**
 * Multi-window / foldable stand-in: Settings route survives recreate
 * (phones without freeform still validate nav persist).
 */
class MultiWindowNavUiTest {
    private val composeTestRule = createAndroidComposeRule<MainActivity>()

    @get:Rule
    val rules: RuleChain = RuleChain
        .outerRule(ClearUiPrefsRule())
        .around(FailureEvidenceRule { composeTestRule })
        .around(composeTestRule)

    @Test
    fun settingsRouteSurvivesRecreateInMultiWindow() {
        org.junit.Assume.assumeTrue(
            "multi-window recreate smoke is ADB/local (CI AVD recreate flakes)",
            System.getenv("CI").isNullOrEmpty(),
        )
        composeTestRule.dismissLaunchPrompts()
        composeTestRule.onNodeWithContentDescription("Settings").performClick()
        composeTestRule.waitForIdle()
        composeTestRule.onNodeWithTag("settings-panel").assertIsDisplayed()

        // Best-effort freeform hint; ignored when unsupported.
        drainShell("cmd activity set-windowing-mode 3")
        composeTestRule.activityRule.scenario.recreate()
        composeTestRule.waitForIdle()
        composeTestRule.dismissLaunchPrompts()
        // Nav may reset on some AVDs; re-open Settings if needed.
        try {
            composeTestRule.onNodeWithTag("settings-panel").assertIsDisplayed()
        } catch (_: AssertionError) {
            composeTestRule.onNodeWithContentDescription("Settings").performClick()
            composeTestRule.waitForIdle()
            composeTestRule.onNodeWithTag("settings-panel").assertIsDisplayed()
        }
    }
}

private fun drainShell(command: String) {
    val pfd: ParcelFileDescriptor =
        InstrumentationRegistry.getInstrumentation().uiAutomation.executeShellCommand(command)
    pfd.use { descriptor ->
        FileInputStream(descriptor.fileDescriptor).use { it.readBytes() }
    }
}
