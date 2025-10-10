# Manifest-Driven Kit System - Implementation Summary

**Date**: 2025-10-09
**Status**: Work in Progress
**Branch**: `feature/merge-kits-to-dev-kit`

## What We Built

### 1. Kit Manifest (`src/lite_kits/kits/kits.yaml`)

Central source of truth for all kit definitions:
- Kit metadata (name, description, icon, recommended status)
- Command lists with status (stable/planned)
- File mappings (source → target for each agent)
- Marker files for detection
- Agent configurations
- Installation options

**Benefits**:
- No hardcoded kit logic in installer
- Easy to add new kits (just edit YAML)
- Easy to add new commands (just add to manifest + files)
- Validation can check against manifest
- Single source of truth

### 2. Manifest Loader (`src/lite_kits/core/manifest.py`)

Python class that loads and provides access to manifest data:

```python
from lite_kits.core import KitManifest

manifest = KitManifest(kits_dir)

# Get kit info
kit = manifest.get_kit('dev')
files = manifest.get_kit_files('dev', agent='claude')
markers = manifest.get_kit_markers('dev')
commands = manifest.get_kit_commands('dev')

# Get all kits
all_kits = manifest.get_all_kits()
recommended = manifest.get_recommended_kits()
```

### 3. Dev Kit (`src/lite_kits/kits/dev/`)

Merged project-kit + git-kit into unified dev-kit:

**Commands (7 total)**:
- `/orient` - Agent orientation (from project-kit)
- `/audit` - Security audit (from project-kit, planned)
- `/stats` - Project stats (from project-kit, planned)
- `/commit` - Smart commit (from git-kit)
- `/pr` - Pull request (from git-kit)
- `/review` - Code review (from git-kit)
- `/cleanup` - Branch cleanup (from git-kit)

**Structure**:
```
dev/
├── README.md
├── claude/commands/
│   ├── orient.md
│   ├── commit.md
│   ├── pr.md
│   ├── review.md
│   ├── cleanup.md
│   ├── audit.md
│   └── stats.md
└── github/prompts/
    ├── orient.prompt.md
    ├── commit.prompt.md
    ├── pr.prompt.md
    ├── review.prompt.md
    ├── cleanup.prompt.md
    ├── audit.prompt.md
    └── stats.prompt.md
```

### 4. Updated Dependencies

Added `pyyaml>=6.0.0` to `pyproject.toml` for manifest loading.

### 5. Updated CLI Constants

Changed kit names from `project`, `git`, `multiagent` → `dev`, `multiagent`

## What's Left

### Next Session Work

1. **Refactor Installer** (`src/lite_kits/core/installer.py`)
   - Replace hardcoded kit logic with manifest lookups
   - Use `manifest.get_kit_files()` for installation
   - Use `manifest.get_kit_markers()` for detection
   - Use `manifest.get_kit_commands()` for validation

2. **Update CLI** (`src/lite_kits/cli.py`)
   - Use manifest for kit icons/descriptions
   - Dynamic kit help text from manifest
   - Remove hardcoded kit constants (use manifest)

3. **Enhanced Validation**
   - Check all files from manifest exist
   - Check file integrity (size > 0, has content)
   - Detect partial installs
   - Suggest repairs

4. **Testing**
   - Test dev-kit installation
   - Test multiagent-kit installation
   - Test validation with missing files
   - Test dry-run with manifest

### Future Enhancements

- **Agent preferences**: `--agent claude/copilot/both` flag
- **Shell preferences**: `--shell bash/pwsh/both` flag
- **Custom kit support**: Load kits from custom locations
- **Kit versioning**: Track kit versions in manifest
- **Kit dependencies**: Express kit dependencies in manifest

## How This Changes Development

### Before (Hardcoded):
```python
# In installer.py
if 'project' in self.kits:
    self._install_file('project/claude/commands/orient.md', '.claude/commands/orient.md')
    # ... 10 more hardcoded lines
```

### After (Manifest-Driven):
```python
# In installer.py
for file in manifest.get_kit_files(kit_name, agent='claude'):
    self._install_file(file['source'], file['path'])
```

### Benefits:
- Add new kits: Edit YAML, no code changes
- Add new commands: Add file + update YAML
- Change file paths: Edit YAML
- Validation: Check against manifest
- Status: Show info from manifest

## Migration Path

1. Keep old `project/` and `git/` dirs temporarily
2. Support both old and new names in CLI (aliases)
3. Show deprecation warnings for old names
4. Remove old dirs in v0.3.0

Or just:
1. Complete refactor now
2. Delete old dirs
3. Ship v0.2.0 with breaking change

## Files Changed

- ✅ `src/lite_kits/kits/kits.yaml` (new)
- ✅ `src/lite_kits/core/manifest.py` (new)
- ✅ `src/lite_kits/kits/dev/` (new)
- ✅ `pyproject.toml` (added pyyaml)
- ✅ `src/lite_kits/cli.py` (updated constants)
- ✅ `src/lite_kits/core/__init__.py` (export KitManifest)
- 🚧 `src/lite_kits/core/installer.py` (started, needs completion)

## Decision Points

**Trenton needs to decide:**

1. **Migration strategy**: Breaking change now or backward compat?
2. **Testing approach**: Manual test before commit or commit WIP?
3. **Timeline**: Finish refactor now (2 hours) or next session?

## Recommendation

**Commit this as WIP**, then in next session:
1. Finish installer refactor (1-2 hours)
2. Test thoroughly
3. Delete old kit dirs
4. Update main README
5. Ship as v0.2.0

This gives you a clean checkpoint and lets you test the manifest system before fully committing.
