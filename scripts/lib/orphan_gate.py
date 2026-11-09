"""Orphan gate skeleton with --baseline (full classes in Part 2)."""
from __future__ import annotations

import json
from pathlib import Path


def load_goldenpath(root: Path) -> dict | None:
    path = root / ".goldenpath.json"
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else None


def load_baseline(path: Path | None) -> set[str]:
    if path is None or not path.is_file():
        return set()
    raw = json.loads(path.read_text(encoding="utf-8"))
    if isinstance(raw, dict):
        return set(raw.keys())
    if isinstance(raw, list):
        return {str(x) for x in raw}
    return set()


def load_allowlist(root: Path) -> set[str]:
    path = root / "scripts" / "orphan-allowlist.txt"
    if not path.is_file():
        return set()
    out: set[str] = set()
    for line in path.read_text(encoding="utf-8").splitlines():
        stripped = line.strip()
        if stripped and not stripped.startswith("#"):
            out.add(stripped.rstrip("/"))
    return out


def scan_orphans(root: Path) -> list[str]:
    """Require .goldenpath.json; full graph walk expands later."""
    gp = load_goldenpath(root)
    if gp is None:
        return ["GOLDENPATH-ORPHAN-TREE:.goldenpath.json missing"]
    if not gp.get("stacks"):
        return ["GOLDENPATH-ORPHAN-TREE:stacks empty"]
    if not (root / "scripts" / "orphan-allowlist.txt").is_file():
        return ["GOLDENPATH-ORPHAN-TREE:scripts/orphan-allowlist.txt missing"]
    _ = load_allowlist(root)
    return []


def check(root: Path, baseline_path: Path | None = None) -> tuple[int, str]:
    baselined = load_baseline(baseline_path)
    findings = [f for f in scan_orphans(root) if f not in baselined]
    if findings:
        return 1, "orphan findings: " + "; ".join(findings)
    return 0, "OK: orphan gate (skeleton; no unbaselined findings)"
