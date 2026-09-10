"""GlitchTip/Bugsink crash-inbox stub stays off the live FOSS path."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from crash_inbox import check_repo, check_stub  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


class CrashInboxTests(unittest.TestCase):
    def test_repo(self) -> None:
        self.assertEqual(check_repo(ROOT), [])

    def test_enabled_or_dsn_fails(self) -> None:
        self.assertTrue(check_stub({"enabled": True, "provider": "none"}, "x"))
        self.assertTrue(check_stub({"enabled": False, "provider": "glitchtip", "dsn": "https://x"}, "x"))
        self.assertEqual(check_stub({"enabled": False, "provider": "bugsink"}, "x"), [])

    def test_wired(self) -> None:
        text = (ROOT / "scripts" / "validate-bootstrap.sh").read_text(encoding="utf-8")
        self.assertIn("check-crash-inbox.sh", text)
        example = json.loads(
            (ROOT / "schemas/golden-path/crash-inbox.example.json").read_text(encoding="utf-8")
        )
        self.assertIs(example["enabled"], False)

    def test_missing_example_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            errors = check_repo(Path(tmp))
            self.assertTrue(any("crash-inbox.example.json" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
