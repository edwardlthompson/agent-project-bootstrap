# Poll GitHub Actions for required workflows on a commit.
# Usage: scripts/check-github-ci.ps1 [-Ref SHA] [-WaitSeconds 300] [-Jobs "Repo Hygiene,Feature Gate"]
param(
    [string]$Ref = "",
    [int]$WaitSeconds = 0,
    [string]$Jobs = ""
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

    if ($Jobs) {
        $ciRun = $runs | Where-Object { $_.workflowName -eq "CI" } | Select-Object -First 1
        if (-not $ciRun) {
            Write-Host "WAIT CI jobs: no CI run yet"
            $pending++
        } else {
            $runId = (gh run list --repo $Repo --commit $Ref --workflow CI --json databaseId | ConvertFrom-Json)[0].databaseId
            $jobData = gh run view $runId --repo $Repo --json jobs | ConvertFrom-Json
            foreach ($jobName in ($Jobs -split "," | ForEach-Object { $_.Trim() } | Where-Object { $_ })) {
                $job = $jobData.jobs | Where-Object { $_.name -eq $jobName } | Select-Object -First 1
                if (-not $job) {
                    Write-Host "WAIT CI job: $jobName (not found)"
                    $pending++
                } elseif ($job.conclusion -eq "success") {
                    Write-Host "OK   CI job: $jobName"
                } else {
                    Write-Host "FAIL CI job ${jobName} ($($job.conclusion))"
                    $failed++
                }
            }
        }
    }

    if ($failed -gt 0) {
        Write-Host "$failed required workflow(s) failed on GitHub"
        exit 1
    }
    if ($pending -eq 0) {
        Write-Host "All required GitHub checks passed"
        exit 0
    }
    if ($WaitSeconds -eq 0 -or (Get-Date) -ge $deadline) {
        Write-Host "INCOMPLETE: $pending workflow(s)/job(s) still pending (use -WaitSeconds 300)"
        exit 1
    }
    Start-Sleep -Seconds 15
}
