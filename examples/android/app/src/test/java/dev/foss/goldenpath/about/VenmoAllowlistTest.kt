package dev.foss.goldenpath.about

import org.junit.Assert.assertFalse
import org.junit.Assert.assertTrue
import org.junit.Test

class VenmoAllowlistTest {
    @Test
    fun allowsExemplar() {
        assertTrue(VenmoAllowlist.isAllowed("https://venmo.com/code?user_id=1857304970395648420"))
    }

    @Test
    fun rejectsOthers() {
        assertFalse(VenmoAllowlist.isAllowed("https://evil.example/code?user_id=1"))
        assertFalse(VenmoAllowlist.isAllowed("http://venmo.com/code?user_id=1"))
    }
}
