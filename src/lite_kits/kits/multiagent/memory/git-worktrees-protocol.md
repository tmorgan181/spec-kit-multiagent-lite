# Git Worktrees Protocol for Multi-Agent Development

**Version**: 1.0.0
**Last Updated**: 2025-10-06

## Purpose

Enable multiple AI agents to work on different aspects of the same feature simultaneously using git worktrees, avoiding merge conflicts and coordination overhead.

## What Are Git Worktrees?

Git worktrees allow multiple working directories from a single repository:
- Each worktree is a separate checkout
- All worktrees share the same .git database
- Changes in one worktree don't affect others until pushed

## When to Use Worktrees

**Use worktrees when**:
- Multiple agents working on same feature simultaneously
- Frontend + backend split work
- Independent file sets with no overlap
- Testing different approaches in parallel

**Don't use worktrees when**:
- Single agent working alone
- Sequential work (use normal git workflow)
- Frequent file overlap (high merge conflict risk)

## Basic Worktree Workflow

### Setup: Create Worktrees

**Agent 1 (Claude Code)** - Backend work:
```bash
# From main repository
git worktree add ../feature-auth-backend 003-user-auth

# This creates:
# - New directory: ../feature-auth-backend
# - Checked out to branch: 003-user-auth
# - Ready for backend work

cd ../feature-auth-backend
# Work on backend files here
```

**Agent 2 (Copilot)** - Frontend work:
```bash
# From main repository
git worktree add ../feature-auth-frontend 003-user-auth

cd ../feature-auth-frontend
# Work on frontend files here
```

### Working: Independent Development

Each agent works in their own worktree:

```bash
# Agent 1: Backend
cd ../feature-auth-backend
# Edit src/auth.py, src/models.py
git add src/auth.py src/models.py
git commit -m "feat: Add authentication backend

via claude-sonnet-4.5 @ claude-code"
git push origin 003-user-auth
```

```bash
# Agent 2: Frontend (in parallel)
cd ../feature-auth-frontend
# Edit src/components/LoginForm.tsx
git add src/components/LoginForm.tsx
git commit -m "feat: Add login form component

via gpt-4 @ github-copilot-cli"
git push origin 003-user-auth
```

### Synchronization: Pull Changes

Each agent periodically pulls others' work:

```bash
# Agent 1: Get frontend changes
cd ../feature-auth-backend
git pull origin 003-user-auth

# Agent 2: Get backend changes
cd ../feature-auth-frontend
git pull origin 003-user-auth
```

### Cleanup: Remove Worktrees

When work is complete:

```bash
# Remove worktree (from main repo)
cd /path/to/main/repo
git worktree remove ../feature-auth-backend
git worktree remove ../feature-auth-frontend

# Or if worktrees already deleted:
git worktree prune
```

## Advanced Patterns

### Pattern 1: Component Isolation

**Scenario**: Split large feature by components

```bash
# Agent 1: Database layer
git worktree add ../feature-db 005-ecommerce
cd ../feature-db
# Work on: src/database/, migrations/

# Agent 2: API layer
git worktree add ../feature-api 005-ecommerce
cd ../feature-api
# Work on: src/api/, src/routes/

# Agent 3: Tests
git worktree add ../feature-tests 005-ecommerce
cd ../feature-tests
# Work on: tests/
```

### Pattern 2: Experimental Branches

**Scenario**: Try different approaches simultaneously

```bash
# Approach A: REST API
git worktree add ../feature-rest 006-api
cd ../feature-rest
# Implement REST endpoints

# Approach B: GraphQL
git worktree add ../feature-graphql 006-api
cd ../feature-graphql
# Implement GraphQL schema

# Later: Merge winning approach back
```

### Pattern 3: Review + Fix

**Scenario**: One agent reviews while another implements

```bash
# Agent 1: Continue implementing
git worktree add ../feature-impl 007-feature
cd ../feature-impl
# Keep coding...

# Agent 2: Review previous work
git worktree add ../feature-review 007-feature
cd ../feature-review
# Read code, test, create review notes in collaboration/
```

## Collaboration Directory Integration

### Session Tracking

Each worktree session should be logged:

