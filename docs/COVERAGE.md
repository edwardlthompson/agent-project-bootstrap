# Code coverage

In-repo coverage is required for budgets; external SaaS (Codecov, etc.) is **optional**.

## Local commands

| Stack | Command | Report |
|-------|---------|--------|
| web | `cd examples/web && npm test` (Vitest `--coverage`) | `examples/web/coverage/` |
| python | `cd examples/python && uv run pytest --cov --cov-fail-under=90` | `examples/python/coverage/` or terminal |
| node | `cd examples/node && npm test` (coverage if configured) | `examples/node/coverage/` |
| android | `cd examples/android && ./gradlew test` | See [Android](#android) |
| template scripts | `python3 -m pytest tests/ --cov=scripts/lib` (optional) | terminal |

`coverage/` directories are gitignored.

## CI

CI uploads `coverage-summary.json` artifacts and may comment on PRs (see `.github/workflows/ci.yml`). Green CI must not depend on a paid coverage host.

## Budgets

- Python: `--cov-fail-under=90` (see `.cursor/rules/testing.mdc`)
- Web: Vitest coverage enabled on `npm test`
- Raise thresholds only with `[HUMAN]` when baselines exist

## Android

Unit tests: `./gradlew test`. For line coverage, enable [Kover](https://github.com/Kotlin/kotlinx-kover) on the app module when ready:

```kotlin
// examples/android/app/build.gradle.kts — after plugins { }
// id("org.jetbrains.kotlinx.kover")
```

Document the chosen plugin version in an ADR if you pin it for a commercial or child app. Template FOSS CI stays on `./gradlew test` without requiring a coverage SaaS.

## Gates helper

```bash
python3 scripts/agent-run.py summarize-coverage
# or: python3 scripts/lib/summarize_coverage.py
```

Prints a one-line summary when coverage JSON artifacts exist under `examples/*/coverage/`.
