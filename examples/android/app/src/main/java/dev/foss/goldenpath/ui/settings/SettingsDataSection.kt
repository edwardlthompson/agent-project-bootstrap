package dev.foss.goldenpath.ui.settings

import android.net.Uri
import androidx.activity.compose.rememberLauncherForActivityResult
import androidx.activity.result.contract.ActivityResultContracts
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedButton
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalContext
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.res.stringResource
import dev.foss.goldenpath.R
import dev.foss.goldenpath.settings.SettingsExport
import dev.foss.goldenpath.ui.theme.SpacingSm
import dev.foss.goldenpath.ui.theme.ThemeMode

@Composable
fun SettingsDataSection(
    themeMode: ThemeMode,
    saveCrashes: Boolean,
    onThemeModeSelect: (ThemeMode) -> Unit,
    onSaveCrashes: (Boolean) -> Unit,
) {
    val context = LocalContext.current
    val export = rememberLauncherForActivityResult(
        ActivityResultContracts.CreateDocument("application/json"),
    ) { uri ->
        if (uri != null) writeBundle(context.contentResolver, uri, themeMode, saveCrashes)
    }
    val import = rememberLauncherForActivityResult(
        ActivityResultContracts.OpenDocument(),
    ) { uri ->
        if (uri == null) return@rememberLauncherForActivityResult
        val bundle = readBundle(context.contentResolver, uri) ?: return@rememberLauncherForActivityResult
        onThemeModeSelect(bundle.theme)
        onSaveCrashes(bundle.saveCrashes)
    }
    Text(
        text = stringResource(R.string.settings_section_data),
        style = MaterialTheme.typography.titleSmall,
        color = MaterialTheme.colorScheme.onSurfaceVariant,
    )
    Row(
        modifier = Modifier.fillMaxWidth(),
        horizontalArrangement = Arrangement.spacedBy(SpacingSm),
    ) {
        OutlinedButton(
            onClick = { export.launch(SettingsExport.FILE_NAME) },
            modifier = Modifier.testTag("settings-export"),
        ) {
            Text(stringResource(R.string.settings_export))
        }
        OutlinedButton(
            onClick = { import.launch(arrayOf("application/json")) },
            modifier = Modifier.testTag("settings-import"),
        ) {
            Text(stringResource(R.string.settings_import))
        }
    }
}

private fun writeBundle(
    resolver: android.content.ContentResolver,
    uri: Uri,
    themeMode: ThemeMode,
    saveCrashes: Boolean,
) {
    val json = SettingsExport.toJson(SettingsExport.snapshot(themeMode, saveCrashes))
    runCatching {
        resolver.openOutputStream(uri)?.use { stream ->
            stream.write(json.toByteArray(Charsets.UTF_8))
        }
    }
}

private fun readBundle(
    resolver: android.content.ContentResolver,
    uri: Uri,
) = runCatching {
    resolver.openInputStream(uri)?.bufferedReader(Charsets.UTF_8)?.use { it.readText() }
}.getOrNull()?.let(SettingsExport::parse)
