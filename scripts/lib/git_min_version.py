"""Warn (or fail in CI) when Git is older than the security floor (2.56.1)."""
from __future__ import annotations

import os
import re
import shutil
import subprocess
from pathlib import Path

MIN = (2, 56, 1)
VER_RE = re.compile(r"git version (\d+)\.(\d+)\.(\d+)")


def parse_version(text: str) -> tuple[int, int, int] | None:
    match = VER_RE.search(text)
    if not match:
        return None
    return int(match.group(1)), int(match.group(2)), int(match.group(3))


def git_version() -> tuple[int, int, int] | None:
    exe = shutil.which("git")
    if not exe:
        return None
    try:
        out = subprocess.check_output([exe, "--version"], text=True, timeout=10)
    except (OSError, subprocess.SubprocessError):
        return None
    return parse_version(out)


def in_ci() -> bool:
    return bool(os.environ.get("CI") or os.environ.get("GITHUB_ACTIONS"))


def check_repo(_root: Path | None = None) -> list[str]:
    ver = git_version()
    if ver is None:
        return ["git missing or version unreadable"]
    if ver >= MIN:
        return []
    floor = ".".join(str(x) for x in MIN)
    found = ".".join(str(x) for x in ver)
    return [
        f"Git {found} < {floor} — upgrade (CVE floor Nov 2026; "
        "https://github.blog/open-source/git/git-security-vulnerabilities-announced-7/)"
    ]


def automate_git_min_version(root: Path, _cfg: dict):
    """HUMAN row: host Git ≥ floor + checker wired into validate-bootstrap."""
    from human_task_core import AttemptResult

    if not (root / "scripts" / "check-git-min-version.sh").is_file():
        return AttemptResult(1, "git-min", "check-git-min-version.sh missing", True)
    if "check-git-min-version.sh" not in (root / "scripts" / "validate-bootstrap.sh").read_text(
        encoding="utf-8"
    ):
        return AttemptResult(1, "git-min", "validate-bootstrap missing git min check", True)
    ver = git_version()
    if ver is None:
        return AttemptResult(1, "git-min", "git missing or unreadable", True)
    if ver < MIN:
        floor = ".".join(str(x) for x in MIN)
        found = ".".join(str(x) for x in ver)
        return AttemptResult(1, "git-min", f"host Git {found} < {floor}; upgrade", True)
    return AttemptResult(0, "git-min", f"host Git {'.'.join(map(str, ver))} OK; checker wired", False)


def main() -> int:
    errors = check_repo(Path.cwd())
    if not errors:
        ver = git_version()
        print(f"OK: git {'.'.join(str(x) for x in ver)} >= {'.'.join(str(x) for x in MIN)}")
        return 0
    for item in errors:
        prefix = "FAIL" if in_ci() else "WARN"
        print(f"{prefix}: {item}")
    return 1 if in_ci() else 0


if __name__ == "__main__":
    raise SystemExit(main())
