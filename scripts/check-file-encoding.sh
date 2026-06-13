#!/usr/bin/env bash
# Fail if text files use UTF-16 or NUL-byte corruption (must be UTF-8)
set -euo pipefail

ROOT="$(cd "$(dirname "$0")/.." && pwd)"
cd "$ROOT"

python3 - "$ROOT" "$@" << 'PY'
import os, sys

root = sys.argv[1]
targets = sys.argv[2:] if len(sys.argv) > 2 else None
exts = {".md", ".json", ".yml", ".yaml", ".sh", ".ps1", ".mdc", ".toml", ".ts", ".tsx"}
skip_dirs = {".git", "node_modules", ".venv"}
errors = []

def is_bad_encoding(path: str) -> bool:
    with open(path, "rb") as f:
        b = f.read(4)
    if b.startswith(b"\xff\xfe") or b.startswith(b"\xfe\xff"):
        return True
    if len(b) >= 2 and b[1] == 0 and b[0] < 128:
        return True
    return False

def iter_files():
    if targets:
        for t in targets:
            if os.path.isfile(t):
                yield t
        return
    for dirpath, dirnames, filenames in os.walk(root):
        dirnames[:] = [d for d in dirnames if d not in skip_dirs]
        for fn in filenames:
            if os.path.splitext(fn)[1].lower() in exts:
                yield os.path.join(dirpath, fn)

for fp in iter_files():
    if is_bad_encoding(fp):
        errors.append(os.path.relpath(fp, root))

if errors:
    print("Invalid encoding (require UTF-8 without BOM):")
    for e in sorted(errors):
        print(f"  {e}")
    sys.exit(1)

print("File encoding check passed")
PY
