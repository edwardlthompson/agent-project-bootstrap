import "./style.css";
import { clearRestartGuard, getRestartGuardKey, isRestartPending } from "./about/applyUpdate";
import { loadDonations } from "./about/donations";
import type { AppUpdateConfig, CheckInterval } from "./about/types";
import {
  detectInstalledFormat,
  isNewerVersion,
  parseReleaseVersion,
  shouldCheck,
} from "./about/updateChecker";
import { createAboutPanel } from "./components/AboutPanel";
import { createThemeToggle } from "./components/ThemeToggle";
import { isOnline } from "./greet";
import { t } from "./i18n";
import { initTheme } from "./theme";

const APP_VERSION = "0.1.0";
const INTERVAL_KEY = "gp-app-update-interval";
const LAST_CHECKED_KEY = "gp-app-update-last-checked";

const app = document.querySelector<HTMLDivElement>("#app");
if (!app) {
  throw new Error("App root element not found");
}
const root = app;

let showAbout = false;
let updateStatus = t("about.update.current");
let donations = { enabled: false, message: "", links: [] as { label: string; url: string }[] };

function getInterval(): CheckInterval {
  const stored = localStorage.getItem(INTERVAL_KEY) as CheckInterval | null;
  return stored ?? "weekly";
}

function setIntervalPref(interval: CheckInterval): void {
  localStorage.setItem(INTERVAL_KEY, interval);
}

async function loadAppUpdateConfig(): Promise<AppUpdateConfig | null> {
  try {
    const res = await fetch("/app-update.json");
    if (!res.ok) return null;
    return (await res.json()) as AppUpdateConfig;
  } catch {
    return null;
  }
}

async function checkForUpdates(): Promise<void> {
  const config = await loadAppUpdateConfig();
  if (!config) return;
  const now = Date.now();
  const last = Number(localStorage.getItem(LAST_CHECKED_KEY) || "0") || null;
  const interval = getInterval();
  if (!shouldCheck(interval, last, now)) return;

  localStorage.setItem(LAST_CHECKED_KEY, String(now));
  const format = config.installed_artifact_format ?? detectInstalledFormat();
  if (format !== "pwa") {
    updateStatus = t("about.update.no_compatible");
    return;
  }

  if (!config.release_repo) return;
  try {
    const res = await fetch(
      `https://api.github.com/repos/${config.release_repo}/releases/latest`,
    );
    if (!res.ok) return;
    const body = (await res.json()) as { tag_name?: string };
    const latest = body.tag_name ? parseReleaseVersion(body.tag_name) : null;
    if (latest && isNewerVersion(APP_VERSION, latest)) {
      updateStatus = `${t("about.update.available")}: ${latest}`;
    } else {
      updateStatus = t("about.update.current");
    }
  } catch {
    // offline or rate limit — keep current status
  }
}

function render(): void {
  const online = isOnline();
  const statusKey = online ? "app.status.online" : "app.status.offline";

  root.innerHTML = `
    <main>
      <div class="gp-header">
        <h1 class="gp-title">${t("app.title")}</h1>
        <div class="gp-header-actions">
          <button type="button" class="gp-about-btn" data-about-open aria-label="${t("about.open")}">i</button>
        </div>
      </div>
      <p class="gp-headline">${t("app.greeting")}</p>
      <p class="gp-body" data-testid="status">${t(statusKey)}</p>
      <div data-about-mount></div>
    </main>
  `;

  const header = root.querySelector<HTMLDivElement>(".gp-header");
  const actions = root.querySelector<HTMLDivElement>(".gp-header-actions");
  if (header && actions) {
    actions.insertBefore(createThemeToggle(), actions.firstChild);
  }

  root.querySelector("[data-about-open]")?.addEventListener("click", () => {
    showAbout = !showAbout;
    renderAbout();
  });

  renderAbout();
}

function renderAbout(): void {
  const mount = root.querySelector("[data-about-mount]");
  if (!mount) return;
  mount.innerHTML = "";
  if (!showAbout) return;

  const panel = createAboutPanel(
    {
      version: APP_VERSION,
      interval: getInterval(),
      updateStatus,
      donations,
    },
    (interval) => {
      setIntervalPref(interval);
      void checkForUpdates().then(renderAbout);
    },
    () => {
      showAbout = false;
      renderAbout();
    },
  );
  mount.appendChild(panel);
}

initTheme();
void loadDonations().then((d) => {
  donations = d;
  render();
});

const guardKey = getRestartGuardKey();
if (isRestartPending(guardKey)) {
  clearRestartGuard(guardKey);
} else {
  void checkForUpdates();
}

window.addEventListener("online", render);
window.addEventListener("offline", render);

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("/sw.js").catch(() => {});
  });
}
