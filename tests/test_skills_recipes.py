"""skills.sh recipes and shape-idea skill exist."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class SkillsRecipesTests(unittest.TestCase):
    def test_recipes_and_skill(self) -> None:
        recipes = (ROOT / "docs/SKILLS_RECIPES.md").read_text(encoding="utf-8")
        self.assertIn("tdd", recipes.lower())
        self.assertIn("grill-me", recipes.lower())
        skill = (ROOT / ".cursor/skills/shape-idea/SKILL.md").read_text(encoding="utf-8")
        self.assertIn("shape", skill.lower())
        self.assertIn("docs/specs", skill)


if __name__ == "__main__":
    unittest.main()
