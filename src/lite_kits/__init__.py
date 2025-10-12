"""
lite-kits: Lightweight enhancement kits for spec-driven development

This package adds productivity-enhancing slash commands to vanilla spec-kit projects
without forking or replacing any core files.
"""

# Version
__version__ = "0.3.2"

# Package metadata
APP_NAME = "lite-kits"
APP_DESCRIPTION = "Quick start: lite-kits add  •  Get help: lite-kits help [COMMAND]"
REPOSITORY_URL = "https://github.com/tmorgan181/lite-kits"
LICENSE = "MIT"

# Kit identifiers
KIT_DEV = "dev"
KIT_MULTIAGENT = "multiagent"
KITS_ALL = [KIT_DEV, KIT_MULTIAGENT]

# Kit descriptions
KIT_DESC_DEV = "Solo development essentials: /orient, /commit, /pr, /review, /cleanup, /audit, /stats"
KIT_DESC_MULTIAGENT = "Multi-agent coordination: /sync, collaboration dirs, memory guides (EXPERIMENTAL)"

# Directory paths
DIR_CLAUDE_COMMANDS = r".claude\commands"
DIR_GITHUB_PROMPTS = r".github\prompts"
DIR_SPECIFY_MEMORY = r".specify\memory"
DIR_SPECIFY_SCRIPTS_BASH = r".specify\scripts\bash"
DIR_SPECIFY_SCRIPTS_POWERSHELL = r".specify\scripts\powershell"
DIR_SPECIFY_TEMPLATES = r".specify\templates"

# Spec-kit detection paths
SPEC_KIT_DIRS = [r".specify", r".claude", r".github\prompts"]

# Error messages
ERROR_NOT_SPEC_KIT = "does not appear to be a spec-kit project!"
ERROR_SPEC_KIT_HINT = r"Looking for one of: .specify\, .claude\, or .github\prompts"

__all__ = [
    "__version__",
    "APP_NAME",
    "APP_DESCRIPTION",
    "REPOSITORY_URL",
    "LICENSE",
    "KIT_DEV",
    "KIT_MULTIAGENT",
    "KITS_ALL",
    "KIT_DESC_DEV",
    "KIT_DESC_MULTIAGENT",
    "DIR_CLAUDE_COMMANDS",
    "DIR_GITHUB_PROMPTS",
    "DIR_SPECIFY_MEMORY",
    "DIR_SPECIFY_SCRIPTS_BASH",
    "DIR_SPECIFY_SCRIPTS_POWERSHELL",
    "DIR_SPECIFY_TEMPLATES",
    "SPEC_KIT_DIRS",
    "ERROR_NOT_SPEC_KIT",
    "ERROR_SPEC_KIT_HINT",
]
