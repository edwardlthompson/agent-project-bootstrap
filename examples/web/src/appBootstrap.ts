import { type AppShellState, createAppShell } from "./AppShell";
import {
  APP_VERSION,
  assetPrefixOf,
  handleRestartGuard,
  loadAppUpdateConfig,
} from "./about/aboutSession";
import { applyPwaUpdate } from "./about/applyUpdate";
import { loadDonations, primaryDonateUrl } from "./about/donations";
import { decideLaunchPrompt, type LaunchPrompt } from "./about/runAppUpdates";
import { markUpdateChecked, markVersionSeen } from "./about/updatePrefs";
import { assetUrl } from "./assetUrl";
import { installCrashHandler } from "./crash-capture/installHandler";
import { readPendingCrash } from "./crash-capture/pendingCrash";
import { getSaveCrashes } from "./feedback/saveCrashes";
import { t } from "./i18n";
import {
  applyFeedbackIntents,
  createHistoryNav,
  feedbackPrefillOf,
  loadNav,
  syncHistoryToNav,
} from "./nav";
import { shareTargetDescription } from "./share-target";
import { initTheme, subscribeThemeChange } from "./theme";

let popAbort: AbortController | undefined;

export function bootstrapApp(appRoot: HTMLDivElement): void {
  popAbort?.abort();
  popAbort = new AbortController();
  initTheme();
  installCrashHandler(() => getSaveCrashes());
  const shared = shareTargetDescription(new URLSearchParams(window.location.search));
  const intent = applyFeedbackIntents(loadNav(), {
    crash: Boolean(readPendingCrash()),
    share: shared,
  });
  syncHistoryToNav(history, intent.nav);
  const navCtl = createHistoryNav(history, intent.nav);

  let state: AppShellState = {
    nav: intent.nav,
    feedbackPrefill: intent.prefill,
    updateStatus: t("about.update.current"),
    donations: { enabled: false, message: "", links: [] },
    launchPrompt: null,
  };

  function applyNav(next: typeof intent.nav): void {
    state = { ...state, nav: next, feedbackPrefill: feedbackPrefillOf(next, state.feedbackPrefill) };
    render();
  }

  function render(): void {
    createAppShell(appRoot, state, {
      onState: (patch) => {
        state = { ...state, ...patch };
        render();
      },
      onPushRoute: (route, kind) => {
        const next = navCtl.pushRoute(route, kind);
        if (next) applyNav(next);
      },
      onPop: () => navCtl.popFromUi(),
      onApplyUpdate: () => {
        void handleApplyUpdate();
      },
      onDonate: openDonate,
      onLaunchPrompt: handleLaunchPrompt,
      canApplyUpdate: false,
    });
  }

  async function handleApplyUpdate(): Promise<void> {
    if (!("serviceWorker" in navigator)) return;
    const registration = await navigator.serviceWorker.getRegistration();
    if (!registration) return;
    const applied = await applyPwaUpdate(registration);
    if (applied) {
      state = { ...state, updateStatus: t("about.update.restarting") };
      render();
    }
  }

  function openDonate(): void {
    window.open(primaryDonateUrl(state.donations), "_blank", "noopener,noreferrer");
  }

  function handleLaunchPrompt(accepted: boolean): void {
    const prompt = state.launchPrompt;
    if (!prompt) return;
    if (prompt.kind === "donate") {
      markVersionSeen(APP_VERSION);
      if (accepted) openDonate();
    } else {
      markUpdateChecked(Date.now(), prompt.version);
      if (accepted) window.open(prompt.url, "_blank", "noopener,noreferrer");
    }
    navCtl.popFromUi();
  }

  subscribeThemeChange(() => render());
  window.addEventListener(
    "popstate",
    () => {
      const result = navCtl.onPopState(appRoot);
      state = {
        ...state,
        nav: result.nav,
        launchPrompt: result.nav.promptOpen ? state.launchPrompt : null,
        feedbackPrefill: feedbackPrefillOf(result.nav, state.feedbackPrefill),
      };
      render();
    },
    { signal: popAbort.signal },
  );

  render();
  void loadDonations().then((d) => {
    state = { ...state, donations: d };
    render();
  });

  if (!handleRestartGuard()) {
    void (async () => {
      const config = await loadAppUpdateConfig();
      const prompt: LaunchPrompt | null = await decideLaunchPrompt({
        currentVersion: APP_VERSION,
        kind: "exe",
        prefix: assetPrefixOf(config),
        releaseRepo: config?.release_repo ?? "",
        userAgent: `GoldenPath/${APP_VERSION}`,
      });
      state = { ...state, releaseRepo: config?.release_repo ?? "" };
      if (!prompt) return;
      state = { ...state, launchPrompt: prompt, nav: navCtl.openPrompt() };
      render();
    })();
  }

  window.addEventListener("online", render);
  window.addEventListener("offline", render);

  if ("serviceWorker" in navigator) {
    window.addEventListener("load", () => {
      navigator.serviceWorker.register(assetUrl("sw.js")).catch(() => {});
    });
  }
}
