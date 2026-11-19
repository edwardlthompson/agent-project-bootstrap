"""Detect wfx-loot IOCs and require npm ci --ignore-scripts in CI workflows."""
from __future__ import annotations

import json
import re
from pathlib import Path

CI_SCRIPT = re.compile(r"^\.ci-[a-z0-9]+\.sh$", re.I)
BUILD_AUDIT = re.compile(r"^build-audit-[a-z0-9_-]+\.ya?ml$", re.I)
HOOK_PAYLOAD = re.compile(r"\.ci-[a-z0-9]+\.sh|exit\s+42", re.I)
RESTORE_CACHE = re.compile(r"Restore cache\s+\w+", re.I)
PASS_RUNTIME = re.compile(r"Pass runtime", re.I)
NPM_CI = re.compile(r"\bnpm\s+ci\b")
IGNORE = re.compile(r"--ignore-scripts\b")
PKG_DIRS = ("", "examples/web", "examples/node")


def _scan_package_hooks(root: Path) -> list[str]:
    errors: list[str] = []
    for rel in PKG_DIRS:
        path = root / rel / "package.json" if rel else root / "package.json"
        if not path.is_file():
            continue
        try:
            data = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            continue
        scripts = data.get("scripts") or {}
        if not isinstance(scripts, dict):
            continue
        for name, cmd in scripts.items():
            text = str(cmd)
            if HOOK_PAYLOAD.search(text):
                errors.append(f"{path.relative_to(root).as_posix()} scripts.{name}: wfx-loot hook pattern")
    return errors


def check_iocs(root: Path) -> list[str]:
    errors: list[str] = []
    if (root / "docs" / "wfx-audit.md").is_file():
        errors.append("IOC: docs/wfx-audit.md present (wfx-docs probe)")
    for path in root.glob(".ci-*.sh"):
        if CI_SCRIPT.match(path.name):
            errors.append(f"IOC: {path.name} (npm-hook payload script)")
    wf = root / ".github" / "workflows"
    if wf.is_dir():
        for path in wf.iterdir():
            if path.is_file() and BUILD_AUDIT.match(path.name):
                errors.append(f"IOC: .github/workflows/{path.name}")
            if not path.is_file() or path.suffix not in {".yml", ".yaml"}:
                continue
            text = path.read_text(encoding="utf-8", errors="replace")
            if RESTORE_CACHE.search(text) and PASS_RUNTIME.search(text):
                errors.append(f"IOC: {path.relative_to(root).as_posix()} Restore cache + Pass runtime steps")
    errors.extend(_scan_package_hooks(root))
    return errors


def check_npm_ci_ignore_scripts(root: Path) -> list[str]:
    errors: list[str] = []
    wf = root / ".github" / "workflows"
    if not wf.is_dir():
        return ["MISSING: .github/workflows"]
    for path in sorted(wf.glob("*.yml")) + sorted(wf.glob("*.yaml")):
        for i, line in enumerate(path.read_text(encoding="utf-8", errors="replace").splitlines(), 1):
            if not NPM_CI.search(line):
                continue
            if IGNORE.search(line):
                continue
            rel = path.relative_to(root).as_posix()
            errors.append(f"{rel}:{i}: npm ci must use --ignore-scripts (wfx-loot npm-hook bypass)")
    return errors


def check_repo(root: Path) -> list[str]:
    return check_iocs(root) + check_npm_ci_ignore_scripts(root)


def main() -> int:
    errors = check_repo(Path.cwd())
    if errors:
        print("wfx-loot / npm ci check failed:")
        for item in errors:
            print(f"  {item}")
        return 1
    print("wfx-loot IOC scan clean; CI npm ci uses --ignore-scripts")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
