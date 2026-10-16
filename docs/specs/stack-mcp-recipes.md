# Spec: Stack MCP recipes

## Goal
Opt-in MCP recipes per existing Golden Path stack without a Next.js Golden Path.

## Trigger / users
Maintainer or child choosing MCP servers for web/android/node/python after init.

## Requirements
- docs/MCP_RECIPES.md lists recommended MCPs per stack.
- Opt-in .cursor/mcp.*.example JSON files; never commit live mcp.json.
- Context7 documented as user-added unless FOSS-reviewed; Chrome DevTools maps to Cursor browser MCP; Next.js is a recipe note only.
- Extend mcp-allowlist.json only for FOSS-safe servers.
- Tests: example JSON parses; allowlist servers documented.

## Out of scope
New Next.js examples/ stack; Cloud-only MCP defaults.

## Acceptance checks
- MCP_RECIPES.md exists; at least one stack example JSON parses.
- FOSS check-cursor-integrations still passes.

## Assumptions (flagged)
- github + depsonar remain the FOSS baseline.

## Open questions
None.

## Files likely touched
docs/MCP_RECIPES.md, .cursor/mcp.web.example, modules/*/MODULE.md, .cursor/mcp-allowlist.json, tests/
