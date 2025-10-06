# Blog with Authentication Example

🚧 **Status**: Coming Soon

## Overview

Full-featured blog platform demonstrating advanced multi-agent coordination with git worktrees.

**Learning Goals**:
- Multi-agent collaboration (Claude Code + GitHub Copilot)
- Git worktrees for parallel development
- Backend/frontend split work
- Agent handoff documents
- PR workflow with attribution

## Tech Stack

- **Backend**: Node.js + Express + TypeScript
- **Frontend**: React + TypeScript + Vite
- **Database**: PostgreSQL
- **Testing**: Jest + React Testing Library
- **Agents**: Claude Code (backend) + GitHub Copilot CLI (frontend)

## Features

- User authentication (signup/login)
- Create/edit/delete blog posts
- Comment system
- User profiles
- Markdown support

## Multi-Agent Workflow

### Agents & Responsibilities

**Agent 1: Claude Code (Backend Lead)**
- API endpoint design
- Database schema
- Authentication logic
- Integration tests
- Architectural decisions

**Agent 2: GitHub Copilot CLI (Frontend Specialist)**
- React components
- UI/UX implementation
- Client-side state management
- Component tests
- Git operations

### Git Worktree Setup

```bash
# Agent 1: Backend worktree
git worktree add ../blog-backend 002-blog-platform
cd ../blog-backend
# Work on: src/api/, src/auth/, migrations/

# Agent 2: Frontend worktree
git worktree add ../blog-frontend 002-blog-platform
cd ../blog-frontend
# Work on: src/components/, src/hooks/, src/pages/
```

## Project Structure

```
blog-with-auth/
├── specs/
│   └── 002-blog-platform/
│       ├── spec.md
│       ├── plan.md
│       ├── tasks.md
│       ├── data-model.md
│       ├── contracts/
│       │   └── api.yaml
│       └── collaboration/
│           ├── active/
│           │   ├── sessions/
│           │   │   ├── 2025-10-06-claude-backend.md
│           │   │   └── 2025-10-06-copilot-frontend.md
│           │   ├── decisions/
│           │   │   ├── handoff-to-copilot.md
│           │   │   └── worktree-coordination.md
│           │   └── README.md
│           ├── archive/
│           └── results/
├── backend/
│   ├── src/
│   │   ├── api/
│   │   ├── auth/
│   │   └── database/
│   └── tests/
├── frontend/
│   ├── src/
│   │   ├── components/
│   │   ├── hooks/
│   │   └── pages/
│   └── tests/
├── .claude/
├── .github/
└── .specify/
```

## Workflow Walkthrough

### Phase 1: Specification (Claude Code)

```bash
/specify Create a blog platform with user authentication
```

Claude generates comprehensive spec including:
- User stories for both auth and blogging
- API endpoints
- Data models
- Success criteria

### Phase 2: Planning (Claude Code)

```bash
/plan
```

Creates implementation plan with:
- Backend architecture
- Frontend architecture
- Integration points
- Testing strategy
- **Split work** notation for multi-agent

### Phase 3: Coordination Setup (Claude Code)

Creates handoff document:

```markdown
# collaboration/active/decisions/agent-split.md

## Work Division

**Claude Code (Backend)**:
- API endpoints (Express routes)
- Database models (Prisma)
- Authentication middleware
- Backend tests

**Copilot CLI (Frontend)**:
- React components
- Auth flow UI
- Blog post editor
- Frontend tests

**Integration Points**:
- API contract: contracts/api.yaml
- Shared types: src/shared/types.ts
```

### Phase 4: Parallel Development

**Claude Code (Backend)**:
```bash
cd ../blog-backend
/tasks  # Generate backend tasks
/implement  # Build backend
git commit -m "feat: Add authentication API

via claude-sonnet-4.5 @ claude-code"
git push origin 002-blog-platform
```

**Copilot CLI (Frontend)**:
```bash
cd ../blog-frontend
/tasks  # Generate frontend tasks
/implement  # Build frontend
git commit -m "feat: Add login/signup UI

via gpt-4 @ github-copilot-cli"
git push origin 002-blog-platform
```

### Phase 5: Synchronization

Both agents periodically sync:

```bash
git pull origin 002-blog-platform
# Resolve any conflicts
# Continue work
```

### Phase 6: Integration Testing

One agent handles integration:

```bash
cd main-repo
git pull origin 002-blog-platform
# Run full integration tests
# Both backend and frontend together
```

## Session Logs

### Backend Session Example

```markdown
# collaboration/active/sessions/2025-10-06-claude-backend.md

## Backend Development Session

**Agent**: Claude Code (claude-sonnet-4.5)
**Worktree**: ../blog-backend
**Duration**: 3 hours

### Completed
- Express app setup
- Prisma schema design
- Authentication middleware (JWT)
- POST /auth/signup, POST /auth/login
- Integration tests (15/15 passing)

### Commits
- abc123: feat: Add Express app structure
- def456: feat: Add Prisma database schema
- ghi789: feat: Add JWT authentication

### Synchronized
- Pulled frontend changes at 14:00 (no conflicts)
- Pushed backend at 16:30

### Status
✅ Backend ready for frontend integration
```

### Frontend Session Example

```markdown
# collaboration/active/sessions/2025-10-06-copilot-frontend.md

## Frontend Development Session

**Agent**: GitHub Copilot CLI (gpt-4)
**Worktree**: ../blog-frontend
**Duration**: 2.5 hours

### Completed
- Vite + React setup
- Login/Signup forms
- Auth context provider
- Protected route wrapper
- Component tests (8/8 passing)

### Commits
- jkl012: feat: Add Vite + React setup
- mno345: feat: Add authentication UI
- pqr678: feat: Add protected routes

### Synchronized
- Pulled backend API updates at 15:00
- Updated API client to match contracts/api.yaml

### Status
✅ Ready for integration testing with backend
```

## Handoff Documents

See example handoff: [collaboration/active/decisions/handoff-to-copilot.md](specs/002-blog-platform/collaboration/active/decisions/handoff-to-copilot.md)

## Running the Example

TODO: Provide complete working code

```bash
# Backend
cd backend
npm install
npm run migrate
npm run dev

# Frontend (separate terminal)
cd frontend
npm install
npm run dev

# Integration tests
npm run test:integration
```

## Key Takeaways

1. **Worktrees enable parallel work**: Agents work simultaneously without conflicts
2. **Clear boundaries**: Define file territories upfront
3. **Contracts first**: API contracts (OpenAPI/GraphQL) prevent integration issues
4. **Regular sync**: Pull frequently to stay coordinated
5. **Session logs**: Document what was done, for handoff continuity

## Advanced Patterns Demonstrated

- Git worktree coordination
- Contract-driven development (API contracts)
- Agent role specialization (backend vs frontend)
- Handoff documents for context sharing
- Integration testing across agent work
- PR creation with multi-agent attribution

## Next Steps

After this example:
- Try implementing your own multi-agent feature
- Experiment with 3+ agents on complex projects
- Explore other coordination patterns
