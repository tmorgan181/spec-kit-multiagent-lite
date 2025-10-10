================================
Testing
================================

🧪 Manual Test Suite for lite-kits v0.2.0
Setup: Create Test Environment
# Navigate to example project
cd C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app

# Create spec-kit structure
New-Item -ItemType Directory -Path ".specify", ".claude", ".github\prompts" -Force

# Verify structure
Get-ChildItem -Directory
Test 1: Status (Before Install)
lite-kits status
Expected: Shows spec-kit detected, no kits installed
Test 2: Add with Preview (Cancel)
# Type 'n' when prompted
lite-kits add --recommended
Expected: Shows preview of 14 files to create, asks for confirmation, cancels when you say 'n'
Test 3: Add with Preview (Confirm)
# Type 'y' when prompted
lite-kits add --recommended
Expected: Shows preview, you confirm, installs 14 files (7 commands × 2 agents)
Test 4: Status (After Install)
lite-kits status
Expected: Shows dev-kit installed
Test 5: Validate
lite-kits validate
Expected: Shows all files validated successfully
Test 6: Reinstall (Test Conflict Handling)
# Type 'y' when asked "Reinstall anyway?"
lite-kits add --recommended
Expected: Asks if you want to reinstall, shows preview, confirms, reinstalls without errors
Test 7: Add with --force (Skip Preview)
lite-kits add --force --recommended
Expected: No preview, installs immediately
Test 8: Agent-Specific Install
# First remove everything
lite-kits remove --all
# Type 'y' to confirm

# Then install only for Claude
lite-kits add --agent claude
Expected: Only installs .claude/commands/ files (7 files), not .github/prompts/
Test 9: Info Command
lite-kits info
Expected: Shows package version, available kits, descriptions
Test 10: Banner with Command
lite-kits --banner status
Expected: Shows banner (or fallback text on Windows), then runs status
Test 11: Remove All
lite-kits remove --all
# Type 'y' to confirm
Expected: Shows files to remove, confirms, removes all kit files
Test 12: Status (After Removal)
lite-kits status
Expected: Shows spec-kit detected, no kits installed
Cleanup (Optional)
# Remove spec-kit structure
Remove-Item -Recurse -Force .specify, .claude, .github
What to look for:
✅ No errors/crashes
✅ Preview always shows before operations (unless --force)
✅ Confirmations work correctly
✅ Files installed in correct locations
✅ Agent detection works (installs for both Claude + Copilot)
✅ --agent flag filters correctly
✅ Clean, readable output
Let me know if any test fails! 🧪

================================
Results
================================

Trenton notes:
1. bug - no preview given before operation on test 6 (reinstall/overwrite existing files)
2. ux - in add commands if no folders/modifications to be made, do not show the headers
3. bug - removal list/preview is not human-readable and does not match style of add command
4. bug -  preview was not shown before prompting for removal. should always show preview before any add/removal ops except when --force
5. ux - we don't show the scripts being created for either claude or copilot
6. bug - when removing while only dev kit is installed, i see multiagent previewed as being removed as well
7. bug - running `--banner info` displays banner twice because info includes static banner by default. probably easiest to just remove that from the info command.

Otherwise, function is excellent, style is mostly consistent (i will manually polish later before v1), and the add/remove process is now a breeze! will be even better once we get spec-kit integration and other QOL rails in place. 

Below is the full run output, let me know if you notice anything I did not note! Great work, Sr Dev Claude Code (promoted as of just now haha)

================================
Output
================================

PS C:\Users\tmorg\Projects> cd .\lite-kits\examples\minimal-todo-app\
PS C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app> dir


    Directory: C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----         10/8/2025   9:13 PM           4352 README.md


PS C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app> lite-kits.exe

██╗     ██╗████████╗███████╗      ██╗  ██╗██╗████████╗███████╗
██║     ██║╚══██╔══╝██╔════╝      ██║ ██╔╝██║╚══██╔══╝██╔════╝
██║     ██║   ██║   █████╗  █████╗█████╔╝ ██║   ██║   ███████╗
██║     ██║   ██║   ██╔══╝  ╚════╝██╔═██╗ ██║   ██║   ╚════██║
███████╗██║   ██║   ███████╗      ██║  ██╗██║   ██║   ███████║
╚══════╝╚═╝   ╚═╝   ╚══════╝      ╚═╝  ╚═╝╚═╝   ╚═╝   ╚══════╝

