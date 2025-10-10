# Feature Specification: Complete Project Kit

**Feature Branch**: `001-complete-project-kit`
**Created**: 2025-10-08
**Status**: Draft
**Input**: User description: "complete project kit"

## Execution Flow (main)
```
1. Parse user description from Input
   → Feature: Add missing commands to project-kit (/review, /audit, /stats)
2. Extract key concepts from description
   → Actors: AI agents (solo developers), human users
   → Actions: Code review, security audit, project statistics
   → Data: Source code, dependencies, git history, test results
   → Constraints: Read-only analysis, concise output, cross-platform
3. For each unclear aspect:
   → All aspects clear from existing /orient implementation
4. Fill User Scenarios & Testing section
   → User flows defined below
5. Generate Functional Requirements
   → All requirements testable
6. Identify Key Entities
   → Commands, kit structure, output formats
7. Run Review Checklist
   → No clarifications needed, implementation-agnostic
8. Return: SUCCESS (spec ready for planning)
```

---

## ⚡ Quick Guidelines
- ✅ Focus on WHAT users need and WHY
- ❌ Avoid HOW to implement (no tech stack, APIs, code structure)
- 👥 Written for business stakeholders, not developers

### Section Requirements
- **Mandatory sections**: Must be completed for every feature
- **Optional sections**: Include only when relevant to the feature
- When a section doesn't apply, remove it entirely (don't leave as "N/A")

### For AI Generation
When creating this spec from a user prompt:
1. **Mark all ambiguities**: Use [NEEDS CLARIFICATION: specific question] for any assumption you'd need to make
2. **Don't guess**: If the prompt doesn't specify something (e.g., "login system" without auth method), mark it
3. **Think like a tester**: Every vague requirement should fail the "testable and unambiguous" checklist item
4. **Common underspecified areas**:
   - User types and permissions
   - Data retention/deletion policies
   - Performance targets and scale
   - Error handling behaviors
   - Integration requirements
   - Security/compliance needs

---

## User Scenarios & Testing *(mandatory)*

### Primary User Story
As an AI agent starting a development session, I need quick access to code review, security audit, and project statistics commands to efficiently assess code quality and project health before making changes.

### Acceptance Scenarios

**Scenario 1: Code Review**
1. **Given** an AI agent working on a codebase with uncommitted changes
2. **When** the agent runs `/review`
3. **Then** the agent receives actionable feedback on code quality, potential issues, and suggestions aligned with project conventions

**Scenario 2: Security Audit**
1. **Given** an AI agent about to implement a feature involving authentication or data handling
2. **When** the agent runs `/audit`
3. **Then** the agent receives security recommendations, dependency vulnerability checks, and best practice guidance

**Scenario 3: Project Statistics**
1. **Given** an AI agent joining a project for the first time
2. **When** the agent runs `/stats`
3. **Then** the agent receives concise metrics (LOC, test coverage, file counts, language breakdown) to understand project scale

**Scenario 4: Cross-Platform Usage**
1. **Given** users on Windows, macOS, or Linux
2. **When** any project-kit command is run
3. **Then** the command works identically across all platforms with proper encoding

**Scenario 5: Integration with /orient**
1. **Given** an AI agent running `/orient`
2. **When** project-kit is detected (via `/review` marker file)
3. **Then** orient output confirms project-kit is installed and suggests relevant commands

### Edge Cases
- What happens when no uncommitted changes exist? → `/review` should review recent commits or prompt user
- How does `/audit` handle projects with no dependencies? → Reports "no dependencies to audit" gracefully
- What if project has no tests? → `/stats` shows "0% coverage" without errors
- How to handle very large codebases (10,000+ files)? → Commands should sample or focus on recent changes

## Requirements *(mandatory)*

### Functional Requirements

**FR-001**: System MUST provide a `/review` command that analyzes code quality
- Checks uncommitted changes or recent commits
- Validates against project conventions (linting, formatting)
- Provides actionable suggestions
- Cross-platform compatible (Bash + PowerShell if scripts needed)

**FR-002**: System MUST provide an `/audit` command that performs security analysis
- Scans dependencies for known vulnerabilities
- Checks for common security anti-patterns (hardcoded secrets, weak crypto)
- Reviews authentication/authorization implementations
- Suggests security best practices

**FR-003**: System MUST provide a `/stats` command that generates project metrics
- Lines of code by language
- File and directory counts
- Test coverage percentage (if tests exist)
- Git history summary (commits, contributors)
- Output concise enough to fit in chat window (~20 lines max)

**FR-004**: All commands MUST integrate with existing `/orient` command
- `/orient` detects project-kit installation via `/review` marker file
- Commands follow same format/style as existing `/commit`, `/pr` commands
- Compatible with both Claude Code and GitHub Copilot interfaces

**FR-005**: Commands MUST be read-only (no modifications to codebase)
- No file writes except optional cache files
- No git operations that change history
- Safe to run multiple times without side effects

**FR-006**: Output MUST be concise and actionable for AI agents
- Summaries fit within AI context windows
- Prioritize most important findings
- Suggest concrete next actions
- Use consistent formatting (markdown, code blocks)

**FR-007**: Commands MUST handle errors gracefully
- Missing files or dependencies → informative messages
- Permission errors → suggest remediation
- Invalid project states → explain requirements

### Key Entities

- **project-kit**: Collection of commands for solo AI agent development
  - Contains: `/orient` (existing), `/review` (new), `/audit` (new), `/stats` (new)
  - Installable independently from git-kit and multiagent-kit
  - Marker file: `.claude/commands/review.md` (used by `/orient` for detection)

- **Command Templates**: Markdown prompt files for AI assistants
  - Claude Code format: `.claude/commands/*.md`
  - GitHub Copilot format: `.github/prompts/*.prompt.md`
  - Structure: YAML frontmatter + execution steps + examples

- **Output Format**: Consistent across all project-kit commands
  - Markdown with code blocks
  - Concise summaries (~150 words or less)
  - Actionable recommendations
  - Links to relevant documentation

---

## Review & Acceptance Checklist
*GATE: Automated checks run during main() execution*

### Content Quality
- [x] No implementation details (languages, frameworks, APIs)
- [x] Focused on user value and business needs
- [x] Written for non-technical stakeholders
- [x] All mandatory sections completed

### Requirement Completeness
- [x] No [NEEDS CLARIFICATION] markers remain
- [x] Requirements are testable and unambiguous
- [x] Success criteria are measurable
- [x] Scope is clearly bounded
- [x] Dependencies and assumptions identified

---

## Execution Status
*Updated by main() during processing*

- [x] User description parsed
- [x] Key concepts extracted
- [x] Ambiguities marked (none found)
- [x] User scenarios defined
- [x] Requirements generated
- [x] Entities identified
- [x] Review checklist passed

---
