# Data Model: Complete Project Kit

**Feature**: 001-complete-project-kit
**Date**: 2025-10-08

## Entity: Command Template

### Structure
```yaml
---
description: string  # One-line command description
---

# Title
string  # Command name and purpose

## Execution Steps
array<Step>  # Ordered list of execution steps

## Important Notes
array<string>  # Guidelines and edge cases

## Example Output
string  # Sample output format
```

### Attributes

| Attribute | Type | Required | Description |
|-----------|------|----------|-------------|
| description | string | Yes | YAML frontmatter description for slash command |
| title | string | Yes | H1 header with command name |
| purpose | string | Yes | One-sentence purpose statement |
| execution_steps | Step[] | Yes | Ordered steps to execute |
| important_notes | string[] | No | Edge case handling guidance |
| example_output | string | Yes | Sample output for clarity |

### Step Structure

| Attribute | Type | Description |
|-----------|------|-------------|
| number | int | Step number (1-indexed) |
| name | string | Step description |
| commands | string[] | Bash/git commands to run |
| output_format | string | Expected output format |

## Entity: Command Output

### Structure
```markdown
## [Section Title]

**Key Finding**: Summary

- Finding 1
- Finding 2  
- Finding 3

**Next Action**: Recommendation
```

### Attributes

| Attribute | Type | Constraint |
|-----------|------|------------|
| section_title | string | Required |
| key_finding | string | <50 words |
| findings | string[] | 3-5 items max |
| next_action | string | Actionable recommendation |
| total_length | int | <150 words typical |

## Validation Rules

### Command Template Validation
- MUST have YAML frontmatter with `description`
- MUST have numbered execution steps (### 1., ### 2., etc.)
- SHOULD have example output section
- MUST use cross-platform commands (no platform-specific)

### Output Validation
- MUST be concise (<150 words typical, <500 words max)
- MUST include actionable next steps
- SHOULD use markdown code blocks for data
- MUST handle errors gracefully (no crashes on missing tools)

## Relationships

```
project-kit (1) ──contains──> (*) CommandTemplate
CommandTemplate (1) ──generates──> (1) CommandOutput
CommandTemplate (1) ──has──> (*) ExecutionStep
```

## State Transitions

Command templates are stateless (pure functions):
```
Input (git state, filesystem) → Execute Steps → Output (markdown)
```

No state persisted between executions.
