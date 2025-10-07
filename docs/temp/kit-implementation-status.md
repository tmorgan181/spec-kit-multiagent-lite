# Spec-Kit-Multiagent Implementation Status
## What's Built, What's Missing, How It Stacks with Vanilla

**Baseline**: Vanilla `specify.exe` (GitHub spec-kit) provides the foundation  
**Add-on**: `spec-kit-multiagent-lite` layers coordination on top  
**Philosophy**: Add new files only, never modify vanilla

---

## 📊 Implementation Status Matrix

### Core CLI & Installer

| Component | Status | Notes |
|-----------|--------|-------|
| **CLI framework** | ✅ Complete | `typer` + `rich`, working `add`, `validate`, `status` |
| **Installer logic** | ✅ Core done | Template copying works, smart merge TODO |
| **Package metadata** | ✅ Complete | `pyproject.toml` configured, ready for PyPI |
| **Error handling** | ✅ Complete | Graceful failures, clear messages |
| **Dry-run mode** | ✅ Complete | Preview before install |
| **Uninstall** | ❌ Missing | `remove` command stubbed but not implemented |

---

### Project Kit (Essential)

| Component | Agent | Status | Location | Notes |
|-----------|-------|--------|----------|-------|
| **`/orient` command** | Claude | ❌ Missing | `kits/project/claude/commands/` | **CRITICAL** - Most important command |
| **`/orient` prompt** | Copilot | ❌ Missing | `kits/project/github/prompts/` | **CRITICAL** |
| **`/review` command** | Claude | ❌ Missing | `kits/project/claude/commands/` | Code review helper |
| **`/review` prompt** | Copilot | ❌ Missing | `kits/project/github/prompts/` | Code review helper |
| **`/audit` command** | Claude | ❌ Missing | `kits/project/claude/commands/` | Security audit |
| **`/audit` prompt** | Copilot | ❌ Missing | `kits/project/github/prompts/` | Security audit |
| **`/stats` command** | Claude | ❌ Missing | `kits/project/claude/commands/` | Project stats |
| **`/stats` prompt** | Copilot | ❌ Missing | `kits/project/github/prompts/` | Project stats |
| **Enhanced scripts** | Bash | ❌ Missing | `kits/project/scripts/bash/` | Custom feature numbering |
| **Enhanced scripts** | PowerShell | ❌ Missing | `kits/project/scripts/powershell/` | Custom feature numbering |

**Priority**: `/orient` is **CRITICAL** - should be first implementation.

---

### Git Kit (Workflow)

| Component | Agent | Status | Location | Notes |
|-----------|-------|--------|----------|-------|
| **`/commit` command** | Claude | ❌ Missing | `kits/git/claude/commands/` | Smart commits + attribution |
| **`/commit` prompt** | Copilot | ❌ Missing | `kits/git/github/prompts/` | Smart commits + attribution |
| **`/pr` command** | Claude | ❌ Missing | `kits/git/claude/commands/` | PR creation helper |
| **`/pr` prompt** | Copilot | ❌ Missing | `kits/git/github/prompts/` | PR creation helper |
| **`/sync` command** | Claude | ❌ Missing | `kits/git/claude/commands/` | Sync status + ASCII viz |
| **`/sync` prompt** | Copilot | ❌ Missing | `kits/git/github/prompts/` | Sync status + ASCII viz |
| **`/cleanup` command** | Claude | ❌ Missing | `kits/git/claude/commands/` | Branch/worktree cleanup |
| **`/cleanup` prompt** | Copilot | ❌ Missing | `kits/git/github/prompts/` | Branch/worktree cleanup |

**Priority**: `/commit` with attribution is most valuable first.

---

### Multiagent Kit (Coordination)

| Component | Status | Location | Notes |
|-----------|--------|----------|-------|
| **PR workflow guide** | ✅ Complete | `kits/multiagent/memory/` | How agents create PRs |
| **Git worktrees protocol** | ✅ Complete | `kits/multiagent/memory/` | Parallel development |
| **Collaboration structure** | ❌ Missing | `kits/multiagent/templates/` | Template for `specs/NNN/collaboration/` |
| **Session log template** | ❌ Missing | `kits/multiagent/templates/` | Individual work sessions |
| **Handoff template** | ❌ Missing | `kits/multiagent/templates/` | Agent-to-agent handoffs |
| **Status template** | ❌ Missing | `kits/multiagent/templates/` | Current status summaries |

**Priority**: Collaboration structure template is most important.

---

## 🎯 Critical Path: What to Build First

### Phase 1: Essential Foundation (MVP) ⭐

**Goal**: Get basic install working with most important command

1. **`/orient` command** (project-kit)
   - File: `kits/project/claude/commands/orient.md`
   - File: `kits/project/github/prompts/orient.prompt.md`
   - **Why critical**: Every agent needs this at start of session
   - **Estimated effort**: 2-3 hours

