"""
Manifest-driven installer for lite-kits.

Orchestrates detection, validation, and file operations.
Delegates to specialized modules for specific tasks.
"""

import shutil
from pathlib import Path
from typing import Dict, List, Optional

from .conflict_checker import ConflictChecker
from .detector import Detector
from .manifest import KitManifest
from .validator import Validator


class Installer:
    """Main installer orchestrator."""

    def __init__(
        self,
        target_dir: Path,
        kits: Optional[List[str]] = None,
        force: bool = False,
        agents: Optional[List[str]] = None,
        shells: Optional[List[str]] = None,
    ):
        """
        Initialize installer.

        Args:
            target_dir: Target spec-kit project directory
            kits: List of kits to install (None = use default from manifest)
            force: Skip confirmations and overwrite existing files
            agents: List of explicit agent preferences (None = auto-detect)
            shells: List of explicit shell preferences (None = auto-detect)
        """
        self.target_dir = Path(target_dir).resolve()
        self.kits_dir = Path(__file__).parent.parent / "kits"

        # Load manifest
        self.manifest = KitManifest(self.kits_dir)

        # Initialize specialized modules
        self.detector = Detector(self.target_dir, self.manifest)
        self.validator = Validator(self.target_dir, self.manifest)
        self.conflict_checker = ConflictChecker(
            self.target_dir,
            self.kits_dir,
            self.manifest
        )

        # Operational modes
        self.force = force

        # Preferences
        self.preferred_agents = agents
        self.preferred_shells = shells

        # Kits to install
        self.kits = kits or [self.manifest.get_default_kit()]

        # Validate kit names
        self._validate_kit_names()

    def _validate_kit_names(self):
        """Validate kit names against manifest."""
        valid_kits = set(self.manifest.get_kit_names())
        invalid = set(self.kits) - valid_kits
        if invalid:
            valid_list = ', '.join(sorted(valid_kits))
            raise ValueError(f"Invalid kit(s): {invalid}. Valid: {valid_list}")

    def is_spec_kit_project(self) -> bool:
        """Check if target is a spec-kit project."""
        return self.detector.is_spec_kit_project()

    def is_kit_installed(self, kit_name: str) -> bool:
        """Check if kit is installed."""
        return self.validator.is_kit_installed(kit_name)

    def preview_installation(self) -> Dict:
        """Preview installation without making changes."""
        agents = self.detector.detect_agents(self.preferred_agents)
        shells = self.detector.detect_shells(self.preferred_shells)

        preview = {
            "kits": [],
            "conflicts": [],
            "warnings": [],
            "agents": agents,
            "shells": shells,
        }

        if not agents:
            supported = [
                name for name, config in self.manifest.manifest.get('agents', {}).items()
                if config.get('supported', False)
            ]
            preview['warnings'].append(f"No AI agents detected. Supported: {', '.join(supported)}")
            return preview

        conflicts = self.conflict_checker.check_conflicts(self.kits, agents, shells)
        preview['conflicts'] = conflicts['overwrites']

        for kit_name in self.kits:
            kit_preview = self._preview_kit(kit_name, agents, shells)
            preview['kits'].append(kit_preview)

        return preview

    def _preview_kit(self, kit_name: str, agents: List[str], shells: List[str]) -> Dict:
        """Preview installation for a single kit."""
        kit_info = self.manifest.get_kit(kit_name)
        kit_preview = {
            "name": kit_info['name'],
            "new_files": [],
            "modified_files": [],
            "new_directories": [],
        }

        for agent in agents:
            files = self.manifest.get_kit_files(kit_name, agent=agent)
            self._preview_files(files, kit_preview)

        for shell in shells:
            files = self.manifest.get_kit_files(kit_name, agent=shell)
            self._preview_files(files, kit_preview)

        # Get other files (not commands\prompts\scripts - those are handled above)
        all_files = self.manifest.get_kit_files(kit_name, agent=None)
        for file_info in all_files:
            if file_info.get('type') in ['command', 'prompt', 'script']:
                continue  # Already handled by agent/shell sections above
            self._preview_files([file_info], kit_preview)

        return kit_preview

    def _preview_files(self, files: List[Dict], preview: Dict):
        """Preview a list of files."""
        for file_info in files:
            if file_info.get('status') == 'planned':
                continue

            # Normalize paths to use backslashes for Windows display
            target_path = str(file_info['path']).replace("/", "\\")
            target_full = self.target_dir / file_info['path']

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

    def install(self) -> Dict:
        """Install kits to target project."""
        result = {
            "success": False,
            "installed": [],
            "skipped": [],
            "error": None,
        }

        try:
            agents = self.detector.detect_agents(self.preferred_agents)
            shells = self.detector.detect_shells(self.preferred_shells)

            if not agents:
                supported = [
                    name for name, config in self.manifest.manifest.get('agents', {}).items()
                    if config.get('supported', False)
                ]
                result["error"] = (
                    f"No supported AI interface found. Supported: {', '.join(supported)}. "
                    r"To enable AI interface support, create a '.claude\' or '.github\prompts\' directory in your project."
                )
                return result

            if not self.force:
                conflicts = self.conflict_checker.check_conflicts(self.kits, agents, shells)

                if conflicts['has_conflicts']:
                    result["conflicts"] = conflicts['overwrites']
                    result["error"] = f"Found {len(conflicts['conflicts'])} file conflicts. Use --force to overwrite."
                    return result

            options = self.manifest.manifest.get('options', {})

            for kit_name in self.kits:
                self._install_kit(kit_name, agents, shells, options, result)

            result["success"] = True

            if options.get('validate_on_install', True):
                result["validation"] = self.validator.validate_all()

        except Exception as e:
            result["error"] = str(e)

        return result

    def _install_kit(self, kit_name: str, agents: List[str], shells: List[str], options: Dict, result: Dict):
        """Install a single kit."""
        skip_existing = options.get('skip_existing', True)

        for agent in agents:
            files = self.manifest.get_kit_files(kit_name, agent=agent)
            self._install_files(files, skip_existing, result)

        for shell in shells:
            files = self.manifest.get_kit_files(kit_name, agent=shell)
            self._install_files(files, skip_existing, result)

        all_files = self.manifest.get_kit_files(kit_name, agent=None)
        for file_info in all_files:
            if file_info.get('type') in ['command', 'prompt', 'script']:
                continue
            self._install_files([file_info], skip_existing, result)

    def _install_files(self, files: List[Dict], skip_existing: bool, result: Dict):
        """Install a list of files."""
        for file_info in files:
            if file_info.get('status') == 'planned':
                result["skipped"].append(f"{file_info['path']} (planned)")
                continue

            target_path = self.target_dir / file_info['path']

            if skip_existing and target_path.exists() and not self.force:
                result["skipped"].append(file_info['path'])
                continue

            self._copy_file(file_info['source'], file_info['path'])
            result["installed"].append(file_info['path'])

    def validate(self) -> Dict:
        """Validate all installed kits."""
        return self.validator.validate_all()

    def preview_removal(self) -> Dict:
        """Preview files that would be removed."""
        preview = {
            "kits": [],
            "total_files": 0,
        }

        for kit_name in self.kits:
            kit_info = self.manifest.get_kit(kit_name)
            files_to_remove = []

            all_files = self.manifest.get_kit_files(kit_name, agent=None)

            for file_info in all_files:
                target_path = self.target_dir / file_info['path']
                if target_path.exists():
                    files_to_remove.append(file_info['path'])

            if files_to_remove:
                preview["kits"].append({
                    'name': kit_info['name'],
                    'files': files_to_remove
                })
                preview["total_files"] += len(files_to_remove)

        return preview

    def remove(self) -> Dict:
        """Remove kits from project."""
        result = {
            "success": False,
            "removed": [],
            "not_found": [],
            "error": None,
        }

        try:
            for kit_name in self.kits:
                kit_info = self.manifest.get_kit(kit_name)
                removed_files = []
                not_found_files = []

                all_files = self.manifest.get_kit_files(kit_name, agent=None)

                for file_info in all_files:
                    target_path = self.target_dir / file_info['path']

                    if target_path.exists():
                        target_path.unlink()
                        removed_files.append(file_info['path'])
                    else:
                        not_found_files.append(file_info['path'])

                if removed_files:
                    result["removed"].append({'kit': kit_info['name'], 'files': removed_files})

                if not_found_files:
                    result["not_found"].extend(not_found_files)

            result["success"] = True

        except Exception as e:
            result["error"] = str(e)

        return result

    def _copy_file(self, kit_relative_path: str, target_relative_path: str):
        """Copy file from kits/ to target project."""
        source = self.kits_dir / kit_relative_path
        target = self.target_dir / target_relative_path

        if not source.exists():
            raise FileNotFoundError(f"Kit file not found: {source}")

        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)
