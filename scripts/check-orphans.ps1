param(
    [string]$Root = (Split-Path -Parent $PSScriptRoot),
    [string]$Baseline = ""
)
$env:PYTHONPATH = Join-Path $Root "scripts/lib"
$argsList = @((Join-Path $Root "scripts/check-orphans.py"))
if ($Baseline) { $argsList += @("--baseline", $Baseline) }
$argsList += $Root
python3 @argsList
if ($LASTEXITCODE -ne 0) { exit $LASTEXITCODE }
