package dev.foss.goldenpath

import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.v2.createAndroidComposeRule
import androidx.compose.ui.test.onNodeWithContentDescription
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import androidx.compose.ui.test.performScrollTo
import org.junit.Rule
import org.junit.Test
import org.junit.rules.RuleChain

/** Smoke: tapping a donate link must not crash (ACTION_VIEW Intent fire). */
class DonateLinkUiTest {
    private val composeTestRule = createAndroidComposeRule<MainActivity>()

    @get:Rule
    val rules: RuleChain = RuleChain
        .outerRule(ClearUiPrefsRule())
        .around(DisableAnimationsRule())
        .around(FailureEvidenceRule { composeTestRule })
        .around(composeTestRule)

    @Test
    fun donateLinkClickStaysOnAbout() {
        composeTestRule.dismissLaunchPrompts()
        composeTestRule.onNodeWithContentDescription("Settings").performClick()
        composeTestRule.onNodeWithTag("settings-about").performScrollTo().performClick()
        composeTestRule.onNodeWithTag("about-panel").assertIsDisplayed()
        composeTestRule.onNodeWithText("Donate via Venmo").performScrollTo().performClick()
        composeTestRule.waitForIdle()
        // Browser may or may not open; About must remain the active route.
        composeTestRule.onNodeWithTag("about-panel").assertIsDisplayed()
    }
}
