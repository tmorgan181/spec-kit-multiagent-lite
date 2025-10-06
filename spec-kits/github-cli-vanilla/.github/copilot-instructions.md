# Spec-Kit Multiagent Development Guidelines

**Project**: spec-kit-multiagent
**Last Updated**: 2025-01-06

## Technology Stack

### Core Technologies
- **Python 3.11+**: Package implementation, build tooling
- **uv**: Package manager and build tool (replaces pip, setuptools)
- **PowerShell**: Cross-platform scripting (setup, validation, sync)
- **Bash**: Alternative shell scripting for Linux/macOS users

### Dependencies/Extensions
- **spec-kit**: Upstream GitHub project (vanilla, not modified)
- **Markdown**: Documentation format (specs, plans, tasks)
- **Git**: Version control with worktree support for parallel development

### Required Features
- **Python packaging**: PEP 420 source layout, entry points
- **Cross-platform**: Windows (PowerShell), Linux/macOS (Bash)
- **Git worktrees**: Parallel development protocol

## Project Structure

```
spec-kit-multiagent/
├── src/speckit_multiagent/     # Python package (FUTURE - not yet implemented)
│   ├── __init__.py             # Package exports
│   ├── cli.py                  # Entry point: speckit-ma command
│   ├── installer.py            # Installation logic
│   └── templates/              # Files to install in target projects
├── examples/                   # Demo projects and templates
│   ├── demo-specs/             # 3 progressive demos (todo, blog, ecommerce)
│   └── templates/              # minimal-spec, full-feature templates
├── specs/                      # This project's feature specifications
│   └── NNN-feature-name/       # Individual features
│       ├── spec.md             # Feature specification
│       ├── plan.md             # Implementation plan
│       ├── tasks.md            # Task breakdown
│       └── collaboration/      # Multi-agent coordination
│           ├── active/         # Current work (sessions, decisions)
│           ├── archive/        # Historical (by YYYY-MM)
│           └── results/        # Completed (validation, artifacts)
├── .claude/commands/           # Claude Code slash commands
├── .github/prompts/            # GitHub Copilot slash commands (synced)
├── .specify/
│   ├── memory/                 # Constitution, PR workflow, git protocols
│   ├── templates/              # Spec, plan, tasks templates
│   └── scripts/powershell/     # Setup, validation, sync scripts
├── docs/                       # Architecture, implementation guides
├── CLAUDE.md                   # AI agent instructions
├── README.md                   # Project overview
└── INSTALL.md                  # Installation instructions
```

## Development Commands

### Setup
```bash
# Install uv (Python package manager)
curl -LsSf https://astral.sh/uv/install.sh | sh

# On Windows:
powershell -ExecutionPolicy ByPass -c "irm https://astral.sh/uv/install.ps1 | iex"
```

### Local Development (FUTURE - when Python package exists)
```bash
# Install from source (editable mode)
uv tool install -e .

# Install from built package
uv tool install dist/spec_kit_multiagent-0.1.0-py3-none-any.whl

# Uninstall
uv tool uninstall spec-kit-multiagent
```

### Testing Installation (FUTURE)
```bash
# Create test vanilla spec-kit project
cd /tmp
specify init test-project
cd test-project

# Test the add command (dry run)
speckit-ma add --here --dry-run

# Actually install multiagent features
speckit-ma add --here

# Verify installation
/orient  # Should work if slash commands configured
```

### PowerShell Scripts (Current)
```powershell
# Validate collaboration structure in specs
pwsh .specify/scripts/powershell/validate-collaboration.ps1

# Setup collaboration directories for new feature
pwsh .specify/scripts/powershell/setup-collaboration.ps1 -FeatureId "007-feature-name"

# Sync commands between .claude/ and .github/prompts/
pwsh .specify/scripts/powershell/sync-commands.ps1
```

### Building Package (FUTURE)
```bash
# Build distribution
uv build

# Check package contents
tar -tzf dist/spec_kit_multiagent-0.1.0.tar.gz
```

## Code Style Guidelines

