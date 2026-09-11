"""WCAG contrast ratios for design tokens."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
ROOT = Path(__file__).resolve().parent.parent
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from token_contrast import check_repo, contrast_ratio  # noqa: E402


class TokenContrastTests(unittest.TestCase):
    def test_black_on_white(self) -> None:
        self.assertGreater(contrast_ratio("#000000", "#FFFFFF"), 20.0)

    def test_repo_tokens_meet_aa(self) -> None:
        self.assertEqual(check_repo(ROOT), [])

    def test_settings_dropdown_pairs_documented(self) -> None:
        from token_contrast import PAIRS

        self.assertIn(("onSurface", "surface", 4.5), PAIRS)
        css = (ROOT / "examples/web/src/style.css").read_text(encoding="utf-8")
        self.assertIn(".gp-settings-row select", css)
        self.assertIn("--gp-color-on-surface", css)
        self.assertIn("--gp-color-surface", css)


if __name__ == "__main__":
    unittest.main()
