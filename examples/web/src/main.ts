import "./style.css";
// Feature wiring: keep ≤10 lines per feature in this composition root (see docs/FEATURE_MODULES.md).
import { APP_VERSION, checkForUpdates, getInterval, handleRestartGuard, setIntervalPref } from "./about/aboutSession";
import { loadDonations } from "./about/donations";
import { createAboutPanel } from "./components/AboutPanel";
import { createThemeToggle } from "./components/ThemeToggle";
import { isOnline } from "./greet";
import { t } from "./i18n";
import { initTheme } from "./theme";

const app = document.querySelector<HTMLDivElement>("#app");
if (!app) {
  throw new Error("App root element not found");
}
const root = app;

let showAbout = false;
let updateStatus = t("about.update.current");
let donations = { enabled: false, message: "", links: [] as { label: string; url: string }[] };

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

  const actions = root.querySelector<HTMLDivElement>(".gp-header-actions");
  if (actions) {
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
      void checkForUpdates().then((status) => {
        updateStatus = status;
        renderAbout();
      });
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

if (!handleRestartGuard()) {
  void checkForUpdates().then((status) => {
    updateStatus = status;
    if (showAbout) renderAbout();
  });
}

window.addEventListener("online", render);
window.addEventListener("offline", render);

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("/sw.js").catch(() => {});
  });
}
