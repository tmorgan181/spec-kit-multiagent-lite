---
description: Smart commit with agent attribution
---

# Smart Commit with Agent Attribution

**Purpose**: Generate conventional commit messages and add agent attribution for multi-agent tracking.

## Execution Steps

Execute the following steps to create a smart commit:

### 1. Check for Staged Changes

```powershell
# Check what's staged
git status --short

# Show staged diff
git diff --staged

# If nothing staged, show unstaged changes
git diff --short
```

**If nothing is staged**:
- Ask user if they want to stage all changes: `git add .`
- Or ask which files to stage
- Or exit with message: "No changes staged. Run `git add <files>` first."

### 2. Analyze Changes

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

### 3. Generate Commit Message

Create a conventional commit message with agent attribution:

```
<type>(<scope>): <subject>

<body>

via <model> @ <agent>
```

**Format Rules**:
- Subject: Max 72 chars, imperative mood ("Add" not "Added")
- Body: Optional, wrap at 72 chars, explain context
- Attribution: `via <model> @ <agent>` on last line

**Examples**:

```
feat(auth): Add JWT-based authentication

Implements token generation, validation, and refresh logic.
Adds middleware for protected routes.

via gpt-4 @ github-copilot-cli
```

```
fix(api): Handle null values in user profile endpoint

Fixes TypeError when optional fields are missing.
Adds null checks and default values.

via gpt-4 @ github-copilot-cli
```

```
docs: Update installation instructions

Clarifies Python version requirement and adds troubleshooting section.

via gpt-4 @ github-copilot-cli
```

### 4. Determine Agent Model

**For GitHub Copilot CLI**:
- Model: `gpt-4` (or current model)
- Agent: `github-copilot-cli`

**For Claude Code**:
- Model: `claude-sonnet-4.5` (or current model)
- Agent: `claude-code`

### 5. Present Commit Message

Show the generated message to the user:

```
═══════════════════════════════════════════════════════════
Suggested Commit Message:
═══════════════════════════════════════════════════════════

feat(git): Add smart commit with agent attribution

Generates conventional commit messages and adds agent
attribution for multi-agent tracking.

via gpt-4 @ github-copilot-cli

═══════════════════════════════════════════════════════════
Staged files (3):
  M src/speckit_multiagent/cli.py
  M src/speckit_multiagent/installer.py
  A src/speckit_multiagent/kits/git/github/prompts/commit.prompt.md
═══════════════════════════════════════════════════════════
```

### 6. Confirm and Execute

**Ask user**:
- **y** - Proceed with commit
- **n** - Cancel
- **e** - Edit message (allow user to modify)

**If confirmed**:
```powershell
git commit -m "<full message including attribution>"
```

**If editing**:
- Allow user to modify the message
- Show updated version
- Ask for confirmation again

### 7. Post-Commit Actions

After successful commit:
```powershell
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

```powershell
# User: /commit

# Agent checks staged changes
> git diff --staged
# (shows changes)

# Agent analyzes and generates message
feat(git): Add smart commit with agent attribution

Generates conventional commit messages...

via gpt-4 @ github-copilot-cli

# Agent asks for confirmation
Proceed with commit? (y/n/e): y

# Agent executes
> git commit -m "..."
[dev/001-starter-kits 53dd4ef] feat(git): Add smart commit...
 3 files changed, 142 insertions(+), 5 deletions(-)

✓ Commit created: 53dd4ef
Branch: dev/001-starter-kits
Next: git push origin dev/001-starter-kits
```

## Multi-Agent Coordination

When working with multiple agents:

1. **Attribution tracks who coded what**:
   ```powershell
   git log --format="%h %s %b" | Select-String "via"
   ```
   Shows which agent made which commits

2. **Session logging** (if multiagent-kit installed):
   - Create/update: `specs/*/collaboration/active/sessions/<date>-<agent>.md`
   - Document what you committed and why

3. **Handoff preparation**:
   - Clear commit messages help the next agent understand changes
   - Attribution makes it easy to ask the right agent about their commits
