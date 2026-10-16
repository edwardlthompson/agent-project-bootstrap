"""Tests for AGENT.md Product (do not drift) stamp and anti-amnesia gate."""
from __future__ import annotations

import json
import sys
import tempfile
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from agent_brief import BEGIN, EMPTY_NOTE, END, parse_brief, render_inner  # noqa: E402
from check_agent_brief import check  # noqa: E402
from stamp_product_brief import stamp_root  # noqa: E402

BRIEF = """# AGENT.md

<!-- agent-brief:one-liner -->
Photoreal Cycles icons from a locked seed, camera, and lighting.
<!-- /agent-brief:one-liner -->

<!-- agent-brief:keywords -->
camera, messages, tame, neon
<!-- /agent-brief:keywords -->

## Rules

- Seeded camera and lighting only.

## First milestone

Ship the factory QA gate.
"""

PLAN = f"""# Build Plan

### Product (do not drift)

{BEGIN}
{EMPTY_NOTE}
{END}
"""


class AgentBriefTests(unittest.TestCase):
    def test_parse_and_render_keywords(self) -> None:
        brief = parse_brief(BRIEF)
        inner = render_inner(brief)
        self.assertIn("Photoreal Cycles icons", inner)
        for word in ("camera", "messages", "tame", "neon"):
            self.assertIn(word, inner)
        self.assertIn("Read `AGENT.md`", inner)

    def test_check_fails_when_keywords_stripped(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENT.md.example").write_text("x", encoding="utf-8")
            (root / "AGENT.md").write_text(BRIEF, encoding="utf-8")
            (root / "bootstrap.config.json").write_text(
                json.dumps({"project_name": "demo", "purpose": "app", "stack": "web"}),
                encoding="utf-8",
            )
            (root / "BUILD_PLAN.md").write_text(
                PLAN.replace(EMPTY_NOTE, "Photoreal Cycles icons from a locked seed."),
                encoding="utf-8",
            )
            errors = check(root)
            self.assertTrue(any("tame" in e or "neon" in e for e in errors), errors)

    def test_stamp_then_check_passes(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENT.md.example").write_text("x", encoding="utf-8")
            (root / "AGENT.md").write_text(BRIEF, encoding="utf-8")
            (root / "bootstrap.config.json").write_text(
                json.dumps({"project_name": "demo", "purpose": "app", "stack": "web"}),
                encoding="utf-8",
            )
            (root / "BUILD_PLAN.md").write_text(PLAN, encoding="utf-8")
            (root / "docs").mkdir()
            (root / "docs" / "spec.md").write_text(
                f"# Spec\n{BEGIN}\n{EMPTY_NOTE}\n{END}\n", encoding="utf-8"
            )
            (root / "AGENT_MEMORY.md").write_text(
                f"# Mem\n{BEGIN}\n{EMPTY_NOTE}\n{END}\n", encoding="utf-8"
            )
            written = stamp_root(root)
            self.assertTrue(written)
            self.assertEqual(check(root), [])
            board = (root / "BUILD_PLAN.md").read_text(encoding="utf-8")
            self.assertIn("tame", board)
            self.assertIn("neon", board)
            self.assertEqual((root / "AGENT.md").read_text(encoding="utf-8"), BRIEF)

    def test_template_without_live_agent(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENT.md.example").write_text("x", encoding="utf-8")
            (root / "bootstrap.config.json").write_text(
                json.dumps(
                    {
                        "project_name": "agent-project-bootstrap",
                        "purpose": "GitHub Template for FOSS coding-agent projects",
                        "stack": "multi",
                    }
                ),
                encoding="utf-8",
            )
            (root / "BUILD_PLAN.md").write_text(PLAN, encoding="utf-8")
            self.assertEqual(check(root), [])

    def test_child_requires_agent_md(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENT.md.example").write_text("x", encoding="utf-8")
            (root / "bootstrap.config.json").write_text(
                json.dumps({"project_name": "demo", "purpose": "app", "stack": "web"}),
                encoding="utf-8",
            )
            errors = check(root)
            self.assertTrue(any("AGENT.md" in e for e in errors), errors)

    def test_about_must_echo_keywords_when_present(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENT.md.example").write_text("x", encoding="utf-8")
            (root / "AGENT.md").write_text(BRIEF, encoding="utf-8")
            (root / "bootstrap.config.json").write_text(
                json.dumps({"project_name": "demo", "purpose": "app", "stack": "web"}),
                encoding="utf-8",
            )
            stamped = render_inner(parse_brief(BRIEF))
            (root / "BUILD_PLAN.md").write_text(
                PLAN.replace(EMPTY_NOTE, stamped),
                encoding="utf-8",
            )
            branding = root / "branding"
            branding.mkdir()
            (branding / "product.json").write_text(
                json.dumps({"mode": "product", "name": "Demo"}),
                encoding="utf-8",
            )
            locale = root / "examples/web/src/locales"
            locale.mkdir(parents=True)
            (locale / "en.json").write_text(
                '{"app.title": "Golden Path PWA", "about.title": "About"}',
                encoding="utf-8",
            )
            errors = check(root)
            self.assertTrue(any("About/purpose" in e for e in errors), errors)
            (locale / "en.json").write_text(
                '{"app.title": "neon camera messages tame", "about.title": "About"}',
                encoding="utf-8",
            )
            self.assertEqual(check(root), [])

    def test_about_keywords_skipped_in_template_branding_mode(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "AGENT.md.example").write_text("x", encoding="utf-8")
            (root / "AGENT.md").write_text(BRIEF, encoding="utf-8")
            (root / "bootstrap.config.json").write_text(
                json.dumps({"project_name": "demo", "purpose": "app", "stack": "web"}),
                encoding="utf-8",
            )
            stamped = render_inner(parse_brief(BRIEF))
            (root / "BUILD_PLAN.md").write_text(
                PLAN.replace(EMPTY_NOTE, stamped),
                encoding="utf-8",
            )
            branding = root / "branding"
            branding.mkdir()
            (branding / "product.json").write_text(
                json.dumps({"mode": "template", "name": "Golden Path"}),
                encoding="utf-8",
            )
            locale = root / "examples/web/src/locales"
            locale.mkdir(parents=True)
            (locale / "en.json").write_text(
                '{"app.title": "Golden Path PWA", "about.title": "About"}',
                encoding="utf-8",
            )
            self.assertEqual(check(root), [])


if __name__ == "__main__":
    unittest.main()
