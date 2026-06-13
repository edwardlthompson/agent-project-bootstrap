# Start Here

> **Read this file first** — whether you are a human or a Cursor agent.

## What is this?

`agent-project-bootstrap` is a **GitHub Template Repository** for bootstrapping FOSS projects with Cursor agents.

## Which mode are you in?

- **Bootstrap:** New project from **Use this template** → read `INITIALIZATION_PROMPT.md` next
- **Reference:** Existing project using this repo as rules reference → read `FOR_AGENTS.md` next

## Bootstrap Read Order

1. `docs/START_HERE.md`
2. `docs/INITIALIZATION_PROMPT.md`
3. `AGENTS.md`
4. `BUILD_PLAN.md` Sequential lane
5. Active `modules/{stack}/MODULE.md` only
6. Active `examples/{stack}/` only

## Reference Read Order

1. `docs/START_HERE.md`
2. `docs/FOR_AGENTS.md`
3. `TEMPLATE_INDEX.json`
4. `AGENTS.md`
5. Matching `modules/{stack}/MODULE.md` only

## Do Not Read Yet

- Inactive `examples/` folders
- `KNOWLEDGE_BASE.md` (empty)
- `docs/MAINTAINING_THE_TEMPLATE.md` (maintainers only)

## BUILD_PLAN Labels

`AGENT` | `HUMAN` | `ADB` | `AUTO` — filter with `grep '\[AGENT\]' BUILD_PLAN.md`

## Agent Prompts

**Bootstrap:** Read @docs/START_HERE.md and @docs/INITIALIZATION_PROMPT.md. Follow Section 8. Use BUILD_PLAN Sequential lane.

**Reference:** Read @docs/FOR_AGENTS.md and @TEMPLATE_INDEX.json. Apply matching rules. Do not copy examples/ wholesale.
