# Golden Path Node (Hono API)

Minimal typed HTTP API using Hono, TypeScript strict mode, and Vitest.

## Commands

```bash
npm ci
npm run lint
npm test
npm run dev
```

## Routes

- `GET /health` — readiness probe
- `GET /greet/:name?` — sample JSON handler

## CI Integration

Runs in the root `.github/workflows/ci.yml` `node` job.
