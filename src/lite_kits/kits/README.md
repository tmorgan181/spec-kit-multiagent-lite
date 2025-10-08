# Spec-Kit Add-on Kits

This directory contains modular add-on kits that can be installed independently or in combination on top of vanilla spec-kit projects.

## Available Kits

### ✅ Recommended (Default Installation)

#### 1. **project-kit**
**Commands**: `/orient` ⭐, `/review`, `/audit`, `/stats`
**Scripts**: Enhanced feature creation with custom naming

Essential project-level utilities combining agent orientation, code quality checks, and vanilla spec-kit enhancements.

**Installs to**:
- `.claude/commands/` (Claude Code)
- `.github/prompts/` (GitHub Copilot)
- `.specify/scripts/{bash,powershell}/` (Enhanced scripts)

**Use case**: Every project should have this. `/orient` is essential for all AI agents.

---

#### 2. **git-kit**
**Commands**: `/commit`, `/pr`, `/sync`, `/cleanup`

Git workflow automation with smart commits, PR creation, sync status, and cleanup operations. Includes ASCII visualization for better readability.

**Installs to**:
- `.claude/commands/` (Claude Code)
- `.github/prompts/` (GitHub Copilot)

**Use case**: Daily git operations made easier with agent assistance.

---

### 📦 Optional

#### 3. **multiagent-kit**
**Files**: Collaboration directories, PR workflow, git worktrees protocol

Multi-agent coordination structure for complex projects with multiple AI agents working in parallel.

**Dependencies**: Requires `project-kit` (for `/review`) and `git-kit` (for `/commit`, `/pr`)

**Installs to**:
- `.specify/memory/pr-workflow-guide.md`
- `.specify/memory/git-worktrees-protocol.md`
- `specs/*/collaboration/` (template, created per-feature)

**Use case**: Large projects with multiple AI agents collaborating (e.g., Claude Code + Copilot).

---

## Installation Matrix

| Kit | Default | Target Users | Adds | Dependencies |
|-----|---------|--------------|------|--------------|
| **project** | ✅ Yes | Everyone | 4 commands + enhanced scripts | None |
| **git** | ✅ Yes | Everyone | 4 commands with ASCII viz | None |
| **multiagent** | ❌ No | Multi-agent projects | Collaboration structure | project, git |

## Kit Structure

Each kit follows this structure:

```
kit-name/
├── README.md              # What this kit does
├── claude/                # Claude Code files (optional)
│   └── commands/          # Slash commands
├── github/                # GitHub Copilot files (optional)
│   └── prompts/           # Prompt files
├── scripts/               # Shell scripts (optional)
│   ├── bash/
│   └── powershell/
├── memory/                # Living documentation (optional)
└── templates/             # File templates (optional)
```

## Cross-Platform & Cross-Agent Support

All kits support:
- **Agents**: Claude Code, GitHub Copilot (both included by default)
- **Shells**: Bash (Linux/macOS), PowerShell (Windows/cross-platform)

When installed, files go to the appropriate locations:
- Claude Code: `.claude/commands/*.md`
- GitHub Copilot: `.github/prompts/*.prompt.md`
- Scripts: `.specify/scripts/{bash,powershell}/*.{sh,ps1}`

## Installation

### Install Recommended Kits (project + git)

```bash
lite-kits install -Recommended
# or
lite-kits install -Kit project,git
```

### Install Individual Kits

```bash
lite-kits install -Kit project
lite-kits install -Kit git
lite-kits install -Kit multiagent  # Auto-installs project + git
```

### Install All Kits

```bash
lite-kits install -All
```

### Uninstall Kits

```bash
lite-kits remove -Kit multiagent
lite-kits remove -Kit git,project
```

## Design Principles

### ✅ DO
- Only add new files (never modify vanilla files)
- Support both Claude Code and GitHub Copilot
- Support both Bash and PowerShell
- Keep commands simple (markdown prompts)
- Version-safe (upgradable without conflicts)
- Modular (install/uninstall independently)

### ❌ DON'T
- Modify vanilla spec-kit files
- Add runtime dependencies
- Require specific Python/Node versions
- Lock users into specific agents or shells
- Create tight coupling between kits

## Kit Details

### project-kit Commands

| Command | Description |
|---------|-------------|
| `/orient` | Agent orientation (read docs, check git, determine role) |
| `/review` | Code review against constitution and best practices |
| `/audit` | Security and quality audit |
| `/stats` | Project statistics (LOC, test coverage, complexity) |

### git-kit Commands

| Command | Description |
|---------|-------------|
| `/commit` | Smart commit with agent attribution |
| `/pr` | Create pull request with auto-generated description |
| `/sync` | Show sync status with ASCII visualization |
| `/cleanup` | Clean merged branches, stale worktrees |

### project-kit Enhancements

| Enhancement | Description |
|-------------|-------------|
| Custom feature numbers | Specify exact feature number instead of auto-increment |
| Custom feature names | Full control over branch/directory names |
| Feature templates | Pre-configured structures (api, cli, library) |

### multiagent-kit Structure

| Component | Description |
|-----------|-------------|
| PR workflow guide | How AI agents create PRs |
| Git worktrees protocol | Parallel development with worktrees |
| Collaboration directories | Active/archive/results structure |

## Examples

- **minimal-todo-app**: Uses `project` + `git` kits
- **blog-with-auth**: Uses `project` + `git` + `multiagent` kits

See [examples/](../../examples/) for working examples.

## Contributing

See [CONTRIBUTING.md](../../CONTRIBUTING.md) for guidelines on adding new kits.

New kit ideas:
- `testing-kit`: Test generation helpers
- `ci-kit`: GitHub Actions templates
- `deploy-kit`: Deployment workflows
- `debug-kit`: Debugging helpers
