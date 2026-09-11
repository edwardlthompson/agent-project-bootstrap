"""Golden Path About payload parity with shared schemas (About slice present)."""

from __future__ import annotations

import json
from pathlib import Path

from hello.about import APP_VERSION, about_payload

ROOT = Path(__file__).resolve().parents[3]
SCHEMA_DIR = ROOT / "schemas" / "golden-path"


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
            elif isinstance(val, list):
                ok = "array" in allowed
            elif isinstance(val, dict):
                ok = "object" in allowed
            else:
                ok = False
            if not ok:
                errors.append(f"{path}: type {type(val).__name__} not in {allowed}")
                return
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
                extra = set(val) - set(spec.get("properties") or {})
                if extra:
                    errors.append(f"{path}: extra {sorted(extra)}")
            props = spec.get("properties") or {}
            for key, child in val.items():
                if key in props:
                    walk(child, props[key], f"{path}.{key}")

    walk(instance, schema, "$")
    return errors


def test_about_payload_matches_shared_schema() -> None:
    schema = json.loads((SCHEMA_DIR / "about-payload.schema.json").read_text(encoding="utf-8"))
    assert _validate(about_payload(), schema) == []


def test_about_version_matches_app_version_sot() -> None:
    sot = json.loads((SCHEMA_DIR / "app-version.json").read_text(encoding="utf-8"))
    assert APP_VERSION == sot["version"]
    assert about_payload()["version"] == sot["version"]


def test_about_golden_fixture() -> None:
    about_golden = {
        "version": APP_VERSION,
        "donate": "https://github.com/sponsors",
        "summary": f"golden-path {APP_VERSION} donate https://github.com/sponsors",
        "update": {"status": "current", "version": None, "url": None},
    }
    assert about_payload() == about_golden
