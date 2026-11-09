"""Argus contract_version 2 loader and gate."""
from __future__ import annotations

import hashlib
import json
from pathlib import Path

CONTRACT_NAME = "argus.contract.json"


def load_contract(root: Path) -> dict | None:
    path = root / CONTRACT_NAME
    if not path.is_file():
        return None
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else None


def contract_body_hash(data: dict) -> str:
    """Stable hash excluding parent_hash (filled by children)."""
    payload = {k: v for k, v in data.items() if k != "parent_hash"}
    raw = json.dumps(payload, sort_keys=True, separators=(",", ":")).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def check(root: Path) -> tuple[int, str]:
    data = load_contract(root)
    if data is None:
        return 1, f"missing {CONTRACT_NAME}"
    version = data.get("contract_version")
    if version != 2:
        return 1, f"CONTRACT-STALE: expected contract_version 2, got {version!r}"
    required = data.get("required_files") or []
    missing = [rel for rel in required if not (root / rel).exists()]
    if missing:
        return 1, "CONTRACT-STALE: missing " + ", ".join(missing)
    parent = data.get("parent_hash")
    if parent is not None and parent != "":
        # Child claimed a parent cache; body must still be version 2 shape
        if not isinstance(parent, str) or len(parent) < 8:
            return 1, "CONTRACT-STALE: invalid parent_hash"
    return 0, f"OK: {CONTRACT_NAME} contract_version={version}"
