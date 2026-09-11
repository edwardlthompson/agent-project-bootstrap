import { beforeEach, describe, expect, it } from "vitest";
import { setLocale, t } from "./index";

describe("feedback kind titles", () => {
  beforeEach(() => {
    setLocale("en");
  });

  it("Bug vs Feature titles differ and are non-empty", () => {
    const bug = t("feedback.bug.title");
    const feature = t("feedback.feature.title");
    expect(bug.length).toBeGreaterThan(0);
    expect(feature.length).toBeGreaterThan(0);
    expect(bug).not.toBe(feature);
    expect(bug.toLowerCase()).toMatch(/bug/);
    expect(feature.toLowerCase()).toMatch(/feature/);
  });
});
