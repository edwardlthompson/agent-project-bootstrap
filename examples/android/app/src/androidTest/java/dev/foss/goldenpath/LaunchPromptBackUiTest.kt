package dev.foss.goldenpath

import android.content.Context
import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.v2.createAndroidComposeRule
import androidx.compose.ui.test.onAllNodesWithText
import androidx.compose.ui.test.onNodeWithContentDescription
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.performClick
import androidx.test.core.app.ApplicationProvider
import androidx.test.espresso.Espresso
import dev.foss.goldenpath.about.UpdateLaunchPrefs
import org.junit.Rule
import org.junit.Test
import org.junit.rules.RuleChain
import org.junit.rules.TestWatcher
import org.junit.runner.Description

/** Seeds a donate nudge so the launch dialog is on screen for Back assertions. */
class SeedDonatePromptRule : TestWatcher() {
    override fun starting(description: Description) {
        val context = ApplicationProvider.getApplicationContext<Context>()
        context.getSharedPreferences(UpdateLaunchPrefs.PREFS, Context.MODE_PRIVATE)
            .edit()
            .putString("last_seen_version", "0.0.0-seed")
            .commit()
    }
}

class LaunchPromptBackUiTest {
    private val composeTestRule = createAndroidComposeRule<MainActivity>()

    @get:Rule
    val rules: RuleChain = RuleChain
        .outerRule(ClearUiPrefsRule())
        .around(SeedDonatePromptRule())
        .around(DisableAnimationsRule())
        .around(FailureEvidenceRule { composeTestRule })
        .around(composeTestRule)

    @Test
    fun systemBackDismissesPromptWithoutLeavingHome() {
        composeTestRule.waitForIdle()
        check(composeTestRule.onAllNodesWithText("Not now").fetchSemanticsNodes().isNotEmpty()) {
            "expected donate launch prompt"
        }
        composeTestRule.onNodeWithTag("home-status").assertIsDisplayed()
        Espresso.pressBack()
        composeTestRule.waitForIdle()
        composeTestRule.onNodeWithTag("home-status").assertIsDisplayed()
        check(composeTestRule.onAllNodesWithText("Not now").fetchSemanticsNodes().isEmpty()) {
            "prompt should dismiss on Back"
        }
        composeTestRule.onNodeWithContentDescription("Settings").assertIsDisplayed()
    }
}
