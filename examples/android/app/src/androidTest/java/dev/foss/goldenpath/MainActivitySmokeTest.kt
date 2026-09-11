package dev.foss.goldenpath

import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.v2.createAndroidComposeRule
import androidx.compose.ui.test.onNodeWithTag
import androidx.test.ext.junit.runners.AndroidJUnit4
import org.junit.Assert.assertEquals
import org.junit.Rule
import org.junit.Test
import org.junit.rules.RuleChain
import org.junit.runner.RunWith

/**
 * Smoke tests use Compose [createAndroidComposeRule] (UI Test v2) so Activity + Compose share one rule.
 * Remaining androidTest classes already migrated; LocaleRtlUiTest stays resource-only (no Activity).
 */
@RunWith(AndroidJUnit4::class)
class MainActivitySmokeTest {
    private val composeTestRule = createAndroidComposeRule<MainActivity>()

    @get:Rule
    val rules: RuleChain = RuleChain
        .outerRule(ClearUiPrefsRule())
        .around(FailureEvidenceRule { composeTestRule })
        .around(composeTestRule)

    @Test
    fun launchesMainActivity() {
        composeTestRule.dismissLaunchPrompts()
        composeTestRule.activityRule.scenario.onActivity { activity ->
            check(!activity.isFinishing)
        }
        composeTestRule.onNodeWithTag("home-status").assertIsDisplayed()
    }

    @Test
    fun prefersFastestSameResolutionDisplayMode() {
        composeTestRule.activityRule.scenario.onActivity { activity ->
            val display = activity.display ?: return@onActivity
            val current = display.mode
            val expected = display.supportedModes
                .filter {
                    it.physicalWidth == current.physicalWidth &&
                        it.physicalHeight == current.physicalHeight
                }
                .maxByOrNull { it.refreshRate }
                ?.modeId
                ?: return@onActivity
            assertEquals(expected, activity.window.attributes.preferredDisplayModeId)
        }
    }
}
