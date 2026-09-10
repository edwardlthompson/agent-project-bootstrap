"""Commercial Automations YAML is an example and stays disabled."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from cursor_automations import check_repo  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


class CursorAutomationsTests(unittest.TestCase):
    def test_repo(self) -> None:
        self.assertEqual(check_repo(ROOT), [])

    def test_wired(self) -> None:
        text = (ROOT / "scripts" / "validate-bootstrap.sh").read_text(encoding="utf-8")
        self.assertIn("check-cursor-automations.sh", text)

    def test_maintain_crons_stay_disabled(self) -> None:
        text = (ROOT / ".cursor" / "automations.commercial.example.yaml").read_text(
            encoding="utf-8"
        )
        self.assertIn("weekly-maintain", text)
        self.assertIn("monthly-dependabot-review", text)
        self.assertIn("enabled: false", text)


if __name__ == "__main__":
    unittest.main()
