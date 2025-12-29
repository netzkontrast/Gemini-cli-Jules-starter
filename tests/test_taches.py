from click.testing import CliRunner
from taches.cli import cli
from taches.commands.consider import PARETO_TEMPLATE
from taches.skills.create_plans import BRIEF_TEMPLATE, ROADMAP_TEMPLATE
import os

def test_consider_pareto():
    runner = CliRunner()
    result = runner.invoke(cli, ['consider', 'pareto', 'testing context'])
    assert result.exit_code == 0
    assert "Apply Pareto's principle to testing context" in result.output
    assert "<output_format>" in result.output

def test_plan_init_and_status():
    runner = CliRunner()
    with runner.isolated_filesystem():
        # Test init
        result = runner.invoke(cli, ['plan', 'init'])
        assert result.exit_code == 0
        assert "Initialized planning structure" in result.output
        assert os.path.exists('.planning/BRIEF.md')
        assert os.path.exists('.planning/ROADMAP.md')
        assert os.path.exists('.planning/phases')

        # Test status
        result = runner.invoke(cli, ['plan', 'status'])
        assert result.exit_code == 0
        assert "✅ BRIEF.md" in result.output
        assert "✅ ROADMAP.md" in result.output
