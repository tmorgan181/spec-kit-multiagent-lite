#!/usr/bin/env python3
"""
CLI for spec-kit-multiagent

Provides commands to add/remove multiagent coordination features to spec-kit projects.
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
    name="speckit-ma",
    help="Lightweight multi-agent coordination add-on for GitHub spec-kit",
    no_args_is_help=True,
)
console = Console()


def version_callback(value: bool):
    """Print version and exit."""
    if value:
        console.print(f"spec-kit-multiagent version {__version__}")
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
    """spec-kit-multiagent: Multi-agent coordination for spec-kit projects."""
    pass


@app.command()
def add(
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
    target: Optional[Path] = typer.Argument(
        None,
        help="Target directory (defaults to current directory)",
    ),
):
    """
    Add multiagent coordination features to a spec-kit project.

    This command installs:
    - /orient command for agent orientation
    - Collaboration directory structure
    - Git workflow guides (PR, worktrees)
    - Multi-agent sections in constitution

    Example:
        speckit-ma add --here --dry-run  # Preview changes
        speckit-ma add --here             # Install features
    """
    if not here and target is None:
        console.print(
            "[red]Error:[/red] Either --here or a target directory must be specified",
            style="bold",
        )
        raise typer.Exit(1)

    target_dir = Path.cwd() if here else target
    installer = Installer(target_dir)

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
            "[yellow]Warning:[/yellow] Multiagent features appear to be already installed",
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
        console.print(f"\n[bold green]Installing multiagent features to {target_dir}[/bold green]\n")

        with console.status("[bold green]Installing..."):
            result = installer.install()

        if result["success"]:
            console.print("\n[bold green]✓ Installation complete![/bold green]\n")
            _display_installation_summary(result)
        else:
            console.print(f"\n[bold red]✗ Installation failed:[/bold red] {result['error']}\n")
            raise typer.Exit(1)


@app.command()
def remove(
    here: bool = typer.Option(
        False,
        "--here",
        help="Remove from current directory",
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
    """
    Remove multiagent coordination features from a spec-kit project.

    Returns the project to vanilla spec-kit state.

    Example:
        speckit-ma remove --here --dry-run  # Preview changes
        speckit-ma remove --here             # Remove features
    """
    # TODO: Implement removal logic
    console.print("[yellow]Note:[/yellow] Remove command not yet implemented", style="bold")
    console.print("\nPlaceholder: Would remove multiagent features from project", style="dim")
    raise typer.Exit(0)


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
    Validate multiagent coordination structure.

    Checks:
    - Collaboration directory structure
    - Required files present
    - Constitution consistency
    - Command synchronization

    Example:
        speckit-ma validate --here
    """
    target_dir = Path.cwd() if here else target
    installer = Installer(target_dir)

    console.print(f"\n[bold cyan]Validating {target_dir}[/bold cyan]\n")

    # Check if it's a spec-kit project
    if not installer.is_spec_kit_project():
        console.print("[red]✗ Not a spec-kit project[/red]")
        raise typer.Exit(1)

    # Check if multiagent is installed
    if not installer.is_multiagent_installed():
        console.print("[yellow]⚠ Multiagent features not installed[/yellow]")
        console.print("  Run: speckit-ma add --here", style="dim")
        raise typer.Exit(1)

    # Validate structure
    with console.status("[bold cyan]Validating..."):
        validation_result = installer.validate()

    _display_validation_results(validation_result)

    if validation_result["valid"]:
        console.print("\n[bold green]✓ Validation passed![/bold green]")
        raise typer.Exit(0)
    else:
        console.print("\n[bold red]✗ Validation failed[/bold red]")
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
    Show coordination status for the project.

    Displays:
    - Installation status
    - Active collaboration directories
    - Recent coordination activity
    - Agent attribution

    Example:
        speckit-ma status --here
    """
    target_dir = Path.cwd() if here else target
    installer = Installer(target_dir)

    console.print(f"\n[bold cyan]Project Status: {target_dir}[/bold cyan]\n")

    # Basic checks
    is_spec_kit = installer.is_spec_kit_project()
    is_multiagent = installer.is_multiagent_installed()

    table = Table(show_header=False, box=None)
    table.add_column("Item", style="cyan")
    table.add_column("Status")

    table.add_row("Spec-kit project", "✓" if is_spec_kit else "✗")
    table.add_row("Multiagent installed", "✓" if is_multiagent else "✗")

    console.print(table)
    console.print()

    # TODO: Add more status information
    # - Active collaboration directories
    # - Recent sessions
    # - Agent attribution from git log


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
        console.print(f"  ✓ {item}")

    console.print("\n[bold cyan]Next steps:[/bold cyan]")
    console.print("  1. Run: /orient (in your AI assistant)")
    console.print("  2. Check: .claude/commands/orient.md or .github/prompts/orient.prompt.md")
    console.print("  3. Validate: speckit-ma validate --here")


def _display_validation_results(result: dict):
    """Display validation results."""
    for check_name, check_result in result.get("checks", {}).items():
        status = "✓" if check_result["passed"] else "✗"
        color = "green" if check_result["passed"] else "red"
        console.print(f"[{color}]{status}[/{color}] {check_name}")

        if not check_result["passed"] and "message" in check_result:
            console.print(f"  {check_result['message']}", style="dim")


if __name__ == "__main__":
    app()
