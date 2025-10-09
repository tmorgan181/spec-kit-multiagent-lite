---
description: Analyze code quality for uncommitted changes or recent commits
---

# Code Review Helper

**Purpose**: Provide quick code quality analysis and actionable suggestions for AI agents before committing.

## Execution Steps

Execute the following steps to analyze code changes:

### 1. Check for Uncommitted Changes

```powershell
# Get status of modified and staged files
git status --short
```

**Analyze the output**:
- Lines starting with `M ` or `A ` = Staged files
- Lines starting with ` M` = Modified but not staged
- Lines starting with `??` = Untracked files
- Lines starting with `MM` = Staged and modified again

### 2. Analyze Changes

If changes exist:
```powershell
# Show unstaged changes
git diff

# Show staged changes
git diff --cached
```

**Review each file**:
- Check for code quality issues
- Look for potential bugs or edge cases
- Verify naming conventions
- Check for TODO/FIXME comments

If no changes:
```powershell
# Suggest reviewing recent commit
git log -1 --stat
```

### 3. Check for Linting Configuration

```powershell
# Look for common linting config files
Get-ChildItem -Path . -Include .ruff.toml,.pylintrc,pyproject.toml,.eslintrc* -Recurse -ErrorAction SilentlyContinue
```

**If linting configs found**:
- Python: Suggest `ruff check .` or `pylint <files>`
- JavaScript: Suggest `eslint <files>`
- TypeScript: Suggest `tsc --noEmit`

### 4. Generate Concise Output

Provide analysis in this format (~150 words max):

```markdown
## Code Review

**Changes**: N files modified (M staged, K unstaged)

- **file1.py**: Brief assessment of changes
- **file2.ts**: Brief assessment of changes
- **file3.md**: Brief assessment of changes

**Suggestions**:
- Actionable suggestion 1
- Actionable suggestion 2
- Actionable suggestion 3

**Next Action**: [Run linter / Commit changes / Review specific pattern]
```

## Important Notes

- **Be concise**: Target <150 words total output
- **Be actionable**: Every suggestion should be specific and doable
- **Handle edge cases gracefully**:
  - No changes → Suggest reviewing recent commits or starting new work
  - Too many files (>20) → Sample most recently modified, note total count
  - Binary files → Skip analysis, just report count
  - Linter not installed → Suggest installation but don't error

- **Cross-platform**: Use git commands (available everywhere)
- **Focus on quick wins**: Highlight obvious improvements, not deep analysis

## Example Output

```markdown
## Code Review

**Changes**: 3 files modified (2 staged, 1 unstaged)

- **src/commands/review.md**: New command template, follows /orient pattern well
- **src/prompts/review.prompt.md**: Copilot version, mirrors Claude structure
- **README.md**: Added /review to command list (unstaged)

**Suggestions**:
- Add example output section to both templates
- Stage README.md with the template changes
- Consider running spell check on documentation

**Next Action**: Add examples, stage all files, then run /commit
```
