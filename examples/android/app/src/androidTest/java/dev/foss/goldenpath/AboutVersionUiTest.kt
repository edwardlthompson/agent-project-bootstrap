package dev.foss.goldenpath

import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.v2.createAndroidComposeRule
import androidx.compose.ui.test.onNodeWithContentDescription
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import androidx.compose.ui.test.performScrollTo
import dev.foss.goldenpath.BuildConfig
import org.junit.Rule
import org.junit.Test
import org.junit.rules.RuleChain

/** About version string comes from package BuildConfig (schemas/golden-path/app-version.json). */
class AboutVersionUiTest {
    private val composeTestRule = createAndroidComposeRule<MainActivity>()

    @get:Rule
    val rules: RuleChain = RuleChain
        .outerRule(ClearUiPrefsRule())
        .around(FailureEvidenceRule { composeTestRule })
        .around(composeTestRule)

    @Test
    fun aboutShowsPackageVersionName() {
        composeTestRule.dismissLaunchPrompts()
        composeTestRule.onNodeWithContentDescription("Settings").performClick()
        composeTestRule.onNodeWithTag("settings-about").performScrollTo().performClick()
        composeTestRule.waitForIdle()
        composeTestRule.onNodeWithTag("about-panel").assertIsDisplayed()
        composeTestRule.onNodeWithText("Version: ${BuildConfig.VERSION_NAME}")
            .assertIsDisplayed()
    }
}
