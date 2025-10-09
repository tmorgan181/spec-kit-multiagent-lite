# Implementation Plan: Complete Project Kit

**Branch**: `001-complete-project-kit` | **Date**: 2025-10-08 | **Spec**: [spec.md](spec.md)
**Input**: Feature specification from `specs/001-complete-project-kit/spec.md`

## Execution Flow (/plan command scope)
```
1. Load feature spec from Input path
   → ✅ Spec loaded successfully
2. Fill Technical Context
   → ✅ Python markdown templates, no storage needed
3. Fill Constitution Check
   → ✅ N/A (template project)
4. Evaluate Constitution Check
   → ✅ PASS
5. Execute Phase 0 → research.md
   → ✅ Complete (analyzed existing patterns)
6. Execute Phase 1 → contracts, data-model.md, quickstart.md
   → ✅ Complete (3 contracts, data model, quickstart)
7. Re-evaluate Constitution Check
   → ✅ PASS
8. Plan Phase 2 → Task generation approach
   → ✅ Described below
9. STOP - Ready for /tasks command
```

**IMPORTANT**: The /plan command STOPS here. Phases 2-4 are executed by other commands:
- Phase 2: /tasks command creates tasks.md
- Phase 3-4: Implementation execution (manual or via tools)

## Summary

Complete the project-kit by adding three AI assistant commands (`/review`, `/audit`, `/stats`) following the existing `/orient` pattern. Each command is a markdown template file that provides structured execution steps for code analysis tasks. Commands must be concise (<150 words output), cross-platform compatible, and handle missing tools gracefully.

## Technical Context

**Language/Version**: Markdown (templates), Python 3.11+ (installer)  
**Primary Dependencies**: None (pure markdown templates)  
**Storage**: N/A (read-only commands)  
**Testing**: Manual command execution testing  
**Target Platform**: Claude Code, GitHub Copilot (cross-platform)  
**Project Type**: Single project (Python package with templates)  
**Performance Goals**: <5 second execution, <150 word output  
**Constraints**: Read-only operations, cross-platform, graceful tool fallbacks  
**Scale/Scope**: 3 commands × 2 interfaces = 6 markdown files

## Constitution Check

*GATE: Must pass before Phase 0 research. Re-check after Phase 1 design.*

**N/A**: This feature involves markdown template files for AI assistants, not application code. Constitution principles (library-first, CLI, TDD) apply to the Python installer (already implemented), not template content.

**Template Quality Gates** (in place of constitution):
- ✅ Templates self-contained and executable
- ✅ Output concise (<150 words)
- ✅ Cross-platform compatible
- ✅ Follow existing `/orient`/`/commit` patterns

## Project Structure

### Documentation (this feature)
```
specs/001-complete-project-kit/
├── plan.md                    # This file
├── research.md                # ✅ Pattern analysis
├── data-model.md              # ✅ Command structure
├── quickstart.md              # ✅ Test scenarios
└── contracts/
    ├── review-command.md      # ✅ /review contract
    ├── audit-command.md       # ✅ /audit contract
    └── stats-command.md       # ✅ /stats contract
```

### Source Code (repository root)
```
src/lite_kits/kits/project/
├── README.md
├── claude/
│   └── commands/
│       ├── orient.md          # Existing
│       ├── review.md          # NEW
│       ├── audit.md           # NEW
│       └── stats.md           # NEW
└── github/
    └── prompts/
        ├── orient.prompt.md   # Existing
        ├── review.prompt.md   # NEW
        ├── audit.prompt.md    # NEW
        └── stats.prompt.md    # NEW
```

**Structure Decision**: Single project structure. New command templates added to existing `src/lite_kits/kits/project/` directory with separate Claude Code and GitHub Copilot versions.

## Phase 0: Outline & Research

**Status**: ✅ Complete

See [research.md](research.md) for full details.

**Key Findings**:
- Existing commands follow YAML frontmatter + execution steps pattern
- Use `tokei` for LOC stats, `pip-audit` for security, git commands for review
- Graceful fallbacks required for missing tools
- Output must be concise (<150 words)

