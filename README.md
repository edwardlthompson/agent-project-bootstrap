# agent-project-bootstrap

GitHub Template Repository for bootstrapping FOSS projects with Cursor agents.

Pure MIT-licensed scaffolding: verbatim initialization prompt, labeled BUILD_PLAN sprints, CI guardrails, workspace memory files, configurable template update checker, and Golden Path stubs (Web, Python, Android).

## Quick Start

1. Click **Use this template** on GitHub to create your project repo.
2. Clone and run the init script:

   ```bash
   # Linux / macOS / WSL
   ./scripts/init-project.sh

   # Windows PowerShell
   .\scripts\init-project.ps1
   ```

3. Open Cursor and paste the bootstrap prompt from [`docs/START_HERE.md`](docs/START_HERE.md):

   ```
   Read @docs/START_HERE.md and @docs/INITIALIZATION_PROMPT.md.
   Follow Section 8 Startup Sequence.
   Use BUILD_PLAN.md Sequential lane first; respect AGENT/HUMAN/ADB/AUTO labels.
   ```

## What's Included

| Component | Location |
|-----------|----------|
| Initialization prompt | `docs/INITIALIZATION_PROMPT.md` |
| Agent routing | `docs/START_HERE.md`, `docs/FOR_AGENTS.md`, `AGENTS.md` |
| Sprint task board | `BUILD_PLAN.md` |
| Workspace memory | `AGENT_MEMORY.md`, `DECISION_LOG.md`, `KNOWLEDGE_BASE.md` |
| Security & privacy | `SECURITY.md`, `docs/SECURITY_TRIAGE.md`, `docs/THREAT_MODEL.md`, `docs/PRIVACY.md` |
| Operations | `docs/RUNBOOK.md` |
| License attribution | `THIRD_PARTY_LICENSES.md`, `LICENSE` |
| Stack modules | `modules/{web,python,android,lightroom}/MODULE.md` |
| Golden Path examples | `examples/{web,python,android}/` |
| CI guardrails | `.github/workflows/` |
| Cursor rules | `.cursor/rules/*.mdc` |

## BUILD_PLAN Labels

Every task carries an owner label for filtering automated vs human work.

| Label | Owner | When to use |
|-------|-------|-------------|
| `AGENT` | Cursor Agent | Code, docs, scaffolding, tests, CI |
| `HUMAN` | Human developer | Approvals, credentials, GitHub settings |
| `ADB` | Human (Android) | Device testing, F-Droid submission |
| `AUTO` | CI/scripts | GitHub Actions, Dependabot, pre-commit |

```bash
grep '\[AGENT\]' BUILD_PLAN.md
grep '\[HUMAN\]' BUILD_PLAN.md
```

Each sprint has **Sequential** (ordered) and **Parallel** (isolated scope) lanes. See [`BUILD_PLAN.md`](BUILD_PLAN.md).

## Template Update Checker

Child repos can check for new upstream template releases on GitHub.

Configure in [`.template-update.json`](.template-update.json):

| `check_interval` | Behavior |
|------------------|----------|
| `off` | Disabled |
| `daily` | Check at most once per day |
| `weekly` | Check at most once per week (default) |
| `monthly` | Check at most once per month |
| `on_session` | Check every devcontainer/session start |

`notify_method` supports `stdout` only (banner printed to terminal).

**Change interval:** edit `.template-update.json` or re-run the init script.

**Manual check:**

```bash
bash scripts/check-template-updates.sh
# or
pwsh scripts/check-template-updates.ps1
```

Runs automatically on devcontainer start. When a new version is available, see [`docs/UPGRADING_FROM_TEMPLATE.md`](docs/UPGRADING_FROM_TEMPLATE.md).

The devcontainer also runs `check-file-encoding.sh` on start, includes the **GitHub CLI** (`gh`) for `validate-workflow-actions.sh`, and prints a reminder to run `check-github-ci.sh --wait 300` after pushing to `main`.

## GitHub CI Gate (post-push)

After pushing workflow or dependency changes to `main`, poll required workflows:

```bash
bash scripts/check-github-ci.sh --wait 300
# Windows:
pwsh scripts/check-github-ci.ps1 -WaitSeconds 300
```

Required workflows: **CI**, **Security Scan**, **CodeQL**.

## Security

### Dependabot alerts (one-time setup)

`[HUMAN]` enables CVE notifications in GitHub:

**Settings → Code security and analysis** → enable **Dependabot alerts** and **Dependabot security updates**.

See [`docs/SECURITY_TRIAGE.md`](docs/SECURITY_TRIAGE.md) for the full setup and weekly triage checklist.

Report vulnerabilities via [`SECURITY.md`](SECURITY.md) (private reporting preferred).

Community standards: [`CODE_OF_CONDUCT.md`](CODE_OF_CONDUCT.md)

### Weekly CVE triage

`[HUMAN]` runs a weekly triage pass (recommended: Monday):

1. Review Dependabot alerts (Critical/High first)
2. Triage open Dependabot PRs (fix / defer / dismiss)
3. Confirm Trivy + CodeQL CI green after merges

## Supported Stacks

| Module | Guide | Example |
|--------|-------|---------|
| Web / PWA | `modules/web/MODULE.md` | `examples/web/` |
| Python | `modules/python/MODULE.md` | `examples/python/` |
| Android / F-Droid | `modules/android/MODULE.md` | `examples/android/` |
| Lightroom plugin | `modules/lightroom/MODULE.md` | _(SDK reference only)_ |

Machine-readable catalog: [`TEMPLATE_INDEX.json`](TEMPLATE_INDEX.json)

## Repository Layout

```
docs/           Entry points, init prompt, security triage, upgrade guide
modules/        Stack-specific agent rules (activate matching stack only)
examples/       Golden Path reference implementations
scripts/        Init, update checker, validation
.cursor/rules/  Persistent Cursor agent directives
.github/        CI workflows, Dependabot, issue templates
```

## Contributing

MIT licensed. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

Template maintainers: [`docs/MAINTAINING_THE_TEMPLATE.md`](docs/MAINTAINING_THE_TEMPLATE.md)

## GitHub About

Repo description draft for the short About preview: [`docs/GITHUB_ABOUT.md`](docs/GITHUB_ABOUT.md)
