# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Overview

**lite-kits** is a pip-installable collection of lightweight enhancement kits for vanilla dev tools. This is an **add-on** framework, not a fork—it works alongside vanilla tools (like [GitHub spec-kit](https://github.com/github/spec-kit)) without replacing any core files.

**Current Status**: Pre-release (v0.1.0 in development)

**Core Philosophy**: From the Atrium Grounds Constitution (`.specify/memory/constitution.md`):
- **Progressive Disclosure**: Build trust gradually through tiered access
- **Multi-Interface Access**: Serve both human users and AI systems
- **Service Independence**: Clean boundaries enable parallel multi-agent development
- **Language Standards**: Grounded, professional, clear—avoid mystical or overly ceremonious language
- **Ethical Boundaries**: Manual curation for all private→public data flows

## Development Commands

### Package Installation

```bash
# Install from source (editable mode for development)
uv tool install -e .

# Install from built package
uv tool install dist/lite_kits-0.1.0-py3-none-any.whl

# Uninstall
uv tool uninstall lite-kits
```

### Testing Installation

```bash
# Create test vanilla spec-kit project
cd /tmp
specify init test-project
cd test-project

# Test the add command (dry run)
lite-kits install -WhatIf

# Actually install multiagent features
lite-kits install -Recommended

# Verify installation
/orient  # Should work if slash commands are configured
```

### Package Building

```bash
# Build distribution
uv build

# Check package contents
tar -tzf dist/spec_kit_multiagent-0.1.0.tar.gz
```

### PowerShell Scripts

```bash
# Validate collaboration structure in specs
pwsh .specify/scripts/powershell/validate-collaboration.ps1

# Setup collaboration directories for new feature
pwsh .specify/scripts/powershell/setup-collaboration.ps1 -FeatureId "001-feature-name"

# Sync commands between .claude/ and .github/prompts/
pwsh .specify/scripts/powershell/sync-commands.ps1
```

## Architecture

### Add-on Design Pattern

This project follows an **add-on architecture** (not a fork):
- **Vanilla spec-kit** provides core workflow: `/specify` → `/plan` → `/tasks` → `/implement`
- **This add-on** layers on coordination features: `/orient`, collaboration directories, git workflow guides
- Users get vanilla updates automatically
- Multiagent features can be added/removed independently

See `docs/ARCHITECTURE.md` for the full rationale.

### What Gets Added

When `lite-kits install` runs:

**New Files**:
- `.claude/commands/orient.md` - Claude Code version of orient command
- `.github/prompts/orient.prompt.md` - GitHub Copilot version
- `.specify/memory/pr-workflow-guide.md` - AI agent PR workflow
- `.specify/memory/git-worktrees-protocol.md` - Parallel development guide
- `.specify/scripts/powershell/validate-collaboration.ps1` - Validation script

**Enhanced Files** (multiagent sections appended):
- `.specify/memory/constitution.md` - Agent roles, orientation protocol
- `.github/copilot-instructions.md` - Coordination protocols

**Future Specs** get collaboration structure:
```
specs/NNN-feature-name/
└── collaboration/
    ├── README.md
    ├── planning/      # Pre-implementation planning
    ├── sessions/      # Work session logs
    ├── reviews/       # Code/spec reviews
    ├── results/       # Completed deliverables
    ├── proposals/     # Feature/change proposals
    ├── status/        # Progress tracking
    └── decisions/     # Technical decisions
```

### Package Structure

```
src/lite_kits/
├── __init__.py          # Package exports
├── cli.py               # Entry point: lite-kits command
├── installer.py         # Installation logic
└── kits/                # Enhancement kits
    ├── git/             # Git workflow commands (/commit, /pr, /cleanup)
    ├── project/         # Project commands (/orient)
    └── multiagent/      # Multi-agent tools (/sync, collaboration)
```

**Current Status**: Package is functional with git-kit, project-kit, and multiagent-kit fully implemented.

## Multi-Agent Workflow

### Slash Commands

These are available in `.claude/commands/` and `.github/prompts/`:
- `/orient` - Agent orientation protocol (NEW from this add-on)
- `/analyze` - Analyze existing code
- `/clarify` - Request clarifications
- `/specify` - Create feature spec
- `/plan` - Create implementation plan
- `/implement` - Execute implementation
- `/tasks` - Break down into tasks
- `/collaborate` - Multi-agent coordination guidance

### Orientation Protocol (`/orient`)

When starting work:
1. Run `/orient` to get project-specific context
2. Review `.specify/memory/constitution.md` for core principles
3. Check `specs/NNN-feature/collaboration/` for current work
4. Review recent git commits for context

### Collaboration Directories

Each feature spec has a `collaboration/` directory for multi-agent coordination:
- **planning/**: Pre-implementation planning documents
- **sessions/**: Logs from individual work sessions
- **reviews/**: Code reviews, spec reviews, validation results
- **results/**: Completed deliverables, summaries
- **proposals/**: Feature proposals, architecture decisions
- **status/**: Progress tracking, handoff documents
- **decisions/**: Technical decisions and rationale

Use these to coordinate work across multiple AI agents or between human developers and AI assistants.

### Git Commit Attribution

When AI agents commit code, include model and interface info:
```
<commit message>

via <model> @ <interface>

Examples:
- via claude-sonnet-4.5 @ claude-code
- via gpt-4 @ github-copilot
```

CI workflow tracks agent/model attribution for transparency.

## Implementation Status

### Current Phase: Foundation (Week 1 of 3-week timeline)

**Completed**:
- ✅ Project structure and documentation
- ✅ Slash command templates
- ✅ Memory documents (PR workflow, git protocol)
- ✅ Collaboration directory templates
- ✅ PowerShell validation script

**In Progress** (See `docs/IMPLEMENTATION-GUIDE.md` Phase 2-4):
- ⏳ Python package structure (`pyproject.toml`, `__init__.py`)
- ⏳ CLI implementation (`cli.py`)
- ⏳ Installer logic (`installer.py`)
- ⏳ Smart merge for constitution/copilot-instructions

**Not Started**:
- ❌ Tests (`tests/test_installer.py`)
- ❌ PyPI publication
- ❌ Examples directory

### Building and Publishing

To build and test the package:
1. **Build**: `uv build` creates wheel and source dist
2. **Test locally**: `uv tool install dist/lite_kits-0.1.0-py3-none-any.whl`
3. **Test commands**: `lite-kits --help`, `lite-kits status`
4. **Publish** (when ready): `uv publish`

See `README.md` for full installation and usage instructions.

## Language & Style Guidelines

From the constitution (Principle I):

**Use precise technical terms**:
- ✅ "AI systems," "LLMs," "machine learning"
- ✅ "Protected," "private," "ethical"

**Avoid**:
- ❌ Religious/mystical language ("sacred," "divine," "blessed")
- ❌ Undefined jargon without clear technical meaning
- ❌ Overly ceremonious or dramatic tone

**Style**:
- Brief over verbose
- Specific over general
- Professional, not pompous
- Playful metaphors okay (gardens, grounds) but stay grounded

## Common Patterns

### Working with Specs

```bash
# Create new feature spec (vanilla spec-kit)
specify init 007-my-feature

# Add collaboration structure (if multiagent is installed)
pwsh .specify/scripts/powershell/setup-collaboration.ps1 -FeatureId "007-my-feature"

# Validate collaboration structure
pwsh .specify/scripts/powershell/validate-collaboration.ps1
```

### Package Development Workflow

```bash
# After making changes to src/
uv tool install -e . --force-reinstall

# Test on a vanilla project
cd /tmp/test-project
lite-kits install -WhatIf
```

### Updating Slash Commands

```bash
# Edit commands in .github/prompts/
# Then sync to .claude/commands/
pwsh .specify/scripts/powershell/sync-commands.ps1
```

## Important Constraints

1. **No vanilla file replacement**: This add-on NEVER replaces vanilla spec-kit files
2. **Manual curation**: All private→public data flows require explicit approval
3. **Service independence**: Each service owns its database, no sharing
4. **Progressive disclosure**: Design for strangers first, build trust gradually
5. **Multi-interface**: All services must work for both humans and AI systems

## Related Documentation

- **README.md**: Project overview and quick start
- **INSTALL.md**: Installation instructions for users and developers
- **docs/ARCHITECTURE.md**: Why add-on (not fork) and technical decisions
- **docs/IMPLEMENTATION-GUIDE.md**: Step-by-step build instructions
- **.specify/memory/constitution.md**: Core principles (Atrium Grounds Constitution v1.3.1)
- **.specify/memory/pr-workflow-guide.md**: AI agent pull request workflow
- **.specify/memory/git-worktrees-protocol.md**: Git worktrees for parallel development

## Current Branch: dev/minimal-kit-mod

**Uncommitted changes**:
- Modified: `INSTALL.md`, `README.md`
- Deleted: `VERSION`, `docs/VISION-AND-PLAN.md`
- New: `AGENT-COMPATIBILITY.md`, `docs/ARCHITECTURE.md`, `docs/HUMAN-VALIDATION-GUIDE.md`, `docs/IMPLEMENTATION-GUIDE.md`, `docs/README.md`, `examples/`, `specs/`

**Recent commits**:
- Add multi-agent notes to specify/plan/implement prompts
- P2 collaboration scaffolding (script, templates, /collaborate prompt, CI workflow)
- Add Copilot reviewer refinements
- P1 installer and validator scripts
- P0 foundation consolidation (v0.1.0)
