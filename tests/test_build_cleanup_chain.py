""" /build must mandatorily chain /cleanup and show a slim BUILD_PLAN. """

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class BuildCleanupChainTests(unittest.TestCase):
    def test_build_wrap_up_mandates_cleanup(self) -> None:
        text = (ROOT / ".cursor/commands/build.md").read_text(encoding="utf-8")
        self.assertIn("cleanup.md", text)
        wrap = text.split("## Wrap-up", 1)[-1]
        self.assertIn("cleanup", wrap.lower())
        self.assertRegex(wrap.lower(), r"never skip|mandatory")
        self.assertTrue(
            "slim" in wrap.lower()
            or "cleaned" in wrap.lower()
            or "**Now:**" in wrap
            or "Now:" in wrap,
            msg="Wrap-up must show slim/cleaned BUILD_PLAN / Now:",
        )
        self.assertIn("/cleanup", text)
        self.assertIn("together", text.lower())

    def test_cline_build_mentions_cleanup(self) -> None:
        text = (ROOT / ".clinerules/workflows/build.md").read_text(encoding="utf-8")
        self.assertIn("cleanup", text.lower())

    def test_cleanup_notes_build_chain(self) -> None:
        text = (ROOT / ".cursor/commands/cleanup.md").read_text(encoding="utf-8")
        self.assertIn("/build", text)


if __name__ == "__main__":
    unittest.main()
