# Quickstart: Complete Project Kit

**Feature**: 001-complete-project-kit
**Purpose**: Validate that `/review`, `/audit`, and `/stats` commands work correctly

## Prerequisites
- lite-kits installed (`uv tool install -e .` from repo root)
- Test project with project-kit installed

## Setup Test Environment

```bash
# Create test project
cd /tmp
mkdir test-project-kit
cd test-project-kit
git init

# Create sample Python files
cat > main.py << 'PYEOF'
def calculate(x, y):
    return x + y

# TODO: Add input validation
result = calculate(5, 3)
print(f"Result: {result}")
PYEOF

cat > requirements.txt << 'REQEOF'
requests==2.28.0  # Known vulnerability for testing
REQEOF

# Make some uncommitted changes
echo "# Test Project" > README.md
git add main.py requirements.txt
# Leave README.md uncommitted

# Create git history
git commit -m "Initial commit"
```

## Test Scenario 1: `/review` Command

**Given**: Uncommitted README.md file  
**When**: Agent runs `/review`  
**Then**: Output shows:
- 1 file modified (README.md)
- Brief assessment of the change
- Next action suggestion

**Manual Test**:
```bash
# In Claude Code or Copilot chat
/review
```

**Expected Output**:
```markdown
## Code Review

**Changes**: 1 file modified

- README.md: New file, basic project documentation

**Suggestions**:
- Add project description
- Include installation instructions

**Next Action**: Stage and commit changes with `/commit`
```

## Test Scenario 2: `/audit` Command

**Given**: requirements.txt with known vulnerability  
**When**: Agent runs `/audit`  
**Then**: Output shows:
- Dependency scan results
- Vulnerability in requests==2.28.0
- Remediation suggestion

**Manual Test**:
```bash
# Install pip-audit first (optional)
pip install pip-audit

# In Claude Code or Copilot chat
/audit
```

**Expected Output** (if pip-audit available):
```markdown
## Security Audit

**Dependencies**: 1 scanned, 1 vulnerability found

**Vulnerabilities**:
- requests==2.28.0: MEDIUM - CVE-2023-XXXX

**Code Patterns**:
- main.py:6: TODO comment - Consider adding validation

**Next Action**: Update requests to 2.31.0+
```

**Expected Output** (if pip-audit NOT available):
```markdown
## Security Audit

**Dependencies**: 1 file found (requirements.txt)

**Tool Not Available**:
Install pip-audit for vulnerability scanning:
`pip install pip-audit`

**Code Patterns**:
- main.py:6: TODO comment

**Next Action**: Install pip-audit and re-run
```

## Test Scenario 3: `/stats` Command

**Given**: Small test project  
**When**: Agent runs `/stats`  
**Then**: Output shows:
- LOC by language (Python)
- File/directory counts
- Git history summary

**Manual Test**:
```bash
# In Claude Code or Copilot chat
/stats
```

**Expected Output**:
```markdown
## Project Statistics

**Code**:
- Python: 8 LOC (80%)
- Text: 2 LOC (20%)

**Structure**:
- 3 files, 1 directory
- 1 commit, 1 contributor

**Testing**:
- Coverage: N/A

**Next Action**: Explore main.py to understand project structure
```

## Validation Checklist

- [ ] All three commands execute without errors
- [ ] Output is concise (<150 words each)
- [ ] Commands handle missing tools gracefully
- [ ] Cross-platform compatible (test on Windows if possible)
- [ ] Output format matches contracts
- [ ] Actionable next steps provided

## Cleanup

```bash
cd /tmp
rm -rf test-project-kit
```

## Success Criteria

✅ **All commands work** - No errors during execution  
✅ **Graceful fallbacks** - Missing tools don't crash commands  
✅ **Concise output** - Fits in chat window  
✅ **Actionable** - Clear next steps provided
