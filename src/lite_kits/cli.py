#!/usr/bin/env python3
"""
CLI for lite-kits

Lightweight enhancement kits for spec-driven development.
"""

import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from . import (
    __version__,
    APP_NAME,
    APP_DESCRIPTION,
    REPOSITORY_URL,
    LICENSE,
    KIT_DEV,
    KIT_MULTIAGENT,
    KITS_ALL,
    KIT_DESC_DEV,
    KIT_DESC_MULTIAGENT,
    DIR_CLAUDE_COMMANDS,
    DIR_GITHUB_PROMPTS,
    DIR_SPECIFY_MEMORY,
    DIR_SPECIFY_SCRIPTS_BASH,
    DIR_SPECIFY_SCRIPTS_POWERSHELL,
    DIR_SPECIFY_TEMPLATES,
    ERROR_NOT_SPEC_KIT,
    ERROR_SPEC_KIT_HINT,
)
from .core import diagonal_reveal_banner, show_loading_spinner, show_static_banner, Installer

app = typer.Typer(
    name=APP_NAME,
    help=APP_DESCRIPTION,  # Restore original description for --help
    no_args_is_help=False,  # We'll handle no-args case ourselves
    add_completion=False,
    rich_markup_mode="rich",
)
console = Console()

def print_help_hint():
    console.print(f"[dim]See [bold cyan]--help[/bold cyan] for all options and commands.[/dim]\n")

def print_version_info():
    """Print version information."""
    console.print(f"[bold]Version:[/bold]")
    console.print(f"  [bold cyan]{APP_NAME} version {__version__}[/bold cyan]")

def print_quick_start():
    console.print("[bold]Quick Start:[/bold]")
    console.print(f"  [cyan]1. {APP_NAME} add[/cyan]          # Add dev-kit (default)")
    console.print(f"  [cyan]2. {APP_NAME} status[/cyan]       # Check installation")
    console.print(f"  [cyan]3. {APP_NAME} validate[/cyan]     # Validate kit files\n")

def print_spec_kit_error():
    """Print standardized spec-kit not found error message with installation instructions."""
    console.print()
    console.print(
        f"[red]Error:[/red] {ERROR_NOT_SPEC_KIT}",
        style="bold",
    )
    console.print(
        f"\n  {ERROR_SPEC_KIT_HINT}",
        style="dim",
    )
    console.print("\n[bold yellow]lite-kits requires GitHub Spec-Kit:[/bold yellow]")
    console.print("  lite-kits enhances vanilla spec-kit projects with additional commands.")
    console.print("  You must install spec-kit first before adding lite-kits enhancements.\n")
    console.print("[bold cyan]Install Spec-Kit:[/bold cyan]")
    console.print("  1. Install Node.js: https://nodejs.org/")
    console.print("  2. Install spec-kit: npm install -g @github/spec-kit")
    console.print("  3. Create project: specify init your-project-name")
    console.print("  4. More info: https://github.com/github/spec-kit\n")
    console.print()

def print_kit_info(target_dir: Path, is_spec_kit: bool, installed_kits: list):
    """Print kit installation info."""
    console.print()
    if is_spec_kit:
        console.print(f"[bold green][OK] Spec-kit project detected in {target_dir}.[/bold green]\n")
        if installed_kits:
            console.print("Installed kits:", style="bold")
            for kit in installed_kits:
                console.print(f"  [green]+[/green] {kit}-kit")
        else:
            console.print("No kits installed.", style="dim yellow")
    else:
        console.print(f"[bold red][X] {target_dir} is not a spec-kit project[/bold red]")
        console.print(f"  {ERROR_SPEC_KIT_HINT}", style="dim")
    console.print()

def version_callback(value: bool):
    """Print version and exit."""
    if value:
        console.print()
        print_version_info()
        raise typer.Exit()

