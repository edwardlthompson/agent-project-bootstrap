"""Canvas / Design Mode walkthrough stays complete."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from cursor_canvas import check_repo  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


class CursorCanvasTests(unittest.TestCase):
    def test_repo(self) -> None:
        self.assertEqual(check_repo(ROOT), [])

    def test_wired(self) -> None:
        boot = (ROOT / "scripts" / "validate-bootstrap.sh").read_text(encoding="utf-8")
        self.assertIn("check-cursor-canvas.sh", boot)
        modes = (ROOT / "docs" / "CURSOR_MODES.md").read_text(encoding="utf-8")
        self.assertIn("CURSOR_CANVAS.md", modes)


if __name__ == "__main__":
    unittest.main()
