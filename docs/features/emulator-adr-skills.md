# Feature: emulator-adr-skills

> Companion skills for `/emulator` and `/adr`.

## Acceptance criteria

- ✅ `.cursor/skills/emulator/SKILL.md` and `.cursor/skills/adr/SKILL.md` exist with See also links
- ✅ Command files point at those skills
- ✅ `check_cursor_integrations` requires both skills

## Smoke scenario

1. _Given_ `/emulator` or `/adr`
2. _When_ the integrations check runs
3. _Then_ the matching skill file is present

## Container map

| Layer | Path |
|-------|------|
| Logic | `scripts/lib/check_cursor_integrations.py` |
| View | `.cursor/skills/emulator/SKILL.md`, `.cursor/skills/adr/SKILL.md` |
| Tests | `tests/test_emulator_adr_skills.py` |
| Wiring | `.cursor/commands/emulator.md`, `.cursor/commands/adr.md` |

## Tests

- Automated: yes — skill files + command pointers
- Coverage: missing See also

## Fallback validation

- Why tests are not feasible: N/A
- Command: `python3 scripts/agent-run.py feature-gate --stack docs`

## Definition of Done

See `docs/FEATURE_MODULES.md`.
