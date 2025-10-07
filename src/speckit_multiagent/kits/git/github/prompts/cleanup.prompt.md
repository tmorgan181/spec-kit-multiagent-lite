---
description: Clean up merged branches
---

# Branch Cleanup

**Purpose**: Safely delete local branches that have been merged, keeping your workspace clean.

## Prerequisites

- Git repository
- On a safe branch (not the branch you want to delete)

## Execution Steps

### 1. Get Current Branch and Base Branch

```powershell
# Get current branch
$CurrentBranch = git branch --show-current

# Determine base branch (develop or main)
$BaseBranch = $null
foreach ($base in @('develop', 'main', 'master')) {
    if (git show-ref --verify --quiet "refs/heads/$base") {
        $BaseBranch = $base
        break
    }
}

Write-Host "Current branch: $CurrentBranch"
Write-Host "Base branch: $BaseBranch"
```

**Safety check**:
```
⚠️  Currently on: dev/004-cleanup-command

Cleanup will check branches merged into: develop

Continue? (y/n): _____
```

### 2. Find Merged Branches

```powershell
# Get all merged branches (excluding current, base, and protected branches)
$MergedBranches = git branch --merged $BaseBranch |
    Where-Object { $_ -notmatch '^\*' } |
    Where-Object { $_ -notmatch $BaseBranch } |
    Where-Object { $_ -notmatch 'main' } |
    Where-Object { $_ -notmatch 'master' } |
    Where-Object { $_ -notmatch 'develop' } |
    ForEach-Object { $_.Trim() }
```

**If no merged branches found**:
```
✓ No merged branches to clean up.

All branches are either:
  - Currently active
  - Protected (main/develop/master)
  - Unmerged

Workspace is clean!
```

**If merged branches found**, analyze each:
```powershell
# For each merged branch, get last commit info
$BranchInfo = @()
foreach ($branch in $MergedBranches) {
    $LastCommit = git log -1 --format="%ar by %an" $branch
    $LastHash = git log -1 --format="%h" $branch
    $BranchInfo += [PSCustomObject]@{
        Name = $branch
        Hash = $LastHash
        LastCommit = $LastCommit
    }
}
```

### 3. Present Branches for Cleanup

Show branches in a code block with clear formatting:

```
**🧹 Merged Branches Available for Cleanup:**

**Base branch:** develop

**Merged branches:**

1. dev/001-starter-kits
   Last commit: 5b1ad35 (2 days ago by tmorgan181)

2. dev/002-installer-polish
   Last commit: 9cd3690 (1 day ago by tmorgan181)

3. feature/old-experiment
   Last commit: abc1234 (2 weeks ago by tmorgan181)

**Protected branches** (will NOT be deleted):
  - develop
  - main
  - dev/004-cleanup-command (current)

===========================================================
```

**Ask for confirmation**:
- **y** - Delete all listed branches
- **n** - Cancel cleanup
- **e** - Select specific branches (reply with numbers: e.g., "1 3")

### 4. Execute Cleanup

**If user selects specific branches (e.g., "1 3")**:
```powershell
# Parse selection
$Selected = "1 3" -split '\s+'

# Delete selected branches
foreach ($num in $Selected) {
    $index = [int]$num - 1
    $branch = $MergedBranches[$index]

    try {
        git branch -d $branch 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Deleted: $branch" -ForegroundColor Green
        } else {
            Write-Host "✗ Failed to delete: $branch" -ForegroundColor Red
        }
    } catch {
        Write-Host "✗ Error deleting: $branch" -ForegroundColor Red
    }
}
```

**If user confirms all (y)**:
```powershell
# Delete all merged branches
foreach ($branch in $MergedBranches) {
    try {
        git branch -d $branch 2>&1 | Out-Null
        if ($LASTEXITCODE -eq 0) {
            Write-Host "✓ Deleted: $branch" -ForegroundColor Green
        } else {
            Write-Host "✗ Failed to delete: $branch" -ForegroundColor Red
        }
    } catch {
        Write-Host "✗ Error deleting: $branch" -ForegroundColor Red
    }
}
```

### 5. Show Summary

After cleanup, show what was done:

