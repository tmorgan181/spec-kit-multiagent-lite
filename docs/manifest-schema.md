# Lite-Kits Manifest Schema

**Version**: 1.0
**Last Updated**: 2025-10-09
**Manifest Location**: `src/lite_kits/kits/kits.yaml`

---

## Overview

The manifest is a YAML file that defines all kits, commands, files, agents, shells, and installation options for lite-kits. It serves as the single source of truth for the entire package.

**Design Principles:**
- **Manifest-Driven**: Zero hardcoded identifiers in Python code
- **DRY**: Constants defined once at the top
- **Extensible**: Easy to add new kits, agents, shells, or commands
- **Self-Documenting**: Clear structure with inline comments

---

## File Structure

```
kits.yaml
├── metadata           # Manifest metadata and compatibility (at top for easy reference)
├── constants          # Reusable constants (versions, paths, types, etc.)
├── spec_kit           # Spec-kit project detection rules
├── kits               # Kit definitions (dev, multiagent, etc.)
├── agents             # AI assistant configurations
├── shells             # Shell environment configurations
└── options            # Installation behavior settings
```

---

## Top-Level Sections

### 1. `metadata`

Manifest metadata and compatibility information (placed at top for easy reference).

```yaml
metadata:
  manifest_version: "1.0"
  last_updated: "2025-10-09"
  schema_url: "https://github.com/tmorgan181/lite-kits/blob/main/docs/manifest-schema.md"

  # Compatibility
  min_lite_kits_version: "0.2.0"
  min_spec_kit_version: "0.1.0"
```

**Fields:**
- `manifest_version` (string, required): Manifest schema version
- `last_updated` (string, required): Last update date (YYYY-MM-DD)
- `schema_url` (string, required): URL to this schema documentation
- `min_lite_kits_version` (string, required): Minimum lite-kits package version
- `min_spec_kit_version` (string, required): Minimum vanilla spec-kit version

---

### 2. `constants`

