import { describe, expect, it } from "vitest";
import { migrateSettings } from "./migrate";

describe("settings migrate", () => {
  it("promotes unversioned and string versions to v1", () => {
    expect(migrateSettings({ theme: "light", saveCrashes: true })).toEqual({
      version: 1,
      theme: "light",
      saveCrashes: true,
    });
    expect(migrateSettings({ version: "1", theme: "dark" })).toEqual({
      version: 1,
      theme: "dark",
      saveCrashes: false,
    });
  });

  it("maps legacy darkMode and rejects future versions", () => {
    expect(migrateSettings({ darkMode: true })).toEqual({
      version: 1,
      theme: "dark",
      saveCrashes: false,
    });
    expect(migrateSettings({ version: 2, theme: "dark" })).toBeNull();
    expect(migrateSettings({ version: -1, theme: "dark" })).toBeNull();
    expect(migrateSettings(null)).toBeNull();
  });
});