### Python (FUTURE)
- PEP 8 style (use `ruff check .` for linting)
- Type hints required for public APIs
- Docstrings for all public functions (Google style)
- Source layout: `src/speckit_multiagent/` (PEP 420)

### PowerShell
- Verb-Noun naming convention (`Get-FeatureStatus`, `Set-CollaborationDirectory`)
- Approved verbs only (`Get-Verb` for list)
- Comment-based help for all scripts
- `-WhatIf` and `-Confirm` support for destructive operations

### Markdown
- One sentence per line (improves git diffs)
- ATX headers (`#` not `===`)
- Fenced code blocks with language tags
- Links at bottom of section (reference style for readability)

### General Principles
- **Agent-agnostic**: Works across Claude Code, Copilot CLI, Cursor
- **Cross-platform**: PowerShell + Bash where possible
- **Reversible**: Users can uninstall and return to vanilla spec-kit
- **Documented**: CLAUDE.md, copilot-instructions.md, examples

## Multi-Agent Collaboration

When working with other AI agents or human collaborators:

### Coordination Protocol
**Location**: Use feature-specific collaboration directories:
- `specs/[feature]/collaboration/active/` - Current work
  - `sessions/` - Work session logs (`YYYY-MM-DD-agent-description.md`)
  - `decisions/` - Handoffs, proposals, decisions
- `specs/[feature]/collaboration/archive/` - Historical (organized by `YYYY-MM/`)
- `specs/[feature]/collaboration/results/` - Completed deliverables
  - `validation/` - Test results, validation reports
  - `artifacts/` - Final outputs, summaries

**Contents**:
- Handoff documents (task delegation between agents)
- Session logs (what was done, issues encountered)
- Decision records (architectural choices, resolved questions)
- Checkpoint documents (progress snapshots)

### Agent Roles
**Claude Code (Primary/Leader)**:
- Higher token limits and context retention
- Handle most development work
- Make architectural decisions
- Capable of all git operations
- Delegate to Copilot when beneficial

**GitHub Copilot CLI (Specialist/Git Expert)**:
- Handle delegated specific tasks
- **Preferred for git operations** (branches, worktrees, complex workflows)
- Cross-platform testing (PowerShell perspective)
- Wait for delegation from Claude Code for development work

**Both agents**: Commit your own work, push your changes, capable of full git workflows.

### Shared File Etiquette
When multiple agents edit the same files:

**Before Editing**:
- Pull latest changes from shared branch
- Review recent commits to understand others' work
- Check collaboration docs for territory assignments
- Run `/orient` if unclear about current state

**During Work**:
- Commit frequently with descriptive messages
- Use targeted commits for specific sections
- Respect assigned file territories
- Document significant decisions in `collaboration/active/decisions/`

**After Editing**:
- Pull before push to detect conflicts early
- Test changes locally before pushing
- Update collaboration docs with status
- Create checkpoint if significant milestone reached

### Git Workflow
**Reference**: See `.specify/memory/git-worktrees-protocol.md` for parallel development strategies using Git worktrees.

**Key Principles**:
- Feature branches for all work (`NNN-feature-name`)
- Clear commit messages with task identifiers
- Regular synchronization between agents
- Documented work division and territories

**Commit Attribution for AI Agents**:
When AI agents commit code, include model and interface info:
```
<commit message>

via <model> @ <interface>

Examples:
- via claude-sonnet-4.5 @ claude-code
- via gpt-4 @ github-copilot-cli
- via claude-opus-4 @ cursor
```

The CI workflow tracks agent/model attribution for transparency.

### Communication Channels
- **Collaboration Documents**: Primary written communication (`collaboration/active/`)
- **Commit Messages**: Technical change descriptions
- **Project Issues**: For questions, blockers, or decisions requiring human input
- **Checkpoint Documents**: End-of-session progress summaries

## Project-Specific Conventions

### Feature Numbering
- 3-digit zero-padded (`001-todo-app`, `007-demo-example-projects`)
- Descriptive kebab-case names
- Stored in `specs/NNN-feature-name/`

### Collaboration Directory Structure
**3-folder system** (active, archive, results):
- `active/` - Current work in progress
  - `sessions/` - Session logs
  - `decisions/` - Handoffs, proposals
  - `README.md` - Current status
