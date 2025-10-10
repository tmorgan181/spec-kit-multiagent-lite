# Lite-Kits Wishlist - Prioritized

**Last Updated**: 2025-10-09 Final Polish Complete
**Status**: v0.2 Ready for Documentation & Ship 🚀

---

## 🎉 v0.2 SHIP CHECKLIST

- [x] All critical bugs fixed
- [x] UX polish complete
- [x] Kit reorganization (content-first structure)
- [x] Manifest constants and schema doc
- [x] Quick wins implemented (spacing, file counts, help command)
- [ ] Update README.md (main repo)
- [ ] Update docs (if needed)
- [ ] Bump version to 0.2.0
- [ ] Ship to PyPI

---

## ✅ QUICK WINS - ALL COMPLETED!

**Tiny UX Improvements** (All shipped in v0.2):
1. ✅ Add newline before all exit paths (cleaner terminal output)
2. ✅ Add file count to preview summaries (e.g., "Total files to install: 14")
3. ✅ Make --force work with remove command (skip preview/prompts)
4. ✅ Add leading newlines to all command outputs (clean spacing after prompt)
5. ✅ Add `help` command that accepts optional command argument (`lite-kits help add`)
6. ✅ Change help description to be useful instead of repeating tagline

---

## ✅ COMPLETED (v0.2.0)

**Core Architecture:**
- Kit Consolidation (project + git → dev-kit)
- Manifest-Driven (YAML single source of truth, zero hardcoded IDs)
- Modular Installer (4 focused modules: detector, validator, conflict_checker, installer)
- Content-First Structure (easy to add agents/shells/content types)
- Manifest Constants & Schema Doc

**UX Improvements:**
- Preview-First (always show preview before operations)
- Smart Detection (auto-detect agents/shells with override flags)
- All Bugs Fixed (#1, #3, #4, #6, #7)
- Empty Section Hiding (cleaner preview output)
- Clean Formatted Output (no raw dicts)
- Perfect Terminal Spacing (leading/trailing newlines on all commands)
- File Count Summaries (preview shows total file counts)
- Help Command (lite-kits help [COMMAND] support)
- Useful Help Text (actionable quick start instead of tagline repetition)

**Agent/Shell Support:**
- Claude Code + GitHub Copilot (dual agent support)
- Bash + PowerShell (dual shell support)
- Auto-detection with explicit overrides (--agent, --shell, --force)

---

## 🔥 NEW IDEAS (v0.3 and Beyond)

### Spec-Kit Integration 🆕
**Idea**: Integrate with spec-kit's specify.exe for full workflow
**Features**:
- `lite-kits init` - Launch specify.exe to initialize spec-kit in current directory
- `lite-kits spec install` - Install spec-kit if not present
- `lite-kits spec remove` - Remove spec-kit from project
- `lite-kits spec upgrade` - Upgrade spec-kit to latest version
- Auto-detection of specify.exe location (PATH, common install dirs)

**Benefits**:
- One-stop shop for spec-kit setup
- Seamless integration between spec-kit and lite-kits
- Lower friction for new users

**Priority**: v0.3 - Nice complement to core functionality

### Release Management Commands 🆕
**Need**: /tag and /release commands for dev-kit
**Commands**:
- `/tag` - Create annotated git tag with version selection
- `/release` - Create GitHub release with changelog generation
**Integration**: Work with /audit and /stats for release notes
**Priority**: v0.3

---

## 📋 MEDIUM PRIORITY (v0.3+ Features)

### Git Status Command
**Problem**: Claude runs multiple git commands to check status (inefficient)
**Solution**: Add `/status` command with optimized git checks
**Priority**: v0.3

### Command Audit & Polish
**Task**: Review all dev-kit commands for quality
**Focus**: /audit and /stats (currently minimal implementations)
**Priority**: v0.3

### Script Standardization
**Problem**: Commands rely on agent making many tool calls
**Solution**: Create helper scripts for common multi-step operations
**Priority**: v1.0

---

## 📝 NEXT ACTIONS FOR v0.2 SHIP

1. ✅ **Fix bugs 1, 3, 4** (High priority - Preview issues)
2. ✅ **Fix bug 6** (Medium - Wrong kits shown)
3. ✅ **Fix bug 7** (Low - Duplicate banner)
4. ✅ **Polish UX issues 2, 5** (All quick wins implemented!)
5. 📝 **Document v0.2.0 changes**
6. 🚀 **Ship v0.2.0 to PyPI!**

---

## BACKLOG IDEAS

- Multi-agent workflow improvements
- Better error messages and recovery suggestions
- Installation analytics/telemetry (opt-in)
- Kit templates for custom kits
- Community kit repository

---

## tiny things

**Completed:**
- ✅ all paths to exit should have a newline so we don't crowd the next cmd
- ✅ on previews, should give count of changes
- ✅ `--force` should work for remove to skip prompts/preview
- ✅ resolve installer versions into single installer.py
- ✅ add help command support

**Future (v0.3+):**
- reorder any help text to mention copilot first
- change force warning to be less vague
- only warn for reinstall if overwriting (resolve with diffing for preview)
- check if any of the files to be removed have been customized or changed from the default kit version
- removal should get rid of the folders too, if they become empty
- remove any bad meta-commentary in comments ("this time we did it right!", e.g.) - UNLESS they are funny. then we definitely keep them.
- show installed kits + agent + shell combos in status/validation, not just kits
- make sure there is good log density for all commands and also add --verbose details. def applies to preview (can just be counts/overview vs. all files)
- option to stash/backup collaboration dir files before removal (--force skips this)
- preview should include names of kits as headers.
- in preview, split by file type (command, memory, template, script, etc.)
- in --banner help text, "can be combined" should include "must be first arg"