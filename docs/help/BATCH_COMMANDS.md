# Agent shortcuts (cheat sheet)

Type `/` in Cursor Agent chat. Other IDEs: paste the matching `docs/help/` file. Print: [`batch-commands-print.html`](batch-commands-print.html).

## Supers

| Command | When |
|---------|------|
| `/bootstrap` | New project Sprint 0 |
| `/tour` | First-run walk |
| `/coach` | One next action |
| `/verify` | Before merge |
| `/build` | Run BUILD_PLAN |
| `/ship` | Release to GitHub |
| `/maintain` | Weekly health |
Red CI → `/fix` or `/ci` + `/gates` first. Dirty Unreleased + empty AGENT → `/ship`. Empty board → `/allideas`.

## By moment

- **Start:** `/tour` · `/init` · `/setup` · `/gates` · `/coach`
- **Build:** `/plan` · `/adr` · `/feature` · `/fix` · `/cleanup` · `/scope`
- **UX:** `/ux-review` · `/ux-apply` · aliases `/ui-review` `/ux-audit` `/ui-audit`
- **Publish:** `/update-deps` · `/prerelease` · `/push` · `/regress`
- **Local:** `/best-of-n` · `/emulator`
- **Maintain:** `/triage` · `/dependabot` · `/audit` · `/upgrade`
- **Handoff:** `/compact` · `/restore` · `/resume`

`/gates` = agent-fast + dirty stacks; `/gates --full` = multi. Registry: [`docs/BATCH_COMMANDS.md`](../BATCH_COMMANDS.md). Cline: [`CLINE.md`](CLINE.md).
