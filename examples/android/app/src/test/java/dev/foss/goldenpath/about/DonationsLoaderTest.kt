package dev.foss.goldenpath.about

import android.content.Context
import androidx.test.core.app.ApplicationProvider
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [26])
class DonationsLoaderTest {
    private val context: Context = ApplicationProvider.getApplicationContext()

    @Test
    fun loadsDonationsFromAssets() {
        val cfg = DonationsLoader.load(context)
        assertTrue(cfg.enabled)
        assertEquals("If this project helps you, consider supporting development.", cfg.message)
        assertTrue(cfg.links.size >= 3)
        assertTrue(cfg.links.any { it.url == DonationsLoader.DEFAULT_VENMO_URL })
        assertTrue(cfg.links.any { it.url.contains("github.com/sponsors") })
        assertTrue(cfg.links.any { it.url.contains("liberapay.com") })
        assertEquals(DonationsLoader.DEFAULT_VENMO_URL, DonationsLoader.primaryUrl(cfg))
    }

    @Test
    fun fallsBackToExemplarAssetName() {
        val exemplar = """
            {"enabled":true,"message":"from example","links":[{"label":"X","url":"https://example.test/x"}]}
        """.trimIndent()
        val cfg = DonationsLoader.loadFromAssets { name ->
            when (name) {
                "donations.json" -> null
                "donations.json.example" -> exemplar
                else -> null
            }
        }
        assertTrue(cfg.enabled)
        assertEquals("from example", cfg.message)
        assertEquals("https://example.test/x", cfg.links.single().url)
    }

    @Test
    fun missingAssetsYieldDisabledConfig() {
        val cfg = DonationsLoader.loadFromAssets { null }
        assertFalse(cfg.enabled)
        assertTrue(cfg.links.isEmpty())
    }
}
