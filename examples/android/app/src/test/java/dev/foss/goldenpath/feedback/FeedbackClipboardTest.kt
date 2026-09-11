package dev.foss.goldenpath.feedback

import java.nio.charset.StandardCharsets
import org.json.JSONObject
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test
import org.junit.runner.RunWith
import org.robolectric.RobolectricTestRunner
import org.robolectric.annotation.Config

@RunWith(RobolectricTestRunner::class)
@Config(sdk = [26])
class FeedbackClipboardTest {
    @Test
    fun goldenJsonMatchesFrozenSchema() {
        val golden = loadGolden()
        val built = FeedbackClipboard.build(
            kind = golden.getString("kind"),
            description = "steps to reproduce",
            appVersion = golden.optString("appVersion").takeIf { it.isNotBlank() && it != "null" },
            osFamily = golden.optString("osFamily").takeIf { it.isNotBlank() && it != "null" },
        )
        assertEquals(1, built.schemaVersion)
        assertEquals("bug", built.kind)
        assertEquals("steps to reproduce", built.whatHappened)
        assertEquals("0.1.0", built.appVersion)
        assertEquals("Android", built.osFamily)
        assertEquals(golden.getString("markdown"), built.markdown)
        assertFalse(built.markdown.contains("ghp_"))

        val json = JSONObject(FeedbackClipboard.toJson(built))
        assertEquals(1, json.getInt("schemaVersion"))
        assertEquals("bug", json.getString("kind"))
        assertTrue(json.isNull("fingerprint"))
        assertTrue(json.isNull("stack"))
        assertEquals(golden.getString("markdown"), json.getString("markdown"))
    }

    @Test
    fun previewCanSubmitStillWorks() {
        assertTrue(FeedbackPreview.canSubmit("steps", null))
        assertFalse(FeedbackPreview.canSubmit("  ", null))
    }

    private fun loadGolden(): JSONObject {
        val loaders = listOfNotNull(
            FeedbackClipboardTest::class.java.getResourceAsStream("/feedback-clipboard.golden.json"),
            FeedbackClipboardTest::class.java.classLoader?.getResourceAsStream("feedback-clipboard.golden.json"),
        )
        val stream = loaders.firstOrNull()
        if (stream != null) {
            return JSONObject(stream.use { String(it.readBytes(), StandardCharsets.UTF_8) })
        }
        val files = listOf(
            java.io.File("../../../../../../schemas/golden-path/feedback-clipboard.golden.json"),
            java.io.File("../../../schemas/golden-path/feedback-clipboard.golden.json"),
            java.io.File("../../schemas/golden-path/feedback-clipboard.golden.json"),
        )
        val hit = files.map { it.canonicalFile }.firstOrNull { it.isFile }
            ?: error("missing feedback-clipboard.golden.json")
        return JSONObject(hit.readText(Charsets.UTF_8))
    }
}
