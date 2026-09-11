/** Locked Settings IA order for chrome tests. */
export const SETTINGS_SECTION_ORDER = ["appearance", "privacy", "data", "about"] as const;

export type SettingsSectionId = (typeof SETTINGS_SECTION_ORDER)[number];
