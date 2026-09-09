"""Golden Path Lightroom stub registers a second Lr* factory."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
INFO = ROOT / "examples/lightroom/Info.lua"
VERIFY = ROOT / "scripts/verify-lightroom.sh"


class LightroomSecondEntryTests(unittest.TestCase):
    def test_info_registers_export_and_tagset(self) -> None:
        text = INFO.read_text(encoding="utf-8")
        self.assertIn("LrExportServiceProvider", text)
        self.assertIn("LrMetadataTagsetFactory", text)
        self.assertIn("MetadataTagset.lua", text)

    def test_verify_script_requires_tagset(self) -> None:
        text = VERIFY.read_text(encoding="utf-8")
        self.assertIn("LrMetadataTagsetFactory", text)
        self.assertIn("MetadataTagset.lua", text)


if __name__ == "__main__":
    unittest.main()
