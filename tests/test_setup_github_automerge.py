"""setup-github-repo.sh wires optional AUTOMERGE_TOKEN without failing setup."""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SETUP = ROOT / "scripts" / "setup-github-repo.sh"


class SetupGithubAutomergeTests(unittest.TestCase):
    def test_setup_script_wires_automerge_helper(self) -> None:
        text = SETUP.read_text(encoding="utf-8")
        self.assertIn("AUTOMERGE_TOKEN", text)
        self.assertIn("SETUP_AUTOMERGE_TOKEN", text)
        self.assertIn("setup-automerge-token.sh", text)
        self.assertIn("maybe_setup_automerge_token", text)
        self.assertIn("NOTE Optional AUTOMERGE_TOKEN not set", text)
        self.assertIn("return 0", text.split("maybe_setup_automerge_token()")[1][:800])

    def test_helper_script_exists(self) -> None:
        helper = ROOT / "scripts" / "setup-automerge-token.sh"
        self.assertTrue(helper.is_file())
        self.assertIn("AUTOMERGE_TOKEN", helper.read_text(encoding="utf-8"))


if __name__ == "__main__":
    unittest.main()
