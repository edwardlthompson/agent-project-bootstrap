"""OpenAPI document and JSON log contract."""

from __future__ import annotations

import json

from hello.about import about_payload
from hello.log import ready_json
from hello.openapi import load_openapi, spec_paths


def test_openapi_lists_cli_paths() -> None:
    spec = load_openapi()
    assert spec["openapi"].startswith("3.")
    assert spec_paths() == ["/health", "/about", "/feedback"]


def test_about_payload_matches_spec_required() -> None:
    payload = about_payload()
    for key in ("version", "donate", "summary", "update"):
        assert key in payload
    assert json.loads(ready_json()) == {"status": "ok"}
