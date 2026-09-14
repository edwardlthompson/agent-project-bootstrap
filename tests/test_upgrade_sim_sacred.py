"""Upgrade sim never lists Sacred child files in cherry-pick AREAS."""
from __future__ import annotations

import re
from pathlib import Path
import unittest

ROOT = Path(__file__).resolve().parent.parent
SCRIPT = ROOT / "scripts" / "simulate-template-upgrade.sh"
SACRED = (
    "AGENTS.md",
    "AGENT.md",
    "docs/spec.md",
    "docs/plan.md",
    "docs/INITIALIZATION_PROMPT.md",
)


class UpgradeSimSacredTests(unittest.TestCase):
    def test_areas_skip_sacred_and_assert_marker(self) -> None:
        text = SCRIPT.read_text(encoding="utf-8")
        match = re.search(r"AREAS=\((.*?)\)", text, re.S)
        self.assertIsNotNone(match)
        areas = match.group(1)
        for path in SACRED:
            self.assertNotIn(path, areas)
        self.assertIn("upgrade-sim-sacred-agents-md", text)
        self.assertIn("upgrade-sim-sacred-agent-md", text)
        self.assertIn("Sacred AGENTS.md was overwritten", text)
        self.assertIn("Sacred AGENT.md was overwritten", text)
        self.assertIn("env -u CI -u GITHUB_ACTIONS", text)
        self.assertIn("child_quick", text)
        self.assertIn("BOOTSTRAP_UPGRADE_SIM=1", text)

    def test_blender_icon_factory_skips_when_example_pruned(self) -> None:
        text = (ROOT / "tests/test_blender_icon_factory.py").read_text(encoding="utf-8")
        self.assertIn('raise unittest.SkipTest("blender example pruned")', text)
        self.assertLess(text.index("SkipTest"), text.index("from cli import"))


if __name__ == "__main__":
    unittest.main()
