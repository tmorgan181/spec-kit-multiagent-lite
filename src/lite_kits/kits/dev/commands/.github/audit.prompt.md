---
description: Perform security analysis on dependencies and code patterns
---

# Security Audit Helper

**Purpose**: Quick security analysis for AI agents working on features involving authentication, data handling, or external dependencies.

## Execution Steps

Execute the following steps to perform a security audit:

### 1. Detect Project Type and Dependencies

```powershell
# Check for Python dependencies
Get-ChildItem -Path . -Include requirements.txt,pyproject.toml,setup.py -Recurse -ErrorAction SilentlyContinue

# Check for Node.js dependencies
Get-ChildItem -Path . -Include package.json,package-lock.json -Recurse -ErrorAction SilentlyContinue

# Check for Rust dependencies
Get-ChildItem -Path . -Include Cargo.toml,Cargo.lock -Recurse -ErrorAction SilentlyContinue

# Check for Go dependencies
Get-ChildItem -Path . -Include go.mod,go.sum -Recurse -ErrorAction SilentlyContinue
```

### 2. Run Dependency Vulnerability Scan

**Python projects**:
```powershell
# Check if pip-audit is available
Get-Command pip-audit -ErrorAction SilentlyContinue

# If available, run scan
pip-audit

# If not available, suggest installation
Write-Host "Install pip-audit: pip install pip-audit"
```

**Node.js projects**:
```powershell
# npm audit is built-in
npm audit

# Or use yarn
yarn audit
```

**Other languages**: Suggest appropriate tools (cargo audit, go list, etc.)

### 3. Scan for Common Security Anti-Patterns

Check source code for security issues:

```powershell
# Look for potential hardcoded secrets
Select-String -Path src\* -Pattern "API_KEY\s*=\s*['""]" -Recurse | Select-Object -First 5
Select-String -Path src\* -Pattern "PASSWORD\s*=\s*['""]" -Recurse | Select-Object -First 5
Select-String -Path src\* -Pattern "SECRET\s*=\s*['""]" -Recurse | Select-Object -First 5

# Look for weak crypto patterns (Python)
Select-String -Path src\* -Pattern "md5|sha1" -Recurse | Select-Object -First 5

# Look for SQL injection risks
Select-String -Path src\* -Pattern "execute.*%|execute.*\+" -Recurse | Select-Object -First 5
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
