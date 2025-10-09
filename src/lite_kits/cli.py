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
APP_DESCRIPTION = "Lightweight enhancement kits for spec-driven development."

# Kit names
KIT_PROJECT = "project"
KIT_GIT = "git"
KIT_MULTIAGENT = "multiagent"
KITS_ALL = [KIT_PROJECT, KIT_GIT, KIT_MULTIAGENT]
KITS_RECOMMENDED = [KIT_PROJECT, KIT_GIT]

# Kit names and collections

# Kit descriptions for help
KIT_DESC_PROJECT = "Agent orientation and project management features"
KIT_DESC_GIT = "Smart git workflows with AI-powered commit messages"
KIT_DESC_MULTIAGENT = "Multi-agent coordination and collaboration protocols"

# Marker files for kit detection
MARKER_PROJECT_KIT = ".claude/commands/orient.md"
MARKER_GIT_KIT = ".claude/commands/commit.md"
MARKER_MULTIAGENT_KIT = ".specify/memory/pr-workflow-guide.md"

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
    console.print(f"  [cyan]1. {APP_NAME} add --recommended[/cyan]  # Add project + git kits")
    console.print(f"  [cyan]2. {APP_NAME} status[/cyan]             # Check installation")
    console.print(f"  [cyan]3. {APP_NAME} info[/cyan]               # Package details\n")

def print_kit_info(target_dir: Path, is_spec_kit: bool, installed_kits: list):
    """Print kit installation info."""
    console.print()
    if is_spec_kit:
        console.print(f"[bold green][OK] Spec-kit project detected in {target_dir}.[/bold green]\n")
        if installed_kits:
            console.print("Installed kits:", style="bold")
            kit_icons = {
                "project": "🎯",
                "git": "🔧",
                "multiagent": "🤝"
            }
            for kit in installed_kits:
                icon = kit_icons.get(kit, "📦")
                console.print(f"  {icon} {kit}-kit", style="green")
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
        raise typer.Exit()

def banner_callback(value: bool):
    """Show banner + hint and exit."""
    if value:
        diagonal_reveal_banner()
        print_help_hint()
        print_quick_start()
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
        help="Show the lite-kits banner",
        callback=banner_callback,
        is_eager=True,
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
    
    # Show banner + hint and quick-start when no command is given
    if ctx.invoked_subcommand is None:
        show_static_banner()
        print_help_hint()
        print_quick_start()

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
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Preview changes without applying them",
    ),
    target: Optional[Path] = typer.Argument(
        None,
        help="Target directory (defaults to current directory)",
    ),
):
    """Add enhancement kits to a spec-kit project."""
    target_dir = Path.cwd() if target is None else target

    # Determine which kits to install
    kits = None
    if recommended:
        kits = KITS_RECOMMENDED
    elif kit:
        kits = [k.strip() for k in kit.split(',')]
    # else: kits=None will use default [KIT_PROJECT] in Installer

    try:
        installer = Installer(target_dir, kits=kits)
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}", style="bold")
        raise typer.Exit(1)

    # Validate target is a spec-kit project
    if not installer.is_spec_kit_project():
        console.print(
            f"[red]Error:[/red] {target_dir} {ERROR_NOT_SPEC_KIT}",
            style="bold",
        )
        console.print(
            f"\n{ERROR_SPEC_KIT_HINT}",
            style="dim",
        )
        raise typer.Exit(1)

    # Check if already installed
    if installer.is_multiagent_installed():
        console.print(
            "[yellow]Warning:[/yellow] Enhancement kits appear to be already installed",
            style="bold",
        )
        if not typer.confirm("Reinstall anyway?"):
            raise typer.Exit(0)

    # Preview or install
    if dry_run:
        console.print("\n[bold cyan]Dry run - no changes will be made[/bold cyan]\n")
        changes = installer.preview_installation()
        _display_changes(changes)
    else:
        console.print(f"\n[bold green]Adding enhancement kits to {target_dir}[/bold green]\n")

        show_loading_spinner("Adding kits...")
        result = installer.install()

        if result["success"]:
            console.print("\n[bold green][OK] Kits added successfully![/bold green]\n")
            _display_installation_summary(result)
            # Show static banner after successful install
            show_static_banner()
        else:
            console.print(f"\n[bold red][X] Failed to add kits:[/bold red] {result['error']}\n")
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
    target: Optional[Path] = typer.Argument(
        None,
        help="Target directory (defaults to current directory)",
    ),
):
    """Remove enhancement kits from a spec-kit project.

    Returns the project to vanilla spec-kit state.

    Examples:
        lite-kits remove --kit git                # Remove git-kit only
        lite-kits remove --kit project,git        # Remove specific kits
        lite-kits remove --all                    # Remove all kits
    """
    target_dir = Path.cwd() if target is None else target

    # Determine which kits to remove
    kits = None
    if all_kits:
        kits = KITS_ALL
    elif kit:
        kits = [k.strip() for k in kit.split(',')]
    else:
        console.print("[yellow]Error:[/yellow] Specify --kit or --all", style="bold")
        console.print("\nExamples:", style="dim")
        console.print(f"  {APP_NAME} remove --here --kit {KIT_GIT}", style="dim")
        console.print(f"  {APP_NAME} remove --here --all", style="dim")
        raise typer.Exit(1)

    try:
        installer = Installer(target_dir, kits=kits)
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}", style="bold")
        raise typer.Exit(1)

    # Check if kits are installed
    if not installer.is_multiagent_installed():
        console.print("[yellow]Warning:[/yellow] No kits detected to remove", style="bold")
        raise typer.Exit(0)

    # Confirm removal
    console.print(f"\n[bold yellow]Remove kits from {target_dir}[/bold yellow]")
    console.print(f"Kits to remove: {', '.join(kits)}\n")

    if not typer.confirm("Continue with removal?"):
        console.print("Cancelled")
        raise typer.Exit(0)

    # Remove kits
    console.print("\n[bold]Removing kits...[/bold]\n")
    with console.status("[bold yellow]Removing..."):
        result = installer.remove()

    if result["success"]:
        console.print("[bold green]Removal complete![/bold green]\n")
        if result["removed"]:
            console.print("[bold]Removed:[/bold]")
            for item in result["removed"]:
                console.print(f"  - {item}")
        else:
            console.print("[dim]No files found to remove[/dim]")
    else:
        console.print(f"\n[bold red]Removal failed:[/bold red] {result['error']}\n")
        raise typer.Exit(1)

