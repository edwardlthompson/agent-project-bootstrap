package dev.foss.goldenpath.about

import java.net.URI

object VenmoAllowlist {
    private val hosts = setOf("venmo.com", "www.venmo.com")

    fun isAllowed(url: String): Boolean {
        val uri = runCatching { URI(url) }.getOrNull() ?: return false
        if (uri.scheme?.lowercase() != "https") return false
        val host = uri.host?.lowercase() ?: return false
        if (host !in hosts) return false
        val path = uri.path ?: return false
        return path == "/code" || path.startsWith("/code/")
    }
}
