# 🌈 LITE-KITS 🎒

[![PyPI version](https://img.shields.io/pypi/v/lite-kits.svg)](https://pypi.org/project/lite-kits/)
[![Python](https://img.shields.io/badge/python-3.11+-blue.svg)](https://www.python.org/downloads/)
[![uv](https://img.shields.io/endpoint?url=https://raw.githubusercontent.com/astral-sh/uv/main/assets/badge/v0.json)](https://github.com/astral-sh/uv)
[![Spec-Kit](https://img.shields.io/badge/spec--kit-compatible-purple.svg)](https://github.com/github/spec-kit)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**Lightweight enhancement kits for spec-driven development.**

<img width="750" height="450" alt="lite-kits banner in terminal" src="assets/banner.gif" />

## What is this?

**lite-kits** adds productivity-enhancing slash commands to [spec-kit](https://github.com/github/spec-kit) projects. Get smart git workflows (`/commit`, `/pr`, `/cleanup`), project orientation (`/orient`), code quality tools (`/review`, `/audit`, `/stats`), and optional multi-agent coordination.

It's an **add-on**, not a fork—your vanilla spec-kit stays vanilla, and you benefit from upstream updates automatically.

## Quick Start

### 1. Install lite-kits

```bash
# Recommended: Install with uv
uv tool install lite-kits

# Or with pip
pip install lite-kits
```

### 2. Add kits to your spec-kit project

```bash
cd your-spec-kit-project

# Add dev-kit (all solo development commands)
lite-kits add

# Check what was installed
lite-kits status
```

### 3. Use the commands

```bash
# In Claude Code or GitHub Copilot
/orient     # Get project context
/commit     # Smart commit with staging
/pr         # Create PR with auto-push
/review     # Review staged changes
/cleanup    # Clean up merged branches
/audit      # Security analysis
/stats      # Project metrics
```

That's it! See [GUIDE.md](docs/GUIDE.md) for detailed command documentation and examples.

## Features

**Dev-Kit** (solo development):
- `/orient` - Quick project orientation for AI agents
- `/commit` - Smart commits with staging proposals and conventional commits
- `/pr` - Pull request creation with auto-push and smart descriptions
- `/review` - Code review against best practices
- `/cleanup` - Safe merged branch cleanup
- `/audit` - Security analysis on dependencies and code patterns
- `/stats` - Project metrics and complexity analysis

**Multiagent-Kit** (optional, for multi-agent workflows):
- `/sync` - Multi-agent coordination status
- Collaboration directories and templates
- Memory guides (PR workflow, git worktrees protocol)

**CLI Features:**
- Beautiful terminal output with proper spacing
- Preview-first (see changes before applying)
- Smart auto-detection (agents and shells)
- File count summaries
- `help` command: `lite-kits help [COMMAND]`
- `--force` flag to skip confirmations

## Installation

### Prerequisites

lite-kits enhances GitHub spec-kit projects. You'll need:

1. **Python 3.11+** - [Download here](https://www.python.org/downloads/)
   - Automatically checked by pip/uv during installation

2. **Node.js & npm** - [Download here](https://nodejs.org/)
   - Required to install spec-kit (spec-kit is a Node.js package)

3. **spec-kit** - GitHub's spec-driven development framework (REQUIRED)
   ```bash
   npm install -g @github/spec-kit
   ```
   - lite-kits won't work without spec-kit initialized first
   - Creates `.claude/` or `.github/prompts/` directories where commands are installed

### Complete Installation Flow

```bash
# 1. Install spec-kit (if not already installed)
npm install -g @github/spec-kit

# 2. Create a spec-kit project (or use existing)
specify init my-project
cd my-project

# 3. Install lite-kits
uv tool install lite-kits     # Recommended: with uv
# OR
pip install lite-kits          # Alternative: with pip

# 4. Add enhancement kits to your project
lite-kits add    # Adds dev-kit (all commands)

# 5. Start using commands in your AI assistant
/orient                        # Get project context
/commit                        # Smart commit workflow
```

### Alternative Install Methods

**With pip:**
```bash
pip install lite-kits
```

**From source:**
```bash
git clone https://github.com/tmorgan181/lite-kits.git
cd lite-kits
uv build
uv tool install dist/lite_kits-*.whl
```

### AI Assistant Compatibility

lite-kits commands work with any AI assistant that supports slash commands:
- ✅ **GitHub Copilot** (VSCode extension or CLI) - Native GitHub integration
- ✅ **Claude Code** (VSCode extension)
- ✅ Any assistant that reads `.md` prompt files

No additional configuration required—commands are just markdown files that your AI assistant reads.

## CLI Commands

```bash
# Kit management
lite-kits add          # Add dev-kit
lite-kits add --kit dev              # Add specific kit
lite-kits add --kit multiagent       # Add multiagent-kit
lite-kits remove --all               # Remove all kits
lite-kits remove --kit dev --force   # Remove without confirmation

# Status and info
lite-kits status                     # Show installed kits
lite-kits validate                   # Verify installation
lite-kits info                       # Package information
lite-kits help [COMMAND]             # Show help

# Global options
lite-kits --version / -V             # Show version
lite-kits --banner                   # Show animated banner
lite-kits --quiet / -q               # Suppress output
lite-kits --verbose / -v             # Extra output
```

See [GUIDE.md](docs/GUIDE.md) for detailed documentation and examples.

## What's New in v0.2.0

**Major rewrite with focus on modularity and UX:**

- ✨ Manifest-driven architecture (zero hardcoded logic)
- 🔧 Modular installer (detector, validator, conflict_checker)
- 📦 Kit consolidation: project-kit + git-kit → **dev-kit**
- 🎨 Perfect terminal spacing and file count summaries
- 💬 `help` command with optional command argument
- ⚡ `--force` flag for remove command
- 🐛 Fixed all critical bugs (#1, #3, #4, #6, #7)

See [CHANGELOG.md](CHANGELOG.md) for full release notes.

## Documentation

- **[GUIDE.md](docs/GUIDE.md)** - Complete command reference, workflows, and examples
- **[CHANGELOG.md](CHANGELOG.md)** - Version history and migration notes
- **[CONTRIBUTING.md](CONTRIBUTING.md)** - How to contribute
- **[manifest-schema.md](docs/manifest-schema.md)** - Technical reference for kits.yaml

## Architecture

**Enhance, don't replace:**
- lite-kits is an add-on for vanilla spec-kit (not a fork)
- Only adds files, never modifies spec-kit core
- Get upstream spec-kit updates automatically
- Modular kits (add/remove as needed)

**Content-first structure:**
- `kits/{kit-name}/commands/{command}.{agent}.md`
- Easy to add new commands, agents, and shells
- Single manifest (kits.yaml) as source of truth

**Modular installer:**
- Auto-detect agents (Claude, Copilot) and shells (Bash, PowerShell)
- Preview-first operations with conflict checking
- Clean separation of concerns across focused modules

## Support & Contributing

- **Issues**: [GitHub Issues](https://github.com/tmorgan181/lite-kits/issues)
- **Discussions**: [GitHub Discussions](https://github.com/tmorgan181/lite-kits/discussions)
- **Contributing**: See [CONTRIBUTING.md](CONTRIBUTING.md)

## License

MIT License - see [LICENSE](LICENSE) for details.

## Acknowledgments

Built to enhance [GitHub Spec-Kit](https://github.com/github/spec-kit), a framework for spec-driven development with AI agents.

---

**Status**: Beta (v0.3.0) - Ready for production use

**Philosophy**: Enhance, don't replace. lite-kits adds features to vanilla spec-kit without forking or modifying core files.
