""" /shape command registry, twins, and blank-line question format. """

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent


class ShapeCommandTests(unittest.TestCase):
    def test_shape_in_batch_registry(self) -> None:
        check = (ROOT / "scripts/check-batch-commands.sh").read_text(encoding="utf-8")
        self.assertIn("shape", check)
        self.assertRegex(check, r"PORTABLE=\([^)]*shape")

    def test_shape_files_exist(self) -> None:
        for rel in (
            ".cursor/commands/shape.md",
            "docs/help/SHAPE.md",
            ".clinerules/workflows/shape.md",
            "docs/specs/_TEMPLATE.md",
            "docs/PREFERENCES.md",
        ):
            self.assertTrue((ROOT / rel).is_file(), msg=rel)

    def test_blank_line_question_format(self) -> None:
        for rel in (".cursor/commands/shape.md", "docs/help/SHAPE.md"):
            text = (ROOT / rel).read_text(encoding="utf-8")
            self.assertIn("blank line", text.lower())
            self.assertIn("★", text)
            self.assertIn("defaults", text.lower())
            self.assertNotRegex(
                text,
                r"options a/b/c \(mark",
                msg=f"{rel} must not use cramped one-line a/b/c options",
            )

    def test_glossary_and_tour_mention_shape(self) -> None:
        glossary = (ROOT / "docs/help/GLOSSARY.md").read_text(encoding="utf-8")
        self.assertIn("/shape", glossary)
        self.assertIn("/ideas", glossary)
        self.assertIn("/coach", glossary)
        tour = (ROOT / "docs/help/TOUR.md").read_text(encoding="utf-8")
        self.assertIn("/shape", tour)
        cheat = (ROOT / "docs/help/BATCH_COMMANDS.md").read_text(encoding="utf-8")
        self.assertIn("/shape", cheat)


if __name__ == "__main__":
    unittest.main()
