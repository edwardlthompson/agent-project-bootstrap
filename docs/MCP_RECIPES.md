# MCP recipes (opt-in)

Copy examples into gitignored `.cursor/mcp.json` only after you choose servers. FOSS allowlist: [`.cursor/mcp-allowlist.json`](../.cursor/mcp-allowlist.json). Never commit live `mcp.json` or tokens.

## Pin policy (required)

- Never use unpinned `npx -y <package>` — always `@exact.version` (malware lure: [GHSA-72xc-q3v8-7grp](https://github.com/advisories/GHSA-72xc-q3v8-7grp)).
- Do **not** install `mcp-server-github` or `@modelcontextprotocol/server-github` (deprecated / malware advisories). Use the official Docker image `ghcr.io/github/github-mcp-server:<tag>`.
- Keep pins in [`.cursor/mcp-allowlist.json`](../.cursor/mcp-allowlist.json) (`packages`, `images`, `banned`) in sync with the example files. Gate: `scripts/check-mcp-allowlist.sh`.

## FOSS baseline

| Server | Role | Example |
|--------|------|---------|
| `github` | Issues/PRs (Docker, pinned tag) | [`.cursor/mcp.foss.example`](../.cursor/mcp.foss.example) |
| `depsonar` | Dependency insight (`depsonar@4.1.0`) | same |

Activation: [`CURSOR_INTEGRATIONS.md`](CURSOR_INTEGRATIONS.md). Requires Docker for the GitHub MCP image.

## Per-stack suggestions

| Stack | Recommended | Notes |
|-------|-------------|-------|
| web | Cursor browser / DevTools MCP; docs-lookup (Context7) | Context7 is **user-added** until FOSS-reviewed — do not allowlist blindly |
| android | github + depsonar | Prefer local emulator skill over cloud-only tools |
| node | github + depsonar | Same baseline |
| python | github + depsonar | Same baseline |
| Next.js apps | Same as web + framework docs MCP | **Not** a Golden Path in this template — recipe only |

## Reference servers (filesystem / git / fetch) — audit

**Template audit (2026-11-19):** FOSS examples ([`mcp.foss.example`](../.cursor/mcp.foss.example), [`mcp.web.example`](../.cursor/mcp.web.example)) and the FOSS allowlist **do not** ship `@modelcontextprotocol/server-filesystem`, `mcp-server-git`, `mcp-server-fetch`, or `server-everything`. Children that add them must pin patched releases — do not use date-versioned npm installs without an explicit `@2.x` pin (semver ranks below `2025.*` / `2026.*`).

| Package | Registry | Minimum pin | Advisories |
|---------|----------|-------------|------------|
| `@modelcontextprotocol/server-filesystem` | npm | `2.4.0` | [v2.4.0](https://github.com/modelcontextprotocol/servers/releases/tag/v2.4.0) + [v2.5.0](https://github.com/modelcontextprotocol/servers/releases/tag/v2.5.0) |
| `mcp-server-git` | PyPI | `2026.11.18` | same |
| `mcp-server-fetch` | PyPI | `2026.11.18` | [v2.4.0](https://github.com/modelcontextprotocol/servers/releases/tag/v2.4.0) (SSRF/robots) + later fetch pins |
| `@modelcontextprotocol/server-everything` | npm | `2.3.1` | [v2.5.0](https://github.com/modelcontextprotocol/servers/releases/tag/v2.5.0) (NAT64) |

Opt-in snippets (not on the FOSS allowlist — add only after review):

```json
{
  "filesystem": {
    "command": "npx",
    "args": ["-y", "@modelcontextprotocol/server-filesystem@2.4.0", "/absolute/allowed/dir"]
  },
  "git": {
    "command": "uvx",
    "args": ["mcp-server-git==2026.11.18"]
  },
  "fetch": {
    "command": "uvx",
    "args": ["mcp-server-fetch==2026.11.18"]
  }
}
```

## Examples

- [`.cursor/mcp.web.example`](../.cursor/mcp.web.example) — FOSS baseline only (no filesystem/git/fetch)
- Commercial SaaS MCPs: [`CURSOR_COMMERCIAL_ACTIVATION.md`](CURSOR_COMMERCIAL_ACTIVATION.md)

## MCP Inspector

This template does **not** document or pin `@modelcontextprotocol/inspector`. If a descendant installs it, use **≥2.16.0** or **≥1.0.6** (SSE line/event size caps — [GHSA-3xgv-mvj6-g78r](https://github.com/modelcontextprotocol/inspector/releases/tag/2.16.0)).

## Chrome DevTools

Prefer Cursor’s built-in browser / IDE browser MCP for page inspection. Do not require a third-party DevTools server on the FOSS path.
