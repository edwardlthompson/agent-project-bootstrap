"""BUILD_PLAN → feature-spec stub generator."""
from __future__ import annotations

import sys
import tempfile
import unittest
from pathlib import Path
from unittest import mock

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

import gen_feature_spec as gfs  # noqa: E402


class GenFeatureSpecTests(unittest.TestCase):
    def test_slugify_strips_issue(self) -> None:
        self.assertEqual(gfs.slugify("Foo bar (#174)"), "foo-bar")

    def test_render_includes_source(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            tmpl = root / "docs" / "features"
            tmpl.mkdir(parents=True)
            (tmpl / "_template.md").write_text(
                "# Feature: {name}\n\n## Notes\n\n- x\n", encoding="utf-8"
            )
            with mock.patch.object(gfs, "ROOT", root), mock.patch.object(
                gfs, "TEMPLATE", tmpl / "_template.md"
            ):
                body = gfs.render("Nav persist (#196)", "nav-persist")
        self.assertIn("nav-persist", body)
        self.assertIn("Source BUILD_PLAN row", body)
        self.assertIn("Nav persist (#196)", body)


if __name__ == "__main__":
    unittest.main()
