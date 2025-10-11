# Changelog

All notable changes to lite-kits will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

---

## [0.3.0] - 2025-10-10

**Polish Release: PyPI Launch Preparation**

This release focuses on user experience polish and documentation improvements in preparation for the first public PyPI release.

### Added

**UX Improvements:**
- Kit name headers in preview output (easier to see what each kit installs)
- Empty directory cleanup after kit removal (cleaner uninstall experience)
- Comprehensive installation flow in README (step-by-step from spec-kit to first command)
- AI assistant compatibility section in README (clarifies GitHub Copilot + Claude Code support)

**Documentation:**
- Project constitution (v1.0.0) - Core principles and development standards
- Dependency audit report - Validates sparkling dependency story for PyPI
- Enhanced README prerequisites with links to all dependencies
- Clarified spec-kit as REQUIRED dependency (not optional)

### Changed

**Error Messages:**
- Spec-kit not found error now includes installation instructions
- Links to Node.js and spec-kit GitHub repo
- Clear explanation that lite-kits enhances spec-kit
- Updated next steps to mention GitHub Copilot first

**Command Files:**
- Fixed all outdated kit references (project-kit/git-kit → dev-kit)
- Updated orient command detection logic (removed redundant checks)
- Consistent kit naming across 26 files

### Fixed

**Critical:**
- Command audit found and fixed 26 files with outdated kit names
- Orient command now correctly detects "dev" kit instead of "project, git"
- All cross-command references verified for accuracy

**Documentation:**
- README installation flow now shows complete dependency chain
- Prerequisites section clarifies Node.js requirement (for spec-kit)
- AI assistant compatibility explained (works with multiple agents)

### Documentation

**Updated:**
- README.md - Complete installation flow overhaul
- CHANGELOG.md - This release!
- .specify/memory/constitution.md - Project principles and standards

**New:**
- docs/validation/v0.3.0-dependency-audit.md - Dependency analysis
- docs/validation/v0.3.0-command-audit.md - Complete command audit report
- docs/wip/wishlist-prioritized.md - Feature roadmap for v0.4+

### Technical Improvements

**Code Quality (Last-Minute Polish):**
- Extracted constants to `__init__.py` for single source of truth
  - Version, app name, kit names, directory paths, error messages
  - Reduced code duplication across cli.py and installer.py
  - All version/identifier references now use constants
- Command audit performed on all 16 command files (8 commands × 2 agents)
  - Verified bash and PowerShell versions match logically
  - Fixed sync.prompt.md having bash syntax instead of PowerShell
  - All cross-command references verified for accuracy

**Bug Fixes (Last-Minute):**
- Agent detection now works when only parent directory exists (e.g., `.github/` without `.github/prompts/`)
  - Copilot detection was failing if `.github/prompts/` didn't exist yet
  - Now detects `.github/` and creates subdirectory on install
  - More flexible detection that doesn't require full path structure upfront

**Planning for v0.4:**
- Updated wishlist with DRY command templating (🔥🔥🔥 priority)
  - Eliminate duplicate .claude + .github files (16 → 8 templates)
  - Single source of truth with shell/agent interpolation
- Added prompt optimization + script standardization
  - Reduce tool call count (Claude makes 5-10 calls for simple git ops)
  - Helper scripts for repeatable multi-step tasks

### Release Notes

This polish release makes lite-kits PyPI-ready with improved error messages, clearer documentation, and verified command accuracy. All user-facing text has been audited for consistency and clarity.

**Key improvements for new users:**
- Installation flow is crystal clear (prerequisites → install → use)
- Error messages guide users through setup (not just "something's wrong")
- Commands are accurate and tested (no broken cross-references)

Ready for PyPI! 🚀

---

## [0.2.0] - 2025-10-10

**Major Release: Manifest-Driven Architecture & UX Polish**

This release represents a complete rewrite of lite-kits with a focus on modularity, extensibility, and professional UX.

### Added

**Core Features:**
- Manifest-driven installer (kits.yaml as single source of truth)
- Modular installer architecture (detector, validator, conflict_checker, installer)
- Content-first kit structure (easy to add new agents/shells/commands)
- Preview-first operations (always show changes before applying)
- Smart auto-detection (agents and shells with explicit override flags)
- Conflict checking before installation

**UX Improvements:**
- File count summaries in previews ("Total files to install: 14")
- `help` command that accepts optional command argument (`lite-kits help add`)
- Perfect terminal spacing (leading/trailing newlines on all commands)
- Useful help description (shows quick start instead of repeating tagline)
- `--force` flag for remove command (skip preview and confirmations)
- Banner works with all commands via `--banner` flag (not just standalone)

**Documentation:**
- Comprehensive manifest schema documentation (docs/manifest-schema.md)
- Installer design documents
- Human validation test results

### Changed

**Kit Structure:**
- Consolidated project-kit + git-kit → **dev-kit** (all solo development commands)
- New file layout: `kits/{kit-name}/commands/{command-name}.{agent}.md`
- Removed agent/shell subdirectories in favor of file extensions
- Single manifest defines all kit metadata and file mappings

