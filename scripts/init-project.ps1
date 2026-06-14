# Post-template clone customization helper
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

Write-Host "=== agent-project-bootstrap init ===" -ForegroundColor Cyan
Write-Host ""

$ProjectName = Read-Host "Project name"
$ProjectPurpose = Read-Host "One-line purpose"
$Stack = Read-Host "Primary stack (web/python/android/multi/none)"
if (-not $Stack) { $Stack = "none" }
$ValidStacks = @("web", "python", "android", "multi", "none")
if ($ValidStacks -notcontains $Stack) {
    Write-Host "Invalid stack '$Stack'; defaulting to none (keep all examples)."
    $Stack = "none"
}
$Interval = Read-Host "Template update check interval (off/daily/weekly/monthly/on_session) [weekly]"
if (-not $Interval) { $Interval = "weekly" }

$files = @(
    "docs/INITIALIZATION_PROMPT.md",
    "AGENT_MEMORY.md"
)

foreach ($file in $files) {
    $path = Join-Path $Root $file
    if (Test-Path $path) {
        $content = Get-Content $path -Raw
        $content = $content -replace '\[INSERT PLATFORM / TECH STACK HERE\]', $Stack
        $content = $content -replace '\[INSERT DETAILED APP DESCRIPTION AND GOALS HERE\]', $ProjectPurpose
        [System.IO.File]::WriteAllText($path, $content, (New-Object System.Text.UTF8Encoding $false))
    }
}

$config = Get-Content (Join-Path $Root ".template-update.json") -Raw | ConvertFrom-Json
$config.check_interval = $Interval
$config | ConvertTo-Json -Depth 5 | Set-Content (Join-Path $Root ".template-update.json") -Encoding UTF8


$ReleaseRepo = Read-Host "GitHub owner/repo for app release checks (OWNER/REPO) [skip]"
$DonationUrl = Read-Host "Donation URL [skip]"
$AppExample = Join-Path $Root ".app-update.json.example"
$AppConfig = Join-Path $Root ".app-update.json"
if ((Test-Path $AppExample) -and -not (Test-Path $AppConfig)) { Copy-Item $AppExample $AppConfig }
if ($ReleaseRepo) {
  $app = Get-Content $AppConfig -Raw | ConvertFrom-Json
  $app.release_repo = $ReleaseRepo.Trim()
  $app | ConvertTo-Json -Depth 5 | Set-Content $AppConfig -Encoding UTF8
}
$DonExample = Join-Path $Root "donations.json.example"
$DonConfig = Join-Path $Root "donations.json"
if ((Test-Path $DonExample) -and -not (Test-Path $DonConfig)) { Copy-Item $DonExample $DonConfig }
if ($DonationUrl) {
  $don = Get-Content $DonConfig -Raw | ConvertFrom-Json
  $don.links = @(@{ label = "Donate"; url = $DonationUrl.Trim() })
  $don | ConvertTo-Json -Depth 5 | Set-Content $DonConfig -Encoding UTF8
}

$CodeOwner = Read-Host "GitHub username for CODEOWNERS (without @)"
if ($CodeOwner) {
    $codeownersPath = Join-Path $Root ".github/CODEOWNERS"
    if (Test-Path $codeownersPath) {
        $co = Get-Content $codeownersPath -Raw
        $co = $co -replace '@\[PROJECT_OWNER\]', "@$CodeOwner"
        [System.IO.File]::WriteAllText($codeownersPath, $co, (New-Object System.Text.UTF8Encoding $false))
    }
}

$About = "$ProjectName - $ProjectPurpose. Built with agent-project-bootstrap. FOSS MIT."
$aboutContent = @"
# GitHub About Block

## Draft Description (edit to <=350 chars)

$About

## Topics

Add topics relevant to your project and stack.
"@
[System.IO.File]::WriteAllText((Join-Path $Root "docs/GITHUB_ABOUT.md"), $aboutContent, (New-Object System.Text.UTF8Encoding $false))

$Pruned = $false
if ($Stack -eq "none") {
    Write-Host "Stack 'none': keeping all examples and modules."
} elseif ($Stack -eq "multi") {
    $Prune = Read-Host "Prune unused examples/modules? (y/N)"
    if ($Prune -eq "y" -or $Prune -eq "Y") {
        $Pruned = $true
        Write-Host "Keeping all examples (multi-stack)."
    }
} else {
    $Prune = Read-Host "Prune unused examples/modules? (y/N)"
    if ($Prune -eq "y" -or $Prune -eq "Y") {
        $Pruned = $true
        $toRemove = switch ($Stack) {
            "web" { @("examples/python", "examples/android", "modules/python", "modules/android", "modules/lightroom") }
            "python" { @("examples/web", "examples/android", "modules/web", "modules/android", "modules/lightroom") }
            "android" { @("examples/web", "examples/python", "modules/web", "modules/python", "modules/lightroom") }
            default { @() }
        }
        foreach ($item in $toRemove) {
            $target = Join-Path $Root $item
            if (Test-Path $target) { Remove-Item -Recurse -Force $target }
        }
    }
}

python3 scripts/init-stack-sync.py $Stack $Root ($Pruned.ToString().ToLower())
python3 scripts/sync-design-tokens.py 2> | Out-Null
Write-Host "Wrote .cursor/stack-selection.json and synced AGENT_MEMORY active modules."

Write-Host ""
Write-Host "=== Workflow validation ===" -ForegroundColor Cyan
if (Get-Command gh -ErrorAction SilentlyContinue) {
    bash scripts/validate-workflow-actions.sh
    if ($LASTEXITCODE -eq 0) {
        Write-Host "Workflow action refs validated via GitHub API."
    } else {
        Write-Host "WARN: validate-workflow-actions.sh failed. Fix refs before first push."
    }
} else {
    Write-Host "WARN: gh CLI not found. Install GitHub CLI and run:"
    Write-Host "  bash scripts/validate-workflow-actions.sh"
    Write-Host "See README.md and docs/SECURITY_TRIAGE.md for setup."
}

Write-Host ""
Write-Host "=== Done ===" -ForegroundColor Green
Write-Host ""
Write-Host "Next steps:"
Write-Host "  1. Review SECURITY.md, CODEOWNERS, playbooks, and .env.example"
Write-Host "  2. Run scripts/setup-github-repo.sh (or .ps1) for Dependabot alerts, private reporting, branch protection"
Write-Host "     See docs/SECURITY_TRIAGE.md if the script prints a manual checklist (API 422)"
Write-Host "  4. Open Cursor and paste:"
Write-Host ""
Write-Host "  Read @docs/START_HERE.md and @docs/INITIALIZATION_PROMPT.md."
Write-Host "  Follow Section 8 Startup Sequence."
Write-Host "  Use BUILD_PLAN.md Sequential lane first; respect AGENT/HUMAN/ADB/AUTO labels."
Write-Host ""
Write-Host "  5. After first push to main, poll required workflows:"
Write-Host "     pwsh scripts/check-github-ci.ps1 -WaitSeconds 300"
Write-Host ""
Write-Host "GitHub About draft: docs/GITHUB_ABOUT.md"
Write-Host "Stack selection: .cursor/stack-selection.json"
