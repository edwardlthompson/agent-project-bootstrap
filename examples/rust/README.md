# Golden Path Rust

Minimal `hello` binary stub plus About (version + donate) and crash-text sanitizer (std-only).

## Commands

```bash
cargo fmt --check
cargo clippy -- -D warnings
cargo test
cargo run
cargo run -- --ready   # {"status":"ok"} on stdout; JSON log on stderr

```

## CI Integration

Runs in root `.github/workflows/ci.yml` **rust** job when `examples/rust/` exists and changed (path filter).
