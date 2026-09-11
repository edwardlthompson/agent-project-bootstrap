package dev.foss.goldenpath

import androidx.compose.ui.test.junit4.v2.createAndroidComposeRule
import androidx.test.core.app.ApplicationProvider
import androidx.test.ext.junit.runners.AndroidJUnit4
import dev.foss.goldenpath.push.UnifiedPushConfig
import dev.foss.goldenpath.push.UnifiedPushDistributors
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertTrue
import org.junit.Rule
import org.junit.Test
import org.junit.rules.RuleChain
import org.junit.runner.RunWith

/**
 * Device E2E: FOSS UnifiedPush distributor (e.g. ntfy) must be discoverable.
 * Install ntfy from F-Droid / GitHub fdroid-release before running.
 */
@RunWith(AndroidJUnit4::class)
class UnifiedPushDistributorUiTest {
    private val composeTestRule = createAndroidComposeRule<MainActivity>()

    @get:Rule
    val rules: RuleChain = RuleChain
        .outerRule(ClearUiPrefsRule())
        .around(FailureEvidenceRule { composeTestRule })
        .around(composeTestRule)

    @Test
    fun discoversInstalledFossDistributor() {
        composeTestRule.dismissLaunchPrompts()
        val context = ApplicationProvider.getApplicationContext<android.content.Context>()
        val packages = UnifiedPushDistributors.installedPackages(context.packageManager)
        assertTrue("expected FOSS distributor packages, got $packages", packages.isNotEmpty())
        val state = UnifiedPushConfig.state(packages, "https://ntfy.sh/goldenpath-smoke")
        assertTrue(state.enabled)
        assertNotNull(state.distributorPackage)
        assertEquals(false, UnifiedPushConfig.usesProprietaryPush())
    }
}
