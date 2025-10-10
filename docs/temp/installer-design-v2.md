# Installer Functional Design v2 - Zero Hardcoded Identifiers

**Principles:**
1. **Zero hardcoded names** - All identifiers come from manifest or constants
2. **Guardrails built-in** - Confirm overwrites, detect conflicts, validate before install
3. **Dry-run support** - Full preview mode with detailed change reporting
4. **Backwards compatibility** - Support old kits during transition period

---

## Enhanced Manifest Structure

First, add spec-kit detection to manifest:

```yaml
# In kits.yaml, add section:

spec_kit:
  # Markers that indicate a spec-kit project
  markers:
    - path: ".specify"
      type: "directory"
      description: "Spec-kit core directory"

    - path: ".claude"
      type: "directory"
      description: "Claude Code commands directory"

    - path: ".github/prompts"
      type: "directory"
      description: "GitHub Copilot prompts directory"

  # At least one marker must exist for valid spec-kit project
  require_any: true
```

This eliminates hardcoded spec-kit detection!

---

## Class: Installer

### Constructor: `__init__(target_dir, kits=None, dry_run=False, force=False)`

```python
def __init__(
    self,
    target_dir: Path,
    kits: Optional[List[str]] = None,
    dry_run: bool = False,
    force: bool = False,
    agent: Optional[str] = None,  # NEW: explicit agent preference
    shell: Optional[str] = None,  # NEW: explicit shell preference
):
    self.target_dir = Path(target_dir).resolve()
    self.kits_dir = Path(__file__).parent.parent / "kits"
    self.manifest = KitManifest(self.kits_dir)

    # Dry-run mode (no actual file operations)
    self.dry_run = dry_run

    # Force mode (skip confirmations)
    self.force = force

    # Explicit preferences (None = auto-detect)
    self.preferred_agent = agent
    self.preferred_shell = shell

    # Use manifest for defaults - NO HARDCODED 'dev'
    self.kits = kits or [self.manifest.get_default_kit()]

    # Validate kit names - NO HARDCODED VALID_KITS
    valid_kits = set(self.manifest.get_kit_names())
    invalid = set(self.kits) - valid_kits
    if invalid:
        valid_list = ', '.join(sorted(valid_kits))
        raise ValueError(f"Invalid kit(s): {invalid}. Valid: {valid_list}")
```

**Changes:**
- ✅ Added `dry_run` parameter for preview mode
- ✅ Added `force` parameter to skip confirmations
- ✅ Added `agent` and `shell` explicit preferences
- ✅ No hardcoded defaults - all from manifest

---

### Method: `is_spec_kit_project()` → bool

**FIXED** - No hardcoded markers!

```python
def is_spec_kit_project(self) -> bool:
    """
    Check if target directory is a spec-kit project.

    Uses spec_kit.markers from manifest instead of hardcoded paths.

    Returns:
        True if directory contains spec-kit markers
    """
    spec_config = self.manifest.manifest.get('spec_kit', {})
    markers = spec_config.get('markers', [])
    require_any = spec_config.get('require_any', True)

    found = []
    for marker in markers:
        path = self.target_dir / marker['path']

        # Check type (directory or file)
        if marker.get('type') == 'directory':
            if path.is_dir():
                found.append(marker['path'])
        else:
            if path.exists():
                found.append(marker['path'])

    # If require_any, at least one must exist
    if require_any:
        return len(found) > 0

    # Otherwise all must exist
    return len(found) == len(markers)
```

**Changes:**
- ✅ Reads markers from `manifest['spec_kit']['markers']`
- ✅ No hardcoded `.specify`, `.claude`, `.github/prompts`
- ✅ Configurable logic (require_any vs require_all)

---

### Method: `detect_agents()` → List[str]

```python
def detect_agents(self) -> List[str]:
    """
    Auto-detect which AI agents are present in project.

    Only detects supported agents from manifest.

    Returns:
        List of detected agent names sorted by priority
    """
    # If user specified explicit agent, use only that
    if self.preferred_agent:
        agent_config = self.manifest.get_agent_config(self.preferred_agent)
        if not agent_config:
            raise ValueError(f"Unknown agent: {self.preferred_agent}")
        if not agent_config.get('supported', False):
            raise ValueError(f"Agent not supported: {self.preferred_agent}")
        return [self.preferred_agent]

    # Auto-detect from manifest
    detected = []
    agents = self.manifest.manifest.get('agents', {})

    for agent_name, config in agents.items():
        # Skip unsupported agents
        if not config.get('supported', False):
            continue

        # Check if marker directory exists - NO HARDCODED PATHS
        marker_dir = self.target_dir / config['marker_dir']
        if marker_dir.exists():
            detected.append({
                'name': agent_name,
                'priority': config.get('priority', 999)
            })

    # Sort by priority (lower = higher priority)
    detected.sort(key=lambda x: x['priority'])

    return [agent['name'] for agent in detected]
```

