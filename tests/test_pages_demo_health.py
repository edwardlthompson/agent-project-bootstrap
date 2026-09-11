"""Pages demo URL must appear in README badges."""

from __future__ import annotations

import sys
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from pages_demo_health import check_readme, expected_pages_url  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


class PagesDemoHealthTests(unittest.TestCase):
    def test_expected_url(self) -> None:
        url = expected_pages_url(ROOT)
        self.assertIsNotNone(url)
        assert url is not None
        self.assertTrue(url.startswith("https://"))
        self.assertIn("github.io", url)

    def test_readme_links_demo(self) -> None:
        self.assertEqual(check_readme(ROOT), [])
        readme = (ROOT / "README.md").read_text(encoding="utf-8")
        self.assertIn("Pages-demo", readme)


if __name__ == "__main__":
    unittest.main()
