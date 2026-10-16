# MCP recipes (opt-in)

Copy examples into gitignored `.cursor/mcp.json` only after you choose servers. FOSS allowlist: [`.cursor/mcp-allowlist.json`](../.cursor/mcp-allowlist.json). Never commit live `mcp.json` or tokens.

## FOSS baseline

| Server | Role | Example |
|--------|------|---------|
| `github` | Issues/PRs | [`.cursor/mcp.foss.example`](../.cursor/mcp.foss.example) |
| `depsonar` | Dependency insight | same |

Activation: [`CURSOR_INTEGRATIONS.md`](CURSOR_INTEGRATIONS.md).

## Per-stack suggestions

| Stack | Recommended | Notes |
|-------|-------------|-------|
| web | Cursor browser / DevTools MCP; docs-lookup (Context7) | Context7 is **user-added** until FOSS-reviewed — do not allowlist blindly |
| android | github + depsonar | Prefer local emulator skill over cloud-only tools |
| node | github + depsonar | Same baseline |
| python | github + depsonar | Same baseline |
| Next.js apps | Same as web + framework docs MCP | **Not** a Golden Path in this template — recipe only |

## Examples

- [`.cursor/mcp.web.example`](../.cursor/mcp.web.example) — baseline + commented Context7 stub
- Commercial SaaS MCPs: [`CURSOR_COMMERCIAL_ACTIVATION.md`](CURSOR_COMMERCIAL_ACTIVATION.md)

## Chrome DevTools

Prefer Cursor’s built-in browser / IDE browser MCP for page inspection. Do not require a third-party DevTools server on the FOSS path.
