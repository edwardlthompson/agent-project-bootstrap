"""Radar writes a gitignored BUILD_PLAN draft and never touches BUILD_PLAN.md."""

from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from cursor_feature_radar_io import write_build_plan_draft  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


class RadarBuildPlanDraftTests(unittest.TestCase):
    def test_draft_uses_build_plan_markers(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_build_plan_draft(
                root,
                [
                    ("https://cursor.com/docs/agent/hooks", 9),
                    ("https://cursor.com/docs/cloud", 6),
                ],
            )
            text = (root / "CURSOR_RADAR_BUILD_PLAN_DRAFT.md").read_text(encoding="utf-8")
            self.assertIn("🔲 [AGENT]", text)
            self.assertIn("hooks", text)
            self.assertNotIn("cloud", text)
            self.assertFalse((root / "BUILD_PLAN.md").exists())

    def test_gitignore_and_docs(self) -> None:
        ignore = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn("CURSOR_RADAR_BUILD_PLAN_DRAFT.md", ignore)
        radar = (ROOT / "docs/CURSOR_FEATURE_RADAR.md").read_text(encoding="utf-8")
        self.assertIn("CURSOR_RADAR_BUILD_PLAN_DRAFT.md", radar)
        self.assertIn("never auto-edit `BUILD_PLAN.md`", radar)
        src = (ROOT / "scripts/lib/cursor_feature_radar.py").read_text(encoding="utf-8")
        self.assertIn("write_build_plan_draft", src)
        self.assertNotIn("BUILD_PLAN.md", src)


if __name__ == "__main__":
    unittest.main()
