# Upgrade gap plan — child repos on template 1.2.0 → next

> For **child** products that forked or “Use this template”’d at **v1.2.0**. Do not overwrite Sacred files. On this template repo, `/upgrade` still runs `simulate-template-upgrade` instead of this plan.

## Acceptance criteria

- ✅ Documents Canon / Mixed / Sacred / Golden Path buckets for 1.2.0 → next
- ✅ Points at `check-template-updates` / `check-template-gaps` and `docs/help/UPGRADE.md`
- ✅ Includes resolved Critique (Issue → Resolution)
- ✅ Does not instruct blind overwrite of Sacred files

## Smoke scenario

1. _Given_ a child still on template tag `1.2.0`
2. _When_ the human runs `check-template-updates` after a newer tag exists
3. _Then_ this plan plus the numbered gap list drive `/upgrade` without touching Sacred files until the human names numbers

## Container map

| Layer | Path |
|-------|------|
| Logic | `scripts/` template-update / gap checkers |
| View | `docs/features/upgrade-gap-1.2.0.md`, `docs/help/UPGRADE.md` |
| Tests | Feature-doc structure gate (`validate-bootstrap`) |
| Wiring | `/upgrade` command |

## Tests

- Automated: yes — feature markdown structure via bootstrap validate
- Coverage: required section headings present

## Fallback validation

- Why tests are not feasible: N/A
- Command: `python3 scripts/agent-run.py validate-bootstrap --quick`

## How to run

```bash
python3 scripts/agent-run.py check-template-updates
python3 scripts/agent-run.py check-template-gaps
```

Then follow [`docs/help/UPGRADE.md`](../help/UPGRADE.md): print numbered Canon / Mixed / Sacred / Golden Path gaps; wait for the human to name numbers before editing.

## Expected deltas after 1.2.0

When the next template tag ships (for example `1.2.1` / `1.3.0`), children typically pull:

| Bucket | Likely paths | Action |
|--------|--------------|--------|
| Canon | `.cursor/rules/*.mdc`, `.cursor/commands/`, `docs/help/BATCH_COMMANDS.md`, `docs/CURSOR_MODES.md`, Semgrep packs, Scorecard classifier | Copy/overwrite after review |
| Mixed | `.github/workflows/*`, `dependabot.yml`, `bootstrap.config.json` keys | Merge; keep child values |
| Sacred | `AGENTS.md`, `docs/spec.md`, `docs/plan.md`, `docs/INITIALIZATION_PROMPT.md`, live `.env` | Human only — never blind overwrite |
| Golden Path | New `examples/{stack}/` slices for the **active** stack only | Adopt with `/feature`; do not copy over the product app |

## Critique

| Issue | Resolution |
|-------|------------|
| Null/empty gap list | Treat as “already current”; still run `simulate-template-upgrade` on the template itself |
| Network timeout on `check-template-updates` | Retry once; if offline, compare CHANGELOG tags manually from Releases |
| Race with open Dependabot PRs | Finish or close Dependabot before Canon copies of workflows |
| Unhandled Sacred merge | Halt; escalate `[HUMAN]` — never auto-merge `AGENTS.md` |

## Definition of Done

1. Gap plan written (this file + numbered list from the checker)
2. Human named item numbers
3. Canon/Mixed applied; Sacred left alone
4. `python3 scripts/agent-run.py validate-bootstrap --quick` green
5. One `DECISION_LOG.md` entry for the upgrade

Policy table: [`UPGRADING_FROM_TEMPLATE.md`](../UPGRADING_FROM_TEMPLATE.md).
