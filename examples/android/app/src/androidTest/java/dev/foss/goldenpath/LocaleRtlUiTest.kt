package dev.foss.goldenpath

import android.content.Context
import android.content.res.Configuration
import android.os.LocaleList
import android.view.View
import androidx.test.core.app.ApplicationProvider
import androidx.test.ext.junit.runners.AndroidJUnit4
import java.util.Locale
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import org.junit.runner.RunWith

@RunWith(AndroidJUnit4::class)
class LocaleRtlUiTest {
    @Test
    fun spanishCatalogLoadsSettingsSearch() {
        val localized = contextFor(Locale("es"))
        assertEquals("Buscar ajustes", localized.getString(R.string.settings_search))
        assertEquals("Ajustes", localized.getString(R.string.settings_title))
        assertEquals("Privacidad", localized.getString(R.string.settings_section_privacy))
    }

    @Test
    fun arabicLocaleForcesRtlEvenWhenStringsFallback() {
        val localized = contextFor(Locale("ar"))
        assertEquals(View.LAYOUT_DIRECTION_RTL, localized.resources.configuration.layoutDirection)
        assertTrue(localized.getString(R.string.settings_search).isNotBlank())
        assertTrue(localized.getString(R.string.settings_title).isNotBlank())
    }

    private fun contextFor(locale: Locale): Context {
        val base = ApplicationProvider.getApplicationContext<Context>()
        val config = Configuration(base.resources.configuration)
        config.setLocales(LocaleList(locale))
        config.setLayoutDirection(locale)
        return base.createConfigurationContext(config)
    }
}
