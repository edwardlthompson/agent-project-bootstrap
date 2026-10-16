# Feature: product-brief-anti-amnesia

> Keep the original product brief across long bootstraps. `AGENT.md` is Sacred; `AGENTS.md` is stamped routing.

## Acceptance criteria

- ✅ `AGENT.md.example` ships on the template; live `AGENT.md` is optional here
- ✅ Init never overwrites `AGENT.md`
- ✅ After init, `BUILD_PLAN.md` Product (do not drift) contains the one-liner and keywords
- ✅ `check-agent-brief` fails if those strings vanish
- ✅ Always-on `.cursor/rules/product-brief.mdc` points agents at `AGENT.md` before About/donate
- ✅ When `AGENT.md` exists on a child, About/purpose surfaces must echo brief keywords (`check-agent-brief`)

## Smoke scenario

1. _Given_ a child `AGENT.md` with keywords `camera, messages, tame, neon`
2. _When_ `stamp_product_brief` then `check-agent-brief`
3. _Then_ BUILD_PLAN contains those keywords; stripping them fails the gate

## Container map

| Layer | Path |
|-------|------|
| Logic | `scripts/lib/agent_brief.py`, `stamp_product_brief.py`, `check_agent_brief.py` |
| View | `BUILD_PLAN.md` Product (do not drift) |
| Tests | `tests/test_agent_brief.py` |
| Wiring | `scripts/check-agent-brief.sh`, `validate-bootstrap.sh` |
## Tests

- Automated: yes — parse, stamp round-trip, stripped keywords fail
- Coverage: template without `AGENT.md` still requires the example

## Fallback validation

- Why tests are not feasible: N/A
- Command: `python3 scripts/agent-run.py check-agent-brief`

## Definition of Done

See `docs/FEATURE_MODULES.md`.
