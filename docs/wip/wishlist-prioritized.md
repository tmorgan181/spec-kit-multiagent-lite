# Lite-Kits Wishlist - v0.4 Planning

**Last Updated**: 2025-10-10
**Current Status**: v0.3.0 complete (ready for merge) → Planning v0.4

---

## ✅ v0.3 COMPLETE

**Theme**: Polish + Quick Wins for PyPI Launch

**Shipped Features** (6 total):
1. ✅ **Command audit** - Fixed 26 files with outdated kit references (project-kit/git-kit → dev-kit)
2. ✅ **Better error messages** - Spec-kit not found includes installation instructions with links
3. ✅ **Preview kit headers** - Shows kit names in preview output
4. ✅ **Delete empty folders** - Cleanup after kit removal
5. ✅ **README prerequisites** - Complete installation flow with dependency chain
6. ✅ **Constitution template** - Filled in lite-kits project constitution (v1.0.0)

**Status**: Ready for merge to main, tag v0.3.0, and PyPI publish 🚀

---

## 🎯 v0.4 GOALS

**Theme**: Release Management & Safety Nets

**Target Features** (3-4 for next session):

### Checkpoint System 🔥
**Inspired by**: claudekit checkpoints
- `/checkpoint` - Create git stash checkpoint before risky changes
- `/checkpoint:restore [id]` - Restore from checkpoint
- `/checkpoint:list` - Show available checkpoints
- Auto-cleanup old checkpoints (keep last 10)

**Benefit**: Safety net for refactoring, easy rollback without git expertise

### Release Management Commands 🔥
**Streamline the release workflow**:
- `/bump [major|minor|patch]` - Version bump with changelog template
- `/tag` - Create annotated git tag with version
- `/release` - Create GitHub release with changelog excerpt
- Integration with `/audit` and `/stats` for release quality checks

**Benefit**: We just did v0.3 manually, automate this!

### Testing Infrastructure
**Missing piece from constitution**:
- Basic test framework setup (pytest)
- Tests for installer, detector, validator
- CI workflow for running tests
- Coverage reporting

**Benefit**: Confidence in changes, catch regressions

### Command Enhancements
**Pick 1-2**:
- `/status` - Optimized git status (reduce tool calls for Claude)
- `/audit` polish - Better security checks, dependency scanning
- `/stats` polish - Code complexity, test coverage, commit velocity

---

## 🚀 FUTURE RELEASES (v0.5+)

### Web Discovery Interface (v0.5) 🆕
**Inspired by**: Claude Code Templates (aitmpl.com)
- GitHub Pages site to browse commands
- Interactive component selector
- Installation preview

### Health Check & Analytics (v0.5) 🆕
**Inspired by**: Claude Code Templates monitoring
- `lite-kits doctor` - Validate installation and dependencies
- `lite-kits analytics` - Track command usage (opt-in)
- Health dashboard

### Spec-Kit Integration (v0.6)
**One-stop setup**:
- `lite-kits init` - Launch specify to initialize spec-kit
- `lite-kits spec install/remove/upgrade` - Manage spec-kit
- Auto-detection of specify location

### Hook System (v0.6) 🆕
**Inspired by**: claudekit hooks
- Pre-commit hooks (lint, test, security)
- Post-install hooks (setup, config)
- Custom hook templates

### Namespace Organization (v0.7) 🆕
**Inspired by**: wshobson/commands (57 commands), Claude-Command-Suite (148 commands)
- `/dev:` - Development commands
- `/test:` - Testing utilities
- `/security:` - Security tools
- `/deploy:` - Deployment workflows

**Note**: Only consider this when we have 20+ commands. For now, flat namespace is fine.

### Script Standardization & Prompt Optimization (v1.0) 🔥
**Problem**: Commands rely on agents making many tool calls, prompts could be more efficient
**Current pain**:
- Claude Code makes 5-10 tool calls for simple git operations
- Prompts don't guide agents to batch operations efficiently
- No helper scripts for repeatable multi-step tasks
**Solution**:
- Helper scripts for common multi-step operations
- Optimized prompts that reduce tool call count
- Batch operation patterns (e.g., single git command instead of 3 separate calls)
**Examples**:
- `scripts/bash/get-git-status.sh` - Returns branch, commits ahead/behind, changes in ONE call
- `scripts/bash/get-git-context.sh` - All git context for /commit in ONE call
- `/orient` prompt: Use pre-built script instead of 8 individual bash calls
- `/commit` prompt: Single status check instead of 3-4 separate git commands
**Benefit**:
- Faster command execution (50% fewer tool calls)
- More reliable (atomic operations)
- Better user experience (less waiting)

