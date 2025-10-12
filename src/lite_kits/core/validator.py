"""
Kit validation and integrity checking.

Validates installed kits, checks for missing/corrupted files.
"""

from pathlib import Path
from typing import Dict

from .manifest import KitManifest
from .detector import Detector


class Validator:
    """Validates kit installations."""

    def __init__(self, target_dir: Path, manifest: KitManifest):
        """
        Initialize validator.

        Args:
            target_dir: Target project directory
            manifest: Loaded kit manifest
        """
        self.target_dir = target_dir
        self.manifest = manifest
        self.detector = Detector(target_dir, manifest)

    def validate_all(self) -> Dict:
        """
        Validate all kits.

        Returns:
            Validation results for all kits
        """
        checks = {}
        options = self.manifest.manifest.get('options', {})

        for kit_name in self.manifest.get_kit_names():
            checks[kit_name] = self.validate_kit(kit_name, options)

        # Overall validation passes if at least one kit is fully installed
        any_installed = any(
            check['status'] == 'installed'
            for check in checks.values()
        )

        return {
            "valid": any_installed,
            "checks": checks,
            "target_dir": self.target_dir,
        }

    def validate_kit(self, kit_name: str, options: Dict) -> Dict:
        """
        Validate a single kit.

        Args:
            kit_name: Name of kit to validate
            options: Options from manifest

        Returns:
            Validation result for this kit
        """
        kit_info = self.manifest.get_kit(kit_name)
        markers = self.manifest.get_kit_markers(kit_name)

        # Check if kit is installed
        kit_installed = any(
            (self.target_dir / marker).exists()
            for marker in markers
        )

        if not kit_installed:
            return {
                "passed": True,
                "status": "not_installed",
                "message": f"{kit_info['name']}: not installed",
            }

        # Detect which agents are actually present in the project
        detected_agents = self.detector.detect_agents()
        detected_shells = self.detector.detect_shells()

        # Kit is installed, validate only files for detected agents/shells that actually have kit files
        files_to_validate = []

        # Add agent-specific files (commands/prompts) - only if at least one kit file exists for that agent
        for agent in detected_agents:
            agent_files = self.manifest.get_kit_files(kit_name, agent=agent)
            # Check if any of this kit's files exist for this agent
            has_kit_files = any(
                (self.target_dir / f['path']).exists()
                for f in agent_files
                if f.get('status') != 'planned'
            )
            if has_kit_files:
                files_to_validate.extend(agent_files)

        # Add shell-specific files (scripts) - only if at least one kit file exists for that shell
        for shell in detected_shells:
            shell_files = self.manifest.get_kit_files(kit_name, agent=shell)
            has_kit_files = any(
                (self.target_dir / f['path']).exists()
                for f in shell_files
                if f.get('status') != 'planned'
            )
            if has_kit_files:
                files_to_validate.extend(shell_files)

        # Add agent/shell-agnostic files (memory, templates, etc.)
        all_files = self.manifest.get_kit_files(kit_name, agent=None)
        for file_info in all_files:
            # Only add files that aren't agent/shell-specific
            if file_info.get('type') not in ['command', 'prompt', 'script']:
                files_to_validate.append(file_info)

        missing = []
        corrupted = []
        outdated = []

        for file_info in files_to_validate:
            # Skip non-required files
            if not file_info.get('required', True):
                continue

            # Skip planned files
            if file_info.get('status') == 'planned':
                continue

            target_path = self.target_dir / file_info['path']

            # Check exists
            if not target_path.exists():
                missing.append(file_info['path'])
                continue

            # Check integrity
            if options.get('check_file_integrity', True):
                min_size = options.get('min_file_size', 100)
                if target_path.stat().st_size < min_size:
                    corrupted.append(file_info['path'])

            # Check if outdated (differs from source)
            # (Placeholder for now, can add diff later)

        # Build result
        if missing or corrupted:
            issues = []
            if missing:
                issues.append(f"{len(missing)} missing")
            if corrupted:
                issues.append(f"{len(corrupted)} corrupted")

            return {
                "passed": False,
                "status": "partial",
                "message": f"{kit_info['name']}: {', '.join(issues)}",
                "missing_files": missing,
                "corrupted_files": corrupted,
            }

        return {
            "passed": True,
            "status": "installed",
            "message": f"{kit_info['name']}: all files present",
        }

    def is_kit_installed(self, kit_name: str) -> bool:
        """
        Quick check if kit is installed.

        Args:
            kit_name: Name of kit

        Returns:
            True if any marker exists
        """
        markers = self.manifest.get_kit_markers(kit_name)
        return any(
            (self.target_dir / marker).exists()
            for marker in markers
        )
