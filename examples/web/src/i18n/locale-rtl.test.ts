import { beforeEach, describe, expect, it } from "vitest";

import { applyLayoutLocale, getLocale, localeDir, setLocale, t } from "./index";

describe("locale RTL smoke (Android LocaleRtlUiTest parity)", () => {
  beforeEach(() => {
    setLocale("en");
    document.documentElement.dir = "ltr";
    document.documentElement.lang = "en";
  });

  it("spanish catalog loads settings search and section titles", () => {
    setLocale("es");
    expect(getLocale()).toBe("es");
    expect(t("settings.search")).toBe("Buscar ajustes");
    expect(t("settings.title")).toBe("Ajustes");
    expect(t("settings.section.privacy")).toBe("Privacidad");
    expect(document.documentElement.dir).toBe("ltr");
  });

  it("arabic layout forces RTL even when strings fall back to English", () => {
    expect(localeDir("ar")).toBe("rtl");
    applyLayoutLocale("ar");
    expect(getLocale()).toBe("en");
    expect(document.documentElement.dir).toBe("rtl");
    expect(document.documentElement.lang).toBe("en");
    expect(t("settings.search").trim().length).toBeGreaterThan(0);
    expect(t("settings.title").trim().length).toBeGreaterThan(0);
  });
});
