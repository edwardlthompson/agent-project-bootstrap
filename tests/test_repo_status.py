"""Repo status report headers (ADR-0010)."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from repo_status import render_status  # noqa: E402


class RepoStatusTests(unittest.TestCase):
    def test_report_headers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "BUILD_PLAN.md").write_text("# Plan\n", encoding="utf-8")
            report = render_status(root)
            for needle in (
                "Repo Status Report",
                "Agent mode:",
                "Distribution tier:",
                "Venue policy:",
                "Open BUILD_PLAN summary:",
                "Relevant ADRs:",
            ):
                self.assertIn(needle, report)
            self.assertIn("balanced", report)


if __name__ == "__main__":
    unittest.main()
