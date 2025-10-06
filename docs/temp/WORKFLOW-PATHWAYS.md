# Workflow Pathways: Vanilla + Kits Integration

**Purpose**: Define exact order of operations for AI contributors using vanilla spec-kit with our add-on kits.

**Key Principle**: Our kits **augment** vanilla, never replace. Commands wrap vanilla logic, scripts work alongside vanilla scripts, all changes are version-safe.

---

## Table of Contents

1. [Detection & Orientation](#detection--orientation)
2. [Feature Creation Pathways](#feature-creation-pathways)
3. [Command Execution Patterns](#command-execution-patterns)
4. [Script Invocation Logic](#script-invocation-logic)
5. [Multi-Agent Coordination](#multi-agent-coordination)
6. [Version Safety Guarantees](#version-safety-guarantees)

---

## Detection & Orientation

### Case 1: Fresh AI Agent Starts Work

**Scenario**: New AI agent (Claude Code or Copilot) opens project

**Pathway**:

```
1. Agent detects available commands
   ├─ Lists .claude/commands/ OR .github/prompts/
   └─ Sees: vanilla commands + /orient (if project-kit installed)

2. Agent runs /orient (if available)
   ├─ /orient detects installation status:
   │  ├─ Checks for .claude/commands/review.md (project-kit marker)
   │  ├─ Checks for .claude/commands/commit.md (git-kit marker)
   │  ├─ Checks for .specify/memory/pr-workflow-guide.md (multiagent-kit marker)
   │  └─ Reports: "Installed kits: project, git" OR "Vanilla spec-kit only"
   │
   ├─ /orient reads (in order):
   │  ├─ .github/copilot-instructions.md (primary, if exists)
   │  ├─ .specify/memory/constitution.md (project philosophy)
   │  ├─ git status + git log -5 (current state)
   │  └─ specs/*/collaboration/ (if multiagent-kit installed)
   │
   └─ /orient outputs (~150 words):
      ├─ Agent role (Claude=primary, Copilot=specialist)
      ├─ Project stack/principles
      ├─ Current branch/commits
      ├─ Installed kits
      └─ Suggested next action

3. Agent proceeds with vanilla workflow OR enhanced workflow
   └─ Decision based on /orient output and installed kits
```

**Key Integration Points**:

- `/orient` is **additive** - doesn't interfere with vanilla
- If `/orient` missing, agent uses vanilla commands directly
- Detection is passive - checks file existence, no modification

---

## Feature Creation Pathways

### Case 2A: Vanilla Feature Creation (No Kits)

**Scenario**: Pure vanilla spec-kit, no kits installed

**Pathway**:

```
1. Agent runs vanilla: /specify "Add user authentication"
   └─ Calls: .specify/scripts/{bash,powershell}/create-new-feature.sh

2. Vanilla script executes:
   ├─ Auto-generates feature number (001, 002, 003...)
   ├─ Creates branch: 003-add-user-authentication
   ├─ Creates directory: specs/003-add-user-authentication/
   └─ Creates spec.md from template

3. Agent runs vanilla: /plan
   └─ Calls: .specify/scripts/{bash,powershell}/setup-plan.sh

4. Agent runs vanilla: /tasks
   └─ Generates tasks.md

5. Agent runs vanilla: /implement
   └─ Implements feature
```

**Result**: Pure vanilla workflow, no kit interference

---

### Case 2B: Feature Creation with Project-Kit

**Scenario**: project-kit installed, wants custom feature naming

**Pathway**:

```
1. Agent runs: /specify "Add user authentication"
   ├─ Our /specify wrapper detects project-kit
   └─ Wrapper logic:
      ├─ IF user provides --num or --name flags:
      │  └─ Call: .specify/scripts/bash/create-feature-enhanced.sh --num 010 --name auth-v2
      ├─ ELSE:
      │  └─ Call vanilla: .specify/scripts/bash/create-new-feature.sh
      └─ Both scripts create same structure, different naming

2. Enhanced script (if used) executes:
   ├─ Uses custom number: 010 (instead of auto-increment)
   ├─ Uses custom name: auth-v2 (instead of first 3 words)
   ├─ Creates branch: 010-auth-v2
   ├─ Creates directory: specs/010-auth-v2/
   └─ Creates spec.md from vanilla template

3. Agent runs vanilla: /plan
   └─ Works identically (uses vanilla script)

4. Agent runs vanilla: /tasks
   └─ Works identically (uses vanilla script)

5. Agent runs vanilla: /implement
   └─ Works identically (vanilla implementation)
```

**Key Integration**:

- `/specify` wrapper checks for flags, delegates to appropriate script
- Enhanced script creates **identical structure** to vanilla
- Vanilla /plan, /tasks, /implement work unchanged
- No vanilla files modified

---

### Case 2C: Feature Creation with Multiagent-Kit

**Scenario**: multiagent-kit installed, creating feature for multi-agent work

**Pathway**:

```
1. Agent runs: /specify "Add blog platform"
   └─ Vanilla or enhanced script creates feature

2. After feature creation, /specify wrapper detects multiagent-kit:
   ├─ Checks for: .specify/memory/pr-workflow-guide.md
   └─ If found:
      ├─ Creates: specs/004-blog-platform/collaboration/
      │  ├─ active/
      │  │  ├─ sessions/
      │  │  ├─ decisions/
      │  │  └─ README.md (template)
      │  ├─ archive/
      │  └─ results/
      │     ├─ validation/
      │     └─ artifacts/
      └─ Reports: "Collaboration structure created for multi-agent work"

3. Agent runs /plan
   └─ Vanilla plan generation

4. Agent optionally creates handoff document:
   └─ specs/004-blog-platform/collaboration/active/decisions/agent-split.md

5. Agents proceed with coordination
```

**Key Integration**:

- Collaboration structure is **post-creation addition**
- Vanilla workflow unaffected
- Optional handoff documents are agent-created, not automated
- Template structure ensures consistency

---

## Command Execution Patterns

### Case 3A: /orient (Project-Kit Only)

**File**: `.claude/commands/orient.md`

**Execution**:

```markdown
---
description: Agent orientation protocol
---

# Agent Orientation

**Purpose**: Quickly orient AI agents to project context.

## Execution Flow:

1. Detect installed kits:
   ```bash
   # Check markers
   [ -f .claude/commands/review.md ] && KIT_PROJECT=true
   [ -f .claude/commands/commit.md ] && KIT_GIT=true
   [ -f .specify/memory/pr-workflow-guide.md ] && KIT_MULTIAGENT=true
   ```

2. Read primary documentation:
   - .github/copilot-instructions.md (if exists)
   - .specify/memory/constitution.md

3. Check git state:
   - Current branch
   - Recent commits (last 5)
   - Uncommitted changes

4. Check collaboration (if multiagent-kit):
   - Active sessions in specs/*/collaboration/active/sessions/
   - Pending handoffs in specs/*/collaboration/active/decisions/

5. Output concise summary:
   ```
   ## Orientation Complete

   **Installed Kits**: project, git

   **I am**: Claude Code (Primary)
   **Project**: [from copilot-instructions.md]
   **Stack**: [from copilot-instructions.md]
   **Branch**: dev/001-starter-kits
   **Recent work**: Reorganized kit structure
   **Coordination**: Solo work
   **Next**: [suggested action based on state]
   ```

6. Suggest next action based on state:
   - If no spec: "Run /specify to start new feature"
   - If spec exists, no plan: "Run /plan to create implementation plan"
   - If plan exists: "Run /implement to start coding"
   - If multiagent + handoff pending: "Review handoff in collaboration/"
```

**Integration with Vanilla**: None - this is a new command, doesn't touch vanilla

---

### Case 3B: /specify (Wrapper Around Vanilla)

**File**: `.claude/commands/specify.md` (OUR VERSION)

**Execution**:

```markdown
---
description: Create or update feature specification (enhanced with kit support)
---

# Feature Specification (Enhanced)

This command wraps vanilla /specify with kit-aware enhancements.

## Execution Flow:

1. Parse user input:
   ```
   /specify "Add user auth" --num 010 --name auth-v2
   ```

2. Detect project-kit installation:
   ```bash
   if [ -f .specify/scripts/bash/create-feature-enhanced.sh ]; then
     ENHANCED=true
   else
     ENHANCED=false
   fi
   ```

3. Route to appropriate script:
   ```bash
   if [ "$ENHANCED" = true ] && [ -n "$NUM_FLAG" -o -n "$NAME_FLAG" ]; then
     # Use enhanced script
     .specify/scripts/bash/create-feature-enhanced.sh --num $NUM --name $NAME "$DESCRIPTION"
   else
     # Use vanilla script (default)
     .specify/scripts/bash/create-new-feature.sh "$DESCRIPTION"
   fi
   ```

4. Post-creation enhancement (if multiagent-kit):
   ```bash
   if [ -f .specify/memory/pr-workflow-guide.md ]; then
     # Create collaboration structure
     mkdir -p "specs/$FEATURE_DIR/collaboration/"{active/{sessions,decisions},archive,results/{validation,artifacts}}
     # Copy template README
     cp .specify/templates/collaboration/README.md "specs/$FEATURE_DIR/collaboration/active/"
   fi
   ```

5. Report results:
   ```
   ✓ Feature created: specs/010-auth-v2/
   ✓ Branch created: 010-auth-v2
   ✓ Spec initialized: specs/010-auth-v2/spec.md
   [if multiagent] ✓ Collaboration structure created

   Next: Edit spec.md, then run /plan
   ```

**Integration Points**:

- Checks for enhanced script before calling vanilla
- Falls back to vanilla if no flags provided
- Adds collaboration structure without modifying vanilla
- Reports all actions transparently

---

### Case 3C: /commit (Git-Kit, Wraps Git)

**File**: `.claude/commands/commit.md`

**Execution**:

```markdown
---
description: Smart commit with agent attribution
---

# Smart Commit

Generates commit message and adds agent attribution.

## Execution Flow:

1. Check staged changes:
   ```bash
   git status --short
   git diff --staged
   ```

2. Analyze changes to generate message:
   - Detect change type (feat, fix, refactor, docs, test, chore)
   - Summarize files changed
   - Generate description

3. Generate commit message:
   ```
   feat: Add user authentication

   Implements bcrypt password hashing, JWT tokens,
   and session management.

   via claude-sonnet-4.5 @ claude-code
   ```

4. Prompt for confirmation:
   ```
   **Suggested commit message**:
   [show message above]

   **Confirm?** (y/n/edit):
   ```

5. Execute commit:
   ```bash
   git commit -m "$MESSAGE"
   ```

**Integration with Vanilla**: None - this is pure git operation, doesn't touch spec-kit

---

## Script Invocation Logic

### Case 4A: Enhanced Script Alongside Vanilla

**Files**:
- Vanilla: `.specify/scripts/bash/create-new-feature.sh` (untouched)
- Enhanced: `.specify/scripts/bash/create-feature-enhanced.sh` (our addition)

**Invocation Logic**:

```bash
# In /specify command wrapper

parse_args() {
  DESCRIPTION=""
  NUM=""
  NAME=""

  for arg in "$@"; do
    case "$arg" in
      --num) shift; NUM="$1" ;;
      --name) shift; NAME="$1" ;;
      *) DESCRIPTION="$DESCRIPTION $arg" ;;
    esac
  done
}

invoke_script() {
  parse_args "$@"

  # Check for enhanced script
  ENHANCED_SCRIPT=".specify/scripts/bash/create-feature-enhanced.sh"
  VANILLA_SCRIPT=".specify/scripts/bash/create-new-feature.sh"

  if [ -f "$ENHANCED_SCRIPT" ] && [ -n "$NUM" -o -n "$NAME" ]; then
    # Use enhanced for custom naming
    echo "Using enhanced feature creation..."
    $ENHANCED_SCRIPT --num "$NUM" --name "$NAME" "$DESCRIPTION"
  elif [ -f "$VANILLA_SCRIPT" ]; then
    # Use vanilla (default behavior)
    echo "Using vanilla feature creation..."
    $VANILLA_SCRIPT "$DESCRIPTION"
  else
    echo "ERROR: No feature creation script found"
    exit 1
  fi
}
```

**Key Points**:

- Enhanced script has **different name** - no conflict
- Vanilla script remains untouched
- Command wrapper decides which to call
- Both scripts create **compatible output** (same directory structure)

---

### Case 4B: Enhanced Script Implementation

**File**: `.specify/scripts/bash/create-feature-enhanced.sh`

**Implementation**:

```bash
#!/usr/bin/env bash
# Enhanced feature creation with custom numbering/naming
# Compatible with vanilla spec-kit structure

set -e

# Parse arguments
NUM=""
NAME=""
DESCRIPTION=""

while [[ $# -gt 0 ]]; do
  case "$1" in
    --num)
      NUM="$2"
      shift 2
      ;;
    --name)
      NAME="$2"
      shift 2
      ;;
    *)
      DESCRIPTION="$DESCRIPTION $1"
      shift
      ;;
  esac
done

# Source vanilla common functions (reuse vanilla logic!)
SCRIPT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
source "$SCRIPT_DIR/common.sh"

# Get repo root using vanilla function
REPO_ROOT=$(get_repo_root)
SPECS_DIR="$REPO_ROOT/specs"

# Determine feature number
if [ -n "$NUM" ]; then
  # Use custom number
  FEATURE_NUM=$(printf "%03d" "$NUM")
else
  # Fall back to vanilla auto-increment logic
  HIGHEST=0
  for dir in "$SPECS_DIR"/*; do
    [ -d "$dir" ] || continue
    dirname=$(basename "$dir")
    number=$(echo "$dirname" | grep -o '^[0-9]\+' || echo "0")
    number=$((10#$number))
    if [ "$number" -gt "$HIGHEST" ]; then HIGHEST=$number; fi
  done
  NEXT=$((HIGHEST + 1))
  FEATURE_NUM=$(printf "%03d" "$NEXT")
fi

# Determine feature name
if [ -n "$NAME" ]; then
  # Use custom name
  BRANCH_NAME="$NAME"
else
  # Fall back to vanilla naming logic (first 3 words)
  BRANCH_NAME=$(echo "$DESCRIPTION" | tr '[:upper:]' '[:lower:]' | sed 's/[^a-z0-9]/-/g' | sed 's/-\+/-/g' | sed 's/^-//' | sed 's/-$//')
  WORDS=$(echo "$BRANCH_NAME" | tr '-' '\n' | grep -v '^$' | head -3 | tr '\n' '-' | sed 's/-$//')
  BRANCH_NAME="$WORDS"
fi

# Combine number + name
BRANCH_NAME="${FEATURE_NUM}-${BRANCH_NAME}"

# Create branch (vanilla logic)
if git rev-parse --show-toplevel >/dev/null 2>&1; then
  git checkout -b "$BRANCH_NAME"
fi

# Create directory structure (vanilla compatible)
FEATURE_DIR="$SPECS_DIR/$BRANCH_NAME"
mkdir -p "$FEATURE_DIR"

# Copy vanilla template
TEMPLATE="$REPO_ROOT/.specify/templates/spec-template.md"
SPEC_FILE="$FEATURE_DIR/spec.md"
if [ -f "$TEMPLATE" ]; then
  cp "$TEMPLATE" "$SPEC_FILE"
else
  touch "$SPEC_FILE"
fi

# Set environment variable (vanilla compatible)
export SPECIFY_FEATURE="$BRANCH_NAME"

# Output (JSON compatible with vanilla)
echo "BRANCH_NAME: $BRANCH_NAME"
echo "SPEC_FILE: $SPEC_FILE"
echo "FEATURE_NUM: $FEATURE_NUM"
```

**Integration Strategy**:

- **Reuses vanilla `common.sh`** - no duplication
- **Same output structure** - vanilla /plan, /tasks, /implement work unchanged
- **Compatible environment variables** - SPECIFY_FEATURE set identically
- **Different filename** - no conflict with vanilla script

---

## Multi-Agent Coordination

### Case 5A: Handoff Between Agents

**Scenario**: Claude Code finishes backend, hands off to Copilot for frontend

**Pathway**:

```
1. Claude Code completes backend work
   └─ Runs vanilla /implement for backend tasks

2. Claude creates handoff document:
   ├─ File: specs/003-blog/collaboration/active/decisions/handoff-to-copilot.md
   └─ Content:
      ## Handoff to Copilot
      **From**: Claude Code
      **Context**: Backend complete, need frontend
      **What's Done**: API endpoints, auth, tests
      **What's Needed**: React components, auth UI
      **Files**: src/components/LoginForm.tsx, etc.

3. Claude commits and pushes:
   └─ Runs /commit (git-kit):
      └─ "feat: Complete backend authentication

          via claude-sonnet-4.5 @ claude-code"

4. Copilot CLI runs /orient:
   ├─ Detects: multiagent-kit installed
   ├─ Checks: specs/003-blog/collaboration/active/decisions/
   ├─ Finds: handoff-to-copilot.md
   └─ Reports: "Handoff pending from Claude Code - review collaboration/active/decisions/"

5. Copilot reviews handoff:
   └─ Reads handoff document

6. Copilot creates worktree (if parallel work):
   └─ git worktree add ../blog-frontend 003-blog

7. Copilot logs session:
   └─ specs/003-blog/collaboration/active/sessions/2025-10-06-copilot-frontend.md

8. Copilot implements frontend:
   └─ Runs vanilla /implement

9. Copilot commits:
   └─ Runs /commit:
      └─ "feat: Add authentication UI

          via gpt-4 @ github-copilot-cli"

10. Both agents sync:
    └─ git pull origin 003-blog (periodically)

11. Integration PR created:
    └─ Either agent runs /pr (git-kit)
       └─ Detects multi-agent commits
       └─ Generates PR description highlighting both agents' work
```

**Key Integration**:

- Handoff documents are **agent-created**, not automated
- Collaboration structure exists **because multiagent-kit installed**
- /orient **detects and reports** handoffs
- Vanilla /implement works unchanged
- /commit and /pr add attribution but don't modify vanilla workflow

---

### Case 5B: Worktree Coordination

**Scenario**: Two agents working simultaneously

**Pathway**:

```
1. Agent 1 (Claude) creates worktree:
   └─ git worktree add ../blog-backend 003-blog

2. Agent 2 (Copilot) creates worktree:
   └─ git worktree add ../blog-frontend 003-blog

3. Both agents define territories in handoff doc:
   └─ specs/003-blog/collaboration/active/decisions/worktree-coordination.md
      **Backend territory**: src/api/, src/models/, tests/api/
      **Frontend territory**: src/components/, src/hooks/, tests/components/
      **Shared**: README.md, package.json (coordinate before editing)

4. Both agents log sessions independently:
   ├─ Agent 1: collaboration/active/sessions/2025-10-06-claude-backend.md
   └─ Agent 2: collaboration/active/sessions/2025-10-06-copilot-frontend.md

5. Both agents run vanilla /implement in their worktrees:
   ├─ Agent 1: Implements backend tasks
   └─ Agent 2: Implements frontend tasks

6. Both agents commit with attribution:
   ├─ Agent 1: /commit → "feat: Add auth API (via claude @ claude-code)"
   └─ Agent 2: /commit → "feat: Add auth UI (via gpt-4 @ copilot)"

7. Both agents push to same branch:
   └─ git push origin 003-blog

8. Periodic sync:
   └─ Both run: git pull origin 003-blog

9. No conflicts because territories defined

10. Integration:
    ├─ One agent handles integration testing
    └─ Runs /pr to create pull request
```

**Integration Points**:

- Worktrees are **git feature**, not our modification
- Vanilla /implement works in each worktree
- Collaboration docs coordinate but don't enforce
- /commit adds attribution
- /pr detects multi-agent work and generates appropriate description

---

## Version Safety Guarantees

### Principle 1: Additive Only

**What we add**:
- New command files (orient.md, review.md, commit.md, etc.)
- New script files (create-feature-enhanced.sh, etc.)
- New memory files (pr-workflow-guide.md, git-worktrees-protocol.md)
- New directory structures (collaboration/)

**What we NEVER modify**:
- Vanilla commands (/specify, /plan, /tasks, /implement, etc.)
- Vanilla scripts (create-new-feature.sh, setup-plan.sh, etc.)
- Vanilla templates (spec-template.md, plan-template.md, etc.)
- Vanilla memory (constitution.md)

**Version safety**: If vanilla updates any file, our kits don't conflict

---

### Principle 2: Wrapper Pattern

**For commands that need enhancement**:

```
Our /specify wrapper:
├─ Detects flags (--num, --name)
├─ Routes to enhanced script OR vanilla script
└─ Adds post-processing (collaboration structure)

Vanilla /specify:
└─ Remains untouched, works identically if called directly
```

**Version safety**: Vanilla command updates don't break our wrapper (we call it as-is)

---

### Principle 3: Compatible Output

**Enhanced scripts produce identical structure**:

```
Vanilla create-new-feature.sh output:
specs/003-add-user-auth/
└── spec.md

Enhanced create-feature-enhanced.sh output:
specs/010-auth-v2/      # Different number/name
└── spec.md             # Same structure!
```

**Version safety**: Vanilla /plan, /tasks, /implement work on both

---

### Principle 4: Detection-Based Behavior

**Commands detect kit installation**:

```bash
# In /orient
if [ -f .claude/commands/review.md ]; then
  echo "Kits installed: project"
else
  echo "Vanilla spec-kit only"
fi

# In /specify wrapper
if [ -f .specify/memory/pr-workflow-guide.md ]; then
  # Add collaboration structure
else
  # Skip (vanilla mode)
fi
```

**Version safety**: Behavior adapts to installation state, no assumptions

---

### Principle 5: Namespace Separation

**Our files use distinct names**:
- `create-feature-enhanced.sh` (not `create-new-feature.sh`)
- `orient.md` (new command, not overwriting existing)
- `pr-workflow-guide.md` (new doc, not `constitution.md`)

**Version safety**: No filename conflicts, ever

---

## Summary: Integration Philosophy

| Aspect | Vanilla | Our Kits | Integration Method |
|--------|---------|----------|-------------------|
| **Commands** | /specify, /plan, etc. | /orient, /review, /commit, etc. | New commands, wrappers for existing |
| **Scripts** | create-new-feature.sh | create-feature-enhanced.sh | Different names, called by wrapper |
| **Templates** | spec-template.md | (reuse vanilla) | No custom templates, use vanilla |
| **Memory** | constitution.md | pr-workflow-guide.md, etc. | New files, don't modify vanilla |
| **Structure** | specs/NNN-name/ | + collaboration/ | Additive directory structure |
| **Detection** | N/A | Check for marker files | Passive detection, no modification |
| **Execution** | Direct script calls | Wrapper → route → vanilla or enhanced | Conditional routing |
| **Output** | Standard structure | Compatible structure | Same format, different content |
| **Version safety** | Vanilla updates freely | Kits detect and adapt | No conflicts, graceful degradation |

---

## Edge Cases & Error Handling

### Case 6A: Kit Partially Installed

**Scenario**: User manually copies some kit files but not all

**Detection**:
```bash
# In /orient
PROJECT_KIT_COMPLETE=true
[ ! -f .claude/commands/orient.md ] && PROJECT_KIT_COMPLETE=false
[ ! -f .claude/commands/review.md ] && PROJECT_KIT_COMPLETE=false

if [ "$PROJECT_KIT_COMPLETE" = false ]; then
  echo "⚠ Warning: project-kit partially installed"
  echo "  Run: speckit-ma install --kit=project"
fi
```

**Handling**: Warn user, suggest reinstall, continue with degraded functionality

---

### Case 6B: Vanilla Updated, Breaks Compatibility

**Scenario**: Vanilla changes script signatures

**Detection**:
```bash
# In create-feature-enhanced.sh
# Try to source vanilla common.sh
if ! source "$SCRIPT_DIR/common.sh" 2>/dev/null; then
  echo "ERROR: Vanilla common.sh not compatible"
  echo "  This may be due to vanilla spec-kit update"
  echo "  Run: speckit-ma update"
  exit 1
fi
```

**Handling**: Detect incompatibility, instruct user to update kits

---

### Case 6C: User Removes Vanilla Files

**Scenario**: User accidentally deletes vanilla scripts

**Detection**:
```bash
# In /specify wrapper
VANILLA_SCRIPT=".specify/scripts/bash/create-new-feature.sh"
if [ ! -f "$VANILLA_SCRIPT" ]; then
  echo "ERROR: Vanilla spec-kit scripts missing"
  echo "  Please reinstall vanilla spec-kit first"
  exit 1
fi
```

**Handling**: Fail gracefully, instruct reinstall of vanilla

---

## Testing Pathways

### Test Case Matrix

| Scenario | Vanilla | project-kit | git-kit | multiagent-kit | Expected Behavior |
|----------|---------|-------------|---------|----------------|-------------------|
| 1. Pure vanilla | ✓ | ✗ | ✗ | ✗ | Standard workflow, no kit commands |
| 2. + project | ✓ | ✓ | ✗ | ✗ | /orient, /review available, vanilla works |
| 3. + git | ✓ | ✗ | ✓ | ✗ | /commit, /pr available, vanilla works |
| 4. Recommended | ✓ | ✓ | ✓ | ✗ | Full kit suite, vanilla works |
| 5. + multiagent | ✓ | ✓ | ✓ | ✓ | Collaboration structure, all features |
| 6. Missing vanilla | ✗ | ✓ | ✓ | ✓ | ERROR: Vanilla required |
| 7. Partial kits | ✓ | partial | ✗ | ✗ | WARN: Partial install, degraded |

---

## Installation Validation

After `speckit-ma install --recommended`:

**Validation checklist**:

```bash
# 1. Vanilla files untouched
diff .specify/scripts/bash/create-new-feature.sh [vanilla-backup]
# → No differences

# 2. Kit files added
[ -f .claude/commands/orient.md ]          # project-kit
[ -f .claude/commands/commit.md ]          # git-kit
[ -f .specify/scripts/bash/create-feature-enhanced.sh ]  # project-kit enhancement

# 3. No modifications to vanilla
grep -l "speckit-multiagent" .specify/scripts/bash/create-new-feature.sh
# → No matches (our kits don't modify vanilla)

# 4. Wrappers work
/specify "Test" --num 999 --name test-feature
# → Uses enhanced script

/specify "Test"
# → Uses vanilla script

# 5. Vanilla commands still work
.specify/scripts/bash/create-new-feature.sh "Direct test"
# → Works identically
```

---

## Questions for Implementation

1. **Command wrapper implementation**: Should wrappers be in `.claude/commands/` or separate directory?
   - **Recommendation**: Same directory, but clearly documented in command frontmatter

2. **Script routing**: Hard-code paths or use discovery?
   - **Recommendation**: Hard-code with fallbacks (faster, more predictable)

3. **Error reporting**: Verbose or minimal?
   - **Recommendation**: Verbose with --quiet flag option

4. **Kit detection**: File-based or manifest-based?
   - **Recommendation**: File-based (simpler, no state to manage)

5. **Collaboration structure**: Auto-create or explicit command?
   - **Recommendation**: Auto-create on /specify if multiagent-kit installed

---

This document will guide implementation of the installer and ensure version-safe integration at every level.