@app.command()
def validate(
    target: Optional[Path] = typer.Argument(
        None,
        help="Target directory (defaults to current directory)",
    ),
):
    """Validate enhancement kit installation.

    Checks:
    - Kit files are present and correctly installed
    - Collaboration directory structure (if multiagent-kit installed)  
    - Required files present
    - Cross-kit consistency

    Example:
        lite-kits validate
    """
    target_dir = Path.cwd() if target is None else target

    # For validation, we don't know which kits are installed yet, so check for all
    installer = Installer(target_dir, kits=KITS_ALL)

    console.print(f"\n[bold cyan]Validating {target_dir}[/bold cyan]\n")

    # Check if it's a spec-kit project
    if not installer.is_spec_kit_project():
        console.print("[red][X] Not a spec-kit project[/red]")
        raise typer.Exit(1)

    # Check if any kits are installed
    if not installer.is_multiagent_installed():
        console.print("[yellow]⚠ No enhancement kits installed[/yellow]")
        console.print(f"  Run: {APP_NAME} add --here --recommended", style="dim")
        raise typer.Exit(1)

    # Validate structure
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
    """Show enhancement kit installation status for the project.

    Displays:
    - Spec-kit project detection
    - Installed kits  
    - Installation health

    Example:
        lite-kits status
    """
    target_dir = Path.cwd() if target is None else target

    # For status, check for all possible kits
    installer = Installer(target_dir, kits=KITS_ALL)

    # Basic checks
    is_spec_kit = installer.is_spec_kit_project()

    # Check individual kits
    project_kit_installed = (target_dir / MARKER_PROJECT_KIT).exists()
    git_kit_installed = (target_dir / MARKER_GIT_KIT).exists()
    multiagent_kit_installed = (target_dir / MARKER_MULTIAGENT_KIT).exists()

    # Build list of installed kits for banner
    installed_kits = []
    if project_kit_installed:
        installed_kits.append("project")
    if git_kit_installed:
        installed_kits.append("git")
    if multiagent_kit_installed:
        installed_kits.append("multiagent")

    # Show banner + kit info
    show_static_banner()
    print_kit_info(target_dir, is_spec_kit, installed_kits)

def _display_changes(changes: dict):
    """Display preview of changes."""
    console.print("[bold]Files to be created:[/bold]")
    for file in changes.get("new_files", []):
        console.print(f"  [green]+[/green] {file}")

    console.print("\n[bold]Files to be modified:[/bold]")
    for file in changes.get("modified_files", []):
        console.print(f"  [yellow]~[/yellow] {file}")

    console.print("\n[bold]Directories to be created:[/bold]")
    for dir in changes.get("new_directories", []):
        console.print(f"  [blue]+[/blue] {dir}")

def _display_installation_summary(result: dict):
    """Display kit addition summary."""
    console.print("[bold]Added:[/bold]")
    for item in result.get("installed", []):
        console.print(f"  [OK] {item}")

    console.print("\n[bold cyan]Next steps:[/bold cyan]")
    console.print(f"  1. Run: /orient (in your AI assistant)")
    console.print(f"  2. Check: {MARKER_PROJECT_KIT} or .github/prompts/orient.prompt.md")
    console.print(f"  3. Validate: {APP_NAME} validate")

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
    """Show package information and installation details."""
    # Show the static banner for visual appeal
    show_static_banner()
    console.print()

    # Package info
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
    
    kits_table.add_row(KIT_PROJECT, KIT_DESC_PROJECT)
    kits_table.add_row(KIT_GIT, KIT_DESC_GIT)
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
    console.print(f"\n[bold yellow]Uninstall {APP_NAME}[/bold yellow]\n")

    console.print("To uninstall the package, run:\n")
    console.print(f"  [cyan]uv tool uninstall {APP_NAME}[/cyan]\n")

    console.print("[dim]Or with pip:[/dim]\n")
    console.print(f"  [dim]pip uninstall {APP_NAME}[/dim]\n")

    console.print("[bold]Note:[/bold] This will remove the package but NOT the kits you've added to projects.")
    console.print(f"To remove kits from a project, first run: [cyan]{APP_NAME} remove --all[/cyan]\n")

@app.command(name="banner", hidden=True)
def show_banner():
    """Show the lite-kits banner (hidden easter egg command)."""
    diagonal_reveal_banner()

if __name__ == "__main__":
    app()
