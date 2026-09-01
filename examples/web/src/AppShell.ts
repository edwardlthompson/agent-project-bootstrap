import { APP_VERSION } from "./about/aboutSession";
import { createLaunchPromptDialog } from "./about/launchPrompt";
import type { LaunchPrompt } from "./about/runAppUpdates";
import type { DonationConfig } from "./about/types";
import { createAboutPanel } from "./components/AboutPanel";
import { createFeedbackPanel } from "./components/FeedbackPanel";
import { createSettingsPanel } from "./components/SettingsPanel";
import { createThemeToggle } from "./components/ThemeToggle";
import { isOnline } from "./greet";
import { t } from "./i18n";
import { applyPanelScroll, current, type FeedbackKind, type GpRoute, type NavState } from "./nav";
import { bindPanelDialog } from "./panelDialog";

let dialogCleanup: (() => void) | undefined;

export type AppShellState = {
  nav: NavState;
  feedbackPrefill?: string;
  updateStatus: string;
  donations: DonationConfig;
  launchPrompt: LaunchPrompt | null;
  releaseRepo?: string;
};

export type AppShellCallbacks = {
  onState: (next: Partial<AppShellState>) => void;
  onPushRoute: (route: GpRoute, kind?: FeedbackKind) => void;
  onPop: () => void;
  onApplyUpdate?: () => void;
  onDonate?: () => void;
  onLaunchPrompt?: (accepted: boolean) => void;
  canApplyUpdate?: boolean;
};

export function createAppShell(
  root: HTMLElement,
  state: AppShellState,
  callbacks: AppShellCallbacks,
): void {
  const online = isOnline();
  const statusKey = online ? "app.status.online" : "app.status.offline";
  const donateEnabled = state.donations.enabled && state.donations.links.length > 0;
  const route = current(state.nav);

  root.innerHTML = `
    <main>
      <div class="gp-header">
        <h1 class="gp-title">${t("app.title")}</h1>
        <div class="gp-header-actions">
          ${
            donateEnabled
              ? `<button type="button" class="gp-donate-btn" data-donate-open>${t("about.donate")}</button>`
              : ""
          }
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

  root.querySelector("[data-donate-open]")?.addEventListener("click", () => {
    callbacks.onDonate?.();
  });

  root.querySelector("[data-about-open]")?.addEventListener("click", () => {
    toggleOrPush(route, "about", callbacks);
  });

  root.querySelector("[data-settings-open]")?.addEventListener("click", () => {
    toggleOrPush(route, "settings", callbacks);
  });

  const mount = root.querySelector("[data-panel-mount]");
  if (!mount) return;

  dialogCleanup?.();
  dialogCleanup = undefined;
  mount.innerHTML = "";

  if (state.nav.promptOpen && state.launchPrompt) {
    const promptDialog = createLaunchPromptDialog(state.launchPrompt, (accepted) => {
      callbacks.onLaunchPrompt?.(accepted);
    });
    mount.appendChild(promptDialog);
    return;
  }

  if (route === "feedback") {
    const panel = createFeedbackPanel(state.nav.feedbackKind ?? "bug", {
      onClose: callbacks.onPop,
      releaseRepo: state.releaseRepo ?? "",
      description: state.feedbackPrefill,
    });
    mount.appendChild(panel);
    dialogCleanup = bindPanelDialog(panel, callbacks.onPop);
    applyPanelScroll(root, state.nav);
    return;
  }

  if (route === "settings") {
    const panel = createSettingsPanel({ onClose: callbacks.onPop });
    mount.appendChild(panel);
    dialogCleanup = bindPanelDialog(panel, callbacks.onPop);
    applyPanelScroll(root, state.nav);
    return;
  }

  if (route !== "about") return;

  mount.appendChild(
    createAboutPanel(
      {
        version: APP_VERSION,
        updateStatus: state.updateStatus,
        donations: state.donations,
        canApplyUpdate: callbacks.canApplyUpdate,
      },
      callbacks.onPop,
      callbacks.onApplyUpdate,
      () => callbacks.onPushRoute("feedback", "bug"),
      () => callbacks.onPushRoute("feedback", "feature"),
    ),
  );
  const aboutPanel = mount.lastElementChild as HTMLElement;
  dialogCleanup = bindPanelDialog(aboutPanel, callbacks.onPop);
  applyPanelScroll(root, state.nav);
}

function toggleOrPush(route: GpRoute, target: GpRoute, callbacks: AppShellCallbacks): void {
  if (route === target) callbacks.onPop();
  else callbacks.onPushRoute(target);
}
