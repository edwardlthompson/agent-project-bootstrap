"""Release Please changelog types and RP workflow hygiene."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class ReleasePleaseHygieneTests(unittest.TestCase):
    def test_docs_and_chore_do_not_bump(self) -> None:
        cfg = json.loads((ROOT / "release-please-config.json").read_text(encoding="utf-8"))
        sections = {item["type"]: item for item in cfg["changelog-sections"]}
        self.assertIn("feat", sections)
        self.assertIn("fix", sections)
        # docs/chore/ci/test are path-filtered + hidden — no version bump noise
        for kind in ("docs", "chore", "ci", "test"):
            self.assertIn(kind, sections)
            self.assertTrue(sections[kind].get("hidden"), kind)
        self.assertIn("docs/**", cfg.get("exclude-paths") or [])

    def test_release_please_runs_dependency_review(self) -> None:
        text = (ROOT / ".github/workflows/release-please.yml").read_text(encoding="utf-8")
        self.assertIn("actions/dependency-review-action@v5", text)
        self.assertIn("checks: write", text)
        self.assertIn("name='Dependency Review'", text)

    def test_extra_files_include_template_version_and_plugin(self) -> None:
        cfg = json.loads((ROOT / "release-please-config.json").read_text(encoding="utf-8"))
        extras = cfg["packages"]["."]["extra-files"]
        by_path = {
            (item if isinstance(item, str) else item.get("path")): item for item in extras
        }
        tv = by_path.get(".template-version")
        self.assertIsInstance(tv, dict)
        self.assertEqual(tv.get("type"), "generic")
        idx = by_path.get("TEMPLATE_INDEX.json")
        self.assertIsInstance(idx, dict)
        self.assertEqual(idx.get("type"), "json")
        self.assertEqual(idx.get("jsonpath"), "$.template_version")
        plugin = by_path.get(".cursor-plugin/plugin.json")
        self.assertIsInstance(plugin, dict)
        self.assertEqual(plugin.get("type"), "json")
        self.assertEqual(plugin.get("jsonpath"), "$.version")
        workflow = (ROOT / ".github" / "workflows" / "release-please.yml").read_text(
            encoding="utf-8"
        )
        self.assertIn(".cursor-plugin/plugin.json", workflow)
        self.assertIn(".template-version", workflow)

    def test_session_state_json_gitignored(self) -> None:
        text = (ROOT / ".gitignore").read_text(encoding="utf-8")
        self.assertIn(".cursor-session-state.json", text)
        hygiene = (ROOT / "scripts/check-repo-hygiene.sh").read_text(encoding="utf-8")
        self.assertIn(".cursor-session-state.json", hygiene)


if __name__ == "__main__":
    unittest.main()
