"""validate-bootstrap --agent profile includes venue + encoding."""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class ValidateBootstrapAgentTests(unittest.TestCase):
    def test_agent_flag_in_script(self) -> None:
        text = (ROOT / "scripts/validate-bootstrap.sh").read_text(encoding="utf-8")
        self.assertIn("--agent)", text)
        self.assertIn('AGENT=true', text)
        # Core safety checks must stay in the agent profile
        agent_block = text.split('if [ "$AGENT" = true ]; then', 1)[1].split("elif !", 1)[0]
        for needle in (
            "check-file-encoding.sh",
            "check-agent-venue.sh",
            "check-repo-hygiene.sh",
            "check-ux-inventory.sh",
        ):
            self.assertIn(needle, agent_block)

    def test_precommit_uses_agent(self) -> None:
        cfg = (ROOT / ".pre-commit-config.yaml").read_text(encoding="utf-8")
        self.assertIn("validate-bootstrap.sh --agent", cfg)
        self.assertNotIn("validate-bootstrap.sh --quick", cfg)


if __name__ == "__main__":
    unittest.main()
