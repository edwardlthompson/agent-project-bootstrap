# Optional Stack Modules

The init script stack picker (`web` / `python` / `android` / `node` / `multi` / `none`) does **not** include optional ecosystems (rust, go, lightroom, blender). Enable them manually when needed. `schemas/golden-path/feature-catalog.json` lists Lightroom as `lightroom-plugin` and Blender as `icon-factory` so `/upgrade` gap reports skip them on web/Android-only children. `check-template-gaps` also emits `optional_stacks` rows for rust, go, lightroom, and blender. Those rows are informational (`required: false`) unless the child's selected stack is that ecosystem.

| Module | Guide | Example | When to keep |
|--------|-------|---------|--------------|
| Lightroom plugin | `modules/lightroom/MODULE.md` | `examples/lightroom/` | Adobe Lightroom Classic plugin work |
| Blender icon factory | `modules/blender/MODULE.md` | `examples/blender/` | Cycles/OptiX icon batch (host runtime) |
| Rust | `modules/rust/MODULE.md` | `examples/rust/` | Rust CLI, services, or libraries |
| Go | `modules/go/MODULE.md` | `examples/go/` | Go CLI, services, or libraries |
| Node API | `modules/node/MODULE.md` | `examples/node/` | Primary stack via `--stack node`; optional when pruning other stacks |
## Dependabot groups (Cargo / Go)

Optional stacks ship weekly grouped updates in `.github/dependabot.yml`:

| Ecosystem | Directory | Group |
|-----------|-----------|-------|
| cargo | `/examples/rust` | `rust-dependencies` |
| gomod | `/examples/go` | `go-dependencies` |
Health check: groups stay weekly; majors still need a human. Prefer local `/update-deps` before merging large Cargo/Go group PRs. Policy: [`DEPENDABOT_AUTOMERGE.md`](DEPENDABOT_AUTOMERGE.md). Child-activation checklists: `modules/rust/MODULE.md`, `modules/go/MODULE.md`.

## Opt-in during init

When the init script asks to prune unused examples, answer **no** (or choose `multi`) if you need optional stacks. Then delete stacks you do **not** need:

```bash
# Example: web-only project, drop Rust/Go/Lightroom/Blender
rm -rf examples/rust examples/go examples/lightroom examples/blender
rm -rf modules/rust modules/go modules/lightroom modules/blender

```

### Golden-path prune (default)

When a **primary** stack is decided (`web` / `python` / `android` / `node`), init **prunes** unused examples and modules automatically — including optional stacks — so the child keeps only that golden path. `multi` and `none` keep everything.

| Flag | Effect |
|------|--------|
| `--no-prune` | Keep all examples/modules (skip golden-path prune) |
| `--keep-optional` | When pruning, retain `rust` / `go` / `lightroom` / `blender` |
| `--prune-optional` | Explicit alias: drop optional stacks (**default** with golden-path prune) |
| `--prune` | Force prune (redundant for primary stacks; kept for scripts) |

```bash
# Web-only fork (default: prune extras + optional)
bash scripts/init-project.sh --non-interactive --stack web \
  --project-name "My App" --purpose "PWA"

# Web golden path but keep optional stacks for later
bash scripts/init-project.sh --non-interactive --stack web --keep-optional \
  --project-name "My App" --purpose "PWA"

# Keep the full catalog
bash scripts/init-project.sh --non-interactive --stack web --no-prune \
  --project-name "My App" --purpose "PWA"

```

PowerShell equivalents: default prune; `-KeepOptional` or `-NoPrune`.

`scripts/simulate-template-upgrade.sh` runs both paths in CI (`--no-prune` then prune with optional removed).

## Linguist attribution (language stats)

Init copies `templates/linguist/child.gitattributes` onto `.gitattributes` (append under `# --- linguist ---` when a file already exists). Flags: `--no-linguist` to skip; `--dry-run` prints the copy/append without writing.

**Python stack:** the `scripts/** linguist-vendored` line is commented out so product scripts still count toward GitHub language stats. Other stacks leave that line active so template scaffolding does not dominate.

## CI behavior

Optional example CI jobs (`rust`, `go`, `lightroom`) and the instrumented Android job run when:

1. The corresponding `examples/{stack}/` directory **exists** (skipped after you delete the folder), and
2. Files under that directory **changed** on the push/PR (or on `workflow_dispatch`, which runs all present optional jobs).

The `node` example job runs on every push when `examples/node/` exists. Core jobs (web, python, android build, feature-gate) always run on every push to `main`.

See the optional stack **hello About** matrix: [`docs/OPTIONAL_STACK_ABOUT_MATRIX.md`](OPTIONAL_STACK_ABOUT_MATRIX.md).
