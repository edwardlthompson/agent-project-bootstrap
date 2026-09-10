import en from "../locales/en.json";
import es from "../locales/es.json";

const catalogs: Record<string, Record<string, string>> = {
  en: en as Record<string, string>,
  es: es as Record<string, string>,
};

function preferredLocale(): string {
  const raw = typeof navigator === "undefined" ? "en" : navigator.language;
  const lang = raw.slice(0, 2).toLowerCase();
  return lang in catalogs ? lang : "en";
}

let currentLocale = preferredLocale();

export function getLocale(): string {
  return currentLocale;
}

export function setLocale(locale: string): void {
  if (!catalogs[locale]) {
    return;
  }
  currentLocale = locale;
  document.documentElement.lang = locale;
}

export function t(key: string): string {
  const catalog = catalogs[currentLocale] ?? catalogs.en;
  return catalog[key] ?? catalogs.en[key] ?? key;
}

export function supportedLocales(): string[] {
  return Object.keys(catalogs);
}
