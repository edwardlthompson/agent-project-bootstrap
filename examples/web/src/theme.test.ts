import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import {
  cycleThemeMode,
  getThemeMode,
  initTheme,
  isDarkTheme,
  setThemeMode,
  subscribeThemeChange,
} from "./theme";

describe("theme", () => {
  beforeEach(() => {
    document.documentElement.dataset.theme = "system";
    document.body.innerHTML = "";
    localStorage.clear();
    vi.stubGlobal(
      "matchMedia",
      vi.fn().mockImplementation((query: string) => ({
        matches: query.includes("dark"),
        media: query,
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
      })),
    );
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("initializes from storage", () => {
    localStorage.setItem("gp-theme", "light");
    initTheme();
    expect(getThemeMode()).toBe("light");
    expect(document.documentElement.dataset.theme).toBe("light");
  });

  it("cycles system → light → dark → system", () => {
    initTheme();
    setThemeMode("system");
    expect(cycleThemeMode()).toBe("light");
    expect(cycleThemeMode()).toBe("dark");
    expect(cycleThemeMode()).toBe("system");
  });

  it("resolves dark theme for dark mode", () => {
    setThemeMode("dark");
    expect(isDarkTheme()).toBe(true);
  });

  it("notifies subscribers when OS color scheme changes under system mode", () => {
    const listeners: Array<(event: MediaQueryListEvent) => void> = [];
    vi.stubGlobal(
      "matchMedia",
      vi.fn().mockImplementation((query: string) => ({
        matches: query.includes("dark"),
        media: query,
        addEventListener: (_: string, fn: (event: MediaQueryListEvent) => void) => {
          listeners.push(fn);
        },
        removeEventListener: vi.fn(),
      })),
    );
    const seen: boolean[] = [];
    setThemeMode("system");
    subscribeThemeChange(() => seen.push(isDarkTheme()));
    expect(listeners.length).toBeGreaterThan(0);
    listeners[0]({ matches: true } as MediaQueryListEvent);
    expect(seen.length).toBeGreaterThan(0);
  });

  it("announces theme changes on an aria-live region", async () => {
    setThemeMode("dark");
    await new Promise<void>((resolve) => requestAnimationFrame(() => resolve()));
    const live = document.getElementById("gp-theme-live");
    expect(live?.getAttribute("aria-live")).toBe("polite");
    expect(live?.textContent || "").toMatch(/dark/i);
  });
});
