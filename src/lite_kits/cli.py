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

from . import __version__
from .core import diagonal_reveal_banner, show_loading_spinner, show_static_banner, Installer

# Constants
APP_NAME = "lite-kits"
APP_DESCRIPTION = "Quick start: lite-kits add  •  Get help: lite-kits help [COMMAND]"

# Kit names
KIT_DEV = "dev"
KIT_MULTIAGENT = "multiagent"
KITS_ALL = [KIT_DEV, KIT_MULTIAGENT]
KITS_RECOMMENDED = [KIT_DEV]  # dev-kit is the default, multiagent is optional

# Kit descriptions for help
KIT_DESC_DEV = "Solo development essentials: /orient, /commit, /pr, /review, /cleanup, /audit, /stats"
KIT_DESC_MULTIAGENT = "Multi-agent coordination: /sync, collaboration dirs, memory guides (optional)"

# Error messages
ERROR_NOT_SPEC_KIT = "does not appear to be a spec-kit project!"
ERROR_SPEC_KIT_HINT = "Looking for one of: .specify/, .claude/, or .github/prompts/"

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
    console.print(f"  [bold cyan]{APP_NAME} version {__version__}[/bold cyan]\n")

def print_quick_start():
    console.print("[bold]Quick Start:[/bold]")
    console.print(f"  [cyan]1. {APP_NAME} add --recommended[/cyan]  # Add dev-kit (all commands)")
    console.print(f"  [cyan]2. {APP_NAME} status[/cyan]             # Check installation")
    console.print(f"  [cyan]3. {APP_NAME} validate[/cyan]           # Validate kit files\n")

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
        console.print(f"[bold red][X] {target_dir} {ERROR_NOT_SPEC_KIT}[/bold red]")
        console.print(f"{ERROR_SPEC_KIT_HINT}", style="dim")
    console.print()

def version_callback(value: bool):
    """Print version and exit."""
    if value:
        console.print()
        print_version_info()
        console.print()
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
    recommended: bool = typer.Option(
        False,
        "--recommended",
        help=f"Add recommended kits: {' + '.join(KITS_RECOMMENDED)}",
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
    Use --force to skip preview and install immediately.
    """
    target_dir = Path.cwd() if target is None else target

    # Determine which kits to install
    kits = None
    if recommended:
        kits = KITS_RECOMMENDED
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
        console.print()
        console.print(
            f"[red]Error:[/red] {target_dir} {ERROR_NOT_SPEC_KIT}",
            style="bold",
        )
        console.print(
            f"\n{ERROR_SPEC_KIT_HINT}",
            style="dim",
        )
        console.print()
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
        console.print("\n[bold cyan]Preview of changes:[/bold cyan]\n")
        preview = installer.preview_installation()
        _display_changes(preview)

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
        console.print("\n[bold green][OK] Kits installed successfully![/bold green]\n")
        _display_installation_summary(result)
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
        console.print(f"\n[bold yellow]Preview - Removing from {target_dir}[/bold yellow]\n")
        preview = installer.preview_removal()

        if preview["total_files"] == 0:
            console.print("[dim]No files found to remove[/dim]")
            console.print()
            raise typer.Exit(0)

        # Display files grouped by kit
        for kit in preview["kits"]:
            console.print(f"[bold]{kit['name']}:[/bold]")
            for file_path in kit['files']:
                console.print(f"  [red]-[/red] {file_path}")
            console.print()

        console.print(f"[bold]Total files to remove:[/bold] {preview['total_files']}\n")

        # Confirm removal
        if not typer.confirm("Continue with removal?"):
            console.print("[dim]Cancelled[/dim]")
            console.print()
            raise typer.Exit(0)

    # Remove kits
    console.print(f"\n[bold green]Removing files...[/bold green]\n")
    with console.status("[bold yellow]Removing..."):
        result = installer.remove()

    if result["success"]:
        console.print("[green][OK] Removal complete![/green]\n")

        # Show summary
        total_removed = sum(len(item['files']) for item in result["removed"])
        console.print(f"[bold]Removed {total_removed} files[/bold]\n")
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

    console.print(f"\n[bold cyan]Validating {target_dir}[/bold cyan]\n")

    # Check if it's a spec-kit project
    if not installer.is_spec_kit_project():
        console.print()
        console.print("[red][X] Not a spec-kit project[/red]")
        console.print()
        raise typer.Exit(1)

    # Check if any kits are installed
    any_installed = any(installer.is_kit_installed(k) for k in KITS_ALL)
    if not any_installed:
        console.print()
        console.print("[yellow]⚠ No enhancement kits installed[/yellow]")
        console.print(f"  Run: {APP_NAME} add --recommended", style="dim")
        console.print()
        raise typer.Exit(1)

    # Validate structure
    console.print(f"\n[bold cyan]Validating {target_dir}[/bold cyan]\n")
    with console.status("[bold bright_cyan]Validating...", spinner="dots"):
        validation_result = installer.validate()

    console.print("[green][OK] Done![/green]\n")
    _display_validation_results(validation_result)

    if validation_result["valid"]:
        console.print("\n[bold green][OK] Validation passed![/bold green]\n")
        console.print()
        raise typer.Exit(0)
    else:
        console.print("\n[bold red][X] Validation failed[/bold red]\n")
        console.print()
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

def _display_changes(changes: dict):
    """Display preview of changes."""
    # Only show sections that have items
    new_files = changes.get("new_files", [])
    modified_files = changes.get("modified_files", [])
    new_directories = changes.get("new_directories", [])

    if new_files:
        console.print("[bold]Files to be created:[/bold]")
        for file in new_files:
            console.print(f"  [green]+[/green] {file}")
        console.print()  # Blank line after section

    if modified_files:
        console.print("[bold]Files to be modified:[/bold]")
        for file in modified_files:
            console.print(f"  [yellow]~[/yellow] {file}")
        console.print()  # Blank line after section

    if new_directories:
        console.print("[bold]Directories to be created:[/bold]")
        for dir in new_directories:
            console.print(f"  [blue]+[/blue] {dir}")
        console.print()  # Blank line after section

    # Display total file count
    total_files = len(new_files) + len(modified_files)
    if total_files > 0:
        console.print(f"[bold]Total files to install:[/bold] {total_files}")

def _display_installation_summary(result: dict):
    """Display kit addition summary."""
    console.print("[bold]Installed files:[/bold]")
    for item in result.get("installed", []):
        console.print(f"  [green]+[/green] {item}")

    if result.get("skipped"):
        console.print("\n[bold]Skipped (already exists):[/bold]")
        for item in result.get("skipped", []):
            console.print(f"  [dim]-[/dim] {item}")

    console.print("\n[bold cyan]Next steps:[/bold cyan]")
    console.print(f"  1. Run: /orient (in your AI assistant)")
    console.print(f"  2. Check: .claude/commands/orient.md or .github/prompts/orient.prompt.md")
    console.print(f"  3. Validate: {APP_NAME} validate")
    console.print()

def _display_validation_results(result: dict):
    """Display validation results."""
    for check_name, check_result in result.get("checks", {}).items():
        status = "[OK]" if check_result["passed"] else "[X]"
        color = "green" if check_result["passed"] else "red"
        console.print(f"[{color}]{status}[/{color}] {check_name}")

        if not check_result["passed"] and "message" in check_result:
            console.print(f"  {check_result['message']}", style="dim")

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
    info_table.add_row("Repository", "https://github.com/tmorgan181/lite-kits")
    info_table.add_row("License", "MIT")

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
