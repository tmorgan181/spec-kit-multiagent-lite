#Requires -Version 5.1

<#
.SYNOPSIS
    Gathers comprehensive git repository context for AI agents.

.DESCRIPTION
    Collects git status, branch information, recent commits, and change statistics
    in a structured format suitable for AI agent orientation and commit workflows.

.PARAMETER IncludeCommits
    Number of recent commits to include (default: 5)

.PARAMETER IncludeDiff
    Include file diff statistics (default: true)

.PARAMETER Format
    Output format: Object, Json, or Text (default: Object)

.EXAMPLE
    Get-GitContext
    Returns git context as PowerShell object

.EXAMPLE
    Get-GitContext -Format Text | Write-Host
    Displays formatted text output

.EXAMPLE
    Get-GitContext -IncludeCommits 10 -Format Json
    Returns last 10 commits as JSON
#>

[CmdletBinding()]
param(
    [Parameter()]
    [int]$IncludeCommits = 5,

    [Parameter()]
    [switch]$IncludeDiff,

    [Parameter()]
    [ValidateSet('Object', 'Json', 'Text')]
    [string]$Format = 'Object'
)

# Check if we're in a git repository
if (-not (git rev-parse --git-dir 2>$null)) {
    Write-Error "Not a git repository"
    return
}

# Gather git context
$context = [PSCustomObject]@{
    Branch = $null
    CommitHash = $null
    Status = @{
        Staged = @()
        Unstaged = @()
        Untracked = @()
        Counts = @{
            Staged = 0
            Unstaged = 0
            Untracked = 0
        }
    }
    RecentCommits = @()
    Remote = @{
        Url = $null
        Ahead = 0
        Behind = 0
        Tracking = $null
    }
    Stats = @{
        TotalFiles = 0
        Insertions = 0
        Deletions = 0
    }
}

# Get current branch
$context.Branch = git branch --show-current

# Get current commit hash
$context.CommitHash = git rev-parse --short HEAD 2>$null

# Get git status
$statusLines = git status --porcelain

foreach ($line in $statusLines) {
    if ($line) {
        $statusCode = $line.Substring(0, 2)
        $filePath = $line.Substring(3)

        # Staged files (first character)
        if ($statusCode[0] -match '[MADRC]') {
            $context.Status.Staged += [PSCustomObject]@{
                Status = $statusCode[0]
                Path = $filePath
            }
            $context.Status.Counts.Staged++
        }

        # Unstaged files (second character)
        if ($statusCode[1] -match '[MD]') {
            $context.Status.Unstaged += [PSCustomObject]@{
                Status = $statusCode[1]
                Path = $filePath
            }
            $context.Status.Counts.Unstaged++
        }

        # Untracked files
        if ($statusCode -eq '??') {
            $context.Status.Untracked += [PSCustomObject]@{
                Path = $filePath
            }
            $context.Status.Counts.Untracked++
        }
    }
}

# Get remote tracking info
$tracking = git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>$null
if ($tracking) {
    $context.Remote.Tracking = $tracking

    # Get ahead/behind counts
    $aheadBehind = git rev-list --left-right --count HEAD...$tracking 2>$null
    if ($aheadBehind) {
        $parts = $aheadBehind -split '\s+'
        $context.Remote.Ahead = [int]$parts[0]
        $context.Remote.Behind = [int]$parts[1]
    }
}

# Get remote URL
$remoteUrl = git remote get-url origin 2>$null
if ($remoteUrl) {
    $context.Remote.Url = $remoteUrl
}

# Get recent commits
if ($IncludeCommits -gt 0) {
    $commitFormat = '%H|%h|%an|%ae|%ad|%s'
    $commitLines = git log -n $IncludeCommits --pretty=format:$commitFormat --date=relative

    foreach ($line in $commitLines) {
        if ($line) {
            $parts = $line -split '\|', 6
            $context.RecentCommits += [PSCustomObject]@{
                Hash = $parts[0]
                ShortHash = $parts[1]
                Author = $parts[2]
                Email = $parts[3]
                Date = $parts[4]
                Subject = $parts[5]
            }
        }
    }
}

# Get diff statistics
if ($IncludeDiff -and $context.Status.Counts.Staged -gt 0) {
    $diffStat = git diff --cached --numstat

    foreach ($line in $diffStat) {
        if ($line) {
            $parts = $line -split '\s+', 3
            $insertions = if ($parts[0] -eq '-') { 0 } else { [int]$parts[0] }
            $deletions = if ($parts[1] -eq '-') { 0 } else { [int]$parts[1] }

            $context.Stats.Insertions += $insertions
            $context.Stats.Deletions += $deletions
            $context.Stats.TotalFiles++
        }
    }
}

# Output based on format
switch ($Format) {
    'Json' {
        $context | ConvertTo-Json -Depth 10
    }
    'Text' {
        # Formatted text output
        Write-Output "==============================================================="
        Write-Output "📊 Git Status (on: $($context.Branch)):"
        Write-Output "==============================================================="
        Write-Output "Staged:    $($context.Status.Counts.Staged) files"
        Write-Output "Unstaged:  $($context.Status.Counts.Unstaged) files"
        Write-Output "Untracked: $($context.Status.Counts.Untracked) files"

        if ($context.Remote.Tracking) {
            Write-Output ""
            Write-Output "Remote: $($context.Remote.Tracking)"
            if ($context.Remote.Ahead -gt 0) {
                Write-Output "  Ahead by $($context.Remote.Ahead) commit(s)"
            }
            if ($context.Remote.Behind -gt 0) {
                Write-Output "  Behind by $($context.Remote.Behind) commit(s)"
            }
        }

        if ($context.Status.Staged.Count -gt 0) {
            Write-Output ""
            Write-Output "Staged files:"
            foreach ($file in $context.Status.Staged) {
                Write-Output "  $($file.Status)  $($file.Path)"
            }
        }

        if ($context.Status.Unstaged.Count -gt 0) {
            Write-Output ""
            Write-Output "Unstaged files:"
            foreach ($file in $context.Status.Unstaged) {
                Write-Output "   $($file.Status) $($file.Path)"
            }
        }

        if ($context.Status.Untracked.Count -gt 0) {
            Write-Output ""
            Write-Output "Untracked files:"
            foreach ($file in $context.Status.Untracked) {
                Write-Output "  ?? $($file.Path)"
            }
        }

        if ($context.RecentCommits.Count -gt 0) {
            Write-Output ""
            Write-Output "Recent commits:"
            foreach ($commit in $context.RecentCommits) {
                Write-Output "  $($commit.ShortHash) $($commit.Subject) ($($commit.Date))"
            }
        }

        Write-Output "==============================================================="
    }
    default {
        # Return PowerShell object
        $context
    }
}
