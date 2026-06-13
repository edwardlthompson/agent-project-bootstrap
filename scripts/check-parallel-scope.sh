#!/usr/bin/env bash
# Detect overlapping isolated scopes in BUILD_PLAN Parallel tables.
set -euo pipefail
ROOT="$(cd "$(dirname "$0")/.." && pwd)"
python3 - "$ROOT/BUILD_PLAN.md" << 'PY'
import re
import sys
from pathlib import Path

text = Path(sys.argv[1]).read_text(encoding="utf-8")
# Rows like: | Task | AGENT | `examples/web/**` |
rows = re.findall(r"^\|[^|]+\|[^|]+\|\s*`([^`]+)`\s*\|", text, re.M)
scopes = [s.strip() for s in rows if s.strip()]
errors = []
for i, a in enumerate(scopes):
    for j, b in enumerate(scopes):
        if j <= i:
            continue
        # Normalize trailing /** for prefix compare
        pa, pb = a.rstrip("/"), b.rstrip("/")
        if pa == pb or pa.startswith(pb + "/") or pb.startswith(pa + "/"):
            errors.append(f"overlap: {a!r} vs {b!r}")
if errors:
    print("Parallel scope collisions detected:")
    for e in errors:
        print(f"  {e}")
    sys.exit(1)
print("No parallel scope overlaps detected")
PY
