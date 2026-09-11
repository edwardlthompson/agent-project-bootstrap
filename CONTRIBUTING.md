# Contributing

Thank you for contributing to **agent-project-bootstrap** — a FOSS project template for coding agents (Cursor, Windsurf, Antigravity, and others).

## Who contributes what

| Label | Contributor | Examples |
|-------|-------------|----------|
| `AGENT` | Coding agent | Scaffolding, tests, CI config, docs |
| `HUMAN` | Human developer | Approvals, credentials, product decisions |
| `ADB` | Human (Android) | Device testing, F-Droid submission |
| `AUTO` | CI/scripts | GitHub Actions, Dependabot, pre-commit |
## For coding agents

Read [`AGENTS.md`](AGENTS.md) and [`docs/START_HERE.md`](docs/START_HERE.md) before editing. Run `/build` for the next Sequential row, then `python3 scripts/agent-run.py watch-agent-gates --once --autofix`. Do not `git push` unless a human approved it or the user invoked `/push` or `/ship`. Use Conventional Commits. Do not halt on `[HUMAN]` or `[ADB]` labels — automate first, then backlog.

## First contribution

Thank you for helping. Read [`docs/BEST_PRACTICES.md`](docs/BEST_PRACTICES.md) if you want the industry *why* behind these files. Questions vs bugs vs vulns: [`SUPPORT.md`](SUPPORT.md). Labeled starter tasks: **Good first issue**.

1. Fork the repository and create a feature branch from `main`.
2. Read `docs/START_HERE.md`, `docs/CURSOR_MODES.md`, `CODE_OF_CONDUCT.md`, and `docs/MAINTAINING_THE_TEMPLATE.md`. First-time walk: `docs/help/TOUR.md` (Cursor: `/tour`).
3. Report security issues via `SECURITY.md` (private reporting preferred).
4. Make changes; run `bash scripts/verify.sh` locally (or the VS Code **Verify** task).
5. Open a PR using the provided template.

## Requirements for acceptable contributions

- Follow Conventional Commits (enforced by the `commit-msg` hook).
- Stay in the active feature container; do not batch unrelated BUILD_PLAN rows.
- Add or update automated tests for `[AGENT]` feature work, or document why tests are not feasible in `docs/features/{name}.md`.
- Run `bash scripts/verify.sh` (or `python3 scripts/agent-run.py verify`) before you open the PR.
- Do not commit secrets, `.env`, or keystores. Do not add proprietary SDKs on the FOSS path.
- Coding style: existing stack linters (Biome, ruff, Android lint). Max 300 lines static data, 150 lines pure logic.

## Subprojects

Runnable Golden Path code lives under `examples/{web,python,android,node,rust,go,lightroom}`. Stack guides are `modules/{stack}/MODULE.md`. Optional rust/go/lightroom: [`docs/OPTIONAL_STACKS.md`](docs/OPTIONAL_STACKS.md).

## Recommended branching (GitHub Flow)

Short-lived branches, one concern per PR, merge to `main` when required checks are green. Do not force-push `main`. Required checks (via `scripts/setup-github-repo.sh`): **CI**, **Security Scan**, **CodeQL**, **Repo Hygiene**, **Feature Gate**, **Template Upgrade Simulation (Windows)**. Full map (merge-blocking vs informational): [`docs/CI_REQUIRED_CHECKS.md`](docs/CI_REQUIRED_CHECKS.md).

### Tag protection and Environments (honesty)

- **Tag protection** on `v*` is optional maintainer setup — this template does **not** claim GitHub tag rules are enabled out of the box. Confirm under Settings → Tags before treating a tag as immutable.
- **Environments** (for example `github-pages`) gate deploy approvals only. Attaching Environments to required-check workflows can deadlock merges; keep Environments on deploy/release jobs, not on **CI** / **Security Scan** / **CodeQL**.
- Release Please opens a release PR; merging it still needs a human (or `/ship`) — see Waiting-on-a-person rows for Release Please.

## Commit messages

Use [Conventional Commits](https://www.conventionalcommits.org/). Enforced by a `commit-msg` hook:

```bash
pre-commit install --hook-type commit-msg

```

Subjects must match `type(scope)?: description` (`feat`, `fix`, `docs`, `chore`, `ci`, `test`, `refactor`, `perf`, `style`, `build`, `revert`). Merge and Revert subjects are allowed.

## Template improvements

Use the **Template Improvement** issue template for feedback.

## Pre-commit hooks

```bash
pip install pre-commit
pre-commit install
pre-commit install --hook-type commit-msg
pre-commit run --all-files

```

Includes repo hygiene checks (`scripts/check-repo-hygiene.sh`). See [`docs/REPO_HYGIENE.md`](docs/REPO_HYGIENE.md).

## Security triage

Maintainers run a weekly CVE triage pass per `docs/SECURITY_TRIAGE.md`. Review Dependabot alerts before each release.

## Release process (maintainers)

See `docs/MAINTAINING_THE_TEMPLATE.md` for the full semver release checklist.
