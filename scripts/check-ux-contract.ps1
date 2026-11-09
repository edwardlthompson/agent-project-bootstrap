param(
    [string]$Root = (Split-Path -Parent $PSScriptRoot),
    [switch]$Baseline
)
$env:PYTHONPATH = Join-Path $Root "scripts/lib"
python3 (Join-Path $Root "scripts/check-ux-contract.py") --baseline $Root
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
