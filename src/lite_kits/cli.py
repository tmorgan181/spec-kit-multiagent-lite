#!/usr/bin/env python3
"""
CLI for lite-kits

Provides commands to add/remove enhancement kits for vanilla dev tools.
"""

import sys
from pathlib import Path
from typing import Optional

import typer
from rich.console import Console
from rich.panel import Panel
from rich.table import Table

from . import __version__
from .installer import Installer

app = typer.Typer(
    name="lite-kits",
    help="Lightweight enhancement kits for vanilla dev tools\n\n[dim]Tip: Run 'lite-kits COMMAND --help' for detailed help on each command[/dim]",
    no_args_is_help=True,
    add_completion=False,  # Disable shell completion to avoid modifying user profiles
    rich_markup_mode="rich",
)
console = Console()


def version_callback(value: bool):
    """Print version and exit."""
    if value:
        console.print(f"lite-kits version {__version__}")
        raise typer.Exit()


@app.callback()
def main(
    version: Optional[bool] = typer.Option(
        None,
        "--version",
        "-v",
        help="Show version and exit",
        callback=version_callback,
        is_eager=True,
    ),
):
    """lite-kits: Lightweight enhancement kits for vanilla dev tools."""
    pass


@app.command()
def install(
    here: bool = typer.Option(
        False,
        "--here",
        help="Install in current directory",
    ),
    dry_run: bool = typer.Option(
        False,
        "--dry-run",
        help="Preview changes without applying them",
    ),
    kit: Optional[str] = typer.Option(
        None,
        "--kit",
        help="Comma-separated list of kits to install: project,git,multiagent (default: project)",
    ),
    recommended: bool = typer.Option(
        False,
        "--recommended",
        help="Install recommended kits: project + git",
    ),
    target: Optional[Path] = typer.Argument(
        None,
        help="Target directory (defaults to current directory)",
    ),
):
    """
    Install enhancement kits to a spec-kit project.

    Available kits:
    - project: /orient command, project orientation features
    - git: /commit, /pr, /cleanup commands with smart workflows
    - multiagent: /sync, collaboration directories, memory guides

    Examples:
        lite-kits install --here --kit project           # Install project kit only
        lite-kits install --here --recommended           # Install project + git kits
        lite-kits install --here --kit multiagent        # Install all kits (auto-includes deps)
        lite-kits install --here --dry-run --recommended # Preview changes
    """
    if not here and target is None:
        console.print(
            "[red]Error:[/red] Either --here or a target directory must be specified",
            style="bold",
        )
        raise typer.Exit(1)

    target_dir = Path.cwd() if here else target

    # Determine which kits to install
    kits = None
    if recommended:
        kits = ['project', 'git']
    elif kit:
        kits = [k.strip() for k in kit.split(',')]
    # else: kits=None will use default ['project'] in Installer

    try:
        installer = Installer(target_dir, kits=kits)
    except ValueError as e:
        console.print(f"[red]Error:[/red] {e}", style="bold")
        raise typer.Exit(1)

    # Validate target is a spec-kit project
    if not installer.is_spec_kit_project():
        console.print(
            f"[red]Error:[/red] {target_dir} does not appear to be a spec-kit project",
            style="bold",
        )
        console.print(
            "\nLooking for one of: .specify/, .claude/, or .github/prompts/",
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
        console.print(f"\n[bold green]Installing enhancement kits to {target_dir}[/bold green]\n")

        with console.status("[bold green]Installing..."):
            result = installer.install()

        if result["success"]:
            console.print("\n[bold green][OK] Installation complete![/bold green]\n")
            _display_installation_summary(result)
        else:
            console.print(f"\n[bold red][X] Installation failed:[/bold red] {result['error']}\n")
            raise typer.Exit(1)


@app.command()
def remove(
    here: bool = typer.Option(
        False,
        "--here",
        help="Remove from current directory",
    ),
    kit: Optional[str] = typer.Option(
        None,
        "--kit",
        help="Comma-separated list of kits to remove: project,git,multiagent",
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
    """
    Remove enhancement kits from a spec-kit project.

    Returns the project to vanilla spec-kit state.

    Examples:
        lite-kits remove --here --kit git                # Remove git-kit only
        lite-kits remove --here --kit project,git        # Remove specific kits
        lite-kits remove --here --all                    # Remove all kits
    """
    if not here and target is None:
        console.print(
            "[red]Error:[/red] Either --here or a target directory must be specified",
            style="bold",
        )
        raise typer.Exit(1)

    target_dir = Path.cwd() if here else target

    # Determine which kits to remove
    kits = None
    if all_kits:
        kits = ['project', 'git', 'multiagent']
    elif kit:
        kits = [k.strip() for k in kit.split(',')]
    else:
        console.print("[yellow]Error:[/yellow] Specify --kit or --all", style="bold")
        console.print("\nExamples:", style="dim")
        console.print("  lite-kits remove --here --kit git", style="dim")
        console.print("  lite-kits remove --here --all", style="dim")
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
    here: bool = typer.Option(
        True,
        "--here",
        help="Validate current directory",
    ),
    target: Optional[Path] = typer.Argument(
        None,
        help="Target directory (defaults to current directory)",
    ),
):
    """
    Validate enhancement kit installation.

    Checks:
    - Kit files are present and correctly installed
    - Collaboration directory structure (if multiagent-kit installed)
    - Required files present
    - Cross-kit consistency

    Example:
        lite-kits validate --here
    """
    target_dir = Path.cwd() if here else target

    # For validation, we don't know which kits are installed yet, so check for all
    installer = Installer(target_dir, kits=['project', 'git', 'multiagent'])

    console.print(f"\n[bold cyan]Validating {target_dir}[/bold cyan]\n")

    # Check if it's a spec-kit project
    if not installer.is_spec_kit_project():
        console.print("[red][X] Not a spec-kit project[/red]")
        raise typer.Exit(1)

    # Check if any kits are installed
    if not installer.is_multiagent_installed():
        console.print("[yellow]⚠ No enhancement kits installed[/yellow]")
        console.print("  Run: lite-kits install --here --recommended", style="dim")
        raise typer.Exit(1)

    # Validate structure
    with console.status("[bold cyan]Validating..."):
        validation_result = installer.validate()

    _display_validation_results(validation_result)

    if validation_result["valid"]:
        console.print("\n[bold green][OK] Validation passed![/bold green]")
        raise typer.Exit(0)
    else:
        console.print("\n[bold red][X] Validation failed[/bold red]")
        raise typer.Exit(1)


@app.command()
def status(
    here: bool = typer.Option(
        True,
        "--here",
        help="Check current directory",
    ),
    target: Optional[Path] = typer.Argument(
        None,
        help="Target directory (defaults to current directory)",
    ),
):
    """
    Show enhancement kit installation status for the project.

    Displays:
    - Spec-kit project detection
    - Installed kits
    - Installation health

    Example:
        lite-kits status --here
    """
    target_dir = Path.cwd() if here else target

    # For status, check for all possible kits
    installer = Installer(target_dir, kits=['project', 'git', 'multiagent'])

    console.print(f"\n[bold cyan]Project Status: {target_dir}[/bold cyan]\n")

    # Basic checks
    is_spec_kit = installer.is_spec_kit_project()

    # Check individual kits
    project_kit_installed = (target_dir / ".claude" / "commands" / "orient.md").exists()
    git_kit_installed = (target_dir / ".claude" / "commands" / "commit.md").exists()
    multiagent_kit_installed = (target_dir / ".specify" / "memory" / "pr-workflow-guide.md").exists()

    table = Table(show_header=False, box=None)
    table.add_column("Item", style="cyan")
    table.add_column("Status")

    table.add_row("Spec-kit project", "[green][OK][/green]" if is_spec_kit else "[red][X][/red]")
    table.add_row("project-kit", "[green][OK][/green]" if project_kit_installed else "[dim][--][/dim]")
    table.add_row("git-kit", "[green][OK][/green]" if git_kit_installed else "[dim][--][/dim]")
    table.add_row("multiagent-kit", "[green][OK][/green]" if multiagent_kit_installed else "[dim][--][/dim]")

    console.print(table)
    console.print()


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
    """Display installation summary."""
    console.print("[bold]Installed:[/bold]")
    for item in result.get("installed", []):
        console.print(f"  [OK] {item}")

    console.print("\n[bold cyan]Next steps:[/bold cyan]")
    console.print("  1. Run: /orient (in your AI assistant)")
    console.print("  2. Check: .claude/commands/orient.md or .github/prompts/orient.prompt.md")
    console.print("  3. Validate: lite-kits validate")


def _display_validation_results(result: dict):
    """Display validation results."""
    for check_name, check_result in result.get("checks", {}).items():
        status = "[OK]" if check_result["passed"] else "[X]"
        color = "green" if check_result["passed"] else "red"
        console.print(f"[{color}]{status}[/{color}] {check_name}")

        if not check_result["passed"] and "message" in check_result:
            console.print(f"  {check_result['message']}", style="dim")


if __name__ == "__main__":
    app()
