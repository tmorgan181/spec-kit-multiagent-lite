"""
Installer logic for spec-kit-multiagent

Handles installation, removal, and validation of multiagent features.
"""

import shutil
from pathlib import Path
from typing import Dict, List, Optional


class Installer:
    """Manages installation of multiagent features to spec-kit projects."""

    def __init__(self, target_dir: Path):
        """
        Initialize installer.

        Args:
            target_dir: Target spec-kit project directory
        """
        self.target_dir = Path(target_dir).resolve()
        self.templates_dir = Path(__file__).parent / "templates"

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
        # Check for orient command in either Claude or GitHub Copilot location
        claude_orient = self.target_dir / ".claude" / "commands" / "orient.md"
        copilot_orient = self.target_dir / ".github" / "prompts" / "orient.prompt.md"

        return claude_orient.exists() or copilot_orient.exists()

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

        # Orient command
        if has_claude:
            changes["new_files"].append(".claude/commands/orient.md")
        if has_copilot:
            changes["new_files"].append(".github/prompts/orient.prompt.md")

        # Memory guides
        if (self.target_dir / ".specify").exists():
            changes["new_files"].extend([
                ".specify/memory/pr-workflow-guide.md",
                ".specify/memory/git-worktrees-protocol.md",
            ])

        # TODO: Check for constitution modifications
        # if (self.target_dir / ".specify" / "memory" / "constitution.md").exists():
        #     changes["modified_files"].append(".specify/memory/constitution.md")

        # Collaboration structure (created on first /specify)
        # Not created during install, just noted
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

            # Install orient command
            if has_claude:
                self._install_claude_orient()
                result["installed"].append("Claude Code: /orient command")

            if has_copilot:
                self._install_copilot_orient()
                result["installed"].append("GitHub Copilot: /orient command")

            # Install memory guides
            if (self.target_dir / ".specify").exists():
                self._install_memory_guides()
                result["installed"].append("Memory: PR workflow guide")
                result["installed"].append("Memory: Git worktrees protocol")

            # TODO: Merge constitution
            # self._merge_constitution()
            # result["installed"].append("Constitution: Multiagent sections")

            # TODO: Create collaboration structure template
            # self._install_collaboration_template()
            # result["installed"].append("Templates: Collaboration directory structure")

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

    def _install_claude_orient(self):
        """Install orient command for Claude Code."""
        source = self.templates_dir / "commands" / "orient.md"
        target = self.target_dir / ".claude" / "commands" / "orient.md"

        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    def _install_copilot_orient(self):
        """Install orient command for GitHub Copilot."""
        source = self.templates_dir / "commands" / "orient.md"
        target = self.target_dir / ".github" / "prompts" / "orient.prompt.md"

        target.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(source, target)

    def _install_memory_guides(self):
        """Install memory guides (PR workflow, git worktrees)."""
        memory_dir = self.target_dir / ".specify" / "memory"
        memory_dir.mkdir(parents=True, exist_ok=True)

        guides = [
            "pr-workflow-guide.md",
            "git-worktrees-protocol.md",
        ]

        for guide in guides:
            source = self.templates_dir / "memory" / guide
            target = memory_dir / guide
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
