import en from "../locales/en.json";
import es from "../locales/es.json";

const catalogs: Record<string, Record<string, string>> = {
  en: en as Record<string, string>,
  es: es as Record<string, string>,
};

/** BCP-47 primary tags that force RTL layout (Android LocaleRtlUiTest parity). */
const RTL_LANGS = new Set(["ar", "he", "fa", "ur"]);

export function localeDir(lang: string): "rtl" | "ltr" {
  return RTL_LANGS.has(lang.slice(0, 2).toLowerCase()) ? "rtl" : "ltr";
}

function browserLang(): string {
  if (typeof navigator === "undefined") return "en";
  return (navigator.language || "en").slice(0, 2).toLowerCase() || "en";
}

function preferredLocale(): string {
  const lang = browserLang();
  return lang in catalogs ? lang : "en";
}

let currentLocale = preferredLocale();

function syncDocumentLocale(layoutLang: string = browserLang()): void {
  if (typeof document === "undefined") return;
  document.documentElement.lang = currentLocale;
  // Layout follows browser language so Arabic still forces RTL when strings fall back to en.
  document.documentElement.dir = localeDir(layoutLang);
}

syncDocumentLocale();

export function getLocale(): string {
  return currentLocale;
}

export function setLocale(locale: string): void {
  if (!catalogs[locale]) {
    return;
  }
  currentLocale = locale;
  syncDocumentLocale(locale);
}

/**
 * Apply layout direction for a locale even when no catalog exists (Arabic fallback strings).
 * Catalog locale updates only when a translation pack is present.
 */
export function applyLayoutLocale(locale: string): void {
  const lang = locale.slice(0, 2).toLowerCase();
  if (lang in catalogs) {
    currentLocale = lang;
  }
  syncDocumentLocale(lang);
}

export function t(key: string): string {
  const catalog = catalogs[currentLocale] ?? catalogs.en;
  return catalog[key] ?? catalogs.en[key] ?? key;
}

export function supportedLocales(): string[] {
  return Object.keys(catalogs);
}
