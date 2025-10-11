---
description: Create pull request with smart description generation
---

# Create Pull Request

**Purpose**: Generate PR description from commits and create pull request using GitHub CLI.

## Prerequisites

- `gh` CLI installed and authenticated
- Current branch pushed to remote
- Git commits on current branch

## Execution Steps

### 1. Verify Prerequisites and Push Branch

```powershell
# Check if gh CLI is available
gh --version

# Check if authenticated
gh auth status

# Check current branch
$CurrentBranch = git branch --show-current
```

**If not authenticated**:
```
GitHub CLI not authenticated.

Run: gh auth login
Follow the prompts to authenticate.
```

**Check if branch needs pushing**:
```powershell
# Check if branch has remote tracking
$HasUpstream = git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>$null
$NeedsPush = $false
$PushType = $null

if ($LASTEXITCODE -ne 0) {
    # No upstream - need initial push
    $NeedsPush = $true
    $PushType = "initial"
} else {
    # Check if local is ahead of remote
    $Local = git rev-parse HEAD
    $Remote = git rev-parse '@{u}'

    if ($Local -ne $Remote) {
        $NeedsPush = $true
        $PushType = "update"
    }
}
```

**If branch needs pushing, push automatically**:
```powershell
if ($NeedsPush) {
    if ($PushType -eq "initial") {
        Write-Host "📤 Pushing branch to remote for the first time..."
        git push -u origin $CurrentBranch
    } else {
        Write-Host "📤 Pushing new commits to remote..."
        git push
    }

    # Verify push succeeded
    if ($LASTEXITCODE -eq 0) {
        Write-Host "✓ Branch pushed successfully" -ForegroundColor Green
    } else {
        Write-Host "❌ Push failed. Please resolve and try again." -ForegroundColor Red
        exit 1
    }
}
```

### 1a. Check Existing PR Status

**CRITICAL**: Always check if a PR already exists for this branch before creating a new one!

```powershell
# Check for existing PR (open or closed)
$ExistingPR = gh pr list --head $CurrentBranch --json number,state,url | ConvertFrom-Json

if ($ExistingPR) {
    $PRNumber = $ExistingPR[0].number
    $PRState = $ExistingPR[0].state
    $PRUrl = $ExistingPR[0].url
}
```

**If PR exists and is OPEN**:
```
✓ Pull Request #5 already exists for this branch.

State: OPEN
URL: https://github.com/owner/repo/pull/5

New commits will automatically appear in the PR.

Options:
  - Push new commits: git push
  - Update PR description: gh pr edit 5 --body "new description"
  - View PR: gh pr view --web

Continue anyway to update PR description? (y/n): _____
```

**If PR exists and is MERGED**:
```
✓ Pull Request #5 for this branch was already MERGED.

URL: https://github.com/owner/repo/pull/5

You have new commits since the merge.

Options:
  1. Create NEW PR for additional changes
  2. Switch to develop and create new feature branch
  3. Cancel

Choice (1-3): _____
```

**If PR exists and is CLOSED (not merged)**:
```
⚠️  Pull Request #5 for this branch exists but was CLOSED (not merged).

URL: https://github.com/owner/repo/pull/5

Options:
  1. Reopen existing PR: gh pr reopen 5
  2. Create new PR (not recommended - will conflict)
  3. Cancel

Choice (1-3): _____
```

### 2. Determine Base Branch

**Enhanced base branch detection with remote-first priority**:

```powershell
# Step 1: Find base branch that exists on REMOTE (preferred)
$BASE_BRANCH_REMOTE = $null
foreach ($base in @('develop', 'main', 'master')) {
    $remote = git ls-remote --heads origin $base 2>$null | Select-String $base
    if ($remote) {
        $BASE_BRANCH_REMOTE = $base
        break
    }
}

# Step 2: If no remote base found, check LOCAL branches
$BASE_BRANCH_LOCAL = $null
if (-not $BASE_BRANCH_REMOTE) {
    foreach ($base in @('develop', 'main', 'master')) {
        if (git show-ref --verify --quiet "refs/heads/$base") {
            $BASE_BRANCH_LOCAL = $base
            break
        }
    }
}
```

