# Minimal Todo App Example

🚧 **Status**: Coming Soon

## Overview

Simple todo application demonstrating basic spec-kit-multiagent workflow with a single AI agent.

**Learning Goals**:
- Understand /specify → /plan → /tasks → /implement flow
- See collaboration directory structure in action
- Learn session logging best practices
- Practice agent attribution in commits

## Tech Stack

- **Backend**: Python 3.11+ with FastAPI
- **Database**: SQLite
- **Testing**: pytest
- **Agent**: Claude Code (claude-sonnet-4.5)

## Features

- Create/read/update/delete todos
- Mark todos as complete
- Filter by status (all/active/completed)
- Simple REST API

## Project Structure

```
minimal-todo-app/
├── specs/
│   └── 001-todo-crud/
│       ├── spec.md              # Feature specification
│       ├── plan.md              # Implementation plan
│       ├── tasks.md             # Task breakdown
│       └── collaboration/
│           ├── active/
│           │   └── sessions/
│           │       └── 2025-10-06-claude-initial.md
│           └── results/
│               └── artifacts/
│                   └── completion-summary.md
├── src/
│   ├── main.py                  # FastAPI app
│   ├── models.py                # Pydantic models
│   └── database.py              # SQLite setup
├── tests/
│   ├── test_api.py
│   └── test_models.py
├── .claude/
│   └── commands/
│       └── orient.md            # Agent orientation
├── .specify/
│   ├── memory/
│   │   ├── constitution.md
│   │   ├── pr-workflow-guide.md
│   │   └── git-worktrees-protocol.md
│   └── templates/
│       └── spec-template.md
├── requirements.txt
└── README.md
```

## Workflow Walkthrough

### 1. Initial Setup

```bash
# Install spec-kit
npm install -g @github/spec-kit

# Install multiagent add-on
pip install spec-kit-multiagent
lite-kits install -Recommended

# Run /orient in Claude Code
# Agent reads constitution, checks git state, confirms ready
```

### 2. Create Specification

```bash
# In Claude Code:
/specify Create a simple todo CRUD API with FastAPI
```

Creates `specs/001-todo-crud/spec.md` with:
- User stories
- API endpoints
- Data model
- Success criteria

### 3. Create Implementation Plan

```bash
/plan
```

Generates `specs/001-todo-crud/plan.md` with:
- Technical approach
- File structure
- Dependencies
- Test strategy

### 4. Break Down Tasks

```bash
/tasks
```

Creates `specs/001-todo-crud/tasks.md` with:
- Granular implementation tasks
- Dependencies between tasks
- Parallel execution opportunities

### 5. Implement

```bash
/implement
```

Agent works through tasks, creating:
- Session logs in `collaboration/active/sessions/`
- Code files in `src/`
- Tests in `tests/`
- Commits with attribution

### 6. Session Example

See [collaboration/active/sessions/2025-10-06-claude-initial.md](specs/001-todo-crud/collaboration/active/sessions/2025-10-06-claude-initial.md) for example session log.

## Agent Attribution

All commits include attribution:

```
feat: Add Todo model and CRUD operations

Implements Pydantic models and SQLite operations
for todo items.

via claude-sonnet-4.5 @ claude-code
```

## Running the Example

TODO: Provide complete working code

```bash
# Install dependencies
pip install -r requirements.txt

# Run tests
pytest

# Start server
uvicorn src.main:app --reload

# Test API
curl http://localhost:8000/todos
```

## Key Takeaways

1. **Collaboration directory**: Even single-agent projects benefit from session logging
2. **Agent attribution**: All AI commits include model and interface info
3. **Structured workflow**: /specify → /plan → /tasks → /implement keeps work organized
4. **Incremental**: Can add multiagent features to existing spec-kit projects

## Next Steps

After understanding this example:
- Try [blog-with-auth](../blog-with-auth/) for multi-agent coordination
- Explore git worktrees for parallel development
- Practice handoff documents between agents
