---
description: Check multi-agent sync status with ASCII visualization
---

# Multi-Agent Sync Status

**Purpose**: Visualize git sync status and multi-agent coordination state.

## Execution Steps

### 1. Check Git Status

```powershell
# Current branch
$CurrentBranch = git branch --show-current

# Check if tracking remote
$RemoteBranch = git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>$null

# Commits ahead/behind
if ($RemoteBranch) {
    $Ahead = (git rev-list --count "$RemoteBranch..HEAD")
    $Behind = (git rev-list --count "HEAD..$RemoteBranch")
} else {
    $Ahead = "N/A"
    $Behind = "N/A"
}

# Uncommitted changes
$Modified = (git status --short | Measure-Object).Count
$Untracked = (git ls-files --others --exclude-standard | Measure-Object).Count
```

### 2. Detect Multi-Agent Activity

```powershell
# Check for recent commits by different agents
git log --since="7 days ago" --format="%b" | Select-String "via.*@" | Sort-Object -Unique

# Count commits by agent
Write-Host "Recent activity (last 7 days):"
git log --since="7 days ago" --format="%b" |
    Select-String "via.*@" |
    ForEach-Object { $_ -replace '.*via (.*)', '$1' } |
    Group-Object |
    Sort-Object Count -Descending |
    ForEach-Object { Write-Host "$($_.Count) $($_.Name)" }
```

### 3. Check Collaboration Structure

```powershell
# Find active collaboration directories
if (Test-Path "specs") {
    # List active sessions
    $SessionCount = (Get-ChildItem -Path specs/*/collaboration/active/sessions -Filter *.md -Recurse -ErrorAction SilentlyContinue).Count

    # List pending handoffs
    $HandoffCount = (Get-ChildItem -Path specs/*/collaboration/active/decisions -Filter handoff-*.md -Recurse -ErrorAction SilentlyContinue).Count

    # List active features
    $Features = (Get-ChildItem -Path specs -Directory | Where-Object { $_.Name -match '^\d+' }).Count
} else {
    $SessionCount = 0
    $HandoffCount = 0
    $Features = 0
}
```

### 4. Generate ASCII Visualization

Create a visual representation of sync status:

```
===========================================================
Multi-Agent Sync Status
===========================================================

Branch: dev/001-starter-kits
Remote: origin/dev/001-starter-kits

     Local                    Remote
       ↓                         ↓
    ┌─────┐                  ┌─────┐
    │ ●●● │  ←──(2 behind)── │ ●●  │
    │ ●●  │  ──(3 ahead)───→ │     │
    └─────┘                  └─────┘

    3 commits to push
    2 commits to pull
    5 uncommitted changes

===========================================================
Agent Activity (last 7 days):
===========================================================

github-copilot         ████████████ 12 commits
claude-code            ████████ 8 commits

===========================================================
Collaboration Status:
===========================================================

Active features:     3
Active sessions:     2
Pending handoffs:    1 ⚠

===========================================================
```

### 5. Check for Conflicts

```powershell
# Check if there are merge conflicts
$ConflictCount = (git ls-files -u | Measure-Object).Count
if ($ConflictCount -eq 0) {
    Write-Host "✓ No merge conflicts" -ForegroundColor Green
} else {
    Write-Host "⚠ Merge conflicts detected" -ForegroundColor Yellow
    git diff --name-only --diff-filter=U
}
```

### 6. Provide Sync Recommendations

Based on the status, suggest actions:

**If commits to pull**:
```
⚠ You are behind the remote branch

Recommended action:
  git pull origin $CurrentBranch

Or if you have local commits:
  git pull --rebase origin $CurrentBranch
```

**If commits to push**:
```
✓ You have commits to push

Recommended action:
  git push origin $CurrentBranch
```

**If handoffs pending**:
```
⚠ Pending handoff detected

Review handoff:
  Get-Content specs/*/collaboration/active/decisions/handoff-*.md

Accept handoff:
  1. Review the handoff document
  2. Create session log for your work
  3. Remove handoff file when complete
```

**If diverged (both ahead and behind)**:
```
⚠ Branches have diverged

You have local commits AND remote has new commits.

Recommended actions:
  1. Review remote changes: git fetch; git log "HEAD..origin/$CurrentBranch"
  2. Pull with rebase: git pull --rebase origin $CurrentBranch
  3. Resolve conflicts if any
  4. Push: git push origin $CurrentBranch
```