```markdown
# collaboration/active/sessions/2025-10-06-claude-backend-worktree.md

## Worktree Session: Backend Development

**Agent**: Claude Code (claude-sonnet-4.5)
**Worktree**: ../feature-auth-backend
**Branch**: 003-user-auth
**Start**: 2025-10-06 14:00
**End**: 2025-10-06 16:30

### Work Completed
- Implemented authentication logic
- Added password hashing
- Created session management

### Commits
- a1b2c3d: feat: Add authentication backend
- d4e5f6g: feat: Add session management

### Synchronized With
- Pulled frontend changes at 15:00 (commit h7i8j9k)
- No merge conflicts

### Status
Ready for integration testing with frontend
```

### Handoff Documents

Create handoffs between worktree agents:

```markdown
# collaboration/active/decisions/worktree-handoff.md

## Worktree Coordination

### Active Worktrees

| Agent | Worktree | Focus Area | Last Push |
|-------|----------|------------|-----------|
| Claude Code | feature-auth-backend | Backend API | 16:30 |
| Copilot CLI | feature-auth-frontend | React components | 16:15 |

### File Territory (Avoid Conflicts)

**Backend worktree** owns:
- src/auth.py
- src/models.py
- src/database/
- tests/test_auth.py

**Frontend worktree** owns:
- src/components/LoginForm.tsx
- src/components/ProtectedRoute.tsx
- src/hooks/useAuth.ts
- tests/components/LoginForm.test.tsx

**Shared** (coordinate before editing):
- README.md
- package.json / requirements.txt
- specs/003-user-auth/

### Merge Strategy
Both agents push to `003-user-auth` branch.
Final merge to main after both complete + integration tests pass.
```

## Best Practices

### DO:
- ✅ Create worktrees in sibling directories (`../feature-*`)
- ✅ Use descriptive worktree directory names
- ✅ Pull frequently to stay synchronized
- ✅ Document worktree sessions in collaboration/
- ✅ Define clear file territories to avoid conflicts
- ✅ Clean up worktrees when done

### DON'T:
- ❌ Create worktrees inside existing worktrees (nested)
- ❌ Edit same files in multiple worktrees simultaneously
- ❌ Forget to push before switching context
- ❌ Leave stale worktrees around (prune regularly)
- ❌ Use worktrees for simple sequential work

## Troubleshooting

### Problem: "Branch already checked out"

**Symptom**: Can't create worktree for a branch already checked out

**Solution**:
```bash
# Option 1: Use same branch in multiple worktrees (advanced)
git worktree add --detach ../feature-copy
cd ../feature-copy
git checkout 003-user-auth

# Option 2: Create from commit instead
git worktree add ../feature-copy abc123
```

### Problem: Merge conflicts between worktrees

**Symptom**: Pull fails with conflicts

**Solution**:
```bash
# In worktree with conflict
git pull origin 003-user-auth
# Resolve conflicts manually
git add .
git commit -m "merge: Resolve conflicts from other worktree

via claude-sonnet-4.5 @ claude-code"
git push origin 003-user-auth
```

### Problem: Can't remove worktree (locked)

**Symptom**: `git worktree remove` fails

**Solution**:
```bash
# Force remove (if directory deleted manually)
git worktree remove --force ../feature-old

# Or prune all stale worktrees
git worktree prune
```

### Problem: Lost track of worktrees

**Symptom**: Don't remember what worktrees exist

**Solution**:
```bash
# List all worktrees
git worktree list

# Example output:
# /path/to/main/repo              abc123 [003-user-auth]
# /path/to/feature-auth-backend   def456 [003-user-auth]
# /path/to/feature-auth-frontend  ghi789 [003-user-auth]
```

## Integration with lite-kits

### Check Worktree Status

```bash
# From main repo
lite-kits status

# Output should show active worktrees (TODO: implement)
# Worktrees:
#   ✓ ../feature-auth-backend (claude-code, last commit 2h ago)
#   ✓ ../feature-auth-frontend (copilot, last commit 30m ago)
```

### Validate Worktree Collaboration

```bash
# Ensure collaboration docs exist for each worktree
lite-kits validate

# Checks:
# - Session logs for each worktree
# - File territory definitions
# - No conflicting edits
```

## Quick Reference

```bash
# Create worktree
git worktree add <path> <branch>

# List worktrees
git worktree list

# Remove worktree
git worktree remove <path>

# Clean up stale worktrees
git worktree prune

# Move worktree (manual)
mv <old-path> <new-path>
git worktree repair <new-path>
```

## Resources

- Git worktree docs: https://git-scm.com/docs/git-worktree
- Parallel development patterns: https://github.blog/2015-07-29-git-2-5-including-multiple-worktrees-and-triangular-workflows/
- Multi-agent coordination: [pr-workflow-guide.md](./pr-workflow-guide.md)
