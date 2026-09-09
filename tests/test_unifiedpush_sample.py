"""UnifiedPush sample stays FOSS and is wired in the Android manifest."""

from __future__ import annotations

import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
PUSH = ROOT / "examples/android/app/src/main/java/dev/foss/goldenpath/push"
MANIFEST = ROOT / "examples/android/app/src/main/AndroidManifest.xml"
APP = ROOT / "examples/android/app/src/main/java/dev/foss/goldenpath/GoldenPathApplication.kt"


class UnifiedPushSampleTests(unittest.TestCase):
    def test_manifest_queries_and_receiver(self) -> None:
        text = MANIFEST.read_text(encoding="utf-8")
        self.assertIn("org.unifiedpush.android.distributor.REGISTER", text)
        self.assertIn("org.unifiedpush.android.connector.MESSAGE", text)
        self.assertIn(".push.UnifiedPushMessageReceiver", text)
        self.assertNotIn("com.google.firebase.MESSAGING_EVENT", text)

    def test_config_never_uses_proprietary_push(self) -> None:
        cfg = (PUSH / "UnifiedPushConfig.kt").read_text(encoding="utf-8")
        self.assertIn("fun usesProprietaryPush(): Boolean = false", cfg)
        self.assertIn("REGISTER_ACTION", cfg)
        app = APP.read_text(encoding="utf-8")
        self.assertIn("logUnifiedPush", app)
        blob = "\n".join(p.read_text(encoding="utf-8") for p in PUSH.glob("*.kt"))
        self.assertNotIn("firebase", blob.lower())
        self.assertNotIn("com.google.android.gms", blob)


if __name__ == "__main__":
    unittest.main()
