package dev.foss.goldenpath

import androidx.compose.ui.test.assertIsDisplayed
import androidx.compose.ui.test.junit4.createAndroidComposeRule
import androidx.compose.ui.test.onNodeWithContentDescription
import androidx.compose.ui.test.onNodeWithTag
import androidx.compose.ui.test.onNodeWithText
import androidx.compose.ui.test.performClick
import androidx.compose.ui.test.performScrollTo
import androidx.core.view.ViewCompat
import androidx.core.view.WindowInsetsCompat
import androidx.test.platform.app.InstrumentationRegistry
import dev.foss.goldenpath.ui.insets.NavigationMode
import dev.foss.goldenpath.ui.insets.readNavigationMode
import org.junit.Assert.assertTrue
import org.junit.Assume
import org.junit.Rule
import org.junit.Test
import org.junit.rules.RuleChain

class NavBarInsetUiTest {
    private val composeTestRule = createAndroidComposeRule<MainActivity>()

    @get:Rule
    val rules: RuleChain = RuleChain
        .outerRule(ClearUiPrefsRule())
        .around(FailureEvidenceRule { composeTestRule })
        .around(composeTestRule)

    private fun setNavigationMode(mode: Int) {
        InstrumentationRegistry.getInstrumentation().uiAutomation.executeShellCommand(
            "settings put secure navigation_mode $mode",
        )
        composeTestRule.activityRule.scenario.recreate()
        composeTestRule.waitForIdle()
        composeTestRule.dismissLaunchPrompts()
    }

    private fun openSettingsAndScrollToAbout() {
        composeTestRule.dismissLaunchPrompts()
        composeTestRule.onNodeWithContentDescription("Settings").performClick()
        composeTestRule.waitForIdle()
        composeTestRule.onNodeWithText("Settings").assertIsDisplayed()
        // About row is last; it can sit below the fold on tall nav bars.
        composeTestRule.onNodeWithTag("settings-about").performScrollTo().assertIsDisplayed()
    }

    @Test
    fun aboutRowClearsNavigationBar_threeButton() {
        setNavigationMode(0)

        val context = composeTestRule.activity
        Assume.assumeTrue(
            "emulator did not honor navigation_mode=0",
            context.readNavigationMode() == NavigationMode.ThreeButton,
        )

        openSettingsAndScrollToAbout()

        val decorView = context.window.decorView
        val navInset = ViewCompat.getRootWindowInsets(decorView)
            ?.getInsets(WindowInsetsCompat.Type.navigationBars())
            ?.bottom ?: 0
        val screenHeight = decorView.height
        val rowBottom = composeTestRule.onNodeWithTag("settings-about")
            .fetchSemanticsNode()
            .boundsInRoot
            .bottom

        val minClearance = if (navInset > 0) navInset else 48
        assertTrue(
            "About row bottom ($rowBottom) should be above nav bar (screen=$screenHeight inset=$navInset)",
            rowBottom <= screenHeight - minClearance + 8,
        )
    }

    @Test
    fun aboutRowClearsNavigationBar_gesture() {
        setNavigationMode(2)

        openSettingsAndScrollToAbout()

        val decorView = composeTestRule.activity.window.decorView
        val navInset = ViewCompat.getRootWindowInsets(decorView)
            ?.getInsets(WindowInsetsCompat.Type.navigationBars())
            ?.bottom ?: 0
        val screenHeight = decorView.height
        val rowBottom = composeTestRule.onNodeWithTag("settings-about")
            .fetchSemanticsNode()
            .boundsInRoot
            .bottom

        assertTrue(
            "About row bottom ($rowBottom) should clear gesture nav inset ($navInset)",
            rowBottom <= screenHeight - navInset + 8,
        )
    }
}
