package dev.foss.goldenpath.ui.screenshot

import android.graphics.Bitmap
import android.graphics.Color
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [26])
class ScreenshotFingerprintTest {
    @Test
    fun encodeDecodeRoundTrip() {
        val values = intArrayOf(10, 20, 30, 40)
        assertEquals("10,20,30,40", ScreenshotFingerprint.encode(values))
        assertTrue(
            ScreenshotFingerprint.decode("10,20,30,40").contentEquals(values),
        )
    }

    @Test
    fun fingerprintDiffersForLightVsDark() {
        val light = Bitmap.createBitmap(32, 32, Bitmap.Config.ARGB_8888).also { it.eraseColor(Color.WHITE) }
        val dark = Bitmap.createBitmap(32, 32, Bitmap.Config.ARGB_8888).also { it.eraseColor(Color.BLACK) }
        try {
            val a = ScreenshotFingerprint.fromBitmap(light)
            val b = ScreenshotFingerprint.fromBitmap(dark)
            assertTrue(ScreenshotFingerprint.maxDelta(a, b) > 100)
        } finally {
            light.recycle()
            dark.recycle()
        }
    }
}
