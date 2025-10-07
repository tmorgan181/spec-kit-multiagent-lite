# Project Kit

**Status**: ✅ Recommended (Default)

Essential project-level utilities and enhancements for vanilla spec-kit. Includes agent orientation, code review, quality checks, and enhanced feature creation scripts.

## What It Adds

### Commands (AI Agents)

| Command | Claude Code | GitHub Copilot | Description |
|---------|-------------|----------------|-------------|
| `/orient` | ✅ | ✅ | Agent orientation protocol (most essential!) |
| `/review` | 🚧 | 🚧 | Code review helper |
| `/audit` | 🚧 | 🚧 | Security & quality audit |
| `/stats` | 🚧 | 🚧 | Project statistics |

### Scripts (Enhanced Vanilla)

| Script | Bash | PowerShell | Description |
|--------|------|------------|-------------|
| Feature creation | 🚧 | 🚧 | Custom feature numbering/naming |

✅ = Implemented | 🚧 = Coming Soon

## Installation

### As part of recommended kits:
```bash
lite-kits install -Recommended  # project + git
```

### Individually:
```bash
lite-kits install -Kit project
```

## What Gets Installed

```
your-project/
├── .claude/commands/              # If Claude Code detected
│   ├── orient.md                  # ✅ Essential!
│   ├── review.md                  # 🚧 Coming Soon
│   ├── audit.md                   # 🚧 Coming Soon
│   └── stats.md                   # 🚧 Coming Soon
├── .github/prompts/               # If GitHub Copilot detected
│   ├── orient.prompt.md           # ✅ Essential!
│   ├── review.prompt.md           # 🚧 Coming Soon
│   ├── audit.prompt.md            # 🚧 Coming Soon
│   └── stats.prompt.md            # 🚧 Coming Soon
└── .specify/scripts/              # Enhanced vanilla scripts
    ├── bash/
    │   └── create-feature-enhanced.sh      # 🚧 Coming Soon
    └── powershell/
        └── Create-Feature-Enhanced.ps1     # 🚧 Coming Soon
```

**Note**: Vanilla spec-kit files are **never modified** - only new files are added.

## Commands

### `/orient` - Agent Orientation ⭐ ESSENTIAL

**Purpose**: Help AI agents quickly understand project context before starting work.

**What it does**:
1. Reads `.github/copilot-instructions.md` (primary source)
2. Reads `.specify/memory/constitution.md` (project philosophy)
3. Checks current git state (branch, recent commits)
4. Reviews collaboration directories (if multiagent-kit installed)
5. Determines agent role (Claude = leader, Copilot = specialist)
6. Outputs concise summary (~150-200 words)

**Example usage**:
```
/orient

## Orientation Complete - Primary Agent

**I am**: claude-sonnet-4.5 @ Claude Code (Primary)

**Project**: Pip-installable add-on for spec-kit

**Stack**: Python 3.11+, typer, rich

**Principles**:
- Add-on pattern (no vanilla modifications)
- Cross-platform (Bash + PowerShell)
- Cross-agent (Claude + Copilot)

**State**: Branch dev/001-starter-kits, 3 files changed

**Coordination**: Solo work

**Next**: Implement project-kit structure

**Confirm?**: Ready to proceed?
```

**Why this is essential**: Every AI agent should run `/orient` at the start of each session to get up to speed quickly without wasting tokens.

---

### `/review` - Code Review (Coming Soon)

**Purpose**: Review code changes against project constitution and best practices.

**What it will do**:
- Check staged changes against constitution principles
- Identify common code smells
- Suggest improvements
- Verify test coverage
- Check documentation completeness

---

### `/audit` - Security & Quality Audit (Coming Soon)

**Purpose**: Scan for security issues and quality problems.

**What it will do**:
- Scan for hardcoded secrets/credentials
- Check for common vulnerabilities (SQL injection, XSS, CSRF)
- Analyze dependencies for known CVEs
- Verify input validation
- Check file permissions

---

### `/stats` - Project Statistics (Coming Soon)

**Purpose**: Show project health metrics.

**What it will do**:
- Lines of code by language
- Test coverage percentage
- Git activity with agent attribution
- Complexity metrics
- Dependency count
- Health score

---

## Enhanced Scripts

### Feature Creation Enhancement (Coming Soon)

**Problem**: Vanilla `create-new-feature` script auto-generates feature numbers and uses first 3 words of description for naming.

**Enhancement**: Full control over feature numbering and naming.

**Usage** (planned):
```bash
# Vanilla (auto number, auto name from "Add user authentication system")
.specify/scripts/bash/create-new-feature.sh "Add user authentication system"
# Creates: 003-add-user-authentication

# Enhanced (custom number and name)
.specify/scripts/bash/create-feature-enhanced.sh --num 010 --name user-auth-v2 "Add user authentication system"
# Creates: 010-user-auth-v2

# Enhanced (custom number, auto name)
.specify/scripts/bash/create-feature-enhanced.sh --num 007 "Add user authentication system"
# Creates: 007-add-user-authentication
```

**Benefits**:
- Match feature numbers to issue/ticket numbers
- Use shorter, clearer names
- Support feature name conventions (e.g., `api-`, `ui-`, `db-` prefixes)

---

## Use Cases

### Solo Developer with AI Agent
**Install**: `--recommended` (includes project-kit)
**Use**: `/orient` at start of every session (essential!)

### Team with Multiple Agents
**Install**: `--recommended` + `--kit=multiagent`
**Use**: `/orient` + `/review` before committing

### Security-Focused Project
**Install**: `--recommended`
**Use**: `/audit` regularly, `/review` on every change

### Custom Workflow Needs
**Install**: `--kit=project`
**Use**: Enhanced scripts for precise feature naming

---

## Configuration

No configuration needed - works out of the box.

**Optional customization**:
- Edit `.github/copilot-instructions.md` - Affects `/orient` output
- Edit `.specify/memory/constitution.md` - Project principles for `/review`

---

## Dependencies

**None** - project-kit is standalone.

**Note**: multiagent-kit recommends project-kit for `/review` and best practices.

---

## Compatibility

- ✅ **Agents**: Claude Code, GitHub Copilot
- ✅ **Platforms**: Linux, macOS, Windows
- ✅ **Shells**: Bash, PowerShell
- ✅ **Vanilla safe**: Only adds new files, never modifies existing

---

## Uninstall

```bash
lite-kits remove -Kit project
```

Removes:
- `.claude/commands/{orient,review,audit,stats}.md`
- `.github/prompts/{orient,review,audit,stats}.prompt.md`
- `.specify/scripts/{bash,powershell}/create-feature-enhanced.{sh,ps1}`

---

## Future Enhancements

Considering for project-kit:
- `/docs` - Generate/update documentation
- `/history` - Show project timeline
- `/dependencies` - Dependency analysis
- `/performance` - Performance profiling
- Template library (api, cli, library, frontend feature templates)

Suggest more in [GitHub Discussions](https://github.com/tmorgan181/spec-kit-multiagent-lite/discussions).
