"""
Installer logic for spec-kit-multiagent

Handles installation, removal, and validation of multiagent features.
"""

import shutil
from pathlib import Path
from typing import Dict, List, Optional


class Installer:
    """Manages installation of multiagent features to spec-kit projects."""

    def __init__(self, target_dir: Path, kits: Optional[List[str]] = None):
        """
        Initialize installer.

        Args:
            target_dir: Target spec-kit project directory
            kits: List of kits to install (project, git, multiagent). Defaults to ['project']
        """
        self.target_dir = Path(target_dir).resolve()
        self.kits_dir = Path(__file__).parent / "kits"
        self.kits = kits or ['project']  # Default to project kit only

        # Validate kit names
        valid_kits = {'project', 'git', 'multiagent'}
        invalid = set(self.kits) - valid_kits
        if invalid:
            raise ValueError(f"Invalid kit(s): {invalid}. Valid: {valid_kits}")

        # Auto-include dependencies
        # multiagent requires both project and git
        if 'multiagent' in self.kits:
            if 'project' not in self.kits:
                self.kits.append('project')
            if 'git' not in self.kits:
                self.kits.append('git')

    def is_spec_kit_project(self) -> bool:
        """
        Check if target directory is a spec-kit project.

        Returns:
            True if directory contains spec-kit markers
        """
        markers = [
            self.target_dir / ".specify",
            self.target_dir / ".claude",
            self.target_dir / ".github" / "prompts",
        ]
        return any(marker.exists() for marker in markers)

    def is_multiagent_installed(self) -> bool:
        """
        Check if multiagent features are already installed.

        Returns:
            True if multiagent features detected
        """
        # Check for kit markers
        markers = {
            'project': [
                self.target_dir / ".claude" / "commands" / "orient.md",
                self.target_dir / ".github" / "prompts" / "orient.prompt.md",
            ],
            'git': [
                self.target_dir / ".claude" / "commands" / "commit.md",
                self.target_dir / ".github" / "prompts" / "commit.prompt.md",
            ],
            'multiagent': [
                self.target_dir / ".specify" / "memory" / "pr-workflow-guide.md",
            ],
        }

        # Check if any requested kit is already installed
        for kit in self.kits:
            if any(marker.exists() for marker in markers.get(kit, [])):
                return True

        return False

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

        # Check which interface(s) exist
        has_claude = (self.target_dir / ".claude").exists()
        has_copilot = (self.target_dir / ".github" / "prompts").exists()

        # Project kit files
        if 'project' in self.kits:
            if has_claude:
                changes["new_files"].append(".claude/commands/orient.md")
            if has_copilot:
                changes["new_files"].append(".github/prompts/orient.prompt.md")

        # Git kit files
        if 'git' in self.kits:
            if has_claude:
                changes["new_files"].append(".claude/commands/commit.md")
                changes["new_files"].append(".claude/commands/pr.md")
            if has_copilot:
                changes["new_files"].append(".github/prompts/commit.prompt.md")
                changes["new_files"].append(".github/prompts/pr.prompt.md")

        # Multiagent kit files
        if 'multiagent' in self.kits and (self.target_dir / ".specify").exists():
            changes["new_files"].extend([
                ".specify/memory/pr-workflow-guide.md",
                ".specify/memory/git-worktrees-protocol.md",
            ])
            changes["new_directories"].append("specs/*/collaboration/ (created with new features)")

        return changes

    def install(self) -> Dict:
        """
        Install multiagent features to target project.

        Returns:
            Dictionary with success status and installed items
        """
        result = {
            "success": False,
            "installed": [],
            "error": None,
        }

        try:
            # Detect which interfaces are present
            has_claude = (self.target_dir / ".claude").exists()
            has_copilot = (self.target_dir / ".github" / "prompts").exists()

            if not has_claude and not has_copilot:
                result["error"] = "No supported AI interface found (.claude or .github/prompts)"
                return result

            # Install project kit
            if 'project' in self.kits:
                if has_claude:
                    self._install_file('project/claude/commands/orient.md', '.claude/commands/orient.md')
                    result["installed"].append("project-kit (Claude): /orient command")

                if has_copilot:
                    self._install_file('project/github/prompts/orient.prompt.md', '.github/prompts/orient.prompt.md')
                    result["installed"].append("project-kit (Copilot): /orient command")

            # Install git kit (not implemented yet, but structure ready)
            if 'git' in self.kits:
                # TODO: Implement git kit installation when files are ready
                # if has_claude:
                #     self._install_file('git/claude/commands/commit.md', '.claude/commands/commit.md')
                #     self._install_file('git/claude/commands/pr.md', '.claude/commands/pr.md')
                #     result["installed"].append("git-kit (Claude): /commit, /pr commands")
                #
                # if has_copilot:
                #     self._install_file('git/github/prompts/commit.prompt.md', '.github/prompts/commit.prompt.md')
                #     self._install_file('git/github/prompts/pr.prompt.md', '.github/prompts/pr.prompt.md')
                #     result["installed"].append("git-kit (Copilot): /commit, /pr commands")
                result["installed"].append("git-kit: (files not yet implemented)")

            # Install multiagent kit
            if 'multiagent' in self.kits and (self.target_dir / ".specify").exists():
                self._install_file('multiagent/memory/pr-workflow-guide.md', '.specify/memory/pr-workflow-guide.md')
                self._install_file('multiagent/memory/git-worktrees-protocol.md', '.specify/memory/git-worktrees-protocol.md')
                result["installed"].append("multiagent-kit: PR workflow guide")
                result["installed"].append("multiagent-kit: Git worktrees protocol")

            result["success"] = True

        except Exception as e:
            result["error"] = str(e)

        return result

    def validate(self) -> Dict:
        """
        Validate multiagent installation.

        Returns:
            Dictionary with validation results
        """
        checks = {}

        # Check orient command exists
        claude_orient = self.target_dir / ".claude" / "commands" / "orient.md"
        copilot_orient = self.target_dir / ".github" / "prompts" / "orient.prompt.md"

        checks["orient_command"] = {
            "passed": claude_orient.exists() or copilot_orient.exists(),
            "message": "Orient command found" if (claude_orient.exists() or copilot_orient.exists())
                      else "Orient command missing - run: speckit-ma add --here",
        }

        # Check memory guides
        pr_guide = self.target_dir / ".specify" / "memory" / "pr-workflow-guide.md"
        worktree_guide = self.target_dir / ".specify" / "memory" / "git-worktrees-protocol.md"

        checks["pr_workflow_guide"] = {
            "passed": pr_guide.exists(),
            "message": "PR workflow guide found" if pr_guide.exists()
                      else "PR workflow guide missing",
        }

        checks["git_worktrees_protocol"] = {
            "passed": worktree_guide.exists(),
            "message": "Git worktrees protocol found" if worktree_guide.exists()
                      else "Git worktrees protocol missing",
        }

        # TODO: Check collaboration structure in existing specs
        # specs_dir = self.target_dir / "specs"
        # if specs_dir.exists():
        #     for spec_dir in specs_dir.iterdir():
        #         if spec_dir.is_dir():
        #             collab_dir = spec_dir / "collaboration"
        #             # Check structure...

        # TODO: Check constitution has multiagent sections
        # constitution = self.target_dir / ".specify" / "memory" / "constitution.md"
        # if constitution.exists():
        #     # Check for multiagent markers...

        all_passed = all(check["passed"] for check in checks.values())

        return {
            "valid": all_passed,
            "checks": checks,
        }

    # Private installation methods

    def _install_file(self, kit_relative_path: str, target_relative_path: str):
        """
        Install a file from kits directory to target project.

        Args:
            kit_relative_path: Path relative to kits/ directory (e.g., 'project/claude/commands/orient.md')
            target_relative_path: Path relative to target directory (e.g., '.claude/commands/orient.md')
        """
        source = self.kits_dir / kit_relative_path
        target = self.target_dir / target_relative_path

        if not source.exists():
            raise FileNotFoundError(f"Kit file not found: {source}")

        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    # TODO: Implement these methods

    def _merge_constitution(self):
        """
        Merge multiagent sections into existing constitution.

        Strategy:
        1. Read existing constitution
        2. Check for multiagent marker (<!-- MULTIAGENT-START -->)
        3. If marker exists, replace section
        4. If marker missing, append section
        5. Preserve user edits outside markers
        """
        # TODO: Implement smart merge logic
        # - Read templates/enhancements/constitution-multiagent.md
        # - Merge into .specify/memory/constitution.md
        # - Use marker comments for idempotent updates
        pass

    def _install_collaboration_template(self):
        """
        Create collaboration directory template.

        Creates:
        - .specify/templates/collaboration-template/
        - Scripts reference this when creating new features
        """
        # TODO: Create collaboration directory template
        # - active/
        # - archive/
        # - results/
        pass

    def remove(self) -> Dict:
        """
        Remove multiagent features from project.

        Returns to vanilla spec-kit state.

        Returns:
            Dictionary with success status and removed items
        """
        # TODO: Implement removal logic
        # - Remove orient commands
        # - Remove memory guides
        # - Remove multiagent sections from constitution
        # - Preserve collaboration directories (user data)
        result = {
            "success": False,
            "removed": [],
            "error": "Not yet implemented",
        }
        return result
