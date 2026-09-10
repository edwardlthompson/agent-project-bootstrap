"""CI branch names and release tags must be sanitized."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from ci_refs import check_env, is_safe_ref, is_safe_tag  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


class CiRefsTests(unittest.TestCase):
    def test_safe_names(self) -> None:
        self.assertTrue(is_safe_ref("main"))
        self.assertTrue(is_safe_ref("cursor/openssf-best-practices-a6c6"))
        self.assertTrue(is_safe_tag("v1.1.0"))
        self.assertFalse(is_safe_ref("evil;rm -rf /"))
        self.assertFalse(is_safe_ref(".."))
        self.assertFalse(is_safe_tag("v1.1.0;wget"))

    def test_env(self) -> None:
        self.assertEqual(check_env({"GITHUB_REF_NAME": "main"}), [])
        self.assertTrue(check_env({"GITHUB_REF_NAME": "a$(id)"}))
        self.assertTrue(check_env({"INPUT_TAG": "v1;echo"}))

    def test_wired(self) -> None:
        ci = (ROOT / ".github/workflows/ci.yml").read_text(encoding="utf-8")
        release = (ROOT / ".github/workflows/release.yml").read_text(encoding="utf-8")
        self.assertIn("check-ci-refs.sh", ci)
        self.assertIn("check-ci-refs.sh", release)
        boot = (ROOT / "scripts/validate-bootstrap.sh").read_text(encoding="utf-8")
        self.assertIn("check-ci-refs.sh", boot)
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn(
            "[![OpenSSF Best Practices](https://www.bestpractices.dev/projects/14564/badge)]"
            "(https://www.bestpractices.dev/projects/14564)",
            readme,
        )


if __name__ == "__main__":
    unittest.main()
