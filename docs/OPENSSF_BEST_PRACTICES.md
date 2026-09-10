# OpenSSF Best Practices badge

Public entry: [project 14564](https://www.bestpractices.dev/en/projects/14564) (formerly CII).

The live JSON still shows **19% Passing** until a logged-in maintainer **saves** answers. Adding the homepage URL alone does not raise the score. `.bestpractices.json` is a proposal file; the site only re-reads it from `main` after **Save (and continue) 🤖**.

Regenerate apply links: `python3 scripts/lib/bestpractices_apply.py`

## Fastest way to raise Passing (today)

1. Log in at [bestpractices.dev](https://www.bestpractices.dev/en) with GitHub.
2. Open this **Passing** link (yellow 🤖 fields). Review, then **Save and Continue**:

   `python3 scripts/lib/bestpractices_apply.py` → print the `passing` URL  
   Or open `/en/projects?as=edit&section=passing&url=https%3A%2F%2Fgithub.com%2Fedwardlthompson%2Fagent-project-bootstrap` and accept the proposals from `.bestpractices.json` after it is on `main`.
3. Open the **Baseline-1** URL from the same script. Save. That clears the Unmet **OSPS-BR-01.02** row once PR #98 is on `main` (branch-name check). Until then, mark BR-01.02 only after you merge, or leave it `?`.
4. Do **not** start Silver/Gold until Passing shows a green passing badge.

## Human-only Passing rows (do these yourself)

| Criterion | What to click | Paste this |
|-----------|---------------|------------|
| `know_secure_design` | **Met** if you have designed security for this repo (threat model, private reporting, no default telemetry) | `docs/THREAT_MODEL.md` + `SECURITY.md`; primary maintainer |
| `know_common_errors` | **Met** if you know injection, secret leak, and supply-chain mistakes for this stack | Gitleaks, input validation at boundaries, Dependabot/`update-deps --audit` |
| `report_responses` | **Met** if you answered most bugs in the last 2–12 months, or there were none | GitHub Issues; no unreplied reports |
| Branch protection **OSPS-AC-03.01 / 03.02** | GitHub → Settings → Branches → `main`: require PR, block force-push and deletion | Then **Met** on Baseline-1 |

## After PR #98 is on `main`

1. Edit any section → **Save (and continue) 🤖** so detectives re-scan LICENSE, SECURITY, CONTRIBUTING, and `.bestpractices.json`.
2. Confirm the README badge at `https://www.bestpractices.dev/projects/14564/badge` turns from in-progress to passing.

## What not to mark Met

- Two-person review / signed git tags / 80–90% coverage (Silver/Gold) unless they are actually true.
- Crypto rows are **N/A** (this template does not implement crypto).
- `vulnerability_report_response` is **N/A** until you receive a private report.

Do not invent Met answers. Status `?` in `.bestpractices.json` is ignored on purpose.
