"""TEMPLATE_INDEX project card matches AGENTS.md."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from project_card_index import check_repo, parse_agents_card  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


class ProjectCardIndexTests(unittest.TestCase):
    def test_repo(self) -> None:
        self.assertEqual(check_repo(ROOT), [])

    def test_parse(self) -> None:
        text = (
            "<!-- bootstrap-project-card -->\n"
            "**Product:** demo\n**Purpose:** demo purpose\n**Stack:** web\n"
            "<!-- /bootstrap-project-card -->\n"
        )
        self.assertEqual(
            parse_agents_card(text),
            {"name": "demo", "purpose": "demo purpose", "stack": "web"},
        )


if __name__ == "__main__":
    unittest.main()