### 7. Session Log Status

If multiagent-kit installed, check session logs:

```powershell
# Find today's session log
$Today = Get-Date -Format "yyyy-MM-dd"
$Agent = "github-copilot"  # or "claude-code"

$SessionLog = Get-ChildItem -Path specs/*/collaboration/active/sessions -Filter "${Today}*${Agent}*.md" -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1

if ($SessionLog) {
    Write-Host "✓ Session log exists: $($SessionLog.FullName)" -ForegroundColor Green
} else {
    Write-Host "⚠ No session log for today" -ForegroundColor Yellow
    Write-Host "  Create one: specs/<feature>/collaboration/active/sessions/${Today}-${Agent}.md"
}
```

## Output Examples

### Example 1: Clean Sync

```
===========================================================
Multi-Agent Sync Status
===========================================================

Branch: dev/001-starter-kits
Remote: origin/dev/001-starter-kits

     Local                    Remote
       ↓                         ↓
    ┌─────┐                  ┌─────┐
    │ ●●● │ ===(in sync)===  │ ●●● │
    └─────┘                  └─────┘

    ✓ Up to date with remote
    ✓ No uncommitted changes

===========================================================
Agent Activity (last 7 days):
===========================================================

github-copilot         ████████████ 12 commits

===========================================================
Collaboration Status:
===========================================================

Active features:     1
Active sessions:     1
Pending handoffs:    0

✓ All in sync, ready to work!
===========================================================
```

### Example 2: Needs Sync

```
===========================================================
Multi-Agent Sync Status
===========================================================

Branch: dev/002-blog-feature
Remote: origin/dev/002-blog-feature

     Local                    Remote
       ↓                         ↓
    ┌─────┐                  ┌─────┐
    │ ●   │  ←──(1 behind)── │ ●●  │
    │     │  ──(0 ahead)───→ │ ●   │
    └─────┘                  └─────┘

    ⚠ 1 commit to pull
    2 uncommitted changes

===========================================================
Agent Activity (last 7 days):
===========================================================

claude-code            ████████ 5 commits (most recent)
github-copilot         ████ 3 commits

===========================================================
Collaboration Status:
===========================================================

Active features:     1
Active sessions:     2
Pending handoffs:    1 ⚠

Handoff found:
  specs/002-blog-feature/collaboration/active/decisions/handoff-to-copilot.md

===========================================================
Recommended Actions:
===========================================================

1. Review handoff: Get-Content specs/002-blog-feature/collaboration/active/decisions/handoff-to-copilot.md
2. Pull latest: git pull origin dev/002-blog-feature
3. Review changes: git log -1 origin/dev/002-blog-feature
4. Start work on handoff items

===========================================================
```

## Advanced Features

### Check Worktree Status

If working with worktrees:

```powershell
# List all worktrees
git worktree list

# Check which worktrees are active
$Worktrees = git worktree list --porcelain | Select-String "^worktree" | ForEach-Object { ($_ -split ' ')[1] }
foreach ($worktree in $Worktrees) {
    Write-Host "Worktree: $worktree"
    Push-Location $worktree
    git status --short
    Pop-Location
}
```

### Compare with Other Branches

```powershell
# Compare with main
git log main..HEAD --oneline --format="%h %s (via %b)" | Select-String "via"

# Show what's new in main since you branched
git log HEAD..main --oneline
```

### Check for Stale Branches

```powershell
# List branches not updated in 30 days
git for-each-ref --format='%(refname:short) %(committerdate:relative)' refs/heads/ |
    Select-String '(weeks|months|years) ago'
```

## Important Notes

- **Read-only**: This command never modifies git state
- **Fast**: Only checks status, doesn't fetch from remote
- **Visual**: ASCII art helps quickly understand sync state
- **Multi-agent aware**: Highlights collaboration indicators
- **Actionable**: Provides specific next steps

## Integration with /orient

The `/sync` command complements `/orient`:
- `/orient` - Initial orientation when starting work
- `/sync` - Check status during work session
- `/commit` - Save work with attribution
- `/pr` - Create pull request when done

Use `/sync` frequently during multi-agent sessions to stay coordinated!
