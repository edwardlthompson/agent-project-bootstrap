import { afterEach, describe, expect, it, vi } from "vitest";
import { canUseViewTransitions, runNavTransition } from "./viewTransitions";

describe("viewTransitions", () => {
  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("is off when reduced motion is preferred", () => {
    vi.stubGlobal(
      "matchMedia",
      vi.fn().mockReturnValue({
        matches: true,
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
      }),
    );
    expect(canUseViewTransitions()).toBe(false);
  });

  it("falls back to sync update without startViewTransition", () => {
    vi.stubGlobal(
      "matchMedia",
      vi.fn().mockReturnValue({
        matches: false,
        addEventListener: vi.fn(),
        removeEventListener: vi.fn(),
      }),
    );
    const spy = vi.fn();
    expect(runNavTransition(spy)).toBeNull();
    expect(spy).toHaveBeenCalledOnce();
  });
});
