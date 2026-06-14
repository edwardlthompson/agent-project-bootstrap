import { describe, expect, it } from "vitest";
import {
  compareVersions,
  isNewerVersion,
  parseReleaseVersion,
  selectReleaseAsset,
  shouldCheck,
} from "./updateChecker";

describe("shouldCheck", () => {
  it("returns false when off", () => {
    expect(shouldCheck("off", null, 0)).toBe(false);
  });

  it("returns true on session when never checked", () => {
    expect(shouldCheck("on_session", null, 100)).toBe(true);
    expect(shouldCheck("on_session", 50, 100)).toBe(false);
  });
});

describe("parseReleaseVersion", () => {
  it("parses semver tags", () => {
    expect(parseReleaseVersion("v1.2.3")).toBe("1.2.3");
  });
});

describe("isNewerVersion", () => {
  it("detects newer releases", () => {
    expect(isNewerVersion("1.0.0", "1.0.1")).toBe(true);
    expect(isNewerVersion("1.0.1", "1.0.0")).toBe(false);
  });
});

describe("selectReleaseAsset", () => {
  it("matches exact format only", () => {
    const assets = [
      { format: "msi", url: "https://example.com/a.msi" },
      { format: "exe", url: "https://example.com/a.exe" },
    ];
    expect(selectReleaseAsset(assets, "msi")?.url).toContain(".msi");
    expect(selectReleaseAsset(assets, "exe")?.url).toContain(".exe");
    expect(selectReleaseAsset(assets, "deb")).toBeNull();
  });
});
