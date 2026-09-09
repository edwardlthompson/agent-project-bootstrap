import AxeBuilder from "@axe-core/playwright";
import { expect, type Page, test } from "@playwright/test";

test("preview sends CSP and referrer policy", async ({ page }) => {
  const response = await page.goto("/");
  expect(response).toBeTruthy();
  const headers = response?.headers() ?? {};
  expect(headers["content-security-policy"] ?? "").toContain("default-src 'self'");
  expect(headers["referrer-policy"]).toBe("no-referrer");
  expect(headers["permissions-policy"] ?? "").toContain("camera=()");
});

test("renders golden path heading", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "Golden Path PWA" })).toBeVisible();
  await expect(page.getByText("Hello, FOSS!")).toBeVisible();
  await expect(page.getByTestId("status")).toContainText("Golden Path PWA");
});

test("rtl dir places the title after header actions", async ({ page }) => {
  await page.goto("/");
  await page.evaluate(() => {
    document.documentElement.setAttribute("dir", "rtl");
  });
  await expect(page.locator("html")).toHaveAttribute("dir", "rtl");
  await expect(page.getByRole("heading", { name: "Golden Path PWA" })).toBeVisible();
  const title = await page.locator(".gp-title").boundingBox();
  const actions = await page.locator(".gp-header-actions").boundingBox();
  expect(title).toBeTruthy();
  expect(actions).toBeTruthy();
  expect(title!.x).toBeGreaterThan(actions!.x);
});

test("reduced motion shortens settings control transitions", async ({ page }) => {
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.goto("/");
  await page.getByRole("button", { name: "Settings" }).click();
  const duration = await page.locator("[data-settings-theme]").evaluate((el) => {
    return Number.parseFloat(getComputedStyle(el).transitionDuration);
  });
  expect(duration).toBeLessThan(0.02);
});

async function tabUntil(page: Page, name: string): Promise<void> {
  const target = page.getByRole("button", { name });
  for (let i = 0; i < 12; i++) {
    if (await target.evaluate((el) => el === document.activeElement)) {
      return;
    }
    await page.keyboard.press("Tab");
  }
  await expect(target).toBeFocused();
}

test("keyboard-only opens Settings, About, and Feedback", async ({ page }) => {
  await page.goto("/");
  await page.locator("body").click({ position: { x: 0, y: 0 } });
  await tabUntil(page, "Settings");
  await page.keyboard.press("Enter");
  await expect(page.getByTestId("settings-panel")).toBeVisible();
  await page.keyboard.press("Escape");
  await expect(page.getByTestId("settings-panel")).toHaveCount(0);

  await tabUntil(page, "Settings");
  await page.keyboard.press("Enter");
  await tabUntil(page, "App info");
  await page.keyboard.press("Enter");
  await expect(page.getByTestId("about-panel")).toBeVisible();

  await page.getByTestId("about-feedback").selectOption("bug");
  await expect(page.getByTestId("feedback-panel")).toBeVisible();
  await page.keyboard.press("Escape");
  await expect(page.getByTestId("feedback-panel")).toHaveCount(0);
  await expect(page.getByTestId("about-panel")).toBeVisible();
});

test("passes accessibility audit", async ({ page }) => {
  await page.goto("/");
  const results = await new AxeBuilder({ page }).analyze();
  expect(results.violations).toEqual([]);
});

test("passes accessibility audit with settings panel open", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: "Settings" }).click();
  await expect(page.getByTestId("settings-panel")).toBeVisible();
  const results = await new AxeBuilder({ page }).analyze();
  expect(results.violations).toEqual([]);
});

test("passes accessibility audit with about panel open", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: "Settings" }).click();
  await page.getByTestId("settings-panel").getByRole("button", { name: "App info" }).click();
  await expect(page.getByTestId("about-panel")).toBeVisible();
  const results = await new AxeBuilder({ page }).analyze();
  expect(results.violations).toEqual([]);
});

test("homepage visual snapshot", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator("main")).toBeVisible();
  await expect(page).toHaveScreenshot("homepage.png", { maxDiffPixelRatio: 0.02 });
});

const SNAPSHOT = { maxDiffPixelRatio: 0.02, animations: "disabled" as const };

test("settings panel visual snapshot", async ({ page }) => {
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.goto("/");
  await page.getByRole("button", { name: "Settings" }).click();
  const panel = page.getByTestId("settings-panel");
  await expect(panel).toBeVisible();
  await expect(panel).toHaveScreenshot("settings-panel.png", SNAPSHOT);
});

test("about panel visual snapshot", async ({ page }) => {
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.goto("/");
  await page.getByRole("button", { name: "Settings" }).click();
  await page.getByTestId("settings-panel").getByRole("button", { name: "App info" }).click();
  const panel = page.getByTestId("about-panel");
  await expect(panel).toBeVisible();
  await expect(panel).toHaveScreenshot("about-panel.png", SNAPSHOT);
});

