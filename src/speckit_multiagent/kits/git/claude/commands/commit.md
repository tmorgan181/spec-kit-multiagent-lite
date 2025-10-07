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

**Step 1a: Present current state and propose staging plan**

**IMPORTANT**: Always wrap the staging proposal in a markdown code block (triple backticks) to ensure consistent formatting across all UIs.

**Scenario 1: Files already staged**
```
**📊 Git Status** (on: dev/001-feature-name)

**Staged:**    2 files
**Unstaged:**  1 file
**Untracked:** 1 file

===========================================================
**📋 Staging Proposal:**
===========================================================

Proposed plan: Use currently staged files (2 files)

Files to commit:

1. M  src/file1.py

2. M  src/file2.py

Excluded from staging:

  M  src/unrelated.py (unstaged)
  ?? tests/new_test.py (untracked)

===========================================================
```

**Accept staging proposal?**
- **y** - Yes, proceed with staged files
- **n** - No, cancel
- **e** - Edit selection (reply with numbers to add)
- **all** - Stage ALL files (including excluded)

**Scenario 2: Nothing staged, propose intelligent staging**
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
```

**Accept staging proposal?**
- **y** - Yes, stage listed files
- **n** - No, cancel
- **e** - Edit selection (reply with numbers: e.g., "1 3")
- **all** - Stage ALL files (including excluded)

**Scenario 3: Mixed state (some staged, related unstaged)**
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

  M  src/commands/commit.md (both are command files)
  M  src/prompts/pr.prompt.md (pr-related)
  M  src/prompts/commit.prompt.md (commit-related)

Excluded from staging:

  ?? random_file.txt (unrelated)

Rationale: Creates cohesive commit for command improvements.

===========================================================
```

**Accept staging proposal?**
- **y** - Yes, add related files
- **s** - Use only already-staged files
- **all** - Stage ALL files
- **e** - Edit selection (specify which files)
- **n** - Cancel - let me adjust manually

**Step 1b: Execute staging based on user choice**

**If nothing is staged AND user needs help**:
```
⚠️  No changes staged for commit.

Unstaged changes found:
  M  src/file1.py
  M  src/file2.py

Options:
  1. Stage ALL changes (git add .)
  2. Stage specific files (specify which)
  3. Cancel - let me stage manually

Your choice (1-3): _____
```

**Execute staging based on user choice**:
```bash
# After user confirms, stage the agreed-upon files
git add <files-from-plan>

echo "✓ Staged files for commit"
git status --short  # Show final staged state
```

**Step 1c: Confirm final staging before proceeding**

```
===========================================================
Final staging confirmed:
===========================================================

Files to be committed:
  M  src/commands/pr.md
  M  src/commands/commit.md
  M  src/prompts/pr.prompt.md

Ready to generate commit message.
===========================================================
```

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

### 5. Present Commit Message

Show the generated message to the user:

```
===============================================================
Suggested Commit Message:
===============================================================

feat(git): Add smart commit with agent attribution

Generates conventional commit messages and adds agent
attribution for multi-agent tracking.

via claude-sonnet-4.5 @ claude-code

===============================================================
Staged files (3):
  M src/speckit_multiagent/cli.py
  M src/speckit_multiagent/installer.py
  A src/speckit_multiagent/kits/git/claude/commands/commit.md
===============================================================
```

### 6. Confirm and Execute

**Ask user**:
- **y** - Proceed with commit
- **n** - Cancel
- **e** - Edit message (allow user to modify)

**If confirmed**:
```bash
git commit -m "<full message including attribution>"
```

**If editing**:
- Allow user to modify the message
- Show updated version
- Ask for confirmation again

### 7. Post-Commit Actions

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

**No changes staged**:
```
No changes staged for commit.

Run one of these first:
  git add <files>      # Stage specific files
  git add .            # Stage all changes

Or use: git commit -a -m "message"  # Stage and commit tracked files
```

**Commit failed** (e.g., pre-commit hook):
```
Commit failed: [error message]

Check git output above for details.
Fix issues and try again.
```

## Example Workflow

```bash
# User: /commit

# Agent checks staged changes
$ git diff --staged
# (shows changes)

# Agent analyzes and generates message
feat(git): Add smart commit with agent attribution

Generates conventional commit messages...

via claude-sonnet-4.5 @ claude-code

# Agent asks for confirmation
Proceed with commit? (y/n/e): y

# Agent executes
$ git commit -m "..."
[dev/001-starter-kits 53dd4ef] feat(git): Add smart commit...
 3 files changed, 142 insertions(+), 5 deletions(-)

Commit created: 53dd4ef
Branch: dev/001-starter-kits
Next: git push origin dev/001-starter-kits
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
