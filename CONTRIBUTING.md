# Contributing to spec-kit-multiagent

## Quick Start

```bash
# Fork and clone
git clone https://github.com/yourusername/spec-kit-multiagent-lite.git
cd spec-kit-multiagent-lite

# Install dev mode
pip install -e ".[dev]"

# Make changes
# ...

# Test locally
cd /tmp/test-vanilla-project
speckit-ma install --kit=project

# Submit PR
```

## What to Contribute

### High Priority
- [ ] Commands in empty kit directories
- [ ] Tests for installer and CLI
- [ ] Example project completions
- [ ] Bug fixes

### Medium Priority
- [ ] New kit ideas
- [ ] Documentation improvements
- [ ] Script enhancements

## Adding a New Command

### 1. Create Command Files

```bash
# For both agents (Claude + Copilot)
kits/YOUR-KIT/claude/commands/YOUR-COMMAND.md
kits/YOUR-KIT/github/prompts/YOUR-COMMAND.prompt.md
```

### 2. Command Structure

```markdown
# /your-command

**Purpose**: Brief description

**What it does**:
1. Step one
2. Step two
3. Step three

**Example usage**:
\`\`\`
/your-command

[Example output]
\`\`\`

**When to use**: Clear use case
```

### 3. Update Kit README

Add command to kit's README.md status table.

### 4. Test Installation

```bash
# Test on vanilla project
speckit-ma install --kit=YOUR-KIT
ls .claude/commands/YOUR-COMMAND.md  # Verify installed
```

## Kit Design Principles

### ✅ DO
- Add new files only
- Support both Claude + Copilot
- Support both Bash + PowerShell
- Keep commands simple
- Write for users, not developers

### ❌ DON'T
- Modify vanilla spec-kit files
- Add runtime dependencies
- Create tight coupling between kits
- Assume specific project structures

## Testing

```bash
# Run tests (when available)
pytest
pytest --cov=src/speckit_multiagent

# Manual testing
cp -r docs/vanilla-reference/claude-code-vanilla /tmp/test
cd /tmp/test
speckit-ma install --recommended
# Verify files created correctly
```

## Commit Messages

Follow conventional commits:
```
feat(kit-name): Add /your-command
fix(installer): Resolve path issue
docs: Update README examples
test: Add installer tests
```

## Pull Request Process

1. Create feature branch from `main`
2. Keep changes focused and minimal
3. Update relevant documentation
4. Reference related issues
5. Request review

## Questions?

- [Discussions](https://github.com/tmorgan181/spec-kit-multiagent-lite/discussions)
- [Issues](https://github.com/tmorgan181/spec-kit-multiagent-lite/issues)

## License

MIT - Your contributions will be licensed under MIT.