- `archive/` - Historical work (organized by `YYYY-MM/`)
- `results/` - Completed deliverables
  - `validation/` - Test results
  - `artifacts/` - Final outputs

### Slash Command Sync
- Commands live in both `.claude/commands/` and `.github/prompts/`
- Use `sync-commands.ps1` to keep them in sync
- `.prompt.md` extension for Copilot, `.md` for Claude
- Frontmatter required for Copilot prompts

### Template Types
- **minimal-spec**: Simple features (spec + plan + tasks)
- **full-feature**: Complex features (+ data-model + contracts + collaboration)

## Recent Feature Implementations

Track completed features for context:

- **007-demo-example-projects**: Demo specs (todo, blog, ecommerce) + templates (minimal, full-feature) + working 001-todo-app
- **P2-collaboration-scaffolding**: 3-folder structure, setup/validation scripts, `/collaborate` command
- **P1-installer-validator**: Installation scripts, validation protocols
- **P0-foundation**: Initial project structure, constitution, core documentation

**Purpose**: Helps agents understand project evolution and existing patterns.

## Agent-Specific Notes

### For AI Assistants
- **Add-on pattern**: Never replace vanilla spec-kit files, only add coordination features
- **Cross-agent compatibility**: Your work will be used by Claude Code, Copilot CLI, and Cursor
- **Orientation protocol**: Run `/orient` before starting work (see `.github/prompts/orient.prompt.md`)
- **Token efficiency**: Be concise in orientation, verbose in documentation
- **Constitution compliance**: Read `.specify/memory/constitution.md` for core principles

### For Human Developers
- **Installation**: See `INSTALL.md` for developer setup
- **Architecture**: See `docs/ARCHITECTURE.md` for add-on design rationale
- **Implementation**: See `docs/IMPLEMENTATION-GUIDE.md` for step-by-step build instructions
- **Validation**: See `docs/HUMAN-VALIDATION-GUIDE.md` for manual testing protocols

## Orientation Protocol

**Agent Roles**:
- **Claude Code (Bash)**: Primary developer, architectural decisions, most work
- **Copilot (PowerShell)**: Delegated tasks, git operations preferred, specialist

**Before starting work**: Run `/orient` or manually review:
1. This file (copilot-instructions.md) - PRIMARY SOURCE
2. `.specify/memory/constitution.md` - project philosophy
3. Current git state - branch, recent work
4. Existing specs (if any)
5. Your role (Claude = leader, Copilot = specialist)

**Token efficiency required**:
- Output essentials only (~150-200 words)
- Combine steps where possible
- Brief summaries not quotes
- Direct answers no preambles
- State conclusions first, details after

**Development voice**:
- Precise, brief, direct, practical, efficient
- No verbosity, apologies, hedging, or ceremony
- Ask clarifying questions before lengthy work
- Optimize for minimal cognitive load

**Git operations**:
- Both agents: Commit and push your own work
- Copilot preferred: Branch creation, worktrees, complex git workflows
- Claude Code: Architectural decisions, code review, final approval

**See**: `.github/prompts/orient.prompt.md` for detailed protocol.

## Manual Additions

<!-- MANUAL ADDITIONS START -->
<!--
Add runtime notes, preferences, or shortcuts here.
This section is preserved across automated updates.
-->

<!-- MANUAL ADDITIONS END -->

---

## Current Status

**Phase**: Foundation (v0.1.0 in development)
**Branch**: `007-demo-example-projects` (merged to `main` via PR #1)
**Progress**: 40% complete on Feature 007
**Next**: Populate collaboration examples, update PowerShell scripts, implement 002/003 demos

**See**:
- `specs/007-demo-example-projects/collaboration/active/README.md` for current status
- `specs/007-demo-example-projects/collaboration/active/TODO.md` for remaining tasks
- `specs/007-demo-example-projects/collaboration/active/sessions/2025-10-05-checkpoint-11pm.md` for detailed checkpoint

---

**This file helps AI agents understand how to work on this project effectively.**
