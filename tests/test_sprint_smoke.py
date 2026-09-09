"""Sprint wrap smoke parser, probe map, and require lock."""
from __future__ import annotations

import json
import re
import sys
import tempfile
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from sprint_smoke import run  # noqa: E402
from sprint_smoke_map import infer_probes  # noqa: E402
from sprint_smoke_parse import find_sprint, parse_sprints  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent

PLAN = """# Build Plan

## Template Maintainer

### M50 — Chrome follow-through

1. ✅ [AGENT] Chrome + chip regression gate in `check-design-cohesion`
2. 🔲 [AGENT] Second locale catalog (web + Android)

### M51 — CLI / API

1. 🔲 [AGENT] Node GitHub feedback HTTP route

### Waiting on a person

1. 🔲 [HUMAN] CII Best Practices checklist (login + public badge)

## Child Repo Playbook (copy after Use this template)

### Sprint 2+ — Incremental Features

1. ✅ [AGENT] Copy feature spec
"""


class SprintSmokeTests(unittest.TestCase):
    def test_parse_ignores_human_leftovers(self) -> None:
        sprints = parse_sprints(PLAN)
        titles = [s.title for s in sprints]
        self.assertTrue(any(t.startswith("M50") for t in titles))
        self.assertTrue(any(t.startswith("Sprint 2") for t in titles))
        m50 = find_sprint(sprints, "M50")
        assert m50 is not None
        self.assertEqual(len(m50.items), 2)
        self.assertFalse(any(i.owner == "HUMAN" for i in m50.items))
        self.assertFalse(m50.complete)

    def test_infer_probes(self) -> None:
        self.assertIn("web", infer_probes("Chrome + chip regression gate"))
        self.assertIn("android", infer_probes("Android TalkBack + keyboard smoke"))
        self.assertIn("node", infer_probes("Node OpenAPI spec + contract tests"))
        self.assertIn("docs", infer_probes("Winget multi-arch docs"))

    def test_require_fails_when_open(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "BUILD_PLAN.md").write_text(PLAN, encoding="utf-8")
            ns = _ns(require=True, sprint="M50", dry_run=False)
            self.assertEqual(run(root, ns), 2)

    def test_if_complete_skips_open(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "BUILD_PLAN.md").write_text(PLAN, encoding="utf-8")
            ns = _ns(if_complete=True, sprint="M50")
            self.assertEqual(run(root, ns), 0)

    def test_dry_run_complete_child(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "BUILD_PLAN.md").write_text(PLAN, encoding="utf-8")
            ns = _ns(dry_run=True, sprint="Sprint 2")
            self.assertEqual(run(root, ns), 0)

    def test_require_passes_complete_sprint(self) -> None:
        done = """# Build Plan
### M99 — Done
1. ✅ [AGENT] Winget multi-arch docs
"""
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "BUILD_PLAN.md").write_text(done, encoding="utf-8")
            ns = _ns(require=True, sprint="M99")
            self.assertEqual(run(root, ns), 0)
            report = json.loads((root / ".cursor/sprint-smoke.json").read_text(encoding="utf-8"))
            self.assertTrue(report["ok"])
            self.assertEqual(len(report["items"]), 1)

    def test_board_queues_fifty_five(self) -> None:
        text = (ROOT / "BUILD_PLAN.md").read_text(encoding="utf-8")
        sprints = parse_sprints(text)
        queued = []
        for sprint in sprints:
            if sprint.title.startswith(("M51", "M52", "M53", "M54", "M55", "M56", "M57")):
                queued.extend(sprint.agent_auto)
        archived = _archived_idea_rows(
            (ROOT / "COMPLETED_TASKS.md").read_text(encoding="utf-8")
        )
        self.assertEqual(len(queued) + archived, 55)

    def test_build_and_gates_require_smoke(self) -> None:
        build = (ROOT / ".cursor/commands/build.md").read_text(encoding="utf-8")
        gates = (ROOT / ".cursor/commands/gates.md").read_text(encoding="utf-8")
        self.assertIn("smoke-sprint --require", build)
        self.assertIn("smoke-sprint", gates)


_IDEA_SPRINTS = tuple(f"M{n}" for n in range(51, 58))
_ARCHIVE_ROW = re.compile(r"^- ✅ \[(AGENT|AUTO)\]")


def _archived_idea_rows(text: str) -> int:
    count = 0
    active = False
    for line in text.splitlines():
        if line.startswith("## "):
            token = line[3:].split()[0]
            active = token in _IDEA_SPRINTS
            continue
        if active and _ARCHIVE_ROW.match(line):
            count += 1
    return count


def _ns(
    *,
    require: bool = False,
    if_complete: bool = False,
    dry_run: bool = False,
    sprint: str | None = None,
    with_feature_gate: bool = False,
):
    return type(
        "Args",
        (),
        {
            "require": require,
            "if_complete": if_complete,
            "dry_run": dry_run,
            "sprint": sprint,
            "with_feature_gate": with_feature_gate,
        },
    )()


class LiveWebSmokeTests(unittest.TestCase):
    def test_web_probe_records_load_order(self) -> None:
        from sprint_smoke_probes import load_budget
        from sprint_smoke_web import probe_web

        result = probe_web(ROOT, load_budget(ROOT))
        self.assertTrue(result.ok, result.detail)
        self.assertTrue(any("main.ts" in item for item in result.load_order))
        self.assertIsNotNone(result.startup_ms)


if __name__ == "__main__":
    unittest.main()
