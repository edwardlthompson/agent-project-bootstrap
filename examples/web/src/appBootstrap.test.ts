import { beforeEach, describe, expect, it, vi } from "vitest";
import { bootstrapApp } from "./appBootstrap";
import { checkForUpdates, handleRestartGuard } from "./about/aboutSession";
import type { AppShellCallbacks } from "./AppShell";

vi.mock("./AppShell", () => ({
  createAppShell: vi.fn(),
}));

vi.mock("./about/aboutSession", () => ({
  handleRestartGuard: vi.fn(() => false),
  checkForUpdates: vi.fn(() => Promise.resolve("about.update.current")),
}));

vi.mock("./about/donations", () => ({
  loadDonations: vi.fn(() =>
    Promise.resolve({ enabled: true, message: "thanks", links: [] }),
  ),
}));

vi.mock("./theme", () => ({
  initTheme: vi.fn(),
  subscribeThemeChange: vi.fn(),
}));

vi.mock("./i18n", () => ({
  t: vi.fn((key: string) => key),
}));

import { createAppShell } from "./AppShell";

describe("bootstrapApp", () => {
  let handlers: AppShellCallbacks | undefined;

  beforeEach(() => {
    vi.clearAllMocks();
    handlers = undefined;
    vi.mocked(createAppShell).mockImplementation((_root, _state, h) => {
      handlers = h;
    });
    Object.defineProperty(navigator, "serviceWorker", {
      configurable: true,
      value: { register: vi.fn(() => Promise.resolve()) },
    });
  });

  it("renders app shell on bootstrap", async () => {
    const root = document.createElement("div");
    bootstrapApp(root);
    await vi.waitFor(() => {
      expect(createAppShell).toHaveBeenCalledWith(
        root,
        expect.objectContaining({ updateStatus: "about.update.current" }),
        expect.any(Object),
      );
    });
  });

  it("re-renders when shell state changes", async () => {
    const root = document.createElement("div");
    bootstrapApp(root);
    await vi.waitFor(() => expect(handlers).toBeDefined());
    const callsBefore = vi.mocked(createAppShell).mock.calls.length;
    handlers!.onState({ showAbout: true });
    expect(createAppShell.mock.calls.length).toBeGreaterThan(callsBefore);
  });

  it("refreshes update status when check toggle enabled", async () => {
    const root = document.createElement("div");
    bootstrapApp(root);
    await vi.waitFor(() => expect(handlers).toBeDefined());
    vi.mocked(checkForUpdates).mockResolvedValueOnce("about.update.available");
    handlers!.onUpdateCheckChange(true);
    await vi.waitFor(() =>
      expect(
        vi
          .mocked(createAppShell)
          .mock.calls.some(([, state]) => state.updateStatus === "about.update.available"),
      ).toBe(true),
    );
  });

  it("registers service worker on load", async () => {
    const root = document.createElement("div");
    bootstrapApp(root);
    window.dispatchEvent(new Event("load"));
    await vi.waitFor(() => {
      expect(navigator.serviceWorker.register).toHaveBeenCalledWith("/sw.js");
    });
  });

  it("skips background update check when restart guard is active", async () => {
    vi.mocked(handleRestartGuard).mockReturnValueOnce(true);
    vi.mocked(checkForUpdates).mockClear();
    const root = document.createElement("div");
    bootstrapApp(root);
    await vi.waitFor(() => expect(handlers).toBeDefined());
    expect(checkForUpdates).not.toHaveBeenCalled();
  });

  it("ignores disabled update-check toggle", async () => {
    const root = document.createElement("div");
    bootstrapApp(root);
    await vi.waitFor(() => expect(handlers).toBeDefined());
    const callsBefore = vi.mocked(checkForUpdates).mock.calls.length;
    handlers!.onUpdateCheckChange(false);
    expect(checkForUpdates.mock.calls.length).toBe(callsBefore);
  });

  it("re-renders about panel when background update completes while open", async () => {
    let resolveCheck: (value: string) => void = () => {};
    vi.mocked(checkForUpdates).mockImplementation(
      () =>
        new Promise((resolve) => {
          resolveCheck = resolve;
        }),
    );
    const root = document.createElement("div");
    bootstrapApp(root);
    await vi.waitFor(() => expect(handlers).toBeDefined());
    handlers!.onState({ showAbout: true });
    const callsBefore = vi.mocked(createAppShell).mock.calls.length;
    resolveCheck("about.update.available");
    await vi.waitFor(() =>
      expect(createAppShell.mock.calls.length).toBeGreaterThan(callsBefore),
    );
  });
});