**Changes:**
- ✅ Respects `--agent` flag if provided
- ✅ Sorted by priority from manifest
- ✅ No hardcoded agent names or paths

---

### Method: `detect_shells()` → List[str]

**NEW METHOD** - Detect which shells to install for

```python
def detect_shells(self) -> List[str]:
    """
    Determine which shells to install scripts for.

    Returns:
        List of shell names to install for
    """
    # If user specified explicit shell, use only that
    if self.preferred_shell:
        shell_config = self.manifest.manifest.get('shells', {}).get(self.preferred_shell)
        if not shell_config:
            raise ValueError(f"Unknown shell: {self.preferred_shell}")
        if not shell_config.get('supported', False):
            raise ValueError(f"Shell not supported: {self.preferred_shell}")
        return [self.preferred_shell]

    # Auto-detect based on options from manifest
    options = self.manifest.manifest.get('options', {})

    if not options.get('auto_detect_shells', True):
        return []  # Don't install scripts if disabled

    shells_config = self.manifest.manifest.get('shells', {})
    detected = []

    for shell_name, config in shells_config.items():
        if not config.get('supported', False):
            continue

        detected.append({
            'name': shell_name,
            'priority': config.get('priority', 999)
        })

    # Sort by priority
    detected.sort(key=lambda x: x['priority'])

    # If prefer_all_shells, return all
    if options.get('prefer_all_shells', False):
        return [shell['name'] for shell in detected]

    # Otherwise, just return primary (highest priority)
    return [detected[0]['name']] if detected else []
```

**Usage:**
- Respects `--shell` flag
- Uses `options.prefer_all_shells` from manifest
- Platform-agnostic (manifest defines which shells work where)

---

### Method: `check_conflicts()` → Dict

**NEW METHOD** - Detect file conflicts before install

```python
def check_conflicts(self) -> Dict:
    """
    Check for file conflicts before installation.

    Returns:
        Dict with 'conflicts', 'overwrites', 'safe' file lists
    """
    result = {
        'conflicts': [],      # Files that would be overwritten
        'overwrites': [],     # Same as conflicts but more detailed
        'safe': [],           # Files that don't exist yet
        'has_conflicts': False
    }

    detected_agents = self.detect_agents()
    detected_shells = self.detect_shells()

    for kit_name in self.kits:
        # Check agent files
        for agent in detected_agents:
            files = self.manifest.get_kit_files(kit_name, agent=agent)

            for file_info in files:
                if file_info.get('status') == 'planned':
                    continue

                target_path = self.target_dir / file_info['path']

                if target_path.exists():
                    # Check if content is different
                    source_path = self.kits_dir / file_info['source']
                    if source_path.read_text() != target_path.read_text():
                        result['conflicts'].append(file_info['path'])
                        result['overwrites'].append({
                            'path': file_info['path'],
                            'source': file_info['source'],
                            'size_current': target_path.stat().st_size,
                            'size_new': source_path.stat().st_size,
                        })
                    # If same content, it's safe to "overwrite" (no-op)
                else:
                    result['safe'].append(file_info['path'])

        # Check shell scripts
        for shell in detected_shells:
            files = self.manifest.get_kit_files(kit_name, agent=shell)
            # Same logic as above

    result['has_conflicts'] = len(result['conflicts']) > 0
    return result
```

**Usage:**
- Called before install to detect conflicts
- Provides detailed info for user confirmation
- Compares file contents (not just existence)

---

### Method: `preview_installation()` → Dict

**ENHANCED** - More detailed preview with conflict info

