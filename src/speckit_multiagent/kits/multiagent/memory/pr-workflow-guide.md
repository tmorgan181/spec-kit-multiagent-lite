# AI Agent Pull Request Workflow Guide

**Version**: 1.0.0
**Last Updated**: 2025-10-06

## Purpose

This guide defines the workflow for AI agents (Claude Code, GitHub Copilot, Cursor) when creating pull requests in spec-kit projects with multiagent coordination.

## Core Principles

1. **Commit your own work**: Each agent commits and pushes their own changes
2. **Attribute properly**: Include model and interface information in commits
3. **Coordinate via collaboration/**: Use feature collaboration directories for handoffs
4. **Test before PR**: Run validation locally before creating pull request

## Pull Request Workflow

### Step 1: Complete Your Work

```bash
# Ensure all changes are committed
git status

# Run tests if available
npm test || pytest || cargo test

# Validate against constitution
lite-kits validate
```

### Step 2: Update Collaboration Directory

Create a session summary:
```
specs/NNN-feature/collaboration/active/sessions/YYYY-MM-DD-agent-summary.md

## Session Summary
**Agent**: Claude Code (claude-sonnet-4.5)
**Date**: 2025-10-06
**Duration**: 45 minutes

### Completed
- Implemented user authentication
- Added password hashing with bcrypt
- Created login/logout endpoints

### Files Changed
- src/auth.py (new)
- src/models.py (modified)
- tests/test_auth.py (new)

### Tests
- All tests passing (12/12)
- Coverage: 94%

### Next Steps
- Review needed on password complexity requirements
- Consider adding 2FA in future iteration
```

### Step 3: Create Pull Request

**Preferred**: Use GitHub CLI (best for Copilot):
```bash
gh pr create --title "feat: Add user authentication" --body "$(cat <<'EOF'
## Summary
- Implemented bcrypt password hashing
- Created login/logout API endpoints
- Added comprehensive test coverage (94%)

## Test Plan
- [x] Unit tests passing (12/12)
- [x] Manual testing of login flow
- [x] Password validation tested
- [ ] Security review needed

## Related
- Implements: specs/003-user-auth/spec.md
- Session: specs/003-user-auth/collaboration/active/sessions/2025-10-06-claude-auth.md

🤖 Generated with spec-kit-multiagent
via claude-sonnet-4.5 @ claude-code
EOF
)"
```

**Alternative**: Manual PR creation via web interface

### Step 4: Request Review

Tag appropriate reviewers based on project conventions:
- Human reviewers for architectural decisions
- Other AI agents for code style/coverage checks
- Automated CI for tests and linting

## Commit Attribution Format

**Required format** for AI agent commits:

```
<conventional-commit-message>

<detailed description if needed>

via <model> @ <interface>
```

**Examples**:
```
feat: Add user authentication with bcrypt

Implements password hashing, login/logout endpoints,
and session management.

via claude-sonnet-4.5 @ claude-code
```

```
fix: Resolve race condition in async handlers

via gpt-4 @ github-copilot-cli
```

```
docs: Update API documentation for auth endpoints

via claude-opus-4 @ cursor
```

## Multi-Agent Coordination

### When Multiple Agents Work on Same Feature

**Use git worktrees** for parallel development:
```bash
# Agent 1: Work on authentication
git worktree add ../feature-auth-backend 003-user-auth

# Agent 2: Work on frontend
git worktree add ../feature-auth-frontend 003-user-auth
```

See [git-worktrees-protocol.md](./git-worktrees-protocol.md) for details.

### Handoff Between Agents

Create handoff document in collaboration directory:
```markdown
# specs/003-user-auth/collaboration/active/decisions/handoff-to-copilot.md

## Handoff to GitHub Copilot

**From**: Claude Code
**To**: GitHub Copilot CLI
**Date**: 2025-10-06

### Context
I've implemented the backend authentication. Frontend integration needed.

### What's Done
- Backend API endpoints (POST /login, POST /logout, GET /session)
- Password hashing with bcrypt
- Session management with JWT
- Comprehensive tests (94% coverage)

### What's Needed
- Frontend login form component
- Session state management
- Protected route wrapper
- Logout button integration

### Files to Create
- src/components/LoginForm.tsx
- src/hooks/useAuth.ts
- src/components/ProtectedRoute.tsx

### Reference
- API docs: specs/003-user-auth/contracts/auth-api.yaml
- Session log: collaboration/active/sessions/2025-10-06-claude-backend.md
```

## PR Checklist for AI Agents

Before creating PR, ensure:

- [ ] All tests passing locally
- [ ] Code follows project conventions (see constitution.md)
- [ ] Session summary created in collaboration/active/sessions/
- [ ] Commit messages include agent attribution
- [ ] No secrets or credentials committed
- [ ] Documentation updated if needed
- [ ] Handoff document created if needed

## Special Cases

### Emergency Fixes

For critical bugs, streamlined process:
```bash
# Fix immediately on feature branch
git commit -m "fix: Critical security patch for auth bypass

via claude-sonnet-4.5 @ claude-code"

# Push directly (skip PR if authorized)
git push origin 003-user-auth
```

### Constitution Conflicts

If your work conflicts with constitution:
1. **STOP** - Do not proceed with PR
2. Create issue describing conflict
3. Tag human maintainers for decision
4. Wait for constitution amendment or spec adjustment

## CI/CD Integration

**Automated checks** run on all PRs:
- Test suite execution
- Code coverage thresholds
- Linting and formatting
- Agent attribution detection (extracts model info)
- Constitution compliance checks

**Agent-specific checks**:
- Verify commit attribution format
- Check for collaboration directory updates
- Validate session summaries exist

## Review Process

**For AI-generated PRs**:
1. Automated CI checks (must pass)
2. Human review for:
   - Architectural decisions
   - Security implications
   - UX considerations
3. Optional: Other AI agents for code quality

**Merge criteria**:
- All CI checks passing
- At least one human approval (for non-trivial changes)
- No unresolved conversations
- Collaboration directory updated

## Post-Merge

After PR merged:
```bash
# Archive session
mv specs/NNN-feature/collaboration/active/sessions/YYYY-MM-DD-*.md \
   specs/NNN-feature/collaboration/archive/YYYY-MM/

# Update status
echo "✓ Feature complete and merged" >> \
   specs/NNN-feature/collaboration/results/artifacts/completion-summary.md
```

## Troubleshooting

**PR creation fails**:
- Check branch is pushed to remote
- Verify GitHub CLI authenticated
- Ensure base branch exists

**CI checks fail**:
- Pull latest from base branch
- Run tests locally
- Check for merge conflicts

**Attribution missing**:
- Amend last commit to add attribution
- Force push (if not yet reviewed)

## Resources

- GitHub CLI docs: https://cli.github.com/manual/
- Git worktrees: [git-worktrees-protocol.md](./git-worktrees-protocol.md)
- Constitution: [constitution.md](./constitution.md)
