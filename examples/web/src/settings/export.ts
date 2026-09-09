import { getSaveCrashes, setSaveCrashes } from "../feedback/saveCrashes";
import { getThemeMode, setThemeMode } from "../theme";
import {
  migrateSettings,
  SETTINGS_BUNDLE_VERSION,
  type SettingsBundle,
} from "./migrate";

export type { SettingsBundle } from "./migrate";

export function snapshotSettings(): SettingsBundle {
  return {
    version: SETTINGS_BUNDLE_VERSION,
    theme: getThemeMode(),
    saveCrashes: getSaveCrashes(),
  };
}

export function parseSettings(raw: string): SettingsBundle | null {
  try {
    return migrateSettings(JSON.parse(raw));
  } catch {
    return null;
  }
}

export function applySettingsBundle(bundle: SettingsBundle): void {
  setThemeMode(bundle.theme);
  setSaveCrashes(bundle.saveCrashes);
}
