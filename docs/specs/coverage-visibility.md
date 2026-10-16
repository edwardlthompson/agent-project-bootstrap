# Spec: Coverage visibility

## Goal
In-repo coverage reports and budgets; Android coverage; gates one-liner.

## Trigger / users
Developers running tests;/gates; CI.

## Requirements
- docs/COVERAGE.md: local commands, report paths, CI artifacts.
- Align fail-under where missing; Android Kover or Jacoco on unit tests.
- Gates or helper prints coverage summary when reports exist.
- Codecov optional only; not required for green CI.

## Out of scope
Paid coverage SaaS as hard dependency.

## Acceptance checks
- COVERAGE.md exists; Android coverage config present; test asserts doc + config.

## Assumptions (flagged)
- coverage/ stays gitignored.

## Open questions
None.

## Files likely touched
docs/COVERAGE.md, examples/android/, examples/web/, scripts/, tests/