@app.callback(invoke_without_command=True)
def main(
    ctx: typer.Context,
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-V",
        help="Display the lite-kits version",
        callback=version_callback,
        is_eager=True,
    ),
    banner: Optional[bool] = typer.Option(
        None,
        "--banner",
        help="Show the animated banner (can be combined with other commands)",
    ),
    quiet: Optional[bool] = typer.Option(
        None,
        "--quiet",
        "-q",
        help="Use quiet output",
    ),
    verbose: Optional[bool] = typer.Option(
        None,
        "--verbose",
        "-v",
        help="Use verbose output",
    ),
    directory: Optional[Path] = typer.Option(
        None,
        "--directory",
        help="Change to the given directory prior to running the command",
    ),
):
    """Main CLI entry point."""
    if directory:
        import os
        os.chdir(directory)

    # Store banner flag in context for commands to use
    ctx.obj = {"show_banner": banner}

    # Show banner if requested
    if banner:
        try:
            diagonal_reveal_banner()
        except UnicodeEncodeError:
            # Windows console doesn't support Unicode box characters
            console.print("[bold cyan]LITE-KITS[/bold cyan]")
            console.print("[dim]Lightweight enhancement kits for spec-driven development[/dim]\n")

    # Show banner + hint and quick-start when no command is given
    if ctx.invoked_subcommand is None:
        if not banner:  # Only show static banner if animated not already shown
            show_static_banner()
        print_help_hint()
        print_quick_start()

@app.command(hidden=True)
def help(ctx: typer.Context):
    """Show help information (alias for --help)."""
    console.print(ctx.parent.get_help())

@app.command(name="add")
def add_kits(
    kit: Optional[str] = typer.Option(
        None,
        "--kit",
        help=f"Comma-separated list of kits to add: {','.join(KITS_ALL)}",
    ),
    all_kits: bool = typer.Option(
        False,
        "--all",
        help="Add all kits",
    ),
    agent: Optional[str] = typer.Option(
        None,
        "--agent",
        help="Explicit agent preference (claude, copilot, etc.)",
    ),
    shell: Optional[str] = typer.Option(
        None,
        "--shell",
        help="Explicit shell preference (bash, powershell)",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show detailed file listings in preview",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Skip preview and confirmations, overwrite existing files",
    ),
    target: Optional[Path] = typer.Argument(
        None,
        help="Target directory (defaults to current directory)",
    ),
):
    """Add enhancement kits to a spec-kit project.

    Shows a preview of changes before installation and asks for confirmation.
    Use --verbose/-v to see detailed file listings.
    Use --force to skip preview and install immediately.
    """
    target_dir = Path.cwd() if target is None else target

    # Determine which kits to install
    kits = None
    if all_kits:
        kits = KITS_ALL
    elif kit:
        kits = [k.strip() for k in kit.split(',')]
    # else: kits=None will use default from manifest

    try:
        installer = Installer(
            target_dir,
            kits=kits,
            force=force,
            agent=agent,
            shell=shell
        )
    except ValueError as e:
        console.print()
        console.print(f"[red]Error:[/red] {e}", style="bold")
        console.print()
        raise typer.Exit(1)

    # Validate target is a spec-kit project
    if not installer.is_spec_kit_project():
        print_spec_kit_error()
        raise typer.Exit(1)

    # Check if already installed (check for dev-kit as default)
    skip_preview = force  # Track if we should skip preview (only when --force flag used)
    reinstalling = False

    if installer.is_kit_installed(KIT_DEV):
        console.print()
        console.print(
            "[yellow]Warning:[/yellow] Enhancement kits appear to be already installed",
            style="bold",
        )
        if not force:
            if not typer.confirm("Reinstall anyway?"):
                console.print()
                raise typer.Exit(0)
            # User confirmed reinstall - mark as reinstalling but still show preview
            reinstalling = True

    # Always show preview unless --force flag was used
    if not skip_preview:
        try:
            preview = installer.preview_installation()
        except ValueError as e:
            console.print()
            console.print(f"[red]Error:[/red] {e}", style="bold")
            console.print()
            raise typer.Exit(1)

        normalized_preview = _normalize_preview_for_display(preview, operation="install")
        _display_changes(normalized_preview, target_dir, verbose=verbose)

        # Show warnings/conflicts
        if preview.get("warnings"):
            console.print("\n[bold yellow]Warnings:[/bold yellow]")
            for warning in preview["warnings"]:
                console.print(f"  ⚠ {warning}")

        if preview.get("conflicts"):
            console.print("\n[bold yellow]Conflicts (will overwrite):[/bold yellow]")
            for conflict in preview["conflicts"]:
                console.print(f"  ⚠ {conflict['path']}")

        # Ask for confirmation
        console.print()
        if not typer.confirm("Proceed with installation?"):
            console.print("[dim]Installation cancelled[/dim]")
            console.print()
            raise typer.Exit(0)

        # User confirmed preview - enable force to bypass conflict checks during install
        # (This recreates installer with force=True to skip conflict detection)
        installer = Installer(
            target_dir,
            kits=kits,
            force=True,  # Skip conflict checks after user confirmed
            agent=agent,
            shell=shell
        )

    # Install
    console.print(f"\n[bold green]Installing kits to {target_dir}[/bold green]\n")
    show_loading_spinner("Installing...")
    result = installer.install()

    if result["success"]:
        _display_installation_summary(result, verbose=verbose)
        console.print("[bold green][OK] Kits installed successfully![/bold green]\n")
    else:
        console.print(f"\n[bold red][X] Installation failed:[/bold red] {result['error']}\n")
        console.print()
        raise typer.Exit(1)

