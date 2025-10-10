# Kit Merge Implementation Plan

**Goal**: Merge `project-kit` and `git-kit` into unified `dev-kit`

## Status: IN PROGRESS

### ✅ Completed
1. Created `src/lite_kits/kits/dev/` directory
2. Copied all 7 commands to dev-kit:
   - orient, audit, stats (from project)
   - commit, pr, review, cleanup (from git)
3. Created dev-kit README.md
4. Updated CLI constants (`cli.py`):
   - KIT_DEV, KIT_MULTIAGENT
   - KITS_ALL, KITS_RECOMMENDED
   - Descriptions
5. Started installer updates (`installer.py`)

### 🚧 Remaining Work

#### 1. Complete Installer Refactor (`src/lite_kits/core/installer.py`)

**Methods that need updating:**

```python
# Line 21: Update docstring
- kits: List of kits to install (project, git, multiagent). Defaults to ['project']
+ kits: List of kits to install (dev, multiagent). Defaults to ['dev']

# Line 49-77: is_multiagent_installed()
markers = {
    'project': [...],  # DELETE
    'git': [...],      # DELETE
    'dev': [           # ADD
        self.target_dir / ".claude" / "commands" / "orient.md",
        self.target_dir / ".github" / "prompts" / "orient.prompt.md",
    ],
    'multiagent': [...],
}

# Line 79-132: preview_installation()
- if 'project' in self.kits: ...  # DELETE
- if 'git' in self.kits: ...      # DELETE
+ if 'dev' in self.kits:          # ADD
    if has_claude:
        changes["new_files"].extend([
            ".claude/commands/orient.md",
            ".claude/commands/commit.md",
            ".claude/commands/pr.md",
            ".claude/commands/review.md",
            ".claude/commands/cleanup.md",
            ".claude/commands/audit.md",
            ".claude/commands/stats.md",
        ])
    if has_copilot:
        # Same for .github/prompts/*.prompt.md

# Line 134-218: install()
- if 'project' in self.kits: ...  # DELETE
- if 'git' in self.kits: ...      # DELETE
+ if 'dev' in self.kits:          # ADD
    if has_claude:
        self._install_file('dev/claude/commands/orient.md', '.claude/commands/orient.md')
        self._install_file('dev/claude/commands/commit.md', '.claude/commands/commit.md')
        # ... all 7 commands
        result["installed"].append("dev-kit (Claude): /orient, /commit, /pr, /review, /cleanup, /audit, /stats")
    if has_copilot:
        # Same for Copilot

# Line 220-272: validate()
- checks["project_kit"] = {...}  # DELETE
- checks["git_kit"] = {...}      # DELETE
+ checks["dev_kit"] = {          # ADD
    "passed": dev_kit_installed,
    "message": "dev-kit: all commands found" if dev_kit_installed
              else "dev-kit not installed - run: lite-kits add --kit dev",
}

# Line 326-437: remove()
- if 'project' in self.kits: ...  # DELETE
- if 'git' in self.kits: ...      # DELETE
+ if 'dev' in self.kits:          # ADD
    removed = []
    dev_commands = ['orient', 'commit', 'pr', 'review', 'cleanup', 'audit', 'stats']
    # Remove logic
```

#### 2. Update CLI Display Functions (`src/lite_kits/cli.py`)

**Functions that reference kits:**

```python
# Line ~70-90: print_kit_info()
kit_icons = {
    "project": "🎯",   # DELETE
    "git": "🔧",        # DELETE
    "dev": "🚀",        # ADD
    "multiagent": "🤝"
}

# Anywhere else that shows kit names
```

#### 3. Delete Old Kit Directories

Once installer is updated and tested:
```bash
rm -rf src/lite_kits/kits/project/
rm -rf src/lite_kits/kits/git/
```

#### 4. Update Main README.md

Replace all references to `project-kit` and `git-kit` with `dev-kit`.

#### 5. Update Examples (if any)

Check `examples/` directory for any kit references.

#### 6. Update Tests (when they exist)

Update any tests that reference old kit names.

---

## Estimation

- **Installer refactor**: 30-45 minutes (tedious but straightforward)
- **CLI updates**: 10 minutes
- **README updates**: 15 minutes
- **Testing**: 30 minutes
- **Total**: ~2 hours

---

## Alternative Approach

If the full refactor is too complex right now, we could:

1. **Keep backward compatibility** - Support both old and new names temporarily
2. **Alias** - Make `project` and `git` aliases for `dev`
3. **Deprecation path** - Warn when using old names, auto-map to new

This would allow:
```bash
lite-kits add --kit project  # Works, installs dev-kit, shows deprecation warning
lite-kits add --kit dev      # Preferred new way
```

---

## Decision Needed

**Option A**: Complete the refactor now (2 hours of work)
**Option B**: Add backward compat aliases (30 minutes), refactor later
**Option C**: Pause, merge what we have, document for later

What's your preference?
