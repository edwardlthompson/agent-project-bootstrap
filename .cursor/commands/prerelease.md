# Pre-release gate

```bash
python3 scripts/agent-run.py pre-release-gate
```

Confirm CI + Security Scan + CodeQL green, zero Critical/High Dependabot alerts, `.template-version` present.
Do not tag or `/push` until this gate passes. See @docs/MAINTAINING_THE_TEMPLATE.md Release Checklist for maintainers.

Begin now.
