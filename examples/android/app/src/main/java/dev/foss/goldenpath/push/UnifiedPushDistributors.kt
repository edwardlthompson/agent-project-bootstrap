package dev.foss.goldenpath.push

import android.content.Intent
import android.content.pm.PackageManager

object UnifiedPushDistributors {
    fun installedPackages(pm: PackageManager): List<String> {
        val intent = Intent(UnifiedPushConfig.REGISTER_ACTION)
        // ntfy (and most UP distributors) expose REGISTER on a BroadcastReceiver
        // without CATEGORY_DEFAULT — do not use MATCH_DEFAULT_ONLY.
        val flags = 0
        val fromActivities =
            pm.queryIntentActivities(intent, flags)
                .mapNotNull { it.activityInfo?.packageName }
        val fromReceivers =
            pm.queryBroadcastReceivers(intent, flags)
                .mapNotNull { it.activityInfo?.packageName }
        return (fromActivities + fromReceivers).distinct()
    }
}
