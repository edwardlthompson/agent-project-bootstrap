import { afterEach, beforeEach, describe, expect, it, vi } from "vitest";
import {
  checkForUpdates,
  getInterval,
  setIntervalPref,
} from "./aboutSession";

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

describe("checkForUpdates", () => {
  beforeEach(() => {
    localStorage.clear();
    vi.restoreAllMocks();
  });

  afterEach(() => {
    vi.unstubAllGlobals();
  });

  it("does not persist lastChecked when GitHub fetch fails", async () => {
    setIntervalPref("daily");
    vi.stubGlobal(
      "fetch",
      vi.fn(async (url: string) => {
        if (url.endsWith("/app-update.json")) {
          return new Response(
            JSON.stringify({
              release_repo: "test-owner/test-repo",
              installed_artifact_format: "pwa",
            }),
            { status: 200 },
          );
        }
        return new Response("error", { status: 500 });
      }),
    );

    await checkForUpdates();

    expect(localStorage.getItem("gp-app-update-last-checked")).toBeNull();
  });

  it("persists lastChecked after successful GitHub fetch", async () => {
    setIntervalPref("daily");
    vi.stubGlobal(
      "fetch",
      vi.fn(async (url: string) => {
        if (url.endsWith("/app-update.json")) {
          return new Response(
            JSON.stringify({
              release_repo: "test-owner/test-repo",
              installed_artifact_format: "pwa",
            }),
            { status: 200 },
          );
        }
        return new Response(JSON.stringify({ tag_name: "v0.1.0" }), {
          status: 200,
        });
      }),
    );

    await checkForUpdates();

    expect(localStorage.getItem("gp-app-update-last-checked")).not.toBeNull();
  });
});
