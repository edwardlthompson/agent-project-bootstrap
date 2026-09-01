import type { FeedbackKind, GpRoute, NavState } from "./types";

export function homeNav(): NavState {
  return { stack: ["home"], scroll: {}, promptOpen: false };
}

export function isRoute(value: unknown): value is GpRoute {
  return value === "home" || value === "settings" || value === "about" || value === "feedback";
}

export function normalizeStack(raw: readonly unknown[]): GpRoute[] {
  const out: GpRoute[] = [];
  for (const item of raw) {
    if (!isRoute(item)) continue;
    if (out.length === 0 && item !== "home") out.push("home");
    if (out[out.length - 1] === item) continue;
    out.push(item);
  }
  if (out.length === 0) return ["home"];
  if (out[0] !== "home") return ["home", ...out];
  return out;
}

export function current(state: NavState): GpRoute {
  const stack = normalizeStack(state.stack);
  return stack[stack.length - 1] ?? "home";
}

export function isHome(state: NavState): boolean {
  return current(state) === "home" && normalizeStack(state.stack).length <= 1;
}

export function canPop(state: NavState): boolean {
  return !isHome(state);
}

export function setPrompt(state: NavState, open: boolean): NavState {
  if (state.promptOpen === open) return state;
  return { ...state, promptOpen: open };
}

export function push(state: NavState, route: GpRoute, kind?: FeedbackKind): NavState {
  if (route === "home") {
    if (isHome(state) && state.feedbackKind === undefined) return state;
    return { ...state, stack: ["home"], feedbackKind: undefined };
  }
  if (current(state) === route) return state;
  return {
    ...state,
    stack: [...normalizeStack(state.stack), route],
    feedbackKind: route === "feedback" ? (kind ?? "bug") : undefined,
  };
}

export function pop(state: NavState): NavState {
  if (state.promptOpen) return { ...state, promptOpen: false };
  if (!canPop(state)) return state;
  const stack = normalizeStack(state.stack).slice(0, -1);
  const next = stack.length === 0 ? ["home"] : stack;
  const top = next[next.length - 1] ?? "home";
  return {
    ...state,
    stack: next,
    feedbackKind: top === "feedback" ? state.feedbackKind : undefined,
  };
}
