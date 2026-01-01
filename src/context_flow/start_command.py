import sys
import click
import datetime
from pathlib import Path
from jinja2 import Environment, FileSystemLoader

# Define the package root for template loading
PACKAGE_ROOT = Path(__file__).parent
TEMPLATE_DIR = PACKAGE_ROOT / "templates"

@click.command()
@click.argument("task_description")
def start(task_description):
    """Start a new task session with the Origami Protocol."""

    # Verify we are in a project
    if not Path("context_flow.yaml").exists():
        click.secho("❌ Error: Not a context-flow project. Run 'context-flow init <name>' first.", fg="red", bold=True)
        sys.exit(1)

    click.secho(f"🚀 Starting new task: {task_description}", fg="blue", bold=True)

    # Initialize Jinja2 environment
    env = Environment(loader=FileSystemLoader(str(TEMPLATE_DIR)))

    # 1. Initialize the Ledger
    timestamp = datetime.datetime.now().strftime("%Y-%m-%d_%H-%M-%S")
    session_id = f"session_{timestamp}"
    ledger_path = Path("thoughts/ledgers") / f"{session_id}.md"

    ledger_template = env.get_template("mdflow/ledger.md.j2")
    ledger_content = ledger_template.render(
        session_id=session_id,
        start_time=timestamp,
        current_goal=task_description
    )

    with open(ledger_path, "w") as f:
        f.write(ledger_content)
    click.secho(f"  📒 Initialized Ledger: {ledger_path}", fg="green")

    # 2. Generate the "Origami" Decomposition Prompt
    # This combines the "Decomposition" skill into a prompt that the user runs

    # Load the skill instructions
    decomp_skill_template = env.get_template("skills/decomposition.md.j2")
    # In the prompt generation, we render the skill template with the task details
    instructions = decomp_skill_template.render(task_goal=task_description)

    # Create the executable mdflow prompt
    prompt_template = env.get_template("mdflow/base_prompt.md.j2")
    prompt_content = prompt_template.render(
        task_name="00_origami_decomposition",
        task_goal=f"Decompose the task: {task_description}",
        ledger_path=f"./{ledger_path}",
        instructions=instructions
    )

    session_file = Path("sessions") / "00_origami_decomposition.md"
    with open(session_file, "w") as f:
        f.write(prompt_content)

    click.secho(f"  ✨ Created Session Prompt: {session_file}", fg="green")
    click.echo("\nTo execute this step (if mdflow is installed):")
    click.secho(f"  mdflow {session_file}", fg="yellow", bold=True)
