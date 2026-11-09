"""Brand icon and Argus Part 1 gate tests."""
from __future__ import annotations

import json
import shutil
import sys
import tempfile
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from brand_icon import TEMPLATE_STOCK_SHA256, check as brand_check  # noqa: E402
from argus_contract import check as contract_check  # noqa: E402
from ux_contract_gate import check as ux_check  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


class BrandIconTests(unittest.TestCase):
    def test_template_repo_passes(self) -> None:
        code, msg = brand_check(ROOT)
        self.assertEqual(code, 0, msg)

    def test_placeholder_fails(self) -> None:
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            (root / "branding" / "assets").mkdir(parents=True)
            icon = root / "branding" / "assets" / "app-icon-1024.png"
            icon.write_bytes(b"tiny")
            (root / "branding" / "brand.json").write_text(
                json.dumps(
                    {
                        "icon": "branding/assets/app-icon-1024.png",
                        "icon_sha256": "0" * 64,
                        "source": "owned",
                        "brand_name": "X",
                        "tokens": "config/tokens.json",
                    }
                ),
                encoding="utf-8",
            )
            code, msg = brand_check(root)
            self.assertEqual(code, 1)
            self.assertIn("PLACEHOLDER", msg)

    def test_contract_and_empty_ux_baseline(self) -> None:
        code, msg = contract_check(ROOT)
        self.assertEqual(code, 0, msg)
        code2, msg2 = ux_check(ROOT)
        self.assertEqual(code2, 0, msg2)
        self.assertIn("no baseline yet", msg2)


if __name__ == "__main__":
    unittest.main()
