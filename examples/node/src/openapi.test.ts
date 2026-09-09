import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

import { describe, expect, it } from "vitest";

import { createApp } from "./app.js";
import { specPaths } from "./openapi.js";

const specFile = join(dirname(fileURLToPath(import.meta.url)), "..", "openapi.json");

function requiredKeys(body: unknown, keys: string[]): void {
  expect(body).toBeTypeOf("object");
  for (const key of keys) {
    expect(body).toHaveProperty(key);
  }
}

describe("OpenAPI contract", () => {
  it("lists implemented routes", () => {
    const spec = JSON.parse(readFileSync(specFile, "utf8")) as { openapi: string };
    expect(spec.openapi).toMatch(/^3\./);
    expect(specPaths()).toEqual(
      expect.arrayContaining([
        "/health",
        "/about",
        "/feedback",
        "/greet",
        "/greet/{name}",
        "/openapi.json",
      ]),
    );
  });

  it("serves the spec and live responses match required fields", async () => {
    const app = createApp();
    const specRes = await app.request("/openapi.json");
    expect(specRes.status).toBe(200);
    const served = (await specRes.json()) as { paths: Record<string, unknown> };
    expect(Object.keys(served.paths)).toEqual(specPaths());

    const health = await (await app.request("/health")).json();
    requiredKeys(health, ["status"]);
    expect((health as { status: string }).status).toBe("ok");

    const about = await (await app.request("/about")).json();
    requiredKeys(about, ["version", "donate", "summary", "update"]);

    const greet = await (await app.request("/greet/FOSS")).json();
    requiredKeys(greet, ["message"]);

    const feedback = await (await app.request("/feedback")).json();
    requiredKeys(feedback, ["kind", "url"]);
  });
});
