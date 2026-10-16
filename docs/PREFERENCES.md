# Preferences (durable)

Short durable preferences for agents and humans. `/shape` may offer to append here — **ask first**.
Read this file before shaping or building features (patterns + security).

## Defaults for this template

- Prefer `/shape` before `/plan` for non-trivial multi-file ideas.
- Prefer small Conventional Commits; after each ✅ `[AGENT]` row, ask the human to `/push` when a remote exists (never silent `git push`).
- Re-read `AGENT.md` before Golden Path About, Settings, purpose, or donate copy.
- FOSS is the default distribution tier; commercial requires explicit init/`[HUMAN]` approval.

## Coding pattern preferences

- Prefer simple solutions; avoid duplication (reuse existing helpers).
- Write code that accounts for **dev, test, and prod** environments.
- Only make changes that were requested or are clearly required for that change.
- When fixing a bug, exhaust existing patterns before introducing new tech; if you replace a path, remove the old implementation.
- Keep the codebase clean and organized.
- Avoid one-off scripts in-repo when a one-liner or existing gate suffices.
- File size: follow [`FILE_SIZE_GUIDE.md`](FILE_SIZE_GUIDE.md) — **150 lines** pure logic, **300 lines** static UI+i18n (not a separate 200–300 limit).
- Mocking, stubbing, and fake data are **tests only** — never in dev or prod paths.
- Never overwrite `.env` without asking and confirming (use `.env.example` for templates).

## Coding workflow preferences

- Focus on code relevant to the task; do not touch unrelated areas.
- Write thorough tests for major functionality (test-first).
- Do not major-rewrite working patterns or architecture unless explicitly asked.
- Before editing, consider callers and other modules that may be affected.

## Vibe-coded app security risks (must address)

Do not create these risks. Deep detail: [`THREAT_MODEL.md`](THREAT_MODEL.md), [`SECURITY.md`](../SECURITY.md), [`PRIVACY.md`](PRIVACY.md), [`SECURITY_TRIAGE.md`](SECURITY_TRIAGE.md).

| Risk | Do this |
|------|---------|
| **API-key leakage** | Never commit secrets, tokens, or live `.env`; no keys in rules, prompts, or logs; keep `.env.example` only |
| **Dependencies** | Prefer `/update-deps` (audit) before ship; do not add unvetted packages |
| **Lack of rate limiting** | Document and enforce rate limits before shipping public or agent-facing HTTP/LLM endpoints |
| **Input validation / sanitization** | Validate at all boundaries; never pass raw user content into shell, SQL, or HTML |
| **Bot attacks & abuse** | Auth where needed; rate limits; no open write APIs without abuse controls |
| **Sensitive user info** | No PII in git, crash reports, or public issues; follow PRIVACY.md |

**Agents must refuse** to hardcode secrets, disable security gates/hooks, or skip private vulnerability reporting ([`SECURITY.md`](../SECURITY.md)).
