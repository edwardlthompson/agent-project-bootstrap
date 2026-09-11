package dev.foss.goldenpath.about

import android.content.Intent
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [26])
class DonateIntentsTest {
    @Test
    fun viewUrlUsesActionViewHttps() {
        val intent = DonateIntents.viewUrl("https://example.com/donate")
        assertEquals(Intent.ACTION_VIEW, intent.action)
        assertEquals("https://example.com/donate", intent.dataString)
        assertTrue(DonateIntents.isHttpView(intent))
    }
}
