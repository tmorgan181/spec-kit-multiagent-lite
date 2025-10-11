# Multiagent Kit

**Status**: 📦 Optional (For Complex Projects)

Multi-agent coordination structure for projects with multiple AI agents working in parallel. Includes collaboration directories, workflow guides, and coordination protocols.

## What It Adds

### Commands

| Command | Claude Code | GitHub Copilot | Description |
|---------|-------------|----------------|-------------|
| `/sync` | ✅ | ✅ | Show git sync status with worktree visualization |

### Memory Guides

| Guide | Description | Status |
|-------|-------------|--------|
| PR Workflow | How AI agents create pull requests | ✅ |
| Git Worktrees Protocol | Parallel development with worktrees | ✅ |

### Templates

| Template | Description | Status |
|----------|-------------|--------|
| Collaboration structure | Active/archive/results directories | 🚧 |

✅ = Implemented | 🚧 = Coming Soon

## Dependencies

**None** - multiagent-kit is standalone.

**Recommended installation**:
```bash
lite-kits install -Kit multiagent
```

**Note**: Works best when combined with dev-kit and dev-kit, but they are not required.

## Installation

### As part of recommended kits:
```bash
lite-kits install -Recommended -Kit multiagent  # project + git + multiagent
```

### Individually:
```bash
lite-kits install -Kit multiagent
```

## What Gets Installed

```
your-project/
├── .claude/commands/              # If Claude Code detected
│   └── sync.md                    # ✅ Sync status with worktrees
├── .github/prompts/               # If GitHub Copilot detected
│   └── sync.prompt.md             # ✅ Sync status with worktrees
├── .specify/memory/
│   ├── pr-workflow-guide.md           # ✅ AI agent PR workflow
│   ├── git-worktrees-protocol.md      # ✅ Parallel development guide
│   └── parallel-work-protocol.md      # ✅ Multi-agent coordination
└── specs/
    └── NNN-feature/
        └── collaboration/             # 🚧 Created per-feature
            ├── active/
            │   ├── sessions/          # Work session logs
            │   ├── decisions/         # Handoffs, proposals
            │   └── README.md          # Current status
            ├── archive/               # Historical (YYYY-MM/)
            └── results/               # Completed deliverables
                ├── validation/        # Test results, reviews
                └── artifacts/         # Final outputs
```

**Note**: Collaboration directories are created automatically when you run `/specify` with multiagent-kit installed.

## Memory Guides

### PR Workflow Guide

**File**: `.specify/memory/pr-workflow-guide.md`

**What it covers**:
- How AI agents should create pull requests
- Commit attribution format (`via model @ interface`)
- PR description templates for AI-generated code
- Multi-agent coordination in PRs
- Handoff procedures between agents
- CI/CD integration for agent attribution

**Example commit attribution**:
```
feat: Add user authentication

Implements bcrypt password hashing and JWT tokens.

via claude-sonnet-4.5 @ claude-code
```

**Use when**: Any AI agent is ready to create a PR

---

### Git Worktrees Protocol

**File**: `.specify/memory/git-worktrees-protocol.md`

**What it covers**:
- Using git worktrees for parallel development
- File territory definitions (avoid conflicts)
- Synchronization strategies
- When to use worktrees vs regular branches
- Troubleshooting common issues

**Example workflow**:
```bash
# Agent 1: Backend worktree
git worktree add ../blog-backend 003-blog

# Agent 2: Frontend worktree
git worktree add ../blog-frontend 003-blog

# Both agents work simultaneously, push to same branch
# No merge conflicts because file territories are defined
```

**Use when**: Multiple agents working on same feature simultaneously

---

## Collaboration Directory Structure

### Purpose

Enable multiple AI agents to coordinate work on the same feature without stepping on each other's toes.

### Structure

```
specs/003-blog-platform/collaboration/
├── active/                           # Current work in progress
│   ├── sessions/                     # Individual work sessions
│   │   ├── 2025-10-06-claude-backend.md
│   │   ├── 2025-10-06-copilot-frontend.md
│   │   └── 2025-10-07-claude-integration.md
│   ├── decisions/                    # Coordination documents
│   │   ├── handoff-to-copilot.md    # Task delegation
│   │   ├── worktree-coordination.md  # File territories
│   │   └── agent-split.md            # Work division
│   └── README.md                     # Current status summary
├── archive/                          # Historical work
│   ├── 2025-10/                      # Organized by month
│   │   ├── sessions/
│   │   └── decisions/
│   └── 2025-11/
└── results/                          # Completed deliverables
    ├── validation/                   # Test results, reviews
    │   ├── test-results.md
    │   └── code-review.md
    └── artifacts/                    # Final outputs
        ├── completion-summary.md
        └── performance-benchmarks.md
```

### Session Log Example

```markdown
# Backend Development Session

**Agent**: Claude Code (claude-sonnet-4.5)
**Worktree**: ../blog-backend
**Date**: 2025-10-06
**Duration**: 3 hours

## Completed
- Express app setup
- Prisma schema design
- Authentication middleware (JWT)
- Integration tests (15/15 passing)

## Commits
- abc123: feat: Add Express app structure
- def456: feat: Add Prisma database schema
- ghi789: feat: Add JWT authentication

## Synchronized
- Pulled frontend changes at 14:00 (no conflicts)
- Pushed backend at 16:30

## Status
✅ Backend ready for frontend integration

## Next Steps
- Frontend team: integrate with auth API
- Add rate limiting (future iteration)
```

