package dev.foss.goldenpath.about

import android.content.Context
import android.content.Intent
import androidx.test.core.app.ApplicationProvider
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config
import java.io.File

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [26])
class UpdateApplierTest {
    private val context: Context = ApplicationProvider.getApplicationContext()

    @Test
    fun buildInstallIntentTargetsApkMimeType() {
        val apk = File(context.cacheDir, "test-update.apk")
        apk.writeBytes(byteArrayOf(0x50, 0x4b, 0x03, 0x04))

        val intent = UpdateApplier.buildInstallIntent(context, apk)

        assertEquals(Intent.ACTION_VIEW, intent.action)
        assertEquals("application/vnd.android.package-archive", intent.type)
        assertTrue(intent.flags and Intent.FLAG_GRANT_READ_URI_PERMISSION != 0)
    }
}
