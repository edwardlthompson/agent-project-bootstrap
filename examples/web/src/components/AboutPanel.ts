import { t } from "../i18n";
import type { CheckInterval, DonationConfig } from "../about/types";

export interface AboutPanelState {
  version: string;
  interval: CheckInterval;
  updateStatus: string;
  donations: DonationConfig;
}

export function createAboutPanel(
  state: AboutPanelState,
  onIntervalChange: (interval: CheckInterval) => void,
  onClose: () => void,
): HTMLElement {
  const panel = document.createElement("section");
  panel.className = "gp-about-panel";
  panel.setAttribute("aria-label", t("about.title"));

  const donationsHtml =
    state.donations.enabled && state.donations.links.length > 0
      ? `<p class="gp-about-donate-msg">${state.donations.message}</p>
         <ul class="gp-about-donate-links">
           ${state.donations.links
             .map(
               (l) =>
                 `<li><a href="${l.url}" target="_blank" rel="noopener noreferrer">${l.label}</a></li>`,
             )
             .join("")}
         </ul>`
      : "";

  panel.innerHTML = `
    <header class="gp-about-header">
      <h2>${t("about.title")}</h2>
      <button type="button" class="gp-about-close" aria-label="${t("about.close")}">×</button>
    </header>
    <p>${t("about.version")}: <strong>${state.version}</strong></p>
    <p>${t("about.format")}: <code>pwa</code></p>
    <label class="gp-about-interval">
      <span>${t("about.update.interval.label")}</span>
      <select data-about-interval>
        <option value="off">${t("about.update.interval.off")}</option>
        <option value="daily">${t("about.update.interval.daily")}</option>
        <option value="weekly">${t("about.update.interval.weekly")}</option>
        <option value="monthly">${t("about.update.interval.monthly")}</option>
        <option value="on_session">${t("about.update.interval.on_session")}</option>
      </select>
    </label>
    <p class="gp-about-status" data-testid="about-status">${state.updateStatus}</p>
    ${donationsHtml}
  `;

  const select = panel.querySelector<HTMLSelectElement>("[data-about-interval]");
  if (select) {
    select.value = state.interval;
    select.addEventListener("change", () => {
      onIntervalChange(select.value as CheckInterval);
    });
  }

  panel.querySelector(".gp-about-close")?.addEventListener("click", onClose);
  return panel;
}