Lightweight enhancement kits for spec-driven development.
See --help for all options and commands.

Quick Start:
  1. lite-kits add --recommended  # Add dev-kit (all commands)
  2. lite-kits status             # Check installation
  3. lite-kits validate           # Validate kit files

PS C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app> lite-kits.exe add
Error: C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app does not appear to be a spec-kit project!

Looking for one of: .specify/, .claude/, or .github/prompts/
PS C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app> New-Item -ItemType Directory -Path ".specify", ".claude", ".github\prompts" -Force


    Directory: C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----         10/9/2025  10:16 PM                .specify
d-----         10/9/2025  10:16 PM                .claude


    Directory: C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app\.github


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----         10/9/2025  10:16 PM                prompts


PS C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app> Get-ChildItem -Directory


    Directory: C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
d-----         10/9/2025  10:16 PM                .claude
d-----         10/9/2025  10:16 PM                .github
d-----         10/9/2025  10:16 PM                .specify


PS C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app> lite-kits status

[OK] Spec-kit project detected in C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app.

No kits installed.

PS C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app> lite-kits add --recommended

Preview of changes:

Files to be created:
  + .claude/commands/orient.md
  + .claude/commands/commit.md
  + .claude/commands/pr.md
  + .claude/commands/review.md
  + .claude/commands/cleanup.md
  + .claude/commands/audit.md
  + .claude/commands/stats.md
  + .github/prompts/orient.prompt.md
  + .github/prompts/commit.prompt.md
  + .github/prompts/pr.prompt.md
  + .github/prompts/review.prompt.md
  + .github/prompts/cleanup.prompt.md
  + .github/prompts/audit.prompt.md
  + .github/prompts/stats.prompt.md

Files to be modified:

Directories to be created:
  + .claude\commands

Proceed with installation? [y/N]: n
Installation cancelled
PS C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app> lite-kits add --recommended

Preview of changes:

Files to be created:
  + .claude/commands/orient.md
  + .claude/commands/commit.md
  + .claude/commands/pr.md
  + .claude/commands/review.md
  + .claude/commands/cleanup.md
  + .claude/commands/audit.md
  + .claude/commands/stats.md
  + .github/prompts/orient.prompt.md
  + .github/prompts/commit.prompt.md
  + .github/prompts/pr.prompt.md
  + .github/prompts/review.prompt.md
  + .github/prompts/cleanup.prompt.md
  + .github/prompts/audit.prompt.md
  + .github/prompts/stats.prompt.md

Files to be modified:

Directories to be created:
  + .claude\commands

Proceed with installation? [y/N]: y

Installing kits to C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app

[OK] Done!

[OK] Kits installed successfully!

Installed files:
  + .claude/commands/orient.md
  + .claude/commands/commit.md
  + .claude/commands/pr.md
  + .claude/commands/review.md
  + .claude/commands/cleanup.md
  + .claude/commands/audit.md
  + .claude/commands/stats.md
  + .github/prompts/orient.prompt.md
  + .github/prompts/commit.prompt.md
  + .github/prompts/pr.prompt.md
  + .github/prompts/review.prompt.md
  + .github/prompts/cleanup.prompt.md
  + .github/prompts/audit.prompt.md
  + .github/prompts/stats.prompt.md

Next steps:
  1. Run: /orient (in your AI assistant)
  2. Check: .claude/commands/orient.md or .github/prompts/orient.prompt.md
  3. Validate: lite-kits validate
PS C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app> lite-kits status

[OK] Spec-kit project detected in C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app.

Installed kits:
  + dev-kit

PS C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app> lite-kits validate

Validating C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app


Validating C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app

[OK] Done!

[OK] dev
[OK] multiagent

[OK] Validation passed!

PS C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app> lite-kits add --recommended
Warning: Enhancement kits appear to be already installed
Reinstall anyway? [y/N]: y

Installing kits to C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app

[OK] Done!

[OK] Kits installed successfully!

