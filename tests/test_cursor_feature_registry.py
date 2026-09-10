"""CURSOR_FEATURE_REGISTRY.json stays current with shipped skills."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class CursorFeatureRegistryTests(unittest.TestCase):
    def test_skills_are_registered(self) -> None:
        data = json.loads((ROOT / "docs" / "CURSOR_FEATURE_REGISTRY.json").read_text(encoding="utf-8"))
        self.assertGreaterEqual(data.get("updated_at"), "2026-09-10")
        ids = {entry["id"] for entry in data["entries"]}
        skills = ROOT / ".cursor" / "skills"
        for path in skills.iterdir():
            if path.is_dir() and (path / "SKILL.md").is_file():
                self.assertIn(f"skills.{path.name}", ids)

    def test_entries_have_tier(self) -> None:
        data = json.loads((ROOT / "docs" / "CURSOR_FEATURE_REGISTRY.json").read_text(encoding="utf-8"))
        for entry in data["entries"]:
            self.assertIn("distribution_tier", entry, entry.get("id"))


if __name__ == "__main__":
    unittest.main()
