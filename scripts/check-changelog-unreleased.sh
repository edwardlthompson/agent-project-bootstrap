#!/usr/bin/env bash
# Fail when CHANGELOG.md has zero or multiple ## [Unreleased] sections.
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
CHANGELOG="$ROOT/CHANGELOG.md"

if [ ! -f "$CHANGELOG" ]; then
  echo "MISSING: CHANGELOG.md"
  exit 1
fi

count="$(grep -c '^## \[Unreleased\]' "$CHANGELOG" || true)"

if [ "$count" -ne 1 ]; then
  echo "CHANGELOG.md must have exactly one ## [Unreleased] section (found $count)"
  exit 1
fi

echo "CHANGELOG Unreleased check passed"