test("feedback panel visual snapshot", async ({ page }) => {
  await page.emulateMedia({ reducedMotion: "reduce" });
  await page.goto("/");
  await page.getByRole("button", { name: "Settings" }).click();
  await page.getByTestId("settings-panel").getByRole("button", { name: "App info" }).click();
  await page.getByTestId("about-feedback").selectOption("bug");
  const panel = page.getByTestId("feedback-panel");
  await expect(panel).toBeVisible();
  await expect(panel).toHaveScreenshot("feedback-panel.png", SNAPSHOT);
});

test("settings search filters groups", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: "Settings" }).click();
  const panel = page.getByTestId("settings-panel");
  await expect(panel.getByRole("heading", { name: "Appearance" })).toBeVisible();
  await page.getByTestId("settings-search").fill("privacy");
  await expect(panel.getByRole("heading", { name: "Privacy" })).toBeVisible();
  await expect(panel.getByRole("heading", { name: "Appearance" })).toHaveCount(0);
  await page.getByTestId("settings-search").fill("zzzz-no-match");
  await expect(page.getByTestId("settings-search-empty")).toBeVisible();
});

test("opens settings panel and toggles theme", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: "Settings" }).click();
  await expect(
    page.getByTestId("settings-panel").getByRole("heading", { name: "Settings" }),
  ).toBeVisible();
  await page.locator("[data-settings-theme]").selectOption("dark");
  await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
});

test("persists dark theme after reload", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: "Settings" }).click();
  await page.locator("[data-settings-theme]").selectOption("dark");
  await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
  await page.reload();
  await expect(page.locator("html")).toHaveAttribute("data-theme", "dark");
});

test("opens About from Settings with donate links", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: "Settings" }).click();
  const settings = page.getByTestId("settings-panel");
  await expect(settings).toBeVisible();
  await settings.getByRole("button", { name: "App info" }).click();
  await expect(page.getByTestId("about-panel")).toBeVisible();
  await expect(page.getByTestId("about-status")).toBeVisible();
  await expect(page.getByRole("heading", { name: "Support development" })).toBeVisible();
  await expect(page.getByRole("link", { name: "Donate via Venmo" })).toHaveAttribute(
    "href",
    "https://venmo.com/code?user_id=1857304970395648420",
  );
});

test("keeps donate, About, and theme out of the header", async ({ page }) => {
  await page.goto("/");
  const header = page.locator(".gp-header");
  await expect(header.getByRole("button", { name: "Settings" })).toBeVisible();
  await expect(header.getByRole("button", { name: "Donate via Venmo" })).toHaveCount(0);
  await expect(page.locator("[data-about-open]")).toHaveCount(0);
  await expect(page.locator("[data-donate-open]")).toHaveCount(0);
  await expect(page.locator(".gp-theme-toggle")).toHaveCount(0);
});

test.describe("donate nudge", () => {
  test("shows once after a version change", async ({ page }) => {
    await page.addInitScript(() => {
      if (!localStorage.getItem("gp.update.lastSeenVersion")) {
        localStorage.setItem("gp.update.lastSeenVersion", "0.0.1");
      }
    });
    await page.goto("/");
    await expect(page.getByTestId("donate-nudge")).toBeVisible();
    await expect(page.getByRole("heading", { name: "Development is still going" })).toBeVisible();
    await page.getByTestId("launch-decline").click();
    await expect(page.getByTestId("donate-nudge")).toHaveCount(0);
    await page.reload();
    await expect(page.getByTestId("donate-nudge")).toHaveCount(0);
  });
});

test.describe("PWA apply update", () => {
  test.use({ serviceWorkers: "block" });

  test("clears restart guard on load", async ({ page }) => {
    await page.addInitScript(() => {
      localStorage.setItem("gp-update-restart-pending", "true");
    });
    await page.goto("/");
    const pending = await page.evaluate(() => localStorage.getItem("gp-update-restart-pending"));
    expect(pending).toBeNull();
  });
});

test("serves cached shell offline via service worker", async ({ page, context }) => {
  await page.goto("/");
  await page.waitForLoadState("networkidle");
  await page.waitForFunction(() => navigator.serviceWorker?.controller != null, null, {
    timeout: 15_000,
  });
  await page.reload();
  await page.waitForLoadState("networkidle");
  await expect(page.getByRole("heading", { name: "Golden Path PWA" })).toBeVisible();
  await expect(page.getByText("Hello, FOSS!")).toBeVisible();

  await context.setOffline(true);
  await page.reload();
  await expect(page.getByRole("heading", { name: "Golden Path PWA" })).toBeVisible();
  await expect(page.getByText("Hello, FOSS!")).toBeVisible();
  await expect(page.getByTestId("status")).toBeVisible();
});
