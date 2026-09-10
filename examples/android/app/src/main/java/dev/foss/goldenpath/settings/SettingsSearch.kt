package dev.foss.goldenpath.settings

object SettingsSearch {
    fun matches(query: String, vararg labels: String): Boolean {
        val needle = query.trim().lowercase()
        if (needle.isEmpty()) return true
        return labels.any { it.lowercase().contains(needle) }
    }
}
