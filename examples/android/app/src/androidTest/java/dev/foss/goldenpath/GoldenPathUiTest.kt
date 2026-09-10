package dev.foss.goldenpath

import androidx.compose.ui.test.assertCountEquals
import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.compose.ui.test.onAllNodesWithContentDescription
import androidx.compose.ui.test.onAllNodesWithTag
import androidx.compose.ui.test.onAllNodesWithText
import androidx.compose.ui.test.onNodeWithContentDescription
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import androidx.compose.ui.test.performScrollTo
import androidx.compose.ui.test.performTextClearance
import androidx.compose.ui.test.performTextInput
import androidx.test.espresso.Espresso
import dev.foss.goldenpath.ui.about.AboutTestTags
import org.junit.Rule
import org.junit.Test
import org.junit.rules.RuleChain

class GoldenPathUiTest {
    private val composeTestRule = createAndroidComposeRule<MainActivity>()

    @get:Rule
    val rules: RuleChain = RuleChain
        .outerRule(ClearUiPrefsRule())
        .around(FailureEvidenceRule { composeTestRule })
        .around(composeTestRule)

    @Test
    fun opensSettingsPanelWithThemeDropdown() {
        composeTestRule.dismissLaunchPrompts()
        composeTestRule.onNodeWithTag("home-status").assertIsDisplayed()
        composeTestRule.onAllNodesWithContentDescription("About").assertCountEquals(0)
        composeTestRule.onNodeWithContentDescription("Settings").performClick()
        composeTestRule.onNodeWithTag("settings-panel").assertIsDisplayed()
        composeTestRule.onNodeWithText("Settings").assertIsDisplayed()
        composeTestRule.onNodeWithText("Appearance").assertIsDisplayed()
        composeTestRule.onNodeWithText("Theme").assertIsDisplayed()
        composeTestRule.onNodeWithText("System theme").performClick()
        composeTestRule.onNodeWithText("Dark theme").performClick()
        composeTestRule.onNodeWithText("Data").performScrollTo().assertIsDisplayed()
        composeTestRule.onNodeWithTag("settings-export").performScrollTo().assertIsDisplayed()
        composeTestRule.onNodeWithTag("settings-import").performScrollTo().assertIsDisplayed()
        composeTestRule.onNodeWithText("Version, updates, and ways to support development")
            .assertIsDisplayed()
        composeTestRule.onNodeWithContentDescription("Back").performClick()
        composeTestRule.waitForIdle()
        composeTestRule.onNodeWithTag("home-status").assertIsDisplayed()
        // Home has no nav Back icon; system Back must stay in-app (NavBack finishActivity=false).
        Espresso.pressBack()
        composeTestRule.waitForIdle()
        composeTestRule.onNodeWithTag("home-status").assertIsDisplayed()
    }

    @Test
    fun settingsSearchHidesNonMatchingSections() {
        composeTestRule.dismissLaunchPrompts()
        composeTestRule.onNodeWithContentDescription("Settings").performClick()
        composeTestRule.onNodeWithTag("settings-search").performTextInput("privacy")
        composeTestRule.onNodeWithText("Privacy").assertIsDisplayed()
        composeTestRule.onNodeWithText("Appearance").assertDoesNotExist()
        composeTestRule.onNodeWithTag("settings-search").performTextClearance()
        composeTestRule.onNodeWithTag("settings-search").performTextInput("zzzz-no-match")
        composeTestRule.onNodeWithTag("settings-search-empty").assertIsDisplayed()
    }

    @Test
    fun opensAboutPanelWithVersion() {
        composeTestRule.dismissLaunchPrompts()
        composeTestRule.onNodeWithContentDescription("Settings").performClick()
        composeTestRule.onNodeWithText("App info").performScrollTo().performClick()
        composeTestRule.onNodeWithTag("about-panel").assertIsDisplayed()
        composeTestRule.onNodeWithText("About").assertIsDisplayed()
        composeTestRule.onNodeWithText("Installed format: apk").assertIsDisplayed()
    }

    @Test
    fun donateLivesUnderSettingsAboutNotTitlebar() {
        composeTestRule.dismissLaunchPrompts()
        // Titlebar / home must not expose About donation tags (dialog Venmo label is OK to ignore).
        composeTestRule.onAllNodesWithTag(AboutTestTags.DONATION_LINK).assertCountEquals(0)
        composeTestRule.onNodeWithContentDescription("Settings").performClick()
        composeTestRule.waitForIdle()
        composeTestRule.onNodeWithTag("settings-about").performScrollTo().performClick()
        composeTestRule.waitForIdle()
        composeTestRule.onNodeWithTag(AboutTestTags.DONATIONS_HEADING)
            .performScrollTo()
            .assertIsDisplayed()
        // Exemplar ships multiple methods; require at least Venmo + one international placeholder.
        val linkCount = composeTestRule.onAllNodesWithTag(AboutTestTags.DONATION_LINK)
            .fetchSemanticsNodes()
            .size
        check(linkCount >= 2) { "expected multiple donation links under About, got $linkCount" }
        composeTestRule.onAllNodesWithText("Donate via Venmo").assertCountEquals(1)
    }

    @Test
    fun opensFeedbackPanelFromAbout() {
        composeTestRule.dismissLaunchPrompts()
        composeTestRule.onNodeWithContentDescription("Settings").performClick()
        composeTestRule.onNodeWithTag("settings-about").performScrollTo().performClick()
        composeTestRule.onNodeWithText("Choose an action").performScrollTo().performClick()
        composeTestRule.onNodeWithText("Report a bug").performClick()
        composeTestRule.onNodeWithTag("feedback-panel").assertIsDisplayed()
        // Title + action chip both say "Report a bug"; require at least one visible.
        check(composeTestRule.onAllNodesWithText("Report a bug").fetchSemanticsNodes().isNotEmpty())
        // Stack is home → settings → about → feedback; Back pops each level; home Back is no-op.
        composeTestRule.onNodeWithContentDescription("Back").performClick()
        composeTestRule.waitForIdle()
        composeTestRule.onNodeWithTag("about-panel").assertIsDisplayed()
        composeTestRule.onNodeWithContentDescription("Back").performClick()
        composeTestRule.waitForIdle()
        composeTestRule.onNodeWithTag("settings-panel").assertIsDisplayed()
        composeTestRule.onNodeWithContentDescription("Back").performClick()
        composeTestRule.waitForIdle()
        composeTestRule.onNodeWithTag("home-status").assertIsDisplayed()
        Espresso.pressBack()
        composeTestRule.waitForIdle()
        composeTestRule.onNodeWithTag("home-status").assertIsDisplayed()
    }
}
