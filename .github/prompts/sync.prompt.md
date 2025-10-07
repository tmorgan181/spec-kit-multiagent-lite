---
description: Check multi-agent sync status with ASCII visualization
---

# Multi-Agent Sync Status

**Purpose**: Visualize git sync status and multi-agent coordination state.

## Execution Steps

### 1. Check Git Status

```powershell
# Current branch
CURRENT_BRANCH=$(git branch --show-current)

# Check if tracking remote
REMOTE_BRANCH=$(git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null)

# Commits ahead/behind
if [ -n "$REMOTE_BRANCH" ]; then
  AHEAD=$(git rev-list --count $REMOTE_BRANCH..HEAD)
  BEHIND=$(git rev-list --count HEAD..$REMOTE_BRANCH)
else
  AHEAD="N/A"
  BEHIND="N/A"
fi

# Uncommitted changes
MODIFIED=$(git status --short | wc -l)
UNTRACKED=$(git ls-files --others --exclude-standard | wc -l)
```

### 2. Detect Multi-Agent Activity

```powershell
# Check for recent commits by different agents
git log --since="7 days ago" --format="%b" | grep "via.*@" | sort -u

# Count commits by agent
echo "Recent activity (last 7 days):"
git log --since="7 days ago" --format="%b" | \
  grep "via.*@" | \
  sed 's/.*via \(.*\)/\1/' | \
  sort | uniq -c | sort -rn
```

### 3. Check Collaboration Structure

```powershell
# Find active collaboration directories
if [ -d "specs" ]; then
  # List active sessions
  SESSION_COUNT=$(find specs/*/collaboration/active/sessions -name "*.md" 2>/dev/null | wc -l)

  # List pending handoffs
  HANDOFF_COUNT=$(find specs/*/collaboration/active/decisions -name "handoff-*.md" 2>/dev/null | wc -l)

  # List active features
  FEATURES=$(find specs -maxdepth 1 -type d -name "[0-9]*" | wc -l)
else
  SESSION_COUNT=0
  HANDOFF_COUNT=0
  FEATURES=0
fi
```

### 4. Generate ASCII Visualization

Create a visual representation of sync status:

```
═══════════════════════════════════════════════════════════
Multi-Agent Sync Status
═══════════════════════════════════════════════════════════

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

═══════════════════════════════════════════════════════════
Agent Activity (last 7 days):
═══════════════════════════════════════════════════════════

github-copilot-cli         ████████████ 12 commits
github-copilot-cli  ████████ 8 commits

═══════════════════════════════════════════════════════════
Collaboration Status:
═══════════════════════════════════════════════════════════

Active features:     3
Active sessions:     2
Pending handoffs:    1 ⚠

═══════════════════════════════════════════════════════════
```

### 5. Check for Conflicts

```powershell
# Check if there are merge conflicts
if git ls-files -u | wc -l | grep -q "^0$"; then
  echo "✓ No merge conflicts"
else
  echo "⚠ Merge conflicts detected"
  git diff --name-only --diff-filter=U
fi
```

### 6. Provide Sync Recommendations

Based on the status, suggest actions:

**If commits to pull**:
```
⚠ You are behind the remote branch

Recommended action:
  git pull origin $CURRENT_BRANCH

Or if you have local commits:
  git pull --rebase origin $CURRENT_BRANCH
```

**If commits to push**:
```
✓ You have commits to push

Recommended action:
  git push origin $CURRENT_BRANCH
```

**If handoffs pending**:
```
⚠ Pending handoff detected

Review handoff:
  cat specs/*/collaboration/active/decisions/handoff-*.md

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
  1. Review remote changes: git fetch && git log HEAD..origin/$CURRENT_BRANCH
  2. Pull with rebase: git pull --rebase origin $CURRENT_BRANCH
  3. Resolve conflicts if any
  4. Push: git push origin $CURRENT_BRANCH
```

### 7. Session Log Status

If multiagent-kit installed, check session logs:

```powershell
# Find today's session log
TODAY=$(date +%Y-%m-%d)
AGENT="github-copilot-cli"  # or "github-copilot-cli"

SESSION_LOG=$(find specs/*/collaboration/active/sessions -name "${TODAY}*${AGENT}*.md" 2>/dev/null | head -1)

if [ -n "$SESSION_LOG" ]; then
  echo "✓ Session log exists: $SESSION_LOG"
else
  echo "⚠ No session log for today"
  echo "  Create one: specs/<feature>/collaboration/active/sessions/${TODAY}-${AGENT}.md"
fi
```

## Output Examples

### Example 1: Clean Sync

```
═══════════════════════════════════════════════════════════
Multi-Agent Sync Status
═══════════════════════════════════════════════════════════

Branch: dev/001-starter-kits
Remote: origin/dev/001-starter-kits

     Local                    Remote
       ↓                         ↓
    ┌─────┐                  ┌─────┐
    │ ●●● │ ═══(in sync)═══  │ ●●● │
    └─────┘                  └─────┘

    ✓ Up to date with remote
    ✓ No uncommitted changes

═══════════════════════════════════════════════════════════
Agent Activity (last 7 days):
═══════════════════════════════════════════════════════════

github-copilot-cli         ████████████ 12 commits

═══════════════════════════════════════════════════════════
Collaboration Status:
═══════════════════════════════════════════════════════════

Active features:     1
Active sessions:     1
Pending handoffs:    0

✓ All in sync, ready to work!
═══════════════════════════════════════════════════════════
```

### Example 2: Needs Sync

```
═══════════════════════════════════════════════════════════
Multi-Agent Sync Status
═══════════════════════════════════════════════════════════

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

═══════════════════════════════════════════════════════════
Agent Activity (last 7 days):
═══════════════════════════════════════════════════════════

github-copilot-cli  ████████ 5 commits (most recent)
github-copilot-cli         ████ 3 commits

═══════════════════════════════════════════════════════════
Collaboration Status:
═══════════════════════════════════════════════════════════

Active features:     1
Active sessions:     2
Pending handoffs:    1 ⚠

Handoff found:
  specs/002-blog-feature/collaboration/active/decisions/handoff-to-claude.md

═══════════════════════════════════════════════════════════
Recommended Actions:
═══════════════════════════════════════════════════════════

1. Review handoff: cat specs/002-blog-feature/collaboration/active/decisions/handoff-to-claude.md
2. Pull latest: git pull origin dev/002-blog-feature
3. Review changes: git log -1 origin/dev/002-blog-feature
4. Start work on handoff items

═══════════════════════════════════════════════════════════
```

## Advanced Features

### Check Worktree Status

If working with worktrees:

```powershell
# List all worktrees
git worktree list

# Check which worktrees are active
for worktree in $(git worktree list --porcelain | grep "worktree" | cut -d' ' -f2); do
  echo "Worktree: $worktree"
  cd "$worktree"
  git status --short
  cd - > /dev/null
done
```

### Compare with Other Branches

```powershell
# Compare with main
git log main..HEAD --oneline --format="%h %s (via %b)" | grep "via"

# Show what's new in main since you branched
git log HEAD..main --oneline
```

### Check for Stale Branches

```powershell
# List branches not updated in 30 days
git for-each-ref --format='%(refname:short) %(committerdate:relative)' \
  refs/heads/ | grep -E '(weeks|months|years) ago'
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
