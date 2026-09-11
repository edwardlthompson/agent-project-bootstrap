import { describe, expect, it } from "vitest";
import { isAllowedVenmoUrl } from "./venmoAllowlist";

describe("Venmo URL allowlist", () => {
  it("allows exemplar Venmo code URL", () => {
    expect(isAllowedVenmoUrl("https://venmo.com/code?user_id=1857304970395648420")).toBe(true);
  });
  it("rejects non-Venmo and http", () => {
    expect(isAllowedVenmoUrl("https://evil.example/code?user_id=1")).toBe(false);
    expect(isAllowedVenmoUrl("http://venmo.com/code?user_id=1")).toBe(false);
    expect(isAllowedVenmoUrl("not-a-url")).toBe(false);
  });
});
