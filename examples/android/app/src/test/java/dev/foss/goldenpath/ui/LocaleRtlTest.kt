package dev.foss.goldenpath.ui

import android.content.Context
import android.view.View
import androidx.test.core.app.ApplicationProvider
import dev.foss.goldenpath.R
import org.junit.Assert.assertEquals
import org.junit.Assert.assertTrue
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config

@RunWith(RobolectricTestRunner::class)
class LocaleRtlTest {
    @Test
    @Config(sdk = [26], qualifiers = "es")
    fun spanishQualifiersLoadSearchLabel() {
        val context = ApplicationProvider.getApplicationContext<Context>()
        assertEquals("Buscar ajustes", context.getString(R.string.settings_search))
        assertEquals("Apariencia", context.getString(R.string.settings_section_appearance))
    }

    @Test
    @Config(sdk = [26], qualifiers = "ar-rSA-ldrtl")
    fun arabicQualifiersAreRtl() {
        val context = ApplicationProvider.getApplicationContext<Context>()
        assertEquals(View.LAYOUT_DIRECTION_RTL, context.resources.configuration.layoutDirection)
        assertTrue(context.getString(R.string.settings_open).isNotBlank())
    }
}
