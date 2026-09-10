# OpenSSF Best Practices badge

Public entry: [project 14564](https://www.bestpractices.dev/en/projects/14564) (formerly CII).

Live JSON (2026-09-10): **96% Passing**, Baseline-1 **0%**, `badge_level: in_progress`. Homepage URL is set. `.bestpractices.json` is a proposal file; the site only re-reads it from `main` after **Save (and continue) 🤖**.

Regenerate apply links: `python3 scripts/lib/bestpractices_apply.py`

## The 4% Passing gap (do this next)

Four Passing MUST rows are still `?`. One short leftover URL fills them as yellow 🤖 proposals. Review, then **Save and Continue**:

`python3 scripts/lib/bestpractices_apply.py` → print `# passing leftovers`

| Criterion | Click | Paste this |
|-----------|-------|------------|
| `homepage_url` | **Met** | `https://github.com/edwardlthompson/agent-project-bootstrap` |
| `report_url` | **Met** | `https://github.com/edwardlthompson/agent-project-bootstrap/issues` |
| `know_secure_design` | **Met** if you designed security for this repo | `docs/THREAT_MODEL.md` + `SECURITY.md`; primary maintainer |
| `know_common_errors` | **Met** if you know injection, secret leak, and supply-chain mistakes | Gitleaks, input validation at boundaries, Dependabot/`update-deps --audit` |

`achieve_passing` stays **Unmet** until those four are Met. Do **not** start Silver/Gold until the Passing badge is green.

## After Passing is 100%

1. Open the **Baseline-1** URL from the same script and Save (optional second badge).
2. GitHub → Settings → Branches → `main`: require PR, block force-push and deletion, then mark **OSPS-AC-03.01 / 03.02** Met.
3. Mark **OSPS-BR-01.02** Met only after PR #98 is on `main` (branch-name check). Until then leave it `?`.
4. Edit any section → **Save (and continue) 🤖** so detectives re-scan LICENSE, SECURITY, CONTRIBUTING, and `.bestpractices.json`.

## What not to mark Met

- Two-person review / signed git tags / 80–90% coverage (Silver/Gold) unless they are actually true.
- Crypto rows are **N/A** (this template does not implement crypto).
- `vulnerability_report_response` is **N/A** until you receive a private report.

Do not invent Met answers. Status `?` in `.bestpractices.json` is ignored on purpose. `know_secure_design` / `know_common_errors` stay out of that file; they appear only on the leftover apply URL for human review.
