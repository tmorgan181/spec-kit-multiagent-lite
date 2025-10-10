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
        self.kits_dir = Path(__file__).parent.parent / "kits"
        self.kits = kits or ['project']  # Default to project kit only

        # Validate kit names
        valid_kits = {'project', 'git', 'multiagent'}
        invalid = set(self.kits) - valid_kits
        if invalid:
            raise ValueError(f"Invalid kit(s): {invalid}. Valid: {valid_kits}")

        # No auto-dependencies - all kits are independent

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
                self.target_dir / ".claude" / "commands" / "review.md",
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
                changes["new_files"].extend([
                    ".claude/commands/orient.md",
                    ".claude/commands/review.md",
                    ".claude/commands/audit.md",
                    ".claude/commands/stats.md",
                ])
            if has_copilot:
                changes["new_files"].extend([
                    ".github/prompts/orient.prompt.md",
                    ".github/prompts/review.prompt.md",
                    ".github/prompts/audit.prompt.md",
                    ".github/prompts/stats.prompt.md",
                ])

        # Git kit files
        if 'git' in self.kits:
            if has_claude:
                changes["new_files"].append(".claude/commands/commit.md")
                changes["new_files"].append(".claude/commands/pr.md")
                changes["new_files"].append(".claude/commands/review.md")
            if has_copilot:
                changes["new_files"].append(".github/prompts/commit.prompt.md")
                changes["new_files"].append(".github/prompts/pr.prompt.md")
                changes["new_files"].append(".github/prompts/review.prompt.md")

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
                    self._install_file('project/claude/commands/review.md', '.claude/commands/review.md')
                    self._install_file('project/claude/commands/audit.md', '.claude/commands/audit.md')
                    self._install_file('project/claude/commands/stats.md', '.claude/commands/stats.md')
                    result["installed"].append("project-kit (Claude): /orient, /review, /audit, /stats commands")

                if has_copilot:
                    self._install_file('project/github/prompts/orient.prompt.md', '.github/prompts/orient.prompt.md')
                    self._install_file('project/github/prompts/review.prompt.md', '.github/prompts/review.prompt.md')
                    self._install_file('project/github/prompts/audit.prompt.md', '.github/prompts/audit.prompt.md')
                    self._install_file('project/github/prompts/stats.prompt.md', '.github/prompts/stats.prompt.md')
                    result["installed"].append("project-kit (Copilot): /orient, /review, /audit, /stats commands")

            # Install git kit
            if 'git' in self.kits:
                if has_claude:
                    self._install_file('git/claude/commands/commit.md', '.claude/commands/commit.md')
                    self._install_file('git/claude/commands/pr.md', '.claude/commands/pr.md')
                    self._install_file('git/claude/commands/review.md', '.claude/commands/review.md')
                    self._install_file('git/claude/commands/cleanup.md', '.claude/commands/cleanup.md')
                    result["installed"].append("git-kit (Claude): /commit, /pr, /review, /cleanup commands")

                if has_copilot:
                    self._install_file('git/github/prompts/commit.prompt.md', '.github/prompts/commit.prompt.md')
                    self._install_file('git/github/prompts/pr.prompt.md', '.github/prompts/pr.prompt.md')
                    self._install_file('git/github/prompts/review.prompt.md', '.github/prompts/review.prompt.md')
                    self._install_file('git/github/prompts/cleanup.prompt.md', '.github/prompts/cleanup.prompt.md')
                    result["installed"].append("git-kit (Copilot): /commit, /pr, /review, /cleanup commands")

            # Install multiagent kit
            if 'multiagent' in self.kits and (self.target_dir / ".specify").exists():
                # Commands
                if has_claude:
                    self._install_file('multiagent/claude/commands/sync.md', '.claude/commands/sync.md')
                if has_copilot:
                    self._install_file('multiagent/github/prompts/sync.prompt.md', '.github/prompts/sync.prompt.md')

                # Memory guides
                self._install_file('multiagent/memory/pr-workflow-guide.md', '.specify/memory/pr-workflow-guide.md')
                self._install_file('multiagent/memory/git-worktrees-protocol.md', '.specify/memory/git-worktrees-protocol.md')
                self._install_file('multiagent/memory/parallel-work-protocol.md', '.specify/memory/parallel-work-protocol.md')

                # Templates
                templates_dir = self.target_dir / ".specify" / "templates"
                templates_dir.mkdir(parents=True, exist_ok=True)
                self._install_file('multiagent/templates/session-log.md', '.specify/templates/session-log.md')
                self._install_file('multiagent/templates/handoff.md', '.specify/templates/handoff.md')
                self._install_file('multiagent/templates/decision.md', '.specify/templates/decision.md')
                self._install_file('multiagent/templates/collaboration-structure/README.md', '.specify/templates/collaboration-README.md')

                result["installed"].append("multiagent-kit: /sync command")
                result["installed"].append("multiagent-kit: Memory guides (PR workflow, git worktrees, parallel work)")
                result["installed"].append("multiagent-kit: Templates (session-log, handoff, decision, collaboration)")

            result["success"] = True

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

        # Check project-kit files
        claude_orient = self.target_dir / ".claude" / "commands" / "orient.md"
        copilot_orient = self.target_dir / ".github" / "prompts" / "orient.prompt.md"

        project_kit_installed = claude_orient.exists() or copilot_orient.exists()
        checks["project_kit"] = {
            "passed": project_kit_installed,
            "message": "project-kit: /orient command found" if project_kit_installed
                      else "project-kit not installed - run: lite-kits add --here --kit project",
        }

        # Check git-kit files
        claude_commit = self.target_dir / ".claude" / "commands" / "commit.md"
        claude_pr = self.target_dir / ".claude" / "commands" / "pr.md"
        claude_review = self.target_dir / ".claude" / "commands" / "review.md"
        claude_cleanup = self.target_dir / ".claude" / "commands" / "cleanup.md"

        git_kit_installed = claude_commit.exists() or claude_pr.exists() or claude_review.exists() or claude_cleanup.exists()
        checks["git_kit"] = {
            "passed": git_kit_installed,
            "message": "git-kit: /commit, /pr, /review, /cleanup commands found" if git_kit_installed
                      else "git-kit not installed - run: lite-kits add --here --kit git",
        }

        # Check multiagent-kit files (only if user is checking for them)
        claude_sync = self.target_dir / ".claude" / "commands" / "sync.md"
        pr_guide = self.target_dir / ".specify" / "memory" / "pr-workflow-guide.md"
        worktree_guide = self.target_dir / ".specify" / "memory" / "git-worktrees-protocol.md"

        multiagent_kit_installed = claude_sync.exists() or pr_guide.exists() or worktree_guide.exists()
        checks["multiagent_kit"] = {
            "passed": multiagent_kit_installed,
            "message": "multiagent-kit: /sync command and memory guides found" if multiagent_kit_installed
                      else "multiagent-kit not installed - run: lite-kits add --here --kit multiagent",
        }

        # Only fail validation if NO kits are installed
        # If they only installed project+git, don't fail on missing multiagent
        all_passed = checks["project_kit"]["passed"] or checks["git_kit"]["passed"] or checks["multiagent_kit"]["passed"]

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
        result = {
            "success": False,
            "removed": [],
            "error": None,
        }

        try:
            # Remove project kit files
            if 'project' in self.kits:
                removed = []
                project_commands = ['orient', 'review', 'audit', 'stats']
                
                # Claude
                for cmd in project_commands:
                    cmd_file = self.target_dir / ".claude" / "commands" / f"{cmd}.md"
                    if cmd_file.exists():
                        cmd_file.unlink()
                        removed.append(f".claude/commands/{cmd}.md")

                # Copilot
                for cmd in project_commands:
                    cmd_file = self.target_dir / ".github" / "prompts" / f"{cmd}.prompt.md"
                    if cmd_file.exists():
                        cmd_file.unlink()
                        removed.append(f".github/prompts/{cmd}.prompt.md")

                if removed:
                    result["removed"].append(f"project-kit: {', '.join(removed)}")

            # Remove git kit files
            if 'git' in self.kits:
                removed = []
                git_commands = ['commit', 'pr', 'review', 'cleanup']

                # Claude
                for cmd in git_commands:
                    cmd_file = self.target_dir / ".claude" / "commands" / f"{cmd}.md"
                    if cmd_file.exists():
                        cmd_file.unlink()
                        removed.append(f".claude/commands/{cmd}.md")

                # Copilot
                for cmd in git_commands:
                    cmd_file = self.target_dir / ".github" / "prompts" / f"{cmd}.prompt.md"
                    if cmd_file.exists():
                        cmd_file.unlink()
                        removed.append(f".github/prompts/{cmd}.prompt.md")

                if removed:
                    result["removed"].append(f"git-kit: {', '.join(removed)}")

            # Remove multiagent kit files
            if 'multiagent' in self.kits:
                removed = []

                # Sync command
                sync_claude = self.target_dir / ".claude" / "commands" / "sync.md"
                if sync_claude.exists():
                    sync_claude.unlink()
                    removed.append(".claude/commands/sync.md")

                sync_copilot = self.target_dir / ".github" / "prompts" / "sync.prompt.md"
                if sync_copilot.exists():
                    sync_copilot.unlink()
                    removed.append(".github/prompts/sync.prompt.md")

                # Memory guides
                memory_files = [
                    'pr-workflow-guide.md',
                    'git-worktrees-protocol.md',
                    'parallel-work-protocol.md',
                ]
                for file in memory_files:
                    file_path = self.target_dir / ".specify" / "memory" / file
                    if file_path.exists():
                        file_path.unlink()
                        removed.append(f".specify/memory/{file}")

                # Templates
                template_files = [
                    'session-log.md',
                    'handoff.md',
                    'decision.md',
                    'collaboration-README.md',
                ]
                for file in template_files:
                    file_path = self.target_dir / ".specify" / "templates" / file
                    if file_path.exists():
                        file_path.unlink()
                        removed.append(f".specify/templates/{file}")

                if removed:
                    result["removed"].append(f"multiagent-kit: {', '.join(removed)}")

            # Note: Preserve collaboration directories (user data)
            # Note: Preserve vanilla spec-kit files

            result["success"] = True

        except Exception as e:
            result["error"] = str(e)

        return result
