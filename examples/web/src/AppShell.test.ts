import { describe, expect, it, vi } from "vitest";
import { type AppShellCallbacks, createAppShell } from "./AppShell";
import { homeNav, push, recordScroll } from "./nav";

vi.mock("./i18n", () => ({
  t: (key: string) => key,
}));

function handlers(): AppShellCallbacks {
  return {
    onState: vi.fn(),
    onPushRoute: vi.fn(),
    onPop: vi.fn(),
  };
}

function baseState() {
  return {
    nav: homeNav(),
    updateStatus: "about.update.current",
    donations: { enabled: false, message: "", links: [] as { label: string; url: string }[] },
    launchPrompt: null as null,
  };
}

describe("createAppShell nav render", () => {
  it("renders settings from current(nav), not boolean flags", () => {
    const root = document.createElement("div");
    createAppShell(root, { ...baseState(), nav: push(homeNav(), "settings") }, handlers());
    expect(root.querySelector("[data-testid='settings-panel']")).toBeTruthy();
    expect(root.querySelector("[data-testid='about-panel']")).toBeNull();
  });

  it("Close and Escape bind to onPop", () => {
    const cb = handlers();
    const root = document.createElement("div");
    createAppShell(root, { ...baseState(), nav: push(homeNav(), "about") }, cb);
    root.querySelector<HTMLButtonElement>(".gp-about-close")?.click();
    expect(cb.onPop).toHaveBeenCalledTimes(1);
    const panel = root.querySelector("[data-testid='about-panel']");
    panel?.dispatchEvent(new KeyboardEvent("keydown", { key: "Escape", bubbles: true }));
    expect(cb.onPop).toHaveBeenCalledTimes(2);
  });

  it("About report-bug pushes feedback instead of flattening", () => {
    const cb = handlers();
    const root = document.createElement("div");
    createAppShell(root, { ...baseState(), nav: push(homeNav(), "about") }, cb);
    root.querySelector<HTMLButtonElement>("[data-testid='about-report-bug']")?.click();
    expect(cb.onPushRoute).toHaveBeenCalledWith("feedback", "bug");
    expect(cb.onPop).not.toHaveBeenCalled();
  });

  it("header About toggles via onPop when already on about", () => {
    const cb = handlers();
    const root = document.createElement("div");
    createAppShell(root, { ...baseState(), nav: push(homeNav(), "about") }, cb);
    root
      .querySelector("[data-about-open]")
      ?.dispatchEvent(new MouseEvent("click", { bubbles: true }));
    expect(cb.onPop).toHaveBeenCalledTimes(1);
    expect(cb.onPushRoute).not.toHaveBeenCalled();
  });

  it("restores persisted panel scroll", () => {
    const root = document.createElement("div");
    const nav = recordScroll(push(homeNav(), "settings"), "settings", 42);
    createAppShell(root, { ...baseState(), nav }, handlers());
    const panel = root.querySelector<HTMLElement>("[data-testid='settings-panel']");
    expect(panel?.scrollTop).toBe(42);
  });
});
