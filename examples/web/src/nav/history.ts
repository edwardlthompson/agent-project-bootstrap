/** Golden Path History API sentinel. In-app Close uses history.back(); popstate pops NavState. */

export const NAV_STORAGE_KEY = "gp.nav.v1";

export type GpHistoryState = { gp: true; depth: number };

export function gpState(depth: number): GpHistoryState {
  const n = Number.isFinite(depth) ? Math.max(0, Math.floor(depth)) : 0;
  return { gp: true, depth: n };
}

export function isGpHistoryState(state: unknown): state is GpHistoryState {
  if (typeof state !== "object" || state === null) return false;
  const rec = state as { gp?: unknown; depth?: unknown };
  return rec.gp === true && typeof rec.depth === "number" && Number.isFinite(rec.depth);
}

export function ensureHomeSentinel(history: Pick<History, "state" | "replaceState">): void {
  if (!isGpHistoryState(history.state)) {
    history.replaceState(gpState(0), "");
  }
}

export function pushPanelHistory(history: Pick<History, "pushState">, depth: number): void {
  history.pushState(gpState(depth), "");
}

export function trapHomeHistory(history: Pick<History, "pushState">): void {
  history.pushState(gpState(0), "");
}
