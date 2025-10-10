---
description: Quickly orient to project context, installed kits, and current state
---

# Agent Orientation Protocol

**Purpose**: Provide concise project orientation for AI agents at start of work session.

## Execution Steps

Execute the following steps to gather orientation information:

### 1. Detect Installed Kits

Check for kit marker files to determine what's installed:

```powershell
# Check all kits in one efficient operation
$KITS_INSTALLED = @()
if (Test-Path .github/prompts/orient.prompt.md) { $KITS_INSTALLED += "project" }
if (Test-Path .github/prompts/commit.prompt.md) { $KITS_INSTALLED += "git" }
if (Test-Path .specify/memory/pr-workflow-guide.md) { $KITS_INSTALLED += "multiagent" }
$KITS_LIST = if ($KITS_INSTALLED.Count -gt 0) { $KITS_INSTALLED -join ", " } else { "vanilla only" }
```

### 2. Determine Agent Role

Identify which agent you are and your role:

```powershell
# Detect model and interface
$MODEL = "Grok Code Fast 1"  # Default Grok model for GitHub Copilot, adjust based on actual model used
$INTERFACE = "GitHub Copilot"
$AGENT_ROLE = "$MODEL @ $INTERFACE (Specialist)"
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

```powershell
# Efficient single-command git status check
# Get branch, recent commits, and changes in one go
$CURRENT_BRANCH = git branch --show-current 2>$null
if (-not $CURRENT_BRANCH) { $CURRENT_BRANCH = "not in git repo" }
$RECENT_COMMITS = (git log --oneline -3 2>$null | Select-Object -First 1)
$CHANGES = (git status --short 2>$null | Measure-Object).Count
```

### 5. Check Active Work

Look for active feature work:

```powershell
# Check if current branch matches a spec directory
if ($CURRENT_BRANCH -match '^\d+' -or $CURRENT_BRANCH -match '^dev/\d+') {
  # Extract spec number from branch name
  $SPEC_NUM = if ($CURRENT_BRANCH -match '\d+') { $Matches[0] } else { $null }
  if ($SPEC_NUM) {
    $SPEC_DIR = Get-ChildItem -Path "specs/$SPEC_NUM-*" -Directory -ErrorAction SilentlyContinue | Select-Object -First 1
    if ($SPEC_DIR) {
      $SPEC_FILES = @("spec.md", "plan.md", "tasks.md") | Where-Object { Test-Path "$($SPEC_DIR.FullName)/$_" }
    }
  }
}
```

### 6. Check Multi-Agent Coordination (if multiagent-kit installed)

```powershell
# Only check if multiagent kit is installed
if ($KITS_INSTALLED -contains "multiagent") {
  # Efficient check for collaboration activity
  $ACTIVE_SESSIONS = (Get-ChildItem -Path specs/*/collaboration/active/sessions/ -Filter *.md -Recurse -ErrorAction SilentlyContinue).Count
  $PENDING_HANDOFF = Get-ChildItem -Path specs/*/collaboration/active/decisions/ -Filter handoff-*.md -Recurse -ErrorAction SilentlyContinue | Select-Object -First 1
}
```

### 7. Generate Concise Output

Provide a **concise summary** (~150 words max) in this format:

```
## Orientation Complete

**Installed Kits**: [$KITS_LIST]

**I am**: [$AGENT_ROLE from step 2]
**Project**: [project name from docs]
**Stack**: [main technologies]
**Branch**: [$CURRENT_BRANCH]
**Recent work**: [$RECENT_COMMITS - just the message]
**Uncommitted changes**: [$CHANGES count]
**Active feature**: [current spec if $SPEC_FILES exists]
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

**I am**: Grok Code Fast 1 @ GitHub Copilot (Specialist)
**Project**: Blog Platform API (TypeScript/Node.js)
**Stack**: Node.js, Express, PostgreSQL, TypeScript
**Branch**: dev/003-user-authentication
**Recent work**: Added JWT token validation (2 commits today)
**Uncommitted changes**: 3 modified files
**Active feature**: specs/003-user-authentication/ (spec + plan complete)
**Coordination**: Solo work

**Next suggested action**: Run `/tasks` to break down the implementation plan into actionable tasks.
```
