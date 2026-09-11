package dev.foss.goldenpath.ui.settings

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.Row
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.automirrored.filled.KeyboardArrowRight
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.ExposedDropdownMenuAnchorType
import androidx.compose.material3.ExposedDropdownMenuBox
import androidx.compose.material3.ExposedDropdownMenuDefaults
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.Icon
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Switch
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.res.stringResource
import dev.foss.goldenpath.R
import dev.foss.goldenpath.display.highRefreshScroll
import dev.foss.goldenpath.settings.SettingsSearch
import dev.foss.goldenpath.ui.insets.bottomInsetPadding
import dev.foss.goldenpath.ui.theme.SpacingMd
import dev.foss.goldenpath.ui.theme.SpacingSm
import dev.foss.goldenpath.ui.theme.ThemeMode

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun SettingsScreen(
    themeMode: ThemeMode,
    onThemeModeSelect: (ThemeMode) -> Unit,
    saveCrashes: Boolean,
    onSaveCrashes: (Boolean) -> Unit,
    onOpenAbout: () -> Unit = {},
    scrollY: Int = 0,
    onScroll: (Int) -> Unit = {},
    modifier: Modifier = Modifier,
) {
    var themeMenuOpen by remember { mutableStateOf(false) }
    var query by remember { mutableStateOf("") }
    val appearance = stringResource(R.string.settings_section_appearance)
    val themeLabel = stringResource(R.string.settings_theme_label)
    val privacy = stringResource(R.string.settings_section_privacy)
    val saveCrashesLabel = stringResource(R.string.settings_feedback_save_crashes)
    val data = stringResource(R.string.settings_section_data)
    val exportLabel = stringResource(R.string.settings_export)
    val importLabel = stringResource(R.string.settings_import)
    val about = stringResource(R.string.settings_section_about)
    val appInfo = stringResource(R.string.settings_about)
    val aboutHint = stringResource(R.string.settings_about_hint)
    val showAppearance = SettingsSearch.fuzzyMatches(query, appearance, themeLabel)
    val showPrivacy = SettingsSearch.fuzzyMatches(query, privacy, saveCrashesLabel)
    val showData = SettingsSearch.fuzzyMatches(query, data, exportLabel, importLabel)
    val showAbout = SettingsSearch.fuzzyMatches(query, about, appInfo, aboutHint)
    val showEmpty = query.isNotBlank() && !showAppearance && !showPrivacy && !showData && !showAbout
    val scrollState = rememberScrollState(initial = scrollY)
    LaunchedEffect(scrollState.value) { onScroll(scrollState.value) }
    Column(
        modifier = modifier
            .testTag("settings-panel")
            .highRefreshScroll()
            .verticalScroll(scrollState)
            .padding(SpacingMd)
            .bottomInsetPadding(),
        verticalArrangement = Arrangement.spacedBy(SpacingMd),
    ) {
        OutlinedTextField(
            value = query,
            onValueChange = { query = it },
            modifier = Modifier
                .fillMaxWidth()
                .testTag("settings-search"),
            label = { Text(stringResource(R.string.settings_search)) },
            singleLine = true,
        )
        if (showEmpty) {
            Text(
                text = stringResource(R.string.settings_search_empty_hint),
                modifier = Modifier.testTag("settings-search-empty"),
                color = MaterialTheme.colorScheme.onSurfaceVariant,
            )
        }
        if (showAppearance) {
        SectionLabel(appearance)
        ExposedDropdownMenuBox(
            expanded = themeMenuOpen,
            onExpandedChange = { themeMenuOpen = it },
        ) {
            OutlinedTextField(
                modifier = Modifier
                    .menuAnchor(ExposedDropdownMenuAnchorType.PrimaryNotEditable)
                    .fillMaxWidth(),
                readOnly = true,
                value = stringResource(themeModeLabel(themeMode)),
                onValueChange = {},
                label = { Text(stringResource(R.string.settings_theme_label)) },
                trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = themeMenuOpen) },
            )
            ExposedDropdownMenu(
                expanded = themeMenuOpen,
                onDismissRequest = { themeMenuOpen = false },
            ) {
                ThemeMode.entries.forEach { mode ->
                    DropdownMenuItem(
                        text = { Text(stringResource(themeModeLabel(mode))) },
                        onClick = {
                            onThemeModeSelect(mode)
                            themeMenuOpen = false
                        },
                    )
                }
            }
        }
        }
        if (showPrivacy) {
        HorizontalDivider()
        SectionLabel(privacy)
        Row(
            modifier = Modifier.fillMaxWidth(),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Text(
                text = saveCrashesLabel,
                modifier = Modifier
                    .weight(1f)
                    .padding(end = SpacingSm),
            )
            Switch(checked = saveCrashes, onCheckedChange = onSaveCrashes)
        }
        }
        if (showData) {
        HorizontalDivider()
        SettingsDataSection(
            themeMode = themeMode,
            saveCrashes = saveCrashes,
            onThemeModeSelect = onThemeModeSelect,
            onSaveCrashes = onSaveCrashes,
        )
        }
        if (showAbout) {
        HorizontalDivider()
        SectionLabel(about)
        Row(
            modifier = Modifier
                .fillMaxWidth()
                .testTag("settings-about")
                .clickable(onClick = onOpenAbout)
                .padding(vertical = SpacingSm),
            horizontalArrangement = Arrangement.SpaceBetween,
            verticalAlignment = Alignment.CenterVertically,
        ) {
            Column(modifier = Modifier.weight(1f)) {
                Text(text = appInfo)
                Text(
                    text = aboutHint,
                    style = MaterialTheme.typography.bodySmall,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                )
            }
            Icon(
                imageVector = Icons.AutoMirrored.Filled.KeyboardArrowRight,
                contentDescription = null,
            )
        }
        }
    }
}

@Composable
private fun SectionLabel(text: String) {
    Text(
        text = text,
        style = MaterialTheme.typography.titleSmall,
        color = MaterialTheme.colorScheme.onSurfaceVariant,
    )
}

private fun themeModeLabel(mode: ThemeMode): Int = when (mode) {
    ThemeMode.System -> R.string.settings_theme_mode_system
    ThemeMode.Light -> R.string.settings_theme_mode_light
    ThemeMode.Dark -> R.string.settings_theme_mode_dark
}
