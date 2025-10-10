"""
Kit manifest loader and utilities.

Loads kit definitions from kits.yaml and provides helpers for installation,
validation, and status checking.
"""

from pathlib import Path
from typing import Dict, List, Optional
import yaml


class KitManifest:
    """Loads and provides access to kit definitions from kits.yaml"""

    def __init__(self, kits_dir: Path):
        """
        Initialize manifest loader.

        Args:
            kits_dir: Path to kits directory containing kits.yaml
        """
        self.kits_dir = kits_dir
        self.manifest_path = kits_dir / "kits.yaml"
        self._manifest = None

    @property
    def manifest(self) -> Dict:
        """Load and cache manifest data"""
        if self._manifest is None:
            with open(self.manifest_path) as f:
                self._manifest = yaml.safe_load(f)
        return self._manifest

    def get_kit(self, kit_name: str) -> Optional[Dict]:
        """Get kit definition by name"""
        return self.manifest['kits'].get(kit_name)

    def get_all_kits(self) -> Dict[str, Dict]:
        """Get all kit definitions"""
        return self.manifest['kits']

    def get_kit_names(self) -> List[str]:
        """Get list of all kit names"""
        return list(self.manifest['kits'].keys())

    def get_recommended_kits(self) -> List[str]:
        """Get list of recommended kit names"""
        return [
            name for name, kit in self.manifest['kits'].items()
            if kit.get('recommended', False)
        ]

    def get_default_kit(self) -> str:
        """Get default kit name"""
        return self.manifest['options']['default_kit']

    def get_kit_files(self, kit_name: str, agent: Optional[str] = None) -> List[Dict]:
        """
        Get list of files for a kit.

        Args:
            kit_name: Name of kit
            agent: Optional agent filter ('claude', 'copilot', None for all)

        Returns:
            List of file dicts with 'path', 'source', 'required' keys
        """
        kit = self.get_kit(kit_name)
        if not kit:
            return []

        files = []
        file_groups = kit.get('files', {})

        # Map agent names to file groups
        agent_groups = {
            'claude': ['claude'],
            'copilot': ['copilot'],
            None: list(file_groups.keys())  # All groups
        }

        groups_to_include = agent_groups.get(agent, [])

        for group_name in groups_to_include:
            if group_name in file_groups:
                files.extend(file_groups[group_name])

        return files

    def get_kit_markers(self, kit_name: str) -> List[str]:
        """
        Get marker files for kit detection.

        Args:
            kit_name: Name of kit

        Returns:
            List of marker file paths
        """
        kit = self.get_kit(kit_name)
        return kit.get('markers', []) if kit else []

    def get_kit_commands(self, kit_name: str) -> List[Dict]:
        """
        Get list of commands for a kit.

        Args:
            kit_name: Name of kit

        Returns:
            List of command dicts with 'name', 'description', 'status' keys
        """
        kit = self.get_kit(kit_name)
        return kit.get('commands', []) if kit else []

    def get_agent_config(self, agent: str) -> Optional[Dict]:
        """
        Get agent configuration.

        Args:
            agent: Agent name ('claude', 'copilot')

        Returns:
            Agent config dict or None
        """
        return self.manifest.get('agents', {}).get(agent)

    def validate_kit_name(self, kit_name: str) -> bool:
        """Check if kit name is valid"""
        return kit_name in self.get_kit_names()

    def get_kit_description(self, kit_name: str) -> str:
        """Get kit description"""
        kit = self.get_kit(kit_name)
        return kit.get('description', '') if kit else ''

    def get_kit_icon(self, kit_name: str) -> str:
        """Get kit icon emoji"""
        kit = self.get_kit(kit_name)
        return kit.get('icon', '📦') if kit else '📦'

    def is_recommended(self, kit_name: str) -> bool:
        """Check if kit is recommended"""
        kit = self.get_kit(kit_name)
        return kit.get('recommended', False) if kit else False
