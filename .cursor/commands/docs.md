# Documentation checks

Docs-only validation (no full feature gate):

```bash
bash scripts/check-readme-health.sh
bash scripts/check-markdown-tables.sh
bash scripts/check-file-encoding.sh
```

Fix failures before commit. On Windows, re-run encoding check after bulk doc edits.

Begin now.
