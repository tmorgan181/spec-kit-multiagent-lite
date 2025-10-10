# Lite-Kits Wishlist - Prioritized

**Source**: Trenton's brain dump 2025-10-09
**Status**: Needs review and selection

---

## 🔥 CRITICAL (Do First - v0.2.0)

### 1. Kit Consolidation Strategy
**Problem**: Project kit and git kit overlap. Good project ops requires git anyway.
**Decision needed**:
- Merge project + git into single kit?
- Keep separate but make git a dependency of project?
- Keep independent but allow file overlap?

**Impact**: Affects entire architecture, installer logic, user experience

**Questions**:
- Can they have overlapping files? (Currently: no)
- Should we combine since good project ops requires git? (Probably yes)
- How do we ensure compatibility if kept separate?

**Recommendation**:
- **Merge for v1.0** - Call it "dev-kit" or keep "project-kit" but include git commands
- Most users want both anyway (--recommended installs both)
- Simpler mental model: project kit = everything you need for solo dev
- Multiagent kit stays separate (truly optional for coordination)

---

## 🚨 HIGH PRIORITY (Fix Before v1.0)

### 2. Validation & Status Robustness
**Problem**: Current validation doesn't account for partial/corrupted/missing kit files
**Needs**:
- ✅ Check for complete kit installation (all expected files present)
- ✅ Detect partial installs (some files missing)
- ✅ Detect corrupted files (empty, malformed)
- ✅ Status command shows health of each kit
- ✅ Validation suggests fixes ("Run: lite-kits add --kit project to repair")

**Files to update**:
- `src/lite_kits/core/installer.py::validate()`
- Add new `status` command to CLI
- Add file integrity checks (size > 0, contains expected markers)

---

### 3. Add/Remove Guardrails & DX
**Problem**: Add command can overwrite files, unclear messaging, no guardrails
**Needs**:
- ✅ Check for existing files before adding
- ✅ Don't add if already installed properly
- ✅ Confirm before overwriting
- ✅ Better error messages: "Did you mean --kit project?"
- ✅ Dry-run improvements (show what files will be created/modified/skipped)
- ✅ Handle edge cases (empty directories, partial installs)

**Specific fixes**:
```bash
# Current: Just installs, might overwrite
lite-kits add --kit project

# Better:
# - Check if project-kit already exists → skip with message
# - Check if files conflict → ask for confirmation
# - Check if directory is wrong → suggest correct usage
```

---

### 4. CLI Output Standardization
**Problem**: Inconsistent status indicators, emojis everywhere, unclear messages
**Needs**:
- ✅ Standardize status indicators:
  - `[OK]` (green) for success
  - `[FAIL]` (red) for errors
  - `[WARN]` (yellow) for warnings
- ✅ Emojis ONLY for summaries/human-readable messages (not status lines)
- ✅ Clear messaging about what's happening where
- ✅ Explicit about directory targets
- ✅ Better help messages and option descriptions

**Files to update**:
- `src/lite_kits/cli.py` (all commands)
- Remove emoji from status checks
- Add emoji only to final summaries

---

### 5. Banner Placement
**Problem**: Banner shows after successful addition (annoying)
**Fix**: Remove `show_static_banner()` call after `installer.install()` success

**File**: `src/lite_kits/cli.py::add_kits()` line ~229

---

## 📋 MEDIUM PRIORITY (Nice to Have)

### 6. Agent & Shell Preferences
**Problem**: Can't specify which agent (Claude/Copilot) or shell (bash/pwsh) to install for
**Idea**: Support explicit preferences with auto-detection and proposals

**Proposed UX**:
```bash
# Specify agent preference
lite-kits add --kit dev --agent claude     # Only .claude/commands/
lite-kits add --kit dev --agent copilot    # Only .github/prompts/
lite-kits add --kit dev --agent both       # Both (default if both dirs exist)

# Specify shell preference (for scripts - future)
lite-kits add --kit dev --shell bash       # Only bash scripts
lite-kits add --kit dev --shell pwsh       # Only PowerShell scripts
lite-kits add --kit dev --shell both       # Both (default)

# Auto-detect and propose
lite-kits add --kit dev
# Detects: .claude/ exists, .github/prompts/ missing
# Proposes: "Installing for Claude Code only (detected .claude/)"
# Confirms: "Also install for GitHub Copilot? [y/N]"
```

