# Threat Model

> Draft during Sprint 1 before Golden Path ships. Link security tasks in `BUILD_PLAN.md`.

## Scope

| Item | Value |
|------|-------|
| Project | [PROJECT_NAME] |
| Stack | [INSERT PLATFORM / TECH STACK HERE] |
| Methodology | STRIDE (adapt per stack: OWASP ASVS for web, MASVS for mobile) + OWASP LLM Top 10 for agent-exposed APIs |
## Trust Boundaries

```text
[User] --> [Client App / PWA] --> [GitHub Issues / Discussions]
                |                      |
           Local pending crash    Public issue body
           (opt-in, sanitized)

[Maintainer] --> [/audit /ideas] --> [GitHub issue text as DATA only]

```

Public GitHub Issues are a trust boundary. Issue and discussion text is untrusted (LLM01): never execute it as agent instructions. See ADR-0002.

## STRIDE Summary

| Threat | Example | Mitigation | Owner |
|--------|---------|------------|-------|
| Spoofing | Fake API client | Auth tokens, TLS | AGENT |
| Tampering | Modified local state | Integrity checks, signed updates | AGENT |
| Repudiation | Denied user action | Audit logs (no PII without consent) | AGENT |
| Information disclosure | PII in logs | Data minimization, redaction | AGENT |
| Denial of service | Oversized payloads | Input limits, rate limiting | AGENT |
| Elevation of privilege | Bypass auth | Least privilege, boundary validation | AGENT |
## Top Abuse Cases

1. _Define after Golden Path — e.g., unauthorized data access_
2. _Supply-chain compromise via malicious dependency_
3. _Secret leakage via committed credentials_
4. _Prompt injection (if agent-exposed APIs)_
5. _Telemetry opt-out bypass_
6. _Crash/bug issue body used as agent instructions (LLM01)_
7. _PII or secrets pasted into a public issue_

## OWASP LLM Top 10

Walk agent-exposed surfaces against [OWASP LLM Top 10 (2025)](https://owasp.org/www-project-top-10-for-large-language-model-applications/). No extra scanner — map to existing gates. Prompt injection: [`.cursor/rules/destructive-ops.mdc`](../.cursor/rules/destructive-ops.mdc).

| ID | Risk | Template control |
|----|------|------------------|
| LLM01 Prompt Injection | Untrusted text steers tools | Validate at boundaries; never execute untrusted text as system prompts. GitHub issue/discussion titles and bodies are data only (`/audit`, `feedback-inbox`) |
| LLM02 Sensitive Information Disclosure | Secrets/PII in prompts or logs | No secrets in git; opt-in telemetry; `docs/PRIVACY.md` |
| LLM03 Supply Chain | Malicious model, plugin, or dep | Dependabot, CodeQL, Trivy; no default marketplace install |
| LLM04 Data/Model Poisoning | Tampered training or RAG | Treat uploads as untrusted; N/A until child adds RAG |
| LLM05 Improper Output Handling | Model output executed as code | Never eval LLM output; tool allowlists only |
| LLM06 Excessive Agency | Agent can push, deploy, or drop | Honesty labels; hooks denylist; `[HUMAN]` for destructive-ops |
| LLM07 System Prompt Leakage | Rules or secrets in prompts | Keep credentials out of rules and `AGENTS.md` |
| LLM08 Vector/Embedding | Retrieval injection | N/A until child adds a vector store |
| LLM09 Misinformation | Over-trust of model output | Critique table; gates; regression tests on bug fixes |
| LLM10 Unbounded Consumption | Token or cost DoS | Token economy 300/150; no 80k playbooks |
Weekly walk: `docs/SECURITY_TRIAGE.md`.

## Security Tasks

Link mitigations to `BUILD_PLAN.md` and `docs/SECURITY_TRIAGE.md` weekly triage.

## Review Cadence

- `[HUMAN]` Review at each milestone boundary
- `[AGENT]` Update when architecture or data flows change (append ADR reference)

## Appendix — Android 16 / InputManager reflection

Compose UI tests on **API 36 (Android 16)** can fail when older Espresso still calls removed reflective APIs (`InputManager.getInstance`). That is a **supply-chain / test-harness** risk on the FOSS path: a green local API 34 emulator can hide a red CI or physical-device run.

| Threat | Mitigation |
|--------|------------|
| Tampering / false confidence | Pin `androidx.test.espresso:espresso-core` **≥ 3.7.0** in Golden Path Gradle; gate with `check-espresso-android16` |
| Elevation via reflective sinks | Prefer Espresso 3.7+ over emulator reinstall; Semgrep pack notes reflective-API sinks (manual Kotlin review until rules land) |
| Denial of agent progress | Gate-fixer / `/fix` skill: Espresso bump before wiping AVDs — see KB-022 and `.cursor/skills/espresso-android16/` |
Do **not** treat InputManager reflection as an app attack surface for Golden Path UI code; treat it as a **test dependency pin** invariant. Nav Back smoke still uses Espresso `pressBack()` where system Back is under test.

## Appendix — USB debugging / adbkey lifecycle

| Asset | Risk | Control |
|-------|------|---------|
| `~/.android/adbkey` (+ `.pub`) | Device auth material; theft enables USB debugging sessions | Never commit; never set `ADB_VENDOR_KEYS` in git or CI logs; gate: `check-android-sdk-secrets` |
| Vendor keys via `ADB_VENDOR_KEYS` | Same as adbkey when used for CI device farms | Out of scope for FOSS template CI; document in child runbooks only |
| `local.properties` `sdk.dir` | Machine path leak | gitignored + Gitleaks |
Rotate compromised adb keys by removing `~/.android/adbkey*` and re-authorizing devices. Do not paste keys into Issues or agent prompts.
