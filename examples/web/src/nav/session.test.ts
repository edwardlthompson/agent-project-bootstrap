import { describe, expect, it } from "vitest";
import { homeNav, push, serialize, setPrompt } from "./index";
import { NAV_STORAGE_KEY } from "./history";
import {
  applyFeedbackIntents,
  applyPanelScroll,
  applyPop,
  historyDepth,
  loadNav,
  readPanelScroll,
  saveNav,
  syncHistoryToNav,
} from "./session";
import { recordScroll } from "./persist";

describe("nav session", () => {
  it("loadNav restores stack and clears promptOpen", () => {
    const storage = new Map<string, string>();
    const persisted = setPrompt(push(homeNav(), "about"), true);
    storage.set(NAV_STORAGE_KEY, serialize(persisted));
    const loaded = loadNav({ getItem: (key) => storage.get(key) ?? null });
    expect(loaded.stack).toEqual(["home", "about"]);
    expect(loaded.promptOpen).toBe(false);
  });

  it("saveNav writes gp.nav.v1", () => {
    const data = new Map<string, string>();
    saveNav(push(homeNav(), "settings"), { setItem: (k, v) => data.set(k, v) });
    expect(data.has(NAV_STORAGE_KEY)).toBe(true);
    expect(loadNav({ getItem: (k) => data.get(k) ?? null }).stack).toEqual(["home", "settings"]);
  });

  it("crash then share still push feedback; share wins kind", () => {
    const about = push(homeNav(), "about");
    const crashed = applyFeedbackIntents(about, { crash: true, share: "" });
    expect(crashed.nav.stack).toEqual(["home", "about", "feedback"]);
    expect(crashed.nav.feedbackKind).toBe("bug");
    const shared = applyFeedbackIntents(crashed.nav, { crash: false, share: "clip" });
    expect(shared.nav.stack).toEqual(["home", "about", "feedback"]);
    expect(shared.nav.feedbackKind).toBe("feature");
    expect(shared.prefill).toBe("clip");
  });

  it("applyPop pops one route and traps only at home", () => {
    const about = push(homeNav(), "about");
    const feedback = push(about, "feedback", "bug");
    const backAbout = applyPop(feedback, 40);
    expect(backAbout.nav.stack).toEqual(["home", "about"]);
    expect(backAbout.nav.scroll.feedback).toBe(40);
    expect(backAbout.trapHome).toBe(false);
    const backHome = applyPop(backAbout.nav, 0);
    expect(backHome.nav.stack).toEqual(["home"]);
    expect(backHome.trapHome).toBe(true);
    expect(applyPop(homeNav(), 0).trapHome).toBe(true);
  });

  it("syncHistoryToNav replaceState then pushState per extra depth", () => {
    const pushed: unknown[] = [];
    const fake = {
      state: null as unknown,
      replaceState(state: unknown) {
        this.state = state;
      },
      pushState(state: unknown) {
        this.state = state;
        pushed.push(state);
      },
    };
    const nav = push(push(homeNav(), "about"), "feedback", "bug");
    syncHistoryToNav(fake, nav);
    expect(pushed).toEqual([{ gp: true, depth: 1 }, { gp: true, depth: 2 }]);
    expect(historyDepth(nav)).toBe(2);
  });

  it("loadNav returns home when storage throws", () => {
    expect(
      loadNav({
        getItem() {
          throw new Error("blocked");
        },
      }),
    ).toEqual(homeNav());
  });

  it("syncHistoryToNav is a no-op when depth already matches", () => {
    const pushed: unknown[] = [];
    const fake = {
      state: { gp: true, depth: 1 } as unknown,
      replaceState() {},
      pushState(state: unknown) {
        pushed.push(state);
      },
    };
    syncHistoryToNav(fake, push(homeNav(), "about"));
    expect(pushed).toEqual([]);
  });

  it("read and apply panel scroll", () => {
    const root = document.createElement("div");
    expect(readPanelScroll(root)).toBe(0);
    const panel = document.createElement("section");
    panel.dataset.testid = "about-panel";
    root.append(panel);
    applyPanelScroll(root, recordScroll(push(homeNav(), "about"), "about", 15));
    expect(panel.scrollTop).toBe(15);
    panel.scrollTop = 8;
    expect(readPanelScroll(root)).toBe(8);
  });

  it("historyDepth counts launch prompt as one extra entry", () => {
    expect(historyDepth(setPrompt(homeNav(), true))).toBe(1);
  });

  it("isFiniteDepth treats missing depth as 0", () => {
    const pushed: unknown[] = [];
    const fake = {
      state: { gp: true } as unknown,
      replaceState(state: unknown) {
        this.state = state;
      },
      pushState(state: unknown) {
        this.state = state;
        pushed.push(state);
      },
    };
    syncHistoryToNav(fake, push(homeNav(), "settings"));
    expect(pushed).toEqual([{ gp: true, depth: 1 }]);
  });
});
