import { beforeEach, describe, expect, it } from "vitest";
import { getInterval, setIntervalPref } from "./aboutSession";

describe("aboutSession interval prefs", () => {
  beforeEach(() => {
    localStorage.clear();
  });

  it("defaults to off (opt-in update checks)", () => {
    expect(getInterval()).toBe("off");
  });

  it("persists interval preference", () => {
    setIntervalPref("daily");
    expect(getInterval()).toBe("daily");
  });
});
