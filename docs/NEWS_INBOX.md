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

- [ ] Pin and allowlist MCP server packages in templates — Agent/MCP package names are an active npm malware lure, so unpinned `npx -y` in descendant configs is a real risk. Label: `[AGENT][LOCAL]` · Priority: P1 · https://github.com/advisories/GHSA-72xc-q3v8-7grp
- [ ] Document Dependabot inactive-repo pause in the template — Descendants that go quiet lose Dependabot alerts from Dec 8 unless they get a push. Label: `[AGENT][LOCAL]` · Priority: P2 · https://github.blog/changelog/2026-11-10-dependabot-alerts-will-pause-on-inactive-repositories
- [ ] Audit template MCP examples for filesystem/git/fetch servers — If any descendant uses those reference servers, it must move to the patched v2.4.0 releases. Label: `[AGENT][LOCAL]` · Priority: P2 · https://github.com/modelcontextprotocol/servers/releases/tag/v2.4.0
- [ ] Offer Modern Web Guidance as a skill for web descendants — Gives web children an official, versioned agent skill and a legacy-pattern scan. Label: `[AGENT][LOCAL]` · Priority: P3 · https://github.com/GoogleChrome/modern-web-guidance/releases/tag/v1.0.0
- [ ] Package sprint and update-check procedures as portable skills — Lets every descendant reuse the same procedures across agents. Label: `[AGENT][LOCAL]` · Priority: P3 · https://github.blog/ai-and-ml/github-copilot/build-once-run-on-any-agent-a-practical-guide-to-agent-skills/
- [ ] Turn key template rules into hook or CI gates — Enforced gates are more reliable than prose rules the agent may skip. Label: `[AGENT][LOCAL]` · Priority: P3 · https://blog.imjackofitall.com/posts/2026-11-12/
- [ ] Evaluate mapping BUILD_PLAN owners to issue types/fields — Native issue types/fields now work on personal repos and could mirror the label scheme. Label: `[AGENT][LOCAL]` · Priority: P3 · https://github.blog/changelog/2026-11-11-issue-types-and-fields-are-available-for-personal-accounts
- [ ] Bump uv and Ruff pins in template tooling — Picks up the credential-file permission fix and safer autofixes. Label: `[AGENT][LOCAL]` · Priority: P3 · https://github.com/astral-sh/uv/releases/tag/0.13.8
