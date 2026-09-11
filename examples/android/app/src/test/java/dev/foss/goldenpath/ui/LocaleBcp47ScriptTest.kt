package dev.foss.goldenpath.ui

import org.junit.Assert.assertTrue
import org.junit.Test
import java.io.File

/** Locale `b+` / script-tag resource qualifier smoke (#167). */
class LocaleBcp47ScriptTest {
    @Test
    fun bcp47ScriptQualifierDirectoryPresent() {
        val candidates = listOf(
            File("src/main/res/values-b+en+Latn/strings.xml"),
            File("app/src/main/res/values-b+en+Latn/strings.xml"),
        )
        val file = candidates.first { it.isFile }
        val text = file.readText()
        assertTrue(text.contains("settings_section_appearance"))
        assertTrue(text.contains("Appearance"))
    }
}
