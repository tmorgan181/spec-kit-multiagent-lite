#!/usr/bin/env bash
set -euo pipefail

# get-git-context.sh
# Gathers comprehensive git repository context for AI agents

show_help() {
    cat << EOF
Usage: get-git-context.sh [OPTIONS]

Gathers git status, branch information, recent commits, and change statistics
in a structured format suitable for AI agent orientation and commit workflows.

OPTIONS:
    -c, --commits NUM     Number of recent commits to include (default: 5)
    -f, --format FORMAT   Output format: text, json (default: text)
    -n, --no-diff         Exclude diff statistics
    -h, --help            Show this help message

EXAMPLES:
    get-git-context.sh
    get-git-context.sh --commits 10
    get-git-context.sh --format json
EOF
}

# Default options
INCLUDE_COMMITS=5
FORMAT="text"
INCLUDE_DIFF=true

# Parse arguments
while [[ $# -gt 0 ]]; do
    case $1 in
        -c|--commits)
            INCLUDE_COMMITS="$2"
            shift 2
            ;;
        -f|--format)
            FORMAT="$2"
            shift 2
            ;;
        -n|--no-diff)
            INCLUDE_DIFF=false
            shift
            ;;
        -h|--help)
            show_help
            exit 0
            ;;
        *)
            echo "Unknown option: $1"
            show_help
            exit 1
            ;;
    esac
done

# Check if we're in a git repository
if ! git rev-parse --git-dir >/dev/null 2>&1; then
    echo "Error: Not a git repository" >&2
    exit 1
fi

# Gather git context
BRANCH=$(git branch --show-current)
COMMIT_HASH=$(git rev-parse --short HEAD 2>/dev/null || echo "")

# Count file statuses
STAGED_COUNT=0
UNSTAGED_COUNT=0
UNTRACKED_COUNT=0

while IFS= read -r line; do
    if [[ -n "$line" ]]; then
        STATUS="${line:0:2}"

        # Staged files (first character)
        if [[ "${STATUS:0:1}" =~ [MADRC] ]]; then
            ((STAGED_COUNT++))
        fi

        # Unstaged files (second character)
        if [[ "${STATUS:1:1}" =~ [MD] ]]; then
            ((UNSTAGED_COUNT++))
        fi

        # Untracked files
        if [[ "$STATUS" == "??" ]]; then
            ((UNTRACKED_COUNT++))
        fi
    fi
done < <(git status --porcelain)

# Get remote tracking info
TRACKING=$(git rev-parse --abbrev-ref --symbolic-full-name '@{u}' 2>/dev/null || echo "")
AHEAD=0
BEHIND=0

if [[ -n "$TRACKING" ]]; then
    # Get ahead/behind counts
    AHEAD_BEHIND=$(git rev-list --left-right --count HEAD..."$TRACKING" 2>/dev/null || echo "0 0")
    AHEAD=$(echo "$AHEAD_BEHIND" | awk '{print $1}')
    BEHIND=$(echo "$AHEAD_BEHIND" | awk '{print $2}')
fi

# Get remote URL
REMOTE_URL=$(git remote get-url origin 2>/dev/null || echo "")

# Get diff statistics
INSERTIONS=0
DELETIONS=0
FILES_CHANGED=0

if [[ "$INCLUDE_DIFF" == true ]] && [[ $STAGED_COUNT -gt 0 ]]; then
    while IFS= read -r line; do
        if [[ -n "$line" ]]; then
            INS=$(echo "$line" | awk '{print $1}')
            DEL=$(echo "$line" | awk '{print $2}')

            # Handle binary files (-)
            [[ "$INS" != "-" ]] && INSERTIONS=$((INSERTIONS + INS))
            [[ "$DEL" != "-" ]] && DELETIONS=$((DELETIONS + DEL))
            ((FILES_CHANGED++))
        fi
    done < <(git diff --cached --numstat)
fi

# Output based on format
if [[ "$FORMAT" == "json" ]]; then
    # JSON output
    cat << EOF
{
  "branch": "$BRANCH",
  "commitHash": "$COMMIT_HASH",
  "status": {
    "counts": {
      "staged": $STAGED_COUNT,
      "unstaged": $UNSTAGED_COUNT,
      "untracked": $UNTRACKED_COUNT
    }
  },
  "remote": {
    "tracking": "$TRACKING",
    "url": "$REMOTE_URL",
    "ahead": $AHEAD,
    "behind": $BEHIND
  },
  "stats": {
    "filesChanged": $FILES_CHANGED,
    "insertions": $INSERTIONS,
    "deletions": $DELETIONS
  }
}
EOF
else
    # Text output
    echo "==============================================================="
    echo "📊 Git Status (on: $BRANCH):"
    echo "==============================================================="
    echo "Staged:    $STAGED_COUNT files"
    echo "Unstaged:  $UNSTAGED_COUNT files"
    echo "Untracked: $UNTRACKED_COUNT files"

    if [[ -n "$TRACKING" ]]; then
        echo ""
        echo "Remote: $TRACKING"
        if [[ $AHEAD -gt 0 ]]; then
            echo "  Ahead by $AHEAD commit(s)"
        fi
        if [[ $BEHIND -gt 0 ]]; then
            echo "  Behind by $BEHIND commit(s)"
        fi
    fi

    if [[ $STAGED_COUNT -gt 0 ]]; then
        echo ""
        echo "Staged files:"
        git status --porcelain | grep '^[MADRC]' | while IFS= read -r line; do
            echo "  ${line:0:2} ${line:3}"
        done
    fi

    if [[ $UNSTAGED_COUNT -gt 0 ]]; then
        echo ""
        echo "Unstaged files:"
        git status --porcelain | grep '^ [MD]' | while IFS= read -r line; do
            echo "  ${line:0:2} ${line:3}"
        done
    fi

    if [[ $UNTRACKED_COUNT -gt 0 ]]; then
        echo ""
        echo "Untracked files:"
        git status --porcelain | grep '^??' | while IFS= read -r line; do
            echo "  ${line:0:2} ${line:3}"
        done
    fi

    if [[ $INCLUDE_COMMITS -gt 0 ]]; then
        echo ""
        echo "Recent commits:"
        git log -n "$INCLUDE_COMMITS" --pretty=format:'  %h %s (%ar)' --abbrev-commit
        echo ""
    fi

    echo "==============================================================="
fi
