"""Required vs informational check map."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
LIB = ROOT / "scripts" / "lib"
sys.path.insert(0, str(LIB))
from required_checks import load_informational, load_names  # noqa: E402


class RequiredChecksMapTests(unittest.TestCase):
    def test_map_doc_exists(self) -> None:
        self.assertTrue((ROOT / "docs/CI_REQUIRED_CHECKS.md").is_file())
        self.assertIn("CI", load_names(ROOT))
        info = load_informational(ROOT)
        self.assertTrue(info)
        self.assertTrue(any("SBOM" in x for x in info))


if __name__ == "__main__":
    unittest.main()
