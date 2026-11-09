"""YOLO runner — refuses unless yolo.on present; never ships armed in template."""
from __future__ import annotations

import json
from pathlib import Path

from argus_contract import check as contract_check

PROTECTED_PREFIXES = (
    ".github/workflows/",
    ".github/CODEOWNERS",
    "docs/",
    "branding/",
    "argus/rules/",
    "package-lock.json",
    "uv.lock",
    "Cargo.lock",
)

CAPS = {"files": 20, "lines": 600, "merges_per_day": 5, "minutes": 30}


def is_armed(root: Path) -> bool:
    return (root / "yolo.on").is_file()


def protected(path: str) -> bool:
    posix = path.replace("\\", "/")
    return any(posix == p or posix.startswith(p) for p in PROTECTED_PREFIXES)


def run(root: Path) -> tuple[int, str]:
    if not is_armed(root):
        return 0, "YOLO off (no yolo.on) — default"
    code, msg = contract_check(root)
    if code != 0:
        return 1, f"YOLO refused: contract stale — {msg}"
    manifest = root / "rules.manifest.json"
    if not manifest.is_file():
        return 1, "YOLO refused: missing rules.manifest.json (pull rules first)"
    return (
        0,
        "YOLO armed: pull rules, one family, caps "
        f"{CAPS['files']} files / {CAPS['lines']} lines; "
        "leave protected paths alone; sticky off via delete yolo.on + YOLO-OFF.md",
    )


def give_up(root: Path, reason: str) -> None:
    on = root / "yolo.on"
    if on.is_file():
        on.unlink()
    (root / "YOLO-OFF.md").write_text(reason.strip() + "\n", encoding="utf-8")
