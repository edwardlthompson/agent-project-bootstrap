# News Inbox

Auto-collected inbox of news, upstream updates, security fixes, and ideas relevant to this repo, appended daily by News Bot.
A Cursor planning agent should review these items and fold the useful ones into BUILD_PLAN; entries are append-only, newest at the bottom.


## 2026-11-13

**News and updates**

- Wave of npm malware posing as MCP/agent tools (e.g. karma365-mcp, @rclaude/darwin-arm64, helper-agent); advisories say treat machines as compromised. [source](https://github.com/advisories/GHSA-72xc-q3v8-7grp)
- GitHub will pause Dependabot alerts on repos with no activity in the past year starting Dec 8, 2026; a push re-enables them. [source](https://github.blog/changelog/2026-11-10-dependabot-alerts-will-pause-on-inactive-repositories)
- MCP reference servers v2.4.0 fix 6 vulnerabilities (filesystem symlink escapes, git config command execution, fetch). [source](https://github.com/modelcontextprotocol/servers/releases/tag/v2.4.0)
- Modern Web Guidance 1.0 from Chrome, Edge, Firefox and MDN: an official coding-agent skill plus `legacy-scan` that flags legacy JS/CSS. [source](https://github.com/GoogleChrome/modern-web-guidance/releases/tag/v1.0.0)
- GitHub Blog guide to portable agent skills (SKILL.md that runs across agents). [source](https://github.blog/ai-and-ml/github-copilot/build-once-run-on-any-agent-a-practical-guide-to-agent-skills/)
- 'Enforcement over alignment': enforce must-happen agent rules with hooks, schemas, and state gates instead of more prompting. [source](https://blog.imjackofitall.com/posts/2026-11-12/)
- Issue types and issue fields (Priority, Effort, dates) are now available on personal-account repos. [source](https://github.blog/changelog/2026-11-11-issue-types-and-fields-are-available-for-personal-accounts)
- uv 0.13.8 (credential files now 0600, Python 3.16.0a2) and Ruff 0.17.5 (autofix bug fixes) released. [source](https://github.com/astral-sh/uv/releases/tag/0.13.8)

**Tasks for the planning agent**

- [x] Pin and allowlist MCP server packages in templates — Agent/MCP package names are an active npm malware lure, so unpinned `npx -y` in descendant configs is a real risk. Label: `[AGENT][LOCAL]` · Priority: P1 · https://github.com/advisories/GHSA-72xc-q3v8-7grp (synced to BUILD_PLAN)
- [x] Document Dependabot inactive-repo pause in the template — Descendants that go quiet lose Dependabot alerts from Dec 8 unless they get a push. Label: `[AGENT][LOCAL]` · Priority: P2 · https://github.blog/changelog/2026-11-10-dependabot-alerts-will-pause-on-inactive-repositories (synced to BUILD_PLAN)
- [x] Audit template MCP examples for filesystem/git/fetch servers — If any descendant uses those reference servers, it must move to the patched v2.4.0 releases. Label: `[AGENT][LOCAL]` · Priority: P2 · https://github.com/modelcontextprotocol/servers/releases/tag/v2.4.0 (synced to BUILD_PLAN)
- [ ] Offer Modern Web Guidance as a skill for web descendants — Gives web children an official, versioned agent skill and a legacy-pattern scan. Label: `[AGENT][LOCAL]` · Priority: P3 · https://github.com/GoogleChrome/modern-web-guidance/releases/tag/v1.0.0
- [ ] Package sprint and update-check procedures as portable skills — Lets every descendant reuse the same procedures across agents. Label: `[AGENT][LOCAL]` · Priority: P3 · https://github.blog/ai-and-ml/github-copilot/build-once-run-on-any-agent-a-practical-guide-to-agent-skills/
- [ ] Turn key template rules into hook or CI gates — Enforced gates are more reliable than prose rules the agent may skip. Label: `[AGENT][LOCAL]` · Priority: P3 · https://blog.imjackofitall.com/posts/2026-11-12/
- [ ] Evaluate mapping BUILD_PLAN owners to issue types/fields — Native issue types/fields now work on personal repos and could mirror the label scheme. Label: `[AGENT][LOCAL]` · Priority: P3 · https://github.blog/changelog/2026-11-11-issue-types-and-fields-are-available-for-personal-accounts
- [ ] Bump uv and Ruff pins in template tooling — Picks up the credential-file permission fix and safer autofixes. Label: `[AGENT][LOCAL]` · Priority: P3 · https://github.com/astral-sh/uv/releases/tag/0.13.8

## 2026-11-14

**News and updates**

- wfx-loot campaign pushed a CI secret stealer into 17,000+ public repos using stolen GitHub credentials since Nov 10; an npm postinstall hook slipped past GitHub's workflow hold. IOCs: wfx-docs branch, .ci-xxxxxx.sh files, build-audit-*.yml workflows. [source](https://blog.gitguardian.com/wfx-loot-a-ci-secret-stealer-pushed-with-stolen-github-credentials/)
- Node.js November security releases (26.13.1 / 24.22.3 / 22.23.5) fix an unauthenticated HTTP/2 crash and an HTTPS heap leak that can expose TLS keys. [source](https://nodejs.org/en/blog/vulnerability/november-2026-security-releases)
- Stack Overflow blog: 'Your coding agent shouldn't grade its own homework' — only 9.6% of 1,000 AI-written tests were useful; argues for an independent fresh-context QA agent. [source](https://stackoverflow.blog/2026/11/13/your-coding-agent-shouldn-t-grade-its-own-homework/)

**Tasks for the planning agent**

- [x] Audit the repo for wfx-loot IOCs — Checks for the wfx-docs branch/PR, .ci-*.sh files, build-audit-*.yml workflows and new npm lifecycle hooks, since the campaign steals CI secrets and Cursor credentials. Label: `[AGENT][LOCAL]` · Priority: P1 · https://blog.gitguardian.com/wfx-loot-a-ci-secret-stealer-pushed-with-stolen-github-credentials/ (synced to BUILD_PLAN)
- [x] Default template CI installs to --ignore-scripts — Blocks postinstall-hook payloads like wfx-loot in every descendant repo. Label: `[AGENT][LOCAL]` · Priority: P2 · https://blog.gitguardian.com/wfx-loot-a-ci-secret-stealer-pushed-with-stolen-github-credentials/ (synced to BUILD_PLAN)
- [x] Bump pinned Node to 24.22.3 or 26.13.1 — Picks up fixes for a high-severity HTTP/2 crash and HTTPS heap leak. Label: `[AGENT][LOCAL]` · Priority: P2 · https://nodejs.org/en/blog/vulnerability/november-2026-security-releases (synced to BUILD_PLAN)
- [ ] Add an independent-verifier step to /verify — A fresh-context reviewer that cannot edit tests catches what the coding agent's own tests miss. Label: `[AGENT][LOCAL]` · Priority: P3 · https://stackoverflow.blog/2026/11/13/your-coding-agent-shouldn-t-grade-its-own-homework/

## 2026-11-15

**News and updates**

- Cursor traced its Oct 29 incident to a vendor-exposed key: attackers copied some non-Privacy-Mode agent traces (some with pasted credentials) and briefly planted a backdoored Claude Code extension (2.1.312/2.1.313); contained since Nov 1. [source](https://cursor.com/blog/security-incident-update) · [IOCs](https://cursor.com/blog/claude-code-extension-security-notice)
- More agent-CLI lures flagged as npm malware: @claudecode/cli and zread CLI (all platform packages); treat any machine that installed them as compromised. [source](https://github.com/advisories/GHSA-vp2q-gp5r-xh5j) · [zread](https://github.com/advisories/GHSA-3429-mj25-c5wf)

**Tasks for the planning agent**

- [x] Add a "never paste secrets into agent chats or support" rule to the AGENTS.md contract — Agent traces can leak, as Cursor's incident showed, and every descendant inherits this contract. Label: `[AGENT][LOCAL]` · Priority: P2 · https://cursor.com/blog/security-incident-update (synced to BUILD_PLAN)
- [ ] Add @claudecode/cli, zread_cli and @zread/cli-* to the MCP/agent package denylist — Keeps template scripts and descendant MCP configs from installing the newest agent-lure malware. Label: `[AGENT][LOCAL]` · Priority: P3 · https://github.com/advisories/GHSA-vp2q-gp5r-xh5j

## 2026-11-16

**News and updates**

- GitHub Actions will block `pull_request_target` runs in public repos by default from Dec 2 unless an Actions event policy allows them; today (Nov 16) 12:00–14:00 AST is the second brownout. [source](https://github.blog/changelog/2026-11-02-pull_request_target-blocked-by-default-december-2/)
- Git 2.56.1 (Nov 10) fixes 6 vulnerabilities, including code execution on recursive clone (CVE-2026-111760); backports 2.55.1–2.50.2 and Git for Windows 2.56.1 shipped the same day; GitHub is patching hosted runners. [source](https://github.blog/open-source/git/git-security-vulnerabilities-announced-7/)
- Google Antigravity 2.32.0 adds Dynamic Workflows: a reviewable, saved Python script fans work out to sub-agents that return JSON-Schema-checked results (SDK 0.1.22 `beta.workflows`). [source](https://antigravity.google/docs/dynamic-workflows/) · [changelog](https://antigravity.google/docs/changelog)

**Tasks for the planning agent**

- [x] Fail validate-workflow-actions on `on: pull_request_target` — The decision log already rejects it, and a check stops descendants from shipping workflows that break when GitHub blocks them on Dec 2. Label: `[AGENT][LOCAL]` · Priority: P2 · https://github.blog/changelog/2026-11-02-pull_request_target-blocked-by-default-december-2/ (synced to BUILD_PLAN)
- [x] Update Git to 2.56.1+ on dev hosts and have the template update checker warn below the patched version — Every descendant is cloned and recursively updated on these hosts, so an old Git is a code-execution risk. Label: `[HUMAN]` · Priority: P2 · https://github.blog/open-source/git/git-security-vulnerabilities-announced-7/ (synced to BUILD_PLAN)
- [ ] Prototype a saved fan-out script for /verify in the Antigravity adapter docs — One schema-bound reviewer per changed file gives a reviewable, re-runnable verify step for Antigravity users. Label: `[AGENT][LOCAL]` · Priority: P3 · https://antigravity.google/docs/dynamic-workflows/

## 2026-11-18

Catch-up for Nov 17–18 (the daily brief did not run those mornings).

**News and updates**

- Both `pull_request_target` brownouts (Nov 9 and Nov 16) have passed, and MultiAppShare-'s `.github/workflows/pr-title.yml` still uses `pull_request_target`. The default block becomes permanent on Dec 2. [source](https://github.blog/changelog/2026-11-02-pull_request_target-blocked-by-default-december-2/)
- Unauthorized PyPI releases 1.26.1 and 1.26.2 of Microsoft's `agent-framework` (Nov 17, now removed) dropped a `.pth` hook that stole env secrets, credential files, and Azure/GitHub OIDC tokens on every Python start. Pin to 1.26.0 or don't install it; treat any hit as compromised. [source](https://www.wiz.io/blog/malicious-version-of-microsofts-agent-framework-published-to-pypi) · [uv 0.13.9](https://github.com/astral-sh/uv/releases/tag/0.13.9) rejects wheels advertised under a different package name.
- MCP reference servers v2.5.0 fix eight vulnerabilities in `mcp-server-git`, `@modelcontextprotocol/server-filesystem` and `server-everything` (git maintenance/hooks, symlink directory swaps, NAT64 SSRF). Upgrade git to 2026.11.18 and filesystem to 2.4.0 (pin date-versioned installs explicitly). [source](https://github.com/modelcontextprotocol/servers/releases/tag/v2.5.0)
- MCP Inspector 2.16.0 and 1.0.6 cap SSE line and event size to stop an unbounded-buffer denial of service (GHSA-3xgv-mvj6-g78r). [source](https://github.com/modelcontextprotocol/inspector/releases/tag/2.16.0) · [v1](https://github.com/modelcontextprotocol/inspector/releases/tag/1.0.6)

**Tasks for the planning agent**

- [x] Confirm agent-framework 1.26.1/1.26.2 is absent and add a denylist plus .pth hook check — The template should keep descendants off the compromised releases and teach them to reject unexpected Python startup hooks. Label: `[AGENT][LOCAL]` · Priority: P2 · https://www.wiz.io/blog/malicious-version-of-microsofts-agent-framework-published-to-pypi (synced to BUILD_PLAN)
- [x] Upgrade template MCP git/filesystem/everything servers to the v2.5.0 patches — v2.4.0 left eight more git/filesystem/SSRF bugs; date-versioned filesystem installs will not move to 2.4.0 on their own. Label: `[AGENT][LOCAL]` · Priority: P2 · https://github.com/modelcontextprotocol/servers/releases/tag/v2.5.0 (synced to BUILD_PLAN)
- [x] Upgrade MCP Inspector to 2.16.0 or 1.0.6 if the template documents it — A malicious MCP server could previously crash the Inspector proxy with an unbounded SSE stream. Label: `[AGENT][LOCAL]` · Priority: P2 · https://github.com/modelcontextprotocol/inspector/releases/tag/2.16.0 (synced to BUILD_PLAN)

## 2026-11-19

**News and updates**

- Update on the agent-framework PyPI compromise: Wiz ties the malicious uploads to a stolen Microsoft ESRP release-signing certificate, and a same-day PyPI account was listed on 14 Microsoft projects (including Semantic Kernel and AutoGen). The bad wheels were live 39 minutes (427 downloads); 1.26.2 also requested GitHub Actions/Azure OIDC tokens, so treat them as exposed for workflows with `id-token: write`. No repo here depends on semantic-kernel or autogen; the existing P2s still apply. [source](https://sxz.io/microsoft-agent-framework-pypi-credential-stealer-esrp-certificate-14-projects/)
- Claude Code 2.1.327/2.1.328: `claude mcp add-json -` reads server JSON from stdin, a bug that deleted other top-level keys from project `.mcp.json` is fixed, and mcp_tool hooks gain `"onFailure": "block"`. [2.1.327](https://github.com/anthropics/claude-code/releases/tag/v2.1.327) · [2.1.328](https://github.com/anthropics/claude-code/releases/tag/v2.1.328)
- "The App Works. Here Is What the Agent Never Checked.": five holes agent-built apps keep shipping (missing record ownership checks, keys in git, user-controlled admin flags, browser-trusted payments, agents on the live DB). [source](https://lambdalynx.dev/vibe-coding-security/)

**Tasks for the planning agent**

- [ ] Add a Claude Code line to docs/MCP_RECIPES.md: use `claude mcp add-json -` with the same pinned server JSON and require Claude Code 2.1.327+ for project `.mcp.json` edits — older versions silently drop other tools' servers and `$schema` from a shared .mcp.json, and stdin keeps tokens off the command line. Label: `[AGENT][LOCAL]` · Priority: P3 · https://github.com/anthropics/claude-code/releases/tag/v2.1.327
- [ ] Add an "authz & payments" gate to the /verify checklist for the web/node Golden Path (two-account ownership test, server-side role check, server-verified payments, agent never on the prod DB) — gitleaks/semgrep catch keys but not the logic holes agents skip. Label: `[AGENT][LOCAL]` · Priority: P3 · https://lambdalynx.dev/vibe-coding-security/

## 2026-11-20

**News and updates**

- Gradle 9.9.2 and 8.14.8 (Nov 19) fix four High-severity build-tool bugs: SFTP repositories didn't verify host keys, transitive snapshot dependencies skipped dependency verification, TestKit used a predictable temp directory, and the daemon registry was briefly readable by other local users. 9.9.2 also fixes a 9.9.0 plugin-resolution regression with registries that answer 401. Wrappers older than 9.9.1/8.14.7 also miss the earlier Critical fix (version-catalog values run as code). [9.9.2 notes](https://docs.gradle.org/9.9.2/release-notes.html) · [8.14.8 notes](https://docs.gradle.org/8.14.8/release-notes.html)
- ETSI published EN 301 549 4th edition (Nov 17), the European Accessibility Act's harmonised ICT accessibility standard: web, document and software requirements move to current guidance (reported as WCAG 2.2), cognitive-accessibility requirements get stronger, and conformance/testing methodology is added. ETSI also published EN 303 919 for accessible emergency communications. [ETSI](https://www.etsi.org/newsroom/press-releases/etsi-advances-digital-accessibility-across-europe-with-two-standards/) · [WCAG 2.2 detail](https://ifdb.io/en/en-301-549-v4-1-1-wcag-2-2-becomes-the-benchmark-what-businesses-need-to-know-now/)
- A wave of DNS-rebinding advisories hit local HTTP MCP servers (obsidian-sync-mcp, @doist/todoist-mcp, jupyter-mcp-server, k8s-mcp-server): each bound to loopback but didn't validate the Host/Origin header (or skipped auth on HTTP), so any web page the user visited could rebind a hostname to 127.0.0.1 and call every MCP tool. [obsidian-sync-mcp](https://github.com/advisories/GHSA-mx6p-3fg7-v6pj) · [todoist-mcp](https://github.com/advisories/GHSA-833v-v58w-294h) · [jupyter-mcp-server](https://github.com/advisories/GHSA-9x8x-crjq-g64h) · [k8s-mcp-server](https://github.com/advisories/GHSA-m932-63jc-4jqq)
- Socket's "Hardening GitHub Actions Against Insider Threats" (part 2) covers stolen maintainer tokens rather than malicious PRs: phishing-resistant 2FA, no long-lived tokens, rulesets restricting who can change .github/workflows/**, Actions execution protections, OIDC trusted publishing, a "Restrict deletions on all branches" ruleset that blocks the cover-tracks step, and alerts on config events (deploy key added, ruleset relaxed, repo flipped public). GitGuardian's React2STEAL write-up shows hijacked accounts quietly gaining scan.yml workflows. [Socket](https://socket.dev/blog/hardening-github-actions-against-insider-threats) · [GitGuardian](https://blog.gitguardian.com/react2steal-hijacked-github-accounts-exploit-react2shell-and-publish-stolen-secrets/)

**Tasks for the planning agent**

- [x] Bump the Gradle wrapper 9.9.1 to 9.9.2 and commit the regenerated wrapper jar and distributionSha256Sum — the patch fixes four High build-tool vulnerabilities (SFTP host keys, snapshot dependency verification, TestKit temp dir, daemon registry). Run ./gradlew wrapper --gradle-version=<ver> in the wrapper (examples/android/gradle/wrapper/). Label: `[AGENT][LOCAL]` · Priority: P2 · https://docs.gradle.org/9.9.2/release-notes.html (synced to BUILD_PLAN)
- [ ] Point the /ux-review checklist and docs/UX_LAW.md at WCAG 2.2 AA / EN 301 549 v4 and add the 2.2-only criteria (target size minimum, focus not obscured, dragging alternatives, accessible authentication, redundant entry) — APB is the template every repo inherits, and the new children (prism-mail, open-fences) start from it; EU legal pressure on hobby FOSS is low. Label: `[AGENT][LOCAL]` · Priority: P3 · https://www.etsi.org/newsroom/press-releases/etsi-advances-digital-accessibility-across-europe-with-two-standards/
- [ ] Add a "local HTTP MCP servers" rule to docs/MCP_RECIPES.md: prefer stdio; if a server must speak HTTP, bind loopback, validate Host and Origin, and require a token even in "local" mode — children such as selfchronicle copy this pattern, and the MCP guidance covers pinning but not transport. Label: `[AGENT][LOCAL]` · Priority: P3 · https://github.com/advisories/GHSA-mx6p-3fg7-v6pj
- [ ] Add a "Restrict deletions" default-branch ruleset and a workflow-path restriction (.github/workflows/**) to the template's repo-hygiene guidance (docs/REPO_HYGIENE.md) so children set them up at init — they block the cover-tracks and silent-workflow steps of a stolen-token takeover at no Actions cost. Label: `[AGENT][LOCAL]` · Priority: P3 · https://socket.dev/blog/hardening-github-actions-against-insider-threats

## 2026-11-25

**News and updates**

- uv 0.13.10 (Nov 24) fixes [GHSA-vjvj-3m3f-fgmm](https://github.com/astral-sh/uv/security/advisories/GHSA-vjvj-3m3f-fgmm) (Low): a crafted ZIP wheel or sdist can install different file contents under uv than under pip, because the two disagree on ZIP data-descriptor sizes. Exploitation needs someone to install an attacker-controlled distribution; PyPI now rejects many of these malformed ZIPs, but local and third-party indexes may not. The open template pin still cites 0.13.8. [0.13.10](https://github.com/astral-sh/uv/releases/tag/0.13.10)

- GitGuardian planted AWS keys in Docker Hub images and saw bots use them in 7.86 seconds; they also argue that provider Zero Data Retention is not a control, because bait prompts leaked keys from three AI providers and those keys were tested within hours. The practical fixes are .dockerignore (so `.gitignore` secrets do not land in image layers), agent-config hygiene, and redaction before a prompt leaves the laptop. [Docker Hub write-up](https://blog.gitguardian.com/docker-hub-secrets-ai-agentsuntitled/) · [ZDR write-up](https://blog.gitguardian.com/zero-data-retention-ai-prompts/)

- Vercel and shadcn released UI SDK, a library of UI behaviors (popup, selection, typeahead, and similar) that agents can compose into components and then operate without clicking through a screenshot. Better Stack's write-up notes that UI SDK can mark a control as needing a person, and in their test UI-SDK agents asked first, but ordinary browser-tool agents clicked through because they never see the mark. [UI SDK](https://ui-sdk.dev) · [GitHub](https://github.com/vercel-labs/ui) · [Better Stack](https://www.youtube.com/watch?v=ubK6Q53jKg8)

**Tasks for the planning agent**

- - [ ] Bump uv pins in template tooling to 0.13.10 or later (supersedes the older 0.13.8 pin) — rejects ZIP members whose descriptor size disagrees with the central directory, so uv and pip cannot be tricked into installing different bytes from the same archive. Label: `[AGENT][LOCAL]` · Priority: P3 · https://github.com/astral-sh/uv/security/advisories/GHSA-vjvj-3m3f-fgmm

- - [ ] Add a template rule that agent and CI Docker builds must use a `.dockerignore` that excludes `.env`, credential files, and agent config, and that `/verify` (or a pre-commit check) flags those paths in image build contexts — `.gitignore` does not apply to `docker build`, and bots are scraping public images for keys in seconds. Label: `[AGENT][LOCAL]` · Priority: P3 · https://blog.gitguardian.com/docker-hub-secrets-ai-agentsuntitled/

- - [ ] Evaluate UI SDK (and its 'needs a person' mark) as an optional recipe for agent-driven settings and approval UIs in the template — useful if descendants start shipping agent-operated interfaces, and the mark is only honored by agents that speak UI SDK. Label: `[AGENT][LOCAL]` · Priority: P3 · https://ui-sdk.dev
