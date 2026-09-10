package dev.foss.goldenpath.ui.about

import androidx.compose.foundation.clickable
import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxWidth
import androidx.compose.foundation.layout.padding
import androidx.compose.foundation.rememberScrollState
import androidx.compose.foundation.verticalScroll
import androidx.compose.material3.Button
import androidx.compose.material3.DropdownMenuItem
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.ExposedDropdownMenuAnchorType
import androidx.compose.material3.ExposedDropdownMenuBox
import androidx.compose.material3.ExposedDropdownMenuDefaults
import androidx.compose.material3.HorizontalDivider
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.OutlinedTextField
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.compose.ui.Modifier
import androidx.compose.ui.platform.LocalUriHandler
import androidx.compose.ui.platform.testTag
import androidx.compose.ui.res.stringResource
import dev.foss.goldenpath.R
import dev.foss.goldenpath.about.DonationsConfig
import dev.foss.goldenpath.display.highRefreshScroll
import dev.foss.goldenpath.ui.insets.LocalNavigationMode
import dev.foss.goldenpath.ui.insets.bottomInsetPadding
import dev.foss.goldenpath.ui.insets.navigationBarInsetBottomDp
import dev.foss.goldenpath.ui.insets.navigationModeLabelRes
import dev.foss.goldenpath.ui.theme.SpacingMd

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun AboutScreen(
    version: String,
    installedFormat: String,
    updateStatus: String,
    donations: DonationsConfig,
    canApplyUpdate: Boolean,
    onApplyUpdate: () -> Unit,
    onReportBug: () -> Unit,
    onRequestFeature: () -> Unit,
    scrollY: Int = 0,
    onScroll: (Int) -> Unit = {},
    modifier: Modifier = Modifier,
) {
    val uriHandler = LocalUriHandler.current
    val navMode = LocalNavigationMode.current
    val insetDp = navigationBarInsetBottomDp()
    val scrollState = rememberScrollState(initial = scrollY)
    var feedbackOpen by remember { mutableStateOf(false) }
    LaunchedEffect(scrollState.value) { onScroll(scrollState.value) }
    Column(
        modifier = modifier
            .highRefreshScroll()
            .verticalScroll(scrollState)
            .padding(SpacingMd)
            .bottomInsetPadding(),
        verticalArrangement = Arrangement.spacedBy(SpacingMd),
    ) {
        SectionLabel(stringResource(R.string.about_section_app))
        Text(text = stringResource(R.string.about_version, version))
        Text(text = stringResource(R.string.about_format, installedFormat))
        Text(text = updateStatus)
        Text(
            text = stringResource(
                R.string.about_debug_navigation_mode,
                stringResource(navigationModeLabelRes(navMode)),
                insetDp,
            ),
            style = MaterialTheme.typography.bodySmall,
            color = MaterialTheme.colorScheme.onSurfaceVariant,
        )
        if (canApplyUpdate) {
            Button(onClick = onApplyUpdate) {
                Text(stringResource(R.string.about_update_apply))
            }
        }
        if (donations.enabled && donations.links.isNotEmpty()) {
            HorizontalDivider()
            SectionLabel(stringResource(R.string.about_section_support))
            Text(
                text = stringResource(R.string.about_donations_heading),
                style = MaterialTheme.typography.titleMedium,
                modifier = Modifier.testTag(AboutTestTags.DONATIONS_HEADING),
            )
            Text(text = donations.message.ifBlank { stringResource(R.string.about_donations_message) })
            donations.links.forEach { link ->
                Text(
                    text = link.label,
                    color = MaterialTheme.colorScheme.primary,
                    modifier = Modifier
                        .testTag(AboutTestTags.DONATION_LINK)
                        .clickable { uriHandler.openUri(link.url) },
                )
            }
        }
        HorizontalDivider()
        SectionLabel(stringResource(R.string.about_section_feedback))
        ExposedDropdownMenuBox(
            expanded = feedbackOpen,
            onExpandedChange = { feedbackOpen = it },
        ) {
            OutlinedTextField(
                modifier = Modifier
                    .menuAnchor(ExposedDropdownMenuAnchorType.PrimaryNotEditable)
                    .fillMaxWidth(),
                readOnly = true,
                value = stringResource(R.string.about_feedback_choose),
                onValueChange = {},
                label = { Text(stringResource(R.string.about_feedback_label)) },
                trailingIcon = { ExposedDropdownMenuDefaults.TrailingIcon(expanded = feedbackOpen) },
            )
            ExposedDropdownMenu(
                expanded = feedbackOpen,
                onDismissRequest = { feedbackOpen = false },
            ) {
                DropdownMenuItem(
                    text = { Text(stringResource(R.string.feedback_bug_title)) },
                    onClick = {
                        feedbackOpen = false
                        onReportBug()
                    },
                )
                DropdownMenuItem(
                    text = { Text(stringResource(R.string.feedback_feature_title)) },
                    onClick = {
                        feedbackOpen = false
                        onRequestFeature()
                    },
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
