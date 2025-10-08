# Collaboration Directory Structure

This directory is created automatically when multiagent-kit is installed and you create a new feature with `/specify`.

## Purpose

Coordinate work between multiple AI agents (Claude Code, GitHub Copilot, etc.) on the same feature.

## Structure

```
specs/<feature-number>-<feature-name>/
└── collaboration/
    ├── active/              # Current work in progress
    │   ├── sessions/        # Individual agent work sessions
    │   ├── decisions/       # Coordination decisions and handoffs
    │   └── README.md        # Quick reference (this file copied here)
    │
    ├── archive/             # Completed sessions and decisions
    │   ├── sessions/
    │   └── decisions/
    │
    └── results/             # Outcomes and artifacts
        ├── validation/      # Test results, reviews
        └── artifacts/       # Generated files, diagrams, etc.
```

## Workflows

### Solo Agent Work

If only one agent is working:
1. Create session log in `active/sessions/`
2. Document decisions in `active/decisions/`
3. When feature complete, archive to `archive/`

### Multi-Agent Coordination

When multiple agents collaborate:

1. **Starting Work**
   - Run `/orient` to check for pending handoffs
   - Create session log: `active/sessions/YYYY-MM-DD-<agent-name>.md`
   - Review recent sessions from other agents

2. **Making Decisions**
   - Document in `active/decisions/<decision-name>.md`
   - Include: what was decided, why, by whom
   - Tag with agent attribution

3. **Handoff to Another Agent**
   - Create: `active/decisions/handoff-to-<agent>.md`
   - Include: context, what's done, what's needed
   - Other agent will see it in `/orient` output

4. **Accepting Handoff**
   - Read the handoff document
   - Create your session log
   - Move handoff to `archive/decisions/` when acknowledged

5. **Completing Feature**
   - Move all active sessions to `archive/sessions/`
   - Move decisions to `archive/decisions/`
   - Save artifacts in `results/artifacts/`

## File Naming Conventions

### Sessions

```
active/sessions/YYYY-MM-DD-<agent-name>.md
active/sessions/YYYY-MM-DD-<agent-name>-<description>.md

Examples:
active/sessions/2025-10-06-claude-code.md
active/sessions/2025-10-06-copilot-frontend-work.md
```

### Decisions

```
active/decisions/<decision-type>-<brief-name>.md

Examples:
active/decisions/handoff-to-copilot.md
active/decisions/architecture-database-choice.md
active/decisions/worktree-territory-split.md
```

### Artifacts

```
results/artifacts/<type>-<name>.<ext>

Examples:
results/artifacts/diagram-auth-flow.svg
results/artifacts/benchmark-api-performance.csv
```

## Template Usage

When creating documents, use the templates:
- Session log: Copy from `../../templates/session-log.md`
- Handoff: Copy from `../../templates/handoff.md`
- Decision: Copy from `../../templates/decision.md`

## Integration with Git

- Session logs and decisions are **committed to git**
- They become part of the feature's history
- Future agents can review them to understand context
- Helps with knowledge transfer and onboarding

## Best Practices

1. **Write for the next agent**: Assume someone else will read your session logs
2. **Link to commits**: Reference git commits in session logs
3. **Keep current**: Move old sessions to archive/ regularly
4. **Be specific**: "Added auth" → "Implemented JWT token validation in auth middleware"
5. **Update handoffs**: If you discover something while working, update the handoff
6. **Time-stamp everything**: Helps understand sequence of events

## Quick Commands

```bash
# Create session log
touch active/sessions/$(date +%Y-%m-%d)-claude-code.md

# Create handoff
cat > active/decisions/handoff-to-copilot.md << EOF
# Handoff to GitHub Copilot

**From**: Claude Code
**Date**: $(date +%Y-%m-%d)

## Context
[What you were working on]

## Completed
- [x] Task 1
- [x] Task 2

## Needed
- [ ] Task 3
- [ ] Task 4

## Files
- src/components/Auth.tsx (needs UI implementation)

## Notes
[Any gotchas or important context]
EOF

# Archive session
mv active/sessions/2025-10-05-*.md archive/sessions/

# List recent activity
ls -lt active/sessions/ | head -5
```

## See Also

- `/orient` - Check for pending handoffs
- `/sync` - View collaboration status
- `/commit` - Smart commits with agent attribution
- Workflow guide: `.specify/memory/pr-workflow-guide.md`
