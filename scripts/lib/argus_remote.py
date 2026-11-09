"""Remote console stub — no-op when disabled; never probes non-allow users."""
from __future__ import annotations

import json
import secrets
import time
from pathlib import Path

DESTRUCTIVE = frozenset({"release", "fleet execute", "revert"})


def load_config(root: Path) -> dict:
    path = root / "argus.remote.json"
    if not path.is_file():
        return {"enabled": False, "readonly": True, "allow": [], "card_ttl_s": 1800}
    data = json.loads(path.read_text(encoding="utf-8"))
    return data if isinstance(data, dict) else {"enabled": False}


def append_log(root: Path, line: str) -> None:
    log = root / "state" / "remote.log"
    log.parent.mkdir(parents=True, exist_ok=True)
    with log.open("a", encoding="utf-8") as fh:
        fh.write(line.rstrip() + "\n")


def status(root: Path) -> tuple[int, str]:
    cfg = load_config(root)
    enabled = bool(cfg.get("enabled"))
    readonly = bool(cfg.get("readonly", True))
    return (
        0,
        f"remote enabled={enabled} readonly={readonly} "
        f"transport={cfg.get('transport')} allow={len(cfg.get('allow') or [])}",
    )


def handle_command(root: Path, user_id: str, text: str) -> tuple[int, str]:
    cfg = load_config(root)
    if not cfg.get("enabled"):
        return 0, "remote disabled — no-op"
    allow = [str(x) for x in (cfg.get("allow") or [])]
    if user_id not in allow:
        # Ignored — no probe reply
        return 0, ""
    if cfg.get("readonly") and not text.strip().startswith("status"):
        return 0, "readonly: status/digest only until argus remote arm"
    verb = text.strip().lower()
    nonce = secrets.token_hex(8)
    ttl = int(cfg.get("card_ttl_s") or 1800)
    append_log(
        root,
        f"{int(time.time())} user={user_id} verb={verb!r} nonce={nonce} ttl={ttl}",
    )
    if any(verb.startswith(d) for d in DESTRUCTIVE):
        return 0, f"confirm destructive: repeat verb with nonce {nonce}"
    return 0, f"accepted nonce={nonce}"
