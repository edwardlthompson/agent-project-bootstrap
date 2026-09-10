# Feature: nix-flake-ci

> Optional CI job evaluates `flake.nix` apps. Not a second generator.

## Acceptance criteria

- ✅ Path-filtered `nix` job runs `check-nix-flake.sh` then `nix flake show`
- ✅ `ci-ok` does not `needs` the nix job (skipped when flake files are untouched)
- ✅ Flake still wraps only `scripts/verify.sh`, validate-bootstrap, feature-gate, update-deps

## Smoke scenario

1. _Given_ `flake.nix` changed on a PR
2. _When_ CI `path-changes` sets `nix=true`
3. _Then_ the optional job installs Nix and evaluates `.#apps.x86_64-linux.verify.program`

## Container map

| Layer | Path |
|-------|------|
| Logic | `flake.nix`, `scripts/lib/nix_flake.py` |
| View | N/A |
| Tests | `tests/test_nix_flake.py` |
| Wiring | `.github/workflows/ci.yml` `nix` job |

## Tests

- Automated: yes — flake snippets + ci-ok must not require nix
- Coverage: missing install-nix-action, ci-ok coupling

## Fallback validation

- Why tests are not feasible: N/A
- Command: `python3 scripts/agent-run.py feature-gate --stack docs`

## Definition of Done

See `docs/FEATURE_MODULES.md`.
