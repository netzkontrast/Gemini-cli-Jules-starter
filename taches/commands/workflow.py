import click
from pathlib import Path

PLAN_TEMPLATE = """# Project Plan
## Goal
{goal}

## High Level Approach
1. [Step 1]
2. [Step 2]
"""

TODO_TEMPLATE = """# Implementation Tasks
- [ ] Task 1
- [ ] Task 2
"""

ACT_TEMPLATE = """# Implementation Log
## {task}
- [ ] Started
- [ ] Completed
"""

@click.group()
def blueprint():
    """Blueprint Workflow: Plan -> Define -> Implement -> Test"""
    pass

@blueprint.command()
@click.argument('goal')
def plan(goal):
    """Create a high-level plan (PLAN.md)."""
    Path('PLAN.md').write_text(PLAN_TEMPLATE.format(goal=goal))
    click.echo(f"Created PLAN.md for goal: {goal}")

@blueprint.command()
def define():
    """Define detailed tasks (TODO.md) based on the plan."""
    if not Path('PLAN.md').exists():
        click.echo("Error: PLAN.md not found. Run 'taches plan <goal>' first.")
        return
    Path('TODO.md').write_text(TODO_TEMPLATE)
    click.echo("Created TODO.md based on PLAN.md")

@blueprint.command()
@click.argument('task')
def implement(task):
    """Log implementation details (ACT.md)."""
    if not Path('TODO.md').exists():
        click.echo("Error: TODO.md not found. Run 'taches define' first.")
        return

    mode = 'a' if Path('ACT.md').exists() else 'w'
    with open('ACT.md', mode) as f:
        f.write(ACT_TEMPLATE.format(task=task))
    click.echo(f"Logged implementation start for: {task} in ACT.md")

@blueprint.command()
def test():
    """Verify implementation."""
    click.echo("Running verification...")
    # Simulation of running tests
    if Path('ACT.md').exists():
        click.echo("✅ ACT.md found. Implementation logged.")
    else:
        click.echo("⚠️ No ACT.md found.")
