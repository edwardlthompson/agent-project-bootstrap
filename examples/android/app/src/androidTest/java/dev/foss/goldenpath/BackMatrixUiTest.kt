package dev.foss.goldenpath

import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.v2.createAndroidComposeRule
import androidx.compose.ui.test.onNodeWithContentDescription
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.performClick
import androidx.compose.ui.test.performScrollTo
import androidx.test.espresso.Espresso
import org.junit.Rule
import org.junit.Test
import org.junit.rules.RuleChain

/** System Back vs toolbar nav-icon Back must both pop one route. */
class BackMatrixUiTest {
    private val composeTestRule = createAndroidComposeRule<MainActivity>()

    @get:Rule
    val rules: RuleChain = RuleChain
        .outerRule(ClearUiPrefsRule())
        .around(DisableAnimationsRule())
        .around(FailureEvidenceRule { composeTestRule })
        .around(composeTestRule)

    @Test
    fun navIconBackPopsSettingsToHome() {
        composeTestRule.dismissLaunchPrompts()
        composeTestRule.onNodeWithContentDescription("Settings").performClick()
        composeTestRule.onNodeWithTag("settings-panel").assertIsDisplayed()
        composeTestRule.onNodeWithContentDescription("Back").performClick()
        composeTestRule.waitForIdle()
        composeTestRule.onNodeWithTag("home-status").assertIsDisplayed()
    }

    @Test
    fun systemBackPopsSettingsToHome() {
        composeTestRule.dismissLaunchPrompts()
        composeTestRule.onNodeWithContentDescription("Settings").performClick()
        composeTestRule.onNodeWithTag("settings-panel").assertIsDisplayed()
        Espresso.pressBack()
        composeTestRule.waitForIdle()
        composeTestRule.onNodeWithTag("home-status").assertIsDisplayed()
    }

    @Test
    fun navIconAndSystemBackAgreeOnAboutStack() {
        composeTestRule.dismissLaunchPrompts()
        composeTestRule.onNodeWithContentDescription("Settings").performClick()
        composeTestRule.onNodeWithTag("settings-about").performScrollTo().performClick()
        composeTestRule.onNodeWithTag("about-panel").assertIsDisplayed()
        composeTestRule.onNodeWithContentDescription("Back").performClick()
        composeTestRule.waitForIdle()
        composeTestRule.onNodeWithTag("settings-panel").assertIsDisplayed()
        Espresso.pressBack()
        composeTestRule.waitForIdle()
        composeTestRule.onNodeWithTag("home-status").assertIsDisplayed()
    }
}
