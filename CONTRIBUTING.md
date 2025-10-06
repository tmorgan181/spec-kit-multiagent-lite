# Contributing to spec-kit-multiagent

🚧 **Status**: Coming Soon

Thank you for your interest in contributing!

## Quick Start

```bash
# Fork and clone
git clone https://github.com/yourusername/spec-kit-multiagent-lite.git
cd spec-kit-multiagent-lite

# Install in development mode
pip install -e ".[dev]"

# Make changes
# ...

# Run tests (when available)
pytest

# Submit PR
```

## What to Contribute

### High Priority
- [ ] **Tests**: Unit tests for installer.py and cli.py
- [ ] **Examples**: Complete minimal-todo-app and blog-with-auth
- [ ] **Templates**: Collaboration directory templates
- [ ] **Smart merge**: Constitution merge logic

### Medium Priority
- [ ] **Session helpers**: CLI for session management
- [ ] **Agent detection**: Auto-detect Claude/Copilot/Cursor
- [ ] **Validation**: Enhanced validation checks
- [ ] **Documentation**: Tutorials, guides

### Ideas Welcome
- Better orient command customization
- Integration with other AI coding tools
- CI/CD workflows for multiagent projects
- Dashboard for coordination status

## Development Guidelines

### Code Style
- Python: Follow PEP 8, use `ruff` for linting
- Type hints for all public functions
- Docstrings (Google style) for modules and functions

### Commit Messages
Follow conventional commits:
```
feat: Add session management CLI
fix: Resolve path traversal in installer
docs: Update README with examples
test: Add installer unit tests
```

### Pull Requests
- Create feature branch from main
- Include tests if applicable
- Update README/docs as needed
- Reference related issues

## Testing

TODO: Add test guidelines once test suite exists

```bash
pytest
pytest --cov=src/speckit_multiagent
```

## Questions?

- Open a [Discussion](https://github.com/yourusername/spec-kit-multiagent-lite/discussions)
- File an [Issue](https://github.com/yourusername/spec-kit-multiagent-lite/issues)

## License

By contributing, you agree your contributions will be licensed under the MIT License.
