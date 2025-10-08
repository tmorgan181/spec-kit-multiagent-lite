# Parallel Work Protocol

**Purpose**: Guide for coordinating multiple AI agents working simultaneously on the same feature.

---

## When to Use Parallel Work

**Good candidates**:
- Backend + Frontend split
- Different modules/components
- Tests + Implementation
- Documentation + Code

**Avoid parallel work for**:
- Single small files
- Tightly coupled code
- Experimental/exploratory work
- Initial architecture decisions

---

## Setup: Define Territories

Before starting parallel work, create a territory document:

**File**: `specs/<feature>/collaboration/active/decisions/worktree-coordination.md`

```markdown
# Worktree Territory Coordination

**Feature**: <feature-name>
**Date**: YYYY-MM-DD
**Agents**: claude-code, github-copilot-cli

## Territory Assignments

### Agent 1: Claude Code
**Focus**: Backend API implementation

**Owned files/directories**:
- `src/api/`
- `src/models/`
- `src/middleware/`
- `tests/api/`

**Responsible for**:
- API endpoints
- Database models
- Authentication middleware
- API tests

### Agent 2: GitHub Copilot CLI
**Focus**: Frontend UI implementation

**Owned files/directories**:
- `src/components/`
- `src/hooks/`
- `src/pages/`
- `tests/components/`

**Responsible for**:
- React components
- Custom hooks
- Page layouts
- Component tests

## Shared Files (Coordinate before editing)

**High conflict risk**:
- `README.md` - Coordinate updates
- `package.json` - Discuss before adding dependencies
- `tsconfig.json` - Agree on config changes
- `src/types/` - Shared type definitions

**Protocol**: Post in decisions/ before modifying shared files

## Integration Points

**Where territories meet**:
- API contracts: Both agents should agree on endpoints
- Type definitions: Shared types go in `src/types/shared.ts`
- Error handling: Use consistent error format

**Sync schedule**:
- Pull from remote: Every 2 hours minimum
- Push commits: After each logical unit of work
- Integration check: End of each work session
```

---

## Worktree Workflow

### 1. Create Worktrees

Each agent creates their own worktree:

**Agent 1** (Claude Code):
```bash
# From main repo
git worktree add ../feature-backend <feature-branch>

cd ../feature-backend
# Work here on backend
```

**Agent 2** (GitHub Copilot):
```bash
# From main repo
git worktree add ../feature-frontend <feature-branch>

cd ../feature-frontend
# Work here on frontend
```

Both worktrees point to the **same branch** but in different directories.

### 2. Initial Sync

Before starting work:

```bash
# Pull latest
git pull origin <feature-branch>

# Verify you're on the right branch
git branch --show-current

# Check status
git status
```

### 3. Work in Your Territory

Stay in your assigned files/directories:

```bash
# Your session log
touch specs/<feature>/collaboration/active/sessions/$(date +%Y-%m-%d)-<agent-name>.md

# Work on your files
code src/api/auth.ts  # or whatever you're working on

# Commit frequently
git add src/api/
git commit -m "feat(api): Add authentication endpoint

via claude-sonnet-4.5 @ claude-code"

# Push regularly
git push origin <feature-branch>
```

### 4. Periodic Sync

**Every 2 hours** or **before making major changes**:

```bash
# Save your work
git add .
git commit -m "WIP: Checkpoint before sync

via <model> @ <agent>"

# Pull changes from other agent
git pull origin <feature-branch>

# Resolve conflicts if any (should be rare with good territories)
# ... fix conflicts ...
git add .
git commit -m "merge: Sync with remote

via <model> @ <agent>"

# Continue working
```

### 5. Resolve Conflicts

If conflicts occur:

**1. Identify the conflict**:
```bash
git status
# Shows conflicted files
```

**2. Check who modified what**:
```bash
git log --oneline -5 -- path/to/conflicted/file.ts
# See recent changes
```

**3. Communicate**:
Create a decision document:
```bash
cat > specs/<feature>/collaboration/active/decisions/conflict-resolution-<file>.md << EOF
# Conflict: <file-name>

**Date**: $(date +%Y-%m-%d)
**File**: path/to/file.ts
**Agents involved**: claude-code, github-copilot-cli

## Conflict Description
[What conflicted and why]

## Resolution
[How we're resolving it]

## Action Items
- [ ] Agent 1: [what they need to do]
- [ ] Agent 2: [what they need to do]
EOF
```

**4. Resolve**:
```bash
# Edit the file to resolve conflict
code path/to/file.ts

# Mark as resolved
git add path/to/file.ts

# Commit resolution
git commit -m "fix: Resolve merge conflict in <file>

Conflict between <agent1> and <agent2> changes.
Resolution: [brief description]

via <model> @ <agent>"
```

---

## Communication Patterns

### Async Updates

**Post session summaries**:
After each work session, update your session log:

```bash
# Update your session log
echo "
## Latest Update ($(date +%H:%M))

Completed:
- [x] Task 1
- [x] Task 2

In progress:
- [ ] Task 3

Pushed commits:
- abc1234 - Add auth endpoint
- def5678 - Add validation

Next: Working on Task 3
" >> specs/<feature>/collaboration/active/sessions/$(date +%Y-%m-%d)-<agent>.md
```

**Check for updates**:
Before starting work:

```bash
# See what other agent did
git log --since="1 day ago" --format="%h %s %b" | grep "via"

# Read their session log
cat specs/<feature>/collaboration/active/sessions/$(date +%Y-%m-%d)-<other-agent>.md
```

