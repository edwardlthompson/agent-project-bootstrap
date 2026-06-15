import { APP_VERSION } from "./about/aboutSession";
import type { DonationConfig } from "./about/types";
import { createAboutPanel } from "./components/AboutPanel";
import { createSettingsPanel } from "./components/SettingsPanel";
import { createThemeToggle } from "./components/ThemeToggle";
import { isOnline } from "./greet";
import { t } from "./i18n";

export type AppShellState = {
  showAbout: boolean;
  showSettings: boolean;
  updateStatus: string;
  donations: DonationConfig;
};

export type AppShellCallbacks = {
  onState: (next: Partial<AppShellState>) => void;
  onUpdateCheckChange?: (enabled: boolean) => void;
};

export function createAppShell(
  root: HTMLElement,
  state: AppShellState,
  callbacks: AppShellCallbacks,
): void {
  const online = isOnline();
  const statusKey = online ? "app.status.online" : "app.status.offline";

  root.innerHTML = `
    <main>
      <div class="gp-header">
        <h1 class="gp-title">${t("app.title")}</h1>
        <div class="gp-header-actions">
          <button type="button" class="gp-settings-btn" data-settings-open aria-label="${t("settings.open")}">⚙</button>
          <button type="button" class="gp-about-btn" data-about-open aria-label="${t("about.open")}">i</button>
        </div>
      </div>
      <p class="gp-headline">${t("app.greeting")}</p>
      <p class="gp-body" data-testid="status">${t(statusKey)}</p>
      <div data-panel-mount></div>
    </main>
  `;

  const actions = root.querySelector<HTMLDivElement>(".gp-header-actions");
  if (actions) {
    actions.insertBefore(createThemeToggle(), actions.firstChild);
  }

  root.querySelector("[data-about-open]")?.addEventListener("click", () => {
    callbacks.onState({ showAbout: !state.showAbout, showSettings: false });
  });

  root.querySelector("[data-settings-open]")?.addEventListener("click", () => {
    callbacks.onState({ showSettings: !state.showSettings, showAbout: false });
  });

  const mount = root.querySelector("[data-panel-mount]");
  if (!mount) return;
  mount.innerHTML = "";

  if (state.showSettings) {
    mount.appendChild(
      createSettingsPanel({
        onClose: () => callbacks.onState({ showSettings: false }),
        onUpdateCheckChange: callbacks.onUpdateCheckChange,
      }),
    );
    return;
  }

  if (!state.showAbout) return;

  mount.appendChild(
    createAboutPanel(
      {
        version: APP_VERSION,
        updateStatus: state.updateStatus,
        donations: state.donations,
      },
      () => callbacks.onState({ showAbout: false }),
    ),
  );
}
