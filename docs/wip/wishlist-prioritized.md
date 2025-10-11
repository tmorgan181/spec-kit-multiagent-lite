# Lite-Kits Wishlist - v0.3 Planning

**Last Updated**: 2025-10-10
**Current Status**: v0.2.0 shipped, planning v0.3.0 → PyPI first publish 🚀

---

## 🎯 v0.3 GOALS

**Theme**: Polish + Quick Wins for PyPI Launch

**Target Features** (pick 5-6 for tonight):
1. **Quick UX polish** - Low-hanging fruit from tiny things list
2. **Command improvements** - Polish `/audit` and `/stats`
3. **Git status optimization** - Add `/status` command (reduces tool calls for Claude)
4. **Constitution template** - Fill in lite-kits project constitution
5. **Command audit** - Review all prompts for minimalist design, accurate cross-refs
6. **Documentation review** - Final polish before PyPI

**Ship Target**: Tonight → PyPI with confidence

---

## 🔥 v0.3 CANDIDATES (Pick from these)

### Quick UX Polish (Easy wins, high impact)

**Priority: HIGH** - Pick 3-4 of these for v0.3:

1. **Preview improvements**
   - [ ] Show kit names as headers in preview
   - [ ] Split files by type (commands, memory, templates, scripts)
   - [ ] Only warn for reinstall if actually overwriting files

2. **Status/validation improvements**
   - [ ] Show installed kit + agent + shell combos (not just kit names)
   - [ ] Better formatting with tables

3. **Removal improvements**
   - [ ] Delete empty folders after removal
   - [ ] Check if files were customized before removing
   - [ ] Option to backup collaboration dir files (--force skips)

4. **Help text polish**
   - [ ] Reorder to mention Copilot first (broader audience)
   - [ ] Clarify `--force` warning (be specific, not vague)
   - [ ] Fix `--banner` help text ("must be first arg")

5. **Logging improvements**
   - [ ] Add `--verbose` details for all commands
   - [ ] Better log density (preview can show counts vs all files)

### Command Improvements

**Priority: MEDIUM** - Pick 1-2 for v0.3:

1. **Git Status Command** (`/status`)
   - Problem: Claude runs 5+ git commands for status checks
   - Solution: Single optimized command with all info
   - Benefit: Faster orientation, fewer tool calls

2. **Audit Command Polish** (`/audit`)
   - Current: Minimal implementation
   - Improve: Better security checks, dependency scanning

3. **Stats Command Polish** (`/stats`)
   - Current: Basic metrics
   - Improve: Code complexity, test coverage, commit stats

### Constitution & Documentation

**Priority: HIGH** - Good for v0.3:

1. **Fill in constitution template**
   - Currently: Generic placeholder
   - Update: Actual lite-kits principles and values

2. **Command audit** 🆕
   - Review all slash command prompt files (.claude/ and .github/)
   - Ensure minimalist design (no bloat, clear instructions)
   - Verify cross-command references are accurate
   - Check for outdated instructions or broken workflows
   - Validate scripts are referenced correctly

3. **Documentation review**
   - GUIDE.md - Check for accuracy
   - README.md - Ensure PyPI-ready
   - CONTRIBUTING.md - Update for new contributors

---

## 🚀 FUTURE RELEASES (v0.4+)

### Checkpoint System (v0.4) 🆕
**Inspired by**: claudekit, ccheckpoints
**Commands**:
- `/checkpoint` - Create git checkpoint before risky changes
- `/checkpoint:restore` - Restore from checkpoint
- `auto-checkpoint.sh` hook - Auto-save on session stop

**Benefit**: Safety net for refactoring, easy rollback

### Release Management Commands (v0.4)
**Commands**:
- `/tag` - Create annotated git tag with version selection
- `/release` - Create GitHub release with changelog generation
- Integration with `/audit` and `/stats` for release notes

**Benefit**: Streamline the release process we just went through!

### Web Discovery Interface (v0.5) 🆕
**Inspired by**: Claude Code Templates (aitmpl.com)
**Features**:
- GitHub Pages site to browse commands
- Interactive component selector
- Installation preview

**Benefit**: Better discoverability, easier onboarding

### Health Check & Analytics (v0.5) 🆕
**Inspired by**: Claude Code Templates monitoring
**Commands**:
- `lite-kits doctor` - Validate installation and dependencies
- `lite-kits analytics` - Track command usage and performance
- Health dashboard

**Benefit**: Better debugging, usage insights

### Spec-Kit Integration (v0.6)
**Features**:
- `lite-kits init` - Launch specify.exe to initialize spec-kit
- `lite-kits spec install/remove/upgrade` - Manage spec-kit installation
- Auto-detection of specify.exe location

**Benefit**: One-stop shop for spec-kit + lite-kits setup

### Hook System (v0.6) 🆕
**Inspired by**: claudekit hooks
**Features**:
- Pre-commit hooks (lint, test, security)
- Post-install hooks (setup, config)
- Custom hook templates

**Benefit**: Automated quality gates, workflow automation

### Namespace Organization (v0.7) 🆕
**Inspired by**: wshobson/commands, Claude-Command-Suite
**Structure**:
- `/dev:` - Development commands
- `/test:` - Testing utilities
- `/security:` - Security tools
- `/deploy:` - Deployment workflows

**Benefit**: Better organization, clearer intent

### Script Standardization (v1.0)
**Problem**: Commands rely on agents making many tool calls
**Solution**: Helper scripts for common multi-step operations
**Benefit**: More reliable, faster command execution

---

## 📦 BACKLOG (Future considerations)

**From Research**:
- Multi-agent coordination (parallel code review agents)
- AI thinking modes (prime, sentient, ultra-think)
- Real-time guardrails (file protection, pattern enforcement)
- Session checkpointing and history navigation
- Plugin marketplace integration

**Original Ideas**:
- Multi-agent workflow improvements
- Better error messages and recovery suggestions
- Installation analytics/telemetry (opt-in)
- Kit templates for custom kits
- Community kit repository
- Quick wins for .claude/CLAUDE.md and .github/copilot-instructions.md templates

---

## 🏁 v0.3 SHIP CHECKLIST

**Pre-implementation**:
- [ ] Decide on v0.3 scope (3-5 features from candidates above)
- [ ] Create implementation plan

**Implementation**:
- [ ] Implement selected features
- [ ] Test manually
- [ ] Update CHANGELOG.md

**Release**:
- [ ] Bump version to 0.3.0
- [ ] Commit and tag
- [ ] Create GitHub release
- [ ] **Publish to PyPI!** 🎉

---

## 💭 NOTES

**v0.2.0 Achievements**:
- ✅ Manifest-driven architecture
- ✅ Modular installer (detector, validator, conflict_checker)
- ✅ Kit consolidation (dev-kit)
- ✅ Content-first structure
- ✅ Perfect UX (spacing, previews, help)
- ✅ GitHub release created

**What's Missing for PyPI Confidence**:
- [ ] A few more polish items (v0.3)
- [ ] Constitution filled in (project identity)
- [ ] Final documentation review
- [ ] Manual validation testing

**Philosophy**: Ship early, iterate fast. v0.3 is about confidence, not perfection.
