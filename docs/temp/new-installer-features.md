# New Installer Features Summary

## Completed ✅

### 1. Zero Hardcoded Identifiers
- All kit names from manifest
- All agent detection from manifest
- All shell detection from manifest
- Spec-kit markers from manifest
- Options/defaults from manifest

### 2. Guardrails & Safety
- `check_conflicts()` - Detects file overwrites before install
- `skip_existing` option - Don't overwrite by default
- `--force` flag - Skip confirmations
- Detailed conflict reporting (file paths, sizes)

### 3. Dry-Run Support
- `--dry-run` flag - Preview without changes
- `preview_installation()` - Detailed preview
- Shows new files, modified files, new directories
- Shows detected agents/shells
- Works for both install and remove

### 4. Agent & Shell Preferences
- `--agent claude|copilot` - Install for specific agent only
- `--shell bash|powershell` - Install scripts for specific shell
- Auto-detection when not specified
- Validates against manifest (supported agents/shells)

### 5. Enhanced Validation
- `validate()` - Check all installed kits
- Detects missing files
- Detects corrupted files (file size < min_size)
- Status tracking: `installed`, `partial`, `not_installed`
- Detailed repair suggestions

## To Add 🚧

### 6. Diff Checking in Validate

Add to `validate()`:

```python
def validate(self) -> Dict:
    # ... existing code ...

    if kit_installed:
        all_files = self.manifest.get_kit_files(kit_name, agent=None)

        missing_files = []
        corrupted_files = []
        outdated_files = []  # NEW

        for file_info in all_files:
            # ... existing checks ...

            # NEW: Check if file differs from source
            source_path = self.kits_dir / file_info['source']
            if source_path.exists() and target_path.exists():
                try:
                    source_content = source_path.read_text()
                    target_content = target_path.read_text()

                    if source_content != target_content:
                        outdated_files.append({
                            'path': file_info['path'],
                            'source': file_info['source'],
                            'diff': True  # Could add actual diff later
                        })
                except Exception:
                    pass

        # Update status message
        if missing_files or corrupted_files or outdated_files:
            status = "partial"
            issues = []
            if missing_files:
                issues.append(f"{len(missing_files)} missing")
            if corrupted_files:
                issues.append(f"{len(corrupted_files)} corrupted")
            if outdated_files:
                issues.append(f"{len(outdated_files)} outdated")
            message = f"{kit_info['name']}: {', '.join(issues)} - run: lite-kits add --kit {kit_name} --upgrade"
```

### 7. Upgrade Mode

Add to `__init__`:

```python
def __init__(
    self,
    # ... existing params ...
    upgrade: bool = False,  # NEW
):
    # ...
    self.upgrade = upgrade
```

Add logic to `install()`:

```python
def install(self) -> Dict:
    # ...

    # In upgrade mode, treat outdated files like conflicts
    if self.upgrade:
        # Check validation first
        validation = self.validate()

        outdated = []
        for kit_name, check in validation['checks'].items():
            if 'outdated_files' in check:
                outdated.extend(check['outdated_files'])

        # Force install outdated files
        for file_info in outdated:
            self._install_file(file_info['source'], file_info['path'])
            result["upgraded"].append(file_info['path'])

    # ... rest of install logic
```

**Usage:**
```bash
# Check for outdated files
lite-kits validate

# Upgrade outdated files only
lite-kits add --kit dev --upgrade

# Force upgrade all files
lite-kits add --kit dev --upgrade --force
```

## All Flags Summary

```bash
lite-kits add [--kit <name>] [OPTIONS]

Options:
  --kit <name>         Kit to install (default: dev)
  --recommended        Install recommended kits
  --dry-run            Preview without making changes
  --force              Skip confirmations, overwrite existing
  --upgrade            Update outdated files to latest versions
  --agent <name>       Install for specific agent (claude|copilot)
  --shell <name>       Install scripts for specific shell (bash|powershell)

Examples:
  lite-kits add --recommended              # Install dev-kit (recommended)
  lite-kits add --kit multiagent           # Install multiagent-kit
  lite-kits add --dry-run                  # Preview installation
  lite-kits add --force                    # Overwrite existing files
  lite-kits add --upgrade                  # Upgrade outdated files
  lite-kits add --agent claude             # Claude Code only
  lite-kits add --shell bash               # Bash scripts only
  lite-kits add --kit dev --agent copilot  # Dev-kit for Copilot only
```

## Implementation Status

- ✅ installer_v2.py created (687 lines)
- 🚧 Add diff checking to validate()
- 🚧 Add upgrade mode to install()
- ⏸️ Replace old installer.py
- ⏸️ Update CLI with new flags
- ⏸️ Test all features

**Current time:** 9:45 PM
**Estimated completion:** 10:30 PM (45 mins)

We're shipping tonight! 🚀
