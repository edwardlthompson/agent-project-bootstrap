# Golden Path Go

Minimal `hello` command stub for agent-project-bootstrap.

## Commands

```bash
gofmt -l .
go vet ./...
go test ./...
go run .
```

## CI Integration

Runs in root `.github/workflows/ci.yml` **go** job when `examples/go/` exists and changed (path filter).