@app.command()
def remove(
    kit: Optional[str] = typer.Option(
        None,
        "--kit",
        help=f"Comma-separated list of kits to remove: {','.join(KITS_ALL)}",
    ),
    all_kits: bool = typer.Option(
        False,
        "--all",
        help="Remove all kits",
    ),
    verbose: bool = typer.Option(
        False,
        "--verbose",
        "-v",
        help="Show detailed file listings in preview",
    ),
    force: bool = typer.Option(
        False,
        "--force",
        help="Skip preview and confirmations",
    ),
    target: Optional[Path] = typer.Argument(
        None,
        help="Target directory (defaults to current directory)",
    ),
):
    """Remove enhancement kits from a spec-kit project.

    Removes kit files and returns the project to vanilla spec-kit state.
    Shows preview of files to be removed before confirmation.
    Use --verbose/-v to see detailed file listings.
    Use --force to skip preview and remove immediately.

    Examples:
        lite-kits remove --kit dev                # Remove dev-kit
        lite-kits remove --kit dev,multiagent     # Remove multiple kits
        lite-kits remove --all                    # Remove all kits
        lite-kits remove --all --force            # Remove all kits without confirmation
    """
    target_dir = Path.cwd() if target is None else target

    # Determine which kits to remove
    kits = None
    if all_kits:
        kits = KITS_ALL
    elif kit:
        kits = [k.strip() for k in kit.split(',')]
    else:
        console.print()
        console.print("[yellow]Error:[/yellow] Specify --kit or --all", style="bold")
        console.print("\nExamples:", style="dim")
        console.print(f"  {APP_NAME} remove --kit {KIT_DEV}", style="dim")
        console.print(f"  {APP_NAME} remove --all", style="dim")
        console.print()
        raise typer.Exit(1)

    try:
        installer = Installer(target_dir, kits=kits)
    except ValueError as e:
        console.print()
        console.print(f"[red]Error:[/red] {e}", style="bold")
        console.print()
        raise typer.Exit(1)

    # Filter to only actually installed kits
    installed_kits = [k for k in kits if installer.is_kit_installed(k)]
    if not installed_kits:
        console.print()
        console.print("[yellow]Warning:[/yellow] No kits detected to remove", style="bold")
        console.print()
        raise typer.Exit(0)

    # Update installer with filtered list
    installer = Installer(target_dir, kits=installed_kits)

    # Show preview and confirmation unless --force is used
    if not force:
        # Show preview of files to be removed
        preview = installer.preview_removal()

        if preview["total_files"] == 0:
            console.print("[dim]No files found to remove[/dim]")
            console.print()
            raise typer.Exit(0)

        # Normalize removal preview to standard format for DRY display
        normalized_preview = _normalize_preview_for_display(preview, operation="remove")
        _display_changes(normalized_preview, target_dir, verbose=verbose)

        # Confirm removal
        if not typer.confirm("Continue with removal?"):
            console.print("[dim]Cancelled[/dim]")
            console.print()
            raise typer.Exit(0)

    # Remove kits
    console.print(f"\n[bold yellow]Removing files...[/bold yellow]")
    result = installer.remove()

    if result["success"]:
        _display_removal_summary(result, verbose=verbose)

        # Clean up empty directories
        _cleanup_empty_directories(target_dir)
        console.print("\n[bold green][OK] Removal complete![/bold green]\n")
    else:
        console.print(f"\n[bold red][X] Removal failed:[/bold red] {result['error']}\n")
        console.print()
        raise typer.Exit(1)

