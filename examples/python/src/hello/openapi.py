"""Load the Golden Path Python OpenAPI document."""

from __future__ import annotations

import json
from pathlib import Path
from typing import Any, cast

SPEC_PATH = Path(__file__).resolve().parents[2] / "openapi.json"


def load_openapi() -> dict[str, Any]:
    data: object = json.loads(SPEC_PATH.read_text(encoding="utf-8"))
    if not isinstance(data, dict):
        raise TypeError("openapi.json must be an object")
    return cast(dict[str, Any], data)


def spec_paths() -> list[str]:
    paths = load_openapi().get("paths")
    if not isinstance(paths, dict):
        return []
    return list(paths)