### Handoff Document Example

```markdown
# Handoff to GitHub Copilot

**From**: Claude Code
**To**: GitHub Copilot CLI
**Date**: 2025-10-06

## Context
Backend authentication complete. Need frontend integration.

## What's Done
- Backend API endpoints (POST /login, POST /logout, GET /session)
- JWT token generation and validation
- Password hashing with bcrypt
- Integration tests passing

## What's Needed
- React login form component
- Auth context provider
- Protected route wrapper
- Session state management

## Files to Create
- src/components/LoginForm.tsx
- src/hooks/useAuth.ts
- src/components/ProtectedRoute.tsx

## API Reference
- See: specs/003-blog/contracts/auth-api.yaml
- Backend: http://localhost:3000/api/auth

## Testing
- Use credentials: test@example.com / Test123!
- Backend health check: GET /health
```

---

## Multi-Agent Workflows

### Scenario 1: Backend + Frontend Split

**Agents**: Claude Code (backend) + Copilot CLI (frontend)

**Workflow**:
1. Claude runs `/specify` and `/plan` for full feature
2. Claude creates handoff document defining split
3. Both agents create worktrees for parallel work
4. Each agent logs sessions in `collaboration/active/sessions/`
5. Agents sync periodically with `git pull`
6. Claude handles integration testing
7. Either agent creates PR using `/pr` (from dev-kit)

**File territories** (avoid conflicts):
- Backend worktree: `src/api/`, `src/models/`, `tests/api/`
- Frontend worktree: `src/components/`, `src/hooks/`, `tests/components/`
- Shared: Coordinate edits to `README.md`, `package.json`

---

### Scenario 2: Review + Implementation

**Agents**: Claude (implementation) + Copilot (review)

**Workflow**:
1. Claude implements feature, commits work
2. Claude creates handoff for review
3. Copilot runs `/review` (from dev-kit)
4. Copilot logs review in `collaboration/active/decisions/`
5. Claude addresses feedback
6. Copilot approves and creates PR

---

### Scenario 3: Test + Fix Cycle

**Agents**: Claude (testing) + Copilot (fixing)

**Workflow**:
1. Claude writes comprehensive tests (TDD)
2. Tests fail (as expected)
3. Claude creates handoff with failing test details
4. Copilot implements code to pass tests
5. Both agents log sessions
6. Tests pass, feature complete

---

## When to Use Multiagent Kit

### ✅ Use when:
- Multiple AI agents working on same feature
- Complex features requiring parallel work (backend + frontend)
- Team handoffs between agents
- Long-running features (>1 week)
- Need coordination history for debugging

### ❌ Don't use when:
- Solo developer with single AI agent
- Simple features (<1 day)
- Proof of concepts or experiments
- Scripts or small utilities

**Rule of thumb**: If you're using git worktrees, you need multiagent-kit.

---

## Integration with Other Kits

### With dev-kit (optional)
- Use `/orient` for each agent to understand their role

### With dev-kit (optional)
- Use `/commit` for agent-attributed commits
- Use `/pr` to create PRs with multi-agent summary
- Use `/review` for agent-to-agent code review
- Use `/cleanup` to remove stale worktrees
- Combine `/sync` (from multiagent-kit) with dev-kit workflows

---

## Best Practices

### Session Logging
- Create session log at start of work
- Update throughout session
- Include commits, syncs, blockers
- End with status and next steps

### Handoff Documents
- Clear context and background
- Specific what's done vs what's needed
- List files to create/modify
- Include API references or contracts
- Set clear expectations

### File Territories
- Define upfront in handoff document
- Avoid editing shared files simultaneously
- Communicate before editing shared files
- Use git worktrees to enforce separation

### Archive Regularly
- Move completed sessions to `archive/YYYY-MM/`
- Keep `active/` clean (current work only)
- Document final results in `results/`

---

## Configuration

No configuration needed - works out of the box.

**Optional**: Customize collaboration templates in future versions.

---

## Compatibility

- ✅ **Agents**: Claude Code, GitHub Copilot
- ✅ **Platforms**: Linux, macOS, Windows
- ✅ **Shells**: Bash, PowerShell
- ✅ **Vanilla safe**: Only adds new files, never modifies existing

---

## Uninstall

```bash
lite-kits remove -Kit multiagent
```

Removes:
- `.claude/commands/sync.md`
- `.github/prompts/sync.prompt.md`
- `.specify/memory/pr-workflow-guide.md`
- `.specify/memory/git-worktrees-protocol.md`
- `.specify/memory/parallel-work-protocol.md`

**Note**: Existing `specs/*/collaboration/` directories are **preserved** (user data).

---

## Examples

See working examples:
- **blog-with-auth**: Full multi-agent workflow with worktrees
  - Backend (Claude Code) + Frontend (Copilot CLI)
  - Collaboration directories in action
  - Handoff documents
  - Integration testing

---

## Future Enhancements

Considering for multiagent-kit:
- Automated session logging (CLI helper)
- Agent dashboard (show current work across agents)
- Conflict detection (warn about file territory violations)
- Collaboration metrics (contribution tracking)
- Multi-agent CI workflows

Suggest more in [GitHub Discussions](https://github.com/tmorgan181/spec-kit-multiagent-lite/discussions).