Installed files:
  + .claude/commands/orient.md
  + .claude/commands/commit.md
  + .claude/commands/pr.md
  + .claude/commands/review.md
  + .claude/commands/cleanup.md
  + .claude/commands/audit.md
  + .claude/commands/stats.md
  + .github/prompts/orient.prompt.md
  + .github/prompts/commit.prompt.md
  + .github/prompts/pr.prompt.md
  + .github/prompts/review.prompt.md
  + .github/prompts/cleanup.prompt.md
  + .github/prompts/audit.prompt.md
  + .github/prompts/stats.prompt.md

Next steps:
  1. Run: /orient (in your AI assistant)
  2. Check: .claude/commands/orient.md or .github/prompts/orient.prompt.md
  3. Validate: lite-kits validate
PS C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app> lite-kits add --force --recommended
Warning: Enhancement kits appear to be already installed

Installing kits to C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app

[OK] Done!

[OK] Kits installed successfully!

Installed files:
  + .claude/commands/orient.md
  + .claude/commands/commit.md
  + .claude/commands/pr.md
  + .claude/commands/review.md
  + .claude/commands/cleanup.md
  + .claude/commands/audit.md
  + .claude/commands/stats.md
  + .github/prompts/orient.prompt.md
  + .github/prompts/commit.prompt.md
  + .github/prompts/pr.prompt.md
  + .github/prompts/review.prompt.md
  + .github/prompts/cleanup.prompt.md
  + .github/prompts/audit.prompt.md
  + .github/prompts/stats.prompt.md

Next steps:
  1. Run: /orient (in your AI assistant)
  2. Check: .claude/commands/orient.md or .github/prompts/orient.prompt.md
  3. Validate: lite-kits validate
PS C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app> lite-kits remove --all

Remove kits from C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app
Kits to remove: dev, multiagent

Continue with removal? [y/N]: y

Removing kits...

Removal complete!

Removed:
  - {'kit': 'Dev Kit', 'files': ['.claude/commands/orient.md', '.claude/commands/commit.md', '.claude/commands/pr.md',
'.claude/commands/review.md', '.claude/commands/cleanup.md', '.claude/commands/audit.md', '.claude/commands/stats.md',
'.github/prompts/orient.prompt.md', '.github/prompts/commit.prompt.md', '.github/prompts/pr.prompt.md',
'.github/prompts/review.prompt.md', '.github/prompts/cleanup.prompt.md', '.github/prompts/audit.prompt.md',
'.github/prompts/stats.prompt.md']}
PS C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app> lite-kits add --agent claude

Preview of changes:

Files to be created:
  + .claude/commands/orient.md
  + .claude/commands/commit.md
  + .claude/commands/pr.md
  + .claude/commands/review.md
  + .claude/commands/cleanup.md
  + .claude/commands/audit.md
  + .claude/commands/stats.md

Files to be modified:

Directories to be created:

Proceed with installation? [y/N]: y

Installing kits to C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app

[OK] Done!

[OK] Kits installed successfully!

Installed files:
  + .claude/commands/orient.md
  + .claude/commands/commit.md
  + .claude/commands/pr.md
  + .claude/commands/review.md
  + .claude/commands/cleanup.md
  + .claude/commands/audit.md
  + .claude/commands/stats.md

Next steps:
  1. Run: /orient (in your AI assistant)
  2. Check: .claude/commands/orient.md or .github/prompts/orient.prompt.md
  3. Validate: lite-kits validate
PS C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app> lite-kits add --agent copilot
Warning: Enhancement kits appear to be already installed
Reinstall anyway? [y/N]: y

Installing kits to C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app

[OK] Done!

[OK] Kits installed successfully!

Installed files:
  + .github/prompts/orient.prompt.md
  + .github/prompts/commit.prompt.md
  + .github/prompts/pr.prompt.md
  + .github/prompts/review.prompt.md
  + .github/prompts/cleanup.prompt.md
  + .github/prompts/audit.prompt.md
  + .github/prompts/stats.prompt.md

Next steps:
  1. Run: /orient (in your AI assistant)
  2. Check: .claude/commands/orient.md or .github/prompts/orient.prompt.md
  3. Validate: lite-kits validate
PS C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app> lite-kits remove --all

