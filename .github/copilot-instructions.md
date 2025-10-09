# lite-kits Development Guidelines

**Project**: A pip-installable collection of lightweight enhancement kits for spec-driven development  
**Repository**: https://github.com/tmorgan181/lite-kits  
**Current Version**: 0.1.1 (Alpha)

## Core Architecture

### Add-on Philosophy (NOT a Fork)
lite-kits **enhances** vanilla [GitHub Spec-Kit](https://github.com/github/spec-kit) without replacing any core files. This is critical:
- ✅ **Only adds new files** - Never modifies existing spec-kit files
- ✅ **Modular installation** - Users can add/remove individual kits
- ✅ **Vanilla compatibility** - Users continue to get upstream spec-kit updates
- ✅ **Reversible** - Complete uninstall returns to vanilla state

### Kit-Based Architecture
Three modular enhancement kits that can be installed independently:

```
project-kit    → /orient command (essential for AI agents)
git-kit        → /commit, /pr, /cleanup commands  
multiagent-kit → /sync command + collaboration structure
```

**Dependencies**: `multiagent-kit` auto-includes `project-kit` + `git-kit`

### What Gets Installed
When users run `lite-kits add --recommended`, the system copies template files:

```
.claude/commands/           ← Claude Code slash commands
.github/prompts/           ← GitHub Copilot prompt files  
.specify/memory/           ← Memory guides (multiagent only)
.specify/templates/        ← Collaboration templates (multiagent only)
```

**Key insight**: These are **markdown prompt files**, not runtime code. The "commands" are AI assistant prompts that guide agents through workflows.

## Technology Stack

**Core Implementation**:
- **Python 3.11+** with modern `typer` + `rich` CLI
- **uv** for packaging (not pip/setuptools)
- **Cross-platform**: PowerShell + Bash scripting
- **Cross-agent**: Claude Code + GitHub Copilot support

**Project Structure**:
```python
src/lite_kits/
├── cli.py              # Typer-based CLI with beautiful ASCII banners
├── core/
│   ├── installer.py    # Core installation logic  
│   └── banner.py       # Rich-based rainbow ASCII art system
└── kits/              # Template files organized by kit
    ├── project/       # /orient command templates
    ├── git/           # /commit, /pr, /cleanup templates  
    └── multiagent/    # /sync + collaboration structure
```

## Essential Development Commands

### Package Development Workflow
```bash
# Install editable for development
uv tool install -e .

# Build distribution  
uv build

# Test on vanilla spec-kit project
cd /tmp && specify init test-project && cd test-project
lite-kits add --dry-run --recommended  # Preview
lite-kits add --recommended            # Install
/orient  # Test the command works
```

### CLI Usage Patterns
```bash
# Beautiful banner + status
lite-kits status

# Add kits to project
lite-kits add --recommended            # project + git kits
lite-kits add --kit multiagent         # specific kit (auto-includes deps)

# Remove kits (returns to vanilla)
lite-kits remove --kit git
lite-kits remove --all

# Validation & info
lite-kits validate                     # Check installation health
lite-kits info                         # Package details with tables
```

## Critical Code Patterns

### Banner System (`banner.py`)
Beautiful rainbow ASCII art with:
- **Static banners** for daily use (`show_static_banner()`)
- **Animated reveals** for special moments (`diagonal_reveal_banner()`)
- **Loading spinners** with rich animations (`show_loading_spinner()`)

### Installation Logic (`installer.py`)
**Key insight**: Installation is **file copying**, not code execution:

```python
def _install_file(self, kit_relative_path: str, target_relative_path: str):
    source = self.kits_dir / kit_relative_path  # From src/lite_kits/kits/
    target = self.target_dir / target_relative_path  # To user's project
    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
```

**Multi-interface support**: Detects `.claude/` vs `.github/prompts/` and installs appropriate versions.

### CLI Architecture (`cli.py`)
Modern `typer` + `rich` patterns:
- **No-args behavior**: Shows banner + quick start (not help)
- **UV-style flags**: `--version/-V`, `--quiet/-q`, `--verbose/-v`  
- **Beautiful output**: Tables, panels, colored status indicators
- **Error handling**: Graceful failures with helpful suggestions

## AI Agent Coordination

### Slash Commands Are Markdown Prompts
The `/orient`, `/commit`, `/pr` commands are **not executable code** - they're markdown files that AI assistants read as prompts:

```markdown
# .claude/commands/orient.md
---
description: Quickly orient to project context and current state
---

# Agent Orientation Protocol
Execute the following steps to gather orientation information:
...
```

### Cross-Agent Compatibility
All commands work across AI assistants:
- **Claude Code**: Reads `.claude/commands/*.md`
- **GitHub Copilot**: Reads `.github/prompts/*.prompt.md`

Templates are kept in sync but optimized per platform (e.g., PowerShell examples for Copilot).

### Multi-Agent Coordination (multiagent-kit)
When multiple AI agents work on the same project:

```
specs/NNN-feature/collaboration/
├── active/           # Current work sessions, decisions
├── archive/          # Historical work (YYYY-MM/)
└── results/          # Completed deliverables, validation
```

**Key protocols**:
- **Git worktrees** for parallel development (different directories, same branch)
- **Commit attribution**: `via claude-sonnet-4.5 @ claude-code`
- **Session logging**: Track what each agent accomplished
- **Territory assignment**: Avoid conflicts by defining ownership

## Project-Specific Conventions

### Kit Detection Logic
The installer uses **marker files** to detect installed kits:

```python
MARKER_PROJECT_KIT = ".claude/commands/orient.md"
MARKER_GIT_KIT = ".claude/commands/commit.md"  
MARKER_MULTIAGENT_KIT = ".specify/memory/pr-workflow-guide.md"
```

### Feature Numbering  
Follows spec-kit convention:
- **3-digit zero-padded**: `001-todo-app`, `007-demo-projects`
- **Kebab-case names**: `002-user-authentication`
- **Branch pattern**: `dev/NNN-feature-name` or `NNN-feature-name`

### Git Commit Attribution
AI agents must include model/interface info:

```
feat(001): add user authentication

Implements password hashing and JWT sessions.

via claude-sonnet-4.5 @ claude-code
```

**Tracked in CI**: The project tracks which AI models contribute which code for transparency.

## Integration Points & Dependencies

### Spec-Kit Integration
- **Requires**: Users must have [GitHub Spec-Kit](https://github.com/github/spec-kit) installed first
- **Detects**: Looks for `.specify/`, `.claude/`, or `.github/prompts/` directories
- **Enhances**: Adds coordination features to existing `/specify`, `/plan`, `/implement` workflow

### External Dependencies
- **No runtime deps**: Templates are pure markdown, no Python/Node runtime needed
- **CLI dependencies**: Only `typer` + `rich` for the installation CLI
- **Shell requirements**: Bash (Linux/macOS) or PowerShell (Windows/cross-platform)

### Cross-Platform Support
**Scripts included for both**:
- `scripts/bash/` - Linux/macOS shell scripts
- `scripts/powershell/` - Windows + cross-platform PowerShell

**File paths**: Always use `pathlib.Path` for cross-platform compatibility.

## Common Development Tasks

### Adding a New Kit
1. Create `src/lite_kits/kits/newkit/` directory
2. Add templates: `claude/commands/`, `github/prompts/`, `memory/`, etc.
3. Update `installer.py` with new kit logic
4. Add kit to `cli.py` constants and help text
5. Update `README.md` and examples

### Testing Installation
```bash
# Create test environment
cd /tmp && specify init test-project && cd test-project

# Test dry run
lite-kits add --dry-run --kit project

# Test actual install  
lite-kits add --kit project
ls .claude/commands/  # Should see orient.md

# Test command works
/orient  # Should run the orientation protocol
```

### Cross-Agent Testing
Since commands are markdown prompts, test by:
1. Installing kit in test project
2. Opening project in Claude Code - test `/orient` 
3. Opening project in GitHub Copilot - test prompt files
4. Verify both produce similar helpful output

### Debugging Installation Issues
```bash
# Check target project structure
lite-kits status  # Shows what's detected vs installed

# Validate installation  
lite-kits validate  # Detailed health check

# Check actual files
ls -la .claude/commands/
ls -la .github/prompts/
```

**Common issues**:
- Missing `.specify/` directory (not a spec-kit project)
- Wrong Python version (need 3.11+)  
- Permission errors (use `uv tool` not global pip)

### Contributing Guidelines
- **Test with multiple AI assistants** - Commands must work in Claude Code AND GitHub Copilot
- **Keep templates concise** - AI agents have token limits
- **Cross-platform compatibility** - Test on Windows PowerShell and Linux Bash
- **Preserve vanilla compatibility** - Never modify existing spec-kit files
- **Document in session logs** - Use collaboration structure for development tracking

---

*This guide helps AI agents understand the essential patterns needed to contribute effectively to lite-kits development.*