"""ADR-0001 remains an open child architecture pick."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from adr_architecture import check_repo  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


class AdrArchitectureTests(unittest.TestCase):
    def test_repo(self) -> None:
        self.assertEqual(check_repo(ROOT), [])

    def test_wired(self) -> None:
        text = (ROOT / "scripts" / "validate-bootstrap.sh").read_text(encoding="utf-8")
        self.assertIn("check-adr-architecture.sh", text)

    def test_rejects_preselected_pattern(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            dest = root / "docs" / "adr"
            dest.mkdir(parents=True)
            src = (ROOT / "docs/adr/0001-core-architecture.md").read_text(encoding="utf-8")
            dest.joinpath("0001-core-architecture.md").write_text(
                src.replace("🔲 MVVM", "✅ MVVM"), encoding="utf-8"
            )
            (root / "docs" / "INITIALIZATION_PROMPT.md").write_text(
                "Draft ADR-0001 core architecture\n", encoding="utf-8"
            )
            errors = check_repo(root)
            self.assertTrue(any("pre-select" in e for e in errors))


if __name__ == "__main__":
    unittest.main()
