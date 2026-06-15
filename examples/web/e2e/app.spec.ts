import { test, expect } from "@playwright/test";
import AxeBuilder from "@axe-core/playwright";

test("renders golden path heading", async ({ page }) => {
  await page.goto("/");
  await expect(page.getByRole("heading", { name: "Golden Path PWA" })).toBeVisible();
  await expect(page.getByText("Hello, FOSS!")).toBeVisible();
  await expect(page.getByTestId("status")).toContainText("Golden Path PWA");
});

test("passes accessibility audit", async ({ page }) => {
  await page.goto("/");
  const results = await new AxeBuilder({ page }).analyze();
  expect(results.violations).toEqual([]);
});

test("homepage visual snapshot", async ({ page }) => {
  await page.goto("/");
  await expect(page.locator("main")).toBeVisible();
  await expect(page).toHaveScreenshot("homepage.png", { maxDiffPixelRatio: 0.02 });
});

test("opens settings panel and toggles theme", async ({ page }) => {
  await page.goto("/");
  await page.getByRole("button", { name: "Settings" }).click();
  await expect(page.getByRole("heading", { name: "Settings" })).toBeVisible();
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