### Sync Decisions

**Before modifying shared files**:

```bash
cat > specs/<feature>/collaboration/active/decisions/shared-file-mod-<name>.md << EOF
# Proposed: Modify <shared-file>

**By**: <agent-name>
**Date**: $(date +%Y-%m-%d)

## What
[What you want to change]

## Why
[Reason for the change]

## Impact on other agent
[How this affects their work]

## Request
Please review and acknowledge before I proceed.

**Status**: pending-review
EOF

# Then wait or proceed with caution
```

---

## Integration Testing

### End-of-Session Integration Check

Before ending your work session:

**1. Pull latest**:
```bash
git pull origin <feature-branch>
```

**2. Run full test suite**:
```bash
# Both agents' tests
npm test

# Or your project's test command
```

**3. Quick manual test**:
```bash
# Start the app
npm start

# Test the integration between backend and frontend
# Verify your changes work with other agent's changes
```

**4. Report integration status**:
```bash
cat > specs/<feature>/collaboration/results/validation/integration-$(date +%Y-%m-%d-%H%M).md << EOF
# Integration Test Results

**Date**: $(date +%Y-%m-%d %H:%M)
**Tester**: <agent-name>

## Test Scenarios

- [x] Scenario 1: [description] - ✓ PASS
- [x] Scenario 2: [description] - ✓ PASS
- [ ] Scenario 3: [description] - ⚠ ISSUES

## Issues Found

1. [Issue description]
   - Impact: [high/medium/low]
   - Assigned to: [agent-name]

## Status

Overall: [PASS / FAIL / NEEDS_WORK]
EOF
```

---

## Cleanup

### When Feature is Complete

**1. Merge worktrees**:
Both agents have been pushing to the same branch, so it's already merged.

**2. Remove worktrees**:
```bash
# From main repo
git worktree remove ../feature-backend
git worktree remove ../feature-frontend

# Or from the worktree
cd ../feature-backend
git worktree remove .
```

**3. Archive collaboration docs**:
```bash
# Move session logs
mv specs/<feature>/collaboration/active/sessions/*.md \
   specs/<feature>/collaboration/archive/sessions/

# Move decisions
mv specs/<feature>/collaboration/active/decisions/*.md \
   specs/<feature>/collaboration/archive/decisions/
```

**4. Create final summary**:
```bash
cat > specs/<feature>/collaboration/results/final-summary.md << EOF
# Final Summary: <feature-name>

**Completed**: $(date +%Y-%m-%d)
**Agents**: claude-code, github-copilot-cli

## Collaboration Stats

Commits by claude-code: $(git log --format="%b" | grep "claude-code" | wc -l)
Commits by github-copilot-cli: $(git log --format="%b" | grep "copilot" | wc -l)

Total collaboration sessions: $(ls specs/<feature>/collaboration/archive/sessions/*.md | wc -l)

## What Went Well

- [Success 1]
- [Success 2]

## What Could Improve

- [Learning 1]
- [Learning 2]

## Final Status

Feature complete and ready for PR.
EOF
```

---

## Best Practices

### ✓ Do

- **Define territories clearly** before starting
- **Commit and push frequently** (every logical unit)
- **Pull before making major changes**
- **Update session logs** after each work period
- **Test integration** regularly
- **Communicate in decision docs** for shared files
- **Use consistent commit attribution**

### ✗ Don't

- **Don't edit other agent's territory** without coordination
- **Don't go silent** - update your session log
- **Don't batch commits** - push small, frequent updates
- **Don't skip conflict resolution** - address immediately
- **Don't modify shared files** without posting a decision
- **Don't forget to sync** - pull at least every 2 hours

---

## Troubleshooting

### "Git won't let me push"

```bash
# Someone pushed before you
git pull --rebase origin <feature-branch>

# Fix any conflicts
# Then push
git push origin <feature-branch>
```

### "I accidentally edited their territory"

```bash
# Create a decision doc explaining
cat > specs/<feature>/collaboration/active/decisions/territory-overlap.md << EOF
# Accidental Territory Overlap

I accidentally modified <file> which is in <other-agent>'s territory.

Changes made:
- [list changes]

Suggest:
- [ ] Other agent review and accept
- [ ] I revert and let them handle it
EOF

# Then coordinate with other agent
```

### "Tests are failing after merge"

```bash
# Run tests to see what broke
npm test

# Check what changed
git log -1 --stat

# Create issue in decisions/
cat > specs/<feature>/collaboration/active/decisions/test-failure-<date>.md << EOF
# Test Failures After Merge

**Date**: $(date +%Y-%m-%d)

Failing tests:
- test/foo.test.ts: "should handle auth"

Likely cause:
[Your analysis]

Action:
- [ ] Agent who changed related code to fix
EOF
```

---

## Quick Reference

```bash
# Setup
git worktree add ../my-worktree <feature-branch>

# Daily workflow
git pull origin <feature-branch>  # Start of session
# ... work ...
git add . && git commit -m "..."  # Frequently
git push origin <feature-branch>  # After each commit

# Sync
git pull origin <feature-branch>  # Every 2 hours

# Check other agent's work
git log --since="1 day ago" --format="%h %s %b" | grep "via"

# End session
git push origin <feature-branch>
# Update session log
# Run integration tests

# Cleanup
git worktree remove ../my-worktree
```

---

**Remember**: Good territories + frequent syncs + clear communication = smooth parallel work!
