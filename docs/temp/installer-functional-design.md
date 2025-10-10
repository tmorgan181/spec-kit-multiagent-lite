# Installer Functional Design - Manifest-Driven Architecture

## Overview

Complete rewrite of `installer.py` to use `kits.yaml` as single source of truth. No hardcoded kit logic.

---

## Class: Installer

### Constructor: `__init__(target_dir, kits=None)`

```python
def __init__(self, target_dir: Path, kits: Optional[List[str]] = None):
    self.target_dir = Path(target_dir).resolve()
    self.kits_dir = Path(__file__).parent.parent / "kits"
    self.manifest = KitManifest(self.kits_dir)  # Load manifest

    # Use manifest for defaults
    self.kits = kits or [self.manifest.get_default_kit()]

    # Validate kit names against manifest
    valid_kits = self.manifest.get_kit_names()
    invalid = set(self.kits) - set(valid_kits)
    if invalid:
        raise ValueError(f"Invalid kit(s): {invalid}. Valid: {valid_kits}")
```

**Changes:**
- ✅ Load KitManifest instead of hardcoding valid kits
- ✅ Use `manifest.get_default_kit()` instead of hardcoded `['dev']`
- ✅ Validate against `manifest.get_kit_names()`

---

### Method: `is_spec_kit_project()` → bool

**NO CHANGES** - This is spec-kit detection, not kit-specific

```python
def is_spec_kit_project(self) -> bool:
    markers = [
        self.target_dir / ".specify",
        self.target_dir / ".claude",
        self.target_dir / ".github" / "prompts",
    ]
    return any(marker.exists() for marker in markers)
```

---

### Method: `is_kit_installed(kit_name: str)` → bool

**Renamed from** `is_multiagent_installed()` (too specific)

```python
def is_kit_installed(self, kit_name: str) -> bool:
    """
    Check if kit is already installed.

    Args:
        kit_name: Name of kit to check

    Returns:
        True if any marker files exist
    """
    markers = self.manifest.get_kit_markers(kit_name)

    for marker in markers:
        if (self.target_dir / marker).exists():
            return True

    return False
```

**Changes:**
- ✅ Use `manifest.get_kit_markers()` instead of hardcoded dict
- ✅ Loop through marker paths from manifest
- ✅ Generic for any kit

---

### Method: `detect_agents()` → List[str]

**NEW METHOD** - Auto-detect which agents are present

```python
def detect_agents(self) -> List[str]:
    """
    Auto-detect which AI agents are present in project.

    Returns:
        List of detected agent names (e.g., ['claude', 'copilot'])
    """
    detected = []

    agents = self.manifest.manifest.get('agents', {})
    for agent_name, config in agents.items():
        if not config.get('supported', False):
            continue

        marker_dir = self.target_dir / config['marker_dir']
        if marker_dir.exists():
            detected.append(agent_name)

    return detected
```

**Usage:**
- Called during installation to determine which file groups to install
- Respects `agents.*.supported` flag from manifest

---

### Method: `preview_installation()` → Dict

```python
def preview_installation(self) -> Dict[str, List[str]]:
    """
    Preview what files will be created/modified.

    Returns:
        Dictionary with lists of new_files, modified_files, new_directories
    """
    changes = {
        "new_files": [],
        "modified_files": [],
        "new_directories": [],
    }

    # Auto-detect agents
    detected_agents = self.detect_agents()

    if not detected_agents:
        return changes  # No agents found, nothing to install

    # For each requested kit
    for kit_name in self.kits:
        # For each detected agent
        for agent in detected_agents:
            # Get files for this kit + agent combo
            files = self.manifest.get_kit_files(kit_name, agent=agent)

            for file_info in files:
                target_path = file_info['path']
                target_full = self.target_dir / target_path

                # Check if file exists
                if target_full.exists():
                    changes["modified_files"].append(target_path)
                else:
                    changes["new_files"].append(target_path)

                    # Track new directories
                    dir_path = str(target_full.parent.relative_to(self.target_dir))
                    if dir_path not in changes["new_directories"] and not target_full.parent.exists():
                        changes["new_directories"].append(dir_path)

        # Also get agent-agnostic files (memory, templates, scripts)
        all_files = self.manifest.get_kit_files(kit_name, agent=None)
        for file_info in all_files:
            # Filter out agent-specific files (already handled)
            if file_info.get('type') in ['command', 'prompt']:
                continue

            target_path = file_info['path']
            target_full = self.target_dir / target_path

            if target_full.exists():
                changes["modified_files"].append(target_path)
            else:
                changes["new_files"].append(target_path)

    return changes
```

