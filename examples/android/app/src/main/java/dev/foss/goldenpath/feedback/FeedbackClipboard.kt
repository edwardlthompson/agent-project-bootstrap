package dev.foss.goldenpath.feedback

import dev.foss.goldenpath.privacyreport.ReportMarkdown
import dev.foss.goldenpath.privacyreport.SanitizeReport
import org.json.JSONObject

/** Frozen schema for the sanitized feedback clipboard payload (markdown + structured fields). */
object FeedbackClipboard {
    const val SCHEMA_VERSION = 1

    data class Payload(
        val schemaVersion: Int = SCHEMA_VERSION,
        val kind: String,
        val whatHappened: String,
        val fingerprint: String? = null,
        val exceptionType: String? = null,
        val appVersion: String? = null,
        val osFamily: String? = null,
        val stack: String? = null,
        val markdown: String,
    )

    fun build(
        kind: String,
        description: String?,
        stack: String? = null,
        exceptionType: String? = null,
        fingerprint: String? = null,
        appVersion: String? = null,
        osFamily: String? = null,
    ): Payload {
        val reportKind = when (kind.lowercase()) {
            "crash", "bug", "feature" -> kind.lowercase()
            else -> "bug"
        }
        val markdown = ReportMarkdown.build(
            kind = reportKind,
            description = description,
            stack = stack,
            exceptionType = exceptionType,
            fingerprint = fingerprint,
            appVersion = appVersion,
            osFamily = osFamily,
        )
        return Payload(
            kind = reportKind,
            whatHappened = SanitizeReport.text(description).ifEmpty { "(no description)" },
            fingerprint = fingerprint?.takeIf { it.isNotBlank() },
            exceptionType = exceptionType?.takeIf { it.isNotBlank() },
            appVersion = appVersion?.takeIf { it.isNotBlank() },
            osFamily = osFamily?.takeIf { it.isNotBlank() },
            stack = SanitizeReport.text(stack, stack = true).takeIf { it.isNotEmpty() },
            markdown = markdown,
        )
    }

    fun toJson(payload: Payload): String =
        JSONObject()
            .put("schemaVersion", payload.schemaVersion)
            .put("kind", payload.kind)
            .put("whatHappened", payload.whatHappened)
            .put("fingerprint", payload.fingerprint ?: JSONObject.NULL)
            .put("exceptionType", payload.exceptionType ?: JSONObject.NULL)
            .put("appVersion", payload.appVersion ?: JSONObject.NULL)
            .put("osFamily", payload.osFamily ?: JSONObject.NULL)
            .put("stack", payload.stack ?: JSONObject.NULL)
            .put("markdown", payload.markdown)
            .toString(2)
}
