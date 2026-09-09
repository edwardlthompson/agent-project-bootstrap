import type { ThemeMode } from "../theme";

export const SETTINGS_BUNDLE_VERSION = 1 as const;

export type SettingsBundle = {
  version: 1;
  theme: ThemeMode;
  saveCrashes: boolean;
};

function asTheme(value: unknown): ThemeMode | null {
  return value === "system" || value === "light" || value === "dark" ? value : null;
}

function asVersion(value: unknown): number | null {
  if (value === undefined) return 0;
  if (typeof value === "number" && Number.isInteger(value)) return value;
  if (typeof value === "string" && /^\d+$/.test(value)) return Number(value);
  return null;
}

/** Lift unversioned or v0/v1 settings JSON to the current bundle. */
export function migrateSettings(data: unknown): SettingsBundle | null {
  if (!data || typeof data !== "object" || Array.isArray(data)) return null;
  const rec = data as Record<string, unknown>;
  const version = asVersion(rec.version);
  if (version === null || version > SETTINGS_BUNDLE_VERSION || version < 0) return null;
  let theme = asTheme(rec.theme);
  if (!theme && rec.darkMode === true) theme = "dark";
  if (!theme && rec.darkMode === false) theme = "light";
  if (!theme) return null;
  return { version: 1, theme, saveCrashes: Boolean(rec.saveCrashes) };
}
