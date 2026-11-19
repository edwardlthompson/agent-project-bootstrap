"""Reject compromised agent-framework 1.26.1/1.26.2 and unexpected .pth hooks."""
from __future__ import annotations

import re
from pathlib import Path

BAD_VERS = ("1.26.1", "1.26.2")
PKG = re.compile(r"agent[-_]framework", re.I)
VER = re.compile(r"1\.26\.[12]\b")
# Unexpected startup hooks under examples (not venv site-packages noise).
PTH_SCAN = (
    Path("examples/python"),
    Path("scripts"),
)


def _scan_text(rel: str, text: str) -> list[str]:
    errors: list[str] = []
    if not PKG.search(text):
        return errors
    if VER.search(text):
        errors.append(f"{rel}: agent-framework 1.26.1/1.26.2 is denylisted (malicious PyPI)")
    return errors


def check_deps(root: Path) -> list[str]:
    errors: list[str] = []
    patterns = (
        "**/pyproject.toml",
        "**/requirements*.txt",
        "**/uv.lock",
        "**/Pipfile.lock",
        "**/constraints*.txt",
    )
    skip = {"node_modules", ".venv", "venv", "dist", "build", ".git"}
    for pattern in patterns:
        for path in root.glob(pattern):
            if any(part in skip for part in path.parts):
                continue
            rel = path.relative_to(root).as_posix()
            errors.extend(_scan_text(rel, path.read_text(encoding="utf-8", errors="replace")))
    return errors


def check_pth_hooks(root: Path) -> list[str]:
    """Flag tracked .pth files under examples/python or scripts (startup hooks)."""
    errors: list[str] = []
    for base in PTH_SCAN:
        folder = root / base
        if not folder.is_dir():
            continue
        for path in folder.rglob("*.pth"):
            if any(part in {".venv", "venv", "site-packages"} for part in path.parts):
                continue
            rel = path.relative_to(root).as_posix()
            errors.append(f"{rel}: unexpected .pth startup hook (review; wfx/agent-framework style)")
    return errors


def check_repo(root: Path) -> list[str]:
    return check_deps(root) + check_pth_hooks(root)


def main() -> int:
    errors = check_repo(Path.cwd())
    if errors:
        print("agent-framework denylist check failed:")
        for item in errors:
            print(f"  {item}")
        return 1
    print("agent-framework denylist clean (no 1.26.1/1.26.2; no tracked .pth hooks)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
