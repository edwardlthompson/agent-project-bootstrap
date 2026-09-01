package dev.foss.goldenpath.ui.nav

import android.content.Context

class NavPreferences(context: Context) {
    private val prefs = context.applicationContext.getSharedPreferences(NavStore.PREFS, Context.MODE_PRIVATE)

    fun read(): NavState = NavStore.load(prefs.getString(NavStore.KEY, null))

    fun write(state: NavState) {
        prefs.edit().putString(NavStore.KEY, NavStore.save(state)).apply()
    }
}
