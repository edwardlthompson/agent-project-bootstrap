/** Filter Settings groups by a case-insensitive substring (diacritics-insensitive). */

function stripDiacritics(text: string): string {
  return text.normalize("NFD").replace(/\p{M}+/gu, "");
}

export function tokensMatch(query: string, haystack: string): boolean {
  const needle = stripDiacritics(query.trim()).toLowerCase();
  if (!needle) return true;
  return stripDiacritics(haystack).toLowerCase().includes(needle);
}

export function applySettingsSearch(
  query: string,
  groups: Iterable<HTMLElement>,
  empty: HTMLElement | null,
): number {
  let shown = 0;
  for (const group of groups) {
    const haystack = group.dataset.settingsHaystack ?? group.textContent ?? "";
    const hit = tokensMatch(query, haystack);
    group.hidden = !hit;
    if (hit) shown += 1;
  }
  if (empty) {
    empty.hidden = !(query.trim() && shown === 0);
  }
  return shown;
}