**Changes:**
- ✅ Auto-detect agents instead of manual `has_claude`/`has_copilot` checks
- ✅ Loop through kits using `manifest.get_kit_files()`
- ✅ No hardcoded file paths
- ✅ Handles agent-agnostic files (memory, templates, scripts)

---

### Method: `install()` → Dict

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
        "error": None,
    }

    try:
        # Auto-detect agents
        detected_agents = self.detect_agents()

        if not detected_agents:
            result["error"] = "No supported AI interface found (.claude or .github/prompts)"
            return result

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
                        continue

                    # Install the file
                    self._install_file(file_info['source'], file_info['path'])

                    # Track command names for summary
                    if file_info.get('type') in ['command', 'prompt']:
                        cmd_name = file_info['path'].split('/')[-1].replace('.md', '').replace('.prompt', '')
                        installed_commands.append(cmd_name)

                if installed_commands:
                    agent_name = self.manifest.get_agent_config(agent)['name']
                    result["installed"].append(
                        f"{kit_info['name']} ({agent_name}): {', '.join(installed_commands)}"
                    )

            # Install agent-agnostic files (memory, templates, scripts)
            all_files = self.manifest.get_kit_files(kit_name, agent=None)
            agnostic_installed = []

            for file_info in all_files:
                # Skip agent-specific files (already handled)
                if file_info.get('type') in ['command', 'prompt']:
                    continue

                # Skip planned files
                if file_info.get('status') == 'planned':
                    continue

                # Install the file
                self._install_file(file_info['source'], file_info['path'])
                agnostic_installed.append(file_info.get('type', 'file'))

            if agnostic_installed:
                types = ', '.join(set(agnostic_installed))
                result["installed"].append(f"{kit_info['name']}: {types}")

        result["success"] = True

    except Exception as e:
        result["error"] = str(e)

    return result
```

**Changes:**
- ✅ Auto-detect agents
- ✅ Loop through kits from manifest
- ✅ Use `manifest.get_kit_files()` for file lists
- ✅ Respect `status: planned` flag (skip planned files)
- ✅ Handle agent-agnostic files (memory, templates, scripts)
- ✅ Dynamic summary messages using kit/agent names from manifest

---

### Method: `validate()` → Dict

```python
def validate(self) -> Dict:
    """
    Validate kit installation.

    Returns:
        Dictionary with validation results
    """
    checks = {}
    options = self.manifest.manifest.get('options', {})

    # For each installed kit (check all kits, not just requested)
    for kit_name in self.manifest.get_kit_names():
        markers = self.manifest.get_kit_markers(kit_name)
        kit_info = self.manifest.get_kit(kit_name)

        # Check if any marker exists
        kit_installed = any((self.target_dir / marker).exists() for marker in markers)

        if kit_installed:
            # Kit is installed, validate files
            all_files = self.manifest.get_kit_files(kit_name, agent=None)

            missing_files = []
            corrupted_files = []

            for file_info in all_files:
                # Skip non-required files
                if not file_info.get('required', True):
                    continue

                # Skip planned files
                if file_info.get('status') == 'planned':
                    continue

                target_path = self.target_dir / file_info['path']

                # Check exists
                if not target_path.exists():
                    missing_files.append(file_info['path'])
                    continue

                # Check integrity (if enabled)
                if options.get('check_file_integrity', True):
                    min_size = options.get('min_file_size', 100)
                    if target_path.stat().st_size < min_size:
                        corrupted_files.append(file_info['path'])

            # Build status message
            if missing_files or corrupted_files:
                status = "partial"
                issues = []
                if missing_files:
                    issues.append(f"{len(missing_files)} missing")
                if corrupted_files:
                    issues.append(f"{len(corrupted_files)} corrupted")
                message = f"{kit_info['name']}: {', '.join(issues)} - run: lite-kits add --kit {kit_name}"
                passed = False
            else:
                status = "installed"
                message = f"{kit_info['name']}: all files present"
                passed = True

            checks[kit_name] = {
                "passed": passed,
                "status": status,
                "message": message,
                "missing_files": missing_files,
                "corrupted_files": corrupted_files,
            }
        else:
            # Kit not installed
            checks[kit_name] = {
                "passed": True,  # Not an error if not installed
                "status": "not_installed",
                "message": f"{kit_info['name']}: not installed",
            }

    # Overall validation passes if at least one kit is fully installed
    any_installed = any(
        check['status'] == 'installed'
        for check in checks.values()
    )

    return {
        "valid": any_installed,
        "checks": checks,
    }
