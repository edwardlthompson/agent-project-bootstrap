import { beforeEach, describe, expect, it } from "vitest";
import { createSettingsPanel } from "../components/SettingsPanel";
import { setLocale } from "../i18n";
import { SETTINGS_SECTION_ORDER } from "./sectionOrder";

describe("settings section order", () => {
  beforeEach(() => {
    setLocale("en");
    localStorage.clear();
  });

  it("locks appearance → privacy → data → about", () => {
    expect([...SETTINGS_SECTION_ORDER]).toEqual(["appearance", "privacy", "data", "about"]);
    const panel = createSettingsPanel({ onClose: () => undefined });
    const haystacks = [...panel.querySelectorAll("[data-settings-haystack]")].map(
      (el) => el.getAttribute("data-settings-haystack") || "",
    );
    expect(haystacks.length).toBeGreaterThanOrEqual(4);
    const joined = haystacks.join(" || ");
    const appearanceAt = joined.indexOf("Appearance");
    const privacyAt = joined.indexOf("Privacy");
    const dataAt = joined.indexOf("Data");
    const aboutAt = joined.indexOf("About");
    expect(appearanceAt).toBeGreaterThanOrEqual(0);
    expect(privacyAt).toBeGreaterThan(appearanceAt);
    expect(dataAt).toBeGreaterThan(privacyAt);
    expect(aboutAt).toBeGreaterThan(dataAt);
  });
});
