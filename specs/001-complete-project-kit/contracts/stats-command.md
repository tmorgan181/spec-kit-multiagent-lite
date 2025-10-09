# Contract: /stats Command

**Purpose**: Generate concise project metrics for AI agent orientation

## Input
- Repository root directory
- Source code files
- Git history
- Test coverage reports (if present)

## Execution Flow
1. Count lines of code by language (use `tokei` if available, fallback to `find`/`wc`)
2. Count files and directories
3. Get git history summary (`git log --oneline | wc -l`, contributor count)
4. Check for coverage reports (`.coverage`, `coverage.xml`, etc.)
5. Generate table format output (<20 lines)

## Output Format
```markdown
## Project Statistics

**Code**:
- Python: 2,453 LOC (87%)
- Markdown: 342 LOC (12%)  
- YAML: 28 LOC (1%)

**Structure**:
- 45 files, 12 directories
- 127 commits, 3 contributors

**Testing**:
- Coverage: 78% (if available)
- Tests: 23 files (if detectable)

**Next Action**: [Explore src/ / Review tests / Check docs]
```

## Edge Cases
- **`tokei` not installed**: Use `find . -name "*.py" | xargs wc -l` fallback
- **No git history**: Report "Not a git repository" or "No commits"
- **No tests**: Show "0% coverage" or "N/A"
- **Very large repo (1M+ LOC)**: Sample or provide summary stats only

## Success Criteria
- ✅ Works on repos from 10 LOC to 1M+ LOC
- ✅ Detects 10+ common languages
- ✅ Output fits in ~20 lines (concise table)
- ✅ Runs in <5 seconds on typical repo
