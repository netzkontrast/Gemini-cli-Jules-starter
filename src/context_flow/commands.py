import os
import click
import shutil
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# Define the package root for template loading
PACKAGE_ROOT = Path(__file__).parent
TEMPLATE_DIR = PACKAGE_ROOT / "templates"

@click.command()
@click.argument("project_name")
def init(project_name):
    """Initialize a new context-flow project."""
    project_path = Path(project_name)

    if project_path.exists():
        click.echo(f"Error: Directory '{project_name}' already exists.")
        return

    # Create directory structure
    click.echo(f"Initializing project '{project_name}'...")
    (project_path / "sessions").mkdir(parents=True)
    (project_path / "thoughts" / "ledgers").mkdir(parents=True)
    (project_path / "thoughts" / "handoffs").mkdir(parents=True)
    (project_path / "skills").mkdir(parents=True)
    (project_path / "agents").mkdir(parents=True)
    (project_path / ".claude").mkdir(parents=True)

    # Initialize Jinja2 environment
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))

    # Generate default skills (The "Specialized Agents" templates)
    skills_dir = project_path / "skills"
    for skill in ["decomposition", "validation", "evaluation"]:
        template = env.get_template(f"skills/{skill}.md.j2")
        content = template.render() # No variables needed for the raw skill definition yet
        with open(skills_dir / f"{skill}.md", "w") as f:
            f.write(content)
        click.echo(f"  Created skill: {skill}")

    # Create a basic configuration file
    config_content = """project_name: {}
model: claude-3-5-sonnet-20241022
""".format(project_name)

    with open(project_path / "context_flow.yaml", "w") as f:
        f.write(config_content)

    click.echo("Project initialized successfully.")
    click.echo(f"Run 'cd {project_name}' and then 'context-flow start \"Your Task\"' to begin.")
