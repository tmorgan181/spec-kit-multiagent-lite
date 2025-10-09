---
description: Generate concise project metrics for AI agent orientation
---

# Project Statistics

**Purpose**: Provide quick project overview metrics for AI agents joining a project or assessing scope.

## Execution Steps

Execute the following steps to gather project statistics:

### 1. Count Lines of Code

**Preferred method** (if tokei installed):
```bash
# Check if tokei is available
command -v tokei >/dev/null 2>&1

# If available, use tokei for fast, accurate counts
tokei --output json
```

**Fallback method** (if tokei not available):
```bash
# Python
find . -name "*.py" -type f | xargs wc -l 2>/dev/null | tail -1

# JavaScript/TypeScript
find . -name "*.js" -o -name "*.ts" | xargs wc -l 2>/dev/null | tail -1

# Markdown
find . -name "*.md" -type f | xargs wc -l 2>/dev/null | tail -1

# All files combined
find . -type f -not -path "*/\.*" | xargs wc -l 2>/dev/null | tail -1
```

### 2. Count Files and Directories

```bash
# Count files (excluding hidden)
find . -type f -not -path "*/\.*" | wc -l

# Count directories (excluding hidden)
find . -type d -not -path "*/\.*" | wc -l
```

### 3. Get Git History Summary

```bash
# Total commits
git log --oneline | wc -l

# Contributor count
git log --format='%aN' | sort -u | wc -l

# Recent activity
git log --oneline -5
```

If not a git repository, skip this section.

### 4. Check for Test Coverage

Look for common coverage report files:
```bash
# Python coverage files
ls .coverage coverage.xml htmlcov/ 2>/dev/null

# JavaScript coverage
ls coverage/ .nyc_output/ 2>/dev/null

# If coverage files exist, try to extract percentage
# Python: coverage report | grep TOTAL
# JavaScript: cat coverage/coverage-summary.json
```

### 5. Generate Concise Table Output

Provide stats in this format (~20 lines max):

```markdown
## Project Statistics

**Code**:
- Language1: X,XXX LOC (NN%)
- Language2: XXX LOC (NN%)
- Language3: XX LOC (NN%)

**Structure**:
- NN files, NN directories
- NNN commits, N contributors

**Testing**:
- Coverage: NN% (or N/A)
- Tests: NN files (or N/A)

**Next Action**: [Explore src/ / Review tests / Check docs]
```

## Important Notes

- **Be concise**: Keep output under 20 lines
- **Use tables**: Well-formatted markdown tables or lists
- **Handle missing tools**:
  - No tokei → Use find/wc fallback, note "Basic LOC count"
  - Not a git repo → Skip git section, note "No git history"
  - No coverage → Show "N/A" gracefully

- **Percentages**: Calculate language percentages from total LOC
- **Large repos**: If >100k LOC, note "Large project" and consider sampling
- **Speed**: Target <5 second execution time

## Edge Cases

- **No git repository**: Skip git section, show file/LOC stats only
- **No test coverage reports**: Show "Coverage: N/A"
- **Tokei not installed**: Use find/wc fallback, note in output
- **Very large repo (1M+ LOC)**: Sample or provide high-level summary only
- **No code files**: "Appears to be a documentation-only or data project"

## Example Output

```markdown
## Project Statistics

**Code**:
- Python: 2,453 LOC (87%)
- Markdown: 342 LOC (12%)
- YAML: 28 LOC (1%)
- Total: 2,823 LOC

**Structure**:
- 45 files, 12 directories
- 127 commits, 3 contributors

**Testing**:
- Coverage: 78% (via pytest-cov)
- Tests: 23 test files

**Next Action**: Explore src/ directory to understand core modules
```

```markdown
## Project Statistics

**Code** (tokei not available, using basic count):
- Python: ~1,200 lines
- Markdown: ~400 lines
- Total: ~1,600 lines (approximate)

**Structure**:
- 32 files, 8 directories
- Not a git repository

**Testing**:
- Coverage: N/A
- Tests: N/A

**Next Action**: Check if this is a standalone library or tool
```
