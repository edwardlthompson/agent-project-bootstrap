# Post-template clone customization helper
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

Write-Host "=== agent-project-bootstrap init ===" -ForegroundColor Cyan
Write-Host ""

$ProjectName = Read-Host "Project name"
$ProjectPurpose = Read-Host "One-line purpose"
$Stack = Read-Host "Primary stack (web/python/android/multi)"
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
        Set-Content $path $content -Encoding UTF8
    }
}

$config = Get-Content (Join-Path $Root ".template-update.json") -Raw | ConvertFrom-Json
$config.check_interval = $Interval
$config | ConvertTo-Json -Depth 5 | Set-Content (Join-Path $Root ".template-update.json") -Encoding UTF8

$CodeOwner = Read-Host "GitHub username for CODEOWNERS (without @)"
if ($CodeOwner) {
    $codeownersPath = Join-Path $Root ".github/CODEOWNERS"
    if (Test-Path $codeownersPath) {
        $co = Get-Content $codeownersPath -Raw
        $co = $co -replace '@\[PROJECT_OWNER\]', "@$CodeOwner"
        [System.IO.File]::WriteAllText($codeownersPath, $co)
    }
}

$About = "$ProjectName - $ProjectPurpose. Built with agent-project-bootstrap. FOSS MIT."
@"
# GitHub About Block

## Draft Description (edit to <=350 chars)

$About

## Topics

Add topics relevant to your project and stack.
"@ | Set-Content (Join-Path $Root "docs/GITHUB_ABOUT.md") -Encoding UTF8

$Prune = Read-Host "Prune unused examples/modules? (y/N)"
if ($Prune -eq "y" -or $Prune -eq "Y") {
    switch ($Stack) {
        "web" { Remove-Item -Recurse -Force examples/python, examples/android, modules/python, modules/android, modules/lightroom -ErrorAction SilentlyContinue }
        "python" { Remove-Item -Recurse -Force examples/web, examples/android, modules/web, modules/android, modules/lightroom -ErrorAction SilentlyContinue }
        "android" { Remove-Item -Recurse -Force examples/web, examples/python, modules/web, modules/python, modules/lightroom -ErrorAction SilentlyContinue }
        default { Write-Host "Keeping all examples (multi-stack)" }
    }
}

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
Write-Host "  2. Enable Dependabot alerts + private vulnerability reporting: docs/SECURITY_TRIAGE.md"
Write-Host "  3. Configure branch protection on main (required checks, linear history)"
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
