package dev.foss.goldenpath.settings

import java.text.Normalizer

object SettingsSearch {
    /** Case-insensitive substring match after stripping diacritics (é → e). */
    fun normalize(text: String): String {
        val decomposed = Normalizer.normalize(text.trim(), Normalizer.Form.NFD)
        return decomposed
            .replace(Regex("\\p{M}+"), "")
            .lowercase()
    }

    fun matches(query: String, vararg labels: String): Boolean {
        val needle = normalize(query)
        if (needle.isEmpty()) return true
        return labels.any { normalize(it).contains(needle) }
    }

    /** True when needle is a near-substring (edit distance ≤ 1) of any label token. */
    fun fuzzyMatches(query: String, vararg labels: String): Boolean {
        val needle = normalize(query)
        if (needle.isEmpty()) return true
        if (matches(query, *labels)) return true
        if (needle.length < 3) return false
        return labels
            .flatMap { normalize(it).split(Regex("\\s+")) }
            .any { token -> token.isNotEmpty() && editDistanceAtMostOne(needle, token) }
    }

    private fun editDistanceAtMostOne(a: String, b: String): Boolean {
        if (kotlin.math.abs(a.length - b.length) > 1) return false
        if (a.length == b.length) {
            var diffs = 0
            for (i in a.indices) {
                if (a[i] != b[i] && ++diffs > 1) return false
            }
            return diffs <= 1
        }
        val shorter = if (a.length < b.length) a else b
        val longer = if (a.length < b.length) b else a
        var i = 0
        var j = 0
        var skipped = false
        while (i < shorter.length && j < longer.length) {
            if (shorter[i] == longer[j]) {
                i++
                j++
            } else if (skipped) {
                return false
            } else {
                skipped = true
                j++
            }
        }
        return true
    }
}
