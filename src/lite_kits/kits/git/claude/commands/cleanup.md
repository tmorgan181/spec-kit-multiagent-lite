---
description: Clean up merged branches
---

# Branch Cleanup

**Purpose**: Safely delete local branches that have been merged, keeping your workspace clean.

## Usage

```bash
/cleanup                    # Clean up local branches only
/cleanup --remote           # Also delete from remote
/cleanup --include-current  # Include current branch if PR merged
```

## Prerequisites

- Git repository
- On a safe branch (not the branch you want to delete, unless using --include-current)

## Execution Steps

### 1. Get Current Branch and Base Branch

```bash
# Get current branch
CURRENT_BRANCH=$(git branch --show-current)

# Determine base branch (develop or main)
for base in develop main master; do
  if git show-ref --verify --quiet refs/heads/$base; then
    BASE_BRANCH=$base
    break
  fi
done

echo "Current branch: $CURRENT_BRANCH"
echo "Base branch: $BASE_BRANCH"
```

### 1a. Check if Current Branch Should Be Included

**If `--include-current` flag is present OR current branch is merged with no uncommitted work**:

```bash
# Check if current branch is merged into base
if git merge-base --is-ancestor HEAD origin/$BASE_BRANCH 2>/dev/null; then
  # Check if there are any commits ahead of base
  COMMITS_AHEAD=$(git rev-list --count origin/$BASE_BRANCH..HEAD)

  if [ $COMMITS_AHEAD -eq 0 ]; then
    # PR was merged, current branch is fully in base
    echo "✓ Current branch PR appears to be merged (no commits ahead of $BASE_BRANCH)"

    # Check for uncommitted changes
    if git diff-index --quiet HEAD --; then
      INCLUDE_CURRENT=true
      echo "⚠️  Current branch can be deleted (will switch to $BASE_BRANCH first)"
    else
      echo "⚠️  Current branch has uncommitted changes - won't auto-delete"
      INCLUDE_CURRENT=false
    fi
  fi
fi
```

**If current branch should be included**:
```
⚠️  Your current branch (dev/004-cleanup-command) appears to be merged!

The PR has been merged into develop with no additional commits.

Include current branch in cleanup?
  - Will switch to develop first
  - Then delete dev/004-cleanup-command

Include? (y/n): _____
```

**Safety check**:
```
⚠️  Currently on: dev/004-cleanup-command

Cleanup will check branches merged into: develop

Continue? (y/n): _____
```

### 2. Find Merged Branches

```bash
# Get all merged branches (excluding current, base, and protected branches)
git branch --merged $BASE_BRANCH | \
  grep -v "^\*" | \
  grep -v "$BASE_BRANCH" | \
  grep -v "main" | \
  grep -v "master" | \
  grep -v "develop"
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
```bash
# For each merged branch, get last commit info
for branch in $MERGED_BRANCHES; do
  LAST_COMMIT=$(git log -1 --format="%ar by %an" $branch)
  LAST_HASH=$(git log -1 --format="%h" $branch)
  echo "$branch | $LAST_HASH | $LAST_COMMIT"
done
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

**If current branch should be deleted, switch first**:
```bash
if [ "$INCLUDE_CURRENT" = true ]; then
  echo "Switching to $BASE_BRANCH..."
  git checkout $BASE_BRANCH
  git pull origin $BASE_BRANCH

  # Add current branch to cleanup list
  MERGED_BRANCHES="$MERGED_BRANCHES
$CURRENT_BRANCH"
fi
```

**If user selects specific branches (e.g., "1 3")**:
```bash
# Parse selection
SELECTED="1 3"

# Delete selected branches
for num in $SELECTED; do
  # Get branch name from list
  BRANCH=$(echo "$MERGED_BRANCHES" | sed -n "${num}p")

  # Delete local branch
  git branch -d $BRANCH

  if [ $? -eq 0 ]; then
    echo "✓ Deleted local: $BRANCH"

    # If --remote flag, also delete from remote
    if [ "$DELETE_REMOTE" = true ]; then
      if git ls-remote --heads origin $BRANCH | grep -q $BRANCH; then
        git push origin --delete $BRANCH
        if [ $? -eq 0 ]; then
          echo "✓ Deleted remote: $BRANCH"
        else
          echo "✗ Failed to delete remote: $BRANCH"
        fi
      fi
    fi
  else
    echo "✗ Failed to delete: $BRANCH"
  fi
done
```

**If user confirms all (y)**:
```bash
# Delete all merged branches
for branch in $MERGED_BRANCHES; do
  # Delete local branch
  git branch -d $branch

  if [ $? -eq 0 ]; then
    echo "✓ Deleted local: $branch"

    # If --remote flag, also delete from remote
    if [ "$DELETE_REMOTE" = true ]; then
      if git ls-remote --heads origin $branch | grep -q $branch; then
        git push origin --delete $branch
        if [ $? -eq 0 ]; then
          echo "✓ Deleted remote: $branch"
        else
          echo "✗ Failed to delete remote: $branch"
        fi
      fi
    fi
  else
    echo "✗ Failed to delete: $branch"
  fi
done
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
- Never deletes current branch (unless `--include-current` and PR is merged)
- Never deletes base branches (main, develop, master)
- Only deletes branches that are fully merged
- Uses `git branch -d` (safe delete, will fail if unmerged changes)
- Always asks for confirmation before deletion
- Remote deletion is opt-in with `--remote` flag

**Protected Branches** (never deleted automatically):
- Current branch (unless `--include-current` and PR merged with no new commits)
- `main`, `master`, `develop` (common base branches)
- Any branch that hasn't been merged

**Flags**:
- `--remote`: Also delete branches from remote repository
- `--include-current`: Allow deletion of current branch if PR is merged

**Error Handling**:
```bash
# If branch has unmerged changes
if git branch -d $branch 2>&1 | grep -q "not fully merged"; then
  echo "⚠️  Branch '$branch' has unmerged changes"
  echo "   Use 'git branch -D $branch' to force delete (destructive!)"
  echo "   Skipping..."
fi
```

## Example Workflow

```bash
# User: /cleanup

# Agent checks current state
$ git branch --show-current
dev/004-cleanup-command

# Agent finds merged branches
$ git branch --merged develop
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
$ git branch -d dev/001-starter-kits
Deleted branch dev/001-starter-kits (was 5b1ad35)

$ git branch -d dev/002-installer-polish
Deleted branch dev/002-installer-polish (was 9cd3690)

✓ Cleanup complete: 2 branches deleted
```

## Multi-Agent Considerations

When working with multiple agents:

1. **Check collaboration status** (if multiagent-kit installed):
   ```bash
   # Don't delete branches with active collaboration
   if [ -d "specs/*/collaboration/active" ]; then
     # Check for active sessions on branches
     echo "⚠️  Multi-agent project detected"
     echo "   Checking for active collaboration..."
   fi
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
