import { t } from "../i18n";
import type { DonationConfig } from "../about/types";

export interface AboutPanelState {
  version: string;
  updateStatus: string;
  donations: DonationConfig;
}

export function createAboutPanel(
  state: AboutPanelState,
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
    <p class="gp-about-status" data-testid="about-status">${state.updateStatus}</p>
    ${donationsHtml}
  `;

  panel.querySelector(".gp-about-close")?.addEventListener("click", onClose);
  return panel;
}
