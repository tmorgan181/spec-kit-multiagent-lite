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

```bash
# Check if gh CLI is available
gh --version

# Check if authenticated
gh auth status

# Check current branch
CURRENT_BRANCH=$(git branch --show-current)
```

**If not authenticated**:
```
GitHub CLI not authenticated.

Run: gh auth login
Follow the prompts to authenticate.
```

**Check if branch needs pushing**:
```bash
# Check if branch has remote tracking
if ! git rev-parse --abbrev-ref --symbolic-full-name @{u} 2>/dev/null; then
  # No upstream - need initial push
  NEEDS_PUSH=true
  PUSH_TYPE="initial"
else
  # Check if local is ahead of remote
  LOCAL=$(git rev-parse HEAD)
  REMOTE=$(git rev-parse @{u})

  if [ "$LOCAL" != "$REMOTE" ]; then
    NEEDS_PUSH=true
    PUSH_TYPE="update"
  fi
fi
```

**If branch needs pushing, push automatically**:
```bash
if [ "$NEEDS_PUSH" = true ]; then
  if [ "$PUSH_TYPE" = "initial" ]; then
    echo "📤 Pushing branch to remote for the first time..."
    git push -u origin $CURRENT_BRANCH
  else
    echo "📤 Pushing new commits to remote..."
    git push
  fi

  # Verify push succeeded
  if [ $? -eq 0 ]; then
    echo "✓ Branch pushed successfully"
  else
    echo "❌ Push failed. Please resolve and try again."
    exit 1
  fi
fi
```

### 1a. Check Existing PR Status

**CRITICAL**: Always check if a PR already exists for this branch before creating a new one!

```bash
# Check for existing PR (open or closed)
EXISTING_PR=$(gh pr list --head $CURRENT_BRANCH --json number,state,url --jq '.[0]')

if [ -n "$EXISTING_PR" ]; then
  PR_NUMBER=$(echo "$EXISTING_PR" | jq -r '.number')
  PR_STATE=$(echo "$EXISTING_PR" | jq -r '.state')
  PR_URL=$(echo "$EXISTING_PR" | jq -r '.url')
fi
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

```bash
# Step 1: Find base branch that exists on REMOTE (preferred)
for base in develop main master; do
  if git ls-remote --heads origin "$base" | grep -q "$base"; then
    BASE_BRANCH_REMOTE=$base
    break
  fi
done

# Step 2: If no remote base found, check LOCAL branches
if [ -z "$BASE_BRANCH_REMOTE" ]; then
  for base in develop main master; do
    if git show-ref --verify --quiet refs/heads/$base; then
      BASE_BRANCH_LOCAL=$base
      break
    fi
  done
fi
```

**Present options to user**:

```bash
if [ -n "$BASE_BRANCH_REMOTE" ]; then
  echo "Detected base branches:"
  echo "  Remote: $BASE_BRANCH_REMOTE (exists on origin)"
  if [ -n "$BASE_BRANCH_LOCAL" ] && [ "$BASE_BRANCH_LOCAL" != "$BASE_BRANCH_REMOTE" ]; then
    echo "  Local:  $BASE_BRANCH_LOCAL (not pushed to remote)"
  fi
  echo ""
  echo "Creating PR requires a remote base branch."
  echo ""
  echo "Options:"
  echo "  1. Use existing remote: $BASE_BRANCH_REMOTE"
  if [ "$BASE_BRANCH_REMOTE" = "main" ]; then
    echo "     ⚠️  WARNING: This will PR into your default/production branch"
  fi
  echo "  2. Use custom branch (specify name)"
  echo "  3. Cancel"
  echo ""
  read -p "Your choice (1-3): " -n 1 -r
  echo ""
  
  case $REPLY in
    1)
      BASE_BRANCH=$BASE_BRANCH_REMOTE
      if [ "$BASE_BRANCH" = "main" ]; then
        echo "⚠️  WARNING: You're about to create a PR into 'main'"
        echo ""
        echo "This is your default/production branch. Are you sure?"
        echo ""
        echo "  y - Yes, PR into main (use sparingly!)"
        echo "  n - Cancel"
        echo ""
        read -p "Confirm (y/n): " -n 1 -r
        echo ""
        if [[ ! $REPLY =~ ^[Yy]$ ]]; then
          echo "PR creation cancelled."
          exit 0
        fi
      fi
      ;;
    2)
      read -p "Enter base branch name: " BASE_BRANCH
      # Check if it exists on remote
      if ! git ls-remote --heads origin "$BASE_BRANCH" | grep -q "$BASE_BRANCH"; then
        echo "Branch '$BASE_BRANCH' doesn't exist on remote."
        echo "Create it? (y/n)"
        read -p "" -n 1 -r
        echo ""
        if [[ $REPLY =~ ^[Yy]$ ]]; then
          git push origin "$BASE_BRANCH"
          echo "✓ Pushed $BASE_BRANCH to remote"
        else
          echo "PR creation cancelled."
          exit 0
        fi
      fi
      ;;
    *)
      echo "PR creation cancelled."
      exit 0
      ;;
  esac

