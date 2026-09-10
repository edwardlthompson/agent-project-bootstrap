# Winget Manifest Stub

Publish runbook: [`docs/WINGET.md`](../../docs/WINGET.md).

Committed example (placeholder SHA-256, `example.com` URL):

```bash
bash scripts/validate-winget-stub.sh packaging/winget/example/manifest.yaml
```

```bash
bash scripts/generate-winget-manifest.sh Example.Publisher.App 1.2.3 packaging/winget
bash scripts/validate-winget-stub.sh packaging/winget/manifest.stub.yaml
```

Submit the filled YAML to https://github.com/microsoft/winget-pkgs. `[HUMAN]` opens that PR.
