"""
Manifest-driven installer for lite-kits.

Zero hardcoded identifiers - everything from kits.yaml manifest.
Includes dry-run, guardrails, conflict detection, and validation.
"""

import shutil
from pathlib import Path
from typing import Dict, List, Optional

from .manifest import KitManifest


class Installer:
    """Manages installation of kits to spec-kit projects."""

    def __init__(
        self,
        target_dir: Path,
        kits: Optional[List[str]] = None,
        dry_run: bool = False,
        force: bool = False,
        agent: Optional[str] = None,
        shell: Optional[str] = None,
    ):
        """
        Initialize installer.

        Args:
            target_dir: Target spec-kit project directory
            kits: List of kits to install. Defaults to manifest default_kit.
            dry_run: Preview mode - no actual file operations
            force: Skip confirmations and overwrite existing files
            agent: Explicit agent preference (None = auto-detect)
            shell: Explicit shell preference (None = auto-detect)
        """
        self.target_dir = Path(target_dir).resolve()
        self.kits_dir = Path(__file__).parent.parent / "kits"
        self.manifest = KitManifest(self.kits_dir)

        # Operational modes
        self.dry_run = dry_run
        self.force = force

        # Explicit preferences (None = auto-detect)
        self.preferred_agent = agent
        self.preferred_shell = shell

        # Use manifest for defaults - NO HARDCODED VALUES
        self.kits = kits or [self.manifest.get_default_kit()]

        # Validate kit names against manifest
        valid_kits = set(self.manifest.get_kit_names())
        invalid = set(self.kits) - valid_kits
        if invalid:
            valid_list = ', '.join(sorted(valid_kits))
            raise ValueError(f"Invalid kit(s): {invalid}. Valid: {valid_list}")

    def is_spec_kit_project(self) -> bool:
        """
        Check if target directory is a spec-kit project.

        Uses spec_kit.markers from manifest - NO HARDCODED PATHS.

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

    def detect_agents(self) -> List[str]:
        """
        Auto-detect which AI agents are present in project.

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

        # Auto-detect from manifest - NO HARDCODED AGENT NAMES
        detected = []
        agents = self.manifest.manifest.get('agents', {})

        for agent_name, config in agents.items():
            # Skip unsupported agents
            if not config.get('supported', False):
                continue

            # Check if marker directory exists
            marker_dir = self.target_dir / config['marker_dir']
            if marker_dir.exists():
                detected.append({
                    'name': agent_name,
                    'priority': config.get('priority', 999)
                })

        # Sort by priority (lower = higher priority)
        detected.sort(key=lambda x: x['priority'])

        return [agent['name'] for agent in detected]

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

    def check_conflicts(self) -> Dict:
        """
        Check for file conflicts before installation.

        Returns:
            Dict with 'conflicts', 'overwrites', 'safe' file lists
        """
        result = {
            'conflicts': [],      # List of conflicting file paths
            'overwrites': [],     # Detailed info about each overwrite
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

                        if source_path.exists():
                            try:
                                source_content = source_path.read_text()
                                target_content = target_path.read_text()

                                if source_content != target_content:
                                    result['conflicts'].append(file_info['path'])
                                    result['overwrites'].append({
                                        'path': file_info['path'],
                                        'source': file_info['source'],
                                        'size_current': target_path.stat().st_size,
                                        'size_new': source_path.stat().st_size,
                                    })
                            except Exception:
                                # If can't read/compare, consider it a conflict
                                result['conflicts'].append(file_info['path'])
                    else:
                        result['safe'].append(file_info['path'])

            # Check shell scripts
            for shell in detected_shells:
                files = self.manifest.get_kit_files(kit_name, agent=shell)
                # Same logic as agent files
                for file_info in files:
                    if file_info.get('status') == 'planned':
                        continue

                    target_path = self.target_dir / file_info['path']

                    if target_path.exists():
                        source_path = self.kits_dir / file_info['source']
                        if source_path.exists():
                            try:
                                if source_path.read_text() != target_path.read_text():
                                    if file_info['path'] not in result['conflicts']:
                                        result['conflicts'].append(file_info['path'])
                                        result['overwrites'].append({
                                            'path': file_info['path'],
                                            'source': file_info['source'],
                                            'size_current': target_path.stat().st_size,
                                            'size_new': source_path.stat().st_size,
                                        })
                            except Exception:
                                if file_info['path'] not in result['conflicts']:
                                    result['conflicts'].append(file_info['path'])
                    else:
                        if file_info['path'] not in result['safe']:
                            result['safe'].append(file_info['path'])

        result['has_conflicts'] = len(result['conflicts']) > 0
        return result

    def preview_installation(self) -> Dict:
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
            # Get supported agents for warning message - NO HARDCODED LIST
            supported = [
                name for name, config in self.manifest.manifest.get('agents', {}).items()
                if config.get('supported', False)
            ]
            preview['warnings'].append(
                f"No AI agents detected. Supported: {', '.join(supported)}"
            )
            return preview

        # Check conflicts
        conflicts = self.check_conflicts()
        preview['conflicts'] = conflicts['overwrites']

        # For each kit
        for kit_name in self.kits:
            # Agent files
            for agent in detected_agents:
                files = self.manifest.get_kit_files(kit_name, agent=agent)

                for file_info in files:
                    if file_info.get('status') == 'planned':
                        continue

                    target_path = file_info['path']
                    target_full = self.target_dir / target_path

                    if target_full.exists():
                        if target_path not in preview["modified_files"]:
                            preview["modified_files"].append(target_path)
                    else:
                        if target_path not in preview["new_files"]:
                            preview["new_files"].append(target_path)

                        # Track new directories
                        parent_dir = str(target_full.parent.relative_to(self.target_dir))
                        if parent_dir not in preview["new_directories"]:
                            if not target_full.parent.exists():
                                preview["new_directories"].append(parent_dir)

            # Shell scripts
            for shell in detected_shells:
                files = self.manifest.get_kit_files(kit_name, agent=shell)
                for file_info in files:
                    if file_info.get('status') == 'planned':
                        continue

                    target_path = file_info['path']
                    target_full = self.target_dir / target_path

                    if target_full.exists():
                        if target_path not in preview["modified_files"]:
                            preview["modified_files"].append(target_path)
                    else:
                        if target_path not in preview["new_files"]:
                            preview["new_files"].append(target_path)

                        parent_dir = str(target_full.parent.relative_to(self.target_dir))
                        if parent_dir not in preview["new_directories"]:
                            if not target_full.parent.exists():
                                preview["new_directories"].append(parent_dir)

            # Agent-agnostic files (memory, templates)
            all_files = self.manifest.get_kit_files(kit_name, agent=None)
            for file_info in all_files:
                # Skip agent/shell-specific files (already handled)
                if file_info.get('type') in ['command', 'prompt', 'script']:
                    continue

                if file_info.get('status') == 'planned':
                    continue

                target_path = file_info['path']
                target_full = self.target_dir / target_path

                if target_full.exists():
                    if target_path not in preview["modified_files"]:
                        preview["modified_files"].append(target_path)
                else:
                    if target_path not in preview["new_files"]:
                        preview["new_files"].append(target_path)

                    parent_dir = str(target_full.parent.relative_to(self.target_dir))
                    if parent_dir not in preview["new_directories"]:
                        if not target_full.parent.exists():
                            preview["new_directories"].append(parent_dir)

        return preview

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
                # Get supported agents from manifest for error message
                supported = [
                    name for name, config in self.manifest.manifest.get('agents', {}).items()
                    if config.get('supported', False)
                ]
                result["error"] = f"No supported AI interface found. Supported: {', '.join(supported)}"
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
                        # In real mode, store conflicts for CLI to handle
                        result["conflicts"] = conflicts['overwrites']
                        result["error"] = (
                            f"Found {len(conflicts['conflicts'])} file conflicts. "
                            "Use --force to overwrite."
                        )
                        return result

            # Get options from manifest - NO HARDCODED DEFAULTS
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

                        # Skip if exists and skip_existing enabled (unless force)
                        if skip_existing and target_path.exists() and not self.force:
                            result["skipped"].append(file_info['path'])
                            continue

                        # DRY-RUN: Don't actually install
                        if self.dry_run:
                            result["installed"].append(f"[DRY-RUN] {file_info['path']}")
                        else:
                            # Actually install the file
                            self._install_file(file_info['source'], file_info['path'])

                        # Track for summary
                        if file_info.get('type') in ['command', 'prompt']:
                            cmd_name = Path(file_info['path']).stem
                            installed_commands.append(cmd_name)

                # Install shell scripts (same logic)
                for shell in detected_shells:
                    files = self.manifest.get_kit_files(kit_name, agent=shell)
                    for file_info in files:
                        if file_info.get('status') == 'planned':
                            result["skipped"].append(f"{file_info['path']} (planned)")
                            continue

                        target_path = self.target_dir / file_info['path']

                        if skip_existing and target_path.exists() and not self.force:
                            result["skipped"].append(file_info['path'])
                            continue

                        if self.dry_run:
                            result["installed"].append(f"[DRY-RUN] {file_info['path']}")
                        else:
                            self._install_file(file_info['source'], file_info['path'])

                # Install agent-agnostic files (memory, templates)
                all_files = self.manifest.get_kit_files(kit_name, agent=None)
                for file_info in all_files:
                    # Skip agent/shell-specific files (already handled)
                    if file_info.get('type') in ['command', 'prompt', 'script']:
                        continue

                    if file_info.get('status') == 'planned':
                        result["skipped"].append(f"{file_info['path']} (planned)")
                        continue

                    target_path = self.target_dir / file_info['path']

                    if skip_existing and target_path.exists() and not self.force:
                        result["skipped"].append(file_info['path'])
                        continue

                    if self.dry_run:
                        result["installed"].append(f"[DRY-RUN] {file_info['path']}")
                    else:
                        self._install_file(file_info['source'], file_info['path'])

            result["success"] = True

            # Run validation if enabled and not dry-run
            if options.get('validate_on_install', True) and not self.dry_run:
                validation = self.validate()
                result["validation"] = validation

        except Exception as e:
            result["error"] = str(e)

        return result

    def validate(self) -> Dict:
        """
        Validate kit installation.

        Returns:
            Dictionary with validation results
        """
        checks = {}
        options = self.manifest.manifest.get('options', {})

        # For each kit (check all, not just requested)
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

    def _install_file(self, kit_relative_path: str, target_relative_path: str):
        """
        Install a file from kits directory to target project.

        Args:
            kit_relative_path: Path relative to kits/ directory
            target_relative_path: Path relative to target directory
        """
        source = self.kits_dir / kit_relative_path
        target = self.target_dir / target_relative_path

        if not source.exists():
            raise FileNotFoundError(f"Kit file not found: {source}")

        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
