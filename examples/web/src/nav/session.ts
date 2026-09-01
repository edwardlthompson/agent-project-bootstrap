import { ensureHomeSentinel, NAV_STORAGE_KEY, pushPanelHistory } from "./history";
import { canPop, current, homeNav, normalizeStack, pop, push } from "./nav";
import { deserialize, recordScroll, restoreScroll, serialize } from "./persist";
import type { FeedbackKind, NavState } from "./types";

export function historyDepth(nav: NavState): number {
  const extra = nav.promptOpen ? 1 : 0;
  return Math.max(0, normalizeStack(nav.stack).length - 1 + extra);
}

export function loadNav(storage: Pick<Storage, "getItem"> = localStorage): NavState {
  try {
    const loaded = deserialize(storage.getItem(NAV_STORAGE_KEY));
    return { ...loaded, promptOpen: false };
  } catch {
    return homeNav();
  }
}

export function saveNav(nav: NavState, storage: Pick<Storage, "setItem"> = localStorage): void {
  storage.setItem(NAV_STORAGE_KEY, serialize(nav));
}

export function applyFeedbackIntents(
  nav: NavState,
  intent: { crash: boolean; share: string },
): { nav: NavState; prefill?: string } {
  let next = nav;
  if (intent.crash) {
    next = { ...push(next, "feedback", "bug"), feedbackKind: "bug" };
  }
  if (intent.share) {
    next = { ...push(next, "feedback", "feature"), feedbackKind: "feature" as FeedbackKind };
    return { nav: next, prefill: intent.share };
  }
  return { nav: next };
}

export function syncHistoryToNav(
  history: Pick<History, "state" | "replaceState" | "pushState">,
  nav: NavState,
): void {
  ensureHomeSentinel(history);
  const want = historyDepth(nav);
  const have = isFiniteDepth(history.state);
  for (let depth = have + 1; depth <= want; depth += 1) {
    pushPanelHistory(history, depth);
  }
}

function isFiniteDepth(state: unknown): number {
  if (typeof state !== "object" || state === null) return 0;
  const depth = (state as { depth?: unknown }).depth;
  return typeof depth === "number" && Number.isFinite(depth) ? Math.max(0, Math.floor(depth)) : 0;
}

export function applyPop(nav: NavState, scrollY: number): { nav: NavState; trapHome: boolean } {
  const next = pop(recordScroll(nav, current(nav), scrollY));
  return { nav: next, trapHome: !canPop(next) && !next.promptOpen };
}

export function readPanelScroll(root: ParentNode): number {
  const el = root.querySelector<HTMLElement>(
    "[data-testid='settings-panel'], [data-testid='about-panel'], [data-testid='feedback-panel'], .gp-launch-dialog",
  );
  return el?.scrollTop ?? 0;
}

export function applyPanelScroll(root: ParentNode, nav: NavState): void {
  const route = current(nav);
  const el = root.querySelector<HTMLElement>(`[data-testid="${route}-panel"]`);
  if (el) el.scrollTop = restoreScroll(nav, route);
}
