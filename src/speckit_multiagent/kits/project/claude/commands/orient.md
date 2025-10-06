---
description: Quickly orient to project context, installed kits, and current state
---

# Agent Orientation Protocol

**Purpose**: Provide concise project orientation for AI agents at start of work session.

## Execution Steps

Execute the following steps to gather orientation information:

### 1. Detect Installed Kits

Check for kit marker files to determine what's installed:

```bash
# Initialize kit detection variables
PROJECT_KIT=false
GIT_KIT=false
MULTIAGENT_KIT=false

# Check for project-kit markers
[ -f .claude/commands/review.md ] && PROJECT_KIT=true

# Check for git-kit markers
[ -f .claude/commands/commit.md ] && GIT_KIT=true

# Check for multiagent-kit markers
[ -f .specify/memory/pr-workflow-guide.md ] && MULTIAGENT_KIT=true
```

### 2. Determine Agent Role

Identify which agent you are and your role:

```bash
# You are Claude Code (primary implementation agent)
AGENT_ROLE="Claude Code (Primary)"
```

### 3. Read Primary Documentation

Read these files in order (if they exist):

1. **`.github/copilot-instructions.md`** - Project overview, stack, conventions
2. **`.specify/memory/constitution.md`** - Project philosophy and principles
3. **`README.md`** - General project information

Extract:
- Project name and description
- Technology stack
- Key architectural decisions
- Development conventions

### 4. Check Git State

```bash
# Current branch
git branch --show-current

# Recent commits (last 5)
git log --oneline -5

# Uncommitted changes
git status --short

# Untracked files count
git ls-files --others --exclude-standard | wc -l
```

### 5. Check Active Work

Look for active feature work:

```bash
# List specs directories
ls -1d specs/*/ 2>/dev/null | tail -3

# Check for current spec/plan/tasks
CURRENT_BRANCH=$(git branch --show-current)
if [[ "$CURRENT_BRANCH" =~ ^[0-9]+ ]]; then
  SPEC_DIR="specs/$CURRENT_BRANCH"
  [ -f "$SPEC_DIR/spec.md" ] && echo "✓ Spec exists"
  [ -f "$SPEC_DIR/plan.md" ] && echo "✓ Plan exists"
  [ -f "$SPEC_DIR/tasks.md" ] && echo "✓ Tasks exist"
fi
```

### 6. Check Multi-Agent Coordination (if multiagent-kit installed)

If `MULTIAGENT_KIT=true`:

```bash
# Check for active sessions
find specs/*/collaboration/active/sessions/ -name "*.md" 2>/dev/null | wc -l

# Check for pending handoffs
find specs/*/collaboration/active/decisions/ -name "handoff-*.md" 2>/dev/null | head -1
```

### 7. Generate Concise Output

Provide a **concise summary** (~150 words max) in this format:

```
## Orientation Complete

**Installed Kits**: [list detected kits or "vanilla only"]

**I am**: Claude Code (Primary)
**Project**: [project name from docs]
**Stack**: [main technologies]
**Branch**: [current branch]
**Recent work**: [summary of last 1-2 commits]
**Uncommitted changes**: [count of modified files]
**Active feature**: [current spec if on feature branch]
**Coordination**: [solo work / handoff pending / etc]

**Next suggested action**: [based on state analysis below]
```

### 8. Suggest Next Action

Based on the state you discovered, suggest the next logical action:

**Decision logic**:

- **No spec on current branch** → "Run `/specify` to start a new feature"
- **Spec exists, no plan** → "Run `/plan` to create implementation plan"
- **Plan exists, no tasks** → "Run `/tasks` to break down into tasks"
- **Tasks exist** → "Run `/implement` to start coding"
- **Handoff detected** (multiagent) → "Review handoff in `specs/[feature]/collaboration/active/decisions/`"
- **Uncommitted changes** → "Review changes and consider running `/commit`" (if git-kit installed)

## Important Notes

- Keep output **concise** - this is an orientation, not a full analysis
- Focus on **actionable context** - what the agent needs to know right now
- **Don't modify any files** - this is read-only orientation
- If documentation is missing, note it briefly and continue
- Gracefully handle missing files (don't error if docs don't exist)

## Example Output

```
## Orientation Complete

**Installed Kits**: project, git

**I am**: Claude Code (Primary)
**Project**: Blog Platform API (TypeScript/Node.js)
**Stack**: Node.js, Express, PostgreSQL, TypeScript
**Branch**: dev/003-user-authentication
**Recent work**: Added JWT token validation (2 commits today)
**Uncommitted changes**: 3 modified files
**Active feature**: specs/003-user-authentication/ (spec + plan complete)
**Coordination**: Solo work

**Next suggested action**: Run `/tasks` to break down the implementation plan into actionable tasks.
```
