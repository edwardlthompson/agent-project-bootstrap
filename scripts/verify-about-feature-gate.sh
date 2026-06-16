#!/usr/bin/env bash
# Verify lego removal: feature-gate passes with About present and after simulated removal.
# Usage: scripts/verify-about-feature-gate.sh
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

if command -v python3 >/dev/null 2>&1; then PY=python3
elif command -v python >/dev/null 2>&1; then PY=python
else PY=python3; fi

WEB_SRC="$ROOT/examples/web/src"
WEB_E2E="$ROOT/examples/web/e2e"
BACKUP="$(mktemp -d)"

restore() {
  if [ -d "$BACKUP/about" ]; then
    rm -rf "$WEB_SRC/about"
    cp -a "$BACKUP/about" "$WEB_SRC/about"
  fi
  for rel in main.ts appBootstrap.ts appBootstrap.test.ts AppShell.ts components/AboutPanel.ts; do
    if [ -f "$BACKUP/$rel" ]; then
      cp -a "$BACKUP/$rel" "$WEB_SRC/$rel"
    fi
  done
  if [ -f "$BACKUP/app.spec.ts" ]; then
    cp -a "$BACKUP/app.spec.ts" "$WEB_E2E/app.spec.ts"
  fi
  rm -rf "$BACKUP"
}
trap restore EXIT

echo "=== About feature gate verification ==="

echo "1/2 Gate with About feature present..."
bash scripts/feature-gate.sh --stack web --step about-with

cp -a "$WEB_SRC/about" "$BACKUP/about"
cp -a "$WEB_SRC/main.ts" "$BACKUP/main.ts"
cp -a "$WEB_SRC/appBootstrap.ts" "$BACKUP/appBootstrap.ts"
cp -a "$WEB_SRC/appBootstrap.test.ts" "$BACKUP/appBootstrap.test.ts"
cp -a "$WEB_SRC/AppShell.ts" "$BACKUP/AppShell.ts"
cp -a "$WEB_SRC/components/AboutPanel.ts" "$BACKUP/AboutPanel.ts"
cp -a "$WEB_E2E/app.spec.ts" "$BACKUP/app.spec.ts"

$PY << 'PY'
from pathlib import Path
import shutil

web = Path("examples/web/src")
e2e = Path("examples/web/e2e")

web.joinpath("main.ts").write_text(
    """import "./style.css";
import { createThemeToggle } from "./components/ThemeToggle";
import { isOnline } from "./greet";
import { t } from "./i18n";
import { initTheme } from "./theme";

const app = document.querySelector<HTMLDivElement>("#app");
if (!app) throw new Error("App root element not found");
const root = app;

function render(): void {
  const online = isOnline();
  const statusKey = online ? "app.status.online" : "app.status.offline";
  root.innerHTML = `
    <main>
      <div class="gp-header">
        <h1 class="gp-title">${t("app.title")}</h1>
        <div class="gp-header-actions"></div>
      </div>
      <p class="gp-headline">${t("app.greeting")}</p>
      <p class="gp-body" data-testid="status">${t(statusKey)}</p>
    </main>
  `;
  const actions = root.querySelector<HTMLDivElement>(".gp-header-actions");
  if (actions) actions.insertBefore(createThemeToggle(), actions.firstChild);
}

initTheme();
render();
window.addEventListener("online", render);
window.addEventListener("offline", render);
""",
    encoding="utf-8",
)

for path in (
    web / "about",
    web / "appBootstrap.ts",
    web / "appBootstrap.test.ts",
    web / "AppShell.ts",
    web / "components" / "AboutPanel.ts",
):
    if path.is_dir():
        shutil.rmtree(path, ignore_errors=True)
    elif path.exists():
        path.unlink()

e2e.joinpath("app.spec.ts").write_text(
    """import { test, expect } from "@playwright/test";

test("renders golden path heading without About slice", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "Golden Path PWA" })).toBeVisible();
  await expect(page.getByTestId("status")).toBeVisible();
});
""",
    encoding="utf-8",
)
PY

echo "2/2 Gate after About removal (in-place, restored on exit)..."
bash scripts/feature-gate.sh --stack web --step about-without

echo "About add/remove verification passed"
