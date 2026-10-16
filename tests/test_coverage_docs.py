"""Coverage docs and summarize helper exist."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class CoverageDocsTests(unittest.TestCase):
    def test_coverage_md(self) -> None:
        text = (ROOT / "docs/COVERAGE.md").read_text(encoding="utf-8")
        self.assertIn("Kover", text)
        self.assertIn("cov-fail-under", text)
        self.assertIn("optional", text.lower())

    def test_summarize_script(self) -> None:
        self.assertTrue((ROOT / "scripts/lib/summarize_coverage.py").is_file())
        self.assertTrue((ROOT / "scripts/summarize-coverage.sh").is_file())


if __name__ == "__main__":
    unittest.main()
