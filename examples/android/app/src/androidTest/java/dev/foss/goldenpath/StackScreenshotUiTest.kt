package dev.foss.goldenpath

import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.v2.createAndroidComposeRule
import androidx.compose.ui.test.onNodeWithContentDescription
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import androidx.compose.ui.test.performScrollTo
import androidx.test.platform.app.InstrumentationRegistry
import org.junit.Assert.assertTrue
import org.junit.Rule
import org.junit.Test
import org.junit.rules.RuleChain

/** Screenshot regression for Settings → About → Feedback stack (capture + non-blank / size). */
class StackScreenshotUiTest {
    private val composeTestRule = createAndroidComposeRule<MainActivity>()

    @get:Rule
    val rules: RuleChain = RuleChain
        .outerRule(ClearUiPrefsRule())
        .around(FailureEvidenceRule { composeTestRule })
        .around(composeTestRule)

    @Test
    fun settingsAboutFeedbackScreenshotsAreNonBlank() {
        composeTestRule.dismissLaunchPrompts()
        composeTestRule.onNodeWithContentDescription("Settings").performClick()
        composeTestRule.onNodeWithTag("settings-panel").assertIsDisplayed()
        assertScreenshotUseful("settings")

        composeTestRule.onNodeWithTag("settings-about").performScrollTo().performClick()
        composeTestRule.waitForIdle()
        composeTestRule.onNodeWithTag("about-panel").assertIsDisplayed()
        assertScreenshotUseful("about")

        composeTestRule.onNodeWithText("Choose an action").performScrollTo().performClick()
        composeTestRule.onNodeWithText("Report a bug").performClick()
        composeTestRule.onNodeWithTag("feedback-panel").assertIsDisplayed()
        assertScreenshotUseful("feedback")
    }

    private fun assertScreenshotUseful(label: String) {
        composeTestRule.waitForIdle()
        val bitmap = InstrumentationRegistry.getInstrumentation().uiAutomation.takeScreenshot()
        check(bitmap != null) { "screenshot null for $label" }
        try {
            assertTrue("$label width", bitmap.width >= 200)
            assertTrue("$label height", bitmap.height >= 200)
            val sample = bitmap.getPixel(bitmap.width / 2, bitmap.height / 2)
            // Reject fully transparent captures.
            assertTrue("$label alpha", (sample ushr 24) > 0)
        } finally {
            bitmap.recycle()
        }
    }
}
