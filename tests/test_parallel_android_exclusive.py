"""examples/android scopes are exclusive across parallel agents."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
sys.path.insert(0, str(LIB))
from parallel_scope_model import find_overlaps  # noqa: E402


class AndroidExclusiveTests(unittest.TestCase):
    def test_sibling_android_paths_conflict(self) -> None:
        errs = find_overlaps(
            [
                "examples/android/app/src/test",
                "examples/android/app/src/androidTest",
            ]
        )
        self.assertTrue(any("examples/android exclusive" in e for e in errs))

    def test_non_android_ok(self) -> None:
        self.assertEqual(
            find_overlaps(["examples/web/src", "examples/node/src"]),
            [],
        )


if __name__ == "__main__":
    unittest.main()
