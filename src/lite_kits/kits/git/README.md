# Git Kit

**Status**: ✅ Recommended (Default)

Git workflow automation with smart commits, PR creation, code review, sync visualization, and cleanup operations. Includes ASCII visualization for better readability.

## What It Adds

### Commands

| Command | Claude Code | GitHub Copilot | Description |
|---------|-------------|----------------|-------------|
| `/commit` | 🚧 | 🚧 | Smart commit with agent attribution |
| `/pr` | 🚧 | 🚧 | Create PR with auto-generated description |
| `/review` | 🚧 | 🚧 | Review staged changes against best practices |
| `/sync` | 🚧 | 🚧 | Show sync status with ASCII visualization |
| `/cleanup` | 🚧 | 🚧 | Clean merged branches, stale worktrees |

🚧 = Coming Soon

## Installation

### As part of recommended kits:
```bash
lite-kits install -Recommended  # project + git
```

### Individually:
```bash
lite-kits install -Kit git
```

## What Gets Installed

```
your-project/
├── .claude/commands/          # If Claude Code detected
│   ├── commit.md
│   ├── pr.md
│   ├── review.md
│   ├── sync.md
│   └── cleanup.md
└── .github/prompts/           # If GitHub Copilot detected
    ├── commit.prompt.md
    ├── pr.prompt.md
    ├── review.prompt.md
    ├── sync.prompt.md
    └── cleanup.prompt.md
```

**Note**: Vanilla spec-kit files are **never modified** - only new files are added.

## Commands

### `/commit` - Smart Commit (Coming Soon)

**Purpose**: Generate smart commit messages with agent attribution.

**What it will do**:
1. Run `git status` to see staged files
2. Run `git diff --staged` to see changes
3. Analyze changes and generate conventional commit message
4. Add agent attribution footer
5. Execute commit with generated message

**Example usage** (planned):
```
/commit

## Smart Commit

**Staged files**: 3
- src/auth.py (new)
- src/models.py (modified)
- tests/test_auth.py (new)

**Changes detected**:
- New feature: Authentication system
- Added User model
- Comprehensive test coverage

**Suggested commit message**:

feat: Add user authentication system

Implements bcrypt password hashing, JWT token generation,
and session management. Includes User model and comprehensive
tests with 94% coverage.

via claude-sonnet-4.5 @ claude-code

**Confirm?** (y/n): y

[dev/003-auth a1b2c3d] feat: Add user authentication system
 3 files changed, 247 insertions(+)
 create mode 100644 src/auth.py
 create mode 100644 tests/test_auth.py
```

**Benefits**:
- Consistent commit message format
- Auto-attribution for AI-generated code
- Follows conventional commits
- Saves time thinking about messages

---

### `/review` - Code Review (Coming Soon)

**Purpose**: Review staged changes against best practices and project standards.

**What it will do**:
1. Run `git diff --staged` to see changes
2. Check changes against common best practices
3. Identify potential code smells
4. Suggest improvements
5. Verify consistent formatting
6. Check for common issues (hardcoded secrets, TODO comments, etc.)

**Example usage** (planned):
```
/review

## Code Review

**Staged files**: 3
- src/auth.py (new)
- src/models.py (modified)
- tests/test_auth.py (new)

**Analysis**:

✅ **Good practices**:
- Clear function names and docstrings
- Comprehensive test coverage (94%)
- Type hints used throughout
- No hardcoded credentials

⚠ **Suggestions**:
- src/auth.py:45: Consider extracting hash_password to utils
- src/models.py:12: TODO comment should be tracked in issue
- tests/test_auth.py: Add edge case for empty passwords

**Overall**: Ready to commit with minor suggestions

**Approve?** (y/n): y
```

**Benefits**:
- Catch issues before committing
- Consistent code quality
- Learn best practices
- Agent-to-agent code review support

---

### `/pr` - Create Pull Request (Coming Soon)

**Purpose**: Create PR with auto-generated description from commits.

**What it will do**:
1. Check current branch against base (main/develop)
2. List all commits that will be in PR
3. Analyze changes across all commits
4. Generate PR title and description
5. Create PR using `gh pr create`

**Example usage** (planned):
```
/pr

## Create Pull Request

**Branch**: dev/003-auth → main
**Commits**: 5

**Changes summary**:
- Added authentication system (bcrypt + JWT)
- Created User model with validation
- Added login/logout API endpoints
- Comprehensive test suite (94% coverage)
- Updated API documentation

**Generated PR**:

Title: feat: Add user authentication system

Body:
## Summary
- Implements bcrypt password hashing
- JWT token generation and validation
- Session management
- User model with SQLAlchemy

## Changes
- `src/auth.py` - Authentication logic
- `src/models.py` - User model
- `src/api/auth_routes.py` - Login/logout endpoints
- `tests/test_auth.py` - Test suite (94% coverage)

## Test Plan
- [x] Unit tests passing (24/24)
- [x] Manual testing of login flow
- [x] Password validation tested
- [ ] Security review pending

## Related
- Implements: specs/003-user-auth/spec.md
- Closes: #42

🤖 Generated with spec-kit-multiagent
via claude-sonnet-4.5 @ claude-code

**Create PR?** (y/n): y

✓ Pull request created: https://github.com/user/repo/pull/15
```

---

### `/sync` - Sync Status with Visualization (Coming Soon)

**Purpose**: Show git sync status with ASCII visualization.

