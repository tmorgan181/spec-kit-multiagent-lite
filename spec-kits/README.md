# Vanilla Spec-Kit Reference Configurations

This directory contains **unmodified** vanilla spec-kit configurations for reference and testing purposes.

## Purpose

These are vanilla configurations from the [GitHub spec-kit](https://github.com/github/spec-kit) project, organized by AI agent interface. They serve as:

1. **Reference material** - See what vanilla spec-kit looks like
2. **Testing baseline** - Test that our kits install correctly on top of vanilla
3. **Comparison** - Compare vanilla vs vanilla+kits side-by-side
4. **Documentation** - Show users what they're getting from upstream

## Directory Structure

```
spec-kits/
├── README.md                    # This file
├── UPSTREAM.md                  # How to update from upstream
├── claude-code-vanilla/         # Vanilla for Claude Code
│   ├── .claude/
│   │   ├── CLAUDE.md
│   │   ├── commands/            # /specify, /plan, /tasks, /implement, etc.
│   │   └── settings.local.json
│   └── .specify/
│       ├── memory/
│       │   └── constitution.md  # Template
│       ├── scripts/
│       │   ├── bash/
│       │   └── powershell/
│       └── templates/
│           ├── spec-template.md
│           ├── plan-template.md
│           └── tasks-template.md
│
├── github-cli-vanilla/          # Vanilla for GitHub Copilot
│   ├── .github/
│   │   ├── copilot-instructions.md
│   │   └── prompts/             # /specify, /plan, /tasks, /implement, etc.
│   └── .specify/
│       ├── memory/
│       │   └── constitution.md  # Template
│       ├── scripts/
│       │   ├── bash/
│       │   └── powershell/
│       └── templates/
│           ├── spec-template.md
│           ├── plan-template.md
│           └── tasks-template.md
│
└── project-kit/                 # Where /orient originated
    └── .github/project-prompts/
        └── orient.prompt.md     # Original /orient command
```

## What Our Kits Add

### Recommended Kits (project + git)

**Install command**: `speckit-ma install --recommended`

Adds to vanilla:
```
your-vanilla-project/
├── .claude/commands/           # If Claude Code
│   ├── [vanilla commands]      # ← Untouched
│   ├── orient.md               # ← NEW (project-kit)
│   ├── review.md               # ← NEW (project-kit)
│   ├── commit.md               # ← NEW (git-kit)
│   └── pr.md                   # ← NEW (git-kit)
├── .github/prompts/            # If GitHub Copilot
│   ├── [vanilla prompts]       # ← Untouched
│   ├── orient.prompt.md        # ← NEW (project-kit)
│   ├── review.prompt.md        # ← NEW (project-kit)
│   ├── commit.prompt.md        # ← NEW (git-kit)
│   └── pr.prompt.md            # ← NEW (git-kit)
└── .specify/
    ├── memory/
    │   └── constitution.md     # ← Untouched
    └── scripts/
        ├── bash/
        │   ├── [vanilla scripts]           # ← Untouched
        │   └── create-feature-enhanced.sh  # ← NEW (project-kit)
        └── powershell/
            ├── [vanilla scripts]               # ← Untouched
            └── Create-Feature-Enhanced.ps1     # ← NEW (project-kit)
```

### Optional Kit (multiagent)

**Install command**: `speckit-ma install --kit=multiagent`

Adds to vanilla:
```
your-vanilla-project/
└── .specify/memory/
    ├── constitution.md               # ← Untouched
    ├── pr-workflow-guide.md          # ← NEW (multiagent-kit)
    └── git-worktrees-protocol.md     # ← NEW (multiagent-kit)
```

## Key Principles

### ✅ What We Do

- **Only add new files** - Never modify vanilla files
- **Version-safe** - Updates to vanilla spec-kit won't break our kits
- **Uninstallable** - Can remove our kits and return to pure vanilla
- **Cross-agent** - Works with both Claude Code and GitHub Copilot
- **Cross-platform** - Works with both Bash and PowerShell

### ❌ What We Don't Do

- ❌ Modify vanilla commands (`/specify`, `/plan`, etc.)
- ❌ Change vanilla scripts (`create-new-feature.sh`, etc.)
- ❌ Edit vanilla templates (`spec-template.md`, etc.)
- ❌ Touch vanilla memory files (`constitution.md`)
- ❌ Require specific versions of vanilla spec-kit

## Vanilla Spec-Kit Workflow

For reference, vanilla spec-kit provides:

### Commands
1. `/specify` - Create feature specification
2. `/clarify` - Clarify ambiguities in spec
3. `/plan` - Create implementation plan
4. `/tasks` - Break down into tasks
5. `/implement` - Execute implementation
6. `/analyze` - Analyze spec/plan/tasks for issues
7. `/constitution` - Update project constitution

### Scripts
- `create-new-feature.sh` - Create feature branch and directory
- `setup-plan.sh` - Initialize plan.md
- `check-prerequisites.sh` - Validate workflow prerequisites
- `update-agent-context.sh` - Update AI agent context files

## Our Add-ons

### project-kit
**Essential commands**:
- `/orient` ⭐ - Agent orientation (most important!)
- `/review` - Code review
- `/audit` - Security audit
- `/stats` - Project statistics

**Enhanced scripts**:
- `create-feature-enhanced.sh` - Custom feature numbering/naming

### git-kit
**Git workflow commands**:
- `/commit` - Smart commits with attribution
- `/pr` - Create pull request
- `/sync` - Sync status with ASCII viz
- `/cleanup` - Clean up branches/worktrees

### multiagent-kit
**Multi-agent coordination**:
- PR workflow guide
- Git worktrees protocol
- Collaboration directory templates

## Testing Our Kits

To test that our kits work correctly with vanilla:

```bash
# 1. Copy vanilla to test directory
cp -r spec-kits/claude-code-vanilla /tmp/test-project
cd /tmp/test-project

# 2. Install our kits
speckit-ma install --recommended

# 3. Verify installation
ls .claude/commands/
# Should show: vanilla commands + orient.md, review.md, commit.md, pr.md

# 4. Test that vanilla still works
# Create a feature using vanilla script
.specify/scripts/bash/create-new-feature.sh "Test feature"

# 5. Test our additions
# Run /orient in Claude Code
```

## Updating from Upstream

See [UPSTREAM.md](UPSTREAM.md) for instructions on updating vanilla configurations when GitHub releases new versions of spec-kit.

## Directory Naming Convention

- `{agent}-vanilla/` - Pure vanilla configuration for specific agent
- `project-kit/` - Where specific add-ons originated (not full spec-kit)

## Questions?

- **Why keep vanilla separate?** - To test compatibility and show users what they're getting
- **Can I use vanilla without kits?** - Yes! Our kits are optional add-ons
- **Do kits work with other spec-kit forks?** - Probably, as long as they follow vanilla structure
- **What if vanilla adds /orient?** - Our version is namespaced differently, no conflict

## Related

- Main package: [src/speckit_multiagent/](../src/speckit_multiagent/)
- Kit documentation: [src/speckit_multiagent/kits/](../src/speckit_multiagent/kits/)
- Examples: [examples/](../examples/)
