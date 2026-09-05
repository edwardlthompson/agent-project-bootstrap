package dev.foss.goldenpath.ui

import androidx.compose.foundation.layout.Arrangement
import androidx.compose.foundation.layout.Column
import androidx.compose.foundation.layout.fillMaxSize
import androidx.compose.foundation.layout.padding
import androidx.compose.material.icons.Icons
import androidx.compose.material.icons.filled.Info
import androidx.compose.material.icons.filled.Settings
import androidx.compose.material3.ExperimentalMaterial3Api
import androidx.compose.material3.Icon
import androidx.compose.material3.IconButton
import androidx.compose.material3.MaterialTheme
import androidx.compose.material3.SnackbarHostState
import androidx.compose.material3.Text
import androidx.compose.material3.TopAppBar
import androidx.compose.runtime.Composable
import androidx.compose.ui.Alignment
import androidx.compose.ui.Modifier
import androidx.compose.ui.res.stringResource
import dev.foss.goldenpath.R
import dev.foss.goldenpath.about.AppUpdates
import dev.foss.goldenpath.about.DonationsConfig
import dev.foss.goldenpath.ui.about.AboutScreen
import dev.foss.goldenpath.ui.about.LaunchPromptDialogs
import dev.foss.goldenpath.ui.components.GoldenPathScaffold
import dev.foss.goldenpath.ui.components.ThemeToggle
import dev.foss.goldenpath.ui.feedback.FeedbackScreen
import dev.foss.goldenpath.ui.nav.FeedbackKind
import dev.foss.goldenpath.ui.nav.GpRoute
import dev.foss.goldenpath.ui.nav.Nav
import dev.foss.goldenpath.ui.nav.NavState
import dev.foss.goldenpath.ui.settings.SettingsScreen
import dev.foss.goldenpath.ui.theme.SpacingLg
import dev.foss.goldenpath.ui.theme.SpacingMd
import dev.foss.goldenpath.ui.theme.ThemeMode

@OptIn(ExperimentalMaterial3Api::class)
@Composable
fun GoldenPathScreen(
    snackbarHostState: SnackbarHostState,
    themeMode: ThemeMode,
    isOnline: Boolean,
    nav: NavState,
    saveCrashes: Boolean,
    releaseRepo: String,
    pendingStack: String?,
    appVersion: String,
    installedFormat: String,
    updateStatus: String,
    donations: DonationsConfig,
    canApplyUpdate: Boolean,
    launchPrompt: AppUpdates.LaunchPrompt?,
    onThemeToggle: () -> Unit,
    onThemeModeSelect: (ThemeMode) -> Unit,
    onPushRoute: (GpRoute, FeedbackKind?) -> Unit,
    onPop: () -> Unit,
    onScroll: (GpRoute, Int) -> Unit,
    onSaveCrashes: (Boolean) -> Unit,
    onFeedbackClose: () -> Unit,
    onDonatePrompt: (Boolean) -> Unit,
    onUpdatePrompt: (Boolean) -> Unit,
    onApplyUpdate: () -> Unit,
) {
    val route = Nav.current(nav)
    GoldenPathScaffold(
        snackbarHostState = snackbarHostState,
        topBar = {
            TopAppBar(
                title = { Text(stringResource(R.string.app_title)) },
                actions = {
                    IconButton(onClick = { toggleRoute(route, GpRoute.Settings, onPushRoute, onPop) }) {
                        Icon(
                            imageVector = Icons.Filled.Settings,
                            contentDescription = stringResource(R.string.settings_open),
                        )
                    }
                    IconButton(onClick = { toggleRoute(route, GpRoute.About, onPushRoute, onPop) }) {
                        Icon(
                            imageVector = Icons.Filled.Info,
                            contentDescription = stringResource(R.string.about_open),
                        )
                    }
                    ThemeToggle(themeMode = themeMode, onToggle = onThemeToggle)
                },
            )
        },
    ) { innerPadding ->
        if (nav.promptOpen && launchPrompt != null) {
            LaunchPromptDialogs(
                prompt = launchPrompt,
                onDonate = onDonatePrompt,
                onUpdate = onUpdatePrompt,
            )
        }
        val panelMod = Modifier.fillMaxSize().padding(innerPadding)
        when (route) {
            GpRoute.Feedback -> FeedbackScreen(
                kind = nav.feedbackKind?.wire ?: FeedbackKind.Bug.wire,
                releaseRepo = releaseRepo,
                stack = pendingStack,
                onBack = onFeedbackClose,
                scrollY = Nav.restoreScroll(nav, GpRoute.Feedback),
                onScroll = { onScroll(GpRoute.Feedback, it) },
                modifier = panelMod,
            )
            GpRoute.Settings -> SettingsScreen(
                themeMode = themeMode,
                onThemeModeSelect = onThemeModeSelect,
                saveCrashes = saveCrashes,
                onSaveCrashes = onSaveCrashes,
                onOpenAbout = { onPushRoute(GpRoute.About, null) },
                onBack = onPop,
                scrollY = Nav.restoreScroll(nav, GpRoute.Settings),
                onScroll = { onScroll(GpRoute.Settings, it) },
                modifier = panelMod,
            )
            GpRoute.About -> AboutScreen(
                version = appVersion,
                installedFormat = installedFormat,
                updateStatus = updateStatus,
                donations = donations,
                canApplyUpdate = canApplyUpdate,
                onApplyUpdate = onApplyUpdate,
                onReportBug = { onPushRoute(GpRoute.Feedback, FeedbackKind.Bug) },
                onRequestFeature = { onPushRoute(GpRoute.Feedback, FeedbackKind.Feature) },
                onBack = onPop,
                scrollY = Nav.restoreScroll(nav, GpRoute.About),
                onScroll = { onScroll(GpRoute.About, it) },
                modifier = panelMod,
            )
            GpRoute.Home -> Column(
                modifier = panelMod.padding(SpacingMd),
                horizontalAlignment = Alignment.CenterHorizontally,
                verticalArrangement = Arrangement.Center,
            ) {
                Text(
                    text = stringResource(R.string.app_greeting),
                    style = MaterialTheme.typography.headlineMedium,
                    color = MaterialTheme.colorScheme.primary,
                )
                Text(
                    text = stringResource(
                        if (isOnline) R.string.app_status_online else R.string.app_status_offline,
                    ),
                    style = MaterialTheme.typography.bodyMedium,
                    color = MaterialTheme.colorScheme.onSurfaceVariant,
                    modifier = Modifier.padding(top = SpacingLg),
                )
            }
        }
    }
}

private fun toggleRoute(
    current: GpRoute,
    target: GpRoute,
    onPushRoute: (GpRoute, FeedbackKind?) -> Unit,
    onPop: () -> Unit,
) {
    if (current == target) onPop() else onPushRoute(target, null)
}
