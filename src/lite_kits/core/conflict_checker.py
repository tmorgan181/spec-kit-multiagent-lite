"""
File conflict detection for installer.

Checks for existing files that would be overwritten.
"""

from pathlib import Path
from typing import Dict, List

from .manifest import KitManifest


class ConflictChecker:
    """Detects file conflicts before installation."""

    def __init__(self, target_dir: Path, kits_dir: Path, manifest: KitManifest):
        """
        Initialize conflict checker.

        Args:
            target_dir: Target project directory
            kits_dir: Kits source directory
            manifest: Loaded kit manifest
        """
        self.target_dir = target_dir
        self.kits_dir = kits_dir
        self.manifest = manifest

    def check_conflicts(
        self,
        kits: List[str],
        agents: List[str],
        shells: List[str]
    ) -> Dict:
        """
        Check for file conflicts.

        Args:
            kits: List of kit names to check
            agents: List of agent names
            shells: List of shell names

        Returns:
            Dict with conflict details
        """
        result = {
            'conflicts': [],
            'overwrites': [],
            'safe': [],
            'has_conflicts': False
        }

        for kit_name in kits:
            # Check agent files
            for agent in agents:
                self._check_file_group(kit_name, agent, result)

            # Check shell files
            for shell in shells:
                self._check_file_group(kit_name, shell, result)

            # Check agent-agnostic files
            all_files = self.manifest.get_kit_files(kit_name, agent=None)
            for file_info in all_files:
                # Skip agent/shell-specific
                if file_info.get('type') in ['command', 'prompt', 'script']:
                    continue

                self._check_file(file_info, result)

        result['has_conflicts'] = len(result['conflicts']) > 0
        return result

    def _check_file_group(self, kit_name: str, agent_or_shell: str, result: Dict):
        """Check a group of files for an agent/shell."""
        files = self.manifest.get_kit_files(kit_name, agent=agent_or_shell)

        for file_info in files:
            if file_info.get('status') == 'planned':
                continue

            self._check_file(file_info, result)

    def _check_file(self, file_info: Dict, result: Dict):
        """Check a single file for conflicts."""
        target_path = self.target_dir / file_info['path']

        if not target_path.exists():
            if file_info['path'] not in result['safe']:
                result['safe'].append(file_info['path'])
            return

        # File exists, check if content differs
        source_path = self.kits_dir / file_info['source']

        if not source_path.exists():
            return

        try:
            source_content = source_path.read_text(encoding='utf-8')
            target_content = target_path.read_text(encoding='utf-8')

            if source_content != target_content:
                if file_info['path'] not in result['conflicts']:
                    result['conflicts'].append(file_info['path'])
                    result['overwrites'].append({
                        'path': file_info['path'],
                        'source': file_info['source'],
                        'size_current': target_path.stat().st_size,
                        'size_new': source_path.stat().st_size,
                    })
        except Exception:
            # If can't read/compare, treat as conflict
            if file_info['path'] not in result['conflicts']:
                result['conflicts'].append(file_info['path'])
