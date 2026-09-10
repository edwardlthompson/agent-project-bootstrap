import { describe, expect, it, vi } from "vitest";

import { createLaunchPromptDialog } from "./launchPrompt";

vi.mock("../i18n", () => ({
  t: (key: string) => key,
}));

describe("launch prompt buttons", () => {
  it("tokenizes accept and decline actions", () => {
    const onChoose = vi.fn();
    const dialog = createLaunchPromptDialog({ kind: "donate" }, onChoose);
    const accept = dialog.querySelector<HTMLButtonElement>(".gp-launch-accept");
    const decline = dialog.querySelector<HTMLButtonElement>(".gp-launch-decline");
    expect(accept).toBeTruthy();
    expect(decline).toBeTruthy();
    expect(dialog.querySelector(".gp-launch-actions")).toBeTruthy();
    accept?.click();
    expect(onChoose).toHaveBeenCalledWith(true);
  });
});
