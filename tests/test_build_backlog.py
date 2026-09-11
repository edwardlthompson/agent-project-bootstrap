"""HUMAN_BACKLOG add/remove helpers."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from build_backlog import HEADER, add_item, remove_item  # noqa: E402


class BuildBacklogTests(unittest.TestCase):
    def test_add_and_remove(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "HUMAN_BACKLOG.md").write_text(HEADER, encoding="utf-8")
            self.assertTrue(add_item(root, "ADB", "nav smoke", "Waiting", "device"))
            self.assertFalse(add_item(root, "ADB", "nav smoke", "Waiting", "again"))
            self.assertTrue(remove_item(root, "ADB", "nav smoke", "Waiting"))
            self.assertFalse(remove_item(root, "ADB", "nav smoke", "Waiting"))


if __name__ == "__main__":
    unittest.main()
