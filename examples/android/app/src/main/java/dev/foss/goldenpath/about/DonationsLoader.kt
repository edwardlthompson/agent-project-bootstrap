package dev.foss.goldenpath.about

import android.content.Context
import org.json.JSONObject

data class DonationLink(val label: String, val url: String)

data class DonationsConfig(
    val enabled: Boolean,
    val message: String,
    val links: List<DonationLink>,
)

object DonationsLoader {
    const val DEFAULT_VENMO_URL = "https://venmo.com/code?user_id=1857304970395648420"

    /** Prefer live config; fall back to packaged exemplar when sync was skipped. */
    val ASSET_CANDIDATES = listOf("donations.json", "donations.json.example")

    fun primaryUrl(config: DonationsConfig): String =
        config.links.firstOrNull()?.url?.ifBlank { null } ?: DEFAULT_VENMO_URL

    fun parse(json: String): DonationsConfig {
        val root = JSONObject(json)
        val enabled = root.optBoolean("enabled", false)
        val message = root.optString("message", "")
        val links = mutableListOf<DonationLink>()
        val arr = root.optJSONArray("links")
        if (arr != null) {
            for (i in 0 until arr.length()) {
                val item = arr.getJSONObject(i)
                links.add(DonationLink(item.optString("label"), item.optString("url")))
            }
        }
        return DonationsConfig(enabled && links.isNotEmpty(), message, links)
    }

    /**
     * @param openAsset returns file contents or null when the asset is missing
     */
    fun loadFromAssets(openAsset: (String) -> String?): DonationsConfig {
        for (name in ASSET_CANDIDATES) {
            val json = openAsset(name) ?: continue
            return try {
                parse(json)
            } catch (_: Exception) {
                continue
            }
        }
        return DonationsConfig(enabled = false, message = "", links = emptyList())
    }

    fun load(context: Context): DonationsConfig =
        loadFromAssets { name ->
            try {
                context.assets.open(name).bufferedReader().use { it.readText() }
            } catch (_: Exception) {
                null
            }
        }
}
