# GitHub Copilot Tasks for v0.3 Release

**Branch**: `dev/v0.3-polish`
**Context**: See [wishlist-prioritized.md](wishlist-prioritized.md) and [v0.3-release-plan.md](v0.3-release-plan.md)

---

## Your Tasks

### Task 1: Better Error Messages
**File**: `src/lite_kits/cli.py`

Update the spec-kit not found error message to include:
- How to install Node.js (link to nodejs.org)
- How to install spec-kit via npm
- Why spec-kit is REQUIRED (lite-kits enhances GitHub spec-kit)
- Link to spec-kit docs (https://github.com/github/spec-kit)

Update the "Next steps" message after installation to:
- Mention GitHub Copilot first, then Claude Code
- Clarify it works with any compatible AI assistant
- Explain commands are just markdown files

---

### Task 2: Preview Kit Headers
**File**: `src/lite_kits/core/installer.py`

Add kit name headers to preview output so users can see which kit each file belongs to.

Example:
```
Preview of changes:

=== Dev Kit ===
Files to be created:
  + .claude/commands/orient.md
  + .claude/commands/commit.md
  ...

=== Multiagent Kit ===
Files to be created:
  + .specify/memory/pr-workflow-guide.md
  ...
```

---

### Task 3: Delete Empty Folders
**File**: `src/lite_kits/cli.py` (remove command)

After removing kit files, check if directories are empty and delete them:
- `.claude/commands/`
- `.github/prompts/`
- `.specify/memory/`
- `.specify/scripts/bash/`
- `.specify/scripts/powershell/`
- `.specify/templates/`

Only delete if completely empty (no files left).

---

## Requirements

- Maintain existing code style and patterns
- Don't break existing functionality
- Test your changes if possible
- Commit each task separately with clear messages
- Use conventional commit format: `feat(scope): description` or `fix(scope): description`

---

## File Ownership

You own these files (no conflicts with Claude):
- `src/lite_kits/cli.py`
- `src/lite_kits/core/installer.py`

Claude is working on:
- Command files in `src/lite_kits/kits/*/commands/`

---

## When Done

Commit your changes and signal completion. Claude will review and integrate.
