import { describe, expect, it } from "vitest";

import { buildFeedbackUrl, isPlaceholderRepo } from "./feedback.js";

describe("feedback URL", () => {
  it("returns empty for placeholder repos", () => {
    expect(isPlaceholderRepo("OWNER/REPO")).toBe(true);
    expect(buildFeedbackUrl("OWNER/REPO", "bug").url).toBe("");
  });

  it("builds a GitHub issue-form URL", () => {
    const { url } = buildFeedbackUrl("acme/app", "feature", "Add locale");
    expect(url).toContain("https://github.com/acme/app/issues/new?");
    expect(url).toContain("template=feature_request.yml");
    expect(url).toContain("title=Add");
  });
});