@app.command()
def validate(
    target: Optional[Path] = typer.Argument(
        None,
        help="Target directory (defaults to current directory)",
    ),
):
    """Validate enhancement kit installation integrity.

    Checks:
    - All required kit files are present
    - Files are not corrupted or empty
    - Kit structure is correct
    - Collaboration directories (for multiagent-kit)

    Example:
        lite-kits validate              # Validate current directory
        lite-kits validate path/to/dir  # Validate specific directory
    """
    target_dir = Path.cwd() if target is None else target

    # For validation, we don't know which kits are installed yet, so check for all
    installer = Installer(target_dir, kits=KITS_ALL)

    # Check if it's a spec-kit project first
    if not installer.is_spec_kit_project():
        print_spec_kit_error()
        raise typer.Exit(1)

    # Check if any kits are installed
    any_installed = any(installer.is_kit_installed(k) for k in KITS_ALL)
    if not any_installed:
        console.print()
        console.print("[yellow]⚠ No enhancement kits installed[/yellow]")
        console.print(f"  Run: {APP_NAME} add", style="dim")
        console.print()
        raise typer.Exit(1)

    # Validate structure
    console.print(f"\n[bold cyan]Validating {target_dir}[/bold cyan]\n")
    validation_result = installer.validate()
    _display_validation_results(validation_result)

    if validation_result["valid"]:
        console.print("\n[bold green][OK] Validation passed![/bold green]\n")
        raise typer.Exit(0)
    else:
        console.print("\n[bold red][X] Validation failed[/bold red]\n")
        raise typer.Exit(1)

@app.command()
def status(
    target: Optional[Path] = typer.Argument(
        None,
        help="Target directory (defaults to current directory)",
    ),
):
    """Show enhancement kit installation status.

    Displays:
    - Whether directory is a spec-kit project
    - Which kits are installed (dev, multiagent)
    - Quick summary of installation state

    Example:
        lite-kits status              # Check current directory
        lite-kits status path/to/dir  # Check specific directory
    """
    target_dir = Path.cwd() if target is None else target

    # For status, check for all possible kits
    installer = Installer(target_dir, kits=KITS_ALL)

    # Basic checks
    is_spec_kit = installer.is_spec_kit_project()

    # Check individual kits using the installer's validator
    installed_kits = []
    for kit_name in KITS_ALL:
        if installer.is_kit_installed(kit_name):
            installed_kits.append(kit_name)

    # Show kit info (skip banner to avoid Windows console Unicode issues)
    print_kit_info(target_dir, is_spec_kit, installed_kits)

def _normalize_preview_for_display(preview: dict, operation: str = "install") -> dict:
    """Normalize preview data to standard format for display.

    Converts both installation and removal previews to a unified format
    that _display_changes can handle.

    Args:
        preview: Raw preview dict from installer (preview_installation or preview_removal)
        operation: "install" or "remove" to determine how to process the preview

    Returns:
        Normalized preview dict with standard keys (new_files, modified_files,
        files_to_remove, new_directories, directories_to_remove)
    """
    if operation == "install":
        # Installation preview is already in the right format
        return preview
    elif operation == "remove":
        # Removal preview needs conversion
        normalized = {"kits": []}
        for kit in preview.get("kits", []):
            # Calculate unique directories that will be affected
            directories = set()
            for file_path in kit.get("files", []):
                parent = str(Path(file_path).parent)
                if parent and parent != ".":
                    directories.add(parent)

            normalized["kits"].append({
                "name": kit["name"],
                "new_files": [],
                "modified_files": [],
                "files_to_remove": kit["files"],
                "new_directories": [],
                "directories_to_remove": sorted(directories)
            })
        return normalized
    else:
        raise ValueError(f"Unknown operation: {operation}")