elif [ -n "$BASE_BRANCH_LOCAL" ]; then
  echo "Detected base branches:"
  echo "  Local: $BASE_BRANCH_LOCAL (not pushed to remote yet)"
  echo ""
  echo "Options:"
  echo "  1. Push $BASE_BRANCH_LOCAL to remote and use it"
  echo "  2. Use custom branch (specify name)"
  echo "  3. Cancel"
  echo ""
  read -p "Your choice (1-3): " -n 1 -r
  echo ""
  
  case $REPLY in
    1)
      git push -u origin "$BASE_BRANCH_LOCAL"
      echo "✓ Pushed $BASE_BRANCH_LOCAL to origin"
      BASE_BRANCH=$BASE_BRANCH_LOCAL
      ;;
    2)
      read -p "Enter base branch name: " BASE_BRANCH
      ;;
    *)
      echo "PR creation cancelled."
      exit 0
      ;;
  esac

else
  echo "No base branches found (develop, main, or master)."
  echo ""
  read -p "Enter base branch name: " BASE_BRANCH
fi
```

### 3. Analyze Commits Since Base Branch

**IMPORTANT**: Only analyze commits that will be included in THIS PR (commits since divergence from base branch). Do NOT include commits that are already in the base branch or from previous merged PRs.

Once base branch is confirmed, analyze commits:

```bash
# Get commits since divergence (ONLY commits in this PR)
git log $BASE_BRANCH..HEAD --oneline

# Get full commit messages (ONLY for commits in this PR)
git log $BASE_BRANCH..HEAD --format="%s%n%b"

# Get file changes (ONLY changes in this PR)
git diff $BASE_BRANCH...HEAD --stat
```

**These are the ONLY commits to describe in the PR**. Previous work is already merged and documented in earlier PRs.

### 4. Detect Multi-Agent Collaboration

Check commit attributions to see if multiple agents contributed:

```bash
# Extract agent attributions from commits
git log $BASE_BRANCH..HEAD --format="%b" | grep "via.*@" || echo "No attributions found"
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
- Add `/orient` command for agent orientation (project-kit)
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
🤖 Generated with Claude Code (https://claude.com/claude-code)
```

### 6. Analyze Recent Activity

Check for collaboration indicators:

```bash
# Check for collaboration directory
if [ -d "specs/*/collaboration/active" ]; then
  echo "✓ Multi-agent collaboration structure detected"

  # List active sessions
  find specs/*/collaboration/active/sessions -name "*.md" 2>/dev/null

  # List decisions
  find specs/*/collaboration/active/decisions -name "*.md" 2>/dev/null
fi
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
```bash
# Create PR using gh CLI
gh pr create \
  --base $BASE_BRANCH \
  --title "$PR_TITLE" \
  --body "$PR_DESCRIPTION"
```

### 9. Post-Creation Actions

After PR is created:

```bash
# Get PR number
PR_NUM=$(gh pr view --json number -q .number)

echo "✓ Pull Request created: #$PR_NUM"
echo ""

# Ask about branch auto-delete
echo "Delete branch after merge? (y/n/later)"
read -r DELETE_CHOICE

if [ "$DELETE_CHOICE" = "y" ]; then
  gh pr edit $PR_NUM --delete-branch
  echo "✓ Branch will be auto-deleted after merge"
elif [ "$DELETE_CHOICE" = "later" ]; then
  echo "You can enable this later with:"
  echo "  gh pr edit $PR_NUM --delete-branch"
fi

# Get PR URL
PR_URL=$(gh pr view --json url -q .url)

echo "✓ Pull Request created: $PR_URL"

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

```bash
# User: /pr

# Agent checks prerequisites
$ gh auth status
✓ Logged in to github.com as username

# Agent analyzes commits
$ git log main..HEAD --oneline
53dd4ef feat: Implement Phase 1 MVP
0ad76b3 refactor: Move vanilla reference
81fdc9d docs: Add workflow pathways

# Agent generates description
[Shows generated PR description]

# Agent asks for confirmation
Create pull request? (y/n/e): y

# Agent creates PR
$ gh pr create --base main --title "..." --body "..."
https://github.com/owner/repo/pull/123

✓ Pull Request created: #123
View: gh pr view --web
```

## Advanced Options

**Create draft PR**:
```bash
gh pr create --draft \
  --base main \
  --title "WIP: Feature in progress" \
  --body "..."
```

**Add reviewers**:
```bash
gh pr create ... --reviewer username1,username2
```

**Add labels**:
```bash
gh pr create ... --label "feature,multiagent"
```

**Auto-fill from template** (if .github/pull_request_template.md exists):
```bash
# gh CLI will automatically use template
gh pr create
```
