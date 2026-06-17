# Post-push CI poll

After pushing to main, poll required GitHub workflows until green:

```bash
bash scripts/check-github-ci.sh --wait 300
```

Required: CI, Security Scan, CodeQL. Do not mark release or Sprint 0 complete while any fail.

Begin now.
