"""Count remaining BUILD_PLAN rows by owner and refresh the tally block."""
from __future__ import annotations

import argparse
import re
import sys
from pathlib import Path

OWNERS = ("AGENT", "AUTO", "HUMAN", "ADB")
OPEN = {"🔲", "❌"}
ROW = re.compile(
    r"^(?:(?:\d+[a-z]?)\.|-)\s+(?P<status>🔲|✅|❌|⬜)\s+"
    r"\[(?P<owner>AGENT|AUTO|HUMAN|ADB)\]"
)
BLOCK = re.compile(
    r"<!-- remaining-tally -->\n.*?\n<!-- /remaining-tally -->",
    re.DOTALL,
)
MARKERS = "<!-- remaining-tally -->\n{body}\n<!-- /remaining-tally -->"


def count_remaining(text: str) -> dict[str, int]:
    counts = {name: 0 for name in OWNERS}
    extra = 0
    for line in text.splitlines():
        match = ROW.match(line)
        if not match or match.group("status") not in OPEN:
            continue
        owner = match.group("owner")
        if owner in counts:
            counts[owner] += 1
        else:
            extra += 1
    if extra:
        counts["OTHER"] = extra
    return counts


def format_tally(counts: dict[str, int]) -> str:
    parts = [f"{name} {counts.get(name, 0)}" for name in OWNERS]
    if counts.get("OTHER"):
        parts.append(f"OTHER {counts['OTHER']}")
    total = sum(counts.get(name, 0) for name in (*OWNERS, "OTHER"))
    return f"**Remaining:** {' · '.join(parts)} · **{total} open**"


def apply_tally(text: str) -> str:
    body = format_tally(count_remaining(text))
    block = MARKERS.format(body=body)
    if BLOCK.search(text):
        return BLOCK.sub(block, text, count=1)
    if text.startswith("# "):
        first, _, rest = text.partition("\n")
        return f"{first}\n\n{block}\n{rest.lstrip()}"
    return f"{block}\n\n{text}"


def refresh_file(path: Path, *, check: bool) -> int:
    if not path.is_file():
        print(f"SKIP: {path} missing", file=sys.stderr)
        return 0
    raw = path.read_text(encoding="utf-8")
    updated = apply_tally(raw)
    if raw == updated:
        print(f"OK: {path.name} tally")
        return 0
    if check:
        print(f"FAIL: {path} tally stale; run refresh-build-plan-tally", file=sys.stderr)
        return 1
    path.write_text(updated, encoding="utf-8")
    print(f"Updated {path}")
    return 0


def plan_paths(root: Path) -> list[Path]:
    names = ("BUILD_PLAN.md", "BUILD_PLAN_TEMPLATE.md")
    return [root / name for name in names if (root / name).is_file()]


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument("--root", default=".")
    parser.add_argument("--check", action="store_true")
    parser.add_argument("paths", nargs="*")
    args = parser.parse_args()
    root = Path(args.root).resolve()
    paths = [Path(p) for p in args.paths] if args.paths else plan_paths(root)
    code = 0
    for path in paths:
        code = max(code, refresh_file(path if path.is_absolute() else root / path, check=args.check))
    return code


if __name__ == "__main__":
    sys.exit(main())
