"""agent-framework 1.26.1/1.26.2 denylist + .pth hook scan."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
ROOT = Path(__file__).resolve().parent.parent
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from agent_framework_denylist import check_deps, check_pth_hooks, check_repo  # noqa: E402


class AgentFrameworkDenylistTests(unittest.TestCase):
    def test_repo_clean(self) -> None:
        self.assertEqual(check_repo(ROOT), [])

    def test_detects_bad_version(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "requirements.txt").write_text("agent-framework==1.26.1\n", encoding="utf-8")
            self.assertTrue(check_deps(root))

    def test_detects_pth(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            py = root / "examples" / "python"
            py.mkdir(parents=True)
            (py / "evil.pth").write_text("import os\n", encoding="utf-8")
            self.assertTrue(check_pth_hooks(root))

    def test_wired(self) -> None:
        text = (ROOT / "scripts" / "validate-bootstrap.sh").read_text(encoding="utf-8")
        self.assertIn("check-agent-framework-denylist.sh", text)


if __name__ == "__main__":
    unittest.main()
