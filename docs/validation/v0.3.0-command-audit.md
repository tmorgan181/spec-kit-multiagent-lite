# Command Audit Findings - v0.3

**Date**: 2025-10-10
**Auditor**: claude-sonnet-4.5 @ Claude Code

---

## 🔍 Issues Found

### Critical: Outdated Kit References
**Impact**: HIGH - Commands reference old "project-kit" and "git-kit" names

**Files affected**: 22 files across all kits

**Problem**: After v0.2.0 consolidation (project + git → dev), many files still reference old names:
- "project-kit" → should be "dev-kit"
- "git-kit" → should be "dev-kit"
- Detection logic checks for wrong marker files

**Examples**:
- `orient.md`: Lines 20-22 check for `.claude/commands/commit.md` (correct) but label it "git" (wrong - should be "dev")
- Multiple README files still describe old kit structure
- `/sync` command references git-kit

**Fix required**: Global find-replace:
- `project-kit` → `dev-kit`
- `git-kit` → `dev-kit`
- `project ` → `dev ` (in kit detection outputs)
- `git ` → (remove, it's all dev now)

---

## 📋 Detailed File Review

### Dev-Kit Commands (.claude/)

#### 1. ✅ audit.md
- **Status**: Needs review for minimalism
- **Issues**: None obvious, appears clean

#### 2. ⚠️ cleanup.md
- **Status**: References to check
- **Issues**: May reference "git-kit" in examples

#### 3. ⚠️ commit.md
- **Status**: References to check
- **Issues**: Likely mentions "git-kit"

#### 4. ⚠️ orient.md
- **Status**: OUTDATED KIT NAMES
- **Issues**:
  - Lines 20-22: Labels kits as "project" and "git" (should be "dev")
  - Line 134: Example shows "project, git" (should be "dev")
  - Line 119: References "/commit (if git-kit installed)" (should be "dev-kit")

#### 5. ⚠️ pr.md
- **Status**: References to check
- **Issues**: Likely mentions "git-kit"

#### 6. ⚠️ review.md
- **Status**: References to check
- **Issues**: Likely mentions "project-kit" or "git-kit"

#### 7. ⚠️ stats.md
- **Status**: References to check
- **Issues**: Likely mentions "project-kit"

### Multiagent-Kit Commands

#### 8. ⚠️ sync.md
- **Status**: References to check
- **Issues**: Likely references "project-kit" and "git-kit"

---

## 🔧 Fixes Required

### 1. Global Find-Replace (22 files)

**Pattern 1**: `project-kit` → `dev-kit`
**Pattern 2**: `git-kit` → `dev-kit`
**Pattern 3**: In kit detection outputs:
- `"project "` → `"dev "`
- `"git "` → (remove or merge into dev)

### 2. Specific File Fixes

**orient.md** (both .claude and .github versions):
```bash
# OLD (lines 20-22):
[ -f .claude/commands/orient.md ] && KITS_INSTALLED="${KITS_INSTALLED}project "
[ -f .claude/commands/commit.md ] && KITS_INSTALLED="${KITS_INSTALLED}git "

# NEW:
[ -f .claude/commands/orient.md ] && KITS_INSTALLED="${KITS_INSTALLED}dev "
# (remove the commit.md check - redundant, both in dev-kit)
```

**Example outputs** (line 134):
```
# OLD:
**Installed Kits**: project, git

# NEW:
**Installed Kits**: dev
```

### 3. README Updates

Update all README files in kit directories to reflect current structure.

---

## ✅ Quality Checks Passed

- **Minimalist design**: Commands are concise, no obvious bloat
- **Clear instructions**: Step-by-step execution patterns
- **Good examples**: Practical, helpful examples included
- **Error handling**: Graceful handling of missing files/commands

---

## 📊 Summary

**Total files audited**: 22
**Issues found**: 1 major (outdated kit references)
**Files needing fixes**: 22
**Est. fix time**: 20-30 min (global find-replace + verification)

**Recommendation**: Fix all outdated references before v0.3 release to avoid user confusion.

---

## 🚀 Action Plan

1. ✅ Create this audit report
2. ⏳ Execute global find-replace for kit name updates
3. ⏳ Verify detection logic in orient.md
4. ⏳ Update README files
5. ⏳ Test commands after fixes
6. ⏳ Commit with clear message