def _display_changes(changes: dict, target_dir: Path, verbose: bool = False):
    """Display preview of changes.

    Args:
        changes: Normalized preview dict with file/directory changes
        target_dir: Target directory being modified
        verbose: If True, show detailed file listings; if False, show only tables
    """
    from collections import defaultdict

    # Show preview header
    console.print(f"\n[bold magenta]Previewing changes for:[/bold magenta]\n[bold yellow]{target_dir}[/bold yellow]\n")

    # Collect stats for each kit
    kit_stats = {}
    total_stats = defaultdict(int)

    for kit in changes.get("kits", []):
        kit_name = kit.get("name", "Unknown Kit")
        stats = defaultdict(int)

        # Count files by type based on path (normalize to forward slashes for matching)
        # Include new_files, modified_files, and files_to_remove
        all_files = (
            kit.get("new_files", []) +
            kit.get("modified_files", []) +
            kit.get("files_to_remove", [])
        )

        for file_path in all_files:
            # Normalize path separators for cross-platform matching
            normalized_path = str(file_path).replace("\\", "/")

            # Track by file type
            if "/commands/" in normalized_path or "/prompts/" in normalized_path:
                stats["commands"] += 1
            elif "/scripts/" in normalized_path:
                stats["scripts"] += 1
            elif "/memory/" in normalized_path:
                stats["memory"] += 1
            elif "/templates/" in normalized_path:
                stats["templates"] += 1
            else:
                stats["other"] += 1

            # Track by agent (for agent breakdown table)
            if ".claude/" in normalized_path:
                stats["agent_claude"] += 1
            elif ".github/" in normalized_path:
                stats["agent_copilot"] += 1
            else:
                stats["agent_shared"] += 1

        # Count directories (both new and to-be-removed)
        stats["directories"] = len(kit.get("new_directories", [])) + len(kit.get("directories_to_remove", []))

        # Total files (excluding directories)
        stats["files"] = len(all_files)

        kit_stats[kit_name.lower().replace(" kit", "")] = stats

        # Accumulate totals
        for key, value in stats.items():
            total_stats[key] += value

    # Display kit details (only if verbose)
    if verbose:
        for kit in changes.get("kits", []):
            kit_name = kit.get("name", "Unknown Kit")
            kit_key = kit_name.lower().replace(" kit", "")
            stats = kit_stats[kit_key]

            console.print(f"[bold magenta]=== {kit_name} ===[/bold magenta]")

            # Only show sections that have items
            new_files = kit.get("new_files", [])
            modified_files = kit.get("modified_files", [])
            files_to_remove = kit.get("files_to_remove", [])
            new_directories = kit.get("new_directories", [])

            if new_files:
                console.print("Files to be created:")
                for file in new_files:
                    console.print(f"  [green]+[/green] {file}")
                console.print()  # Blank line after section

            if modified_files:
                console.print("Files to be modified:")
                for file in modified_files:
                    console.print(f"  [yellow]~[/yellow] {file}")
                console.print()  # Blank line after section

            if files_to_remove:
                console.print("Files to be removed:")
                for file in files_to_remove:
                    console.print(f"  [red]-[/red] {file}")
                console.print()  # Blank line after section

            if new_directories:
                console.print("Directories to be created:")
                for dir in new_directories:
                    console.print(f"  [blue]+[/blue] {dir}")
                console.print()  # Blank line after section

            # Show kit summary
            summary_parts = []
            if stats["files"] > 0:
                summary_parts.append(f"{stats['files']} files")
            if stats["directories"] > 0:
                summary_parts.append(f"{stats['directories']} directory")
            if summary_parts:
                console.print(f"{kit_name}: {', '.join(summary_parts)}")
                console.print()  # Blank line after kit

    # Display summary tables
    _display_preview_tables(kit_stats, changes)

