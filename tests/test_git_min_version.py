"""Git minimum version floor (2.56.1)."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
ROOT = Path(__file__).resolve().parent.parent
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from git_min_version import MIN, check_repo, parse_version  # noqa: E402


class GitMinVersionTests(unittest.TestCase):
    def test_parse(self) -> None:
        self.assertEqual(parse_version("git version 2.56.1.windows.1"), (2, 56, 1))
        self.assertEqual(parse_version("git version 2.45.0"), (2, 45, 0))
        self.assertIsNone(parse_version("not git"))

    def test_repo_ok_or_warn_only(self) -> None:
        # Host may be old; check_repo returns messages, does not raise.
        errors = check_repo(ROOT)
        self.assertIsInstance(errors, list)
        if not errors:
            self.assertGreaterEqual(MIN, (2, 56, 1))

    def test_wired(self) -> None:
        text = (ROOT / "scripts" / "validate-bootstrap.sh").read_text(encoding="utf-8")
        self.assertIn("check-git-min-version.sh", text)


if __name__ == "__main__":
    unittest.main()