```
===========================================================
✓ Cleanup Complete
===========================================================

**Deleted branches:**
  ✓ dev/001-starter-kits
  ✓ dev/002-installer-polish

**Kept branches:**
  - develop (protected)
  - main (protected)
  - dev/004-cleanup-command (current)
  - feature/in-progress (unmerged)

**Workspace status:**
  - 2 branches deleted
  - 4 branches remaining

===========================================================
```

## Important Notes

**Safety Features**:
- Never deletes current branch
- Never deletes base branches (main, develop, master)
- Only deletes branches that are fully merged
- Uses `git branch -d` (safe delete, will fail if unmerged changes)
- Always asks for confirmation before deletion

**Protected Branches** (never deleted):
- Current branch (wherever you are)
- `main`, `master`, `develop` (common base branches)
- Any branch that hasn't been merged

**Error Handling**:
```powershell
# If branch has unmerged changes
try {
    $result = git branch -d $branch 2>&1
    if ($result -match "not fully merged") {
        Write-Host "⚠️  Branch '$branch' has unmerged changes" -ForegroundColor Yellow
        Write-Host "   Use 'git branch -D $branch' to force delete (destructive!)"
        Write-Host "   Skipping..."
    }
} catch {
    Write-Host "⚠️  Error checking branch: $branch" -ForegroundColor Yellow
}
```

## Example Workflow

```powershell
# User: /cleanup

# Agent checks current state
> git branch --show-current
dev/004-cleanup-command

# Agent finds merged branches
> git branch --merged develop
  dev/001-starter-kits
  dev/002-installer-polish
  dev/003-git-kit-enhancements

# Agent presents options
Merged branches available for cleanup:
1. dev/001-starter-kits (2 days ago)
2. dev/002-installer-polish (1 day ago)
3. dev/003-git-kit-enhancements (2 hours ago)

Delete which branches? (y/n/e): e

# User selects
Selection: 1 2

# Agent deletes
> git branch -d dev/001-starter-kits
Deleted branch dev/001-starter-kits (was 5b1ad35)

> git branch -d dev/002-installer-polish
Deleted branch dev/002-installer-polish (was 9cd3690)

✓ Cleanup complete: 2 branches deleted
```

## Advanced Options

**Check remote tracking**:
```powershell
# Show if branch still exists on remote
foreach ($branch in $MergedBranches) {
    $remote = git config "branch.$branch.remote" 2>$null
    if ($remote) {
        Write-Host "⚠️  Branch '$branch' still has remote: $remote" -ForegroundColor Yellow
        Write-Host "   Consider: git push origin --delete $branch"
    }
}
```

**Suggest remote cleanup** (informational only, don't execute):
```
📝 Note: Some deleted branches may still exist on remote.

To remove from remote:
  git push origin --delete <branch-name>

Or delete via GitHub/GitLab UI after PR merge.
```

## Multi-Agent Considerations

When working with multiple agents:

1. **Check collaboration status** (if multiagent-kit installed):
   ```powershell
   # Don't delete branches with active collaboration
   if (Test-Path "specs/*/collaboration/active") {
       # Check for active sessions on branches
       Write-Host "⚠️  Multi-agent project detected" -ForegroundColor Yellow
       Write-Host "   Checking for active collaboration..."
   }
   ```

2. **Warn about shared branches**:
   ```
   ⚠️  Branch 'feature/shared' may be used by other agents.

   Check collaboration status before deleting.
   Safe to delete? (y/n): _____
   ```

3. **Preserve handoff branches**:
   - Branches with recent handoff documents shouldn't be auto-deleted
   - Warn user if collaboration files exist

## When NOT to Use

**Don't use /cleanup for**:
- Deleting unmerged branches (use `git branch -D` manually with caution)
- Deleting remote branches (use `git push origin --delete`)
- Deleting branches with uncommitted work (stash or commit first)
- Cleaning up worktrees (that's a multiagent-kit feature)

**Use /cleanup for**:
- ✅ Removing local branches after PR merge
- ✅ Cleaning up old feature branches
- ✅ Keeping workspace tidy
- ✅ Safe, confirmed deletions only