**Present options to user**:

```powershell
if ($BASE_BRANCH_REMOTE) {
    Write-Host "Detected base branches:"
    Write-Host "  Remote: $BASE_BRANCH_REMOTE (exists on origin)"
    if ($BASE_BRANCH_LOCAL -and $BASE_BRANCH_LOCAL -ne $BASE_BRANCH_REMOTE) {
        Write-Host "  Local:  $BASE_BRANCH_LOCAL (not pushed to remote)"
    }
    Write-Host ""
    Write-Host "Creating PR requires a remote base branch."
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  1. Use existing remote: $BASE_BRANCH_REMOTE"
    if ($BASE_BRANCH_REMOTE -eq 'main') {
        Write-Host "     ⚠️  WARNING: This will PR into your default/production branch" -ForegroundColor Yellow
    }
    Write-Host "  2. Use custom branch (specify name)"
    Write-Host "  3. Cancel"
    Write-Host ""
    $choice = Read-Host "Your choice (1-3)"

    switch ($choice) {
        '1' {
            $BASE_BRANCH = $BASE_BRANCH_REMOTE
            if ($BASE_BRANCH -eq 'main') {
                Write-Host "⚠️  WARNING: You're about to create a PR into 'main'" -ForegroundColor Yellow
                Write-Host ""
                Write-Host "This is your default/production branch. Are you sure?"
                Write-Host ""
                Write-Host "  y - Yes, PR into main (use sparingly!)"
                Write-Host "  n - Cancel"
                Write-Host ""
                $confirm = Read-Host "Confirm (y/n)"
                if ($confirm -ne 'y') {
                    Write-Host "PR creation cancelled."
                    exit 0
                }
            }
        }
        '2' {
            $BASE_BRANCH = Read-Host "Enter base branch name"
            # Check if it exists on remote
            $remoteCheck = git ls-remote --heads origin $BASE_BRANCH 2>$null | Select-String $BASE_BRANCH
            if (-not $remoteCheck) {
                Write-Host "Branch '$BASE_BRANCH' doesn't exist on remote."
                $create = Read-Host "Create it? (y/n)"
                if ($create -eq 'y') {
                    git push origin $BASE_BRANCH
                    Write-Host "✓ Pushed $BASE_BRANCH to remote"
                } else {
                    Write-Host "PR creation cancelled."
                    exit 0
                }
            }
        }
        default {
            Write-Host "PR creation cancelled."
            exit 0
        }
    }
} elseif ($BASE_BRANCH_LOCAL) {
    Write-Host "Detected base branches:"
    Write-Host "  Local: $BASE_BRANCH_LOCAL (not pushed to remote yet)"
    Write-Host ""
    Write-Host "Options:"
    Write-Host "  1. Push $BASE_BRANCH_LOCAL to remote and use it"
    Write-Host "  2. Use custom branch (specify name)"
    Write-Host "  3. Cancel"
    Write-Host ""
    $choice = Read-Host "Your choice (1-3)"

    switch ($choice) {
        '1' {
            git push -u origin $BASE_BRANCH_LOCAL
            Write-Host "✓ Pushed $BASE_BRANCH_LOCAL to origin"
            $BASE_BRANCH = $BASE_BRANCH_LOCAL
        }
        '2' {
            $BASE_BRANCH = Read-Host "Enter base branch name"
        }
        default {
            Write-Host "PR creation cancelled."
            exit 0
        }
    }
} else {
    Write-Host "No base branches found (develop, main, or master)."
    Write-Host ""
    $BASE_BRANCH = Read-Host "Enter base branch name"
}
```

### 3. Analyze Commits Since Base Branch

**IMPORTANT**: Only analyze commits that will be included in THIS PR (commits since divergence from base branch). Do NOT include commits that are already in the base branch or from previous merged PRs.

Once base branch is confirmed, analyze commits:

