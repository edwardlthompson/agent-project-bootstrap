import { describe, expect, it } from "vitest";
import { createLaunchPromptDialog } from "./launchPrompt";
import type { LaunchPrompt } from "./runAppUpdates";

const FORBIDDEN = ["gtag(", "plausible(", "posthog", "mixpanel", "segment."];

describe("launch prompt analytics-free", () => {
  it("Not now / Later handlers do not call analytics SDKs", () => {
    const prompt: LaunchPrompt = {
      kind: "update",
      version: "9.9.9",
      url: "https://example.com/app",
    };
    const dialog = createLaunchPromptDialog(prompt, () => undefined);
    const decline = dialog.querySelector("[data-testid='launch-decline']");
    expect(decline).toBeTruthy();
    const src = createLaunchPromptDialog.toString().toLowerCase();
    for (const needle of FORBIDDEN) {
      expect(src.includes(needle)).toBe(false);
    }
  });
});
