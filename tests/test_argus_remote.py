"""Remote console disabled by default."""
from __future__ import annotations

import sys
import unittest
from pathlib import Path

LIB = Path(__file__).resolve().parent.parent / "scripts" / "lib"
ROOT = Path(__file__).resolve().parent.parent
if str(LIB) not in sys.path:
    sys.path.insert(0, str(LIB))

from argus_remote import handle_command, status  # noqa: E402


class RemoteTests(unittest.TestCase):
    def test_status_disabled(self) -> None:
        code, msg = status(ROOT)
        self.assertEqual(code, 0)
        self.assertIn("enabled=False", msg)

    def test_non_allow_silent(self) -> None:
        code, msg = handle_command(ROOT, "stranger", "release")
        self.assertEqual(code, 0)
        # disabled path returns no-op message; when enabled+non-allow returns ""
        self.assertTrue(msg == "" or "disabled" in msg)


if __name__ == "__main__":
    unittest.main()
