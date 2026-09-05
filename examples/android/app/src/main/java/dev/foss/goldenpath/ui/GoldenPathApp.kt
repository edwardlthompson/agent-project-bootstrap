package dev.foss.goldenpath.ui

import android.content.Context
import android.content.Intent
import android.net.Uri
import androidx.activity.compose.BackHandler
import androidx.compose.runtime.Composable
import androidx.compose.runtime.LaunchedEffect
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.saveable.Saver
import androidx.compose.runtime.saveable.rememberSaveable
import androidx.compose.runtime.setValue
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import androidx.compose.material3.SnackbarHostState
import dev.foss.goldenpath.BuildConfig
import dev.foss.goldenpath.R
import dev.foss.goldenpath.crashcapture.PendingCrashStore
import dev.foss.goldenpath.feedback.FeedbackPrefs
import dev.foss.goldenpath.about.ReleaseTagFetcher
import dev.foss.goldenpath.about.AppUpdatePreferences
import dev.foss.goldenpath.about.AppUpdates
import dev.foss.goldenpath.about.DonationsLoader
import dev.foss.goldenpath.about.UpdateLaunchPrefs
import dev.foss.goldenpath.network.NetworkStatusMonitor
import dev.foss.goldenpath.ui.insets.NavigationModeProvider
import dev.foss.goldenpath.ui.nav.GpRoute
import dev.foss.goldenpath.ui.nav.Nav
import dev.foss.goldenpath.ui.nav.NavBack
import dev.foss.goldenpath.ui.nav.NavPreferences
import dev.foss.goldenpath.ui.nav.NavSession
import dev.foss.goldenpath.ui.nav.NavState
import dev.foss.goldenpath.ui.nav.NavStore
import dev.foss.goldenpath.ui.theme.ThemeMode
import dev.foss.goldenpath.ui.theme.ThemePreferences
import dev.foss.goldenpath.ui.theme.next
import kotlinx.coroutines.CoroutineScope
import dev.foss.goldenpath.ui.theme.GoldenPathTheme
import kotlinx.coroutines.launch

private val NavStateSaver = Saver<NavState, String>(
    save = { NavStore.save(it) },
    restore = { NavStore.load(it) },
)

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
    val pendingRestart by appUpdatePreferences.pendingRestart.collectAsStateWithLifecycle(initialValue = false)
    val navPrefs = remember { NavPreferences(context) }
    val crashStore = remember { PendingCrashStore(context) }
    var nav by rememberSaveable(stateSaver = NavStateSaver) {
        mutableStateOf(NavSession.boot(navPrefs.read(), crashStore.read() != null))
    }
    val scrollRef = remember { mutableMapOf<GpRoute, Int>() }
    val feedbackPrefs = remember { FeedbackPrefs(context) }
    var saveCrashes by remember { mutableStateOf(feedbackPrefs.saveCrashes()) }
    var updateStatus by remember { mutableStateOf(context.getString(R.string.about_update_current)) }
    var launchPrompt by remember { mutableStateOf<AppUpdates.LaunchPrompt?>(null) }
    val donations = remember { DonationsLoader.load(context) }
    val appVersion = BuildConfig.VERSION_NAME
    val snackbarHostState = remember { SnackbarHostState() }
    val launchPrefs = remember { UpdateLaunchPrefs(context) }

    fun applyNav(next: NavState) {
        var merged = next
        scrollRef.forEach { (route, y) -> merged = Nav.recordScroll(merged, route, y) }
        nav = merged
        navPrefs.write(merged)
    }

    fun popNav() {
        val result = NavBack.onSystemBack(nav)
        applyNav(result.next)
        if (!result.next.promptOpen) launchPrompt = null
    }

    BackHandler(enabled = true) { popNav() }

    LaunchedEffect(pendingRestart) {
        if (pendingRestart) {
            updateStatus = context.getString(R.string.about_update_restarting)
        }
    }

    LaunchedEffect(Unit) {
        navPrefs.write(nav)
        val prompt = AppUpdates.onLaunch(context, appVersion)
        launchPrompt = prompt
        if (prompt != null) applyNav(Nav.setPrompt(nav, true))
    }

    fun openUrl(url: String) {
        runCatching {
            context.startActivity(Intent(Intent.ACTION_VIEW, Uri.parse(url)))
        }
    }

    GoldenPathTheme(themeMode = themeMode) {
        NavigationModeProvider {
            GoldenPathScreen(
                snackbarHostState = snackbarHostState,
                themeMode = themeMode,
                isOnline = isOnline,
                nav = nav,
                saveCrashes = saveCrashes,
                releaseRepo = ReleaseTagFetcher.loadReleaseRepo(context).orEmpty(),
                pendingStack = crashStore.read()?.stack,
                appVersion = appVersion,
                installedFormat = installedFormat ?: "apk",
                updateStatus = updateStatus,
                donations = donations,
                canApplyUpdate = false,
                launchPrompt = launchPrompt,
                onThemeToggle = { scope.launch { themePreferences.setThemeMode(themeMode.next()) } },
                onThemeModeSelect = { mode -> scope.launch { themePreferences.setThemeMode(mode) } },
                onPushRoute = { route, kind -> applyNav(Nav.push(nav, route, kind)) },
                onPop = { popNav() },
                onScroll = { route, y -> scrollRef[route] = y },
                onSaveCrashes = { on -> feedbackPrefs.setSaveCrashes(on); saveCrashes = on },
                onFeedbackClose = {
                    crashStore.clear()
                    popNav()
                },
                onDonatePrompt = { donate ->
                    launchPrefs.markVersionSeen(appVersion)
                    launchPrompt = null
                    applyNav(Nav.setPrompt(nav, false))
                    if (donate) openUrl(DonationsLoader.primaryUrl(donations))
                },
                onUpdatePrompt = { install ->
                    val prompt = launchPrompt as? AppUpdates.LaunchPrompt.Update
                    launchPrompt = null
                    applyNav(Nav.setPrompt(nav, false))
                    if (prompt != null) {
                        launchPrefs.markChecked(System.currentTimeMillis(), prompt.version)
                        if (install) openUrl(prompt.url)
                    }
                },
                onApplyUpdate = {},
            )
        }
    }
}
