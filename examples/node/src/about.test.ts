import { describe, expect, it } from "vitest";

import { APP_VERSION, aboutPayload, aboutSummary } from "./about.js";

function assertAboutShape(payload: ReturnType<typeof aboutPayload>): void {
  expect(payload.version).toBeTruthy();
  expect(payload.donate.startsWith("http")).toBe(true);
  expect(payload.summary.length).toBeGreaterThan(0);
  expect(["current", "available", "unknown"]).toContain(payload.update.status);
  expect(payload).toHaveProperty("update.version");
  expect(payload).toHaveProperty("update.url");
}

describe("about", () => {
  it("includes version and donate", () => {
    const text = aboutSummary();
    expect(text).toContain(APP_VERSION);
    expect(text).toContain("donate");
  });

  it("payload matches About fields", () => {
    const payload = aboutPayload();
    expect(payload.version).toBe(APP_VERSION);
    expect(payload.donate).toContain("http");
    expect(payload.summary).toBe(aboutSummary());
    expect(payload.update).toEqual({ status: "current", version: null, url: null });
  });

  it("matches golden-path about-payload schema contract", () => {
    const payload = aboutPayload();
    assertAboutShape(payload);
    expect(Object.keys(payload).sort()).toEqual(["donate", "summary", "update", "version"]);
    expect(Object.keys(payload.update).sort()).toEqual(["status", "url", "version"]);
  });
});