Remove kits from C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app
Kits to remove: dev, multiagent

Continue with removal? [y/N]: y

Removing kits...

Removal complete!

Removed:
  - {'kit': 'Dev Kit', 'files': ['.claude/commands/orient.md', '.claude/commands/commit.md', '.claude/commands/pr.md',
'.claude/commands/review.md', '.claude/commands/cleanup.md', '.claude/commands/audit.md', '.claude/commands/stats.md',
'.github/prompts/orient.prompt.md', '.github/prompts/commit.prompt.md', '.github/prompts/pr.prompt.md',
'.github/prompts/review.prompt.md', '.github/prompts/cleanup.prompt.md', '.github/prompts/audit.prompt.md',
'.github/prompts/stats.prompt.md']}
PS C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app> lite-kits add --agent copilot

Preview of changes:

Files to be created:
  + .github/prompts/orient.prompt.md
  + .github/prompts/commit.prompt.md
  + .github/prompts/pr.prompt.md
  + .github/prompts/review.prompt.md
  + .github/prompts/cleanup.prompt.md
  + .github/prompts/audit.prompt.md
  + .github/prompts/stats.prompt.md

Files to be modified:

Directories to be created:

Proceed with installation? [y/N]: y

Installing kits to C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app

[OK] Done!

[OK] Kits installed successfully!

Installed files:
  + .github/prompts/orient.prompt.md
  + .github/prompts/commit.prompt.md
  + .github/prompts/pr.prompt.md
  + .github/prompts/review.prompt.md
  + .github/prompts/cleanup.prompt.md
  + .github/prompts/audit.prompt.md
  + .github/prompts/stats.prompt.md

Next steps:
  1. Run: /orient (in your AI assistant)
  2. Check: .claude/commands/orient.md or .github/prompts/orient.prompt.md
  3. Validate: lite-kits validate
PS C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app> lite-kits remove --all

Remove kits from C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app
Kits to remove: dev, multiagent

Continue with removal? [y/N]: n
Cancelled
PS C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app> lite-kits info

██╗     ██╗████████╗███████╗      ██╗  ██╗██╗████████╗███████╗
██║     ██║╚══██╔══╝██╔════╝      ██║ ██╔╝██║╚══██╔══╝██╔════╝
██║     ██║   ██║   █████╗  █████╗█████╔╝ ██║   ██║   ███████╗
██║     ██║   ██║   ██╔══╝  ╚════╝██╔═██╗ ██║   ██║   ╚════██║
███████╗██║   ██║   ███████╗      ██║  ██╗██║   ██║   ███████║
╚══════╝╚═╝   ╚═╝   ╚══════╝      ╚═╝  ╚═╝╚═╝   ╚═╝   ╚══════╝

Lightweight enhancement kits for spec-driven development.

Info:
  Version       0.1.0
  Repository    https://github.com/tmorgan181/lite-kits
  License       MIT

Available Kits:
  dev           Solo development essentials: /orient, /commit, /pr, /review, /cleanup, /audit, /stats
  multiagent    Multi-agent coordination: /sync, collaboration dirs, memory guides (optional)

Package Management:
  Update       uv tool install --upgrade lite-kits
  Uninstall    uv tool uninstall lite-kits

PS C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app> lite-kits status

[OK] Spec-kit project detected in C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app.

Installed kits:
  + dev-kit

PS C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app> lite-kits status --banner
Usage: lite-kits status [OPTIONS] [TARGET]
Try 'lite-kits status --help' for help.
╭─ Error ──────────────────────────────────────────────────────────────────────────────────────────────────────────────╮
│ No such option: --banner                                                                                             │
╰──────────────────────────────────────────────────────────────────────────────────────────────────────────────────────╯
PS C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app> lite-kits --banner status

██╗     ██╗████████╗███████╗      ██╗  ██╗██╗████████╗███████╗
██║     ██║╚══██╔══╝██╔════╝      ██║ ██╔╝██║╚══██╔══╝██╔════╝
██║     ██║   ██║   █████╗  █████╗█████╔╝ ██║   ██║   ███████╗
██║     ██║   ██║   ██╔══╝  ╚════╝██╔═██╗ ██║   ██║   ╚════██║
███████╗██║   ██║   ███████╗      ██║  ██╗██║   ██║   ███████║
╚══════╝╚═╝   ╚═╝   ╚══════╝      ╚═╝  ╚═╝╚═╝   ╚═╝   ╚══════╝

