import { describe, expect, it } from "vitest";
import { normalizeDonations } from "./donations";

describe("donate methods empty JSON", () => {
  it("hides donate when links empty", () => {
    const cfg = normalizeDonations({ enabled: true, message: "x", links: [] });
    expect(cfg.enabled).toBe(false);
    expect(cfg.links).toEqual([]);
  });

  it("hides donate when raw null", () => {
    const cfg = normalizeDonations(null);
    expect(cfg.enabled).toBe(false);
  });
});
