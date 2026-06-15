package dev.foss.goldenpath

// Feature wiring: keep ≤10 lines per feature in this composition root (see docs/FEATURE_MODULES.md).
import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.runtime.getValue
import androidx.compose.runtime.mutableStateOf
import androidx.compose.runtime.remember
import androidx.compose.runtime.setValue
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import dev.foss.goldenpath.about.AppUpdatePreferences
import dev.foss.goldenpath.network.NetworkStatusMonitor
import dev.foss.goldenpath.ui.GoldenPathScreen
import dev.foss.goldenpath.ui.theme.GoldenPathTheme
import dev.foss.goldenpath.ui.theme.ThemeMode
import dev.foss.goldenpath.ui.theme.ThemePreferences
import dev.foss.goldenpath.ui.theme.next
import kotlinx.coroutines.launch

class MainActivity : ComponentActivity() {
    private lateinit var themePreferences: ThemePreferences
    private lateinit var appUpdatePreferences: AppUpdatePreferences
    private lateinit var networkStatusMonitor: NetworkStatusMonitor

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        themePreferences = ThemePreferences(applicationContext)
        appUpdatePreferences = AppUpdatePreferences(applicationContext)
        networkStatusMonitor = NetworkStatusMonitor(applicationContext)
        networkStatusMonitor.start()

        lifecycleScope.launch {
            appUpdatePreferences.clearPendingRestart()
            appUpdatePreferences.ensureInstalledFormat()
        }

        setContent {
            val themeMode by themePreferences.themeMode.collectAsStateWithLifecycle(
                initialValue = ThemeMode.System,
            )
            val isOnline by networkStatusMonitor.isOnline.collectAsStateWithLifecycle(
                initialValue = true,
            )
            val installedFormat by appUpdatePreferences.installedFormat.collectAsStateWithLifecycle(
                initialValue = "apk",
            )
            var showAbout by remember { mutableStateOf(false) }

            GoldenPathTheme(themeMode = themeMode) {
                GoldenPathScreen(
                    themeMode = themeMode,
                    isOnline = isOnline,
                    showAbout = showAbout,
                    appVersion = "0.1.0",
                    installedFormat = installedFormat ?: "apk",
                    updateStatus = getString(R.string.about_update_current),
                    onThemeToggle = {
                        lifecycleScope.launch {
                            val nextMode = themeMode.next()
                            themePreferences.setThemeMode(nextMode)
                        }
                    },
                    onAboutOpen = { showAbout = true },
                    onAboutClose = { showAbout = false },
                )
            }
        }
    }

    override fun onDestroy() {
        if (::networkStatusMonitor.isInitialized) {
            networkStatusMonitor.stop()
        }
        super.onDestroy()
    }
}
