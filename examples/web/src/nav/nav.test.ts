import { describe, expect, it } from "vitest";
import {
  canPop,
  current,
  deserialize,
  homeNav,
  pop,
  push,
  recordScroll,
  restoreScroll,
  serialize,
  setPrompt,
} from "./index";

describe("nav stack", () => {
  it("push same top is a no-op", () => {
    const about = push(homeNav(), "about");
    expect(push(about, "about")).toEqual(about);
  });

  it("opening a panel pushes", () => {
    const next = push(homeNav(), "settings");
    expect(current(next)).toBe("settings");
    expect(canPop(next)).toBe(true);
  });

  it("pop one level never goes below home", () => {
    const settings = push(homeNav(), "settings");
    expect(current(pop(settings))).toBe("home");
    expect(pop(homeNav())).toEqual(homeNav());
    expect(canPop(homeNav())).toBe(false);
  });

  it("about then report-bug pushes feedback; back returns to about then home", () => {
    const about = push(homeNav(), "about");
    const feedback = push(about, "feedback", "bug");
    expect(feedback.stack).toEqual(["home", "about", "feedback"]);
    expect(feedback.feedbackKind).toBe("bug");
    const backAbout = pop(feedback);
    expect(current(backAbout)).toBe("about");
    expect(backAbout.stack).toEqual(["home", "about"]);
    expect(current(pop(backAbout))).toBe("home");
  });

  it("pop dismisses launch prompt before popping a route", () => {
    const prompted = setPrompt(push(homeNav(), "about"), true);
    const dismissed = pop(prompted);
    expect(dismissed.promptOpen).toBe(false);
    expect(current(dismissed)).toBe("about");
    expect(current(pop(dismissed))).toBe("home");
  });
});

describe("nav persist", () => {
  it("serialize deserialize roundtrip keeps stack kind scroll and prompt", () => {
    let state = recordScroll(push(push(homeNav(), "about"), "feedback", "feature"), "about", 80);
    state = setPrompt(state, true);
    const restored = deserialize(serialize(state));
    expect(restored.stack).toEqual(["home", "about", "feedback"]);
    expect(restored.feedbackKind).toBe("feature");
    expect(restoreScroll(restored, "about")).toBe(80);
    expect(restored.promptOpen).toBe(true);
  });

  it("deserialize invalid or empty returns home", () => {
    expect(deserialize("")).toEqual(homeNav());
    expect(deserialize("{")).toEqual(homeNav());
    expect(deserialize("null")).toEqual(homeNav());
  });

  it("restoreScroll reads settings about feedback and ignores home", () => {
    const withScroll = recordScroll(recordScroll(homeNav(), "settings", 12.9), "home", 99);
    expect(restoreScroll(withScroll, "settings")).toBe(12);
    expect(restoreScroll(withScroll, "home")).toBe(0);
    expect(restoreScroll(homeNav(), "about")).toBe(0);
  });
});