def _display_preview_tables(kit_stats: dict, changes: dict):
    """Display preview summary tables with color-coded values.

    Colors:
    - Green +N: Additions (new files)
    - Yellow ~N: Modifications (changed files)
    - Red -N: Removals (deleted files)
    - White 0: No changes
    """
    from rich.box import ROUNDED

    if not kit_stats:
        return

    # Helper to format kit names
    def format_kit_name(kit_key: str) -> str:
        return "Dev Kit" if kit_key == "dev" else "Multiagent Kit"

    # Helper to style values based on operation type
    def style_value(value: int, is_addition: bool = True, is_modification: bool = False) -> str:
        """Style numeric values with colors and prefix symbols."""
        if value == 0:
            return "0"
        elif is_modification:
            return f"[yellow]~{value}[/yellow]"
        elif is_addition:
            return f"[green]+{value}[/green]"
        else:  # removal
            return f"[red]-{value}[/red]"

    # Determine operation type from changes dict
    has_new_files = any(kit.get("new_files") for kit in changes.get("kits", []))
    has_modified_files = any(kit.get("modified_files") for kit in changes.get("kits", []))
    is_removal = not has_new_files and not has_modified_files  # If no new/modified, it's a removal

    # Agent breakdown table (show which agents get which files)
    agent_categories = ["agent_claude", "agent_copilot", "agent_shared"]
    has_agent_breakdown = any(
        any(stats.get(cat, 0) > 0 for cat in agent_categories)
        for stats in kit_stats.values()
    )

    if has_agent_breakdown:
        console.print("[bold magenta]Agent Breakdown:[/bold magenta]")
        table = Table(show_header=True, header_style="bold cyan", box=ROUNDED)
        table.add_column("Agent", style="cyan", no_wrap=True)

        # Add kit columns
        for kit_key in kit_stats.keys():
            table.add_column(format_kit_name(kit_key), justify="right")

        # Add Total column if multiple kits
        show_total = len(kit_stats) > 1
        if show_total:
            table.add_column("Total", justify="right")

        # Add rows (only agents with non-zero values)
        agent_labels = {
            "agent_claude": "Claude Code",
            "agent_copilot": "GitHub Copilot",
            "agent_shared": "Shared"
        }

        for cat in agent_categories:
            values = [kit_stats[kit_key].get(cat, 0) for kit_key in kit_stats.keys()]
            if sum(values) > 0:  # Only show row if at least one kit has files for this agent
                styled_values = [style_value(v, not is_removal, has_modified_files) for v in values]
                row = [agent_labels[cat]] + styled_values
                if show_total:
                    row.append(style_value(sum(values), not is_removal, has_modified_files))
                table.add_row(*row)

        console.print(table)
        console.print()

    # Kit contents table (Commands, Scripts, Memory, Templates)
    file_type_categories = ["commands", "scripts", "memory", "templates"]
    has_file_types = any(
        any(stats.get(cat, 0) > 0 for cat in file_type_categories)
        for stats in kit_stats.values()
    )

    if has_file_types:
        console.print("[bold magenta]Kit Contents:[/bold magenta]")
        table = Table(show_header=True, header_style="bold cyan", box=ROUNDED)
        table.add_column("Type", style="cyan", no_wrap=True)

        # Add kit columns (only kits that have file types)
        active_kits = [
            kit_key for kit_key in kit_stats.keys()
            if any(kit_stats[kit_key].get(cat, 0) > 0 for cat in file_type_categories)
        ]

        for kit_key in active_kits:
            table.add_column(format_kit_name(kit_key), justify="right")

        # Add Total column if multiple kits
        show_total = len(active_kits) > 1
        if show_total:
            table.add_column("Total", justify="right")

        # Add rows (only categories with non-zero values)
        for cat in file_type_categories:
            values = [kit_stats[kit_key].get(cat, 0) for kit_key in active_kits]
            if sum(values) > 0:  # Only show row if at least one kit has this type
                styled_values = [style_value(v, not is_removal, has_modified_files) for v in values]
                row = [cat.capitalize()] + styled_values
                if show_total:
                    row.append(style_value(sum(values), not is_removal, has_modified_files))
                table.add_row(*row)

        console.print(table)
        console.print()

    # Totals table (Files and Directories)
    console.print("[bold magenta]File Totals:[/bold magenta]")
    table = Table(show_header=True, header_style="bold cyan", box=ROUNDED)
    table.add_column("Category", style="cyan", no_wrap=True)

    # Add kit columns
    for kit_key in kit_stats.keys():
        table.add_column(format_kit_name(kit_key), justify="right")

    # Add Total column if multiple kits
    show_total = len(kit_stats) > 1
    if show_total:
        table.add_column("Total", justify="right")

    # Add rows (only if totals > 0)
    for cat in ["files", "directories"]:
        values = [kit_stats[kit_key].get(cat, 0) for kit_key in kit_stats.keys()]
        if sum(values) > 0:
            styled_values = [style_value(v, not is_removal, has_modified_files) for v in values]
            row = [cat.capitalize()] + styled_values
            if show_total:
                row.append(style_value(sum(values), not is_removal, has_modified_files))
            table.add_row(*row)

    console.print(table)
    console.print()

