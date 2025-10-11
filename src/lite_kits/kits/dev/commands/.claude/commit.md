---
description: Smart commit with agent attribution
---

# Smart Commit with Agent Attribution

**Purpose**: Generate conventional commit messages and add agent attribution for multi-agent tracking.

## Execution Steps

Execute the following steps to create a smart commit:

### 1. Analyze Git Status and Propose Staging Plan

**CRITICAL**: Always analyze the complete git status and propose a staging plan BEFORE staging anything!

```bash
# Get complete status - staged, unstaged, and untracked
git status --short
```

**Analyze the output**:
- Lines starting with `M ` or `A ` = Staged files (ready to commit)
- Lines starting with ` M` = Modified but NOT staged
- Lines starting with `??` = Untracked files
- Lines starting with `MM` = Staged AND modified again

**Step 1a: Analyze and Present Complete Commit Plan**

**IMPORTANT**: Present BOTH staging plan AND commit message in a single prompt. User can approve both, edit staging, edit message, or cancel.

**CRITICAL FORMATTING**: Wrap the ENTIRE proposal (staging plan + commit message + approval options) in a markdown code block using triple backticks (```). This ensures proper formatting in the CLI.

**Scenario 1: Files already staged**

Present the proposal like this (wrapped in code block):

````markdown
```
**📊 Git Status** (on: dev/001-feature-name)

**Staged:**    2 files
**Unstaged:**  1 file
**Untracked:** 1 file

===========================================================
**📋 Staging Plan:**
===========================================================

Files to commit:
1. M  src/file1.py
2. M  src/file2.py

Excluded from staging:
  M  src/unrelated.py (unstaged)
  ?? tests/new_test.py (untracked)

===========================================================
**💬 Commit Message:**
===========================================================

feat(001): add feature improvements

## Summary
Added improvements to src files for better functionality.

## Changes
- **src/file1.py**: Enhanced feature logic
- **src/file2.py**: Updated implementation

---
🤖 Co-authored with claude sonnet 4.5 @ claude code via vscode

===========================================================

**Approve commit?**
- **y** - Yes, stage files and commit with this message
- **n** - No, cancel
- **es** - Edit staging (reply with numbers: e.g., "1 3" or "all")
- **em** - Edit message (reply with new message)
```
````

**Scenario 2: Nothing staged, propose intelligent staging**

Present the proposal like this (wrapped in code block):

````markdown
```
**📊 Git Status** (on: dev/001-feature-name)

**Staged:**    0 files
**Modified:**  3 files
**Untracked:** 1 file

===========================================================
**📋 Staging Proposal:**
===========================================================

Proposed plan: Stage related command files (3 files)

Files to stage:

1. M  src/commands/pr.md
   → Command update for PR workflow

2. M  src/commands/commit.md
   → Related command improvements

3. M  src/prompts/pr.prompt.md
   → Matching prompt for GitHub Copilot

Excluded from staging:

  ?? docs/new_feature.md (unrelated documentation)

Rationale: Logical commit unit - these files represent coordinated
command workflow improvements that should be committed together to
maintain consistency across Claude Code and GitHub Copilot.

===========================================================
**💬 Commit Message:**
===========================================================

feat(004): enhance PR and commit command workflows

## Summary
Updated PR and commit commands with better user experience and
cross-platform consistency between Claude Code and GitHub Copilot.

## Changes
- **src/commands/pr.md**:
  - Added base branch detection
  - Enhanced user confirmation prompts

- **src/commands/commit.md**:
  - Improved staging proposal format
  - Added better examples

- **src/prompts/pr.prompt.md**:
  - Mirrored Claude Code improvements
  - PowerShell-specific enhancements

---
🤖 Co-authored with claude sonnet 4.5 @ claude code via vscode

===========================================================

**Approve commit?**
- **y** - Yes, stage files and commit with this message
- **n** - No, cancel
- **es** - Edit staging (reply with numbers: e.g., "1 3" or "all")
- **em** - Edit message (reply with new message)
```
````

**Scenario 3: Mixed state (some staged, related unstaged)**

Present the proposal like this (wrapped in code block):

````markdown
```
**📊 Git Status** (on: dev/001-feature-name)

**Staged:**    1 file
**Modified:**  3 files
**Untracked:** 1 file

===========================================================
**📋 Staging Proposal:**
===========================================================

Proposed plan: Add related command files (4 files total)

Already staged:

  M  src/commands/pr.md

Related unstaged files to add:

1. M  src/commands/commit.md (both are command files)
2. M  src/prompts/pr.prompt.md (pr-related)
3. M  src/prompts/commit.prompt.md (commit-related)

Excluded from staging:

  ?? random_file.txt (unrelated)

Rationale: Creates cohesive commit for command improvements.

===========================================================
**💬 Commit Message:**
===========================================================

feat(004): improve command workflow consistency

## Summary
Enhanced PR and commit commands with consistent UX across both
Claude Code and GitHub Copilot interfaces.

## Changes
- **src/commands/pr.md**: Added base branch detection
- **src/commands/commit.md**: Improved staging workflow
- **src/prompts/pr.prompt.md**: PowerShell version of PR enhancements
- **src/prompts/commit.prompt.md**: PowerShell version of commit improvements

---
🤖 Co-authored with claude sonnet 4.5 @ claude code via vscode

===========================================================

**Approve commit?**
- **y** - Yes, add related files and commit with this message
- **s** - Use only already-staged files and commit
- **es** - Edit staging (reply with numbers: e.g., "1 3" or "all")
- **em** - Edit message (reply with new message)
- **n** - No, cancel
```
````

**Scenario 4: Many changes - propose multiple modular commits**

When there are many unrelated changes (10+ files, or changes spanning unrelated features), propose breaking into multiple logical commits.

Present the proposal like this (wrapped in code block):

````markdown
```
**📊 Git Status** (on: dev/001-feature-name)

**Staged:**    0 files
**Modified:**  15 files
**Untracked:** 3 files

===========================================================
**📋 Multi-Commit Proposal:**
===========================================================

Detected many changes across different areas. Proposing 3 modular commits:

**Commit 1: Git workflow commands** (5 files)
1. M  src/commands/commit.md
2. M  src/commands/pr.md
3. M  src/commands/cleanup.md
4. M  src/prompts/commit.prompt.md
5. M  src/prompts/pr.prompt.md

Message:
  feat(004): enhance git workflow commands

  Updated commit, PR, and cleanup commands with better UX
  and cross-platform consistency.

---

**Commit 2: Documentation updates** (4 files)
6. M  docs/ARCHITECTURE.md
7. M  docs/IMPLEMENTATION-GUIDE.md
8. M  README.md
9. ?? docs/new-guide.md

Message:
  docs(004): update documentation for dev-kit

  Added git workflow documentation and updated README
  with new command examples.

---

**Commit 3: Status tracking** (2 files)
10. M  docs/temp/PHASE-1-AUDIT.md
11. M  docs/temp/kit-implementation-status.md

Message:
  chore(004): update implementation status tracking

  Marked dev-kit as complete in status docs.

---

**Excluded from commits:**
  M  src/experimental/test.py (work in progress)
  M  src/debug.log (debug file)
  ?? temp/ (temporary directory)

===========================================================

**Approve multi-commit plan?**
- **y** - Yes, execute all commits in sequence
- **n** - No, cancel
- **ec** - Edit commits (specify which commits: e.g., "1 3")
- **em** - Edit messages (will prompt for each)
- **single** - Combine into single commit instead
```
````

**Step 1b: Execute staging and commit based on user choice**

After user approves (y), execute the plan:
```bash
# Stage files for approved commits
git add <files-from-plan>

# Create commit with approved message
git commit -m "<message-including-attribution>"

# Show result
git log -1 --oneline
```

If user edits staging (es) or message (em):
- Show updated plan
- Ask for confirmation again
- Then execute

### 2. Analyze Staged Changes

Examine the staged changes to determine:

**Change Type** (following Conventional Commits):
- `feat:` New feature or capability
- `fix:` Bug fix
- `refactor:` Code restructuring without behavior change
- `docs:` Documentation only
- `test:` Adding or updating tests
- `chore:` Maintenance (dependencies, config, build)
- `style:` Formatting, whitespace
- `perf:` Performance improvements

**Scope** (optional):
- Identify the main area/component affected
- Examples: `auth`, `api`, `ui`, `cli`, `installer`

**Summary**:
- 1-2 sentences describing what changed
- Focus on the "what" and "why", not the "how"

### 3. Detect Feature Number

**Check for feature number in order of priority**:

1. **From branch name** (highest priority):
```bash
# Get current branch
git branch --show-current

# Extract feature number from patterns like:
# - dev/001-feature-name → 001
# - feature/002-auth → 002
# - 003-bugfix → 003
```

2. **From specs directory** (if branch has no number):
```bash
# Look for specs directory with feature number
ls specs/*/spec.md 2>/dev/null | head -1

# Extract from pattern: specs/NNN-feature-name/spec.md → NNN
```

3. **Use component name** (fallback):
- If no feature number found anywhere, use component/scope name
- Examples: `cli`, `installer`, `git`, `multiagent`

**Feature Number Format**:
- Must be 3 digits: `001`, `002`, `042`, etc.
- Branch pattern: `dev/NNN-*`, `feature/NNN-*`, `NNN-*`
- Specs pattern: `specs/NNN-*`

### 4. Generate Commit Message

Create a beautiful, structured commit message with feature number and agent attribution:

```
<type>(NNN): <subject>

## Summary
<Brief 1-2 sentence overview with enthusiasm>

## Changes
- **<file/component>**:
  - <specific change>
  - <specific change>

- **<file/component>**:
  - <specific change>

## <Additional Section if Relevant>
<Context, impacts, visual improvements, etc.>

---
🤖 Co-authored with claude sonnet 4.5 @ claude code via vscode
```

**Format Rules**:
- Subject: `feat(NNN):` format with feature number
- Use feature number if available, otherwise component name
- Summary: 1-2 sentences, be enthusiastic but genuine
- Changes: Bulleted list grouped by file/component
- Use markdown bold for file names
- Add emoji where appropriate (sparingly)
- Keep professional but friendly tone
- Attribution: Claude Code standard footer

**Examples**:

```
feat(002): add beautiful colorful pytest output with pytest-sugar

## Summary
Added pytest-sugar for gorgeous colorful test output with progress bars
and instant failure reporting. MOAR GREEN! 🎉

## Changes
- **pyproject.toml**:
  - Added pytest-sugar dependency for beautiful output
  - Configured pytest with --color=yes and markers
  - Added -ra flag for summary of all outcomes

- **quick-start.ps1**:
  - Simplified pytest args to let pytest-sugar shine
  - Verbose mode: -v flag shows test names
  - Default mode: pytest-sugar progress bar (no -q)

## Visual Improvements
- ✨ Beautiful progress bar during test execution
- 🟢 Green PASSED markers with percentages
- 🟡 Yellow SKIPPED with clear reasons
- 🔴 Red FAILED with instant feedback
- 📊 Colored summary statistics

---
🤖 Co-authored with claude sonnet 4.5 @ claude code via vscode
```

```
fix(003): handle null values in user profile endpoint

## Summary
Fixed TypeError when optional profile fields are missing. Now handles
null values gracefully with sensible defaults.

## Changes
- **src/api/users.py**:
  - Added null checks for optional fields
  - Set default empty strings for missing values
  - Added validation before JSON serialization

- **tests/test_users.py**:
  - Added test cases for null profile fields
  - Verified default value behavior

---
🤖 Co-authored with claude sonnet 4.5 @ claude code via vscode
```

```
docs(installer): update installation instructions

## Summary
Clarified Python version requirement and added comprehensive
troubleshooting section for common installation issues.

## Changes
- **README.md**:
  - Added Python 3.8+ requirement
  - Added pip install examples
  - Linked to troubleshooting guide

- **docs/TROUBLESHOOTING.md**:
  - Added Windows-specific issues
  - Added virtual environment setup
  - Added common error solutions

---
🤖 Co-authored with claude sonnet 4.5 @ claude code via vscode
```

### 5. Post-Commit Actions

After successful commit:
```bash
# Show commit hash and summary
git log -1 --oneline

# Show current branch status
git status --short
```

**Suggest next steps**:
- "Commit created. Push with: `git push`"
- If on feature branch: "Ready to create PR? Run `/pr`"
- If collaboration/ exists: "Update session log in specs/*/collaboration/active/sessions/"

## Important Notes

- **Don't commit secrets**: Check for `.env`, `credentials.json`, API keys
- **No commits without user confirmation**: Always show message first
- **Preserve git hooks**: Don't use `--no-verify` unless user explicitly requests
- **Attribution format is fixed**: `via <model> @ <agent>` - don't modify
- **Keep subjects concise**: Max 72 characters for good git log display
- **Use imperative mood**: "Add feature" not "Added feature"

## Error Handling

**No changes at all**:
```
⚠️  No changes detected.

Working directory is clean - nothing to commit.
```

**Commit failed** (e.g., pre-commit hook):
```
❌ Commit failed: [error message]

Check git output above for details.
Fix issues and run /commit again.
```

**User cancels during approval**:
- Don't stage anything if not already staged
- Leave repository in clean state
- Suggest: "Cancelled. Changes remain unstaged. Run /commit when ready."

## Example Workflow

```bash
# User: /commit

# Agent checks git status
$ git status --short
M  src/commands/commit.md
M  src/prompts/commit.prompt.md

# Agent presents combined staging + commit plan
**📊 Git Status** (on: dev/004-cleanup-command)

**Staged:**    0 files
**Modified:**  2 files

===========================================================
**📋 Staging Proposal:**
===========================================================

Proposed plan: Stage commit command updates (2 files)

Files to stage:
1. M  src/commands/commit.md
   → Simplified approval workflow
2. M  src/prompts/commit.prompt.md
   → PowerShell version of changes

===========================================================
**💬 Commit Message:**
===========================================================

feat(004): simplify commit approval workflow

## Summary
Combined staging proposal and commit message into single prompt
for better UX. Fewer user interactions needed.

## Changes
- **src/commands/commit.md**:
  - Show both staging and commit message together
  - Single approval step with edit options

- **src/prompts/commit.prompt.md**:
  - Mirrored bash version improvements

---
🤖 Co-authored with claude sonnet 4.5 @ claude code via vscode

===========================================================

**Approve commit?**
- **y** - Yes, stage files and commit with this message
- **n** - No, cancel
- **es** - Edit staging
- **em** - Edit message

# User: y

# Agent executes
$ git add src/commands/commit.md src/prompts/commit.prompt.md
$ git commit -m "..."
[dev/004-cleanup-command 8a3f2c1] feat(004): simplify commit...
 2 files changed, 87 insertions(+), 142 deletions(-)

✓ Commit created: 8a3f2c1
Branch: dev/004-cleanup-command
Next: git push origin dev/004-cleanup-command
```

## Multi-Agent Coordination

When working with multiple agents:

1. **Attribution tracks who coded what**:
   ```bash
   git log --format="%h %s %b" | grep "via"
   ```
   Shows which agent made which commits

2. **Session logging** (if multiagent-kit installed):
   - Create/update: `specs/*/collaboration/active/sessions/<date>-<agent>.md`
   - Document what you committed and why

3. **Handoff preparation**:
   - Clear commit messages help the next agent understand changes
   - Attribution makes it easy to ask the right agent about their commits
