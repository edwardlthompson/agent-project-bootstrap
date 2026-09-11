package dev.foss.goldenpath.ui.screenshot

import android.graphics.Bitmap
import android.graphics.Color
import kotlin.math.abs

/** Coarse fingerprint for Settings/About/Feedback screenshot regression (device-tolerant). */
object ScreenshotFingerprint {
    const val GRID = 8

    fun fromBitmap(bitmap: Bitmap, grid: Int = GRID): IntArray {
        val w = bitmap.width.coerceAtLeast(1)
        val h = bitmap.height.coerceAtLeast(1)
        val out = IntArray(grid * grid)
        for (gy in 0 until grid) {
            for (gx in 0 until grid) {
                val x0 = gx * w / grid
                val x1 = ((gx + 1) * w / grid).coerceAtLeast(x0 + 1)
                val y0 = gy * h / grid
                val y1 = ((gy + 1) * h / grid).coerceAtLeast(y0 + 1)
                var sum = 0L
                var count = 0
                for (y in y0 until y1) {
                    for (x in x0 until x1) {
                        val c = bitmap.getPixel(x, y)
                        sum += (Color.red(c) + Color.green(c) + Color.blue(c)) / 3
                        count++
                    }
                }
                out[gy * grid + gx] = if (count == 0) 0 else (sum / count).toInt()
            }
        }
        return out
    }

    fun maxDelta(a: IntArray, b: IntArray): Int {
        require(a.size == b.size)
        var max = 0
        for (i in a.indices) {
            max = maxOf(max, abs(a[i] - b[i]))
        }
        return max
    }

    fun encode(values: IntArray): String = values.joinToString(",")

    fun decode(raw: String): IntArray =
        raw.split(',').map { it.trim().toInt() }.toIntArray()
}