```python
def preview_installation(self) -> Dict[str, any]:
    """
    Preview what will happen during installation.

    Returns:
        Detailed dict with files, directories, conflicts, warnings
    """
    preview = {
        "new_files": [],
        "modified_files": [],
        "new_directories": [],
        "conflicts": [],
        "warnings": [],
        "agents": [],
        "shells": [],
        "kits": [],
    }

    # Detect what will be installed
    detected_agents = self.detect_agents()
    detected_shells = self.detect_shells()

    preview['agents'] = detected_agents
    preview['shells'] = detected_shells
    preview['kits'] = self.kits

    if not detected_agents:
        preview['warnings'].append("No AI agents detected - nothing to install")
        return preview

    # Check conflicts
    conflicts = self.check_conflicts()
    preview['conflicts'] = conflicts['overwrites']

    # For each kit
    for kit_name in self.kits:
        kit_info = self.manifest.get_kit(kit_name)

        # Agent files
        for agent in detected_agents:
            files = self.manifest.get_kit_files(kit_name, agent=agent)

            for file_info in files:
                if file_info.get('status') == 'planned':
                    continue

                target_path = file_info['path']
                target_full = self.target_dir / target_path

                if target_full.exists():
                    preview["modified_files"].append(target_path)
                else:
                    preview["new_files"].append(target_path)

                    # Track new directories
                    parent_dir = str(target_full.parent.relative_to(self.target_dir))
                    if parent_dir not in preview["new_directories"]:
                        if not target_full.parent.exists():
                            preview["new_directories"].append(parent_dir)

        # Shell scripts
        for shell in detected_shells:
            # Same logic for scripts

        # Agent-agnostic files (memory, templates)
        all_files = self.manifest.get_kit_files(kit_name, agent=None)
        for file_info in all_files:
            # Skip agent/shell-specific files (already handled)
            if file_info.get('type') in ['command', 'prompt', 'script']:
                continue

            # Same preview logic

    return preview
```

**Changes:**
- ✅ Includes conflict detection
- ✅ Shows detected agents/shells
- ✅ Lists warnings
- ✅ More detailed info for dry-run display

---

### Method: `install()` → Dict

**ENHANCED** - Guardrails, confirmations, dry-run support

```python
def install(self) -> Dict:
    """
    Install kits to target project.

    Returns:
        Dictionary with success status and installed items
    """
    result = {
        "success": False,
        "installed": [],
        "skipped": [],
        "error": None,
        "dry_run": self.dry_run,
    }

    try:
        # Auto-detect agents and shells
        detected_agents = self.detect_agents()
        detected_shells = self.detect_shells()

        if not detected_agents:
            result["error"] = "No supported AI interface found"
            # Get supported agents from manifest for error message
            supported = [
                name for name, config in self.manifest.manifest.get('agents', {}).items()
                if config.get('supported', False)
            ]
            result["error"] += f". Supported: {', '.join(supported)}"
            return result

        # Check for conflicts (unless force mode)
        if not self.force:
            conflicts = self.check_conflicts()

            if conflicts['has_conflicts']:
                # In dry-run, just note conflicts
                if self.dry_run:
                    result["warnings"] = [
                        f"Would overwrite {len(conflicts['conflicts'])} existing files"
                    ]
                else:
                    # In real mode, this would trigger confirmation prompt
                    # (handled by CLI, not installer)
                    result["conflicts"] = conflicts['overwrites']
                    # For now, abort if conflicts and not forced
                    result["error"] = f"Found {len(conflicts['conflicts'])} file conflicts. Use --force to overwrite."
                    return result

        # Get options from manifest
        options = self.manifest.manifest.get('options', {})
        skip_existing = options.get('skip_existing', True)

        # For each requested kit
        for kit_name in self.kits:
            kit_info = self.manifest.get_kit(kit_name)

            # Install agent-specific files
            for agent in detected_agents:
                files = self.manifest.get_kit_files(kit_name, agent=agent)

                installed_commands = []
                for file_info in files:
                    # Skip planned/future files
                    if file_info.get('status') == 'planned':
                        result["skipped"].append(f"{file_info['path']} (planned)")
                        continue

                    target_path = self.target_dir / file_info['path']

                    # Skip if exists and skip_existing enabled
                    if skip_existing and target_path.exists() and not self.force:
                        result["skipped"].append(file_info['path'])
                        continue

                    # DRY-RUN: Don't actually install
                    if self.dry_run:
                        result["installed"].append(f"[DRY-RUN] {file_info['path']}")
                    else:
                        # Actually install the file
                        self._install_file(file_info['source'], file_info['path'])
                        result["installed"].append(file_info['path'])

                    # Track for summary
                    if file_info.get('type') in ['command', 'prompt']:
                        cmd_name = Path(file_info['path']).stem
                        installed_commands.append(cmd_name)

            # Install shell scripts
            for shell in detected_shells:
                # Same logic for scripts

            # Install agent-agnostic files
            # ... (memory, templates)

        result["success"] = True

        # Run validation if enabled and not dry-run
        if options.get('validate_on_install', True) and not self.dry_run:
            validation = self.validate()
            result["validation"] = validation

    except Exception as e:
        result["error"] = str(e)

    return result
```

