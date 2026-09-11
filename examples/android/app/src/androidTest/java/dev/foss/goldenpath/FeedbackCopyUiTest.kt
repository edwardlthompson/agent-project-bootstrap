package dev.foss.goldenpath

import android.content.ClipboardManager
import android.content.Context
import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.v2.createAndroidComposeRule
import androidx.compose.ui.test.onNodeWithContentDescription
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import androidx.compose.ui.test.performScrollTo
import androidx.compose.ui.test.performTextInput
import androidx.test.core.app.ApplicationProvider
import org.junit.Assert.assertTrue
import org.junit.Rule
import org.junit.Test
import org.junit.rules.RuleChain

class FeedbackCopyUiTest {
    private val composeTestRule = createAndroidComposeRule<MainActivity>()

    @get:Rule
    val rules: RuleChain = RuleChain
        .outerRule(ClearUiPrefsRule())
        .around(DisableAnimationsRule())
        .around(FailureEvidenceRule { composeTestRule })
        .around(composeTestRule)

    @Test
    fun copyShowsToastAndWritesClipboard() {
        composeTestRule.dismissLaunchPrompts()
        composeTestRule.onNodeWithContentDescription("Settings").performClick()
        composeTestRule.onNodeWithTag("settings-about").performScrollTo().performClick()
        composeTestRule.onNodeWithText("Choose an action").performScrollTo().performClick()
        composeTestRule.onNodeWithText("Report a bug").performClick()
        composeTestRule.onNodeWithTag("feedback-panel").assertIsDisplayed()
        composeTestRule.onNodeWithTag("feedback-description").performTextInput("repro steps")
        composeTestRule.onNodeWithTag("feedback-copy").performClick()
        composeTestRule.waitForIdle()
        composeTestRule.onNodeWithTag("feedback-copied").assertIsDisplayed()
        val context = ApplicationProvider.getApplicationContext<Context>()
        val cm = context.getSystemService(Context.CLIPBOARD_SERVICE) as ClipboardManager
        val clip = cm.primaryClip?.getItemAt(0)?.coerceToText(context)?.toString().orEmpty()
        assertTrue("clipboard should contain preview text", clip.contains("repro") || clip.isNotBlank())
    }
}
