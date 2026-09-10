package dev.foss.goldenpath.push

import android.content.BroadcastReceiver
import android.content.Context
import android.content.Intent
import android.util.Log

/** Distributor → app sample. No-op until a real payload arrives. */
class UnifiedPushMessageReceiver : BroadcastReceiver() {
    override fun onReceive(context: Context, intent: Intent) {
        val payload = UnifiedPushConfig.parseMessage(
            intent.action,
            intent.getByteArrayExtra(EXTRA_BYTES),
            intent.getStringExtra(EXTRA_MESSAGE),
        ) ?: return
        Log.d(TAG, "unifiedpush bytes=${payload.size}")
    }

    companion object {
        const val EXTRA_BYTES = "bytes"
        const val EXTRA_MESSAGE = "message"
        private const val TAG = "GpPush"
    }
}
