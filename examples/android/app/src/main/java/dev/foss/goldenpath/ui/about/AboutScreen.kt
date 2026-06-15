package dev.foss.goldenpath.ui.about

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.padding
import androidx.compose.material3.Button
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.Text
import androidx.compose.runtime.Composable
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import dev.foss.goldenpath.R
import dev.foss.goldenpath.about.DonationsConfig
import dev.foss.goldenpath.ui.theme.SpacingMd

@Composable
fun AboutScreen(
    version: String,
    installedFormat: String,
    updateStatus: String,
    donations: DonationsConfig,
    onBack: () -> Unit,
    modifier: Modifier = Modifier,
) {
    Column(
        modifier = modifier.padding(SpacingMd),
        verticalArrangement = Arrangement.spacedBy(SpacingMd),
    ) {
        Text(
            text = stringResource(R.string.about_title),
            style = MaterialTheme.typography.headlineSmall,
        )
        Text(text = stringResource(R.string.about_version, version))
        Text(text = stringResource(R.string.about_format, installedFormat))
        Text(text = updateStatus)
        if (donations.enabled && donations.links.isNotEmpty()) {
            Text(text = donations.message)
            donations.links.forEach { link ->
                Text(text = "${link.label}: ${link.url}")
            }
        }
        Button(onClick = onBack) {
            Text(stringResource(R.string.about_close))
        }
    }
}
