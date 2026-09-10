# OpenSSF Best Practices badge

Public entry: [project 14564](https://www.bestpractices.dev/en/projects/14564) (formerly CII).

Live JSON (2026-09-10): **99% Passing** because `vulnerability_report_private` is Met with prose and **no `https://`**. BadgeApp does not count Met without a URL. Do **not** choose N/A: this repo supports private HTTPS reports (GitHub Advisories). N/A is only for projects that never accept private reports.

Regenerate apply links: `python3 scripts/lib/bestpractices_apply.py`

## The 1% Passing gap (do this next)

The last apply link was **unforced**, so it did not overwrite the existing prose (blue ≠). Use the **forced** leftover URL (orange ⚠️), then **Save and Continue**:

`python3 scripts/lib/bestpractices_apply.py` → print `# passing leftovers`

Or edit [project 14564 Passing](https://www.bestpractices.dev/en/projects/14564/passing/edit) by hand:

| Criterion | Click | Replace the justification with this URL only |
|-----------|-------|----------------------------------------------|
| `vulnerability_report_private` | **Met** (not N/A) | `https://github.com/edwardlthompson/agent-project-bootstrap/security/advisories/new` |

That page is a private defect report over HTTPS/TLS. `SECURITY.md` documents the same URL.

## After Passing is 100%

1. Open the **Baseline-1** URL from the same script and Save (optional second badge).
2. GitHub → Settings → Branches → `main`: require PR, block force-push and deletion, then mark **OSPS-AC-03.01 / 03.02** Met.
3. Mark **OSPS-BR-01.02** Met only after PR #98 is on `main` (branch-name check). Until then leave it `?`.
4. Edit any section → **Save (and continue) 🤖** so detectives re-scan LICENSE, SECURITY, CONTRIBUTING, and `.bestpractices.json`.

## What not to mark Met

- Two-person review / signed git tags / 80–90% coverage (Silver/Gold) unless they are actually true.
- Crypto rows are **N/A** (this template does not implement crypto).
- `vulnerability_report_response` is **N/A** until you receive a private report.
- `vulnerability_report_private` is **not** N/A while GitHub private reporting is offered.
