# Research: Complete Project Kit

**Feature**: 001-complete-project-kit
**Date**: 2025-10-08

## Existing Command Pattern Analysis

### Structure (from `/orient` and `/commit`)
```yaml
---
description: Brief description
---

# Command Title
**Purpose**: One sentence

## Execution Steps
### 1. Step Name
[Commands]

### N. Generate Output
[Format spec]

## Important Notes
## Example Output
```

**Decision**: Follow this structure for all three new commands

## Tool Availability Research

### `/stats` - Use `tokei` or fallback to `find`/`wc`
### `/audit` - Use `pip-audit` or manual pattern checks  
### `/review` - Use git commands (always available)

## Output Format

**Guideline**: Concise (<150 words), actionable, markdown formatted

## Next Steps

Phase 1 will create command templates following these patterns.
