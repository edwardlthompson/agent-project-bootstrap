package dev.foss.goldenpath.push

/**
 * FOSS UnifiedPush sample: talk to a distributor (ntfy, NextPush, …), never FCM.
 * Registration stays off until [pickDistributor] finds a package.
 */
object UnifiedPushConfig {
    const val CONNECTOR_ACTION = "org.unifiedpush.android.connector.MESSAGE"
    const val REGISTER_ACTION = "org.unifiedpush.android.distributor.REGISTER"
    const val UNREGISTER_ACTION = "org.unifiedpush.android.distributor.UNREGISTER"
    const val FEATURE_BYTES_MESSAGE = "org.unifiedpush.android.feature.BYTES_MESSAGE"
    const val INSTANCE_DEFAULT = "default"
    const val EXTRA_INSTANCE = "instance"

    fun usesProprietaryPush(): Boolean = false

    fun pickDistributor(packages: Iterable<String>): String? =
        packages.map { it.trim() }.firstOrNull { it.isNotEmpty() }

    fun state(packages: Iterable<String>, endpoint: String?): UnifiedPushState {
        val distributor = pickDistributor(packages)
        val url = endpoint?.trim().orEmpty().ifEmpty { null }
        return UnifiedPushState(
            distributorPackage = distributor,
            endpoint = url,
            enabled = distributor != null,
        )
    }

    fun registerExtras(instance: String = INSTANCE_DEFAULT): Map<String, String> =
        mapOf(EXTRA_INSTANCE to instance.ifBlank { INSTANCE_DEFAULT })

    fun parseMessage(action: String?, bytes: ByteArray?, text: String?): ByteArray? {
        if (action != CONNECTOR_ACTION) return null
        if (bytes != null && bytes.isNotEmpty()) return bytes
        val trimmed = text?.toByteArray(Charsets.UTF_8)
        return trimmed?.takeIf { it.isNotEmpty() }
    }
}

data class UnifiedPushState(
    val distributorPackage: String?,
    val endpoint: String?,
    val enabled: Boolean,
) {
    val registered: Boolean get() = enabled && !endpoint.isNullOrBlank()
}
