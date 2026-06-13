# For Agents

## Phased Loading

SessionStart → START_HERE.md → Mode → AGENTS.md → BUILD_PLAN Sequential → Active module → Plan Mode → Execute

## Token Economy

1. Never read all of `examples/` — active stack only
2. Never fill KNOWLEDGE_BASE.md with generic framework docs
3. Update memory files only at session start, milestone end, or architectural pivot
4. Read-before-write: @filename before edits
5. Sequential before Parallel in BUILD_PLAN

## Parallel Guardrails

- Branch: `feature/agent-[task-name]` per agent, separate worktree
- No overlapping file scopes
- Shared schema/types: sequential agent only first

## 3-Strike Rule

After 3 failed fix attempts: halt, summarize conflict, request human direction.

## Session Checkpoint

Write `.cursor-session-state`, clear chat, restore on restart, delete file.