```

**Changes:**
- ✅ Loop through all kits from manifest
- ✅ Use `manifest.get_kit_markers()` for detection
- ✅ Use `manifest.get_kit_files()` for validation
- ✅ Check file integrity (size > min_file_size)
- ✅ Detect partial installs (missing/corrupted files)
- ✅ Skip non-required and planned files
- ✅ Detailed status: `installed`, `partial`, `not_installed`

---

### Method: `remove()` → Dict

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
        "error": None,
    }

    try:
        for kit_name in self.kits:
            kit_info = self.manifest.get_kit(kit_name)
            removed_files = []

            # Get all files for this kit
            all_files = self.manifest.get_kit_files(kit_name, agent=None)

            for file_info in all_files:
                target_path = self.target_dir / file_info['path']

                if target_path.exists():
                    target_path.unlink()
                    removed_files.append(file_info['path'])

            if removed_files:
                result["removed"].append(
                    f"{kit_info['name']}: {len(removed_files)} files"
                )

        result["success"] = True

    except Exception as e:
        result["error"] = str(e)

    return result
```

**Changes:**
- ✅ Loop through kits from manifest
- ✅ Use `manifest.get_kit_files()` for removal
- ✅ No hardcoded file paths or command lists

---

### Private Method: `_install_file()` → None

**NO CHANGES** - This is a low-level file copy utility

```python
def _install_file(self, kit_relative_path: str, target_relative_path: str):
    source = self.kits_dir / kit_relative_path
    target = self.target_dir / target_relative_path

    if not source.exists():
        raise FileNotFoundError(f"Kit file not found: {source}")

    target.parent.mkdir(parents=True, exist_ok=True)
    shutil.copy2(source, target)
```

---

## Summary of Changes

### Before (Hardcoded):
- 437 lines of hardcoded kit logic
- 5+ methods with kit-specific code
- Need to edit installer for every new kit/command

### After (Manifest-Driven):
- ~200 lines of generic logic
- All kit info from manifest
- Add new kits: edit YAML only

### Key Improvements:
1. ✅ **Auto-detect agents** instead of manual checks
2. ✅ **Loop through manifest** instead of hardcoded paths
3. ✅ **File integrity validation** (missing, corrupted)
4. ✅ **Partial install detection** (some files missing)
5. ✅ **Status tracking** (installed, partial, not_installed)
6. ✅ **Future-proof** (Cursor, Windsurf, Fish, Zsh ready)
7. ✅ **Script support** (Bash, PowerShell, planned shells)

### Methods Changed:
- `__init__()` - Use manifest for validation
- `is_kit_installed()` - Generic using markers
- `detect_agents()` - NEW, auto-detect from manifest
- `preview_installation()` - Loop through manifest files
- `install()` - Loop through manifest files
- `validate()` - Full integrity checking
- `remove()` - Loop through manifest files

### Methods Unchanged:
- `is_spec_kit_project()` - Spec-kit detection
- `_install_file()` - Low-level file copy

---

## Next Steps

1. ✅ Review this design
2. Implement new installer.py
3. Update CLI to use manifest methods
4. Test with dev-kit
5. Delete old project/ and git/ dirs
6. Ship v0.2.0!

**Estimated implementation time**: 1-2 hours (mostly careful refactoring)
