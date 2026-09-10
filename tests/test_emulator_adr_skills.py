"""Companion skills exist for /emulator and /adr."""
from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class EmulatorAdrSkillsTests(unittest.TestCase):
    def test_skill_files(self) -> None:
        for name in ("emulator", "adr"):
            path = ROOT / ".cursor" / "skills" / name / "SKILL.md"
            text = path.read_text(encoding="utf-8")
            self.assertIn("See also:", text)
            cmd = (ROOT / ".cursor" / "commands" / f"{name}.md").read_text(encoding="utf-8")
            self.assertIn(f".cursor/skills/{name}/", cmd)

    def test_integrations_lists_skills(self) -> None:
        text = (ROOT / "scripts" / "lib" / "check_cursor_integrations.py").read_text(encoding="utf-8")
        self.assertIn('"emulator"', text)
        self.assertIn('"adr"', text)


if __name__ == "__main__":
    unittest.main()
