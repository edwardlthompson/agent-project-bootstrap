package dev.foss.goldenpath.about

import android.content.Intent
import android.net.Uri

/** Builds the donate / external-link intent used by About ACTION_VIEW smokes. */
object DonateIntents {
    fun viewUrl(url: String): Intent =
        Intent(Intent.ACTION_VIEW, Uri.parse(url.trim())).apply {
            addCategory(Intent.CATEGORY_BROWSABLE)
        }

    fun isHttpView(intent: Intent): Boolean {
        if (intent.action != Intent.ACTION_VIEW) return false
        val scheme = intent.data?.scheme?.lowercase() ?: return false
        return scheme == "https" || scheme == "http"
    }
}
