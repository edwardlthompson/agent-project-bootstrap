# Threat Model

> Draft during Sprint 1 before Golden Path ships. Link security tasks in `BUILD_PLAN.md`.

## Scope

| Item | Value |
|------|-------|
| Project | [PROJECT_NAME] |
| Stack | [INSERT PLATFORM / TECH STACK HERE] |
| Methodology | STRIDE (adapt per stack: OWASP ASVS for web, MASVS for mobile) |

## Trust Boundaries

```text
[User] --> [Client App / PWA] --> [API / Backend] --> [Data Store]
                |                      |
           Local storage          External services
```

Document your actual boundaries after architecture is defined.

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

## Security Tasks

Link mitigations to `BUILD_PLAN.md` and `docs/SECURITY_TRIAGE.md` weekly triage.

## Review Cadence

- `[HUMAN]` Review at each milestone boundary
- `[AGENT]` Update when architecture or data flows change (append ADR reference)
