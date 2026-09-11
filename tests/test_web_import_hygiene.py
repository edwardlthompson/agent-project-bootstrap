from __future__ import annotations

import sys
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
sys.path.insert(0, str(LIB))
from web_import_hygiene import check  # noqa: E402

ROOT = Path(__file__).resolve().parents[1]


class WebImportHygieneTests(unittest.TestCase):
    def test_repo_clean(self) -> None:
        self.assertEqual(check(ROOT), [])


if __name__ == "__main__":
    unittest.main()
