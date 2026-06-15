# Module F: Go Applications

> Optional stack — not in the default init stack picker. See `docs/OPTIONAL_STACKS.md` to opt in.

## Requirements (Verbatim)

- **Module pinning:** Commit `go.sum`; use `go mod tidy` before release tags.
- **Static analysis:** Run `go vet ./...` and `gofmt -l` (empty output) in CI.
- **Testing:** `go test ./...` with race detector on supported packages.

## Activation Checklist

- ⬜ Copy or keep `examples/go/` Golden Path stub
- ⬜ Set Go version in `go.mod` and CI
- ⬜ Enable vet/fmt/test in CI
- ⬜ Document Go version in `AGENT_MEMORY.md`

## Golden Path Reference

See `examples/go/` for a minimal `hello` command (MIT).

## Owner Labels for This Module

| Task type | Label |
|-----------|-------|
| Scaffold module, tests | `AGENT` |
| Go version policy | `HUMAN` |
| vet/fmt/test CI gates | `AUTO` |
