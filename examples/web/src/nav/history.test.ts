import { describe, expect, it } from "vitest";
import {
  ensureHomeSentinel,
  gpState,
  isGpHistoryState,
  pushPanelHistory,
  trapHomeHistory,
} from "./history";

describe("gp history sentinel", () => {
  it("accepts only { gp: true, depth: number }", () => {
    expect(isGpHistoryState({ gp: true, depth: 0 })).toBe(true);
    expect(isGpHistoryState({ gp: true, depth: 2 })).toBe(true);
    expect(isGpHistoryState({ gp: true })).toBe(false);
    expect(isGpHistoryState({ gp: false, depth: 0 })).toBe(false);
    expect(isGpHistoryState(null)).toBe(false);
    expect(isGpHistoryState(undefined)).toBe(false);
    expect(gpState(Number.NaN)).toEqual({ gp: true, depth: 0 });
    expect(gpState(-2.8)).toEqual({ gp: true, depth: 0 });
  });

  it("replaceState when the current entry is not our sentinel", () => {
    const calls: unknown[] = [];
    const fake = {
      state: null as unknown,
      replaceState(state: unknown) {
        this.state = state;
        calls.push(state);
      },
    };
    ensureHomeSentinel(fake);
    expect(calls).toEqual([gpState(0)]);
    ensureHomeSentinel(fake);
    expect(calls).toHaveLength(1);
  });

  it("pushState records panel depth; trap re-pushes depth 0", () => {
    const pushed: unknown[] = [];
    const fake = {
      pushState(state: unknown) {
        pushed.push(state);
      },
    };
    pushPanelHistory(fake, 1);
    trapHomeHistory(fake);
    expect(pushed).toEqual([gpState(1), gpState(0)]);
  });
});
