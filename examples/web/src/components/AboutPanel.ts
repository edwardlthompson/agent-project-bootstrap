import type { DonationConfig } from "../about/types";
import { t } from "../i18n";

export interface AboutPanelState {
  version: string;
  updateStatus: string;
  donations: DonationConfig;
  canApplyUpdate?: boolean;
}

export function createAboutPanel(
  state: AboutPanelState,
  onClose: () => void,
  onApplyUpdate?: () => void,
  onReportBug?: () => void,
  onRequestFeature?: () => void,
): HTMLElement {
  const panel = document.createElement("section");
  panel.className = "gp-about-panel";
  panel.setAttribute("aria-label", t("about.title"));
  panel.dataset.testid = "about-panel";

  const header = document.createElement("header");
  header.className = "gp-about-header";
  const title = document.createElement("h2");
  title.textContent = t("about.title");
  const closeBtn = document.createElement("button");
  closeBtn.type = "button";
  closeBtn.className = "gp-about-close";
  closeBtn.setAttribute("aria-label", t("about.close"));
  closeBtn.textContent = "×";
  closeBtn.addEventListener("click", onClose);
  header.append(title, closeBtn);
  panel.append(header);

  const appGroup = document.createElement("section");
  appGroup.className = "gp-about-group";
  const appHeading = document.createElement("h3");
  appHeading.textContent = t("about.section.app");
  appGroup.append(appHeading, metaLine(t("about.version"), state.version, true), metaLine(t("about.format"), "pwa", false));
  const statusP = document.createElement("p");
  statusP.className = "gp-about-status";
  statusP.dataset.testid = "about-status";
  statusP.setAttribute("aria-live", "polite");
  statusP.textContent = state.updateStatus;
  appGroup.append(statusP);
  if (state.canApplyUpdate && onApplyUpdate) {
    const applyBtn = document.createElement("button");
    applyBtn.type = "button";
    applyBtn.className = "gp-about-apply";
    applyBtn.dataset.testid = "about-apply";
    applyBtn.textContent = t("about.update.apply");
    applyBtn.addEventListener("click", onApplyUpdate);
    appGroup.append(applyBtn);
  }
  panel.append(appGroup);

  if (state.donations.enabled && state.donations.links.length > 0) {
    panel.append(supportGroup(state.donations));
  }
  if (onReportBug || onRequestFeature) {
    panel.append(feedbackGroup(onReportBug, onRequestFeature));
  }
  return panel;
}

function metaLine(label: string, value: string, strong: boolean): HTMLParagraphElement {
  const p = document.createElement("p");
  p.append(`${label}: `);
  if (strong) {
    const el = document.createElement("strong");
    el.textContent = value;
    p.append(el);
  } else {
    const el = document.createElement("code");
    el.textContent = value;
    p.append(el);
  }
  return p;
}

function supportGroup(donations: DonationConfig): HTMLElement {
  const group = document.createElement("section");
  group.className = "gp-about-group";
  const heading = document.createElement("h3");
  heading.textContent = t("about.section.support");
  const donateHeading = document.createElement("h4");
  donateHeading.className = "gp-about-donate-heading";
  donateHeading.dataset.testid = "about-donations-heading";
  donateHeading.textContent = t("about.donations.heading");
  const donateMsg = document.createElement("p");
  donateMsg.className = "gp-about-donate-msg";
  donateMsg.textContent = donations.message;
  const donateList = document.createElement("ul");
  donateList.className = "gp-about-donate-links";
  donateList.dataset.testid = "about-donation-links";
  for (const link of donations.links) {
    const item = document.createElement("li");
    const anchor = document.createElement("a");
    anchor.href = link.url;
    anchor.target = "_blank";
    anchor.rel = "noopener noreferrer";
    anchor.dataset.testid = "about-donation-link";
    anchor.textContent = link.label;
    item.append(anchor);
    donateList.append(item);
  }
  group.append(heading, donateHeading, donateMsg, donateList);
  return group;
}

function feedbackGroup(onReportBug?: () => void, onRequestFeature?: () => void): HTMLElement {
  const group = document.createElement("section");
  group.className = "gp-about-group";
  const heading = document.createElement("h3");
  heading.textContent = t("about.section.feedback");
  const row = document.createElement("label");
  row.className = "gp-settings-row";
  const label = document.createElement("span");
  label.textContent = t("about.feedback.label");
  const select = document.createElement("select");
  select.dataset.aboutFeedback = "true";
  select.dataset.testid = "about-feedback";
  select.setAttribute("aria-label", t("about.feedback.label"));
  const placeholder = document.createElement("option");
  placeholder.value = "";
  placeholder.textContent = t("about.feedback.choose");
  select.append(placeholder);
  if (onReportBug) {
    const bug = document.createElement("option");
    bug.value = "bug";
    bug.dataset.testid = "about-report-bug";
    bug.textContent = t("feedback.bug.title");
    select.append(bug);
  }
  if (onRequestFeature) {
    const feat = document.createElement("option");
    feat.value = "feature";
    feat.dataset.testid = "about-request-feature";
    feat.textContent = t("feedback.feature.title");
    select.append(feat);
  }
  select.addEventListener("change", () => {
    if (select.value === "bug") onReportBug?.();
    if (select.value === "feature") onRequestFeature?.();
    select.value = "";
  });
  row.append(label, select);
  group.append(heading, row);
  return group;
}
