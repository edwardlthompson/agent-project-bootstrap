package dev.foss.goldenpath.ui

import android.content.Context
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import dev.foss.goldenpath.R
import dev.foss.goldenpath.about.AppUpdatePreferences
import dev.foss.goldenpath.about.CheckSchedule
import dev.foss.goldenpath.about.DonationsLoader
import dev.foss.goldenpath.about.ReleaseTagFetcher
import dev.foss.goldenpath.about.UpdateStatusEvaluator
import dev.foss.goldenpath.network.NetworkStatusMonitor
import dev.foss.goldenpath.settings.SettingsLogic
import dev.foss.goldenpath.ui.theme.GoldenPathTheme
import dev.foss.goldenpath.ui.theme.ThemeMode
import dev.foss.goldenpath.ui.theme.ThemePreferences
import dev.foss.goldenpath.ui.theme.next
import kotlinx.coroutines.CoroutineScope
import kotlinx.coroutines.launch

private const val APP_VERSION = "0.1.0"

@Composable
fun GoldenPathApp(
    context: Context,
    scope: CoroutineScope,
    themePreferences: ThemePreferences,
    appUpdatePreferences: AppUpdatePreferences,
    networkStatusMonitor: NetworkStatusMonitor,
) {
    val themeMode by themePreferences.themeMode.collectAsStateWithLifecycle(initialValue = ThemeMode.System)
    val isOnline by networkStatusMonitor.isOnline.collectAsStateWithLifecycle(initialValue = true)
    val installedFormat by appUpdatePreferences.installedFormat.collectAsStateWithLifecycle(initialValue = "apk")
    val checkInterval by appUpdatePreferences.checkInterval.collectAsStateWithLifecycle(initialValue = "off")
    val lastChecked by appUpdatePreferences.lastChecked.collectAsStateWithLifecycle(initialValue = null)
    var showAbout by remember { mutableStateOf(false) }
    var showSettings by remember { mutableStateOf(false) }
    var updateStatus by remember { mutableStateOf(context.getString(R.string.about_update_current)) }
    val donations = remember { DonationsLoader.load(context) }

    LaunchedEffect(checkInterval, lastChecked) {
        if (!CheckSchedule.shouldCheck(checkInterval, lastChecked, System.currentTimeMillis())) return@LaunchedEffect
        val repo = ReleaseTagFetcher.loadReleaseRepo(context) ?: return@LaunchedEffect
        val tag = ReleaseTagFetcher.fetchLatestTag(repo)
        appUpdatePreferences.setLastChecked(System.currentTimeMillis())
        updateStatus = when (val result = UpdateStatusEvaluator.evaluate(APP_VERSION, tag)) {
            is UpdateStatusEvaluator.Result.Current -> context.getString(R.string.about_update_current)
            is UpdateStatusEvaluator.Result.Available ->
                context.getString(R.string.about_update_available, result.version)
        }
    }

    GoldenPathTheme(themeMode = themeMode) {
        GoldenPathScreen(
            themeMode = themeMode,
            isOnline = isOnline,
            showAbout = showAbout,
            showSettings = showSettings,
            updateCheckEnabled = SettingsLogic.isUpdateCheckEnabled(checkInterval),
            appVersion = APP_VERSION,
            installedFormat = installedFormat ?: "apk",
            updateStatus = updateStatus,
            donations = donations,
            onThemeToggle = {
                scope.launchTheme(themePreferences, themeMode.next())
            },
            onThemeModeSelect = { mode ->
                scope.launchTheme(themePreferences, mode)
            },
            onAboutOpen = { showAbout = true; showSettings = false },
            onAboutClose = { showAbout = false },
            onSettingsOpen = { showSettings = true; showAbout = false },
            onSettingsClose = { showSettings = false },
            onUpdateCheckChange = { enabled ->
                scope.launchInterval(appUpdatePreferences, SettingsLogic.intervalForToggle(enabled, checkInterval))
            },
        )
    }
}

private fun CoroutineScope.launchTheme(prefs: ThemePreferences, mode: ThemeMode) {
    kotlinx.coroutines.launch {
        prefs.setThemeMode(mode)
    }
}

private fun CoroutineScope.launchInterval(prefs: AppUpdatePreferences, interval: String) {
    kotlinx.coroutines.launch {
        prefs.setCheckInterval(interval)
    }
}