**Status**: Already auto-detects! Just needs:
- Explicit flags for user control (`--agent`, `--shell`)
- Better messaging about what was detected
- Confirmation prompts when adding new agent support

**Recommendation**: Add in v0.3.0 (after kit merge)

---

### 7. Git Status Script/Command
**Problem**: Claude runs multiple git commands to check status (inefficient)
**Idea**: Add `/status` command to git-kit with optimized git checks

**Implementation**:
- Single bash/powershell script that runs all git checks efficiently
- Output structured data for AI parsing
- Include in git-kit

**Example**:
```bash
/status
# Outputs:
# Branch: develop
# Commits behind origin: 2
# Uncommitted changes: 5 files
# Untracked files: 3
# Last commit: 2 hours ago
```

**Recommendation**: Add in v0.3.0 after kit consolidation

---

## 🔍 RESEARCH (Needs Investigation)

### 8. Command Audit
**Action**: Actually read what the project commands do
**Commands to review**:
- `/orient` - Agent orientation protocol
- `/review` - Code review helper (moved to git-kit)
- `/audit` - Security audit (not implemented)
- `/stats` - Project statistics (not implemented)

**Outcome**: Fine-tune prompts, add missing scripts, ensure quality

---

### 9. Script Standardization
**Problem**: Claude runs lots of individual tool calls instead of scripts
**Action**:
- Review all kit commands
- Identify repetitive multi-step operations
- Create reusable scripts for common patterns
- Update command prompts to use scripts

**Example patterns to script**:
- Git status checks (branch, commits, changes, untracked)
- Project info gathering (stack, conventions, recent work)
- Multi-agent coordination checks (sessions, handoffs)

---

## 🎯 STRATEGIC DECISIONS NEEDED

### A. Kit Architecture
**Current**: 3 kits (project, git, multiagent)
**Decision**: ✅ **APPROVED - Merge to 2 kits** (dev-kit [project+git merged], multiagent-kit)

**Rationale**:
- Good project ops requires git anyway
- Most users want both (--recommended installs both currently)
- Simpler mental model
- Cleaner architecture (no overlap questions)

**New structure**:
- **dev-kit**: Solo development essentials (/orient, /commit, /pr, /review, /cleanup)
- **multiagent-kit**: Multi-agent coordination (/sync, collaboration dirs, memory guides)

**Name**: "dev-kit" (catchier than "project-kit", avoids ADO/PM confusion)

### B. Agent Support Strategy
**Current**: Claude Code + GitHub Copilot (dual support, auto-detect)
**Decision**: ✅ **APPROVED - Keep both, focus polish on Copilot CLI**

**What this means**:
- ✅ Keep Claude Code support (already built, working, no reason to remove)
- ✅ Keep dual installation (`.claude/` and `.github/prompts/`)
- ✅ Keep auto-detection
- 🎯 **Prioritize** Copilot CLI workflows for testing
- 🎯 **Document** Copilot CLI as primary use case
- 🎯 **Polish** Copilot CLI UX first

**Marketing**: "Lite-kits enhances GitHub Spec-Kit for Copilot CLI users. Also works with Claude Code."

### C. Scope for v1.0
**Current plan**:
- Fix critical issues (#2-5 above)
- Ship to PyPI
- Polish later

**Alternative**:
- Fix everything (#2-9)
- Perfect v1.0
- Ship in 2-3 weeks

**Decision**: Trenton to choose (probably former)

---

## 📝 NEXT STEPS

1. **Trenton reviews this doc** and picks priorities
2. **Create issues** for selected items
3. **Implement in order**:
   - Critical items first
   - High priority next
   - Medium/Research as time allows

4. **Ship v0.2.0** when critical items are done
5. **Ship v1.0** when high priority items are done

---

## IMMEDIATE ACTION ITEMS

For next work session:

1. ✅ **Decide on kit consolidation** (merge project+git or keep separate?)
2. ✅ **Review command prompts** (what do they actually do?)
3. ✅ **Implement validation robustness** (detect partial/corrupted kits)
4. ✅ **Standardize CLI output** (OK/FAIL/WARN, no emoji spam)
5. ✅ **Add guardrails to add command** (check existing, confirm overwrites)

Pick 1-2 to start with!
