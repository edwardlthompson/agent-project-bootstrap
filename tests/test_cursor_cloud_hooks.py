"""Commercial Cloud hook merge keeps FOSS beforeShellExecution + afterFileEdit."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from cursor_cloud_hooks import check_repo, merge_hooks  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


class CursorCloudHooksTests(unittest.TestCase):
    def test_repo(self) -> None:
        self.assertEqual(check_repo(ROOT), [])

    def test_merge_keeps_foss_and_adds_cloud(self) -> None:
        merged = merge_hooks(
            {"version": 1, "hooks": {"beforeShellExecution": [{"command": "foss"}]}},
            {"hooks": {"afterAgentResponse": [{"command": "cloud"}]}},
        )
        self.assertEqual(merged["hooks"]["beforeShellExecution"][0]["command"], "foss")
        self.assertEqual(merged["hooks"]["afterAgentResponse"][0]["command"], "cloud")

    def test_wired(self) -> None:
        text = (ROOT / "scripts" / "validate-bootstrap.sh").read_text(encoding="utf-8")
        self.assertIn("check-cursor-cloud-hooks.sh", text)


if __name__ == "__main__":
    unittest.main()
