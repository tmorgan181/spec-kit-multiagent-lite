# lite-kits User Guide

Complete reference for lite-kits commands, workflows, and best practices.

---

## Table of Contents

1. [CLI Commands](#cli-commands)
2. [Dev-Kit Commands](#dev-kit-commands)
3. [Multiagent-Kit Commands](#multiagent-kit-commands)
4. [Workflows](#workflows)
5. [Architecture](#architecture)
6. [Tips & Tricks](#tips--tricks)

---

## CLI Commands

### Kit Management

#### `lite-kits add`

Add enhancement kits to a spec-kit project.

**Basic Usage:**
```bash
# Add recommended kits (dev-kit)
lite-kits add

# Add specific kit
lite-kits add --kit dev
lite-kits add --kit multiagent

# Add multiple kits
lite-kits add --kit dev,multiagent
```

**Options:**
- `--recommended` - Add dev-kit (default recommended setup)
- `--kit NAMES` - Comma-separated list of kits to add
- `--agent AGENT` - Override agent detection (claude, copilot)
- `--shell SHELL` - Override shell detection (bash, powershell)
- `--force` - Skip preview and confirmations, overwrite existing files
- `TARGET` - Target directory (defaults to current directory)

**Examples:**
```bash
# Preview changes before installing
lite-kits add
# (Shows preview, asks for confirmation)

# Force install without confirmation
lite-kits add --force

# Install to specific directory
lite-kits add /path/to/project

# Override agent detection
lite-kits add --agent copilot
```

**What Gets Added:**
- Dev-kit: `.claude/commands/*.md` and `.github/prompts/*.prompt.md` files
- Multiagent-kit: Adds collaboration directories and memory guides

---

#### `lite-kits remove`

Remove enhancement kits from a spec-kit project.

**Basic Usage:**
```bash
# Remove specific kit
lite-kits remove --kit dev

# Remove all kits
lite-kits remove --all

# Remove without confirmation
lite-kits remove --all --force
```

**Options:**
- `--kit NAMES` - Comma-separated list of kits to remove
- `--all` - Remove all kits
- `--force` - Skip preview and confirmations
- `TARGET` - Target directory (defaults to current directory)

**Examples:**
```bash
# See what would be removed
lite-kits remove --all
# (Shows preview, asks for confirmation)

# Force remove without preview
lite-kits remove --all --force
```

---

#### `lite-kits status`

Show enhancement kit installation status.

**Usage:**
```bash
# Check current directory
lite-kits status

# Check specific directory
lite-kits status /path/to/project
```

**Output:**
- Whether directory is a spec-kit project
- Which kits are installed (dev, multiagent)
- Installation summary

---

#### `lite-kits validate`

Validate enhancement kit installation integrity.

**Usage:**
```bash
lite-kits validate
```

**Checks:**
- All required kit files are present
- Files are not corrupted or empty
- Kit structure is correct
- Collaboration directories (for multiagent-kit)

---

#### `lite-kits help`

Show help and available commands.

**Usage:**
```bash
# General help
lite-kits help

# Help for specific command
lite-kits help add
lite-kits help remove
```

---

#### `lite-kits info`

Show package information and available kits.

**Usage:**
```bash
lite-kits info
```

**Output:**
- Package version and repository
- Available kits (dev, multiagent)
- Kit descriptions and commands
- Package management commands

---

#### Global Options

Available on all commands:

```bash
lite-kits --version / -V        # Show version
lite-kits --banner              # Show animated banner
lite-kits --quiet / -q          # Suppress output
lite-kits --verbose / -v        # Extra output
lite-kits --directory PATH      # Change working directory
```

---

## Dev-Kit Commands

The dev-kit provides essential commands for solo development workflows. All commands work in both Claude Code and GitHub Copilot.

### `/orient`

**Quick project orientation for AI agents.**

Provides concise context about the current project:
- Reads project documentation (README, CONTRIBUTING, etc.)
- Checks current git state (branch, commits, changes)
- Determines agent role and capabilities
- Summarizes recent activity

**When to use:**
- Starting a new session
- Switching between projects
- After pulling latest changes
- When agent seems unfamiliar with project

**Example:**
```bash
/orient
```

**Output:**
- Project name and description
- Current branch and git status
- Recent commits
- Key files and structure
- Next steps or active work

---

### `/commit`

**Smart commits with staging proposals and conventional commits.**

Creates commits with combined staging and message approval:
- Analyzes changes and proposes staging plan
- Drafts conventional commit message
- Shows both in one prompt for approval
- Supports multi-commit suggestions for large changesets
- Adds agent attribution

**When to use:**
- After making changes you want to commit
- When you need well-formatted commit messages
- For conventional commits with proper formatting

**Example:**
```bash
/commit
```

**Workflow:**
1. Shows staging plan (which files to add)
2. Shows draft commit message
3. Options: approve (y), edit staging (es), edit message (em)
4. Creates commit with attribution

**Commit Message Format:**
```
type(scope): Brief description

Detailed explanation of changes and why they were made.

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

---

### `/pr`

**Pull request creation with auto-push and smart descriptions.**

Creates pull requests with automatic branch pushing:
- Checks for existing PR (prevents duplicates)
- Pushes branch to remote automatically
- Generates smart description from commits
- Modular scope (only describes commits in THIS PR)

**When to use:**
- When your feature is ready for review
- After completing a set of commits
- To create a PR without manual push

**Example:**
```bash
/pr
```

**Workflow:**
1. Checks if PR already exists
2. Pushes branch to remote (`git push -u`)
3. Analyzes commits since branch diverged from main
4. Generates PR title and description
5. Creates PR using `gh pr create`

**PR Description Format:**
```markdown
## Summary
- Key change 1
- Key change 2
- Key change 3

## Test plan
- [ ] Manual testing step 1
- [ ] Manual testing step 2

🤖 Generated with [Claude Code](https://claude.com/claude-code)
```

---

### `/review`

**Code review against best practices.**

Reviews staged changes for:
- Code quality and style
- Potential bugs or issues
- Security concerns
- Best practices violations
- Suggestions for improvement

**When to use:**
- Before committing changes
- During code review process
- When you want feedback on your code

**Example:**
```bash
# Stage files first
git add src/

# Review staged changes
/review
```

---

### `/cleanup`

**Safe merged branch cleanup.**

Deletes merged branches with protection for:
- Current branch (won't delete what you're on)
- Base branch (main/master protected)
- Unmerged branches (prevents data loss)

**When to use:**
- After PR is merged
- To clean up stale local branches
- Regular housekeeping

**Example:**
```bash
/cleanup
```

**Options:**
- Default: Delete local branches only
- `--remote`: Also delete from remote

**Safety Features:**
- Shows list of branches to delete
- Asks for confirmation
- Protects current and base branches
- Won't delete unmerged work

---

### `/audit`

**Security analysis on dependencies and code patterns.**

Performs security checks:
- Dependency vulnerabilities
- Code security patterns
- Common security issues
- Recommendations for fixes

**When to use:**
- Before releasing
- After adding dependencies
- Regular security checks
- Pre-deployment audit

**Example:**
```bash
/audit
```

**Output:**
- Dependency vulnerabilities
- Code security issues
- Risk assessment
- Fix recommendations

---

### `/stats`

**Project metrics and complexity analysis.**

Generates project statistics:
- Lines of code by language
- File and directory counts
- Code complexity metrics
- Test coverage (if available)
- Dependency analysis

**When to use:**
- Understanding project size
- Tracking growth over time
- Before refactoring decisions
- Project documentation

**Example:**
```bash
/stats
```

**Output:**
- Language breakdown
- File statistics
- Complexity metrics
- Growth trends

---

## Multiagent-Kit Commands

Optional kit for multi-agent coordination workflows.

### `/sync`

**Multi-agent coordination status.**

Shows visual sync status display:
- Agent activity tracking
- Collaboration structure detection
- Recent work by each agent
- Recommendations for coordination

**When to use:**
- Working with multiple AI agents
- Checking team activity
- Before making conflicting changes
- Coordinating parallel work

**Example:**
```bash
/sync
```

**Output:**
- Active agents and last activity
- Current work in progress
- Collaboration structure status
- Sync recommendations

---

### Collaboration Structure

Multiagent-kit adds collaboration directories:

```
specs/NNN-feature/collaboration/
├── active/              # Current work
│   ├── sessions/        # Work session logs
│   └── decisions/       # Handoffs, proposals
├── archive/             # Historical (YYYY-MM/)
└── results/             # Completed deliverables
```

**Session Logs:**
- Document work sessions
- Track decisions made
- Share context between agents

**Decision Documents:**
- Agent role assignments
- Architecture decisions
- Handoff protocols
- Integration agreements

---

### Memory Guides

Multiagent-kit includes memory guides:

**PR Workflow Guide** (`.specify/memory/pr-workflow-guide.md`):
- How AI agents should create pull requests
- PR description standards
- Attribution requirements
- Review process

**Git Worktrees Protocol** (`.specify/memory/git-worktrees-protocol.md`):
- Parallel development with worktrees
- Branch management
- Conflict avoidance
- Integration workflow

---

## Workflows

### Solo Development Workflow

**Standard spec-driven development with enhanced git commands:**

```bash
# 1. Orient to project
/orient

# 2. Create spec and plan
/specify Build a user authentication system
/plan

# 3. Generate tasks
/tasks

# 4. Implement features
/implement

# 5. Review changes
git add .
/review

# 6. Commit with smart staging
/commit

# 7. Run security audit
/audit

# 8. Create pull request
/pr

# 9. After merge, clean up
/cleanup
```

---

### Multi-Agent Workflow

**Scenario: Claude Code (backend) + GitHub Copilot (frontend) building a blog.**

**1. Claude Code: Create spec and plan**
```bash
/specify Build a blog platform with auth
/plan
```

**2. Claude Code: Create handoff document**
```markdown
# specs/002-blog/collaboration/active/decisions/agent-split.md

Agent Roles:
- Claude Code: Backend (API, database, auth)
- GitHub Copilot: Frontend (React, UI, components)

Integration Points:
- REST API at /api/*
- Auth tokens via JWT
- Shared types in /shared/
```

**3. Both agents: Work in parallel with git worktrees**
```bash
# Claude Code
git worktree add ../blog-backend 002-blog
cd ../blog-backend

# GitHub Copilot
git worktree add ../blog-frontend 002-blog
cd ../blog-frontend
```

**4. Both agents: Implement features**
```bash
# Claude: Backend API
/implement

# Copilot: Frontend UI
/implement
```

**5. Both agents: Commit with attribution**
```bash
/commit
# Message includes: via claude-sonnet-4.5 @ claude-code
# Or: via gpt-4 @ github-copilot
```

**6. Check sync status**
```bash
/sync
# Shows: agent activity, collaboration status, recommendations
```

**7. Integration: Test together**
```bash
# Both agents coordinate integration
# Run tests
# Resolve conflicts
```

**8. Create PR**
```bash
/pr
# Creates PR with both agents' work
```

---

## Architecture

### Manifest-Driven Design

All kit metadata lives in `kits.yaml`:
- Kit definitions (name, description)
- File mappings (commands, memory, templates)
- Agent/shell support
- Installation paths

**Benefits:**
- Zero hardcoded logic
- Easy to add new commands
- Easy to add new agents/shells
- Single source of truth

### Modular Installer

Four focused modules:

**detector.py** - Auto-detection
- Detects AI agents (Claude, Copilot)
- Detects shells (Bash, PowerShell)
- Checks if directory is spec-kit project

**validator.py** - Installation integrity
- Validates kit installation
- Checks file presence and structure
- Verifies collaboration directories

**conflict_checker.py** - Safety
- Checks for file conflicts before installation
- Prevents accidental overwrites
- Shows what would be overwritten

**installer.py** - Main orchestrator
- Coordinates all modules
- Preview-first operations
- Manifest-driven file copying
- No hardcoded kit logic

### Content-First Structure

Files organized by content type, not agent:

```
kits/
└── dev/
    └── commands/
        ├── .claude/
        │   ├── commit.md
        │   ├── orient.md
        │   └── pr.md
        └── .github/
            ├── commit.prompt.md
            ├── orient.prompt.md
            └── pr.prompt.md
```

**Benefits:**
- Easy to compare agent implementations
- Clear file organization
- Simple to add new agents (just add file variant)
- No directory duplication

---

## Tips & Tricks

### Preview Before Installing

Always preview changes before applying:

```bash
# Shows preview and asks for confirmation
lite-kits add

# Skip preview with --force
lite-kits add --force
```

### Override Auto-Detection

Explicitly specify agent or shell:

```bash
# Force Copilot even if Claude is detected
lite-kits add --agent copilot

# Force PowerShell even on Linux
lite-kits add --shell powershell
```

### Check What's Installed

Verify installation:

```bash
# Quick status check
lite-kits status

# Detailed validation
lite-kits validate
```

### Reinstall After Updates

If you update lite-kits:

```bash
# Remove old version
lite-kits remove --all

# Install new version
lite-kits add
```

### Multiple Projects

Install to different directories:

```bash
lite-kits add /path/to/project1
lite-kits add /path/to/project2
```

### Custom Kit Selection

Mix and match kits:

```bash
# Just dev-kit
lite-kits add --kit dev

# Both kits
lite-kits add --kit dev,multiagent
```

### Use Help Command

Get help on any command:

```bash
lite-kits help
lite-kits help add
lite-kits help remove
```

### Agent Attribution

All commits include agent attribution:

```
🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>
```

This helps track which agent made which changes in multi-agent workflows.

### Collaboration Best Practices

For multi-agent work:

1. **Define roles clearly** - Document who does what
2. **Use git worktrees** - Avoid conflicts with parallel work
3. **Sync frequently** - Run `/sync` to check status
4. **Document decisions** - Use collaboration/active/decisions/
5. **Commit often** - Small, attributed commits work best

---

## Troubleshooting

### Installation Issues

**Problem: "Not a spec-kit project"**
```bash
# Initialize spec-kit first
specify init

# Then install lite-kits
lite-kits add
```

**Problem: "No supported AI interface found"**
- Make sure you have Claude Code or GitHub Copilot installed
- Use `--agent` flag to override detection

### Command Issues

**Problem: Commands not showing up**
```bash
# Verify installation
lite-kits status
lite-kits validate

# Reinstall if needed
lite-kits remove --all
lite-kits add
```

**Problem: Wrong agent detected**
```bash
# Force specific agent
lite-kits add --agent copilot
```

### Git Workflow Issues

**Problem: `/pr` fails to push**
- Check git remote is configured: `git remote -v`
- Verify you have push permissions
- Ensure branch is tracked: `git branch -vv`

**Problem: `/cleanup` won't delete branch**
- Branch might not be fully merged
- Check with: `git branch --merged`
- Force delete if needed: `git branch -D branch-name`

---

## Getting Help

- **Documentation**: [README.md](../README.md) | [CHANGELOG.md](../CHANGELOG.md)
- **Issues**: [GitHub Issues](https://github.com/tmorgan181/lite-kits/issues)
- **Discussions**: [GitHub Discussions](https://github.com/tmorgan181/lite-kits/discussions)
- **Contributing**: [CONTRIBUTING.md](../CONTRIBUTING.md)

---

**Last Updated**: v0.2.0 (2025-10-10)
