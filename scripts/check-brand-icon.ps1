param([string]$Root = (Split-Path -Parent $PSScriptRoot))
$env:PYTHONPATH = Join-Path $Root "scripts/lib"
python3 (Join-Path $Root "scripts/check-brand-icon.py") $Root
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
