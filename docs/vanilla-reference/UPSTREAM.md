# Updating from Upstream Spec-Kit

This document explains how to update the vanilla spec-kit reference configurations when GitHub releases new versions.

## Upstream Source

**GitHub spec-kit**: https://github.com/github/spec-kit

This is the official vanilla spec-kit repository maintained by GitHub Next.

## Update Frequency

Check for updates:
- **Monthly**: Quick check for major changes
- **Quarterly**: Full sync and test
- **On major releases**: Immediate update and compatibility check

## Update Process

### 1. Check for Upstream Changes

```bash
# Visit GitHub spec-kit releases
open https://github.com/github/spec-kit/releases

# Or check commits
open https://github.com/github/spec-kit/commits/main
```

### 2. Download Latest Vanilla

```bash
# Clone fresh copy
cd /tmp
git clone https://github.com/github/spec-kit.git spec-kit-latest
cd spec-kit-latest
```

### 3. Compare with Our Vanilla

```bash
# Compare directories
diff -r /tmp/spec-kit-latest/.claude docs/vanilla-reference/claude-code-vanilla/.claude
diff -r /tmp/spec-kit-latest/.github docs/vanilla-reference/github-cli-vanilla/.github
diff -r /tmp/spec-kit-latest/.specify docs/vanilla-reference/claude-code-vanilla/.specify

# Look for:
# - New commands
# - Modified templates
# - New scripts
# - Changed workflows
```

### 4. Update Our Vanilla Copies

**Important**: Only update the vanilla reference directories, not our kits!

```bash
# Backup current vanilla
cp -r docs/vanilla-reference/claude-code-vanilla docs/vanilla-reference/claude-code-vanilla.backup

# Copy new vanilla files
rsync -av --delete /tmp/spec-kit-latest/.claude/ docs/vanilla-reference/claude-code-vanilla/.claude/
rsync -av --delete /tmp/spec-kit-latest/.specify/ docs/vanilla-reference/claude-code-vanilla/.specify/

# Repeat for github-cli-vanilla if there are GitHub Copilot specific changes
```

### 5. Test Compatibility

```bash
# Test our kits still install on updated vanilla
cd /tmp
cp -r docs/vanilla-reference/claude-code-vanilla test-install
cd test-install

# Install our kits
lite-kits install -Recommended

# Verify no conflicts
ls -la .claude/commands/
ls -la .specify/scripts/

# Test vanilla commands still work
.specify/scripts/bash/create-new-feature.sh "Test"

# Test our commands work
# In Claude Code: /orient
```

### 6. Update Changelog

Document changes in main [CHANGELOG.md](../CHANGELOG.md):

```markdown
## [Unreleased]
### Vanilla Spec-Kit Updated
- Updated to spec-kit v1.2.3 (2025-10-15)
- Changes:
  - New /analyze command in vanilla
  - Updated plan template
  - Enhanced prerequisite checks
- Compatibility: ✅ All kits tested and working
```

### 7. Commit Changes

```bash
git add docs/vanilla-reference/
git commit -m "chore: Update vanilla spec-kit to v1.2.3

- Updated claude-code-vanilla from upstream
- Updated github-cli-vanilla from upstream
- Tested compatibility with all kits
- No breaking changes detected

Upstream: https://github.com/github/spec-kit/releases/tag/v1.2.3

via claude-sonnet-4.5 @ claude-code"
```

## Breaking Changes from Upstream

If upstream makes breaking changes:

### Scenario 1: New Command Conflicts with Ours

**Example**: Upstream adds `/orient` command

**Solution**:
1. Rename our command to `/orient-ma` (multiagent version)
2. Or: Detect upstream version and only install ours if missing
3. Update documentation explaining difference

```python
# In installer.py
def should_install_orient(self):
    """Check if vanilla already has /orient"""
    vanilla_orient = self.target_dir / ".claude" / "commands" / "orient.md"
    if vanilla_orient.exists():
        console.print("[yellow]Vanilla /orient detected, skipping project-kit /orient[/yellow]")
        return False
    return True
```

### Scenario 2: Script Signature Changes

**Example**: `create-new-feature.sh` changes arguments

**Solution**:
1. Update our enhanced script to match new signature
2. Test both vanilla and enhanced versions
3. Add compatibility layer if needed

### Scenario 3: Template Structure Changes

**Example**: `spec-template.md` gets new sections

**Solution**:
1. Update our templates if we reference spec structure
2. Test that our commands still work with new templates
3. Document any new features users should know about

## Conflict Detection

Our installer should detect vanilla version:

```python
# In installer.py
def detect_vanilla_version(self) -> str:
    """Detect vanilla spec-kit version if possible"""
    # Check for version file or git tag
    # Return version string or "unknown"
    pass

def check_compatibility(self, vanilla_version: str) -> bool:
    """Check if our kits are compatible with vanilla version"""
    # Known compatible versions
    compatible = ["1.0.0", "1.1.0", "1.2.0"]
    if vanilla_version in compatible:
        return True

    # Warn about unknown versions
    console.print(f"[yellow]Warning: Vanilla version {vanilla_version} not tested[/yellow]")
    return True  # Allow installation anyway
```

## Version Pinning (Not Recommended)

We intentionally **don't pin** to specific vanilla versions because:

- ✅ Users should get upstream improvements automatically
- ✅ We only add files, never modify vanilla
- ✅ Breaking changes from upstream are rare
- ✅ Can always uninstall our kits and return to pure vanilla

If you need to pin for stability:

```bash
# In pyproject.toml (if we add vanilla as dependency in future)
[project]
dependencies = [
    "spec-kit>=1.0.0,<2.0.0",  # Major version lock
]
```

## Communication

When updating vanilla:

1. **Test thoroughly** - Don't break users' workflows
2. **Document changes** - Clear changelog entry
3. **Announce if breaking** - GitHub Discussions post
4. **Provide migration path** - If users need to update

## Automated Checks (Future)

Consider adding automated upstream checks:

```yaml
# .github/workflows/check-upstream.yml
name: Check Upstream Spec-Kit

on:
  schedule:
    - cron: '0 0 * * 1'  # Weekly on Monday

jobs:
  check:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v3
      - name: Check for upstream updates
        run: |
          # Clone upstream
          # Compare versions
          # Create issue if updates available
```

## Questions?

- **How often should I update?** - Quarterly, or when major upstream release
- **What if I break compatibility?** - Test before committing, roll back if needed
- **Should users update vanilla themselves?** - Yes, independently of our kits
- **Do kits auto-update with vanilla?** - No, kits and vanilla are independent

## Related

- Vanilla configurations: [docs/vanilla-reference/](.)
- Kit implementations: [../src/speckit_multiagent/kits/](../src/speckit_multiagent/kits/)
- Testing: [../tests/](../tests/) (TODO)
