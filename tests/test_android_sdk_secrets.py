"""local.properties / SDK path secret scanning."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from android_sdk_secrets import check_repo  # noqa: E402

ROOT = Path(__file__).resolve().parent.parent


class AndroidSdkSecretsTests(unittest.TestCase):
    def test_repo(self) -> None:
        self.assertEqual(check_repo(ROOT), [])

    def test_gitleaks_rules(self) -> None:
        text = (ROOT / ".gitleaks.toml").read_text(encoding="utf-8")
        self.assertIn("android-local-properties-sdk-dir", text)
        self.assertIn("local.properties", text)
        validate = (ROOT / "scripts/validate-bootstrap.sh").read_text(encoding="utf-8")
        self.assertIn("check-android-sdk-secrets.sh", validate)


if __name__ == "__main__":
    unittest.main()
