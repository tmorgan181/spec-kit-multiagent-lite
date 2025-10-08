# lite-kits

**Lightweight enhancement kits for vanilla dev tools**

Add modular enhancement kits to vanilla projects (spec-kit, etc.) without forking or replacing core files.

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/tmorgan181/lite-kits)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What is this?

**lite-kits** is a collection of lightweight, modular enhancement kits that add useful features to vanilla development tools without replacing them.

Currently supports:
- **spec-kit** - GitHub's framework for spec-driven development with AI agents

Available kits:
- 🎯 **project-kit** - Project orientation and context (`/orient` command)
- 🔧 **git-kit** - Smart git workflows (`/commit`, `/pr`, `/cleanup`)
- 🤝 **multiagent-kit** - Multi-agent coordination (`/sync`, collaboration directories)

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

- Python 3.11+
- Existing spec-kit project (or create one first)
- At least one AI interface: Claude Code, GitHub Copilot, or Cursor

### Install via pip

```bash
pip install lite-kits
```

### Install from source

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

### 1. Install kits to your spec-kit project

```bash
cd your-spec-kit-project
lite-kits install -Recommended -WhatIf  # Preview changes
lite-kits install -Recommended          # Install
```

**What gets installed**:
- Git workflow commands (`/commit`, `/pr`, `/cleanup`)
- Project orientation command (`/orient`)
- Multi-agent coordination tools (`/sync`, collaboration structure)
- Memory guides (PR workflow, git worktrees protocol)

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

```bash
# Install kits
lite-kits install -Recommended [--WhatIf]

# Validate installation
lite-kits validate

# Show project status
lite-kits status

# Remove kits (TODO)
lite-kits remove -All

# Show version
lite-kits --version
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

This package is an **add-on**, not a fork:
- [OK] Vanilla tools stay vanilla
- [OK] Users get vanilla updates automatically
- [OK] Kits can be added/removed independently
- [OK] No core file replacement

### What Gets Added

**New files** (kit commands):
- `.claude/commands/*.md` (Claude Code versions)
- `.github/prompts/*.prompt.md` (GitHub Copilot versions)

**New files** (memory guides):
- `.specify/memory/pr-workflow-guide.md`
- `.specify/memory/git-worktrees-protocol.md`

**New structure** (when creating features):
- `specs/NNN-feature/collaboration/` directories

**No modifications** to existing vanilla files.

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

### [OK] Phase 1: Foundation (Current - v0.1.0)
- [x] Package structure
- [x] Kit-based architecture
- [x] Git-kit (/commit, /pr, /cleanup)
- [x] Project-kit (/orient)
- [x] Multiagent-kit (/sync, collaboration)
- [x] Cross-platform support (Bash + PowerShell)

### Phase 2: Polish & Publish (Next - v0.2.0)
- [ ] Fix Windows encoding issues
- [ ] Complete documentation rebrand
- [ ] Add examples
- [ ] PyPI publication
- [ ] Remove command implementation

### Phase 3: Expansion (Future - v0.3.0)
- [ ] Additional kits for other vanilla tools
- [ ] Template library
- [ ] Test suite
- [ ] CI/CD automation

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

Built to enhance [GitHub spec-kit](https://github.com/github/spec-kit) and other vanilla dev tools.

---

**Status**: Alpha (v0.1.0) - APIs may change

**Philosophy**: Lightweight enhancement kits, not framework replacements
