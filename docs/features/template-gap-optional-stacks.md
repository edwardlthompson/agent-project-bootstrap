# Feature: template-gap-optional-stacks

> Gap reports list rust/go/lightroom as optional, never required on a web child.

## Acceptance criteria

- ✅ `check-template-gaps` JSON includes `optional_stacks` for rust, go, and lightroom
- ✅ Web (and other default stacks) mark those rows `required: false`
- ✅ A child with `stack: rust` marks only rust as required

## Smoke scenario

1. _Given_ a web child checkout
2. _When_ `python3 scripts/lib/template_gap.py` runs
3. _Then_ rust/go/lightroom appear under `optional_stacks` and not as required feature gaps

## Container map

| Layer | Path |
|-------|------|
| Logic | `scripts/lib/template_gap.py` |
| View | `docs/OPTIONAL_STACKS.md` |
| Tests | `tests/test_template_gap.py` |
| Wiring | `scripts/check-template-gaps.sh` |

## Tests

- Automated: yes — web not required; rust selected is required
- Coverage: missing optional_stacks key

## Fallback validation

- Why tests are not feasible: N/A
- Command: `python3 scripts/agent-run.py feature-gate --stack docs`

## Definition of Done

See `docs/FEATURE_MODULES.md`.
