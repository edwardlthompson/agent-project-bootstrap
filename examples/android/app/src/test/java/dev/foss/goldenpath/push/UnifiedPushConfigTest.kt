package dev.foss.goldenpath.push

import org.junit.Assert.assertArrayEquals
import org.junit.Assert.assertEquals
import org.junit.Assert.assertFalse
import org.junit.Assert.assertNull
import org.junit.Assert.assertTrue
import org.junit.Test

class UnifiedPushConfigTest {
    @Test
    fun staysFossAndPicksFirstDistributor() {
        assertFalse(UnifiedPushConfig.usesProprietaryPush())
        assertTrue(UnifiedPushConfig.CONNECTOR_ACTION.startsWith("org.unifiedpush."))
        assertEquals("io.heckel.ntfy", UnifiedPushConfig.pickDistributor(listOf("  ", "io.heckel.ntfy")))
        assertNull(UnifiedPushConfig.pickDistributor(listOf("", "  ")))
    }

    @Test
    fun stateIsOffWithoutDistributorAndRegisteredWithEndpoint() {
        val off = UnifiedPushConfig.state(emptyList(), "https://up.example/ep")
        assertFalse(off.enabled)
        assertFalse(off.registered)
        val on = UnifiedPushConfig.state(listOf("io.heckel.ntfy"), "https://up.example/ep")
        assertTrue(on.enabled)
        assertTrue(on.registered)
        assertEquals("io.heckel.ntfy", on.distributorPackage)
    }

    @Test
    fun registerExtrasDefaultInstance() {
        assertEquals(
            mapOf(UnifiedPushConfig.EXTRA_INSTANCE to UnifiedPushConfig.INSTANCE_DEFAULT),
            UnifiedPushConfig.registerExtras(""),
        )
    }

    @Test
    fun parseMessageIgnoresOtherActions() {
        assertNull(UnifiedPushConfig.parseMessage("android.intent.action.VIEW", byteArrayOf(1), "x"))
        assertArrayEquals(
            byteArrayOf(9, 8),
            UnifiedPushConfig.parseMessage(UnifiedPushConfig.CONNECTOR_ACTION, byteArrayOf(9, 8), "ignored"),
        )
        assertArrayEquals(
            "hi".toByteArray(),
            UnifiedPushConfig.parseMessage(UnifiedPushConfig.CONNECTOR_ACTION, null, "hi"),
        )
    }
}
