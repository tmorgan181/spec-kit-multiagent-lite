---
description: Perform security analysis on dependencies and code patterns
---

# Security Audit Helper

**Purpose**: Quick security analysis for AI agents working on features involving authentication, data handling, or external dependencies.

## Execution Steps

Execute the following steps to perform a security audit:

### 1. Detect Project Type and Dependencies

```bash
# Check for Python dependencies
ls requirements.txt pyproject.toml setup.py 2>/dev/null

# Check for Node.js dependencies
ls package.json package-lock.json 2>/dev/null

# Check for Rust dependencies
ls Cargo.toml Cargo.lock 2>/dev/null

# Check for Go dependencies
ls go.mod go.sum 2>/dev/null
```

### 2. Run Dependency Vulnerability Scan

**Python projects**:
```bash
# Check if pip-audit is available
command -v pip-audit >/dev/null 2>&1

# If available, run scan
pip-audit

# If not available, suggest installation
echo "Install pip-audit: pip install pip-audit"
```

**Node.js projects**:
```bash
# npm audit is built-in
npm audit

# Or use yarn
yarn audit
```

**Other languages**: Suggest appropriate tools (cargo audit, go list, etc.)

### 3. Scan for Common Security Anti-Patterns

Check source code for security issues:

```bash
# Look for potential hardcoded secrets
grep -r "API_KEY\s*=\s*['\"]" src/ 2>/dev/null | head -5
grep -r "PASSWORD\s*=\s*['\"]" src/ 2>/dev/null | head -5
grep -r "SECRET\s*=\s*['\"]" src/ 2>/dev/null | head -5

# Look for weak crypto patterns (Python)
grep -r "md5\|sha1" src/ 2>/dev/null | head -5

# Look for SQL injection risks
grep -r "execute.*%\|execute.*+" src/ 2>/dev/null | head -5
```

**Common patterns to flag**:
- Hardcoded API keys, passwords, tokens
- Weak cryptographic algorithms (MD5, SHA1)
- SQL string concatenation
- Eval/exec with user input
- Insecure file permissions

### 4. Generate Concise Report

Provide analysis in this format (~150 words max):

```markdown
## Security Audit

**Dependencies**: N scanned, M vulnerabilities found

**Vulnerabilities** (if any):
- package-name==version: [SEVERITY] - Brief description
- Link to advisory for details

**Code Patterns** (if any):
- file.py:line: [PATTERN] - Recommendation

**Next Action**: [Fix CVE-XXXX / Update package / Review auth code]
```

## Important Notes

- **Graceful fallbacks**: If audit tools not installed, do basic pattern checks only
- **Be concise**: Target <150 words total output
- **Prioritize**: Show highest severity issues first
- **Avoid false positives**: Note that manual review may be needed
- **No dependencies**: Report "No dependencies to audit" gracefully
- **Cross-platform**: Use commands available on Windows, macOS, Linux

## Edge Cases

- **No dependency files**: "No dependencies found. This appears to be a dependency-free project."
- **Tool not installed**: Provide installation command, run basic grep checks
- **No vulnerabilities**: "✅ No known vulnerabilities found! Consider reviewing auth/data handling patterns."
- **Too many issues**: Sample top 5, note total count

## Example Output

```markdown
## Security Audit

**Dependencies**: 12 scanned, 2 vulnerabilities found

**Vulnerabilities**:
- requests==2.25.0: MEDIUM - CVE-2023-32681 (Proxy-Auth header leak)
  Update to: requests>=2.31.0

**Code Patterns**:
- src/auth.py:42: Hardcoded API key detected
- src/db.py:103: SQL string concatenation (injection risk)

**Next Action**: Update requests package, move API key to environment variables, use parameterized queries
```

```markdown
## Security Audit

**Dependencies**: pip-audit not installed

**Tool Not Available**:
Install pip-audit for vulnerability scanning:
`pip install pip-audit`

**Code Patterns**: Basic grep checks performed, no obvious issues found

**Next Action**: Install pip-audit and re-run for comprehensive dependency scan
```
