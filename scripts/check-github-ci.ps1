# Poll GitHub Actions for required workflows on a commit.
# Usage: scripts/check-github-ci.ps1 [-Ref SHA] [-WaitSeconds 300]
param(
    [string]$Ref = "",
    [int]$WaitSeconds = 0
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent (Split-Path -Parent $MyInvocation.MyCommand.Path)
Set-Location $Root

if (-not (Get-Command gh -ErrorAction SilentlyContinue)) {
    Write-Host "ERROR: gh CLI required (https://cli.github.com/)"
    exit 1
}

if (-not $Ref) { $Ref = "HEAD" }
$Ref = (git rev-parse $Ref).Trim()
$Required = @("CI", "Security Scan", "CodeQL")

$RepoJson = gh repo view --json nameWithOwner 2>$null
if (-not $RepoJson) {
    Write-Host "ERROR: run from a git repo with gh auth"
    exit 1
}
$Repo = (ConvertFrom-Json $RepoJson).nameWithOwner
$ShortRef = $Ref.Substring(0, [Math]::Min(7, $Ref.Length))
Write-Host "GitHub Actions status for $Repo @ $ShortRef"

$deadline = (Get-Date).AddSeconds($WaitSeconds)
while ($true) {
    $runs = gh run list --repo $Repo --commit $Ref --json workflowName,conclusion,status,url | ConvertFrom-Json
    $pending = 0
    $failed = 0

    foreach ($wf in $Required) {
        $run = $runs | Where-Object { $_.workflowName -eq $wf } | Select-Object -First 1
        if (-not $run) {
            Write-Host "WAIT ${wf}: no run yet"
            $pending++
            continue
        }
        switch ($run.conclusion) {
            "success" { Write-Host "OK   ${wf}: $($run.url)" }
            { $_ -in @("failure", "cancelled", "timed_out", "action_required") } {
                Write-Host "FAIL ${wf} ($($run.conclusion)): $($run.url)"
                $failed++
            }
            default {
                if ($run.status -eq "completed") {
                    Write-Host "FAIL ${wf} ($($run.conclusion)): $($run.url)"
                    $failed++
                } else {
                    Write-Host "WAIT ${wf} ($($run.status)): $($run.url)"
                    $pending++
                }
            }
        }
    }

    if ($failed -gt 0) {
        Write-Host "$failed required workflow(s) failed on GitHub"
        exit 1
    }
    if ($pending -eq 0) {
        Write-Host "All $($Required.Count) required workflows passed on GitHub"
        exit 0
    }
    if ($WaitSeconds -eq 0 -or (Get-Date) -ge $deadline) {
        Write-Host "INCOMPLETE: $pending workflow(s) still pending (use -WaitSeconds 300)"
        exit 1
    }
    Start-Sleep -Seconds 15
}
