# Examples

This directory contains example projects demonstrating spec-kit-multiagent usage.

## Available Examples

### 1. minimal-todo-app
**Status**: 🚧 Coming Soon

Simple todo application demonstrating:
- Basic /specify → /plan → /tasks → /implement workflow
- Single-agent coordination
- Collaboration directory structure
- Session logging

**Stack**: Python + FastAPI + SQLite

### 2. blog-with-auth
**Status**: 🚧 Coming Soon

Blog platform with authentication demonstrating:
- Multi-agent coordination (Claude Code + Copilot)
- Git worktrees for parallel development
- PR workflow with agent attribution
- Backend/frontend split work

**Stack**: Node.js + Express + React + PostgreSQL

### 3. templates/
**Status**: 🚧 Coming Soon

Reusable templates:
- `minimal-spec/` - Quick start template
- `full-feature/` - Complete feature with collaboration structure
- `collaboration-only/` - Just collaboration directories

## Using Examples

### Option 1: Start from Example

```bash
# Copy example to new project
cp -r examples/minimal-todo-app my-project
cd my-project

# Install spec-kit (if not already installed)
npm install -g @github/spec-kit

# Install multiagent features
lite-kits install -Recommended
```

### Option 2: Reference for Learning

Browse examples to understand:
- How to structure collaboration directories
- Session log formatting
- Agent attribution in commits
- Handoff document patterns

## Example Structure

Each example includes:
```
example-name/
├── specs/
│   └── 001-initial-feature/
│       ├── spec.md
│       ├── plan.md
│       ├── tasks.md
│       └── collaboration/
│           ├── active/
│           │   ├── sessions/
│           │   └── decisions/
│           ├── archive/
│           └── results/
├── src/
├── tests/
├── .claude/
│   └── commands/
│       └── orient.md
├── .github/
│   └── prompts/
│       └── orient.prompt.md
└── .specify/
    └── memory/
        ├── constitution.md
        ├── pr-workflow-guide.md
        └── git-worktrees-protocol.md
```

## Contributing Examples

Have a good multiagent workflow example? Contribute it!

Requirements:
- Working code (tests passing)
- Complete spec + plan + tasks
- Session logs demonstrating coordination
- README explaining workflow

See [CONTRIBUTING.md](../CONTRIBUTING.md) for guidelines.

## TODO: Examples to Add

- [ ] Minimal todo app (single agent)
- [ ] Blog with auth (multi-agent, worktrees)
- [ ] E-commerce platform (complex multi-agent)
- [ ] CLI tool (simple spec-kit workflow)
- [ ] REST API (contract-driven development)
- [ ] Template: minimal-spec
- [ ] Template: full-feature
- [ ] Template: collaboration-only
