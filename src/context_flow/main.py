import click
from context_flow.commands import init
from context_flow.start_command import start

@click.group()
def cli():
    """Context Flow CLI: Setup and manage optimized mdflow environments."""
    pass

cli.add_command(init)
cli.add_command(start)

if __name__ == "__main__":
    cli()
