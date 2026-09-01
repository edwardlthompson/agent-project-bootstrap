import { describe, expect, it, vi } from "vitest";
import { createHistoryNav, feedbackPrefillOf } from "./controller";
import { current, homeNav, push } from "./nav";

describe("history nav controller", () => {
  it("Close uses history.back and does not pop until popstate", () => {
    const back = vi.fn();
    const pushState = vi.fn();
    const ctl = createHistoryNav({ back, pushState }, homeNav());
    expect(current(ctl.pushRoute("about")!)).toBe("about");
    expect(pushState).toHaveBeenCalledWith({ gp: true, depth: 1 }, "");
    ctl.pushRoute("feedback", "bug");
    expect(current(ctl.get())).toBe("feedback");
    ctl.popFromUi();
    expect(back).toHaveBeenCalledTimes(1);
    expect(current(ctl.get())).toBe("feedback");
    const popped = ctl.onPopState(document);
    expect(current(popped.nav)).toBe("about");
    expect(popped.trapHome).toBe(false);
  });

  it("popstate at home re-pushState the sentinel", () => {
    const pushState = vi.fn();
    const ctl = createHistoryNav({ back: vi.fn(), pushState }, homeNav());
    const result = ctl.onPopState(document);
    expect(result.trapHome).toBe(true);
    expect(pushState).toHaveBeenCalledWith({ gp: true, depth: 0 }, "");
  });

  it("same-route push calls history.back instead of stacking", () => {
    const back = vi.fn();
    const ctl = createHistoryNav({ back, pushState: vi.fn() }, push(homeNav(), "about"));
    expect(ctl.pushRoute("about")).toBeNull();
    expect(back).toHaveBeenCalledTimes(1);
    expect(current(ctl.get())).toBe("about");
  });

  it("openPrompt pushState a history layer", () => {
    const pushState = vi.fn();
    const ctl = createHistoryNav({ back: vi.fn(), pushState }, homeNav());
    expect(ctl.openPrompt().promptOpen).toBe(true);
    expect(pushState).toHaveBeenCalledWith({ gp: true, depth: 1 }, "");
  });

  it("feedbackPrefillOf drops prefill off the feedback route", () => {
    expect(feedbackPrefillOf(push(homeNav(), "feedback", "bug"), "clip")).toBe("clip");
    expect(feedbackPrefillOf(homeNav(), "clip")).toBeUndefined();
  });
});