---

## 📦 BACKLOG (Ideas from research)

**From Claude Code Enhancement Mods**:
- Multi-agent coordination (parallel code review agents)
- AI thinking modes (prime, sentient, ultra-think)
- Real-time guardrails (file protection, pattern enforcement)
- Session checkpointing and history navigation
- Plugin marketplace integration

**Code Quality & DRY Improvements**:
- **Kit Folder Organization in Agent Directories** 🔥 - Improve command organization
  - **Problem**: Currently all commands flat in `.claude/commands/` and `.github/prompts/`
  - **Current structure**:
    ```
    .claude/commands/
      orient.md
      commit.md
      pr.md
      review.md
      cleanup.md
      audit.md
      stats.md
      sync.md (if multiagent installed)
    ```
  - **Proposed structure**:
    ```
    .claude/commands/
      dev/
        orient.md
        commit.md
        pr.md
        review.md
        cleanup.md
        audit.md
        stats.md
      multiagent/
        sync.md
    ```
  - **Benefits**:
    - Clear kit ownership (easy to see which commands belong to which kit)
    - Easier to add/remove specific kits
    - Scales better as more kits are added
    - Mirrors source structure in `src/lite_kits/kits/`
  - **Considerations**:
    - Need to verify Claude Code and GitHub Copilot support nested slash commands
    - May need path updates in command references
    - Migration path for existing installations
  - **Estimated effort**: 1-2 hours for manifest updates, migration logic
- **DRY Command Templating** 🔥🔥🔥 - Single source of truth for commands
  - **Problem**: Maintaining duplicate `.claude/commands/*.md` AND `.github/prompts/*.prompt.md` files
  - **Current pain**: 16 files to maintain (8 commands × 2 versions), bash/PowerShell sync issues
  - **Solution**: Template-based approach with agent/shell interpolation
  - **Implementation ideas**:
    - Option A: Jinja2 templates with `{% if shell == 'bash' %}...{% elif shell == 'powershell' %}...{% endif %}`
    - Option B: Single markdown with embedded code fence annotations (```bash vs ```powershell)
    - Option C: YAML command spec + template engine → generates both versions at install time
  - **Benefits**:
    - One file to maintain per command (8 instead of 16)
    - Automatic consistency between Claude/Copilot versions
    - Easier to add new agents (just add new shell variant)
    - No more sync bugs like sync.prompt.md having bash syntax
  - **Example structure**:
    ```
    src/lite_kits/kits/dev/commands/templates/
      commit.md.j2         # Single template
      orient.md.j2         # Single template
      pr.md.j2             # Single template
    ```
  - **Manifest integration**: `kits.yaml` specifies which templates to render for which agents
  - **Estimated effort**: 2-3 hours to implement, saves hours in ongoing maintenance
- Use constants in core/installer.py (like we did for cli.py)
- Consolidate version numbers and common strings
- Type hints consistency across modules

**Original Ideas**:
- Multi-agent workflow improvements beyond current multiagent-kit
- Installation analytics/telemetry (opt-in, privacy-preserving)
- Kit templates for custom kits (community contributions)
- Community kit repository
- Templates for CLAUDE.md and copilot-instructions.md

---

## 🏁 v0.4 SHIP CHECKLIST (Template)

**Pre-implementation**:
- [ ] Review v0.4 candidates and finalize scope
- [ ] Create implementation plan or delegate to /plan

**Implementation**:
- [ ] Implement selected features
- [ ] Write tests (if testing infrastructure exists)
- [ ] Manual validation testing
- [ ] Update CHANGELOG.md

**Release**:
- [ ] Bump version to 0.4.0
- [ ] Commit and tag
- [ ] Create GitHub release
- [ ] Publish to PyPI

---

## 💭 NOTES

**v0.3.0 Achievements**:
- ✅ Command audit (26 files fixed)
- ✅ Better error messages (install guidance)
- ✅ Preview UX improvements (kit headers)
- ✅ Empty folder cleanup
- ✅ README overhaul (installation flow)
- ✅ Constitution v1.0.0
- ✅ Ready for PyPI publish

**v0.4 Priority Rationale**:
- **Checkpoints**: Safety is critical for AI-assisted refactoring
- **Release commands**: We just did manual release, let's automate it
- **Testing**: Constitution says tests required, need infrastructure
- **Command polish**: Nice-to-have, pick 1-2 based on time

**Philosophy**: Ship early, iterate fast. v0.4 should focus on developer experience (checkpoints + release automation).

**Research Reminder**: We have excellent ideas from claudekit, wshobson/commands, and Claude-Command-Suite to draw from. Don't reinvent wheels, adapt their best patterns.
