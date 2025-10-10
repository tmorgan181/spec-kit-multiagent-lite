---
description: Review staged changes against best practices
---

# Code Review of Staged Changes

**Purpose**: Review staged git changes for quality, best practices, and potential issues before committing.

## Execution Steps

Execute the following steps to review staged changes:

### 1. Check Staged Files

```bash
# Get list of staged files with status
git diff --staged --name-status
```

**If no files are staged**:
- Inform user that nothing is staged
- Suggest running `git add` or `@terminal /commit` to stage and commit together
- Exit gracefully

### 2. Analyze Staged Changes

```bash
# Get the actual diff with context
git diff --staged
```

### 3. Review Changes

Analyze the diff output for:

**✅ Good Practices to Acknowledge**:
- Clear, descriptive function/variable names
- Appropriate comments where needed
- Consistent formatting
- Type hints (Python) or type annotations
- Test coverage for new code
- Error handling
- Input validation

**⚠️ Issues to Flag**:
- **Security**:
  - Hardcoded credentials or API keys
  - SQL injection vulnerabilities
  - XSS vulnerabilities
  - Unsafe deserialization
  - Missing authentication/authorization checks
  
- **Code Quality**:
  - TODOs or FIXMEs (should be tracked in issues)
  - Commented-out code blocks
  - Magic numbers without explanation
  - Overly complex functions (>50 lines)
  - Duplicate code patterns
  - Inconsistent naming conventions
  
- **Best Practices**:
  - Missing error handling
  - No logging for important operations
  - Hardcoded configuration values
  - Missing input validation
  - Unused imports or variables
  - Missing docstrings for public APIs

### 4. Present Review Results

Format output as follows:

```
## Code Review Results

**Staged files**: [count]
[list files with status: A=added, M=modified, D=deleted]

**Summary of changes**:
[brief description of what's being changed]

===========================================================
**✅ Good Practices Found:**
===========================================================

[List positive findings, grouped by file]
- [file]: [specific good practice observed]

===========================================================
**⚠️ Suggestions for Improvement:**
===========================================================

[List issues/suggestions, grouped by file with line numbers if possible]
- [file]:[line]: [specific issue and suggested fix]

===========================================================
**🔒 Security Check:**
===========================================================

[Report any security concerns or confirm none found]
- ✓ No hardcoded credentials detected
- ✓ No obvious security vulnerabilities
- ⚠ [Any security concerns]

===========================================================
**📊 Overall Assessment:**
===========================================================

[One of: "Ready to commit", "Ready with minor suggestions", "Needs changes"]

[Brief summary of overall code quality]

**Recommendation**: [Approve / Address suggestions / Do not commit]
```

### 5. Handle User Response

After presenting results, wait for user action. They may:
- Proceed with commit anyway
- Make changes and re-review
- Cancel the review

## Example Output

```
## Code Review Results

**Staged files**: 3
- A  src/auth.py (new file)
- M  src/models.py (modified)
- A  tests/test_auth.py (new file)

**Summary of changes**:
Adding user authentication system with bcrypt password hashing
and JWT token generation.

===========================================================
**✅ Good Practices Found:**
===========================================================

- src/auth.py: Clear function names (hash_password, verify_password)
- src/auth.py: Type hints used throughout
- src/auth.py: Comprehensive docstrings for all functions
- src/models.py: Proper SQLAlchemy relationship definitions
- tests/test_auth.py: Good test coverage with fixtures

===========================================================
**⚠️ Suggestions for Improvement:**
===========================================================

- src/auth.py:45: Consider extracting hash_password to utils module
  Current: Function in auth.py
  Suggest: Move to src/utils/crypto.py for reusability

- src/models.py:12: TODO comment present
  Line: "# TODO: Add password reset functionality"
  Suggest: Create GitHub issue and reference it in comment

- tests/test_auth.py:67: Missing edge case test
  Suggest: Add test for empty password input

- src/auth.py:23: Magic number for token expiration
  Current: expires_delta = timedelta(hours=24)
  Suggest: Move to config file or environment variable

===========================================================
**🔒 Security Check:**
===========================================================

✓ No hardcoded credentials detected
✓ Using bcrypt for password hashing (good choice!)
✓ JWT tokens generated securely
⚠ Consider adding rate limiting to prevent brute force attacks

===========================================================
**📊 Overall Assessment:**
===========================================================

**Status**: Ready with minor suggestions

The code follows good practices with proper type hints, docstrings,
and test coverage. The suggestions above are minor improvements that
can be addressed now or in future iterations.

**Recommendation**: Approve and commit - suggestions are non-blocking
```

## Important Notes

- This command is **read-only** - it never modifies files
- Focus on **actionable feedback** - be specific about what to change
- Be **encouraging** - acknowledge good practices
- **Security first** - always check for security issues
- Keep review **concise** - don't overwhelm with minor issues
- **Respect the agent's work** - balance critique with acknowledgment

## Integration with Other Commands

- Run `@terminal /review` before `@terminal /commit` to catch issues early
- Use after making changes and staging them with `git add`
- Combine with `@terminal /pr` workflow - review before creating PR
- Works great in multi-agent workflows (one agent reviews another's work)
