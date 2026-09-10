package dev.foss.goldenpath

import androidx.compose.ui.input.key.Key
import androidx.compose.ui.test.assertHasClickAction
import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.compose.ui.test.onNodeWithContentDescription
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.performKeyInput
import androidx.compose.ui.test.pressKey
import androidx.compose.ui.test.requestFocus
import org.junit.Rule
import org.junit.Test
import org.junit.rules.RuleChain

class TalkBackKeyboardUiTest {
    private val composeTestRule = createAndroidComposeRule<MainActivity>()

    @get:Rule
    val rules: RuleChain = RuleChain
        .outerRule(ClearUiPrefsRule())
        .around(FailureEvidenceRule { composeTestRule })
        .around(composeTestRule)

    @Test
    fun settingsAndBackExposeTalkBackNames() {
        composeTestRule.dismissLaunchPrompts()
        composeTestRule.onNodeWithContentDescription("Settings")
            .assertIsDisplayed()
            .assertHasClickAction()
        composeTestRule.onNodeWithTag("home-status").assertIsDisplayed()
    }

    @Test
    fun enterKeyOpensSettingsThenBackIsLabeled() {
        composeTestRule.dismissLaunchPrompts()
        val settings = composeTestRule.onNodeWithContentDescription("Settings")
        settings.requestFocus()
        settings.performKeyInput { pressKey(Key.Enter) }
        composeTestRule.waitForIdle()
        composeTestRule.onNodeWithTag("settings-panel").assertIsDisplayed()
        composeTestRule.onNodeWithContentDescription("Back")
            .assertIsDisplayed()
            .assertHasClickAction()
    }
}
