import { homeNav, isRoute, normalizeStack } from "./nav";
import { type GpRoute, type NavState, PANEL_ROUTES } from "./types";

function isKind(value: unknown): value is NonNullable<NavState["feedbackKind"]> {
  return value === "bug" || value === "feature";
}

function panelScroll(scroll: NavState["scroll"]): NavState["scroll"] {
  const next: NavState["scroll"] = {};
  for (const route of PANEL_ROUTES) {
    const y = scroll[route];
    if (typeof y === "number" && Number.isFinite(y) && y >= 0) next[route] = Math.floor(y);
  }
  return next;
}

export function recordScroll(state: NavState, route: GpRoute, y: number): NavState {
  if (route === "home") return state;
  const n = Number.isFinite(y) ? Math.max(0, Math.floor(y)) : 0;
  return { ...state, scroll: { ...state.scroll, [route]: n } };
}

export function restoreScroll(state: NavState, route: GpRoute): number {
  const y = state.scroll[route];
  return typeof y === "number" && Number.isFinite(y) ? Math.max(0, y) : 0;
}

export function serialize(state: NavState): string {
  return JSON.stringify({
    stack: normalizeStack(state.stack),
    feedbackKind: state.feedbackKind ?? null,
    scroll: panelScroll(state.scroll),
    promptOpen: Boolean(state.promptOpen),
  });
}

export function deserialize(raw: string | null | undefined): NavState {
  if (!raw) return homeNav();
  try {
    const parsed = JSON.parse(raw) as Record<string, unknown>;
    if (typeof parsed !== "object" || parsed === null) return homeNav();
    const stack = normalizeStack(Array.isArray(parsed.stack) ? parsed.stack : []);
    const kind = isKind(parsed.feedbackKind) ? parsed.feedbackKind : undefined;
    const scrollRaw =
      parsed.scroll && typeof parsed.scroll === "object" && !Array.isArray(parsed.scroll)
        ? (parsed.scroll as Record<string, unknown>)
        : {};
    const scroll: NavState["scroll"] = {};
    for (const [key, value] of Object.entries(scrollRaw)) {
      if (isRoute(key) && key !== "home" && typeof value === "number" && Number.isFinite(value)) {
        scroll[key] = Math.max(0, Math.floor(value));
      }
    }
    return {
      stack,
      feedbackKind: currentKind(stack, kind),
      scroll,
      promptOpen: parsed.promptOpen === true,
    };
  } catch {
    return homeNav();
  }
}

function currentKind(stack: GpRoute[], kind: NavState["feedbackKind"]): NavState["feedbackKind"] {
  return stack[stack.length - 1] === "feedback" ? kind : undefined;
}
