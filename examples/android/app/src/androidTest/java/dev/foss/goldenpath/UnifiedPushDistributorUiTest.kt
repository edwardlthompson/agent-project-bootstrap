package dev.foss.goldenpath

import androidx.test.core.app.ApplicationProvider
import androidx.test.ext.junit.runners.AndroidJUnit4
import dev.foss.goldenpath.push.UnifiedPushConfig
import dev.foss.goldenpath.push.UnifiedPushDistributors
import org.junit.Assert.assertEquals
import org.junit.Assert.assertNotNull
import org.junit.Assert.assertTrue
import org.junit.Assume
import org.junit.Test
import org.junit.runner.RunWith

/**
 * Device E2E: FOSS UnifiedPush distributor (e.g. ntfy) must be discoverable.
 * CI emulator has no distributor — skipped via Assume. Install ntfy before local ADB runs.
 */
@RunWith(AndroidJUnit4::class)
class UnifiedPushDistributorUiTest {
    @Test
    fun discoversInstalledFossDistributor() {
        val context = ApplicationProvider.getApplicationContext<android.content.Context>()
        val packages = UnifiedPushDistributors.installedPackages(context.packageManager)
        Assume.assumeTrue(
            "install ntfy (or another UP distributor) for UnifiedPush E2E",
            packages.isNotEmpty(),
        )
        val state = UnifiedPushConfig.state(packages, "https://ntfy.sh/goldenpath-smoke")
        assertTrue(state.enabled)
        assertNotNull(state.distributorPackage)
        assertEquals(false, UnifiedPushConfig.usesProprietaryPush())
    }
}
