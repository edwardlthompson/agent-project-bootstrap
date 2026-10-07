# Brand voice

Placeholder voice for Golden Path / child products. Replace when you have a real brand. Run `/brand` to align voice with the new mark and `product.json`.

## Tone

- **Clear and direct** — say what the app does in one breath
- **FOSS-first** — emphasize user control, privacy, and open distribution
- **Confident, not hype** — no “revolutionary” / “ultimate” filler
- **Agent-friendly** — short paragraphs, scannable bullets, concrete next steps

## Pitch formulas

Use these shapes when filling `product.json` or README hero copy:

1. **Outcome → proof → CTA**  
   *Outcome:* what the user gets. *Proof:* FOSS / privacy / stack fact. *CTA:* init, install, or open Settings.  
   Example: “Ship offline-ready FOSS alarms without a Google account. MIT, no tracking. Clone and `/tour`.”

2. **Who → job → without**  
   “For [who] who need to [job] without [pain].”

3. **Tagline test** — if you delete the product name, the tagline still makes sense and stays under ~12 words.

Keep the elevator pitch to **1–2 sentences**. Features are benefits (“offline-ready PWA”), not internals (“uses Vite”).

## Pitch rules

1. Lead with the user outcome, then the stack.
2. Keep the elevator pitch to 1–2 sentences.
3. Features are benefits (“offline-ready PWA”), not internals (“uses Vite”).
4. README hero + badges must still read if images fail to load (alt text / headings).

## Do / don’t

| Do | Don’t |
|----|-------|
| Specific verbs: ship, verify, prune, release | Vague adjectives without proof |
| Link to SECURITY / CONTRIBUTING | Promise proprietary store SDKs |
| Match `product.json` name to UI `app.title` | Invent a second product name in docs |
| Write splash-adjacent copy that matches first-frame chrome | Treat donate/update prompts as brand splash |
