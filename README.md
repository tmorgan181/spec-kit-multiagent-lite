# lite-kits

**Lightweight enhancement kits for spec-driven development**

Add modular enhancement kits to vanilla [GitHub Spec-Kit](https://github.com/github/spec-kit) projects without forking or replacing core files.

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/tmorgan181/lite-kits)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What is this?

**lite-kits** enhances spec-driven development workflows built on [GitHub Spec-Kit](https://github.com/github/spec-kit).

Spec-Kit is a framework for AI-driven collaborative development (spec → plan → tasks → implement) using markdown prompts and scripts. Think "vibe coding" but with structure.

**lite-kits** adds three optional enhancement kits to vanilla spec-kit projects:

- 🎯 **project-kit** - Agent orientation (`/orient` command)
- 🔧 **git-kit** - Smart git workflows (`/commit`, `/pr`, `/cleanup`)
- 🤝 **multiagent-kit** - Multi-agent coordination (`/sync`, collaboration directories)

Each kit installs `.md` prompt files for AI assistants (Claude Code, GitHub Copilot, Cursor) and optional scripts.

## Key Features

### 🔧 Git-Kit

Smart git workflow commands:

**`/commit`** - Intelligent commits with staging proposals
- Combined staging + commit message approval
- Multi-commit suggestions for large changesets
- Conventional commits with feature numbers
- Agent attribution tracking

**`/pr`** - Pull request creation with auto-push
- Automatic branch pushing before PR
- PR status checking (prevents duplicates)
- Smart description generation from commits
- Modular PR scope (only describes current work)

**`/cleanup`** - Safe branch cleanup
- Delete merged branches safely
- Optional remote deletion
- Current branch detection
- Protected branch safety

### 🎯 Project-Kit

**`/orient`** - Agent orientation command
- Reads project documentation
- Checks current git state
- Determines agent role
- Provides concise context

### 🤝 Multiagent-Kit

**`/sync`** - Multi-agent coordination status
- Visual sync status display
- Agent activity tracking
- Collaboration structure detection

**Collaboration directories** for multi-agent coordination:
```
specs/NNN-feature/collaboration/
├── active/          # Current work
│   ├── sessions/    # Work session logs
│   └── decisions/   # Handoffs, proposals
├── archive/         # Historical (YYYY-MM/)
└── results/         # Completed deliverables
```

**Memory guides**:
- PR Workflow Guide - How AI agents create pull requests
- Git Worktrees Protocol - Parallel development with worktrees

## Installation

### Prerequisites

1. **GitHub Spec-Kit** - Install the `specify` CLI tool:
   ```bash
   # See: https://github.com/github/spec-kit
   npm install -g @github/specify
   # Or use pipx, etc.
   ```

2. **Create a spec-kit project** (if you don't have one):
   ```bash
   specify init my-project
   cd my-project
   ```

3. **Python 3.11+** - For lite-kits itself

4. **AI Assistant** - At least one: Claude Code, GitHub Copilot, or Cursor

### Install lite-kits

**Via pip** (when published):
```bash
pip install lite-kits
```

**From source** (current):
```bash
# Clone repository
git clone https://github.com/tmorgan181/lite-kits.git
cd lite-kits

# Install with uv (recommended)
uv tool install .

# Or with pip
pip install -e .
```

## Quick Start

### 1. Add kits to your spec-kit project

```bash
cd your-spec-kit-project
lite-kits add --here --dry-run --recommended  # Preview changes
lite-kits add --here --recommended            # Add project + git kits
```

**What gets added**:
- Git workflow commands (`/commit`, `/pr`, `/cleanup`)
- Project orientation command (`/orient`)
- Multi-agent coordination tools (`/sync`, collaboration structure) - optional
- Memory guides (PR workflow, git worktrees protocol) - optional

### 2. Use the commands in your AI assistant

```bash
# In Claude Code or GitHub Copilot
/orient     # Get project context
/commit     # Smart commit with staging
/pr         # Create PR with auto-push
/cleanup    # Clean up merged branches
/sync       # Check multi-agent status
```

### 3. Start building

```bash
# Standard spec-kit workflow with enhanced git commands
/specify Build a user authentication system
/plan
/tasks
/implement
/commit     # Use smart commit
/pr         # Auto-push and create PR
```

## Usage

### CLI Commands

**Kit Management:**
```bash
# Add kits to a project
lite-kits add --here --recommended           # Add project + git kits
lite-kits add --here --kit project           # Add specific kit
lite-kits add --here --dry-run --recommended # Preview changes

# Check status
lite-kits status --here                      # Show installed kits

# Validate installation
lite-kits validate --here                    # Verify kit installation

# Remove kits
lite-kits remove --here --kit git            # Remove specific kit
lite-kits remove --here --all                # Remove all kits
```

**Package Management:**
```bash
# Get package info
lite-kits info                               # Show version, kits, quick start

# Uninstall instructions
lite-kits uninstall                          # How to remove package

# Version
lite-kits --version                          # Show version only
```

### Git Workflow Example

```bash
# Make changes to your code

# Smart commit with combined staging + message approval
/commit
# Shows: staging plan + commit message in one prompt
# Options: y (approve), es (edit staging), em (edit message)

# Create PR (auto-pushes branch first!)
/pr
# Checks: No existing PR, pushes branch, creates PR
# Description: Only describes commits in THIS PR (modular scope)

# Clean up merged branches
/cleanup
# Safe deletion with protection for current/base/unmerged branches
# Optional: --remote flag to delete from remote too
```

### Multi-Agent Workflow Example

**Scenario**: Claude Code (backend) + GitHub Copilot (frontend) building a blog.

1. **Claude Code**: Creates spec and plan
   ```bash
   /specify Build a blog platform with auth
   /plan
   ```

2. **Claude Code**: Creates handoff document
   ```
   specs/002-blog/collaboration/active/decisions/agent-split.md
   - Claude: Backend (API, database, auth)
   - Copilot: Frontend (React, UI, components)
   ```

3. **Both agents**: Work in parallel with git worktrees
   ```bash
   # Claude
   git worktree add ../blog-backend 002-blog

   # Copilot
   git worktree add ../blog-frontend 002-blog
   ```

4. **Both agents**: Commit with attribution
   ```bash
   /commit
   # Message includes: via claude-sonnet-4.5 @ claude-code
   ```

5. **Check sync status**:
   ```bash
   /sync
   # Shows: agent activity, collaboration status, recommendations
   ```

6. **Integration**: Test together, create PR with `/pr`

## Architecture

### Add-on Design (Not a Fork)

**lite-kits** is an **add-on** for vanilla spec-kit, not a fork or replacement:

- ✅ **Vanilla spec-kit stays vanilla** - Your `specify` workflow is unchanged
- ✅ **Get upstream updates** - Benefit from spec-kit improvements automatically
- ✅ **Modular kits** - Add/remove individual kits as needed
- ✅ **No file replacements** - Only adds new files, never modifies spec-kit core

### What Gets Added

When you run `lite-kits add`, it installs `.md` prompt files and optional scripts:

**Kit commands** (markdown prompts for AI assistants):
- `.claude/commands/*.md` - Claude Code slash commands
- `.github/prompts/*.prompt.md` - GitHub Copilot prompt files

**Memory guides** (multiagent-kit only):
- `.specify/memory/pr-workflow-guide.md` - How AI agents should create PRs
- `.specify/memory/git-worktrees-protocol.md` - Parallel dev with worktrees

**Collaboration structure** (multiagent-kit only):
- `specs/NNN-feature/collaboration/` - Session logs, handoffs, decisions

**No modifications** to existing spec-kit files like `.specify/`, vanilla prompts, etc.

## Project Structure

```
lite-kits/
├── src/lite_kits/
│   ├── __init__.py
│   ├── cli.py              # CLI commands
│   ├── installer.py        # Installation logic
│   └── kits/               # Enhancement kits
│       ├── git/            # Git workflow commands
│       ├── project/        # Project orientation
│       └── multiagent/     # Multi-agent coordination
├── examples/               # Example projects
├── docs/                   # Documentation
├── pyproject.toml          # Package metadata
└── README.md
```

## Development

### Setup

```bash
# Clone repository
git clone https://github.com/tmorgan181/lite-kits.git
cd lite-kits

# Install with dev dependencies
uv tool install -e ".[dev]"
```

### Building

```bash
# Build package
uv build

# Install locally
uv tool install dist/lite_kits-0.1.0-py3-none-any.whl
```

### Testing (TODO)

```bash
pytest
pytest --cov=src/lite_kits
```

## Roadmap

### ✅ Phase 1: Foundation (v0.1.0)
- [x] Package structure with constants and clean architecture
- [x] Kit-based modular architecture
- [x] Git-kit (/commit, /pr, /cleanup)
- [x] Project-kit (/orient)
- [x] Multiagent-kit (/sync, collaboration)
- [x] Cross-platform support (Bash + PowerShell)
- [x] Windows encoding fixes (ASCII-safe status indicators)
- [x] CLI with Kit Management and Package Management sections
- [x] Shell completion disabled (no profile modifications)
- [x] Proper pip/uv tool installation

### Phase 2: Polish & Publish (Next - v0.2.0)
- [x] Complete CLI rebrand (`install` → `add`, proper flags)
- [x] Fix installer kit mappings (sync in multiagent, cleanup in git)
- [ ] Add examples directory with sample projects
- [ ] PyPI publication
- [ ] Documentation improvements (architecture docs, guides)

### Phase 3: Expansion (Future - v0.3.0)
- [ ] Additional kits for other vanilla tools
- [ ] Template library expansion
- [ ] Test suite (pytest)
- [ ] CI/CD automation
- [ ] Plugin system for custom kits

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Related Projects

- [GitHub spec-kit](https://github.com/github/spec-kit) - Spec-driven development framework
- [Claude Code](https://claude.ai/code) - AI coding assistant
- [GitHub Copilot](https://github.com/features/copilot) - AI pair programmer

## Support

- **Issues**: [GitHub Issues](https://github.com/tmorgan181/lite-kits/issues)
- **Discussions**: [GitHub Discussions](https://github.com/tmorgan181/lite-kits/discussions)

## Acknowledgments

Built to enhance [GitHub Spec-Kit](https://github.com/github/spec-kit), a framework for spec-driven development with AI agents.

---

**Status**: Alpha (v0.1.0) - APIs may change

**Philosophy**: Enhance, don't replace. lite-kits adds features to vanilla spec-kit without forking or modifying core files.
