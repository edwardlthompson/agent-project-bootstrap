"""Settings export v1 schema and migration contract."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "schemas/golden-path/settings-bundle.schema.json"
WEB = ROOT / "examples/web/src/settings/migrate.ts"
ANDROID = ROOT / "examples/android/app/src/main/java/dev/foss/goldenpath/settings/SettingsExport.kt"


class SettingsBundleSchemaTests(unittest.TestCase):
    def test_schema_is_v1_theme_and_save_crashes(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual(schema["required"], ["version", "theme", "saveCrashes"])
        self.assertEqual(schema["properties"]["version"]["const"], 1)
        self.assertEqual(schema["properties"]["theme"]["enum"], ["system", "light", "dark"])

    def test_web_and_android_share_migrate_entry(self) -> None:
        if not WEB.is_file() or not ANDROID.is_file():
            self.skipTest("web or android example pruned")
        web = WEB.read_text(encoding="utf-8")
        android = ANDROID.read_text(encoding="utf-8")
        self.assertIn("export function migrateSettings", web)
        self.assertIn("fun migrate(", android)
        self.assertIn("darkMode", web)
        self.assertIn("darkMode", android)


if __name__ == "__main__":
    unittest.main()
