/** Allowlist for Venmo donate deep links (no open redirects). */
const VENMO_HOSTS = new Set(["venmo.com", "www.venmo.com"]);

export function isAllowedVenmoUrl(url: string): boolean {
  try {
    const u = new URL(url);
    if (u.protocol !== "https:") return false;
    if (!VENMO_HOSTS.has(u.hostname.toLowerCase())) return false;
    return u.pathname === "/code" || u.pathname.startsWith("/code?");
  } catch {
    return false;
  }
}
