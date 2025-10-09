# Contract: /review Command

**Purpose**: Analyze code quality for uncommitted changes or recent commits

## Input
- Git repository state (uncommitted changes, staged files)
- Project files (.gitignore, linting configs if present)

## Execution Flow
1. Check for uncommitted changes (`git status --short`)
2. If changes exist: analyze diff (`git diff`, `git diff --cached`)
3. If no changes: suggest reviewing recent commits
4. Check for linting configs (`.ruff.toml`, `.pylintrc`, etc.)
5. Suggest running linters if configs found
6. Generate concise output (<150 words)

## Output Format
```markdown
## Code Review

**Changes**: N files modified

- file1.py: [brief assessment]
- file2.py: [brief assessment]

**Suggestions**:
- [Actionable suggestion 1]
- [Actionable suggestion 2]

**Next Action**: [Run linter / Commit changes / Review X pattern]
```

## Edge Cases
- **No changes**: Suggest `git log -1 --stat` or prompt user
- **Too many files (>20)**: Sample most recently modified
- **Binary files**: Skip, report count only
- **Linter not installed**: Suggest installation, don't error

## Success Criteria
- ✅ Handles repos with 0-1000+ uncommitted files
- ✅ Runs in <5 seconds on typical repo
- ✅ Output fits in chat window (<150 words)
- ✅ Cross-platform (Windows, macOS, Linux)