2. **Installer template system** (core)
   - Update `installer.py` to copy from `kits/` structure
   - Test installation to vanilla project
   - **Why critical**: Without this, nothing installs
   - **Estimated effort**: 1-2 hours

3. **Kit selection logic** (core)
   - Implement `--kit=project,git,multiagent` selection
   - Auto-install dependencies (multiagent → project + git)
   - **Why critical**: User experience
   - **Estimated effort**: 1 hour

**MVP Deliverable**: `speckit-ma install --kit=project` → installs `/orient` command

---

### Phase 2: Git Workflow (High Value)

**Goal**: Smart commits with agent attribution

4. **`/commit` command** (git-kit)
   - File: `kits/git/claude/commands/commit.md`
   - File: `kits/git/github/prompts/commit.prompt.md`
   - **Why important**: Core multiagent need - track who coded what
   - **Estimated effort**: 3-4 hours

5. **`/pr` command** (git-kit)
   - File: `kits/git/claude/commands/pr.md`
   - File: `kits/git/github/prompts/pr.prompt.md`
   - **Why important**: PR creation is common workflow
   - **Estimated effort**: 3-4 hours

**Phase 2 Deliverable**: Full git workflow with attribution

---

### Phase 3: Multiagent Structure (Coordination)

**Goal**: Templates for multi-agent projects

6. **Collaboration directory template** (multiagent-kit)
   - Create template in `kits/multiagent/templates/`
   - Update installer to create on feature creation
   - **Why important**: Core multiagent coordination
   - **Estimated effort**: 2-3 hours

7. **Document templates** (multiagent-kit)
   - Session log template
   - Handoff document template
   - Status update template
   - **Why important**: Structure for agent communication
   - **Estimated effort**: 2 hours

**Phase 3 Deliverable**: Full multiagent coordination structure

---

### Phase 4: Polish & Extras

8. **`/review`, `/audit`, `/stats`** (project-kit)
9. **`/sync`, `/cleanup`** (git-kit)
10. **Enhanced scripts** (project-kit)
11. **Remove command** (core)
12. **Smart constitution merge** (core)

---

## 🏗️ Integration Architecture

### How Vanilla + Kits Stack

```
┌─────────────────────────────────────────────────┐
│ User Experience Layer                            │
│ • AI Agent (Claude Code / GitHub Copilot)       │
│ • Runs slash commands: /specify, /orient, /pr   │
└────────────┬────────────────────────────────────┘
             │
             │ executes
             ▼
┌─────────────────────────────────────────────────┐
│ Command Layer (Markdown Prompts)                │
│                                                  │
│ Vanilla (Never Modified):                       │
│ • /specify → .claude/commands/specify.md        │
│ • /plan    → .claude/commands/plan.md           │
│ • /tasks   → .claude/commands/tasks.md          │
│                                                  │
│ Our Add-ons (New Files):                        │
│ • /orient  → .claude/commands/orient.md    ⭐   │
│ • /commit  → .claude/commands/commit.md         │
│ • /pr      → .claude/commands/pr.md             │
└────────────┬────────────────────────────────────┘
             │
             │ calls
             ▼
┌─────────────────────────────────────────────────┐
│ Script Layer (Shell Execution)                  │
│                                                  │
│ Vanilla (Never Modified):                       │
│ • create-new-feature.sh                         │
│ • setup-plan.sh                                 │
│ • check-prerequisites.sh                        │
│                                                  │
│ Our Add-ons (New Files):                        │
│ • create-feature-enhanced.sh                    │
└────────────┬────────────────────────────────────┘
             │
             │ creates/modifies
             ▼
┌─────────────────────────────────────────────────┐
│ Project Structure Layer                         │
│                                                  │
│ Vanilla (Never Modified):                       │
│ • specs/NNN-feature/spec.md                     │
│ • specs/NNN-feature/plan.md                     │
│ • specs/NNN-feature/tasks.md                    │
│ • .specify/memory/constitution.md               │
│                                                  │
│ Our Add-ons (New Files):                        │
│ • .specify/memory/pr-workflow-guide.md          │
│ • .specify/memory/git-worktrees-protocol.md     │
│ • specs/NNN-feature/collaboration/              │
│   ├── active/                                   │
│   ├── archive/                                  │
│   └── results/                                  │
└─────────────────────────────────────────────────┘
```

### Installation Flow