**Problem**: `git status` output is text-heavy and hard to parse visually.

**Solution**: ASCII tree diagrams and colorized status.

**Example usage** (planned):
```
/sync

## Git Sync Status

**Branch**: dev/003-auth
**Tracking**: origin/dev/003-auth

**Local vs Remote**:

    origin/main ─────────────┬──────> main (up to date)
                              │
                              ├──────> dev/003-auth (5 commits ahead)
                              │        ↑ PUSH NEEDED
                              │
    Your commits:             │
    ├─ a1b2c3d feat: Add auth│
    ├─ b2c3d4e feat: Add user│
    ├─ c3d4e5f test: Add auth│
    ├─ d4e5f6g docs: Update  │
    └─ e5f6g7h fix: Resolve  │
                              │
**Status**:
✓ No uncommitted changes
⚠ 5 commits not pushed
✓ Up to date with remote (fetched 2m ago)

**Actions**:
1. git push origin dev/003-auth
2. git fetch (refresh remote status)
3. /pr (create pull request)

**Worktrees** (if any):
None active

**Branches** (recent):
- dev/003-auth (current) ← 5 commits ahead
- main (up to date)
- dev/002-blog (merged, can cleanup)
```

**Benefits**:
- Visual understanding at a glance
- Clear action items
- Worktree awareness
- Branch cleanup suggestions

---

### `/cleanup` - Git Cleanup (Coming Soon)

**Purpose**: Clean up merged branches, stale worktrees, and old features.

**What it will do**:
1. Detect merged branches (local and remote)
2. Find stale worktrees
3. Identify old feature directories in `specs/`
4. Suggest safe cleanup actions
5. Execute cleanup with confirmation

**Example usage** (planned):
```
/cleanup

## Git Cleanup

**Merged branches** (safe to delete):
- dev/001-init (merged 2 weeks ago)
- dev/002-blog (merged 1 week ago)
- feature/old-experiment (merged 3 months ago)

**Stale worktrees**:
- ../blog-backend (branch merged, worktree orphaned)

**Old feature specs**:
- specs/001-init/ (merged, archived?)

**Cleanup plan**:
1. Delete 3 merged local branches
2. Delete 2 merged remote branches
3. Remove 1 stale worktree
4. Suggest archiving specs/001-init/

**Disk space freed**: ~45 MB

**Proceed?** (y/n): y

✓ Deleted branch dev/001-init
✓ Deleted branch dev/002-blog
✓ Deleted branch feature/old-experiment
✓ Deleted remote branch origin/dev/001-init
✓ Removed stale worktree ../blog-backend
⚠ Manual action: Archive specs/001-init/ to specs/.archive/

**Cleanup complete!**
```

---

## ASCII Visualization Examples

Git-kit emphasizes visual output because AI agents are good at generating ASCII art and it makes git status much easier to understand.

### Branch Relationships
```
main ──────────┬──────────> origin/main (synced)
               │
               ├─ develop ──> origin/develop (2 ahead, 1 behind)
               │              ↕ PULL & PUSH NEEDED
               │  │
               │  ├─ dev/001-kits (current, 3 ahead)
               │  │  ↑ PUSH NEEDED
               │  │
               │  └─ dev/002-examples (merged)
               │     🗑 CAN DELETE
               │
               └─ hotfix/security (1 ahead)
                  ⚠ URGENT PUSH
```

### Commit Graph
```
Commits ahead of main:

  * e5f6g7h (HEAD) fix: Resolve merge conflict
  │
  * d4e5f6g docs: Update README
  │
  * c3d4e5f test: Add auth tests
  │
  * b2c3d4e feat: Add User model
  │
  * a1b2c3d feat: Add auth system
  │
  o ─────── (origin/main)
```

---

## Use Cases

### Daily Development
**Use**: `/review` before committing, `/commit` for every commit, `/sync` multiple times per day

### Before Creating PR
**Use**: `/review` final check, `/sync` to ensure up to date, `/pr` to create pull request

### Weekly Maintenance
**Use**: `/cleanup` to remove merged branches and free up space

### Multi-Agent Projects
**Combine with**: multiagent-kit for coordination
**Use**: `/review` for agent-to-agent code review, `/sync` shows worktree status for parallel development

---

## Dependencies

**None** - git-kit is standalone.

**Requires**: Git 2.0+, optionally `gh` CLI for `/pr` command

**Recommended with**: multiagent-kit (for worktree visualization)

---

## Compatibility

- ✅ **Agents**: Claude Code, GitHub Copilot
- ✅ **Platforms**: Linux, macOS, Windows
- ✅ **Shells**: Bash, PowerShell (ASCII works in both!)
- ✅ **Vanilla safe**: Only adds new files, never modifies existing

---

## Uninstall

```bash
lite-kits remove -Kit git
```

Removes:
- `.claude/commands/{commit,pr,review,sync,cleanup}.md`
- `.github/prompts/{commit,pr,review,sync,cleanup}.prompt.md`

---

## Future Enhancements

Considering for git-kit:
- `/rebase` - Interactive rebase helper
- `/stash` - Stash management with visualization
- `/blame` - Enhanced git blame with agent attribution
- `/conflicts` - Merge conflict resolver helper
- `/bisect` - Git bisect helper for finding bugs

Suggest more in [GitHub Discussions](https://github.com/tmorgan181/spec-kit-multiagent-lite/discussions).
