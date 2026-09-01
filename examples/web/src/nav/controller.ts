import { current, push, setPrompt, type FeedbackKind, type GpRoute, type NavState } from "./nav";
import { pushPanelHistory, trapHomeHistory } from "./history";
import { applyPop, historyDepth, readPanelScroll, saveNav } from "./session";

export type HistoryNav = {
  get: () => NavState;
  pushRoute: (route: GpRoute, kind?: FeedbackKind) => NavState | null;
  popFromUi: () => void;
  openPrompt: () => NavState;
  onPopState: (root: ParentNode) => { nav: NavState; trapHome: boolean };
};

export function createHistoryNav(
  historyRef: Pick<History, "back" | "pushState">,
  initial: NavState,
): HistoryNav {
  let nav = initial;
  return {
    get: () => nav,
    pushRoute(route, kind) {
      if (current(nav) === route) {
        historyRef.back();
        return null;
      }
      nav = push(nav, route, kind);
      saveNav(nav);
      pushPanelHistory(historyRef, historyDepth(nav));
      return nav;
    },
    popFromUi: () => historyRef.back(),
    openPrompt() {
      nav = setPrompt(nav, true);
      saveNav(nav);
      pushPanelHistory(historyRef, historyDepth(nav));
      return nav;
    },
    onPopState(root) {
      const result = applyPop(nav, readPanelScroll(root));
      nav = result.nav;
      saveNav(nav);
      if (result.trapHome) trapHomeHistory(historyRef);
      return result;
    },
  };
}

export function feedbackPrefillOf(nav: NavState, prefill: string | undefined): string | undefined {
  return current(nav) === "feedback" ? prefill : undefined;
}
