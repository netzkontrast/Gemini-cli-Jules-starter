import click
from taches.commands.consider import consider
from taches.skills.create_plans import plan

@click.group()
def cli():
    """Taches CLI: A collection of Claude Code resources simulated for Gemini."""
    pass

cli.add_command(consider)
cli.add_command(plan)

if __name__ == '__main__':
    cli()
