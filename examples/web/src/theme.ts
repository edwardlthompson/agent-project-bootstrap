import themeMeta from "./theme-meta.json";

export type ThemeMode = "system" | "light" | "dark";

const STORAGE_KEY = "gp-theme";

let currentMode: ThemeMode = "system";
let mediaQuery: MediaQueryList | null = null;
let mediaListener: ((event: MediaQueryListEvent) => void) | null = null;
const themeListeners = new Set<() => void>();

function notifyThemeListeners(): void {
  themeListeners.forEach((fn) => fn());
}

export function subscribeThemeChange(listener: () => void): () => void {
  themeListeners.add(listener);
  return () => themeListeners.delete(listener);
}

function readStoredMode(): ThemeMode {
  const stored = localStorage.getItem(STORAGE_KEY);
  if (stored === "light" || stored === "dark" || stored === "system") {
    return stored;
  }
  return "system";
}

function resolvedIsDark(): boolean {
  if (currentMode === "dark") {
    return true;
  }
  if (currentMode === "light") {
    return false;
  }
  return window.matchMedia("(prefers-color-scheme: dark)").matches;
}

function updateThemeColorMeta(): void {
  const meta = document.querySelector('meta[name="theme-color"]');
  if (!meta) {
    return;
  }
  meta.setAttribute(
    "content",
    resolvedIsDark() ? themeMeta.themeColorDark : themeMeta.themeColorLight,
  );
}

function ensureThemeLiveRegion(): HTMLElement {
  let live = document.getElementById("gp-theme-live");
  if (!live) {
    live = document.createElement("div");
    live.id = "gp-theme-live";
    live.setAttribute("role", "status");
    live.setAttribute("aria-live", "polite");
    live.setAttribute("aria-atomic", "true");
    live.className = "gp-visually-hidden";
    document.body.appendChild(live);
  }
  return live;
}

function announceThemeChange(): void {
  const live = ensureThemeLiveRegion();
  const label =
    currentMode === "system"
      ? "Theme set to system"
      : currentMode === "dark"
        ? "Theme set to dark"
        : "Theme set to light";
  live.textContent = "";
  // Force polite re-announcement when mode repeats after navigation.
  window.requestAnimationFrame(() => {
    live.textContent = label;
  });
}

function applyDomTheme(): void {
  document.documentElement.dataset.theme = currentMode;
  updateThemeColorMeta();
}

function detachMediaListener(): void {
  if (mediaQuery && mediaListener) {
    mediaQuery.removeEventListener("change", mediaListener);
  }
  mediaQuery = null;
  mediaListener = null;
}

function attachMediaListener(): void {
  detachMediaListener();
  if (currentMode !== "system") {
    return;
  }
  mediaQuery = window.matchMedia("(prefers-color-scheme: dark)");
  mediaListener = () => {
    updateThemeColorMeta();
    notifyThemeListeners();
  };
  mediaQuery.addEventListener("change", mediaListener);
}

export function getThemeMode(): ThemeMode {
  return currentMode;
}

export function setThemeMode(mode: ThemeMode): void {
  currentMode = mode;
  localStorage.setItem(STORAGE_KEY, mode);
  applyDomTheme();
  attachMediaListener();
  announceThemeChange();
  notifyThemeListeners();
}

export function cycleThemeMode(): ThemeMode {
  const next: ThemeMode =
    currentMode === "system" ? "light" : currentMode === "light" ? "dark" : "system";
  setThemeMode(next);
  return next;
}

export function initTheme(): ThemeMode {
  currentMode = readStoredMode();
  applyDomTheme();
  attachMediaListener();
  return currentMode;
}

export function isDarkTheme(): boolean {
  return resolvedIsDark();
}
