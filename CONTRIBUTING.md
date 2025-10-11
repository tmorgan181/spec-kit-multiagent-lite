# Contributing to lite-kits

Thank you for your interest in contributing to lite-kits! This document provides guidelines and information for contributors.

---

## Table of Contents

1. [Quick Start](#quick-start)
2. [Development Setup](#development-setup)
3. [Project Structure](#project-structure)
4. [Adding Commands](#adding-commands)
5. [Adding Agents or Shells](#adding-agents-or-shells)
6. [Testing](#testing)
7. [Pull Request Process](#pull-request-process)
8. [Code Style](#code-style)

---

## Quick Start

```bash
# 1. Fork and clone
git clone https://github.com/YOUR_USERNAME/lite-kits.git
cd lite-kits

# 2. Install with dev dependencies
uv tool install -e ".[dev]"

# 3. Make changes
# ...

# 4. Test locally
cd /tmp/test-project
specify init  # Create test spec-kit project
lite-kits add

# 5. Submit PR
```

---

## Development Setup

### Prerequisites

- Python 3.11+
- uv (recommended) or pip
- Git
- A spec-kit project for testing

### Install for Development

```bash
# Clone repository
git clone https://github.com/tmorgan181/lite-kits.git
cd lite-kits

# Install with uv (recommended)
uv tool install -e ".[dev]"

# Or with pip
pip install -e ".[dev]"
```

### Verify Installation

```bash
# Check version
lite-kits --version

# Test on a spec-kit project
cd path/to/spec-kit-project
lite-kits add
lite-kits status
lite-kits validate
```

---

## Project Structure

```
lite-kits/
├── src/lite_kits/
│   ├── __init__.py
│   ├── cli.py                     # CLI commands and interface
│   ├── core/
│   │   ├── __init__.py
│   │   ├── banner.py              # Banner display
│   │   ├── detector.py            # Agent/shell detection
│   │   ├── validator.py           # Installation validation
│   │   ├── conflict_checker.py    # Conflict detection
│   │   ├── installer.py           # Main installer orchestrator
│   │   └── manifest.py            # Manifest parser
│   └── kits/
│       ├── kits.yaml              # Kit manifest (SOURCE OF TRUTH)
│       ├── dev/
│       │   ├── README.md
│       │   └── commands/
│       │       ├── .claude/       # Claude Code commands
│       │       │   ├── orient.md
│       │       │   ├── commit.md
│       │       │   └── ...
│       │       └── .github/       # GitHub Copilot prompts
│       │           ├── orient.prompt.md
│       │           ├── commit.prompt.md
│       │           └── ...
│       └── multiagent/
│           ├── README.md
│           ├── commands/
│           ├── memory/
│           └── templates/
├── docs/
│   ├── GUIDE.md                   # Comprehensive user guide
│   ├── manifest-schema.md         # Manifest technical reference
│   └── temp/                      # Design documents
├── examples/                      # Example projects
├── CHANGELOG.md                   # Version history
├── CONTRIBUTING.md                # This file
├── README.md                      # Main documentation
└── pyproject.toml                 # Package metadata
```

---

## Adding Commands

### 1. Create Command Files

Commands use the **content-first** structure with file extensions for agent support:

```bash
# For Claude Code
kits/dev/commands/.claude/my-command.md

# For GitHub Copilot
kits/dev/commands/.github/my-command.prompt.md
```

### 2. Command File Structure

**Claude Code Command** (`.claude/my-command.md`):

```markdown
# /my-command

[Brief description of what this command does]

## Instructions

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Output Format

[Description of expected output]

## Examples

[Optional: Example usage]
```

**GitHub Copilot Prompt** (`.github/my-command.prompt.md`):

```markdown
# My Command

[Brief description]

## Task

[What the agent should do]

## Steps

1. [Step 1]
2. [Step 2]
3. [Step 3]

## Output

[Expected output format]
```

### 3. Update Manifest

Add your command to `kits/kits.yaml`:

```yaml
kits:
  dev:
    name: "Dev Kit"
    description: "Solo development essentials"
    files:
      # ... existing files ...

      # Add your command
      - type: "command"
        name: "my-command"
        description: "My command description"
        agents:
          claude:
            source: "dev/commands/.claude/my-command.md"
            path: ".claude/commands/my-command.md"
          copilot:
            source: "dev/commands/.github/my-command.prompt.md"
            path: ".github/prompts/my-command.prompt.md"
```

### 4. Test Your Command

```bash
# Remove old installation
lite-kits remove --all

# Install with your new command
lite-kits add

# Verify it was installed
lite-kits validate

# Test the command
# In your AI assistant:
/my-command
```

---

## Adding Agents or Shells

### Adding a New Agent

To add support for a new AI agent (e.g., Cursor):

**1. Create command variant:**
```bash
kits/dev/commands/.cursor/orient.md
kits/dev/commands/.cursor/commit.md
# ... etc
```

**2. Update manifest:**
```yaml
files:
  - type: "command"
    name: "orient"
    agents:
      claude: { ... }
      copilot: { ... }
      cursor:  # New agent
        source: "dev/commands/.cursor/orient.md"
        path: ".cursor/commands/orient.md"
```

**3. Update detector:**

Edit `src/lite_kits/core/detector.py`:

```python
def _detect_cursor(self) -> bool:
    """Detect Cursor AI assistant."""
    return (self.target_dir / ".cursor").exists()
```

**4. Update manifest.py:**

Add cursor to supported agents in `src/lite_kits/core/manifest.py` if needed.

### Adding a New Shell

To add support for a new shell (e.g., Zsh):

**1. Create script variant:**
```bash
kits/dev/scripts/zsh/my-script.zsh
```

**2. Update manifest:**
```yaml
- type: "script"
  name: "my-script"
  shells:
    bash: { ... }
    powershell: { ... }
    zsh:  # New shell
      source: "dev/scripts/zsh/my-script.zsh"
      path: "scripts/zsh/my-script.zsh"
```

**3. Update detector:**

Edit `src/lite_kits/core/detector.py`:

```python
def _detect_zsh(self) -> bool:
    """Detect Zsh shell."""
    shell = os.environ.get('SHELL', '')
    return 'zsh' in shell.lower()
```

---

## Testing

### Manual Testing

```bash
# Create test project
cd /tmp
specify init test-project
cd test-project

# Test installation
lite-kits add

# Verify status
lite-kits status
lite-kits validate

# Test commands
/orient
/commit
# ... etc

# Test removal
lite-kits remove --all
lite-kits status  # Should show no kits installed
```

### Automated Tests (TODO)

We're working on adding pytest-based tests. Stay tuned!

```bash
# When tests are added:
pytest
pytest --cov=src/lite_kits
```

---

## Pull Request Process

### 1. Create Feature Branch

```bash
git checkout -b feature/my-new-command
```

### 2. Make Changes

- Add your command files
- Update manifest (kits.yaml)
- Update README if needed
- Test locally

### 3. Commit Changes

Use `/commit` command for conventional commits:

```bash
/commit
```

Or manually:

```bash
git commit -m "feat: Add /my-command for XYZ functionality

Adds new command that does XYZ...

🤖 Generated with [Claude Code](https://claude.com/claude-code)

Co-Authored-By: Claude <noreply@anthropic.com>"
```

### 4. Push and Create PR

```bash
git push origin feature/my-new-command
```

Then create PR on GitHub with:
- Clear description of changes
- Examples of command usage
- Screenshots if applicable

### 5. PR Review

- Maintainers will review your PR
- Address any feedback
- Once approved, PR will be merged

---

## Code Style

### Python

- Follow PEP 8
- Use type hints where possible
- Keep functions focused and single-purpose
- Add docstrings to classes and functions

```python
def example_function(param: str) -> bool:
    """Brief description of what this function does.

    Args:
        param: Description of parameter

    Returns:
        Description of return value
    """
    # Implementation
    return True
```

### Markdown (Command Files)

- Use clear, concise language
- Break instructions into numbered steps
- Include examples where helpful
- Keep formatting consistent with existing commands

### YAML (Manifest)

- Use 2-space indentation
- Keep structure consistent
- Add comments for complex sections
- Validate YAML syntax before committing

---

## What to Contribute

### High Priority

- **New commands** for existing kits
- **Bug fixes** for installer or CLI
- **Documentation improvements**
- **Tests** (when test framework is added)
- **Example projects**

### Medium Priority

- **New kit ideas** (propose via issue first)
- **Performance improvements**
- **Error message improvements**
- **Platform-specific enhancements**

### Low Priority

- **Cosmetic changes** (unless part of larger improvement)
- **Refactoring** (discuss in issue first)

---

## Getting Help

- **Questions**: [GitHub Discussions](https://github.com/tmorgan181/lite-kits/discussions)
- **Bugs**: [GitHub Issues](https://github.com/tmorgan181/lite-kits/issues)
- **Feature Requests**: [GitHub Issues](https://github.com/tmorgan181/lite-kits/issues) with `enhancement` label

---

## Code of Conduct

Be respectful, inclusive, and constructive. We're all here to make lite-kits better!

---

## License

By contributing to lite-kits, you agree that your contributions will be licensed under the MIT License.

---

**Thank you for contributing!** 🎉

Your contributions help make spec-driven development better for everyone.