def _display_installation_summary(result: dict, verbose: bool = False):
    """Display kit addition summary.

    Args:
        result: Install result dict with 'installed' and 'skipped' lists
        verbose: If True, show full file list; if False, show only count
    """
    installed = result.get("installed", [])
    skipped = result.get("skipped", [])

    if verbose and installed:
        console.print("[bold]\nInstalled files:[/bold]")
        for item in installed:
            # Normalize to backslashes for Windows display
            display_path = str(item).replace("/", "\\")
            console.print(f"  [green]+[/green] {display_path}")

    if verbose and skipped:
        console.print("\n[bold]Skipped (already exists):[/bold]")
        for item in skipped:
            # Normalize to backslashes for Windows display
            display_path = str(item).replace("/", "\\")
            console.print(f"  [dim]-[/dim] {display_path}")

    # Summary count (always show)
    if not verbose:
        if installed:
            console.print(f"\nInstalled {len(installed)} files")
        if skipped:
            console.print(f"Skipped {len(skipped)} files (already exist)")

    console.print("\n[bold cyan]Next steps:[/bold cyan]")
    console.print(f"  1. Run: /orient (in GitHub Copilot or Claude Code)")
    console.print(r"  2. Check: .github\prompts\orient.prompt.md or .claude\commands\orient.md")
    console.print(f"  3. Validate: {APP_NAME} validate")
    console.print("\n[dim]Note: Commands are markdown prompt files that work with any compatible AI assistant.[/dim]")
    console.print()

def _display_removal_summary(result: dict, verbose: bool = False):
    """Display kit removal summary.

    Args:
        result: Removal result dict with 'removed' list of kit dicts
        verbose: If True, show full file list; if False, show only count
    """
    # Flatten all removed files from all kits
    all_removed = []
    for kit_result in result.get("removed", []):
        all_removed.extend(kit_result.get("files", []))

    if verbose and all_removed:
        console.print("\n[bold]Removed files:[/bold]")
        for item in all_removed:
            # Normalize to backslashes for Windows display
            display_path = str(item).replace("/", "\\")
            console.print(f"  [red]-[/red] {display_path}")

    # Summary count (always show)
    if not verbose and all_removed:
        console.print(f"\nRemoved {len(all_removed)} files")

def _display_validation_results(validation_result: dict):
    """Display validation results in a user-friendly format.

    Args:
        validation_result: Dict with 'valid' (bool) and 'checks' (dict of kit results)
    """
    checks = validation_result.get("checks", {})

    for kit_name, result in checks.items():
        status = result.get("status", "unknown")

        if status == "installed":
            console.print(f"[green][OK] {kit_name}[/green]")
        elif status == "not_installed":
            console.print(f"[dim][-] {kit_name} (not installed)[/dim]")
        elif status == "partial":
            console.print(f"[yellow][!] {kit_name} (partial - some files missing)[/yellow]")
            missing = result.get("missing_files", [])
            if missing:
                console.print(f"[dim]  Missing files: {', '.join(missing[:3])}" + (" ..." if len(missing) > 3 else "") + "[/dim]")
        else:
            console.print(f"[red][X] {kit_name} ({status})[/red]")

