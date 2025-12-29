import click
from taches.commands.consider import consider
from taches.commands.workflow import blueprint

@click.group()
def cli():
    """Taches CLI: Blueprint Workflow & Thinking Models for Gemini."""
    pass

cli.add_command(consider)
cli.add_command(blueprint)

if __name__ == '__main__':
    cli()
