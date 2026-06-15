package dev.foss.goldenpath.about

import android.content.Context
import androidx.test.core.app.ApplicationProvider
import kotlinx.coroutines.flow.first
import kotlinx.coroutines.runBlocking
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [26])
class AppUpdatePreferencesTest {
    private val context: Context = ApplicationProvider.getApplicationContext()

    @Test
    fun defaultsCheckIntervalToOff() = runBlocking {
        val prefs = AppUpdatePreferences(context)
        assertEquals("off", prefs.checkInterval.first())
    }

    @Test
    fun persistsCheckInterval() = runBlocking {
        val prefs = AppUpdatePreferences(context)
        prefs.setCheckInterval("weekly")
        assertEquals("weekly", prefs.checkInterval.first())
    }

    @Test
    fun ensureInstalledFormatDetectsApk() = runBlocking {
        val prefs = AppUpdatePreferences(context)
        val format = prefs.ensureInstalledFormat()
        assertFalse(format.isBlank())
    }
}