## Phase 1: Design & Contracts

**Status**: ✅ Complete

### Data Model
See [data-model.md](data-model.md) for full entity definitions.

**Key Entities**:
- `CommandTemplate`: YAML frontmatter + execution steps + example output
- `CommandOutput`: Concise markdown with findings + next action

### Contracts
See [contracts/](contracts/) directory for complete specifications.

1. **`/review` command** - [review-command.md](contracts/review-command.md)
   - Input: Git state (uncommitted changes)
   - Output: File assessments + suggestions + next action
   - Edge cases: No changes, too many files, binary files

2. **`/audit` command** - [audit-command.md](contracts/audit-command.md)
   - Input: Dependency files, source code
   - Output: Vulnerabilities + code patterns + next action
   - Edge cases: No dependencies, tool missing, false positives

3. **`/stats` command** - [stats-command.md](contracts/stats-command.md)
   - Input: Repository files, git history
   - Output: LOC table + structure + git summary
   - Edge cases: Tool missing, very large repo, no tests

### Quickstart
See [quickstart.md](quickstart.md) for complete test scenarios.

**Test Coverage**:
- Scenario 1: `/review` with uncommitted changes
- Scenario 2: `/audit` with vulnerable dependencies
- Scenario 3: `/stats` on small test project

## Phase 2: Task Planning Approach

*This section describes what the /tasks command will do - DO NOT execute during /plan*

**Task Generation Strategy**:

1. **Template Creation Tasks** (6 tasks - one per file):
   - Task: Create `/review` for Claude Code
   - Task: Create `/review` for GitHub Copilot
   - Task: Create `/audit` for Claude Code
   - Task: Create `/audit` for GitHub Copilot
   - Task: Create `/stats` for Claude Code
   - Task: Create `/stats` for GitHub Copilot

2. **Installer Update Tasks** (1 task):
   - Task: Verify project-kit installer includes new commands

3. **Documentation Tasks** (1 task):
   - Task: Update project-kit README.md with new commands

4. **Testing Tasks** (1 task):
   - Task: Execute quickstart.md test scenarios

**Ordering Strategy**:
- Create all 6 template files first (can be done in parallel)
- Update installer second (depends on templates existing)
- Update documentation third
- Test last (depends on all files existing)

**Estimated Output**: 9 numbered tasks in tasks.md

**Task Breakdown**:
```
1. [P] Create review.md (Claude)
2. [P] Create review.prompt.md (Copilot)
3. [P] Create audit.md (Claude)
4. [P] Create audit.prompt.md (Copilot)
5. [P] Create stats.md (Claude)
6. [P] Create stats.prompt.md (Copilot)
7. Verify installer mappings
8. Update project-kit README
9. Run quickstart tests
```

[P] = Can be executed in parallel

**IMPORTANT**: This phase is executed by the /tasks command, NOT by /plan

## Phase 3+: Future Implementation

*These phases are beyond the scope of the /plan command*

**Phase 3**: Task execution (/tasks command creates tasks.md)  
**Phase 4**: Implementation (create 6 template files + update docs)  
**Phase 5**: Validation (run quickstart.md scenarios)

## Complexity Tracking

*Fill ONLY if Constitution Check has violations that must be justified*

No violations - constitution not applicable to template files.

## Progress Tracking

*This checklist is updated during execution flow*

**Phase Status**:
- [x] Phase 0: Research complete (/plan command)
- [x] Phase 1: Design complete (/plan command)
- [x] Phase 2: Task planning complete (/plan command - describe approach only)
- [ ] Phase 3: Tasks generated (/tasks command)
- [ ] Phase 4: Implementation complete
- [ ] Phase 5: Validation passed

**Gate Status**:
- [x] Initial Constitution Check: PASS (N/A for templates)
- [x] Post-Design Constitution Check: PASS (N/A for templates)
- [x] All NEEDS CLARIFICATION resolved
- [x] Complexity deviations documented (none)

---
*Based on Constitution v2.1.1 - See `.specify/memory/constitution.md`*
