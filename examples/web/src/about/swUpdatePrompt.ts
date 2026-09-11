/** Opt-in service-worker update prompt — never auto SKIP_WAITING. */

export const SW_UPDATE_PROMPT_TESTID = "sw-update-prompt";

export type SwUpdateListener = (waiting: boolean) => void;

export function hasWaitingWorker(
  registration: ServiceWorkerRegistration | null | undefined,
): boolean {
  return Boolean(registration?.waiting);
}

/** Wire updatefound / waiting so the UI can show Apply (opt-in). */
export function watchWaitingWorker(
  registration: ServiceWorkerRegistration,
  onChange: SwUpdateListener,
): () => void {
  const emit = () => onChange(hasWaitingWorker(registration));
  emit();
  const onUpdateFound = () => {
    const installing = registration.installing;
    if (!installing) return;
    installing.addEventListener("statechange", () => {
      if (installing.state === "installed") emit();
    });
  };
  registration.addEventListener("updatefound", onUpdateFound);
  return () => registration.removeEventListener("updatefound", onUpdateFound);
}

export function createSwUpdatePrompt(onApply: () => void, onDismiss: () => void): HTMLElement {
  const dialog = document.createElement("div");
  dialog.role = "dialog";
  dialog.setAttribute("aria-modal", "true");
  dialog.setAttribute("aria-label", "Offline update ready");
  dialog.dataset.testid = SW_UPDATE_PROMPT_TESTID;
  dialog.className = "gp-sw-update-prompt";
  const body = document.createElement("p");
  body.textContent = "A newer offline shell is ready. Apply when you want.";
  const apply = document.createElement("button");
  apply.type = "button";
  apply.dataset.testid = "sw-update-apply";
  apply.textContent = "Apply update";
  apply.addEventListener("click", onApply);
  const later = document.createElement("button");
  later.type = "button";
  later.dataset.testid = "sw-update-later";
  later.textContent = "Later";
  later.addEventListener("click", onDismiss);
  dialog.append(body, apply, later);
  return dialog;
}
