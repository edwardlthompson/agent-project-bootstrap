"""Unit tests for init --profile memory hygiene under .agent/."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from init_profile import (  # noqa: E402
    apply_core_profile,
    check_profile,
    relocate_memory_logs,
    stamp_profile,
)


class InitProfileMemoryTests(unittest.TestCase):
    def test_relocate_moves_root_and_deletes_duplicate(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENT_MEMORY.md").write_text("# root mem\n", encoding="utf-8")
            (root / ".agent").mkdir()
            (root / ".agent" / "AGENT_MEMORY.md").write_text(
                "# agent mem\n", encoding="utf-8"
            )
            (root / "DECISION_LOG.md").write_text("# root log\n", encoding="utf-8")
            actions = relocate_memory_logs(root)
            self.assertFalse((root / "AGENT_MEMORY.md").exists())
            self.assertFalse((root / "DECISION_LOG.md").exists())
            self.assertEqual(
                (root / ".agent" / "AGENT_MEMORY.md").read_text(encoding="utf-8"),
                "# agent mem\n",
            )
            self.assertEqual(
                (root / ".agent" / "DECISION_LOG.md").read_text(encoding="utf-8"),
                "# root log\n",
            )
            self.assertTrue(any("remove root AGENT_MEMORY.md" in a for a in actions))

    def test_check_profile_rejects_root_memory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / ".agent").mkdir()
            (root / ".agent" / "AGENT_MEMORY.md").write_text("# ok\n", encoding="utf-8")
            stamp_profile(root, "full")
            (root / "AGENT_MEMORY.md").write_text("# bad\n", encoding="utf-8")
            code, msg = check_profile(root)
            self.assertEqual(code, 1)
            self.assertIn("root AGENT_MEMORY.md", msg)

    def test_core_profile_writes_only_agent_memory(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENT_MEMORY.md").write_text("# legacy\n", encoding="utf-8")
            (root / "docs").mkdir()
            (root / "docs" / "x.md").write_text("x", encoding="utf-8")
            apply_core_profile(root)
            self.assertFalse((root / "AGENT_MEMORY.md").exists())
            self.assertTrue((root / ".agent" / "AGENT_MEMORY.md").is_file())
            stamp_profile(root, "core")
            code, msg = check_profile(root)
            self.assertEqual(code, 0, msg)
            data = json.loads((root / "bootstrap.config.json").read_text(encoding="utf-8"))
            self.assertEqual(data.get("profile"), "core")


if __name__ == "__main__":
    unittest.main()
