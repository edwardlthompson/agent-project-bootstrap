package dev.foss.goldenpath.push

import android.content.Intent
import android.content.pm.PackageManager

object UnifiedPushDistributors {
    fun installedPackages(pm: PackageManager): List<String> {
        val intent = Intent(UnifiedPushConfig.REGISTER_ACTION)
        return pm.queryIntentActivities(intent, PackageManager.MATCH_DEFAULT_ONLY)
            .mapNotNull { it.activityInfo?.packageName }
            .distinct()
    }
}
