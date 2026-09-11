package dev.foss.goldenpath.about

import org.junit.Assert.assertEquals
import org.junit.Test

class ArtifactFormatDetectorTest {
    @Test
    fun defaultsToApk() {
        assertEquals("apk", ArtifactFormatDetector.detectAndroidFormat())
    }

    @Test
    fun splitNamesHintAppBundle() {
        assertEquals("aab", ArtifactFormatDetector.detectAndroidFormat(splitNames = arrayOf("config.xxhdpi")))
    }

    @Test
    fun labelNormalizesBundleAliases() {
        assertEquals("aab", ArtifactFormatDetector.labelFor("app-bundle"))
        assertEquals("apk", ArtifactFormatDetector.labelFor("APK"))
    }
}
