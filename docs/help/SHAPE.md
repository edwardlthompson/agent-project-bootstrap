# Shape (any IDE)

Turn a rough idea into a short buildable spec. No app code. Cursor: `/shape`.

## Paste

```
Read docs/help/SHAPE.md. Shape my idea into docs/specs/{slug}.md. Do not implement.
```

## Recipe

1. **Size gate** — trivial → offer to just do it; several features → split, shape the first; `defaults`/`skip` → no questions.
2. **Look** — README, BUILD_PLAN, touched files; **must read** `docs/PREFERENCES.md` (patterns + security). One line that matters.
3. **Mirror** — "Here's what I heard…" Invite correction.
4. **Questions** (max 5) — blank lines between options (never cramped `a/b/c` on one line):

```text
1. · <plain question>
   · Why it matters: <≤8 words>

   a) <option>
   b) <option> ★ recommended
   c) <option>

   or tell me
```

   Order: trigger · done-looks-like · out of scope · must-not-break · concrete example.
   End: `Reply like \`1a 2b 3 skip\` — or say \`defaults\`.`

5. Write `docs/specs/{slug}.md` (≤40 lines) from `_TEMPLATE.md`.
6. Add one BUILD_PLAN `[AGENT][LOCAL]` row. Stop. Offer PREFERENCES append (ask first).

## Split

`/ideas` = what to build · `/shape` = one idea → spec · `/coach` = what next · `/plan` = how to implement.
