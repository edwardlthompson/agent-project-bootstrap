#!/usr/bin/env bash
# Hash desktop installer files (or a local dry-run zip) and write a Winget stub.
# Does not submit to microsoft/winget-pkgs. [HUMAN] opens that PR.
# Usage:
#   scripts/winget-publish-loop.sh --dry-run
#   WINGET_INSTALLER_X64=dist/app-x64.zip WINGET_INSTALLER_ARM64=dist/app-arm64.zip \
#     scripts/winget-publish-loop.sh
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"
# shellcheck source=lib/resolve-python.sh
. "$(cd "$(dirname "$0")" && pwd)/lib/resolve-python.sh"

OUT_DIR="${WINGET_LOOP_OUT:-$ROOT/dist/winget-loop}"
STUB="$OUT_DIR/manifest.stub.yaml"
DRY=0
if [ "${1:-}" = "--dry-run" ]; then
  DRY=1
fi

mkdir -p "$OUT_DIR"
X64="${WINGET_INSTALLER_X64:-}"
ARM64="${WINGET_INSTALLER_ARM64:-}"

if [ -z "$X64" ] && [ "$DRY" = "1" ]; then
  X64="$OUT_DIR/goldenpath-dry-x64.zip"
  printf 'Golden Path Winget dry-run\n' > "$OUT_DIR/README.txt"
  if command -v zip >/dev/null 2>&1; then
    (cd "$OUT_DIR" && zip -q -X "goldenpath-dry-x64.zip" README.txt)
  else
    tar -C "$OUT_DIR" -cf "$X64" README.txt
  fi
  echo "NOTE dry-run packed $X64 — replace with Windows Release assets before submit"
fi

if [ -z "$X64" ] || [ ! -f "$X64" ]; then
  echo "FAIL: set WINGET_INSTALLER_X64 to an existing installer, or pass --dry-run"
  exit 1
fi

ARGS=(--x64 "$X64" --out "$STUB")
if [ -n "$ARM64" ] && [ -f "$ARM64" ]; then
  ARGS+=(--arm64 "$ARM64")
else
  echo "NOTE arm64 installer omitted — set WINGET_INSTALLER_ARM64 for both arches"
fi

"$PY" "$ROOT/scripts/lib/winget_publish_loop.py" "${ARGS[@]}"
bash "$ROOT/scripts/validate-winget-stub.sh" "$STUB"
echo "OK   Winget loop wrote $STUB (no submit)"