**Commands:**
- `/orient` - Now in dev-kit (was project-kit)
- `/commit` - Now in dev-kit (was git-kit)
- `/pr` - Now in dev-kit (was git-kit)
- `/review` - Now in dev-kit (was git-kit)
- `/cleanup` - Now in dev-kit (was git-kit)
- `/audit` - Now in dev-kit (was project-kit)
- `/stats` - Now in dev-kit (was project-kit)
- `/sync` - Remains in multiagent-kit

**CLI:**
- Help description changed from tagline to actionable quick start
- Improved preview formatting (cleaner, more professional)
- Better error messages and validation
- Consistent `--force` behavior across add and remove

### Fixed

**Critical Bugs:**
- #1: Preview not showing before installation
- #3: Preview confirmation flow issues
- #4: Empty sections showing in preview
- #6: Wrong kits shown in status command
- #7: Duplicate banner in help output

**Other Fixes:**
- Preview confirmation flow (don't skip when user confirms reinstall)
- Duplicate tagline in help output when using `--banner`
- Banner callback logic cleaned up
- Windows console Unicode handling (graceful fallback)

### Architecture

**New Modular Design:**
- `detector.py` - Auto-detect agents, shells, and project type
- `validator.py` - Validate kit installation and integrity
- `conflict_checker.py` - Check for file conflicts before installation
- `installer.py` - Main orchestrator (manifest-driven, no hardcoded logic)
- `manifest.py` - YAML manifest parser and query interface

**Benefits:**
- Zero hardcoded kit IDs or file paths
- Easy to add new commands (just add file + manifest entry)
- Easy to add new agents/shells (just add file variant)
- Separation of concerns (each module has single responsibility)
- Better error handling and validation

### Removed

- Old monolithic installer with hardcoded kit logic
- Separate project-kit and git-kit (consolidated into dev-kit)
- Agent-specific subdirectories (claude/, github/)
- Duplicate files in root (.github/prompts/, .specify/)
- Installer prototype files (installer_old.py, installer_v2.py)

---

## [0.1.1] - 2025-10-08

**Polish Release: Beautiful CLI Experience**

### Added

**Banner System:**
- Beautiful ASCII art LITE-KITS branding
- Static banners for daily use
- Animated diagonal reveal for special moments (`--banner` flag)
- Professional UV-inspired CLI patterns

**Global Options:**
- `--version` / `-V` - Show version
- `--quiet` / `-q` - Suppress banners
- `--verbose` / `-v` - Extra output
- `--directory` - Set working directory

**Professional Output:**
- Clean information displays
- Professional tables for status and info
- Context-aware kit status display

### Changed

- CLI rebrand: `install` → `add` command
- Improved flag consistency
- Better help text and descriptions

### Fixed

- Windows encoding issues (ASCII-safe status indicators)
- Installer kit mappings (sync in multiagent, cleanup in git)
- Shell completion disabled (no profile modifications)

---

## [0.1.0] - 2025-10-07

**Initial Release: Foundation**

### Added

**Core Features:**
- Package structure with clean architecture
- Kit-based modular design
- CLI with kit and package management

**Kits:**
- **git-kit**: `/commit`, `/pr`, `/cleanup` commands
- **project-kit**: `/orient`, `/audit`, `/stats`, `/review` commands
- **multiagent-kit**: `/sync` command, collaboration structure, memory guides

**Cross-Platform Support:**
- Bash scripts for Linux/macOS
- PowerShell scripts for Windows
- Both Claude Code and GitHub Copilot support

**Installation:**
- Proper pip/uv tool installation
- No shell profile modifications
- Safe add/remove operations

### Philosophy

**Enhance, Don't Replace:**
- Add-on for vanilla spec-kit (not a fork)
- Get upstream updates automatically
- Modular kits (add/remove as needed)
- No file replacements (only adds new files)

---

## Release Notes

### v0.2.0 Highlights

This is the biggest release yet! We've completely rewritten the installer architecture to be:
- **Manifest-driven**: All kit metadata in one place (kits.yaml)
- **Modular**: Clean separation of concerns across 4 focused modules
- **Extensible**: Easy to add new commands, agents, shells, and content types
- **Professional**: Perfect UX with proper spacing, file counts, and help system

The kit consolidation (project + git → dev) makes lite-kits simpler to understand and use, while the content-first structure makes it easier for contributors to add new features.

### Migration from v0.1.x to v0.2.0

If you have v0.1.x installed:

```bash
# Remove old kits
lite-kits remove --all

# Upgrade package
pip install --upgrade lite-kits

# Add new dev-kit (replaces project + git)
lite-kits add
```

The dev-kit includes all commands from the old project-kit and git-kit, so you won't lose any functionality.

---

[0.3.0]: https://github.com/tmorgan181/lite-kits/releases/tag/v0.3.0
[0.2.0]: https://github.com/tmorgan181/lite-kits/releases/tag/v0.2.0
[0.1.1]: https://github.com/tmorgan181/lite-kits/releases/tag/v0.1.1
[0.1.0]: https://github.com/tmorgan181/lite-kits/releases/tag/v0.1.0
