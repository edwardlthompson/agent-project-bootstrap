package dev.foss.goldenpath

import android.os.Bundle
import androidx.activity.ComponentActivity
import androidx.activity.compose.setContent
import androidx.activity.enableEdgeToEdge
import androidx.compose.runtime.getValue
import androidx.lifecycle.lifecycleScope
import androidx.lifecycle.compose.collectAsStateWithLifecycle
import dev.foss.goldenpath.network.NetworkStatusMonitor
import dev.foss.goldenpath.ui.GoldenPathScreen
import dev.foss.goldenpath.ui.theme.GoldenPathTheme
import dev.foss.goldenpath.ui.theme.ThemeMode
import dev.foss.goldenpath.ui.theme.ThemePreferences
import dev.foss.goldenpath.ui.theme.next
import kotlinx.coroutines.launch

class MainActivity : ComponentActivity() {
    private lateinit var themePreferences: ThemePreferences
    private lateinit var networkStatusMonitor: NetworkStatusMonitor

    override fun onCreate(savedInstanceState: Bundle?) {
        super.onCreate(savedInstanceState)
        enableEdgeToEdge()
        themePreferences = ThemePreferences(applicationContext)
        networkStatusMonitor = NetworkStatusMonitor(applicationContext)
        networkStatusMonitor.start()

        setContent {
            val themeMode by themePreferences.themeMode.collectAsStateWithLifecycle(
                initialValue = ThemeMode.System,
            )
            val isOnline by networkStatusMonitor.isOnline.collectAsStateWithLifecycle(
                initialValue = true,
            )

            GoldenPathTheme(themeMode = themeMode) {
                GoldenPathScreen(
                    themeMode = themeMode,
                    isOnline = isOnline,
                    onThemeToggle = {
                        lifecycleScope.launch {
                            val nextMode = themeMode.next()
                            themePreferences.setThemeMode(nextMode)
                        }
                    },
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
