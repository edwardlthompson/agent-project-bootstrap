package dev.foss.goldenpath.about

object ArtifactFormatDetector {
    /** Returns apk or aab for About "Installed format" (bundle vs package). */
    fun detectAndroidFormat(applicationInfoFlags: Int = 0, splitNames: Array<String>? = null): String {
        // Split APKs / Play feature modules still report as apk packages; AAB is install-time only.
        // Prefer explicit split presence as a weak "from bundle" hint for sideload smoke docs.
        if (!splitNames.isNullOrEmpty()) return "aab"
        return "apk"
    }

    fun labelFor(format: String): String = when (format.lowercase()) {
        "aab", "app-bundle", "bundle" -> "aab"
        else -> "apk"
    }
}
