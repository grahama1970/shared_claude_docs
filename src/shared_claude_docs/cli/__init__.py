"""Command-line interface for Shared Claude Documentation System."""

import click
import os
from pathlib import Path
from rich.console import Console
from rich.table import Table

console = Console()

@click.group()
@click.version_option(version="0.1.0")
def main():
    """Shared Claude Documentation System CLI."""
    pass

@main.command()
def setup():
    """Initialize the documentation system."""
    console.print("[bold green]Setting up Shared Claude Documentation System...[/bold green]")
    
    # Check environment
    if not Path(".env").exists():
        console.print("[yellow]Warning: .env file not found. Creating from template...[/yellow]")
        # Create basic .env if needed
    
    console.print("[green]✓[/green] Setup complete!")

@main.command()
@click.option("--path", "-p", default=".", help="Path to projects directory")
def validate(path):
    """Validate project structure and conventions."""
    console.print(f"[bold]Validating projects in: {path}[/bold]")
    
    # Import validator
    from ..validators import validate_all
    results = validate_all(path)
    
    # Display results
    table = Table(title="Validation Results")
    table.add_column("Project", style="cyan")
    table.add_column("Status", style="green")
    table.add_column("Issues", style="yellow")
    
    for project, result in results.items():
        status = "✓ Pass" if result["valid"] else "✗ Fail"
        issues = len(result.get("issues", []))
        table.add_row(project, status, str(issues))
    
    console.print(table)

@main.command()
@click.option("--source", "-s", help="Source documentation path")
@click.option("--targets", "-t", help="Target projects (comma-separated)")
def sync(source, targets):
    """Synchronize documentation across projects."""
    console.print(f"[bold]Syncing documentation from {source} to {targets}[/bold]")
    
    # Import sync module
    from ..sync import sync_documentation
    sync_documentation(source, targets.split(","))
    
    console.print("[green]✓[/green] Sync complete!")

@main.command()
def list_projects():
    """List all registered projects."""
    experiments_dir = os.getenv("EXPERIMENTS_DIR", "/home/graham/workspace/experiments")
    
    table = Table(title="Claude Projects")
    table.add_column("Project", style="cyan")
    table.add_column("Has CLAUDE.md", style="green")
    table.add_column("Has Tests", style="yellow")
    
    for project_dir in Path(experiments_dir).iterdir():
        if project_dir.is_dir() and not project_dir.name.startswith("."):
            has_claude = (project_dir / "CLAUDE.md").exists()
            has_tests = (project_dir / "tests").exists()
            
            table.add_row(
                project_dir.name,
                "✓" if has_claude else "✗",
                "✓" if has_tests else "✗"
            )
    
    console.print(table)

if __name__ == "__main__":
    main()
