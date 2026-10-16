"""Coach/build/feature pressure frequent commit + human /push."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class PushCadenceTests(unittest.TestCase):
    def test_nudge_and_no_silent_push(self) -> None:
        for rel in (
            ".cursor/commands/coach.md",
            ".cursor/commands/build.md",
            ".cursor/commands/feature.md",
            "docs/help/COACH.md",
            "docs/PREFERENCES.md",
        ):
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("/push", text)
            self.assertIn("commit", text.lower())
            self.assertIn("never silent", text.lower())


if __name__ == "__main__":
    unittest.main()
