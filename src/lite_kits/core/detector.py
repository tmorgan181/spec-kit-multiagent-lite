"""
Agent and shell detection for lite-kits installer.

Detects which AI agents and shell environments are present in a project.
"""

from pathlib import Path
from typing import List, Optional

from .manifest import KitManifest


class Detector:
    """Detects agents and shells in target project."""

    def __init__(self, target_dir: Path, manifest: KitManifest):
        """
        Initialize detector.

        Args:
            target_dir: Target project directory
            manifest: Loaded kit manifest
        """
        self.target_dir = target_dir
        self.manifest = manifest

    def detect_agents(self, preferred: Optional[str] = None) -> List[str]:
        """
        Auto-detect which AI agents are present.

        Args:
            preferred: Explicit agent preference (overrides auto-detection)

        Returns:
            List of agent names sorted by priority
        """
        # If explicit preference, validate and return
        if preferred:
            config = self.manifest.get_agent_config(preferred)
            if not config:
                raise ValueError(f"Unknown agent: {preferred}")
            if not config.get('supported', False):
                raise ValueError(f"Agent not supported: {preferred}")
            return [preferred]

        # Auto-detect from manifest
        detected = []
        agents = self.manifest.manifest.get('agents', {})

        for agent_name, config in agents.items():
            if not config.get('supported', False):
                continue

            marker_dir = self.target_dir / config['marker_dir']
            if marker_dir.exists():
                detected.append({
                    'name': agent_name,
                    'priority': config.get('priority', 999)
                })

        # Sort by priority (lower = higher)
        detected.sort(key=lambda x: x['priority'])
        return [agent['name'] for agent in detected]

    def detect_shells(self, preferred: Optional[str] = None) -> List[str]:
        """
        Determine which shells to install for.

        Args:
            preferred: Explicit shell preference (overrides auto-detection)

        Returns:
            List of shell names
        """
        # If explicit preference, validate and return
        if preferred:
            config = self.manifest.manifest.get('shells', {}).get(preferred)
            if not config:
                raise ValueError(f"Unknown shell: {preferred}")
            if not config.get('supported', False):
                raise ValueError(f"Shell not supported: {preferred}")
            return [preferred]

        # Check if shell detection is enabled
        options = self.manifest.manifest.get('options', {})
        if not options.get('auto_detect_shells', True):
            return []

        # Get all supported shells
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

        # Return all or just primary based on options
        if options.get('prefer_all_shells', False):
            return [shell['name'] for shell in detected]

        return [detected[0]['name']] if detected else []

    def is_spec_kit_project(self) -> bool:
        """
        Check if target is a spec-kit project.

        Returns:
            True if spec-kit markers found
        """
        spec_config = self.manifest.manifest.get('spec_kit', {})
        markers = spec_config.get('markers', [])
        require_any = spec_config.get('require_any', True)

        found = []
        for marker in markers:
            path = self.target_dir / marker['path']

            if marker.get('type') == 'directory':
                if path.is_dir():
                    found.append(marker['path'])
            else:
                if path.exists():
                    found.append(marker['path'])

        # Check requirement
        if require_any:
            return len(found) > 0

        return len(found) == len(markers)
