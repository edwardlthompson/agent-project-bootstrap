# agent-project-bootstrap

GitHub Template Repository for bootstrapping FOSS projects with Cursor agents.

Pure MIT-licensed scaffolding: verbatim initialization prompt, labeled BUILD_PLAN sprints, CI guardrails, workspace memory files, configurable template update checker, and Golden Path stubs (Web, Python, Node, Android).

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

## Stack Selection (Sprint 0)

During `init-project`, choose `web`, `python`, `android`, `multi`, or `none` (keep all).

Active modules are synced to `AGENT_MEMORY.md` and recorded in `.cursor/stack-selection.json`.

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

| Stack modules | `modules/{web,python,android,lightroom,rust,go}/MODULE.md` |

| Golden Path examples | `examples/{web,python,android,lightroom}/`; optional `rust/`, `go/` — see `docs/OPTIONAL_STACKS.md` |
| Agent documentation | `docs/` — prompts, security, design guide (**not** the public website) |
| Public website source | `examples/web/` (Vite PWA source; see `docs/WEB_PROJECT_LAYOUT.md`) |
| GitHub Pages deploy | `.github/workflows/pages.yml` → `examples/web/dist` (Actions artifact) |
| CI guardrails | `.github/workflows/` (incl. OpenSSF Scorecard weekly) |

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

## GitHub Pages Demo

The `examples/web` PWA deploys to GitHub Pages on push to `main` (workflow: `.github/workflows/pages.yml`). The build sets `VITE_BASE_PATH` for project-site hosting with no analytics or tracking scripts.

**`docs/` is not your website.** The `docs/` folder holds agent instructions, security playbooks, and design guides — it is never published as the live site. Website source is `examples/web/`; only the built output in `examples/web/dist/` is deployed via GitHub Actions. Set Pages source to **GitHub Actions** in repo settings, not "Deploy from `/docs`". See [`docs/WEB_PROJECT_LAYOUT.md`](docs/WEB_PROJECT_LAYOUT.md) for the full folder map and localization layout (`src/locales/` + `t()` separate from `style.css`).

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

One-time repo security setup (Dependabot alerts, private reporting, branch protection):

```bash

bash scripts/setup-github-repo.sh

# Windows:

pwsh scripts/setup-github-repo.ps1

```

Before any version bump or release tag:

```bash

bash scripts/pre-release-gate.sh

# Windows:

pwsh scripts/pre-release-gate.ps1

```

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

| Lightroom plugin | `modules/lightroom/MODULE.md` | `examples/lightroom/` |

Optional stacks (Rust, Go, Node when present) are documented in [`docs/OPTIONAL_STACKS.md`](docs/OPTIONAL_STACKS.md) — not in the default init stack picker.

Machine-readable catalog: [`TEMPLATE_INDEX.json`](TEMPLATE_INDEX.json)

## Repository Layout

```
docs/           Agent docs only (NOT the public website) — see docs/WEB_PROJECT_LAYOUT.md
modules/        Stack-specific agent rules (activate matching stack only)
examples/       Golden Path reference implementations
examples/web/   PWA source; dist/ published via GitHub Actions
scripts/        Init, update checker, validation
.cursor/rules/  Persistent Cursor agent directives
.github/        CI workflows, Dependabot, issue templates

```

## Contributing

MIT licensed. See [`CONTRIBUTING.md`](CONTRIBUTING.md).

Template maintainers: [`docs/MAINTAINING_THE_TEMPLATE.md`](docs/MAINTAINING_THE_TEMPLATE.md)

## GitHub About

Repo description draft for the short About preview: [`docs/GITHUB_ABOUT.md`](docs/GITHUB_ABOUT.md)

## Maintainer Release

Current template version: **0.7.1** (see `.template-version`, Release Please, and `scripts/pre-release-gate.sh`).
