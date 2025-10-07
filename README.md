# spec-kit-multiagent

**Lightweight multi-agent coordination add-on for [GitHub spec-kit](https://github.com/github/spec-kit)**

Add multi-agent coordination capabilities to vanilla spec-kit projects without forking or replacing core files.

[![Version](https://img.shields.io/badge/version-0.1.0-blue.svg)](https://github.com/yourusername/spec-kit-multiagent-lite)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## What is this?

**spec-kit** is GitHub's framework for spec-driven development with AI agents. It provides workflows like `/specify` → `/plan` → `/tasks` → `/implement`.

**spec-kit-multiagent** is a pip-installable add-on that layers coordination features on top, enabling:

- 🤝 **Multiple AI agents** working together (Claude Code, GitHub Copilot, Cursor)
- 📋 **Coordination protocols** via collaboration directories
- 🔀 **Git worktrees** for parallel development
- 📝 **Session logging** and handoff documents
- 🏷️ **Agent attribution** in commits

## Key Features

### 🎯 The `/orient` Command

New slash command for agent orientation:
- Reads project documentation (constitution, copilot-instructions)
- Checks current git state
- Determines agent role (leader vs specialist)
- Provides concise context (~150 words)

### 📁 Collaboration Directories

Structure for multi-agent coordination:
```
specs/NNN-feature/collaboration/
├── active/          # Current work
│   ├── sessions/    # Work session logs
│   └── decisions/   # Handoffs, proposals
├── archive/         # Historical (YYYY-MM/)
└── results/         # Completed deliverables
```

### 📚 Memory Guides

- **PR Workflow Guide**: How AI agents create pull requests
- **Git Worktrees Protocol**: Parallel development with worktrees

### 🏷️ Agent Attribution

Track which AI model created what code:
```
feat: Add user authentication

via claude-sonnet-4.5 @ claude-code
```

## Installation

### Prerequisites

- Python 3.11+
- Existing spec-kit project (or create one first)
- At least one AI interface: Claude Code, GitHub Copilot, or Cursor

### Install via pip (Coming Soon)

```bash
pip install spec-kit-multiagent
```

### Install from source (Current)

```bash
# Clone repository
git clone https://github.com/yourusername/spec-kit-multiagent-lite.git
cd spec-kit-multiagent-lite

# Install in development mode
pip install -e .

# Or build and install
pip install build
python -m build
pip install dist/spec_kit_multiagent-0.1.0-py3-none-any.whl
```

## Quick Start

### 1. Install multiagent features to your spec-kit project

```bash
cd your-spec-kit-project
lite-kits install -Recommended -WhatIf  # Preview changes
lite-kits install -Recommended          # Install
```

**What gets installed**:
- `/orient` command (`.claude/commands/` or `.github/prompts/`)
- PR workflow guide (`.specify/memory/pr-workflow-guide.md`)
- Git worktrees protocol (`.specify/memory/git-worktrees-protocol.md`)

### 2. Run `/orient` in your AI assistant

```bash
# In Claude Code or GitHub Copilot
/orient
```

Agent will:
- Read project documentation
- Check git state
- Determine its role and model
- Summarize next actions

### 3. Start coordinating

Create a feature with collaboration:
```bash
# In your AI assistant
/specify Build a user authentication system
/plan
/tasks
/implement
```

Collaboration directories are automatically created for session logging.

## Usage

### CLI Commands

```bash
# Install multiagent features
lite-kits install -Recommended [--WhatIf]

# Validate installation
lite-kits validate

# Show project status
lite-kits status

# Remove multiagent features (TODO)
lite-kits remove -All

# Show version
lite-kits --version
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
   git commit -m "feat: Add auth API

   via claude-sonnet-4.5 @ claude-code"
   ```

5. **Periodic sync**: Pull each other's changes
   ```bash
   git pull origin 002-blog
   ```

6. **Integration**: Test together, create PR

See [examples/blog-with-auth](examples/blog-with-auth/) for complete example.

## Architecture

### Add-on Design (Not a Fork)

This package is an **add-on**, not a fork:
- ✅ Vanilla spec-kit stays vanilla
- ✅ Users get vanilla updates automatically
- ✅ Multiagent features can be added/removed independently
- ✅ No core file replacement

### What Gets Added

**New files**:
- `.claude/commands/orient.md` (Claude Code version)
- `.github/prompts/orient.prompt.md` (GitHub Copilot version)
- `.specify/memory/pr-workflow-guide.md`
- `.specify/memory/git-worktrees-protocol.md`

**New structure** (when creating features):
- `specs/NNN-feature/collaboration/` directories

**No modifications** to existing spec-kit files.

## Examples

See [examples/](examples/) directory:

- **minimal-todo-app**: Single-agent workflow (🚧 Coming Soon)
- **blog-with-auth**: Multi-agent with worktrees (🚧 Coming Soon)
- **templates/**: Reusable templates (🚧 Coming Soon)

## Development

### Setup

```bash
# Clone repository
git clone https://github.com/yourusername/spec-kit-multiagent-lite.git
cd spec-kit-multiagent-lite

# Install dependencies
pip install -e ".[dev]"
```

### Project Structure

```
spec-kit-multiagent-lite/
├── src/speckit_multiagent/
│   ├── __init__.py
│   ├── cli.py              # CLI commands
│   ├── installer.py        # Installation logic
│   └── templates/          # Files to install
│       ├── commands/       # /orient command
│       └── memory/         # PR guide, worktrees protocol
├── examples/               # Example projects
├── spec-kits/              # Reference vanilla configs
├── tests/                  # Unit tests (TODO)
├── pyproject.toml          # Package metadata
└── README.md
```

### Testing (TODO)

```bash
pytest
pytest --cov=src/speckit_multiagent
```

### Building

```bash
python -m build
```

## Roadmap

### ✅ Phase 1: Foundation (Current - v0.1.0)
- [x] Package structure
- [x] Basic CLI (`add`, `validate`, `status`)
- [x] `/orient` command template
- [x] Memory guides (PR workflow, git worktrees)
- [x] Documentation

### 🚧 Phase 2: Smart Features (Next - v0.2.0)
- [ ] Smart constitution merge (idempotent updates)
- [ ] Collaboration template creation
- [ ] Session management helpers
- [ ] Agent auto-detection
- [ ] Remove command implementation

### 📋 Phase 3: Examples & Polish (Future - v0.3.0)
- [ ] Complete minimal-todo-app example
- [ ] Complete blog-with-auth example
- [ ] Template library
- [ ] Test suite
- [ ] PyPI publication

## Contributing

Contributions welcome! See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

## License

MIT License - see [LICENSE](LICENSE) for details.

## Related Projects

- [GitHub spec-kit](https://github.com/github/spec-kit) - The vanilla framework
- [Claude Code](https://claude.ai/code) - AI coding assistant
- [GitHub Copilot](https://github.com/features/copilot) - AI pair programmer

## Documentation

- **[Quick Start](docs/QUICKSTART.md)** - 5-minute setup guide
- **[Examples](examples/)** - Working project examples
- **[Troubleshooting](docs/TROUBLESHOOTING.md)** - Common issues and solutions
- **[Contributing](CONTRIBUTING.md)** - How to contribute

## Support

- **Issues**: [GitHub Issues](https://github.com/yourusername/spec-kit-multiagent-lite/issues)
- **Discussions**: [GitHub Discussions](https://github.com/yourusername/spec-kit-multiagent-lite/discussions)

## Acknowledgments

Built on top of [GitHub spec-kit](https://github.com/github/spec-kit) by the GitHub Next team.

---

**Status**: Alpha (v0.1.0) - APIs may change

**Philosophy**: Lightweight coordination layer, not a framework replacement
