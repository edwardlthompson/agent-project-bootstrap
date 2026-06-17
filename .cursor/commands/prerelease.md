# Pre-release gate

```bash
bash scripts/pre-release-gate.sh
```

Confirm CI + Security Scan + CodeQL green, zero Critical/High Dependabot alerts, `.template-version` present.
Do not tag or `/push` until this gate passes. See @docs/MAINTAINING_THE_TEMPLATE.md Release Checklist for maintainers.

Begin now.