Lightweight enhancement kits for spec-driven development.

[OK] Spec-kit project detected in C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app.

Installed kits:
  + dev-kit

PS C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app> lite-kits --banner info

██╗     ██╗████████╗███████╗      ██╗  ██╗██╗████████╗███████╗
██║     ██║╚══██╔══╝██╔════╝      ██║ ██╔╝██║╚══██╔══╝██╔════╝
██║     ██║   ██║   █████╗  █████╗█████╔╝ ██║   ██║   ███████╗
██║     ██║   ██║   ██╔══╝  ╚════╝██╔═██╗ ██║   ██║   ╚════██║
███████╗██║   ██║   ███████╗      ██║  ██╗██║   ██║   ███████║
╚══════╝╚═╝   ╚═╝   ╚══════╝      ╚═╝  ╚═╝╚═╝   ╚═╝   ╚══════╝

Lightweight enhancement kits for spec-driven development.

██╗     ██╗████████╗███████╗      ██╗  ██╗██╗████████╗███████╗
██║     ██║╚══██╔══╝██╔════╝      ██║ ██╔╝██║╚══██╔══╝██╔════╝
██║     ██║   ██║   █████╗  █████╗█████╔╝ ██║   ██║   ███████╗
██║     ██║   ██║   ██╔══╝  ╚════╝██╔═██╗ ██║   ██║   ╚════██║
███████╗██║   ██║   ███████╗      ██║  ██╗██║   ██║   ███████║
╚══════╝╚═╝   ╚═╝   ╚══════╝      ╚═╝  ╚═╝╚═╝   ╚═╝   ╚══════╝

Lightweight enhancement kits for spec-driven development.

Info:
  Version       0.1.0
  Repository    https://github.com/tmorgan181/lite-kits
  License       MIT

Available Kits:
  dev           Solo development essentials: /orient, /commit, /pr, /review, /cleanup, /audit, /stats
  multiagent    Multi-agent coordination: /sync, collaboration dirs, memory guides (optional)

Package Management:
  Update       uv tool install --upgrade lite-kits
  Uninstall    uv tool uninstall lite-kits

PS C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app> lite-kits --banner status

██╗     ██╗████████╗███████╗      ██╗  ██╗██╗████████╗███████╗
██║     ██║╚══██╔══╝██╔════╝      ██║ ██╔╝██║╚══██╔══╝██╔════╝
██║     ██║   ██║   █████╗  █████╗█████╔╝ ██║   ██║   ███████╗
██║     ██║   ██║   ██╔══╝  ╚════╝██╔═██╗ ██║   ██║   ╚════██║
███████╗██║   ██║   ███████╗      ██║  ██╗██║   ██║   ███████║
╚══════╝╚═╝   ╚═╝   ╚══════╝      ╚═╝  ╚═╝╚═╝   ╚═╝   ╚══════╝

Lightweight enhancement kits for spec-driven development.

[OK] Spec-kit project detected in C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app.

Installed kits:
  + dev-kit

PS C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app> lite-kits remove --all

Remove kits from C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app
Kits to remove: dev, multiagent

Continue with removal? [y/N]: y

Removing kits...

Removal complete!

Removed:
  - {'kit': 'Dev Kit', 'files': ['.github/prompts/orient.prompt.md', '.github/prompts/commit.prompt.md',
'.github/prompts/pr.prompt.md', '.github/prompts/review.prompt.md', '.github/prompts/cleanup.prompt.md',
'.github/prompts/audit.prompt.md', '.github/prompts/stats.prompt.md']}
PS C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app> lite-kits status

[OK] Spec-kit project detected in C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app.

No kits installed.

PS C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app> Remove-Item -Recurse -Force .specify, .claude, .github
PS C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app> dir


    Directory: C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app


Mode                 LastWriteTime         Length Name
----                 -------------         ------ ----
-a----         10/8/2025   9:13 PM           4352 README.md


PS C:\Users\tmorg\Projects\lite-kits\examples\minimal-todo-app>