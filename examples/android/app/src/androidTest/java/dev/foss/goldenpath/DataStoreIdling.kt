package dev.foss.goldenpath

import androidx.test.espresso.IdlingResource
import java.util.concurrent.atomic.AtomicInteger

/** Simple counting IdlingResource for DataStore reads in instrumented tests. */
class DataStoreIdling(private val name: String = "datastore-idle") : IdlingResource {
    private val counter = AtomicInteger(0)
    @Volatile private var callback: IdlingResource.ResourceCallback? = null

    fun increment() {
        counter.incrementAndGet()
    }

    fun decrement() {
        if (counter.decrementAndGet() == 0) {
            callback?.onTransitionToIdle()
        }
    }

    override fun getName(): String = name

    override fun isIdleNow(): Boolean = counter.get() == 0

    override fun registerIdleTransitionCallback(callback: IdlingResource.ResourceCallback?) {
        this.callback = callback
    }
}
