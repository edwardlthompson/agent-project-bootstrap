import { readFileSync } from "node:fs";
import { dirname, join } from "node:path";
import { fileURLToPath } from "node:url";

const specPath = join(dirname(fileURLToPath(import.meta.url)), "..", "openapi.json");

export function loadOpenApiSpec(): Record<string, unknown> {
  return JSON.parse(readFileSync(specPath, "utf8")) as Record<string, unknown>;
}

export function specPaths(): string[] {
  const spec = loadOpenApiSpec();
  const paths = spec.paths;
  if (!paths || typeof paths !== "object") {
    return [];
  }
  return Object.keys(paths);
}
