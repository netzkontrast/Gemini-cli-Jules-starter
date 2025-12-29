import click
from context_flow.commands import init
from context_flow.start_command import start
from context_flow.engine import ContextEngine

@click.group()
def cli():
    """Context Flow CLI: Setup and manage optimized mdflow environments."""
    pass

@click.command()
@click.argument("name")
@click.argument("arguments", required=False, default="")
def run_command(name, arguments):
    """Executes a command (e.g., sdd:01-specify)."""
    engine = ContextEngine()
    try:
        result = engine.execute("command", name, arguments)
        click.echo(result)
    except Exception as e:
        click.echo(f"Error executing command: {e}")

@click.command()
@click.argument("name")
@click.argument("arguments", required=False, default="")
def run_skill(name, arguments):
    """Executes a skill (e.g., create-plans)."""
    engine = ContextEngine()
    try:
        result = engine.execute("skill", name, arguments)
        click.echo(result)
    except Exception as e:
        click.echo(f"Error executing skill: {e}")

cli.add_command(init)
cli.add_command(start)
cli.add_command(run_command)
cli.add_command(run_skill)

if __name__ == "__main__":
    cli()
