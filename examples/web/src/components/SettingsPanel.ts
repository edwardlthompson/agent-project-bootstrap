import { onSaveCrashesChanged } from "../crash-capture/pendingCrash";
import { getSaveCrashes, setSaveCrashes } from "../feedback/saveCrashes";
import { t } from "../i18n";
import { applySettingsBundle, parseSettings, snapshotSettings } from "../settings/export";
import { applySettingsThemeMode, getSettingsThemeMode } from "../settings/preferences";
import type { ThemeMode } from "../theme";

export type SettingsPanelCallbacks = {
  onClose: () => void;
  onOpenAbout?: () => void;
};

export function createSettingsPanel(callbacks: SettingsPanelCallbacks): HTMLElement {
  const panel = document.createElement("section");
  panel.className = "gp-settings-panel";
  panel.setAttribute("aria-label", t("settings.title"));
  panel.dataset.testid = "settings-panel";

  const themeMode = getSettingsThemeMode();

  panel.innerHTML = `
    <header class="gp-settings-header">
      <h2>${t("settings.title")}</h2>
      <button type="button" class="gp-settings-close" aria-label="${t("settings.close")}">×</button>
    </header>
    <section class="gp-settings-group">
      <h3>${t("settings.section.appearance")}</h3>
      <label class="gp-settings-row">
        <span>${t("settings.theme.label")}</span>
        <select data-settings-theme>
          <option value="system">${t("settings.theme.mode.system")}</option>
          <option value="light">${t("settings.theme.mode.light")}</option>
          <option value="dark">${t("settings.theme.mode.dark")}</option>
        </select>
      </label>
    </section>
    <section class="gp-settings-group">
      <h3>${t("settings.section.privacy")}</h3>
      <label class="gp-settings-row">
        <span>${t("settings.feedback.save_crashes")}</span>
        <input type="checkbox" data-save-crashes />
      </label>
    </section>
    <section class="gp-settings-group">
      <h3>${t("settings.section.data")}</h3>
      <div class="gp-settings-row gp-settings-actions">
        <button type="button" data-settings-export>${t("settings.export")}</button>
        <button type="button" data-settings-import>${t("settings.import")}</button>
        <input type="file" accept="application/json" hidden data-settings-import-file />
      </div>
    </section>
    <section class="gp-settings-group">
      <h3>${t("settings.section.about")}</h3>
      <button type="button" class="gp-settings-nav" data-settings-about aria-label="${t("settings.about")}">
        <span>${t("settings.about")}</span>
        <span class="gp-settings-hint">${t("settings.about_hint")}</span>
      </button>
    </section>
  `;

  const themeSelect = panel.querySelector<HTMLSelectElement>("[data-settings-theme]");
  if (themeSelect) {
    themeSelect.value = themeMode;
    themeSelect.addEventListener("change", () => {
      applySettingsThemeMode(themeSelect.value as ThemeMode);
    });
  }

  const save = panel.querySelector<HTMLInputElement>("[data-save-crashes]");
  if (save) {
    save.checked = getSaveCrashes();
    save.addEventListener("change", () => {
      setSaveCrashes(save.checked);
      onSaveCrashesChanged(save.checked);
    });
  }

  panel.querySelector(".gp-settings-close")?.addEventListener("click", callbacks.onClose);
  panel.querySelector("[data-settings-about]")?.addEventListener("click", () => {
    callbacks.onOpenAbout?.();
  });

  const fileInput = panel.querySelector<HTMLInputElement>("[data-settings-import-file]");
  panel.querySelector("[data-settings-export]")?.addEventListener("click", () => {
    const blob = new Blob([JSON.stringify(snapshotSettings(), null, 2)], {
      type: "application/json",
    });
    const url = URL.createObjectURL(blob);
    const link = document.createElement("a");
    link.href = url;
    link.download = "golden-path-settings.json";
    link.click();
    URL.revokeObjectURL(url);
  });
  panel.querySelector("[data-settings-import]")?.addEventListener("click", () => {
    fileInput?.click();
  });
  fileInput?.addEventListener("change", () => {
    const file = fileInput.files?.[0];
    if (!file) return;
    void file.text().then((raw) => {
      const bundle = parseSettings(raw);
      if (bundle) applySettingsBundle(bundle);
    });
  });
  return panel;
}
