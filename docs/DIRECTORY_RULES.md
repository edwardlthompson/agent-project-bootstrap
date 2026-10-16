# Cursor.Directory rule curation

Playbook for [cursor.directory/generate](https://cursor.directory/generate). **AGENTS.md stays Sacred** ([ADR-0005](adr/0005-no-second-memory-tree.md)).

## When

Sprint 0 / after stack selection, or when adopting a new stack module.

## Steps

1. Open Directory generate (or a curated catalog) for the **active** Golden Path (e.g. Vite/TypeScript/PWA for `web` — not Next.js unless the child uses Next).
2. Pick at most **3** useful rules. Prefer stack-scoped practices over always-on law.
3. Ask the human to confirm before writing files.
4. Write either:
   - a short section under `modules/{stack}/MODULE.md`, and/or
   - `.cursor/rules/{stack}-practices.mdc` with **`globs`** for `examples/{stack}/**` (never blank globs + alwaysApply unless reviewed).
5. Do **not** overwrite `AGENTS.md`, `AGENT.md`, or invent a second memory tree.

## Checklist (init / bootstrap)

- [ ] Directory rules reviewed for active stack
- [ ] Human confirmed the shortlist
- [ ] Any new `.mdc` declares `globs`
- [ ] Cap ≤3 stack practice files
