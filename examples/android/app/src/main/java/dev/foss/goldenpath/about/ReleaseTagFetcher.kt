package dev.foss.goldenpath.about

import android.content.Context
import org.json.JSONObject
import java.net.HttpURLConnection
import java.net.URL

object ReleaseTagFetcher {
    fun loadReleaseRepo(context: Context): String? {
        return try {
            val json = context.assets.open("app-update.json").bufferedReader().use { it.readText() }
            val repo = JSONObject(json).optString("release_repo", "").trim()
            repo.ifEmpty { null }
        } catch (_: Exception) {
            null
        }
    }

    fun fetchLatestTag(releaseRepo: String): String? {
        return try {
            val url = URL("https://api.github.com/repos/$releaseRepo/releases/latest")
            val conn = url.openConnection() as HttpURLConnection
            conn.requestMethod = "GET"
            conn.setRequestProperty("Accept", "application/vnd.github+json")
            conn.connectTimeout = 10_000
            conn.readTimeout = 10_000
            if (conn.responseCode != HttpURLConnection.HTTP_OK) return null
            val body = conn.inputStream.bufferedReader().use { it.readText() }
            JSONObject(body).optString("tag_name", "").ifEmpty { null }
        } catch (_: Exception) {
            null
        }
    }
}
