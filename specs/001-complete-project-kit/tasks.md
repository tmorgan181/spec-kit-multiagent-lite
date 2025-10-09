# Tasks: Complete Project Kit

**Input**: Design documents from `specs/001-complete-project-kit/`
**Prerequisites**: plan.md ✅, research.md ✅, data-model.md ✅, contracts/ ✅

## Execution Flow (main)
```
1. Load plan.md from feature directory
   → ✅ Tech stack: Markdown templates, Python installer
   → ✅ Structure: Single project (src/lite_kits/kits/project/)
2. Load optional design documents:
   → ✅ contracts/: 3 command contracts (review, audit, stats)
   → ✅ data-model.md: CommandTemplate entity
   → ✅ research.md: Pattern analysis from /orient
3. Generate tasks by category:
   → Setup: Verify project structure
   → Tests: N/A (manual testing via quickstart.md)
   → Core: 6 command template files
   → Integration: Installer verification
   → Polish: Documentation updates, manual testing
4. Apply task rules:
   → 6 template files = all [P] (different files, independent)
   → Installer check sequential (depends on templates)
   → Documentation sequential (depends on implementation)
5. Number tasks sequentially (T001, T002...)
6. Generate dependency graph
7. Create parallel execution examples
8. Validate task completeness:
   → ✅ All 3 contracts have 2 templates each (Claude + Copilot)
   → ✅ All templates follow /orient pattern
   → ✅ Installer mappings verified
9. Return: SUCCESS (tasks ready for execution)
```

## Format: `[ID] [P?] Description`
- **[P]**: Can run in parallel (different files, no dependencies)
- Include exact file paths in descriptions

## Path Conventions
Using single project structure from plan.md:
- Templates: `src/lite_kits/kits/project/{claude/commands,github/prompts}/`
- Documentation: `src/lite_kits/kits/project/README.md`
- Existing reference: `src/lite_kits/kits/project/claude/commands/orient.md`

## Phase 3.1: Setup & Verification
- [x] T001 Verify project structure exists at `src/lite_kits/kits/project/`
- [x] T002 Read existing `/orient` command as pattern reference

## Phase 3.2: Core Implementation - Command Templates

**Note**: No traditional tests for markdown templates. Manual testing via quickstart.md happens in Phase 3.4.

### Claude Code Templates (can run in parallel)
- [x] T003 [P] Create `/review` command at `src/lite_kits/kits/project/claude/commands/review.md`
  - Follow contract: `specs/001-complete-project-kit/contracts/review-command.md`
  - Pattern: YAML frontmatter + execution steps + example output
  - Content: Git diff analysis, linting suggestions, concise output

- [x] T004 [P] Create `/audit` command at `src/lite_kits/kits/project/claude/commands/audit.md`
  - Follow contract: `specs/001-complete-project-kit/contracts/audit-command.md`
  - Pattern: YAML frontmatter + execution steps + example output
  - Content: Dependency scanning, security patterns, graceful fallbacks

- [x] T005 [P] Create `/stats` command at `src/lite_kits/kits/project/claude/commands/stats.md`
  - Follow contract: `specs/001-complete-project-kit/contracts/stats-command.md`
  - Pattern: YAML frontmatter + execution steps + example output
  - Content: LOC counts, git history, concise table format

### GitHub Copilot Templates (can run in parallel)
- [x] T006 [P] Create `/review` prompt at `src/lite_kits/kits/project/github/prompts/review.prompt.md`
  - Mirror T003 content with Copilot-specific format
  - Follow existing `orient.prompt.md` structure

- [x] T007 [P] Create `/audit` prompt at `src/lite_kits/kits/project/github/prompts/audit.prompt.md`
  - Mirror T004 content with Copilot-specific format
  - Follow existing `orient.prompt.md` structure

- [x] T008 [P] Create `/stats` prompt at `src/lite_kits/kits/project/github/prompts/stats.prompt.md`
  - Mirror T005 content with Copilot-specific format
  - Follow existing `orient.prompt.md` structure

