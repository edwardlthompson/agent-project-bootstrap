# Feature: cursor-feature-registry

> Keep `CURSOR_FEATURE_REGISTRY.json` current with shipped skills.

## Acceptance criteria

- ✅ `updated_at` is at least 2026-09-10
- ✅ Every `.cursor/skills/*/SKILL.md` has a `skills.{name}` registry id
- ✅ Integrations check fails on a missing skill id

## Smoke scenario

1. _Given_ the skills directory
2. _When_ `check_cursor_integrations` runs
3. _Then_ every skill folder is in the registry

## Container map

| Layer | Path |
|-------|------|
| Logic | `scripts/lib/check_cursor_integrations.py` |
| View | `docs/CURSOR_FEATURE_REGISTRY.json` |
| Tests | `tests/test_cursor_feature_registry.py` |
| Wiring | `scripts/check-cursor-integrations.sh` |

## Tests

- Automated: yes — skill ids + updated_at
- Coverage: missing distribution_tier

## Fallback validation

- Why tests are not feasible: N/A
- Command: `python3 scripts/agent-run.py feature-gate --stack docs`

## Definition of Done

See `docs/FEATURE_MODULES.md`.