```powershell
# Get commits since divergence (ONLY commits in this PR)
git log "$BASE_BRANCH..HEAD" --oneline

# Get full commit messages (ONLY for commits in this PR)
git log "$BASE_BRANCH..HEAD" --format="%s%n%b"

# Get file changes (ONLY changes in this PR)
git diff "$BASE_BRANCH...HEAD" --stat
```

**These are the ONLY commits to describe in the PR**. Previous work is already merged and documented in earlier PRs.

### 4. Detect Multi-Agent Collaboration

Check commit attributions to see if multiple agents contributed:

```powershell
# Extract agent attributions from commits
git log "$BASE_BRANCH..HEAD" --format="%b" | Select-String "via.*@"
```

**If multiple agents detected**:
- Note which agents contributed (e.g., "claude-code" and "github-copilot-cli")
- Highlight collaboration in PR description

### 5. Generate PR Description

**CRITICAL**: The PR description should ONLY cover the commits identified in Step 3 (commits since base branch). This PR is one modular piece of work - don't describe previous merged work.

Create a comprehensive PR description:

**Format**:
```markdown
## Summary

[1-3 sentence overview of what this PR accomplishes]

## Changes

[Bullet points of major changes, grouped by commit type]

- feat: [Features added]
- fix: [Bugs fixed]
- refactor: [Code improvements]
- docs: [Documentation updates]

## Testing

- [ ] Manual testing performed
- [ ] Existing tests pass
- [ ] New tests added (if applicable)

## Multi-Agent Collaboration

[If multiple agents detected]
This PR was developed collaboratively:
- **Claude Code** (claude-sonnet-4.5): [their contributions]
- **GitHub Copilot** (gpt-4): [their contributions]

See commit history for detailed attributions.

---
🤖 Generated with [agent-name]
```

**Example**:
```markdown
## Summary

Implements Phase 1 MVP with `/orient` command and modular kit system for multi-agent coordination.

## Changes

### Features
- Add `/orient` command for agent orientation (dev-kit)
- Implement kit-aware installer with --kit flag support
- Add modular kit structure (project, git, multiagent)
- Auto-dependency inclusion (multiagent → project + git)

### Documentation
- Complete audit against WORKFLOW-PATHWAYS.md
- Implementation status matrix
- Phase roadmap documentation

## Testing

- [x] Manual testing performed
- [x] Dry-run installation preview works
- [x] Actual installation to vanilla project succeeds
- [x] Kit detection and validation functional

## Version Safety

✓ Zero vanilla files modified
✓ Additive-only pattern maintained
✓ Namespace separation enforced

---
🤖 Generated with GitHub Copilot CLI
```

### 6. Analyze Recent Activity

Check for collaboration indicators:

```powershell
# Check for collaboration directory
if (Test-Path "specs/*/collaboration/active") {
  Write-Host "✓ Multi-agent collaboration structure detected"

  # List active sessions
  Get-ChildItem -Path specs/*/collaboration/active/sessions -Filter *.md -Recurse -ErrorAction SilentlyContinue

  # List decisions
  Get-ChildItem -Path specs/*/collaboration/active/decisions -Filter *.md -Recurse -ErrorAction SilentlyContinue
}
```

### 7. Present PR Details

Show the generated PR information:

```
===========================================================
Pull Request Preview:
===========================================================

Title: feat: Implement Phase 1 MVP - /orient and kit system

Base: main
Head: dev/001-starter-kits

Commits: 3
Files changed: 10 (+1456, -132)

Description:
[Generated description from step 4]

===========================================================
```

### 8. Confirm and Create PR

**Ask user**:
- **y** - Create PR
- **n** - Cancel
- **e** - Edit title or description

**If confirmed, create PR**:
```powershell
# Create PR using gh CLI
gh pr create `
  --base $BASE_BRANCH `
  --title "$PR_TITLE" `
  --body "$PR_DESCRIPTION"
```

**Alternative method if gh CLI not available**:
```
Open PR manually:
https://github.com/[owner]/[repo]/compare/[base]...[head]

