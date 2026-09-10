/** Filter Settings groups by a case-insensitive substring. */

export function tokensMatch(query: string, haystack: string): boolean {
  const needle = query.trim().toLowerCase();
  if (!needle) return true;
  return haystack.toLowerCase().includes(needle);
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
