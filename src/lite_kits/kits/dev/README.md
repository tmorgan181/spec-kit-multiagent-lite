# Dev Kit

**Status**: ✅ Recommended (Default)

Essential development utilities for solo developers using spec-kit. Combines project management commands with git workflow automation.

## What It Adds

### Commands (AI Agents)

| Command | Claude Code | GitHub Copilot | Description |
|---------|-------------|----------------|-------------|
| `/orient` | ✅ | ✅ | Agent orientation protocol (most essential!) |
| `/commit` | ✅ | ✅ | Smart commit with staging and message generation |
| `/pr` | ✅ | ✅ | Pull request creation with auto-push |
| `/review` | ✅ | ✅ | Code review helper for staged changes |
| `/cleanup` | ✅ | ✅ | Safe branch cleanup (delete merged branches) |
| `/audit` | 🚧 | 🚧 | Security & quality audit (coming soon) |
| `/stats` | 🚧 | 🚧 | Project statistics (coming soon) |

✅ = Implemented | 🚧 = Coming Soon

## Installation

### As recommended kit (default):
```bash
lite-kits add --recommended  # Installs dev-kit
```

### Individually:
```bash
lite-kits add --kit dev
```

## What Gets Installed

```
your-project/
├── .claude/commands/              # If Claude Code detected
│   ├── orient.md                  # ✅ Essential!
│   ├── commit.md                  # ✅ Smart commits
│   ├── pr.md                      # ✅ PR creation
│   ├── review.md                  # ✅ Code review
│   ├── cleanup.md                 # ✅ Branch cleanup
│   ├── audit.md                   # 🚧 Coming Soon
│   └── stats.md                   # 🚧 Coming Soon
└── .github/prompts/               # If GitHub Copilot detected
    ├── orient.prompt.md           # ✅ Essential!
    ├── commit.prompt.md           # ✅ Smart commits
    ├── pr.prompt.md               # ✅ PR creation
    ├── review.prompt.md           # ✅ Code review
    ├── cleanup.prompt.md          # ✅ Branch cleanup
    ├── audit.prompt.md            # 🚧 Coming Soon
    └── stats.prompt.md            # 🚧 Coming Soon
```

**Note**: Vanilla spec-kit files are **never modified** - only new files are added.

## Commands

### `/orient` - Agent Orientation ⭐ ESSENTIAL

**Purpose**: Help AI agents quickly understand project context before starting work.

**What it does**:
1. Detects installed kits
2. Determines agent role
3. Reads project documentation (`.github/copilot-instructions.md`, `.specify/memory/constitution.md`)
4. Checks current git state (branch, recent commits, changes)
5. Reviews active spec work
6. Outputs concise summary (~150 words max)

**Example usage**:
```
/orient

## Orientation Complete

**Installed Kits**: dev

**I am**: claude-sonnet-4.5 @ Claude Code (Primary)
**Project**: Lite-kits - Lightweight enhancement kits for spec-driven development
**Stack**: Python 3.11+, typer, rich
**Branch**: develop
**Recent work**: Merged PR #16 (kit refactor)
**Uncommitted changes**: 12 files
**Active feature**: None
**Coordination**: Solo work

**Next suggested action**: Review uncommitted changes with /review
```

**Why this is essential**: Every AI agent should run `/orient` at the start of each session to get up to speed quickly without wasting tokens.

---

### `/commit` - Smart Commit

**Purpose**: Intelligent commit workflow with staging proposals and message generation.

**What it does**:
- Analyzes unstaged changes
- Proposes files to stage
- Generates conventional commit message
- Shows combined staging + message for approval
- Supports multi-commit suggestions for large changesets

---

### `/pr` - Pull Request Creation

**Purpose**: Create pull request with automatic branch push.

**What it does**:
- Checks for existing PR (prevents duplicates)
- Pushes current branch to remote
- Generates PR description from commits
- Creates PR via `gh pr create`
- Shows PR URL when complete

---

### `/review` - Code Review

**Purpose**: Review staged changes against project conventions and best practices.

**What it does**:
- Analyzes staged changes (`git diff --staged`)
- Checks against constitution principles
- Identifies common code smells
- Suggests improvements
- Verifies test coverage

---

### `/cleanup` - Branch Cleanup

**Purpose**: Safely delete merged branches.

**What it does**:
- Lists merged branches
- Excludes current branch, base branches (main/develop)
- Confirms before deletion
- Optional remote deletion (`--remote` flag)
- Protected branch safety

---

### `/audit` - Security & Quality Audit (Coming Soon)

**Purpose**: Scan for security issues and quality problems.

**Planned features**:
- Scan for hardcoded secrets/credentials
- Check for common vulnerabilities (SQL injection, XSS, CSRF)
- Analyze dependencies for known CVEs
- Verify input validation
- Check file permissions

---

### `/stats` - Project Statistics (Coming Soon)

**Purpose**: Show project health metrics.

**Planned features**:
- Lines of code by language
- Test coverage percentage
- Git activity with agent attribution
- Complexity metrics
- Dependency count
- Health score

---

## Use Cases

### Solo Developer with AI Agent
**Install**: `lite-kits add --recommended` (includes dev-kit)
**Use**: `/orient` at start of every session, `/commit` and `/pr` for git workflow

### Pair Programming with Claude Code
**Install**: `lite-kits add --recommended`
**Use**: `/orient` → `/review` → `/commit` → `/pr` workflow

### Security-Focused Project
**Install**: `lite-kits add --kit dev`
**Use**: `/audit` regularly for security scans (when implemented)

---

## Configuration

No configuration needed - works out of the box.

**Optional customization**:
- Edit `.github/copilot-instructions.md` - Affects `/orient` output
- Edit `.specify/memory/constitution.md` - Project principles for `/review`

---

## Dependencies

**None** - dev-kit is standalone.

**Optional pairing**: Works great with multiagent-kit for team coordination.

---

## Compatibility

- ✅ **Agents**: Claude Code, GitHub Copilot
- ✅ **Platforms**: Linux, macOS, Windows
- ✅ **Shells**: Bash, PowerShell
- ✅ **Vanilla safe**: Only adds new files, never modifies existing

---

## Uninstall

```bash
lite-kits remove --kit dev
```

Removes:
- `.claude/commands/{orient,commit,pr,review,cleanup,audit,stats}.md`
- `.github/prompts/{orient,commit,pr,review,cleanup,audit,stats}.prompt.md`

---

## Future Enhancements

Considering for dev-kit:
- `/docs` - Generate/update documentation
- `/history` - Show project timeline
- `/dependencies` - Dependency analysis
- `/performance` - Performance profiling
- `/status` - Optimized git status command
- Template library (api, cli, library, frontend feature templates)

Suggest more in [GitHub Discussions](https://github.com/tmorgan181/lite-kits/discussions).