## Phase 3.3: Integration & Verification
- [x] T009 Verify installer includes new commands in project-kit mapping
  - Check `src/lite_kits/installer.py` project-kit kit definition
  - Ensure `review.md`, `audit.md`, `stats.md` will be copied on install
  - No code changes needed (installer already handles all .md files)

## Phase 3.4: Documentation & Testing
- [x] T010 Update `src/lite_kits/kits/project/README.md` with new commands
  - Add `/review`, `/audit`, `/stats` descriptions
  - Document purpose, usage, and output format
  - Include cross-references to contracts

- [x] T011 Execute manual testing via `specs/001-complete-project-kit/quickstart.md`
  - Test Scenario 1: `/review` with uncommitted changes
  - Test Scenario 2: `/audit` with test dependencies
  - Test Scenario 3: `/stats` on lite-kits repo
  - Validate: concise output, graceful fallbacks, actionable next steps

## Dependencies

**Critical Path**:
```
T001, T002 (setup)
  ↓
T003-T008 (all [P] - can run in parallel)
  ↓
T009 (installer check - requires templates to exist)
  ↓
T010 (docs - requires templates complete)
  ↓
T011 (manual testing - requires all complete)
```

**Parallel Execution Groups**:
- Group 1: T003, T004, T005 (Claude templates)
- Group 2: T006, T007, T008 (Copilot templates)
- Can run Group 1 + Group 2 simultaneously (all 6 templates at once)

## Parallel Example

```bash
# Launch all 6 template tasks together:
# (In Claude Code or task runner)

Task: "Create review.md for Claude at src/lite_kits/kits/project/claude/commands/review.md following contracts/review-command.md"
Task: "Create audit.md for Claude at src/lite_kits/kits/project/claude/commands/audit.md following contracts/audit-command.md"
Task: "Create stats.md for Claude at src/lite_kits/kits/project/claude/commands/stats.md following contracts/stats-command.md"
Task: "Create review.prompt.md for Copilot at src/lite_kits/kits/project/github/prompts/review.prompt.md"
Task: "Create audit.prompt.md for Copilot at src/lite_kits/kits/project/github/prompts/audit.prompt.md"
Task: "Create stats.prompt.md for Copilot at src/lite_kits/kits/project/github/prompts/stats.prompt.md"
```

## Notes

- **No traditional TDD**: Markdown templates don't have unit tests; validated via manual execution
- **Pattern consistency**: All templates MUST follow `/orient` structure (see T002)
- **Cross-platform**: Avoid platform-specific commands (use git, not PowerShell-only)
- **Graceful fallbacks**: Handle missing tools (tokei, pip-audit) without errors
- **Concise output**: All commands target <150 words output
- **Installer agnostic**: Installer already copies all `.md` files; no changes needed

## Task Generation Rules
*Applied during main() execution*

1. **From Contracts**: ✅
   - 3 contracts → 6 template files (3 Claude + 3 Copilot) = T003-T008

2. **From Data Model**: ✅
   - CommandTemplate entity → validated by following `/orient` pattern

3. **From User Stories**: ✅
   - Quickstart scenarios → manual testing task = T011

4. **Ordering**: ✅
   - Setup → Templates → Integration → Documentation → Testing

## Validation Checklist
*GATE: Checked by main() before returning*

- [x] All contracts have corresponding templates (3 contracts × 2 interfaces = 6 files)
- [x] All templates follow same structure (YAML + steps + examples)
- [x] Parallel tasks truly independent (T003-T008 all different files)
- [x] Each task specifies exact file path
- [x] No task modifies same file as another [P] task
- [x] Manual testing covers all three commands

---

**Total Tasks**: 11
**Parallel Tasks**: 6 (T003-T008)
**Sequential Tasks**: 5 (T001, T002, T009, T010, T011)
**Estimated Time**: 2-3 hours (templates straightforward, follow existing pattern)
