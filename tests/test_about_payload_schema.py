"""Shared About/donate/update JSON contract for CLI stacks."""
from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "schemas/golden-path/about-payload.schema.json"


def validate_payload(data: object) -> list[str]:
    errors: list[str] = []
    if not isinstance(data, dict):
        return ["payload must be an object"]
    for key in ("version", "donate", "summary", "update"):
        if key not in data:
            errors.append(f"missing {key}")
    if not isinstance(data.get("version"), str) or not data.get("version"):
        errors.append("version must be a non-empty string")
    donate = data.get("donate")
    if not isinstance(donate, str) or not donate.startswith("http"):
        errors.append("donate must be an http(s) URL")
    if not isinstance(data.get("summary"), str) or not data.get("summary"):
        errors.append("summary must be a non-empty string")
    update = data.get("update")
    if not isinstance(update, dict):
        errors.append("update must be an object")
        return errors
    if update.get("status") not in {"current", "available", "unknown"}:
        errors.append("update.status must be current|available|unknown")
    if "version" not in update or "url" not in update:
        errors.append("update needs version and url (nullable)")
    return errors


class AboutPayloadSchemaTests(unittest.TestCase):
    def test_schema_lists_required_fields(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual(schema["required"], ["version", "donate", "summary", "update"])
        self.assertEqual(schema["properties"]["update"]["required"], ["status", "version", "url"])

    def test_current_stub_payload_passes(self) -> None:
        payload = {
            "version": "0.1.0",
            "donate": "https://github.com/sponsors",
            "summary": "golden-path 0.1.0 donate https://github.com/sponsors",
            "update": {"status": "current", "version": None, "url": None},
        }
        self.assertEqual(validate_payload(payload), [])

    def test_rejects_missing_update(self) -> None:
        self.assertTrue(validate_payload({"version": "1", "donate": "https://x", "summary": "s"}))


if __name__ == "__main__":
    unittest.main()
