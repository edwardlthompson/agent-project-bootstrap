"""Web, Android, and CLI sanitizer fixtures must stay aligned."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sanitize_fixtures import check_repo  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


class SanitizeFixtureParityTests(unittest.TestCase):
    def test_repo(self) -> None:
        self.assertEqual(check_repo(ROOT), [])

    def test_wired(self) -> None:
        text = (ROOT / "scripts" / "validate-bootstrap.sh").read_text(encoding="utf-8")
        self.assertIn("check-sanitize-fixtures.sh", text)
        ci = (ROOT / ".github" / "workflows" / "ci.yml").read_text(encoding="utf-8")
        self.assertIn("sanitize-fixtures:", ci)
        self.assertIn("check-sanitize-fixtures.sh", ci)

    def test_missing_canon_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            errors = check_repo(Path(tmp))
            self.assertTrue(any("sanitize-fixtures.json" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
