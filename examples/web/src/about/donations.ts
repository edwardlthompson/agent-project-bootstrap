import { assetUrl } from "../assetUrl";
import { withQuietDonate } from "./donate";
import type { DonationConfig, DonationLink } from "./types";

export const DEFAULT_VENMO_URL = "https://venmo.com/code?user_id=1857304970395648420";

export function primaryDonateUrl(config: DonationConfig): string {
  return config.links[0]?.url || DEFAULT_VENMO_URL;
}

function isLink(value: unknown): value is DonationLink {
  if (!value || typeof value !== "object") return false;
  const v = value as DonationLink;
  return typeof v.label === "string" && typeof v.url === "string";
}

export function normalizeDonations(raw: unknown): DonationConfig {
  if (!raw || typeof raw !== "object") {
    return { enabled: false, message: "", links: [] };
  }
  const obj = raw as DonationConfig;
  const links = Array.isArray(obj.links) ? obj.links.filter(isLink) : [];
  return {
    enabled: Boolean(obj.enabled) && links.length > 0,
    message: typeof obj.message === "string" ? obj.message : "",
    links,
  };
}

async function fetchDonationsJson(url: string): Promise<DonationConfig | null> {
  try {
    const res = await fetch(url);
    if (!res.ok) return null;
    return normalizeDonations(await res.json());
  } catch {
    return null;
  }
}

/** Prefer live donations.json; fall back to packaged exemplar when sync was skipped. */
export async function loadDonations(
  url = assetUrl("donations.json"),
  exemplarUrl = assetUrl("donations.json.example"),
): Promise<DonationConfig> {
  const primary = await fetchDonationsJson(url);
  if (primary) return withQuietDonate(primary);
  const exemplar = await fetchDonationsJson(exemplarUrl);
  if (exemplar) return withQuietDonate(exemplar);
  return withQuietDonate({ enabled: false, message: "", links: [] });
}
