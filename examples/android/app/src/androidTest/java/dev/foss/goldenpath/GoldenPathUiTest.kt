package dev.foss.goldenpath

import androidx.compose.ui.test.assertCountEquals
import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.compose.ui.test.onAllNodesWithText
import androidx.compose.ui.test.onNodeWithContentDescription
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import org.junit.Rule
import org.junit.Test

class GoldenPathUiTest {
    @get:Rule
    val composeTestRule = createAndroidComposeRule<MainActivity>()

    @Test
    fun opensSettingsPanelWithThemeAndUpdateControls() {
        composeTestRule.onNodeWithContentDescription("Settings").performClick()
        composeTestRule.onNodeWithText("Settings").assertIsDisplayed()
        composeTestRule.onNodeWithText("Theme").assertIsDisplayed()
        composeTestRule.onNodeWithText("Dark theme").performClick()
        composeTestRule.onNodeWithText("Close settings").performClick()
    }

    @Test
    fun opensAboutPanelWithVersion() {
        composeTestRule.onNodeWithContentDescription("About").performClick()
        composeTestRule.onNodeWithText("About").assertIsDisplayed()
        composeTestRule.onNodeWithText("Installed format: apk").assertIsDisplayed()
    }

    @Test
    fun donateLivesUnderSettingsAboutNotTitlebar() {
        // Titlebar must not show donate; assertCountEquals avoids assertDoesNotExist import gaps.
        composeTestRule.onAllNodesWithText("Donate via Venmo").assertCountEquals(0)
        composeTestRule.onNodeWithContentDescription("Settings").performClick()
        composeTestRule.onNodeWithText("About", substring = false).performClick()
        composeTestRule.onNodeWithText("Support development").assertIsDisplayed()
        composeTestRule.onNodeWithText("Donate via Venmo").assertIsDisplayed()
    }
}
