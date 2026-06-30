# Commercial Cursor activation

Requires **Commercial** distribution tier (`--distribution-tier commercial` or `sync-cursor-features.py --tier commercial`).

## Checklist

1. Confirm `[HUMAN]` approval to swap from FOSS compliance (`foss-compliance.mdc` → `commercial-compliance.mdc`)
2. Run `python3 scripts/sync-cursor-features.py --tier commercial --copy-commercial`
3. Copy examples (if not auto-copied):
   - `.cursor/environment.json.commercial.example` → `.cursor/environment.json`
   - `.cursor/BUGBOT.md.commercial.example` → `.cursor/BUGBOT.md`
   - `.cursor/mcp.commercial.example` → `.cursor/mcp.json` (or merge servers)
4. Set environment variables (`LINEAR_API_KEY`, Sentry auth, etc.) — never commit secrets
5. Restart Cursor; verify Cloud Agent / Bugbot in Cursor settings
6. Run `bash scripts/check-cursor-integrations.sh --tier commercial`

## Android commercial patterns

See [`modules/android/COMMERCIAL.md`](../modules/android/COMMERCIAL.md) for Play Services / Firebase guidance (not in FOSS path).

## Automations

See [`CURSOR_AUTOMATIONS.commercial.md`](CURSOR_AUTOMATIONS.commercial.md) for cron/event automations (Cursor Cloud billing applies).
