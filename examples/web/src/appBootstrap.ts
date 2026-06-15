import { handleRestartGuard, checkForUpdates } from "./about/aboutSession";
import { loadDonations } from "./about/donations";
import { createAppShell, type AppShellState } from "./AppShell";
import { t } from "./i18n";
import { initTheme, subscribeThemeChange } from "./theme";

export function bootstrapApp(appRoot: HTMLDivElement): void {
  let state: AppShellState = {
    showAbout: false,
    showSettings: false,
    updateStatus: t("about.update.current"),
    donations: { enabled: false, message: "", links: [] },
  };

  function render(): void {
    createAppShell(appRoot, state, {
      onState: (patch) => {
        state = { ...state, ...patch };
        render();
      },
      onUpdateCheckChange: (enabled) => {
        if (enabled) {
          void checkForUpdates().then((status) => {
            state = { ...state, updateStatus: status };
            render();
          });
        }
      },
    });
  }

  initTheme();
  subscribeThemeChange(() => render());
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
}
