# Brand (any IDE)

Ask your agent to rebrand the child product using the branding playbook. In Cursor you can type `/brand` instead.

Replaces Golden Path placeholder logos, colors, and pitch. Does not touch parent template art under `branding/template/`.

## Paste prompt

```
Read docs/help/BRAND.md and branding/BRANDING.md. Run the creative brief, propose 3 marks, wait for my pick, then replace branding/assets/, tokens, and product.json. Sync and align UI strings. Do not edit branding/template/.

```

## Recipe

1. Creative brief: audience, one promise, three adjectives, do/don’t (`branding/BRANDING.md`).
2. Propose 3 marks; human picks one.
3. Replace `branding/assets/*` (same filenames), edit `design-tokens/design-tokens.json` and `branding/product.json` (`mode: product`).
4. `python3 scripts/sync-design-tokens.py` then `python3 scripts/generate-project-readme.py`.
5. Align locales / `strings.xml` / manifest / splash continuity.

See [`AGENT_PORTABILITY.md`](../AGENT_PORTABILITY.md) if your tool has no slash commands.
