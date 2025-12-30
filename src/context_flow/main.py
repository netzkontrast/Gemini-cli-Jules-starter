import click
import sys
from context_flow.commands import init
from context_flow.start_command import start
from context_flow.engine import ContextEngine

@click.group()
def cli():
    """Context Flow CLI: Setup and manage optimized mdflow environments."""
    pass

def _run_command_logic(name, arguments):
    """Shared logic for running a command."""
    engine = ContextEngine()
    try:
        click.secho(f"🚀 Executing command: {name}...", fg="blue", bold=True)
        result = engine.execute("command", name, arguments)
        click.secho(f"✅ Success! Output:", fg="green", bold=True)
        click.echo("---------------------------------------------------")
        click.echo(result)
        click.echo("---------------------------------------------------")
    except Exception as e:
        click.secho(f"❌ Error executing command: {e}", fg="red", bold=True)
        sys.exit(1)

def _run_skill_logic(name, arguments):
    """Shared logic for running a skill."""
    engine = ContextEngine()
    try:
        click.secho(f"🧠 Activating skill: {name}...", fg="magenta", bold=True)
        result = engine.execute("skill", name, arguments)
        click.secho(f"✅ Skill executed successfully! Output:", fg="green", bold=True)
        click.echo("---------------------------------------------------")
        click.echo(result)
        click.echo("---------------------------------------------------")
    except Exception as e:
        click.secho(f"❌ Error executing skill: {e}", fg="red", bold=True)
        sys.exit(1)

@click.command(name="run-command")
@click.argument("name")
@click.argument("arguments", required=False, default="")
def run_command(name, arguments):
    """Executes a command (e.g., sdd:01-specify)."""
    _run_command_logic(name, arguments)

@click.command(name="run-skill")
@click.argument("name")
@click.argument("arguments", required=False, default="")
def run_skill(name, arguments):
    """Executes a skill (e.g., create-plans)."""
    _run_skill_logic(name, arguments)

# Backward compatibility alias
@click.command(name="run_command", hidden=True)
@click.argument("name")
@click.argument("arguments", required=False, default="")
def run_command_alias(name, arguments):
    """Alias for run-command."""
    _run_command_logic(name, arguments)

@click.command(name="run_skill", hidden=True)
@click.argument("name")
@click.argument("arguments", required=False, default="")
def run_skill_alias(name, arguments):
    """Alias for run-skill."""
    _run_skill_logic(name, arguments)


cli.add_command(init)
cli.add_command(start)
cli.add_command(run_command)
cli.add_command(run_skill)
cli.add_command(run_command_alias)
cli.add_command(run_skill_alias)

if __name__ == "__main__":
    cli()
