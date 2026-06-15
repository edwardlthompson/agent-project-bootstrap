import { APP_VERSION, checkForUpdates, getInterval, setIntervalPref } from "./about/aboutSession";
import type { DonationConfig } from "./about/types";
import { createAboutPanel } from "./components/AboutPanel";
import { createThemeToggle } from "./components/ThemeToggle";
import { isOnline } from "./greet";
import { t } from "./i18n";

export type AppShellState = {
  showAbout: boolean;
  updateStatus: string;
  donations: DonationConfig;
};

export function createAppShell(root: HTMLElement, state: AppShellState, onState: (next: Partial<AppShellState>) => void): void {
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
    onState({ showAbout: !state.showAbout });
  });

  const mount = root.querySelector("[data-about-mount]");
  if (!mount) return;
  mount.innerHTML = "";
  if (!state.showAbout) return;

  const panel = createAboutPanel(
    {
      version: APP_VERSION,
      interval: getInterval(),
      updateStatus: state.updateStatus,
      donations: state.donations,
    },
    (interval) => {
      setIntervalPref(interval);
      void checkForUpdates().then((status) => onState({ updateStatus: status }));
    },
    () => onState({ showAbout: false }),
  );
  mount.appendChild(panel);
}