```
User runs: speckit-ma install --recommended
                    │
                    ▼
            ┌──────────────┐
            │ CLI (cli.py) │
            └──────┬───────┘
                   │
                   ▼
        ┌──────────────────────┐
        │ Installer            │
        │ (installer.py)       │
        └──────┬───────────────┘
               │
               ├─ 1. Detect interfaces (Claude/Copilot)
               ├─ 2. Select kits (project + git)
               ├─ 3. Copy templates from kits/
               └─ 4. Create new files only
                      │
                      ▼
        ┌─────────────────────────────────┐
        │ Result: Vanilla + Kits          │
        │                                  │
        │ .claude/commands/                │
        │ ├── [vanilla commands] (INTACT) │
        │ ├── orient.md          (NEW)    │
        │ ├── commit.md          (NEW)    │
        │ └── pr.md              (NEW)    │
        │                                  │
        │ .specify/memory/                 │
        │ ├── constitution.md    (INTACT) │
        │ ├── pr-workflow-guide.md (NEW)  │
        │ └── git-worktrees-protocol.md   │
        └─────────────────────────────────┘
```

---

## 🔌 Vanilla Integration Points

### What Vanilla Provides (Baseline)

**Commands** (Don't modify these):
```
.claude/commands/
├── analyze.md        # Analyze spec/plan/tasks
├── clarify.md        # Clarify ambiguities
├── constitution.md   # Update constitution
├── implement.md      # Execute tasks
├── plan.md           # Create plan
├── specify.md        # Create spec
└── tasks.md          # Break into tasks
```

**Scripts** (Don't modify these):
```
.specify/scripts/bash/
├── check-prerequisites.sh
├── common.sh
├── create-new-feature.sh
├── setup-plan.sh
└── update-agent-context.sh
```

**Memory** (Read from, don't modify):
```
.specify/memory/
└── constitution.md   # Project principles (user edits)
```

**Templates** (Don't modify these):
```
.specify/templates/
├── agent-file-template.md
├── plan-template.md
├── spec-template.md
└── tasks-template.md
```

---

### What Our Kits Add (Stacked On Top)

**New Commands** (Install alongside vanilla):
```
.claude/commands/
├── [vanilla commands]  ← UNCHANGED
├── orient.md           ← NEW (project-kit)
├── review.md           ← NEW (project-kit)
├── audit.md            ← NEW (project-kit)
├── stats.md            ← NEW (project-kit)
├── commit.md           ← NEW (git-kit)
├── pr.md               ← NEW (git-kit)
├── sync.md             ← NEW (git-kit)
└── cleanup.md          ← NEW (git-kit)
```

**Enhanced Scripts** (Install alongside vanilla):
```
.specify/scripts/bash/
├── [vanilla scripts]           ← UNCHANGED
└── create-feature-enhanced.sh  ← NEW (project-kit)
```

**New Memory Guides** (Install alongside vanilla):
```
.specify/memory/
├── constitution.md              ← UNCHANGED (vanilla)
├── pr-workflow-guide.md         ← NEW (multiagent-kit)
└── git-worktrees-protocol.md    ← NEW (multiagent-kit)
```

**New Per-Feature Structure** (Created on demand):
```
specs/NNN-feature/
├── spec.md                      ← VANILLA
├── plan.md                      ← VANILLA
├── tasks.md                     ← VANILLA
└── collaboration/               ← NEW (multiagent-kit)
    ├── active/
    ├── archive/
    └── results/
```

---

## 📝 Implementation Checklist

### MVP (Phase 1) - Essential Foundation

- [ ] **Create `/orient` command markdown**
  - [ ] `kits/project/claude/commands/orient.md`
  - [ ] `kits/project/github/prompts/orient.prompt.md`
  - Content: Read docs, check git state, determine role, output concise summary

- [ ] **Update installer for kit structure**
  - [ ] Modify `installer.py` to read from `kits/*/` directories
  - [ ] Implement kit selection (--kit=project,git,multiagent)
  - [ ] Auto-detect agent interface (Claude vs Copilot)
  - [ ] Test: Install project-kit to vanilla project

- [ ] **Test MVP workflow**
  - [ ] Copy vanilla reference to /tmp/test-project
  - [ ] Run: `speckit-ma install --kit=project`
  - [ ] Verify: `/orient` command appears in correct location
  - [ ] Test: Run `/orient` in AI agent, verify output

**Success Criteria**: User can install project-kit and run `/orient` command.

---

### High Value (Phase 2) - Git Workflow

- [ ] **Create `/commit` command**
  - [ ] `kits/git/claude/commands/commit.md`
  - [ ] `kits/git/github/prompts/commit.prompt.md`
  - Content: Analyze changes, generate conventional commit, add attribution

- [ ] **Create `/pr` command**
  - [ ] `kits/git/claude/commands/pr.md`
  - [ ] `kits/git/github/prompts/pr.prompt.md`
  - Content: Analyze commits, generate PR description, create with `gh`

- [ ] **Test git workflow**
  - [ ] Make test changes to project
  - [ ] Run `/commit`, verify smart message generation
  - [ ] Run `/pr`, verify PR creation

**Success Criteria**: Agent can create attributed commits and PRs.

---

### Coordination (Phase 3) - Multiagent Structure

- [ ] **Create collaboration templates**
  - [ ] `kits/multiagent/templates/collaboration-structure/`
  - [ ] `kits/multiagent/templates/session-log.md`
  - [ ] `kits/multiagent/templates/handoff.md`
  - [ ] `kits/multiagent/templates/status.md`

- [ ] **Update installer for templates**
  - [ ] Copy templates to project on install
  - [ ] Create collaboration/ on feature creation

- [ ] **Test multiagent workflow**
  - [ ] Create test feature with collaboration structure
  - [ ] Verify templates are copied correctly
  - [ ] Test handoff workflow between agents

**Success Criteria**: Feature directories have collaboration structure.

---

### Polish (Phase 4) - Remaining Commands

- [ ] Create `/review` command (project-kit)
- [ ] Create `/audit` command (project-kit)
- [ ] Create `/stats` command (project-kit)
- [ ] Create `/sync` command (git-kit)
- [ ] Create `/cleanup` command (git-kit)
- [ ] Create enhanced scripts (project-kit)
- [ ] Implement remove command (core)
- [ ] Implement smart constitution merge (core)

---

## 🚀 User Experience Flow

### First-Time Setup

```bash
# User has vanilla spec-kit project
cd my-vanilla-project

# Install multiagent (includes recommended kits)
pip install spec-kit-multiagent
speckit-ma install --recommended --kit=multiagent

# What gets added (new files only):
# ✅ /orient command
# ✅ /commit command  
# ✅ /pr command
# ✅ PR workflow guide
# ✅ Git worktrees protocol
# ✅ Vanilla spec-kit: UNTOUCHED
```

### Daily Workflow

```bash
# Morning: Start work
/orient                    # NEW: Get oriented (project-kit)
/specify "Add user auth"   # VANILLA: Create spec
/plan                      # VANILLA: Create plan
/tasks                     # VANILLA: Break into tasks

# Work: Implement
/implement                 # VANILLA: Execute tasks

# Git: Commit work
/commit                    # NEW: Smart commit (git-kit)

# Review: Check quality
/review                    # NEW: Code review (project-kit)

# Ship: Create PR
/pr                        # NEW: Create PR (git-kit)
```

### Multi-Agent Workflow

```bash
# Agent 1: Create feature and handoff
/orient
/specify "Blog platform"
/plan
# Creates: specs/003-blog/collaboration/
# Creates handoff in: collaboration/active/decisions/

# Agent 2: Pick up and continue
/orient                    # NEW: Shows handoff available
cd specs/003-blog
# Read: collaboration/active/decisions/handoff-to-copilot.md
# Work on assigned tasks
/commit                    # NEW: Attribution shows it's Agent 2
```

---

## 🎯 Summary: Build Priority

**Critical (Do First)**:
1. ⭐ `/orient` command (project-kit) - Most essential
2. ⭐ Installer kit structure (core) - Makes everything work
3. ⭐ `/commit` command (git-kit) - Agent attribution

**High Value (Do Next)**:
4. `/pr` command (git-kit)
5. Collaboration templates (multiagent-kit)

**Nice to Have (Do Later)**:
6. `/review`, `/audit`, `/stats` (project-kit)
7. `/sync`, `/cleanup` (git-kit)
8. Enhanced scripts (project-kit)

**Total Estimated Effort**: 
- MVP (Phase 1): ~4 hours
- High Value (Phase 2): ~8 hours
- Coordination (Phase 3): ~5 hours
- **Working system**: ~17 hours
- Polish (Phase 4): +10 hours

---

## ✨ Key Architectural Decisions

### ✅ Good Decisions Already Made

1. **Add-on pattern** - Never modify vanilla (version-safe)
2. **Cross-agent support** - Works with Claude + Copilot
3. **Cross-platform** - Supports Bash + PowerShell
4. **Modular kits** - Install what you need
5. **Pip-installable** - Easy distribution

### 🎯 Decisions Needed

1. **Template location**: Store in `kits/*/templates/` or separate?
   - **Recommendation**: Keep in `kits/*/` for modularity

2. **Constitution merge**: When to implement smart merge vs manual?
   - **Recommendation**: Phase 4, not critical for MVP

3. **Collaboration auto-creation**: On install or on first `/specify`?
   - **Recommendation**: On first feature creation (lazy)

4. **Command format**: Use vanilla style or innovate?
   - **Recommendation**: Match vanilla style for consistency

---

**Current Status**: 
- Core CLI: ✅ Working
- Kits: ❌ Empty shells (READMEs only)
- **Next Step**: Implement `/orient` command + update installer
- **MVP Blockers**: None - ready to build!