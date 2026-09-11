# Module G: Go Applications

> Optional stack — not in the default init stack picker. See `docs/OPTIONAL_STACKS.md` to opt in.

## Requirements (Verbatim)

- **Module pinning:** Commit `go.sum`; use `go mod tidy` before release tags.
- **Static analysis:** Run `go vet ./...` and `gofmt -l` (empty output) in CI.
- **Testing:** `go test ./...` with race detector on supported packages.

## Activation Checklist

> **Child-activation:** After `init-project` with Go kept (or restored from `--keep-optional`), run this list before the first Go PR. Gate: `python3 -m unittest tests.test_rust_go_module_checklist`.

- 🔲 Copy or keep `examples/go/` Golden Path stub
- 🔲 Set Go version in `go.mod` and CI
- 🔲 Enable vet/fmt/test in CI
- 🔲 Add gomod to `.github/dependabot.yml` (`directory: /examples/go`, group `go-dependencies`)
- 🔲 Document Go version in `AGENT_MEMORY.md`

## Golden Path Reference

See `examples/go/` for a minimal `hello` command (MIT).

## CodeQL

Root `.github/workflows/codeql.yml` does **not** analyze `examples/go/` (optional stack). Use `go vet` and govulncheck (when adopted) in CI when this module is active. See `docs/OPTIONAL_STACKS.md`.

## Owner Labels for This Module

| Task type | Label |
|-----------|-------|
| Scaffold module, tests | `AGENT` |
| Go version policy | `HUMAN` |
| vet/fmt/test CI gates | `AUTO` |