def _cleanup_empty_directories(target_dir: Path):
    """Clean up empty directories created by lite-kits."""
    directories_to_check = [
        DIR_CLAUDE_COMMANDS,
        DIR_GITHUB_PROMPTS,
        DIR_SPECIFY_MEMORY,
        DIR_SPECIFY_SCRIPTS_BASH,
        DIR_SPECIFY_SCRIPTS_POWERSHELL,
        DIR_SPECIFY_TEMPLATES,
    ]

    cleaned = []
    for dir_path in directories_to_check:
        full_path = target_dir / dir_path
        if full_path.exists() and full_path.is_dir():
            # Check if directory is empty (no files or subdirs)
            try:
                if not any(full_path.iterdir()):
                    full_path.rmdir()
                    cleaned.append(dir_path)
            except OSError:
                # Directory not empty or permission error, skip
                pass

    if cleaned:
        console.print(f"\nCleaned up empty directories: [dim]{', '.join(cleaned)}[/dim]")

@app.command(name="info")
def package_info():
    """Show package information and available kits.

    Displays:
    - Package version and repository
    - Available kits (dev, multiagent)
    - Kit descriptions and commands
    - Package management commands
    """
    # Package info (banner removed to avoid duplication with --banner flag)
    console.print()
    console.print("[bold]Info:[/bold]")
    info_table = Table(show_header=False, box=None, padding=(0, 2))
    info_table.add_column("Key", style="cyan")
    info_table.add_column("Value")

    info_table.add_row("Version", __version__)
    info_table.add_row("Repository", REPOSITORY_URL)
    info_table.add_row("License", LICENSE)

    console.print(info_table)
    console.print()

    # Available kits
    console.print("[bold]Available Kits:[/bold]")
    kits_table = Table(show_header=False, box=None, padding=(0, 2))
    kits_table.add_column("Kit", style="cyan")
    kits_table.add_column("Description")

    kits_table.add_row(KIT_DEV, KIT_DESC_DEV)
    kits_table.add_row(KIT_MULTIAGENT, KIT_DESC_MULTIAGENT)

    console.print(kits_table)
    console.print()

    # Package management
    console.print("[bold]Package Management:[/bold]")
    package_table = Table(show_header=False, box=None, padding=(0, 2))
    package_table.add_column("Action", style="cyan")
    package_table.add_column("Command")
    
    package_table.add_row("Update", f"[dim]uv tool install --upgrade {APP_NAME}[/dim]")
    package_table.add_row("Uninstall", f"[dim]uv tool uninstall {APP_NAME}[/dim]")
    
    console.print(package_table)
    console.print()

@app.command(name="uninstall")
def package_uninstall():
    """Instructions for uninstalling the lite-kits package."""
    console.print()
    console.print(f"[bold yellow]Uninstall {APP_NAME}[/bold yellow]\n")

    console.print("To uninstall the package, run:\n")
    console.print(f"  [cyan]uv tool uninstall {APP_NAME}[/cyan]\n")

    console.print("[dim]Or with pip:[/dim]\n")
    console.print(f"  [dim]pip uninstall {APP_NAME}[/dim]\n")

    console.print("[bold]Note:[/bold] This will remove the package but NOT the kits you've added to projects.")
    console.print(f"To remove kits from a project, first run: [cyan]{APP_NAME} remove --all[/cyan]\n")

@app.command(name="help")
def show_help(
    ctx: typer.Context,
    command_name: Optional[str] = typer.Argument(
        None,
        help="Command to get help for (e.g., 'add', 'remove')",
    ),
):
    """Show help and available commands.

    Usage:
        lite-kits help           # Show general help
        lite-kits help add       # Show help for 'add' command
    """
    if command_name:
        # Show help for specific command by invoking it with --help
        import sys
        sys.argv = [APP_NAME, command_name, "--help"]
        try:
            app()
        except SystemExit:
            pass
    else:
        # Show general help
        console.print(ctx.parent.get_help())
    raise typer.Exit(0)

@app.command(name="banner", hidden=True)
def show_banner():
    """Show the lite-kits banner (hidden easter egg command)."""
    diagonal_reveal_banner()

if __name__ == "__main__":
    app()
