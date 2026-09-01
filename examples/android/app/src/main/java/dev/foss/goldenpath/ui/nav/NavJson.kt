package dev.foss.goldenpath.ui.nav

object NavJson {
    fun serialize(state: NavState): String {
        val stack = Nav.normalizeStack(state.stack).joinToString(",") { "\"${it.wire}\"" }
        val kind = state.feedbackKind?.let { "\"${it.wire}\"" } ?: "null"
        val scroll = state.scroll
            .filterKeys { it != GpRoute.Home }
            .entries
            .joinToString(",") { "\"${it.key.wire}\":${it.value.coerceAtLeast(0)}" }
        return "{\"stack\":[$stack],\"feedbackKind\":$kind,\"scroll\":{$scroll},\"promptOpen\":${state.promptOpen}}"
    }

    fun deserialize(raw: String?): NavState {
        if (raw.isNullOrBlank()) return Nav.home()
        return runCatching { parse(raw.trim()) }.getOrElse { Nav.home() }
    }

    private fun parse(raw: String): NavState {
        if (!raw.startsWith("{") || !raw.endsWith("}")) error("not object")
        val stackBlob = arrayBlob(raw, "stack") ?: error("stack")
        val stack = Nav.normalizeStack(
            Regex("\"([a-z]+)\"").findAll(stackBlob).mapNotNull { GpRoute.fromWire(it.groupValues[1]) }.toList(),
        )
        val kindMatch = Regex("\"feedbackKind\"\\s*:\\s*(null|\"([a-z]+)\")").find(raw)
        val kind = kindMatch?.groupValues?.getOrNull(2)?.let(FeedbackKind::fromWire)
        val scrollBlob = objectBlob(raw, "scroll").orEmpty()
        val scroll = mutableMapOf<GpRoute, Int>()
        Regex("\"([a-z]+)\"\\s*:\\s*(-?\\d+)").findAll(scrollBlob).forEach { match ->
            val route = GpRoute.fromWire(match.groupValues[1]) ?: return@forEach
            if (route != GpRoute.Home) scroll[route] = match.groupValues[2].toInt().coerceAtLeast(0)
        }
        val prompt = Regex("\"promptOpen\"\\s*:\\s*(true|false)").find(raw)?.groupValues?.get(1) == "true"
        val top = stack.last()
        return NavState(
            stack = stack,
            feedbackKind = if (top == GpRoute.Feedback) kind else null,
            scroll = scroll,
            promptOpen = prompt,
        )
    }

    private fun arrayBlob(raw: String, key: String): String? {
        val start = Regex("\"$key\"\\s*:\\s*\\[").find(raw)?.range?.last ?: return null
        val end = raw.indexOf(']', start)
        if (end < 0) return null
        return raw.substring(start + 1, end)
    }

    private fun objectBlob(raw: String, key: String): String? {
        val start = Regex("\"$key\"\\s*:\\s*\\{").find(raw)?.range?.last ?: return null
        val end = raw.indexOf('}', start)
        if (end < 0) return null
        return raw.substring(start + 1, end)
    }
}
