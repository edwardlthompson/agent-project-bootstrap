package dev.foss.goldenpath

import androidx.compose.ui.test.assertCountEquals
import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.compose.ui.test.onAllNodesWithTag
import androidx.compose.ui.test.onAllNodesWithText
import androidx.compose.ui.test.onNodeWithContentDescription
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import androidx.compose.ui.test.performScrollTo
import dev.foss.goldenpath.ui.about.AboutTestTags
import org.junit.Rule
import org.junit.Test
import org.junit.rules.RuleChain

class GoldenPathUiTest {
    private val composeTestRule = createAndroidComposeRule<MainActivity>()

    @get:Rule
    val rules: RuleChain = RuleChain
        .outerRule(FailureEvidenceRule { composeTestRule })
        .around(composeTestRule)

    @Test
    fun opensSettingsPanelWithThemeAndUpdateControls() {
        composeTestRule.onNodeWithContentDescription("Settings").performClick()
        composeTestRule.onNodeWithText("Settings").assertIsDisplayed()
        composeTestRule.onNodeWithText("Theme").assertIsDisplayed()
        composeTestRule.onNodeWithText("Version, updates, and ways to support development")
            .assertIsDisplayed()
        composeTestRule.onNodeWithText("Dark theme").performClick()
        composeTestRule.onNodeWithText("Close settings").performScrollTo().performClick()
    }

    @Test
    fun opensAboutPanelWithVersion() {
        composeTestRule.onNodeWithContentDescription("About").performClick()
        composeTestRule.onNodeWithText("About").assertIsDisplayed()
        composeTestRule.onNodeWithText("Installed format: apk").assertIsDisplayed()
    }

    @Test
    fun donateLivesUnderSettingsAboutNotTitlebar() {
        // Titlebar must not expose About donation tags.
        composeTestRule.onAllNodesWithTag(AboutTestTags.DONATION_LINK).assertCountEquals(0)
        composeTestRule.onNodeWithContentDescription("Settings").performClick()
        composeTestRule.waitForIdle()
        composeTestRule.onNodeWithText("About", substring = false).performScrollTo().performClick()
        composeTestRule.waitForIdle()
        composeTestRule.onNodeWithTag(AboutTestTags.DONATIONS_HEADING)
            .performScrollTo()
            .assertIsDisplayed()
        composeTestRule.onAllNodesWithTag(AboutTestTags.DONATION_LINK).assertCountEquals(5)
        composeTestRule.onAllNodesWithText("Donate via Venmo").assertCountEquals(1)
    }
}
