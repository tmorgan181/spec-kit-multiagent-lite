# Contract: /audit Command

**Purpose**: Perform security analysis on dependencies and code patterns

## Input
- Project dependency files (`requirements.txt`, `pyproject.toml`, `package.json`, etc.)
- Source code files (for pattern scanning)

## Execution Flow
1. Detect project type (Python, Node.js, etc.)
2. Find dependency manifest files
3. Check for `pip-audit` or equivalent tool
4. If tool available: run vulnerability scan
5. If tool not available: suggest installation
6. Scan code for common security anti-patterns:
   - Hardcoded secrets (API keys, passwords)
   - Weak cryptographic patterns
   - SQL injection risks
7. Generate concise report (<150 words)

## Output Format
```markdown
## Security Audit

**Dependencies**: [N scanned, M vulnerabilities found]

**Vulnerabilities**:
- [package-name](link): [severity] - [brief description]

**Code Patterns**:
- [file:line]: [pattern] - [recommendation]

**Next Action**: [Fix CVE-XXXX / Review auth implementation / etc.]
```

## Edge Cases
- **No dependencies**: Report "No dependencies to audit" gracefully
- **Tool not installed**: Provide installation command, basic manual checks only
- **False positives**: Note that manual review may be needed
- **No vulnerabilities**: Celebrate! Still suggest best practices

## Success Criteria
- ✅ Detects Python, Node.js, Rust, Go dependency files
- ✅ Gracefully handles missing audit tools
- ✅ Scans for top 10 OWASP patterns
- ✅ Output <150 words with actionable links
