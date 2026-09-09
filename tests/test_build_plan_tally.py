"""Remaining-item tally on BUILD_PLAN files."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
ROOT = Path(__file__).resolve().parent.parent
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from build_plan_tally import apply_tally, count_remaining, format_tally  # noqa: E402
from child_build_plan import install_child_build_plan  # noqa: E402


SAMPLE = """# Build Plan

<!-- remaining-tally -->
**Remaining:** AGENT 0 · AUTO 0 · HUMAN 0 · ADB 0 · **0 open**
<!-- /remaining-tally -->

### Sprint 0

1. 🔲 [AGENT] One
2. ✅ [AGENT] Done
3. 🔲 [HUMAN] Two
4. ❌ [ADB] Blocked

## Ongoing Maintenance

- 🔲 [AUTO] Weekly
"""


class TallyTests(unittest.TestCase):
    def test_counts_open_and_blocked(self) -> None:
        counts = count_remaining(SAMPLE)
        self.assertEqual(counts["AGENT"], 1)
        self.assertEqual(counts["HUMAN"], 1)
        self.assertEqual(counts["ADB"], 1)
        self.assertEqual(counts["AUTO"], 1)
        self.assertIn("AGENT 1", format_tally(counts))
        self.assertIn("**4 open**", format_tally(counts))

    def test_apply_updates_block(self) -> None:
        updated = apply_tally(SAMPLE)
        self.assertIn("AGENT 1", updated)
        self.assertIn("**4 open**", updated)

    def test_repo_plans_have_markers(self) -> None:
        for name in ("BUILD_PLAN.md", "BUILD_PLAN_TEMPLATE.md"):
            text = (ROOT / name).read_text(encoding="utf-8")
            self.assertIn("<!-- remaining-tally -->", text)
            self.assertNotIn("#### Sequential", text)

    def test_install_replaces_maintainer_board(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "bootstrap.config.json").write_text(
                '{"project_name":"notes","purpose":"Offline notes","stack":"web"}',
                encoding="utf-8",
            )
            src = (ROOT / "BUILD_PLAN_TEMPLATE.md").read_text(encoding="utf-8")
            (root / "BUILD_PLAN_TEMPLATE.md").write_text(src, encoding="utf-8")
            (root / "BUILD_PLAN.md").write_text(
                "# Build Plan\n## Template Maintainer\n1. 🔲 [AGENT] maintainer only\n",
                encoding="utf-8",
            )
            dest = install_child_build_plan(root)
            assert dest is not None
            text = dest.read_text(encoding="utf-8")
            self.assertIn("Sprint 0", text)
            self.assertNotIn("Template Maintainer", text)
            self.assertIn("<!-- remaining-tally -->", text)

    def test_install_skips_template_repo(self) -> None:
        self.assertIsNone(install_child_build_plan(ROOT))


if __name__ == "__main__":
    unittest.main()