Reusable constants to maintain DRY principle. These are documented for reference but not interpolated (YAML doesn't support `${var}` syntax).

```yaml
constants:
  versions:              # Version tracking
    manifest: "1.0"
    dev_kit: "0.2.0"
    multiagent_kit: "0.2.0"
    min_lite_kits: "0.2.0"
    min_spec_kit: "0.1.0"

  status_values:         # Command/feature lifecycle states
    stable: "stable"
    beta: "beta"
    planned: "planned"
    deprecated: "deprecated"

  file_types:            # File type classifications
    command: "command"
    prompt: "prompt"
    script: "script"
    memory: "memory"
    template: "template"

  categories:            # Organizational categories
    project: "project"
    git: "git"
    analysis: "analysis"
    coordination: "coordination"
    workflow: "workflow"
    collaboration: "collaboration"

  required_values:       # Validation flags
    required: true
    optional: false

  paths:                 # Directory structure constants
    kit_sources: {...}   # Source directories in lite-kits
    content_dirs: {...}  # Content type subdirectories
    agent_dirs: {...}    # Agent subdirectories
    shell_dirs: {...}    # Shell subdirectories
    target_paths: {...}  # Installation paths in user projects
```

**Usage**: Use these values consistently throughout the manifest to ensure maintainability.

---

### 3. `spec_kit`

Detection rules for spec-kit projects.

```yaml
spec_kit:
  markers:
    - path: ".specify"
      type: "directory"
      description: "Spec-kit core directory"
    - path: ".claude"
      type: "directory"
      description: "Claude Code commands directory"
    - path: ".github/prompts"
      type: "directory"
      description: "GitHub Copilot prompts directory"

  require_any: true  # At least one marker must exist
```

**Fields:**
- `markers`: List of files/directories that indicate a spec-kit project
  - `path`: Relative path from project root
  - `type`: `"file"` or `"directory"`
  - `description`: Human-readable description
- `require_any`: Boolean - `true` = at least one marker, `false` = all markers required

---

### 4. `kits`

Kit definitions. Each kit is a collection of commands, files, and metadata.

```yaml
kits:
  <kit_id>:
    name: "Display Name"
    description: "Short description"
    icon: "🚀"
    recommended: true/false
    version: "0.2.0"

    commands:
      - name: "command_name"
        description: "Command description"
        status: "stable"      # stable | beta | planned | deprecated
        category: "project"   # project | git | analysis | coordination | workflow | collaboration

    files:
      <agent_or_shell>:
        - path: ".claude/commands/example.md"        # Where file goes in user project
          source: "dev/commands/.claude/example.md"  # Where file is in lite-kits
          required: true/false
          type: "command"                            # command | prompt | script | memory | template
          category: "project"
          status: "stable"                           # Optional, defaults to stable

    markers:
      - ".claude/commands/example.md"  # Files whose existence indicates kit is installed
```

**Kit Structure:**

**Top-Level Fields:**
- `name` (string, required): Display name
- `description` (string, required): User-facing description
- `icon` (string, optional): Emoji or symbol
- `recommended` (boolean, required): Include in `--recommended` flag
- `version` (string, required): Kit version (semver)

**Commands Array:**
- `name` (string, required): Command name (e.g., "orient", "commit")
- `description` (string, required): What the command does
- `status` (string, required): Lifecycle state (see `status_values` in constants)
- `category` (string, required): Organizational category (see `categories` in constants)

**Files Object:**

Organized by agent or shell identifier (e.g., `claude`, `copilot`, `bash`, `powershell`, `memory`, `templates`).

Each file entry contains:
- `path` (string, required): Installation path in user's project
- `source` (string, required): Source path in lite-kits package
- `required` (boolean, required): If `false`, file is optional
- `type` (string, required): File type classification (see `file_types` in constants)
- `category` (string, required): Organizational category
- `status` (string, optional): Defaults to "stable", use for planned features

**Markers Array:**
- List of file paths whose existence indicates the kit is installed
- Used for detection in `status` and `validate` commands

---

### 5. `agents`

AI assistant configurations for auto-detection and installation.

```yaml
agents:
  <agent_id>:
    name: "Agent Name"
    marker_dir: ".claude"               # Directory that indicates agent is present
    commands_dir: ".claude/commands"    # Where commands are installed
    file_extension: ".md"               # File extension for commands
    supported: true/false               # Whether lite-kits supports this agent
    priority: 1                         # Lower = higher priority for auto-detection
    status: "planned"                   # Optional, for future agents
```

**Fields:**
- `name` (string, required): Display name
- `marker_dir` (string, required): Directory whose existence indicates agent presence
- `commands_dir` (string, required): Target directory for command files
- `file_extension` (string, required): Extension for command files (e.g., `.md`, `.prompt.md`)
- `supported` (boolean, required): Whether lite-kits currently supports this agent
- `priority` (integer, required): Auto-detection priority (1 = highest)
- `status` (string, optional): For future/planned agents

**Current Agents:**
- `claude`: Claude Code (.claude/commands/)
- `copilot`: GitHub Copilot (.github/prompts/)
- `cursor`: Planned
- `windsurf`: Planned

---

### 6. `shells`

Shell environment configurations for script installation.

```yaml
shells:
  <shell_id>:
    name: "Shell Name"
    extension: ".sh"
    script_dir: ".specify/scripts/bash"
    platforms: ["linux", "macos", "wsl"]
    supported: true/false
    priority: 1
    status: "planned"  # Optional
```

**Fields:**
- `name` (string, required): Display name
- `extension` (string, required): Script file extension (e.g., `.sh`, `.ps1`)
- `script_dir` (string, required): Target directory for scripts
- `platforms` (array, required): Supported platforms (`"linux"`, `"macos"`, `"windows"`, `"wsl"`)
- `supported` (boolean, required): Whether lite-kits currently supports this shell
- `priority` (integer, required): Auto-detection priority (1 = highest)
- `status` (string, optional): For future/planned shells

**Current Shells:**
- `bash`: Bash (.sh)
- `powershell`: PowerShell (.ps1, cross-platform)
- `fish`: Planned
- `zsh`: Planned

---

### 7. `options`

Installation and validation behavior settings.

```yaml
options:
  # Kit selection
  default_kit: "dev"
  recommended_kits: ["dev"]

  # Installation behavior
  allow_partial_install: true
  skip_existing: true
  validate_on_install: true
  create_backups: false

  # Auto-detection behavior
  auto_detect_agents: true
  auto_detect_shells: true
  prefer_all_agents: true
  prefer_all_shells: false

  # Validation behavior
  check_file_integrity: true
  min_file_size: 100

  # Future options
  enable_telemetry: false
  auto_update_check: false
```

**Fields:**

**Kit Selection:**
- `default_kit` (string): Kit installed when no `--kit` specified
- `recommended_kits` (array): Kits installed with `--recommended` flag

**Installation Behavior:**
- `allow_partial_install` (boolean): Can install for just one agent/shell
- `skip_existing` (boolean): Don't overwrite existing files by default
- `validate_on_install` (boolean): Run validation after installation
- `create_backups` (boolean): Create `.bak` files before overwriting (future)

**Auto-Detection Behavior:**
- `auto_detect_agents` (boolean): Automatically detect which agents are present
- `auto_detect_shells` (boolean): Automatically detect which shells to install for
- `prefer_all_agents` (boolean): Install for all detected agents by default
- `prefer_all_shells` (boolean): Install for all detected shells by default

**Validation Behavior:**
- `check_file_integrity` (boolean): Verify file contents during validation
- `min_file_size` (integer): Minimum file size in bytes to be considered valid

**Future Options:**
- `enable_telemetry` (boolean): Anonymous usage stats (planned)
- `auto_update_check` (boolean): Check for kit updates (planned)

---

## Directory Structure

The manifest uses a **content-first hierarchy** for scalability:

### Lite-Kits Package Structure
```
src/lite_kits/kits/
├── kits.yaml           # This manifest
├── dev/
│   ├── commands/
│   │   ├── .claude/    # Claude Code command files
│   │   └── .github/    # GitHub Copilot prompt files
│   ├── scripts/
│   │   ├── bash/       # Bash scripts (no dot)
│   │   └── powershell/ # PowerShell scripts (no dot)
│   ├── memory/         # Memory guides (placeholder)
│   └── templates/      # Templates (placeholder)
└── multiagent/
    ├── commands/
    │   ├── .claude/
    │   └── .github/
    ├── scripts/
    │   ├── bash/
    │   └── powershell/
    ├── memory/         # Multi-agent memory guides
    └── templates/      # Collaboration templates
```

### User Project Structure
```
user-project/
├── .specify/
│   ├── scripts/
│   │   ├── bash/
│   │   └── powershell/
│   ├── memory/
│   └── templates/
├── .claude/
│   └── commands/
└── .github/
    └── prompts/
```

**Design Rationale:**
- **Content-first**: Easy to add new content types (e.g., `workflows/`)
- **Agent subdirectories**: Easy to add new agents (e.g., `commands/.cursor/`)
- **Shell subdirectories**: Easy to add new shells (e.g., `scripts/fish/`)
- **Dots for agents**: Match user project structure (`.claude`, `.github`)
- **No dots for shells**: Match vanilla spec-kit convention (`bash`, `powershell`)

---

## Adding New Kits

To add a new kit:

1. **Create directory structure** in `src/lite_kits/kits/<kit-name>/`
   ```
   <kit-name>/
   ├── commands/.claude/
   ├── commands/.github/
   ├── scripts/bash/
   ├── scripts/powershell/
   ├── memory/
   └── templates/
   ```

2. **Add files** to appropriate directories

3. **Update manifest** (`kits.yaml`):
   ```yaml
   kits:
     <kit-name>:
       name: "My Kit"
       description: "..."
       version: "0.1.0"
       recommended: false
       commands: [...]
       files: [...]
       markers: [...]
   ```

4. **Add to constants** (if needed):
   - Update `versions.<kit-name>_kit`
   - Update `paths.kit_sources.<kit-name>`

5. **Test** with `lite-kits add --kit <kit-name>`

---

## Adding New Agents

To add a new agent (e.g., Cursor):

1. **Create directory** in each kit: `<kit>/commands/.cursor/`

2. **Add agent to manifest**:
   ```yaml
   agents:
     cursor:
       name: "Cursor"
       marker_dir: ".cursor"
       commands_dir: ".cursor/commands"
       file_extension: ".md"
       supported: true
       priority: 3
   ```

3. **Add files to each kit**:
   ```yaml
   kits:
     dev:
       files:
         cursor:
           - path: ".cursor/commands/orient.md"
             source: "dev/commands/.cursor/orient.md"
             required: true
             type: "command"
             category: "project"
   ```

4. **Update constants**:
   ```yaml
   paths:
     agent_dirs:
       cursor: ".cursor"
     target_paths:
       cursor_commands: ".cursor/commands"
   ```

5. **Test** with `lite-kits add --agent cursor`

---

## Adding New Shells

To add a new shell (e.g., Fish):

1. **Create directory** in each kit: `<kit>/scripts/fish/`

2. **Add shell to manifest**:
   ```yaml
   shells:
     fish:
       name: "Fish Shell"
       extension: ".fish"
       script_dir: ".specify/scripts/fish"
       platforms: ["linux", "macos"]
       supported: true
       priority: 3
   ```

3. **Add scripts to each kit**:
   ```yaml
   kits:
     dev:
       files:
         fish:
           - path: ".specify/scripts/fish/git-status.fish"
             source: "dev/scripts/fish/git-status.fish"
             required: false
             type: "script"
             category: "git"
   ```

4. **Update constants**:
   ```yaml
   paths:
     shell_dirs:
       fish: "fish"
   ```

5. **Test** with `lite-kits add --shell fish`

---

## Validation Rules

The manifest must adhere to these rules:

**Required Fields:**
- All top-level sections must be present
- Each kit must have: `name`, `description`, `version`, `recommended`, `commands`, `files`, `markers`
- Each agent must have: `name`, `marker_dir`, `commands_dir`, `file_extension`, `supported`, `priority`
- Each shell must have: `name`, `extension`, `script_dir`, `platforms`, `supported`, `priority`

**File Paths:**
- `source` paths must exist in the lite-kits package
- `path` (target) paths must be valid relative paths
- Agent directories must start with `.` (e.g., `.claude`)
- Shell directories must NOT start with `.` (e.g., `bash`)

**Consistency:**
- Status values must match `status_values` in constants
- Type values must match `file_types` in constants
- Category values must match `categories` in constants
- Agent IDs in `files` must match keys in `agents` section
- Shell IDs in `files` must match keys in `shells` section

**Versioning:**
- All versions must follow semantic versioning (e.g., `0.2.0`)
- `min_lite_kits_version` must be ≤ current lite-kits version
- Kit versions should increment with changes

---

## Best Practices

1. **Use constants**: Reference the constants section when adding new values
2. **Document changes**: Update `last_updated` in metadata
3. **Test thoroughly**: Run full test suite after manifest changes
4. **Increment versions**: Bump kit versions when making changes
5. **Maintain DRY**: Don't repeat paths, types, or categories
6. **Comment liberally**: Help future maintainers understand decisions
7. **Follow hierarchy**: Content-first, then agent/shell subdirectories
8. **Validate before commit**: Ensure YAML is valid and references are correct

---

## Troubleshooting

**Common Issues:**

1. **Files not installing**: Check `source` path exists in package
2. **Agent not detected**: Verify `marker_dir` exists in user project
3. **Wrong files installed**: Check agent/shell ID matches in `files` section
4. **Validation fails**: Ensure `markers` list includes installed files
5. **YAML parse errors**: Validate syntax with `yamllint` or online validator

**Debug Commands:**
```bash
# Check manifest syntax
python -c "import yaml; yaml.safe_load(open('src/lite_kits/kits/kits.yaml'))"

# Dry-run installation
lite-kits add --kit dev --dry-run

# Validate installation
lite-kits validate
```

---

## Version History

**1.0** (2025-10-09)
- Initial schema documentation
- Content-first directory structure
- Constants section for DRY principle
- Support for dev-kit and multiagent-kit
- Claude Code and GitHub Copilot agents
- Bash and PowerShell shells

---

## Related Documentation

- [Lite-Kits README](../README.md)
- [Kit Development Guide](kit-development.md) *(planned)*
- [Manifest Changelog](manifest-changelog.md) *(planned)*
- [Contributing Guidelines](../CONTRIBUTING.md) *(planned)*

---

**Questions or Issues?**
Open an issue: https://github.com/tmorgan181/lite-kits/issues
