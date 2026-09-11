"""Feedback clipboard schema + golden freeze."""

from __future__ import annotations

import json
import unittest
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
SCHEMA = ROOT / "schemas/golden-path/feedback-clipboard.schema.json"
GOLDEN = ROOT / "schemas/golden-path/feedback-clipboard.golden.json"


def _validate(instance: object, schema: dict) -> list[str]:
    errors: list[str] = []

    def walk(val: object, spec: dict, path: str) -> None:
        types = spec.get("type")
        if types is not None:
            allowed = types if isinstance(types, list) else [types]
            if val is None:
                ok = "null" in allowed
            elif isinstance(val, bool):
                ok = "boolean" in allowed
            elif isinstance(val, int) and not isinstance(val, bool):
                ok = "integer" in allowed or "number" in allowed
            elif isinstance(val, float):
                ok = "number" in allowed
            elif isinstance(val, str):
                ok = "string" in allowed
            elif isinstance(val, dict):
                ok = "object" in allowed
            else:
                ok = False
            if not ok:
                errors.append(f"{path}: type {type(val).__name__} not in {allowed}")
                return
        if "const" in spec and val != spec["const"]:
            errors.append(f"{path}: expected const {spec['const']!r}")
        if "enum" in spec and val not in spec["enum"]:
            errors.append(f"{path}: {val!r} not in enum")
        if spec.get("type") == "string" and isinstance(val, str):
            min_len = spec.get("minLength")
            if isinstance(min_len, int) and len(val) < min_len:
                errors.append(f"{path}: shorter than minLength")
        if spec.get("type") == "object" and isinstance(val, dict):
            for key in spec.get("required") or []:
                if key not in val:
                    errors.append(f"{path}: missing {key}")
            if spec.get("additionalProperties") is False:
                extra = set(val) - set((spec.get("properties") or {}))
                if extra:
                    errors.append(f"{path}: extra {sorted(extra)}")
            props = spec.get("properties") or {}
            for key, child in val.items():
                if key in props:
                    walk(child, props[key], f"{path}.{key}")

    walk(instance, schema, "$")
    return errors


class FeedbackClipboardSchemaTests(unittest.TestCase):
    def test_golden_matches_schema(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        golden = json.loads(GOLDEN.read_text(encoding="utf-8"))
        self.assertEqual(_validate(golden, schema), [])
        self.assertEqual(schema["required"], list(golden.keys()))

    def test_schema_freezes_version_one(self) -> None:
        schema = json.loads(SCHEMA.read_text(encoding="utf-8"))
        self.assertEqual(schema["properties"]["schemaVersion"]["const"], 1)


if __name__ == "__main__":
    unittest.main()
