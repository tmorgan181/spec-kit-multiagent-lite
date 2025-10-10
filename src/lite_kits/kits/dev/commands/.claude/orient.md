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
# Check all kits in one command
KITS_INSTALLED=""
[ -f .claude/commands/orient.md ] && KITS_INSTALLED="${KITS_INSTALLED}project "
[ -f .claude/commands/commit.md ] && KITS_INSTALLED="${KITS_INSTALLED}git "
[ -f .specify/memory/pr-workflow-guide.md ] && KITS_INSTALLED="${KITS_INSTALLED}multiagent "
KITS_INSTALLED="${KITS_INSTALLED:-vanilla only}"
```

### 2. Determine Agent Role

Identify which agent you are and your role:

```bash
# Detect model and interface
MODEL="claude-sonnet-4.5"  # Default Claude model, adjust based on actual model used
INTERFACE="Claude Code"
AGENT_ROLE="$MODEL @ $INTERFACE (Primary)"
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
# Efficient single-command git status check
# Get branch, recent commits, and changes in one go
CURRENT_BRANCH=$(git branch --show-current 2>/dev/null || echo "(not in git repo)")
RECENT_COMMITS=$(git log --oneline -3 2>/dev/null | head -1 || echo "(no commits)")
CHANGES=$(git status --short 2>/dev/null | wc -l || echo "0")
```

### 5. Check Active Work

Look for active feature work:

```bash
# Check if current branch matches a spec directory
if [[ "$CURRENT_BRANCH" =~ ^[0-9]+ ]] || [[ "$CURRENT_BRANCH" =~ ^dev/[0-9]+ ]]; then
  # Extract spec number from branch name
  SPEC_NUM=$(echo "$CURRENT_BRANCH" | grep -oE '[0-9]+' | head -1)
  SPEC_DIR="specs/$SPEC_NUM-*"
  # Check for spec files efficiently
  SPEC_FILES=$(ls -1 $SPEC_DIR/{spec,plan,tasks}.md 2>/dev/null | wc -l)
fi
```

### 6. Check Multi-Agent Coordination (if multiagent-kit installed)

```bash
# Only check if multiagent kit is installed
if [[ "$KITS_INSTALLED" == *"multiagent"* ]]; then
  # Efficient check for collaboration activity
  ACTIVE_SESSIONS=$(find specs/*/collaboration/active/sessions/ -name "*.md" 2>/dev/null | wc -l)
  PENDING_HANDOFF=$(find specs/*/collaboration/active/decisions/ -name "handoff-*.md" 2>/dev/null | head -1)
fi
```

### 7. Generate Concise Output

Provide a **concise summary** (~150 words max) in this format:

```
## Orientation Complete

**Installed Kits**: [KITS_INSTALLED]

**I am**: [AGENT_ROLE from step 2]
**Project**: [project name from docs]
**Stack**: [main technologies]
**Branch**: [CURRENT_BRANCH]
**Recent work**: [RECENT_COMMITS - just the message]
**Uncommitted changes**: [CHANGES count]
**Active feature**: [current spec if SPEC_FILES > 0]
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

**I am**: claude-sonnet-4.5 @ Claude Code (Primary)
**Project**: Blog Platform API (TypeScript/Node.js)
**Stack**: Node.js, Express, PostgreSQL, TypeScript
**Branch**: dev/003-user-authentication
**Recent work**: Added JWT token validation (2 commits today)
**Uncommitted changes**: 3 modified files
**Active feature**: specs/003-user-authentication/ (spec + plan complete)
**Coordination**: Solo work

**Next suggested action**: Run `/tasks` to break down the implementation plan into actionable tasks.
```
