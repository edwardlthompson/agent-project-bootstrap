# Golden Path Python

uv + ruff + mypy + pytest CLI stub for agent-project-bootstrap.

## Commands

```bash
uv sync --all-extras
uv run pytest
uv run ruff check .
uv run ruff format --check .
uv run mypy src
uv run hello FOSS
```

## Features

- Strict type hints validated by mypy
- ruff lint and format checks
- pytest with 90% coverage budget
- Pure business logic in `greet.py`, CLI in `cli.py`

## CI Integration

Runs in root `.github/workflows/ci.yml` Python job (`uv run pytest`) and weekly health check pytest smoke when `examples/python/` is present.
