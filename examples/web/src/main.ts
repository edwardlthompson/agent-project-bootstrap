import "./style.css";
import { handleRestartGuard, checkForUpdates } from "./about/aboutSession";
import { loadDonations } from "./about/donations";
import { createAppShell, type AppShellState } from "./AppShell";
import { t } from "./i18n";
import { initTheme } from "./theme";

const rootEl = document.querySelector<HTMLDivElement>("#app");
if (!rootEl) throw new Error("App root element not found");

let state: AppShellState = {
  showAbout: false,
  updateStatus: t("about.update.current"),
  donations: { enabled: false, message: "", links: [] },
};

function render(): void {
  createAppShell(rootEl, state, (patch) => {
    state = { ...state, ...patch };
    render();
  });
}

initTheme();
void loadDonations().then((d) => {
  state = { ...state, donations: d };
  render();
});

if (!handleRestartGuard()) {
  void checkForUpdates().then((status) => {
    state = { ...state, updateStatus: status };
    if (state.showAbout) render();
  });
}

window.addEventListener("online", render);
window.addEventListener("offline", render);

if ("serviceWorker" in navigator) {
  window.addEventListener("load", () => {
    navigator.serviceWorker.register("/sw.js").catch(() => {});
  });
}
