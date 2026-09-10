"""Print cheat sheet stays in sync with the batch command registry."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
ROOT = Path(__file__).resolve().parent.parent
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from batch_commands_print import check, load_commands, render  # noqa: E402
from batch_commands_print_audit import audit_html  # noqa: E402


class BatchCommandsPrintTests(unittest.TestCase):
    def test_committed_html_matches_render(self) -> None:
        check_script = (ROOT / "scripts/check-batch-commands.sh").read_text(encoding="utf-8")
        self.assertIn("batch_commands_print.py", check_script)
        cmds = load_commands(ROOT)
        html = render(cmds)
        for name in cmds:
            self.assertIn(f"/{name}", html)
        self.assertIn("/push", html)
        self.assertIn("/ship", html)
        self.assertIn('scope="col"', html)
        self.assertNotIn("atomic", html.lower())
        header = html.split("<h2", 1)[0]
        for banned in ("Theme", "donate", "About"):
            self.assertNotIn(banned.lower(), header.lower())
        self.assertEqual(audit_html(html, cmds), [])
        errors = check(ROOT, set(cmds))
        self.assertEqual(errors, [])

    def test_audit_requires_settings_only_captions(self) -> None:
        cmds = load_commands(ROOT)
        broken = dict(cmds)
        broken["tour"] = {**cmds["tour"], "caption": "A walkthrough."}
        errors = audit_html(render(cmds), broken)
        self.assertTrue(any("tour caption" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
