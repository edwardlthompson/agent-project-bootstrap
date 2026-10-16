# Spec: `/shape` workflow

## Goal
First-timers turn a rough idea into a short buildable spec without writing app code.

## Trigger / users
Maintainer (or agent) runs `/shape` with a rough idea, or answers with `defaults` / `skip`.

## Requirements
- `.cursor/commands/shape.md`, `docs/help/SHAPE.md`, and `.clinerules/workflows/shape.md` follow: size gate → look → mirror → ≤5 Qs → write `docs/specs/{slug}.md` → one BUILD_PLAN `[AGENT][LOCAL]` row → stop.
- `docs/specs/_TEMPLATE.md` and `docs/PREFERENCES.md` stub exist (shape may offer preference append; ask first).
- Cheat sheet, registry, print sheet, `batch-commands.mdc`, and VS Code cheat sheet list `/shape`.
- `/tour` and `docs/help/TOUR.md` mention `/shape` once (near coach/ideas).
- Glossary: `/ideas` = what to build · `/shape` = one idea → spec · `/coach` = what next · `/plan` = how to implement.
- `bash scripts/check-batch-commands.sh` passes; registry counts updated.

## Out of scope
`/shape quick`; rewriting `/plan`; app/Golden Path features; forcing Plan mode; Cloud-only defaults.

## Acceptance checks
- Sample `/shape` yields a ≤40-line `docs/specs/{slug}.md` and one 🔲 BUILD_PLAN row.
- Question options use blank lines between a/b/c (not cramped one-line a/b/c).
- Cheat sheet, tour, and glossary mention `/shape`.
- `check-batch-commands` exits 0.

## Assumptions (flagged)
- Atomic command (not a super); Build-moment on the cheat sheet.
- Slug derived from idea title.
- `docs/specs/` = pre-build shaping; `docs/features/` stays for shipped feature docs.

## Open questions
None for slice 1 (`defaults`).

## Files likely touched
`.cursor/commands/shape.md`, `.clinerules/workflows/shape.md`, `docs/help/SHAPE.md`, `docs/specs/_TEMPLATE.md`, `docs/PREFERENCES.md`, `docs/BATCH_COMMANDS.md`, `docs/help/BATCH_COMMANDS.md`, `docs/help/batch-commands-print.html`, `.cursor/rules/batch-commands.mdc`, `docs/help/TOUR.md`, `.cursor/commands/tour.md`, `docs/help/GLOSSARY.md`, `docs/help/VSCODE_COMMANDS.md` (optional: `PROMPT_LIBRARY.md`, `AGENTS.md`).
