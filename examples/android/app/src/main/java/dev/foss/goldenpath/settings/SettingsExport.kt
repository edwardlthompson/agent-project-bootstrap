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
        runCatching {
            val data = JSONObject(raw)
            if (data.optInt("version") != VERSION) return null
            val theme = themeFromWire(data.optString("theme")) ?: return null
            SettingsBundle(VERSION, theme, data.optBoolean("saveCrashes"))
        }.getOrNull()

    private fun themeFromWire(raw: String): ThemeMode? =
        ThemeMode.entries.find { it.name.equals(raw, ignoreCase = true) }
}