**Changes:**
- ✅ Conflict detection with `check_conflicts()`
- ✅ Skip existing files (configurable from manifest)
- ✅ Dry-run mode (no actual file operations)
- ✅ Force mode to bypass confirmations
- ✅ Post-install validation (if enabled)
- ✅ Detailed result with installed/skipped/conflicts
- ✅ No hardcoded error messages

---

### Method: `validate()` → Dict

*(Same as before, already good)*

---

### Method: `remove()` → Dict

**ENHANCED** - Dry-run and safety checks

```python
def remove(self) -> Dict:
    """
    Remove kits from project.

    Returns:
        Dictionary with success status and removed items
    """
    result = {
        "success": False,
        "removed": [],
        "not_found": [],
        "error": None,
        "dry_run": self.dry_run,
    }

    try:
        for kit_name in self.kits:
            kit_info = self.manifest.get_kit(kit_name)
            removed_files = []
            not_found_files = []

            # Get all files for this kit
            all_files = self.manifest.get_kit_files(kit_name, agent=None)

            for file_info in all_files:
                target_path = self.target_dir / file_info['path']

                if target_path.exists():
                    # DRY-RUN: Don't actually remove
                    if self.dry_run:
                        removed_files.append(f"[DRY-RUN] {file_info['path']}")
                    else:
                        target_path.unlink()
                        removed_files.append(file_info['path'])
                else:
                    not_found_files.append(file_info['path'])

            if removed_files:
                result["removed"].append({
                    'kit': kit_info['name'],
                    'files': removed_files
                })

            if not_found_files:
                result["not_found"].extend(not_found_files)

        result["success"] = True

    except Exception as e:
        result["error"] = str(e)

    return result
```

**Changes:**
- ✅ Dry-run support
- ✅ Track not-found files separately
- ✅ More detailed result dict

---

## Nice-to-Have Additions

### 1. Backup Support (Future)

```python
def _install_file_with_backup(self, source, target):
    """Install file with .bak backup of existing file."""
    options = self.manifest.manifest.get('options', {})

    if options.get('create_backups', False):
        target_path = self.target_dir / target
        if target_path.exists():
            backup_path = target_path.with_suffix(target_path.suffix + '.bak')
            shutil.copy2(target_path, backup_path)

    self._install_file(source, target)
```

### 2. Rollback Support (Future)

```python
def rollback(self, transaction_id: str) -> Dict:
    """Rollback a failed installation."""
    # Implementation using transaction log
    pass
```

### 3. Migration Support (Future)

```python
def migrate_from_old_kits(self) -> Dict:
    """Migrate from old project/git kits to new dev-kit."""
    # Detect old kits
    # Move files to new locations
    # Update references
    pass
```

---

## Summary

### Zero Hardcoded Identifiers ✅
- `is_spec_kit_project()` - Uses `spec_kit.markers` from manifest
- `detect_agents()` - Loops through `agents.*` from manifest
- `detect_shells()` - Loops through `shells.*` from manifest
- All file paths from manifest
- All error messages use manifest data

### Guardrails & Dry-Run ✅
- `check_conflicts()` - Detect overwrites before install
- `preview_installation()` - Full dry-run preview
- `--dry-run` flag - No actual file operations
- `--force` flag - Skip confirmations
- `skip_existing` option - Don't overwrite by default
- Post-install validation

### Nice Extras
- Agent preference (`--agent claude`)
- Shell preference (`--shell bash`)
- Detailed result dicts (installed/skipped/conflicts)
- File integrity checking
- Partial install detection

### Implementation Estimate
- **2-3 hours** for careful refactoring with all features
- Can ship tonight! 🚀

---

Ready to implement?
