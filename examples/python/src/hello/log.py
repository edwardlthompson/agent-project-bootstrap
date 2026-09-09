"""Structured JSON logs and readiness (no PII)."""

from __future__ import annotations

import json
import sys


def ready_json() -> str:
    return json.dumps({"status": "ok"}, separators=(",", ":"))


def log_json(level: str, msg: str) -> str:
    return json.dumps({"level": level, "msg": msg}, separators=(",", ":"))


def log_event(level: str, msg: str) -> None:
    print(log_json(level, msg), file=sys.stderr)
