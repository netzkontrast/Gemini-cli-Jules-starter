import click
import os
from pathlib import Path

PLANNING_DIR = Path('.planning')
PHASES_DIR = PLANNING_DIR / 'phases'

BRIEF_TEMPLATE = """# Project Brief

## Vision
[What are we building and why?]

## Goals
- [Goal 1]
- [Goal 2]
"""

ROADMAP_TEMPLATE = """# Project Roadmap

## Phase 1: Foundation
- [ ] Task 1
- [ ] Task 2

## Phase 2: Implementation
- [ ] Task 1
"""

@click.group()
def plan():
    """Hierarchical planning tools."""
    pass

@plan.command()
def init():
    """Initialize the planning structure (.planning/)."""
    if PLANNING_DIR.exists():
        click.echo("Planning directory already exists.")
        return

    PLANNING_DIR.mkdir()
    PHASES_DIR.mkdir()

    (PLANNING_DIR / 'BRIEF.md').write_text(BRIEF_TEMPLATE)
    (PLANNING_DIR / 'ROADMAP.md').write_text(ROADMAP_TEMPLATE)

    click.echo(f"Initialized planning structure in {PLANNING_DIR}/")
    click.echo("- Created BRIEF.md")
    click.echo("- Created ROADMAP.md")
    click.echo("- Created phases/ directory")

@plan.command()
def status():
    """Check the status of the planning artifacts."""
    if not PLANNING_DIR.exists():
        click.echo("No planning structure found. Run 'taches plan init' to start.")
        return

    click.echo("Planning Status:")

    files = {
        'BRIEF.md': (PLANNING_DIR / 'BRIEF.md').exists(),
        'ROADMAP.md': (PLANNING_DIR / 'ROADMAP.md').exists(),
    }

    for filename, exists in files.items():
        status_icon = "✅" if exists else "❌"
        click.echo(f"{status_icon} {filename}")

    # Check phases
    phases = list(PHASES_DIR.glob('*')) if PHASES_DIR.exists() else []
    if phases:
        click.echo(f"\nFound {len(phases)} phases:")
        for phase in phases:
            click.echo(f"- {phase.name}")
    else:
        click.echo("\nNo phases created yet.")
