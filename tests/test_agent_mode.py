"""Agent mode load/set/convert (ADR-0010)."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from agent_mode import (  # noqa: E402
    convert_cloud_to_local,
    load_mode,
    write_mode,
)


class AgentModeTests(unittest.TestCase):
    def test_missing_file_is_balanced(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            info = load_mode(Path(tmp))
            self.assertEqual(info["mode"], "balanced")
            self.assertTrue(info["effective"])

    def test_write_and_load(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            write_mode(root, "lean", updated_by="test")
            info = load_mode(root)
            self.assertEqual(info["mode"], "lean")
            data = json.loads((root / ".cursor" / "agent-mode.json").read_text(encoding="utf-8"))
            self.assertEqual(data["updated_by"], "test")

    def test_convert_cloud_idempotent(self) -> None:
        text = "🔲 [AGENT][CLOUD] Do X — scope: src/\n🔲 [AGENT][LOCAL] Keep — scope: a/\n"
        once, n1 = convert_cloud_to_local(text)
        self.assertEqual(n1, 1)
        self.assertIn("[AGENT][LOCAL] Do X", once)
        twice, n2 = convert_cloud_to_local(once)
        self.assertEqual(n2, 0)
        self.assertEqual(once, twice)


if __name__ == "__main__":
    unittest.main()
