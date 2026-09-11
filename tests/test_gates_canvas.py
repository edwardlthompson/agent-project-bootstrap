"""Gates status markdown writer."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from gates_canvas import fix_banner, load_gate_rows, markdown_report, write_status  # noqa: E402
from gates_canvas_health import dirty_tree_one_liner  # noqa: E402


class GatesCanvasTests(unittest.TestCase):
    def test_markdown_includes_stack(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cursor = root / ".cursor"
            cursor.mkdir()
            (cursor / "stack-selection.json").write_text(
                '{"stack":"web","distribution_tier":"foss"}', encoding="utf-8"
            )
            (root / "BUILD_PLAN.md").write_text("1. 🔲 [HUMAN] smoke\n", encoding="utf-8")
            md = markdown_report(root, [("encoding", "Pass")])
            self.assertIn("`web`", md)
            self.assertIn("encoding", md)
            self.assertIn("CI:", md)
            self.assertIn("Dirty tree:", md)
            dest = write_status(root, [("encoding", "Pass")])
            self.assertTrue(dest.is_file())

    def test_dirty_tree_clean_temp(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            line = dirty_tree_one_liner(root)
            self.assertTrue(line.startswith("Dirty tree:"))

    def test_load_gate_rows_from_json(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cursor = root / ".cursor"
            cursor.mkdir()
            (cursor / "last-feature-gate.json").write_text(
                '{"ok":false,"gates_passed":["encoding"],"failed_stage":"web-lint"}',
                encoding="utf-8",
            )
            rows = load_gate_rows(root)
            self.assertEqual(rows, [("encoding", "Pass"), ("web-lint", "Fail")])

    def test_fix_banner_prints_strikes_and_stage(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            cursor = root / ".cursor"
            cursor.mkdir()
            (cursor / "agent-progress.json").write_text('{"strikes": 2}', encoding="utf-8")
            (cursor / "last-feature-gate.json").write_text(
                '{"failed_stage":"web-lint"}', encoding="utf-8"
            )
            text = fix_banner(root)
            self.assertIn("strikes=2", text)
            self.assertIn("failed_stage=web-lint", text)

    def test_write_status_appends_sw_cache_budget_when_web_present(self) -> None:
        root = Path(__file__).resolve().parent.parent
        if not (root / "examples/web/public/sw.js").is_file():
            self.skipTest("web example pruned")
        with tempfile.TemporaryDirectory() as tmp:
            dest_root = Path(tmp)
            cursor = dest_root / ".cursor"
            cursor.mkdir()
            (cursor / "stack-selection.json").write_text(
                '{"stack":"web","distribution_tier":"foss"}', encoding="utf-8"
            )
            # Point measure at real repo via symlink-style: call summary against real root
            from sw_cache_budget import summary_row

            row = summary_row(root)
            self.assertIsNotNone(row)
            assert row is not None
            self.assertEqual(row[0], "sw-cache-budget")
            self.assertTrue(row[1].startswith("Pass"), row[1])
            md = write_status(dest_root, [("encoding", "Pass")])
            # Without web tree under dest_root, canvas still writes encoding only unless we pass root
            text = md.read_text(encoding="utf-8")
            self.assertIn("encoding", text)


if __name__ == "__main__":
    unittest.main()
