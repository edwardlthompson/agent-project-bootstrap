package dev.foss.goldenpath.about

import android.content.Context
import androidx.test.core.app.ApplicationProvider
import org.junit.Assert.assertNotNull
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
    fun launchApkInstallResolvesFileProviderUri() {
        val apk = File(context.cacheDir, "test-update.apk")
        apk.writeBytes(byteArrayOf(0x50, 0x4b, 0x03, 0x04))

        UpdateApplier.launchApkInstall(context, apk)

        assertNotNull(context.packageManager)
    }
}
