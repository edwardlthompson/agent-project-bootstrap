package dev.foss.goldenpath.settings

import dev.foss.goldenpath.ui.theme.ThemeMode
import org.json.JSONObject

data class SettingsBundle(
    val version: Int,
    val theme: ThemeMode,
    val saveCrashes: Boolean,
)

object SettingsExport {
    const val VERSION = 1
    const val FILE_NAME = "golden-path-settings.json"

    fun snapshot(theme: ThemeMode, saveCrashes: Boolean): SettingsBundle =
        SettingsBundle(VERSION, theme, saveCrashes)

    fun toJson(bundle: SettingsBundle): String =
        JSONObject()
            .put("version", bundle.version)
            .put("theme", bundle.theme.name.lowercase())
            .put("saveCrashes", bundle.saveCrashes)
            .toString(2)

    fun parse(raw: String): SettingsBundle? =
        runCatching { migrate(JSONObject(raw)) }.getOrNull()

    fun migrate(data: JSONObject): SettingsBundle? {
        val version = readVersion(data) ?: return null
        if (version < 0 || version > VERSION) return null
        val theme = themeFromWire(data.optString("theme")) ?: legacyTheme(data) ?: return null
        return SettingsBundle(VERSION, theme, data.optBoolean("saveCrashes"))
    }

    private fun readVersion(data: JSONObject): Int? {
        if (!data.has("version")) return 0
        val raw = data.opt("version")
        if (raw is Number) return raw.toInt()
        val text = raw as? String ?: return null
        return text.toIntOrNull()
    }

    private fun legacyTheme(data: JSONObject): ThemeMode? {
        if (!data.has("darkMode")) return null
        return if (data.optBoolean("darkMode")) ThemeMode.Dark else ThemeMode.Light
    }

    private fun themeFromWire(raw: String): ThemeMode? =
        ThemeMode.entries.find { it.name.equals(raw, ignoreCase = true) }
}
