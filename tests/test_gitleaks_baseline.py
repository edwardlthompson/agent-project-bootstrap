"""Gitleaks baseline allowlists documented sanitizer fixtures."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from gitleaks_baseline import check_repo  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


class GitleaksBaselineTests(unittest.TestCase):
    def test_repo_ok(self) -> None:
        self.assertEqual(check_repo(ROOT), [])

    def test_wired(self) -> None:
        text = (ROOT / "scripts" / "validate-bootstrap.sh").read_text(encoding="utf-8")
        self.assertIn("check-gitleaks-baseline.sh", text)

    def test_allowlist_excludes_sdk_paths(self) -> None:
        text = (ROOT / ".gitleaks.toml").read_text(encoding="utf-8")
        block = text.split("[allowlist]", 1)[1].split("\n[", 1)[0]
        for banned in ("Android/Sdk", "micromamba", ".local/android", "keystore"):
            self.assertNotIn(banned, block)


if __name__ == "__main__":
    unittest.main()
