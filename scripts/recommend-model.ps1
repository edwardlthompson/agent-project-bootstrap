# Hardware-aware local model recommendation (opt-in).
$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
if (-not $Root) { $Root = (Resolve-Path (Join-Path $PSScriptRoot "..")).Path }
Set-Location $Root
$py = Get-Command python3 -ErrorAction SilentlyContinue
if (-not $py) { $py = Get-Command python -ErrorAction SilentlyContinue }
if (-not $py) { Write-Error "python3/python not found"; exit 1 }
& $py.Source (Join-Path $Root "scripts\recommend_model.py") @args
exit $LASTEXITCODE
