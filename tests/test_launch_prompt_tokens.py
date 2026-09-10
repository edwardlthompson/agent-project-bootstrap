"""Launch-prompt buttons must use design tokens for dark-mode contrast."""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class LaunchPromptTokenTests(unittest.TestCase):
    def test_web_launch_buttons_use_tokens(self) -> None:
        css = (ROOT / "examples/web/src/style.css").read_text(encoding="utf-8")
        self.assertIn(".gp-launch-actions button", css)
        block_start = css.index(".gp-launch-actions button {")
        block = css[block_start : block_start + 400]
        self.assertIn("var(--gp-color-surface-variant)", block)
        self.assertIn("var(--gp-color-on-surface-variant)", block)
        self.assertIn(".gp-launch-actions .gp-launch-accept", css)
        self.assertIn("var(--gp-color-on-primary)", css)


if __name__ == "__main__":
    unittest.main()