Use the generated description above.
```

### 9. Post-Creation Actions

After PR is created:

```powershell
# Get PR number
$PR_NUM = gh pr view --json number -q .number

Write-Host "✓ Pull Request created: #$PR_NUM"
Write-Host ""

# Ask about branch auto-delete
Write-Host "Delete branch after merge? (y/n/later)"
$DELETE_CHOICE = Read-Host

if ($DELETE_CHOICE -eq 'y') {
    gh pr edit $PR_NUM --delete-branch
    Write-Host "✓ Branch will be auto-deleted after merge"
} elseif ($DELETE_CHOICE -eq 'later') {
    Write-Host "You can enable this later with:"
    Write-Host "  gh pr edit $PR_NUM --delete-branch"
}

```powershell
# Get PR URL
$PR_URL = gh pr view --json url -q .url

Write-Host "✓ Pull Request created: $PR_URL"

# Show PR number and status
gh pr view
```

**Suggest next steps**:
- "PR created. Add reviewers with: `gh pr edit --add-reviewer <username>`"
- "Mark as draft with: `gh pr ready --undo`"
- "View PR: `gh pr view --web`"

## Important Notes

- **Review before creating**: Always show PR description for user approval
- **Don't auto-merge**: Never create and merge in one step
- **Check CI status**: Mention if there are failing checks
- **Link related issues**: If this closes an issue, add "Closes #123" to description
- **Draft PRs**: For work-in-progress, create as draft: `gh pr create --draft`

## Error Handling

**gh CLI not installed**:
```
GitHub CLI not found.

Install from: https://cli.github.com/

Or create PR manually at:
https://github.com/[owner]/[repo]/compare/[base]...[head]
```

**Not authenticated**:
```
Not authenticated with GitHub.

Run: gh auth login
```

**No commits**:
```
No commits to create PR from.

Current branch is up to date with base branch.
Make some commits first.
```

**PR already exists**:
```
Pull request already exists: #42
https://github.com/[owner]/[repo]/pull/42

Update it with: gh pr edit 42 --body "new description"
```

## Multi-Agent PR Workflow

When multiple agents collaborate:

1. **Detect collaboration**:
   - Check commit attributions for multiple agents
   - Look for collaboration/ directory structure
   - Check for handoff documents

2. **Highlight contributions**:
   ```markdown
   ## Multi-Agent Collaboration

   This PR was developed collaboratively:

   ### Claude Code (claude-sonnet-4.5)
   - Implemented core /orient command
   - Created kit-aware installer
   - Wrote documentation and audit

   ### GitHub Copilot (gpt-4)
   - Added PowerShell script variants
   - Implemented error handling
   - Created test cases

   See individual commit messages for detailed attributions.
   ```

3. **Link to collaboration docs**:
   - Reference session logs from specs/*/collaboration/
   - Link to decision documents
   - Mention any unresolved handoffs

## Example Workflow

```powershell
# User: /pr

# Agent checks prerequisites
> gh auth status
✓ Logged in to github.com as username

# Agent analyzes commits
> git log main..HEAD --oneline
53dd4ef feat: Implement Phase 1 MVP
0ad76b3 refactor: Move vanilla reference
81fdc9d docs: Add workflow pathways

# Agent generates description
[Shows generated PR description]

# Agent asks for confirmation
Create pull request? (y/n/e): y

# Agent creates PR
> gh pr create --base main --title "..." --body "..."
https://github.com/owner/repo/pull/123

✓ Pull Request created: #123
View: gh pr view --web
```

## Advanced Options

**Create draft PR**:
```powershell
gh pr create --draft `
  --base main `
  --title "WIP: Feature in progress" `
  --body "..."
```

**Add reviewers**:
```powershell
gh pr create ... --reviewer username1,username2
```

**Add labels**:
```powershell
gh pr create ... --label "feature,multiagent"
```

**Auto-fill from template** (if .github/pull_request_template.md exists):
```powershell
# gh CLI will automatically use template
gh pr create
```
