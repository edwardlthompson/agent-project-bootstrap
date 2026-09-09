import { describe, expect, it } from "vitest";
import { applySettingsSearch, tokensMatch } from "./search";

describe("settings search", () => {
  it("matches trimmed case-insensitive substrings", () => {
    expect(tokensMatch("", "Appearance Theme")).toBe(true);
    expect(tokensMatch("  THEME ", "Appearance Theme")).toBe(true);
    expect(tokensMatch("privacy", "Appearance Theme")).toBe(false);
  });

  it("hides groups and shows empty state", () => {
    const a = document.createElement("section");
    a.dataset.settingsHaystack = "Appearance Theme";
    const b = document.createElement("section");
    b.dataset.settingsHaystack = "Privacy crashes";
    const empty = document.createElement("p");
    empty.hidden = true;
    expect(applySettingsSearch("privacy", [a, b], empty)).toBe(1);
    expect(a.hidden).toBe(true);
    expect(b.hidden).toBe(false);
    expect(empty.hidden).toBe(true);
    expect(applySettingsSearch("zzzz", [a, b], empty)).toBe(0);
    expect(empty.hidden).toBe(false);
    expect(applySettingsSearch("", [a, b], empty)).toBe(2);
    expect(empty.hidden).toBe(true);
  });
});
