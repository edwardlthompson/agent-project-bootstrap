"""Linguist child attribution patterns and dominant-language gate."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from check_linguist_attribution import check, dominant_language  # noqa: E402
from linguist_attrs import PATTERNS, apply_linguist_attrs, render_block  # noqa: E402


class LinguistAttrsTests(unittest.TestCase):
    def test_patterns_include_tests_and_templates(self) -> None:
        self.assertIn("tests/** linguist-vendored", PATTERNS)
        self.assertIn("templates/** linguist-vendored", PATTERNS)

    def test_python_stack_comments_scripts_only(self) -> None:
        block = render_block(
            "python",
            "scripts/** linguist-vendored\ntests/** linguist-vendored\n",
        )
        self.assertIn("# scripts/** linguist-vendored", block)
        self.assertIn("tests/** linguist-vendored", block)
        self.assertNotIn("\nscripts/** linguist-vendored\n", "\n" + block)

    def test_apply_and_check_passes_for_web_product(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "templates" / "linguist").mkdir(parents=True)
            src = root / "templates" / "linguist" / "child.gitattributes"
            src.write_text(
                "\n".join(PATTERNS) + "\n",
                encoding="utf-8",
            )
            (root / "examples" / "web" / "src").mkdir(parents=True)
            (root / "examples" / "web" / "src" / "app.ts").write_text(
                "export {}\n", encoding="utf-8"
            )
            (root / "tests").mkdir()
            (root / "tests" / "test_x.py").write_text("def test():\n  pass\n", encoding="utf-8")
            (root / "scripts").mkdir()
            (root / "scripts" / "x.py").write_text("print(1)\n", encoding="utf-8")
            (root / "bootstrap.config.json").write_text(
                '{"project_name":"Demo","purpose":"app","stack":"web","profile":"full"}\n',
                encoding="utf-8",
            )
            apply_linguist_attrs(root, stack="web")
            code, msg = check(root)
            self.assertEqual(code, 0, msg)
            attrs = (root / ".gitattributes").read_text(encoding="utf-8")
            self.assertEqual(dominant_language(root, attrs), "TypeScript")


if __name__ == "__main__":
    unittest.main()
