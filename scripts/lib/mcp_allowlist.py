"""beforeMCPExecution server allowlist + pin checks (fail-open if config missing)."""
from __future__ import annotations

import json
import re
from pathlib import Path

ALLOWLIST = Path(".cursor") / "mcp-allowlist.json"
EXAMPLES = (
    Path(".cursor") / "mcp.foss.example",
    Path(".cursor") / "mcp.web.example",
    Path(".cursor") / "mcp.commercial.example",
)
# npm package with @version, or docker image with :tag (not :latest)
NPX_PIN = re.compile(r"^(?:@[^\s]+\/[^\s]+|[^\s@]+)@\d")
IMAGE_PIN = re.compile(r"^[^:\s]+:(?!latest$)[^\s]+$")


def load_allowlist(root: Path) -> dict:
    allow = root / ALLOWLIST
    if not allow.is_file():
        return {}
    try:
        data = json.loads(allow.read_text(encoding="utf-8"))
    except json.JSONDecodeError:
        return {}
    return data if isinstance(data, dict) else {}


def load_allowed(root: Path) -> set[str]:
    names: set[str] = set()
    data = load_allowlist(root)
    names.update(str(item).lower() for item in data.get("servers") or [])
    foss = root / EXAMPLES[0]
    if foss.is_file():
        try:
            cfg = json.loads(foss.read_text(encoding="utf-8"))
        except json.JSONDecodeError:
            cfg = {}
        names.update(str(key).lower() for key in (cfg.get("mcpServers") or {}))
    return names


def decide(payload: dict, root: Path) -> dict:
    server = str(payload.get("server") or payload.get("mcp_server") or "").strip()
    if not server:
        return {"permission": "allow"}
    allowed = load_allowed(root)
    if not allowed:
        return {"permission": "allow"}
    if server.lower() in allowed:
        return {"permission": "allow"}
    return {
        "permission": "deny",
        "user_message": f"MCP server '{server}' is not on the FOSS allowlist",
        "agent_message": "Add the server to .cursor/mcp-allowlist.json or use mcp.foss.example names.",
    }


def _npx_package(args: list) -> str | None:
    for arg in reversed(args):
        if not str(arg).startswith("-"):
            return str(arg)
    return None


def _check_server_entry(name: str, entry: dict, banned: set[str]) -> list[str]:
    if not isinstance(entry, dict):
        return [f"{name}: entry must be an object"]
    if entry.get("url"):
        return []
    errors: list[str] = []
    command = str(entry.get("command") or "").strip().lower()
    args = [str(a) for a in (entry.get("args") or [])]
    blob = " ".join(args).lower()
    errors.extend(f"{name}: banned package/image '{bad}'" for bad in banned if bad.lower() in blob)
    if command == "npx":
        pkg = _npx_package(args)
        if not pkg or not NPX_PIN.match(pkg):
            errors.append(f"{name}: pin npx package with @version (got {pkg!r})")
    elif command == "docker":
        image = args[-1] if args else ""
        if not image or not IMAGE_PIN.match(image):
            errors.append(f"{name}: pin docker image with :tag (not :latest)")
    elif command:
        errors.append(f"{name}: unsupported command {command!r} (use docker, npx, or url)")
    return errors


def check_examples(root: Path) -> list[str]:
    data = load_allowlist(root)
    banned = {str(x) for x in data.get("banned") or []}
    errors: list[str] = []
    for rel in EXAMPLES:
        path = root / rel
        if not path.is_file():
            errors.append(f"MISSING: {rel.as_posix()}")
            continue
        try:
            cfg = json.loads(path.read_text(encoding="utf-8"))
        except json.JSONDecodeError as exc:
            errors.append(f"{rel.as_posix()}: invalid JSON ({exc})")
            continue
        servers = cfg.get("mcpServers") or {}
        if not isinstance(servers, dict) or not servers:
            errors.append(f"{rel.as_posix()}: mcpServers must be a non-empty object")
            continue
        for name, entry in servers.items():
            errors.extend(_check_server_entry(f"{rel.as_posix()}:{name}", entry, banned))
    return errors


def check_repo(root: Path) -> list[str]:
    errors: list[str] = []
    if not (root / ALLOWLIST).is_file():
        return [f"MISSING: {ALLOWLIST.as_posix()}"]
    allowed = load_allowed(root)
    for name in ("github", "depsonar"):
        if name not in allowed:
            errors.append(f"allowlist must include {name}")
    data = load_allowlist(root)
    if "depsonar" not in (data.get("packages") or {}):
        errors.append("allowlist packages must pin depsonar")
    if "ghcr.io/github/github-mcp-server" not in (data.get("images") or {}):
        errors.append("allowlist images must pin ghcr.io/github/github-mcp-server")
    optional = data.get("optional_min_pins") or {}
    for pkg in ("@modelcontextprotocol/server-filesystem", "mcp-server-git", "mcp-server-fetch"):
        if pkg not in optional:
            errors.append(f"optional_min_pins must include {pkg}")
    if "decide" not in (root / ".cursor" / "hooks" / "mcp_audit.py").read_text(encoding="utf-8"):
        errors.append("mcp_audit.py must enforce the allowlist")
    errors.extend(check_examples(root))
    return errors


def main() -> int:
    errors = check_repo(Path.cwd())
    if errors:
        print("MCP allowlist check failed:")
        for item in errors:
            print(f"  {item}")
        return 1
    print("MCP allowlist check passed")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
