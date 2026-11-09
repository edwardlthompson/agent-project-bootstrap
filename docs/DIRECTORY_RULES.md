# Directory rules (asset classes)

Machine layout law companion to [`LAYOUT.md`](LAYOUT.md). Cursor.Directory curation lives in [`CURSOR_DIRECTORY.md`](CURSOR_DIRECTORY.md).

## Rules

1. **Product code** stays under `examples/{active-stack}/` after init prune.
2. **Docs for humans/agents** stay under `docs/` — never the public website root.
3. **Brand icons** resolve via [`BRAND_ICON.md`](BRAND_ICON.md); never duplicate SoT icons under `docs/`.
4. **Generated tokens** are outputs of `scripts/sync-design-tokens.py` — do not hand-edit.
5. **Orphan exceptions** require `config/orphan-exceptions.yaml` with reason + expiry.
6. **Allowlisted scripts** for intentional orphans: `scripts/orphan-allowlist.txt`.
